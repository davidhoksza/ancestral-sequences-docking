"""Shared filesystem layout for the docking pipeline.

All pipeline scripts import their input/output locations from here so the
directory structure only has to change in one place.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = REPO_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"

INTERMEDIATE_DIR = DATA_DIR / "intermediate"
RELAXED_DIR = INTERMEDIATE_DIR / "relaxed"
PDBQT_DIR = INTERMEDIATE_DIR / "pdbqt"
VINA_CONFIGS_DIR = INTERMEDIATE_DIR / "vina_configs"
LOGS_DIR = INTERMEDIATE_DIR / "logs"
MOTIF_RESIDUES_FILE = INTERMEDIATE_DIR / "motif_residues.json"

OUTPUT_DIR = DATA_DIR / "output"
VINA_POSES_DIR = OUTPUT_DIR / "vina_poses"
PYMOL_SCRIPTS_DIR = OUTPUT_DIR / "pymol_scripts"
DOCKING_SCORES_FILE = OUTPUT_DIR / "docking_scores.csv"

REFERENCE_STRUCTURE = INPUT_DIR / "6c2u.pdb"
LIGAND_SDF = INPUT_DIR / "atp.sdf"
LIGAND_PDBQT = PDBQT_DIR / "atp.pdbqt"

DOCKING_BOX_SCRIPT = REPO_ROOT / "scripts" / "docking_box.py"


def rel(path):
    """Path relative to REPO_ROOT, as a forward-slash string.

    Vina config files are read with the repo root as the working directory
    (see scripts/04_run_docking.sh), so paths inside them must stay relative
    rather than absolute -- the repo lives under a path with spaces
    ("OneDrive - Univerzita Karlova"), which Vina's config parser can't quote.
    """
    return Path(path).resolve().relative_to(REPO_ROOT).as_posix()
