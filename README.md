# Ancestral P-loop NTPase — ATP Docking Pipeline

## Background

P-loop NTPases are one of the oldest and most widespread nucleotide-binding protein
families, built around the Walker A motif (`G-x(4)-GK-[T/S]`) — a short loop that wraps
around the phosphate tail of ATP/GTP. Two glycines let the backbone bend sharply enough to
cradle the phosphates via backbone NH groups, a conserved lysine makes the only
side-chain-specific contact (a bidentate salt bridge to the β,γ-phosphate), and a
Ser/Thr coordinates the catalytic Mg²⁺. See [`docs/background/`](docs/background/) for the
full mechanistic writeup (ATP's phosphate chain, Mg²⁺ coordination, the Walker B motif and
hydrolysis chemistry, and why the P-loop's early-evolving glycines/Ser-Thr contrast with its
one late-evolving residue, lysine).

This project asks a narrower question: given a set of **ancestrally-reconstructed**
sequences (`prot1.pdb` … `prot8.pdb`) inferred to sit along the evolutionary lineage leading
to a present-day P-loop NTPase, do their predicted 3D structures still fold into a
plausible ATP-binding pocket? We use the real crystal structure of that modern relative,
`6c2u.pdb`, as a reference: its Walker A motifs are located by sequence, used to place a
docking search box, and every ancestral variant (plus 20 NMR-ensemble models of the
reference itself, `6c2u_model_*`, as a sanity-check baseline) has ATP docked into the
corresponding pocket with AutoDock Vina. Structures are also independently refined with
Rosetta `relax` and scored. Predicted binding affinity is then used as a rough proxy for
"did this ancestor plausibly still bind ATP?" — see the caveats on trusting Vina's score as
an absolute ΔG in [`docs/background/P-loop_ATP_binding_summary.md`](docs/background/P-loop_ATP_binding_summary.md#atpp-loop-binding-energy).

There is no application code here — this is a data-processing pipeline of Python scripts, a
shell script, and Rosetta/Vina inputs and outputs, plus a couple of Jupyter notebooks for
exploration and results analysis.

## Repository layout

- **`data/input/`** — raw, never-modified source structures and ligand: `protN.pdb`,
  `6c2u.pdb` (+ its 20 NMR models), `atp.sdf`.
- **`data/intermediate/`** — everything derived along the way: the identified motif residue
  ranges, Rosetta-relaxed models and their score table, Vina-ready `.pdbqt` conversions, and
  generated Vina config files (one per structure).
- **`data/output/`** — final results: docked poses (`vina_poses/`, ranked by predicted
  binding affinity), generated PyMOL viewer scripts (`pymol_scripts/`), and the ranked
  summary `docking_scores.csv` (and `docking_scores-exhaustiveness<N>.csv` variants, one per
  Vina `exhaustiveness` setting that's been tried).
- **`scripts/`** — the numbered pipeline steps (`01_...` – `06_...`), plus shared helpers
  (`paths.py`, `pdb_utils.py`) and the PyMOL box-visualization plugin (`docking_box.py`).
- **`notebooks/`** — analysis notebooks, e.g. `analyze_docking_scores.ipynb`, which combines
  the per-exhaustiveness score CSVs and charts how many/which structures clear a chosen
  affinity threshold.
- **`docs/background/`** — the mechanistic background on P-loop/ATP binding referenced above.
- **`metacentrum/`** — HPC deployment for distributing docking runs across the Czech
  Metacentrum grid.
- **`scratch/`** — ad-hoc/exploratory work, not part of the reproducible pipeline.

Full details on each subdirectory and file-naming convention are in
[`CLAUDE.md`](CLAUDE.md).

## Pipeline

Run from the repository root, in order. Each step reads the files earlier steps wrote,
rather than taking piped input, so any step can be re-run independently once its inputs
exist.

1. **Identify the motif** (`scripts/01_identify_motif.py`) — regex-search the reference
   structure's sequence for the Walker A pattern and record the matching residue ranges.
2. **Relax structures** (`scripts/02_relax_structures.py`) — run Rosetta `relax` on every
   ancestral structure, producing 5 relaxed models each plus a score table. This serves two
   purposes: sampling whether alternate, lower-energy backbone/side-chain conformations
   change the docking outcome, and — more practically — resolving steric clashes. Some
   ancestral designs have clashes severe enough that `mk_prepare_receptor.py` (step 3)
   refuses to convert them to `.pdbqt` at all; relaxing first fixes those geometries so the
   structure can proceed through the rest of the pipeline.
3. **Prepare docking inputs** (`scripts/03_prepare_docking.py`) — convert structures and the
   ATP ligand to `.pdbqt`, compute a docking search box around the motif residues, and write
   a Vina config per structure (optionally with flexible P-loop side chains via
   `--flexible`).
4. **Run docking** (`scripts/04_run_docking.sh`) — run AutoDock Vina against every config,
   writing poses and a log per structure.
5. **Visualize** (`scripts/05_generate_pymol_scripts.py`) — generate a PyMOL script per
   docked structure: receptor cartoon, motif residues highlighted, docked poses, polar
   contacts, and the search box overlay.
6. **Score and rank** (`scripts/06_score_docking.py`) — parse each structure's best-pose
   affinity from the Vina logs and rank all structures from strongest to weakest predicted
   binder.

See [`CLAUDE.md`](CLAUDE.md) for exact commands, flags, and file-naming details for every
step.

`data/output/` currently holds the results of running this pipeline (step 4 onward) several
times with different Vina `exhaustiveness` settings — one ranked CSV per run
(`docking_scores-exhaustiveness<N>.csv`), to check how sensitive the results are to that
setting. [`notebooks/analyze_docking_scores.ipynb`](notebooks/analyze_docking_scores.ipynb)
loads and compares all of them: it combines the per-run CSVs into one dataframe and, for
each exhaustiveness value separately, lists and charts which structures clear a chosen
binding-affinity threshold.

## Requirements

The easiest way to get everything steps 2 and 3 need is the bundled conda/mamba
environment, [`env/rosetta-environment.yml`](env/rosetta-environment.yml) (Linux/WSL only —
it's what this project's own WSL setup uses). It pins Rosetta itself alongside `meeko`,
`openbabel`, `rdkit`, `numpy`, `pandas`, `matplotlib-base`, `scipy`, `gemmi`, `biopython`,
and `prody`, so activating it is enough to run steps 1-3 (and do basic analysis) without
installing anything else:

```bash
conda env create -f env/rosetta-environment.yml   # or: mamba env create -f ...
conda activate rosetta
```

Once active, `relax` is directly on `PATH`, so `scripts/02_relax_structures.py` needs no
`--relax-bin`/`--conda-env` override *if you're already running inside that environment*
(e.g. a WSL shell with it activated); from Windows PowerShell instead, pass
`--conda-env rosetta` so the script wraps the call in `conda run -n rosetta` (this is exactly
the env `--conda-env`'s docstring example refers to).

What the environment does **not** cover, since they're not conda packages / aren't needed
inside it:

- [AutoDock Vina](https://vina.scripps.edu/) for step 4 (a Windows binary,
  `vina_1.2.7_win.exe`, is included at the repo root; install separately for a Linux/WSL run).
- [PyMOL](https://pymol.org/) to view the step 5 output.
- `seaborn` and `jupyter`, needed only to run the analysis notebooks.

## Running on Metacentrum

`metacentrum/` distributes step 4 (docking) across the Czech Metacentrum HPC grid as one PBS
job per protein. See the "Running on Metacentrum" section of [`CLAUDE.md`](CLAUDE.md) for
setup and submission instructions.
