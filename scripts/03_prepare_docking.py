#!/usr/bin/env python3
"""Prepare every structure for docking: convert to PDBQT and generate a Vina config.

For each PDB in data/input/ (the ancestral candidates prot1-8 plus the 6c2u reference,
kept in the loop as a docking sanity check) and every relaxed model in
data/intermediate/relaxed/:
  - ensures a receptor .pdbqt exists in data/intermediate/pdbqt/, converting
    via Meeko's mk_prepare_receptor.py if missing (a matching .pdbqt for the
    ATP ligand is produced once via mk_prepare_ligand.py)
  - computes a docking box (padded bounding box of the CA atoms of the P-loop
    motif residues from 01_identify_motif.py's output)
  - writes a Vina config to data/intermediate/vina_configs/

Requires Meeko (`pip install meeko`), which provides mk_prepare_receptor.py /
mk_prepare_ligand.py on PATH; override with --prepare-receptor-cmd /
--prepare-ligand-cmd if they need to be invoked differently (e.g. via
"python -m meeko.cli.mk_prepare_receptor"). mk_prepare_receptor.py expects a
receptor PDB with realistic protonation already applied -- it does not add
hydrogens itself.
"""
import argparse
import shlex
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np

from paths import (
    INPUT_DIR, RELAXED_DIR, PDBQT_DIR, VINA_CONFIGS_DIR, VINA_POSES_DIR,
    MOTIF_RESIDUES_FILE, LIGAND_SDF, LIGAND_PDBQT, LOGS_DIR, REPO_ROOT, rel,
)
from pdb_utils import ca_coords, bounding_box, load_motif_residues

PADDING = 10.0
EXHAUSTIVENESS = 16
NUM_MODES = 9
ENERGY_RANGE = 4
RECEPTOR_ERROR_LOG = LOGS_DIR / "prepare_docking_errors.log"


def log_error(log_path, pdb_path, cmd, result):
    """Append a failed subprocess's command + stdout/stderr to log_path."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(f"=== {datetime.now().isoformat(timespec='seconds')} {pdb_path.name} ===\n")
        f.write(f"command: {' '.join(cmd)}\n")
        f.write(f"exit code: {result.returncode}\n")
        f.write("--- stdout ---\n")
        f.write(result.stdout or "(empty)")
        f.write("\n--- stderr ---\n")
        f.write(result.stderr or "(empty)")
        f.write("\n\n")


def ensure_receptor_pdbqt(pdb_path, pdbqt_dir, prepare_receptor_cmd, error_log=RECEPTOR_ERROR_LOG):
    out_path = pdbqt_dir / f"{pdb_path.stem}.pdbqt"
    if out_path.exists():
        return out_path
    pdbqt_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Converting {pdb_path.name} -> {out_path.name}")
    # -p/--write_pdbqt takes an optional filename (nargs="*"); without one it
    # defaults to "<output_basename>_rigid.pdbqt" instead, so we pass the
    # exact path we want written rather than relying on -o/--output_basename.
    cmd = shlex.split(prepare_receptor_cmd) + ["-i", rel(pdb_path), "-p", rel(out_path)]
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        log_error(error_log, pdb_path, cmd, result)
        print(
            f"  ERROR: receptor prep failed for {pdb_path.name} "
            f"(exit {result.returncode}) -- logged to {error_log}, skipping"
        )
        return None
    return out_path


def ensure_ligand_pdbqt(sdf_path, out_path, prepare_ligand_cmd):
    if out_path.exists():
        return out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Converting ligand {sdf_path.name} -> {out_path.name}")
    cmd = shlex.split(prepare_ligand_cmd) + ["-i", rel(sdf_path), "-o", rel(out_path)]
    print(f"  Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)
    return out_path


def compute_box(pdb_path, motif_residues, padding):
    coords = []
    for start, end in motif_residues:
        c = ca_coords(pdb_path, start, end)
        if c is None or len(c) == 0:
            print(f"  WARNING: no CA atoms for residues {start}-{end} in {pdb_path.name}")
            continue
        coords.append(c)
    if not coords:
        return None, None
    return bounding_box(np.vstack(coords), padding=padding)


def write_config(config_path, receptor, ligand, center, size, out_pose, exhaustiveness):
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        f"# AutoDock Vina configuration for ATP docking into {receptor.stem}\n"
        f"receptor = {rel(receptor)}\n"
        f"ligand = {rel(ligand)}\n\n"
        f"center_x = {center[0]:.3f}\n"
        f"center_y = {center[1]:.3f}\n"
        f"center_z = {center[2]:.3f}\n\n"
        f"size_x = {size[0]:.3f}\n"
        f"size_y = {size[1]:.3f}\n"
        f"size_z = {size[2]:.3f}\n\n"
        f"out = {rel(out_pose)}\n\n"
        f"exhaustiveness = {exhaustiveness}\n"
        f"num_modes = {NUM_MODES}\n"
        f"energy_range = {ENERGY_RANGE}\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--motif-residues", type=Path, default=MOTIF_RESIDUES_FILE)
    parser.add_argument("--padding", type=float, default=PADDING)
    parser.add_argument("--exhaustiveness", type=int, default=EXHAUSTIVENESS)
    parser.add_argument("--prepare-receptor-cmd", default="mk_prepare_receptor.py")
    parser.add_argument("--prepare-ligand-cmd", default="mk_prepare_ligand.py")
    parser.add_argument(
        "--error-log", type=Path, default=RECEPTOR_ERROR_LOG,
        help="Where failed receptor-prep runs get logged instead of aborting "
             "the whole script (default: %(default)s)",
    )
    args = parser.parse_args()

    if not args.motif_residues.exists():
        raise SystemExit(
            f"{args.motif_residues} not found -- run 01_identify_motif.py first"
        )
    motif_residues = load_motif_residues(args.motif_residues)

    if VINA_CONFIGS_DIR.exists():
        for stale_config in VINA_CONFIGS_DIR.glob("*.txt"):
            stale_config.unlink()

    ligand_pdbqt = ensure_ligand_pdbqt(LIGAND_SDF, LIGAND_PDBQT, args.prepare_ligand_cmd)

    structures = sorted(INPUT_DIR.glob("*.pdb")) + sorted(RELAXED_DIR.glob("*.pdb"))
    print(f"Found {len(structures)} structures to prepare\n")

    for pdb_path in structures:
        
        # if '6c2u' in str(pdb_path.name):
        #     continue

        print(f"Processing {pdb_path.name}")
        receptor_pdbqt = ensure_receptor_pdbqt(
            pdb_path, PDBQT_DIR, args.prepare_receptor_cmd, args.error_log
        )
        if receptor_pdbqt is None or not receptor_pdbqt.exists():
            print(f"  Skipping config -- no receptor .pdbqt for {pdb_path.name}\n")
            continue

        center, size = compute_box(pdb_path, motif_residues, args.padding)
        if center is None:
            print("  ERROR: could not compute a docking box, skipping\n")
            continue
        print(
            f"  Box: center=({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f}) "
            f"size=({size[0]:.2f}, {size[1]:.2f}, {size[2]:.2f})"
        )

        base_name = pdb_path.stem
        config_path = VINA_CONFIGS_DIR / f"{base_name}_config.txt"
        out_pose = VINA_POSES_DIR / f"{base_name}_vina_output.pdbqt"        
        write_config(
            config_path, receptor_pdbqt, ligand_pdbqt, center, size, out_pose,
            args.exhaustiveness,
        )
        print(f"  Config written to {config_path}\n")

    print("Done.")


if __name__ == "__main__":
    main()
