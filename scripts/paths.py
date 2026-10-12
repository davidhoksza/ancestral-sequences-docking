"""Shared filesystem layout and naming conventions for the docking pipeline.

All pipeline scripts import their input/output locations -- and the
candidate-design naming convention -- from here, so the directory structure
and file-naming rules only have to change in one place.
"""
import re
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
DOCKING_SCORES_FILE = OUTPUT_DIR / "docking_scores.csv"

REFERENCE_STRUCTURE = INPUT_DIR / "6c2u.pdb"
LIGAND_SDF = INPUT_DIR / "atp.sdf"
LIGAND_PDBQT = PDBQT_DIR / "atp.pdbqt"

DOCKING_BOX_SCRIPT = REPO_ROOT / "scripts" / "docking_box.py"

# Candidate designs are named prot_<round>_<index>, e.g. prot_1_1 (round 1,
# design 1) or prot_2_29. Both numbers are open-ended: rounds accumulate over
# time and a round holds as many designs as it holds, so nothing in the
# pipeline may hardcode a list of design names -- discover them from
# data/input/ via input_designs() instead.
DESIGN_GLOB = "prot_*_*.pdb"
DESIGN_NAME_RE = re.compile(r"^prot_(\d+)_(\d+)$")
# Same name, but allowing derived suffixes: prot_2_7_flex, prot_2_7_relaxed_0001.
DESIGN_PREFIX_RE = re.compile(r"^(prot_\d+_\d+)(?:_|$)")


def parse_design_name(name):
    """(round, index) for a "prot_<round>_<index>" design, or None.

    Takes a name, stem or Path. Names derived from a design (e.g.
    "prot_2_7_relaxed_0001") deliberately don't parse -- they're not designs
    themselves; use natural_key to order those.
    """
    match = DESIGN_NAME_RE.match(Path(name).stem)
    return (int(match.group(1)), int(match.group(2))) if match else None


def design_label(name):
    """The design a structure name belongs to, for grouping its variants.

    "prot_2_7", "prot_2_7_flex" and "prot_2_7_relaxed_0001" all label as
    "prot_2_7". Names that aren't designs fall back to their first
    underscore-separated token, so the reference and its NMR models
    ("6c2u", "6c2u_model_10") group together under "6c2u".
    """
    stem = Path(name).stem
    match = DESIGN_PREFIX_RE.match(stem)
    return match.group(1) if match else stem.split("_", 1)[0]


def natural_key(name):
    """Sort key that orders embedded numbers numerically, not lexically.

    Design indices run past 9 (prot_2_0 .. prot_2_29), so plain string
    sorting would interleave them as prot_2_1, prot_2_10, prot_2_11, ...,
    prot_2_2. Works on any name, design or derived (relaxed models, pose
    files, logs), as a Path or a string.
    """
    return tuple(
        (1, int(part)) if part.isdigit() else (0, part)
        for part in re.split(r"(\d+)", Path(name).stem)
    )


def input_designs(input_dir=INPUT_DIR):
    """Every prot_<round>_<index>.pdb design in input_dir, naturally sorted."""
    return sorted(
        (p for p in Path(input_dir).glob(DESIGN_GLOB) if parse_design_name(p)),
        key=natural_key,
    )


def rel(path):
    """Path relative to REPO_ROOT, as a forward-slash string.

    Vina config files are read with the repo root as the working directory
    (see scripts/04_run_docking.sh), so paths inside them must stay relative
    rather than absolute -- the repo lives under a path with spaces
    ("OneDrive - Univerzita Karlova"), which Vina's config parser can't quote.
    """
    return Path(path).resolve().relative_to(REPO_ROOT).as_posix()
