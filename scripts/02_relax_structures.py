#!/usr/bin/env python3
"""Run Rosetta `relax` on each candidate structure in data/input/.

Rosetta isn't installed natively on Windows, so by default this script wraps
the call through WSL (`wsl bash -lc "..."`) and translates Windows paths to
their /mnt/... equivalents via `wslpath`. Use --no-wsl if you're already
running inside a Linux shell that has `relax` on its PATH.

All paths handed to relax are relative to the repo root (with relax run from
that directory), never absolute: Rosetta's option parser splits vector
options like -in:file:s on whitespace in the value regardless of shell
quoting, and this repo's path contains spaces ("OneDrive - Univerzita
Karlova"), which would otherwise get silently torn into bogus file
fragments.

Produces 5 relaxed models per structure plus a score table under
data/intermediate/relaxed/, matching the flags recovered from a previous
crash log (data/intermediate/logs/ROSETTA_CRASH.log):
  -relax:fast -relax:constrain_relax_to_start_coords -relax:coord_constrain_sidechains

If `relax` isn't on PATH inside your WSL environment, pass the full binary
path with --relax-bin, e.g. the one this project used previously:
  --relax-bin /home/<user>/miniconda3/envs/rosetta/bin/relax.cxx11threadserialization.linuxclangrelease
"""
import argparse
import shlex
import subprocess
from pathlib import Path

from paths import INPUT_DIR, RELAXED_DIR, REPO_ROOT, rel

NSTRUCT = 5


def to_wsl_path(path):
    """Convert a Windows path to its WSL-visible equivalent via `wslpath`."""
    result = subprocess.run(
        ["wsl", "wslpath", "-a", str(path)], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def build_command(pdb_path, out_dir, scorefile, relax_bin, nstruct, use_wsl, conda_env):
    """Build the relax invocation using paths relative to REPO_ROOT.

    Rosetta's option parser splits vector-valued options like -in:file:s on
    any whitespace found in the value -- independent of shell quoting, since
    that splitting happens inside Rosetta itself after the shell has already
    handed it a clean argv token. This repo lives under a directory
    containing spaces ("OneDrive - Univerzita Karlova"), so an absolute path
    gets silently torn into bogus file fragments. Using paths relative to
    REPO_ROOT (and cd-ing there first) keeps every value Rosetta sees
    whitespace-free.
    """
    relax_args = [
        relax_bin,
        f"-in:file:s={rel(pdb_path)}",
        f"-out:nstruct={nstruct}",
        "-out:suffix=_relaxed",
        f"-out:path:pdb={rel(out_dir)}/",
        f"-out:file:scorefile={rel(scorefile)}",
        "-relax:fast",
        "-relax:constrain_relax_to_start_coords",
        "-relax:coord_constrain_sidechains",
        "-overwrite"
    ]
    if not use_wsl:
        # No shell involved -- subprocess's own cwd handles the directory
        # change, so relax_args can be passed straight through as argv.
        return relax_args, REPO_ROOT

    relax_cmd = " ".join(shlex.quote(a) for a in relax_args)
    if conda_env:
        relax_cmd = f"conda run -n {shlex.quote(conda_env)} {relax_cmd}"
    repo_root_wsl = to_wsl_path(REPO_ROOT)
    inner = f"cd {shlex.quote(repo_root_wsl)} && {relax_cmd}"
    return ["wsl", "bash", "-lc", inner], None


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "structures", nargs="*", type=Path,
        help="Specific PDB files to relax (default: all data/input/prot*.pdb)",
    )
    parser.add_argument("--relax-bin", default="relax",
                         help="Rosetta relax executable name/path (default: %(default)s)")
    parser.add_argument("--conda-env", default=None,
                         help="Conda environment to run relax in via `conda run -n` (WSL only)")
    parser.add_argument("--no-wsl", action="store_true",
                         help="Invoke relax directly instead of wrapping via `wsl bash -lc`")
    parser.add_argument("--nstruct", type=int, default=NSTRUCT)
    parser.add_argument("--out-dir", type=Path, default=RELAXED_DIR)
    parser.add_argument(
        "--scorefile-name", default="{stem}_score.sc",
        help="Score filename per structure, written into --out-dir; {stem} is the "
             "input PDB's basename without extension (default: %(default)s)",
    )
    args = parser.parse_args()

    structures = args.structures or sorted(INPUT_DIR.glob("prot*.pdb"))
    if not structures:
        raise SystemExit(f"No structures found in {INPUT_DIR}")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    for pdb_path in structures:
        scorefile = args.out_dir / args.scorefile_name.format(stem=pdb_path.stem)
        print(f"Relaxing {pdb_path} -> {args.out_dir}/ ({args.nstruct} models, "
              f"scores -> {scorefile.name})")
        cmd, cwd = build_command(
            pdb_path, args.out_dir, scorefile, args.relax_bin, args.nstruct,
            use_wsl=not args.no_wsl, conda_env=args.conda_env,
        )
        print(f"------RUN-------\n{cmd}\n\n")
        subprocess.run(cmd, check=True, cwd=cwd)


if __name__ == "__main__":
    main()
