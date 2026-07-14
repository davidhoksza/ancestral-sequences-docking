# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Structural pipeline studying whether ancestrally-reconstructed variants of a P-loop
NTPase (`prot1.pdb` … `prot8.pdb`) retain a plausible ATP-binding pocket, using the real
crystal structure `6c2u.pdb` as reference. Two Walker-A P-loop motifs
(`G-x(4)-GK-[T/S]`, residues 9-16 and 62-69 in `6c2u`) are located and used to place the
AutoDock Vina search box for every structure; ATP is then docked into each. Structures are
also refined with Rosetta `relax` and scored, independent of docking.

There is no application code — this is a data-processing pipeline of Python scripts, a
shell script, and Rosetta/Vina inputs/outputs under `data/`.

## Directory layout

`data/` is split by pipeline stage — never write generated files back into `data/input/`:

- `data/input/` — raw, never-modified source structures/ligand: `protN.pdb`, `6c2u.pdb`,
  `atp.sdf`.
- `data/intermediate/motif_residues.json` — P-loop residue ranges written by
  `01_identify_motif.py`, consumed by `03_prepare_docking.py`.
- `data/intermediate/relaxed/` — Rosetta relax output models (`protN_relaxed_000M.pdb`) and
  their score table (`score_relaxed.sc`).
- `data/intermediate/pdbqt/` — Vina-ready `.pdbqt` conversions of both `data/input/` and
  `data/intermediate/relaxed/` structures, plus the ligand.
- `data/intermediate/vina_configs/` — generated Vina config files, one per structure; treat
  as derived/regenerable, not hand-edited (though `data/intermediate/vina_configs/config.txt`
  and a few per-protein configs predate this pipeline and have hand-tuned box
  sizes/exhaustiveness that differ from the script defaults — re-running
  `03_prepare_docking.py` will overwrite those tweaks).
- `data/intermediate/logs/` — `ROSETTA_CRASH.log`, `prepare_docking_errors.log` (failed
  receptor-prep runs, see step 3) and similar.
- `data/output/vina_poses/` — final docked poses (multi-model `.pdbqt`, ranked by Vina's
  predicted binding affinity, best pose first) and each run's `<structure>_vina_log.txt`
  (Vina's full stdout, including the per-mode affinity table).
- `data/output/pymol_scripts/` — generated `.pml` viewers, one per docked structure (see
  step 5).
- `data/output/docking_scores.csv` — every structure's best-pose binding affinity, ranked
  strongest to weakest (see step 6).

Top level: `scripts/` (pipeline scripts, see below — including `docking_box.py`, the PyMOL
box-visualization plugin used by step 5), `vina_1.2.7_win.exe`, `scratch/` (ad-hoc/
exploratory, not part of the reproducible pipeline — currently just `prepare_docking.ipynb`,
the superseded notebook this pipeline replaced).

## Pipeline / commands

Run from the repository root, in order. Each step is independent and re-runnable; later
steps read the files the earlier ones wrote rather than taking piped input.

1. **`python scripts/01_identify_motif.py`** — parses SEQRES records from the reference
   structure (default `data/input/6c2u.pdb`), regex-searches for the P-loop motif
   (`G.{4}GK[TS]`), and writes the matching residue ranges to
   `data/intermediate/motif_residues.json`. Override the reference/pattern/output path with
   `--reference` / `--pattern` / `--out`.

2. **`python scripts/02_relax_structures.py`** — runs Rosetta `relax` on every
   `data/input/prot*.pdb`, producing 5 relaxed models each plus a per-structure score table
   (`data/intermediate/relaxed/<stem>_score.sc`, via `-out:file:scorefile`, so different
   proteins' runs don't clobber a shared score file — override the naming with
   `--scorefile-name`), using the flags recovered from a prior
   `ROSETTA_CRASH.log`: `-relax:fast -relax:constrain_relax_to_start_coords
   -relax:coord_constrain_sidechains`. Rosetta isn't installed natively on this Windows
   machine, so by default the script shells out through WSL (`wsl bash -lc "..."`) and
   translates Windows paths via `wslpath`; pass `--no-wsl` if running inside a Linux shell
   directly. If `relax` isn't on PATH inside WSL, pass the real binary via `--relax-bin`
   (this project previously used
   `/home/<user>/miniconda3/envs/rosetta/bin/relax.cxx11threadserialization.linuxclangrelease`
   — see the `--relax-bin` example in the script's `--help`). `--conda-env` wraps the call in
   `conda run -n <env>` if relax lives in a conda environment.

3. **`python scripts/03_prepare_docking.py`** — for every PDB in `data/input/` and
   `data/intermediate/relaxed/`: converts it to `.pdbqt` in `data/intermediate/pdbqt/` if
   missing (via Meeko's `mk_prepare_receptor.py`, and `mk_prepare_ligand.py` once for the
   ATP ligand — requires `pip install meeko`; override the commands with
   `--prepare-receptor-cmd`/`--prepare-ligand-cmd` if they need a different invocation.
   `mk_prepare_receptor.py` expects the input PDB to already have realistic protonation —
   it does not add hydrogens itself), computes a docking box from
   `data/intermediate/motif_residues.json` (CA-atom extent + `--padding`, default 10 Å), and
   writes a config to `data/intermediate/vina_configs/<structure>_config.txt`
   (`exhaustiveness=16` by default, override with `--exhaustiveness`). Requires step 1's
   output to exist first.

4. **`scripts/04_run_docking.sh`** — runs Vina (`vina` on PATH by default — edit `VINA_BIN`
   in the script to point at `./vina_1.2.7_win.exe` or elsewhere) against every config in
   `data/intermediate/vina_configs/`, writing poses to `data/output/vina_poses/` per each
   config's `out =` line, and tee's Vina's stdout to a matching
   `<structure>_vina_log.txt` in the same directory. Requires step 3's configs to exist
   first.

5. **`python scripts/05_generate_pymol_scripts.py`** — for every
   `data/output/vina_poses/<structure>_vina_output.pdbqt`, finds the matching original
   receptor (`data/input/<structure>.pdb` or `data/intermediate/relaxed/<structure>.pdb`)
   and writes `data/output/pymol_scripts/<structure>_view.pml`: loads the receptor as
   cartoon and the docked poses as sticks (each Vina mode becomes a separate PyMOL state);
   highlights the P-loop motif residues (from `data/intermediate/motif_residues.json`) as
   magenta sticks (`--no-motif` to skip; not orange, which is PyMOL's default phosphorus
   color and would blend into ATP's phosphate tail); draws polar contacts
   (`distance ..., mode=2`, 50% dash transparency) between the poses and the receptor,
   colored yellow for contacts to P-loop residues and cyan for contacts elsewhere
   (`--no-hbonds` to skip; falls back to a single undifferentiated color if motif
   highlighting is off); and — if a matching
   `data/intermediate/vina_configs/<structure>_config.txt` exists — overlays the docking
   search box via `scripts/docking_box.py` (`--no-box` to skip this). Generated scripts use
   paths relative to the repo root (same convention as the Vina configs), so run PyMOL from
   there: `pymol data/output/pymol_scripts/<structure>_view.pml`.
   Requires step 4's poses to exist first.

6. **`python scripts/06_score_docking.py`** — parses every
   `data/output/vina_poses/<structure>_vina_log.txt` for its per-mode affinity table, takes
   each structure's best (lowest/most negative) affinity, and prints a ranking from
   strongest to weakest predicted binder, also writing it to
   `data/output/docking_scores.csv` (override with `--out`). Requires step 4's logs to exist
   first.

7. **Box visualization** (used directly by step 5, or standalone): `scripts/docking_box.py`
   is a PyMOL plugin (`from pymol import cmd; cmd.extend("docking_box", docking_box)`).
   Load it inside PyMOL with `run scripts/docking_box.py`, then call
   `docking_box name=box, center_x=.., center_y=.., center_z=.., size_x=.., size_y=.., size_z=..`
   using the center/size values from a `data/intermediate/vina_configs/*_config.txt` to draw
   the search box as a wireframe cube over the loaded structure.

`scripts/paths.py` and `scripts/pdb_utils.py` hold shared constants (the `data/` layout
above) and PDB-parsing helpers (SEQRES parsing, CA-coordinate extraction, bounding-box
calc) used by steps 1, 3, 5 and 6 — change the directory layout there, not per-script.

There is no build, lint, or automated test tooling in this repo. Requires `numpy`.

## Working with data files

- `data/score*.sc` files are Rosetta score tables (whitespace-aligned, `SCORE:` prefixed
  rows); the `description` column matches the corresponding relaxed-model filename.

When adding a new candidate structure: drop `protN.pdb` into `data/input/`, then run steps
2-6 above (step 1 only needs re-running if you change the reference structure or motif
pattern).
