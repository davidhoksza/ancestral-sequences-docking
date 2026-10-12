#!/bin/bash
# Master script: submits one PBS job per design, each docking all of that
# design's configs (rigid, flexible, relaxed replicates -- everything matching
# its name) via metacentrum/run_docking_job.pbs.
#
# With no arguments, the designs are discovered from data/input/ by the
# prot_<round>_<index>.pdb naming convention and ordered naturally
# (prot_1_1 ... prot_2_9, prot_2_10 ...), so new rounds/designs are picked up
# without editing this script.
#
# Arguments are name prefixes matched on underscore boundaries by
# scripts/04_run_docking.sh, so a round submits as a single job.
#
# Usage (run on a frontend node, from anywhere -- paths below are absolute):
#   bash metacentrum/submit_all.sh                    # one job per design in data/input/
#   bash metacentrum/submit_all.sh prot_2_5 prot_2_7  # only these designs
#   bash metacentrum/submit_all.sh prot_2             # all of round 2 as ONE job
#
# Set VINA_EXHAUSTIVENESS to dock at that exhaustiveness instead of the
# configs' own; it's forwarded to every job, whose poses/logs then land in
# data/output/vina_poses-exhaustiveness<N>/ (see scripts/04_run_docking.sh):
#   VINA_EXHAUSTIVENESS=128 bash metacentrum/submit_all.sh
#
# Jobs skip configs whose results already exist (see run_docking_job.pbs);
# set SKIP_EXISTING=0 to force re-docking everything:
#   SKIP_EXISTING=0 bash metacentrum/submit_all.sh prot_2_5
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/storage/praha5-elixir/home/davidhoksza/projects/ancestral-docking}"
JOB_SCRIPT="$PROJECT_DIR/metacentrum/run_docking_job.pbs"
INPUT_DIR="$PROJECT_DIR/data/input"
LOG_DIR="$PROJECT_DIR/metacentrum/logs"

if [ "$#" -gt 0 ]; then
    DESIGNS=("$@")
else
    shopt -s nullglob
    names=()
    for pdb in "$INPUT_DIR"/prot_*_*.pdb; do
        name=$(basename "$pdb" .pdb)
        # Skip anything that only looks like a design (e.g. a stray
        # prot_2_7_variant.pdb) -- a design is exactly prot_<round>_<index>.
        [[ "$name" =~ ^prot_[0-9]+_[0-9]+$ ]] || continue
        names+=("$name")
    done
    # Numeric sort on round then index, so prot_2_9 precedes prot_2_10.
    # (Guarded: under `set -u`, expanding an empty array is an error on older bash.)
    DESIGNS=()
    if [ ${#names[@]} -gt 0 ]; then
        mapfile -t DESIGNS < <(printf '%s\n' "${names[@]}" | sort -t_ -k2,2n -k3,3n)
    fi
fi

if [ ${#DESIGNS[@]} -eq 0 ]; then
    echo "No prot_<round>_<index>.pdb designs found in $INPUT_DIR" >&2
    exit 1
fi

if [ ! -d "$PROJECT_DIR/envs/docking" ]; then
    echo "No environment at $PROJECT_DIR/envs/docking -- run metacentrum/setup_env.sh first" >&2
    exit 1
fi

mkdir -p "$LOG_DIR"

# Only forwarded when set, so an unset value keeps the configs' exhaustiveness.
# Job names/logs get the same suffix as the output directory, so runs at
# different settings don't overwrite each other's PBS logs either.
VINA_EXHAUSTIVENESS="${VINA_EXHAUSTIVENESS:-}"
extra_vars=""
suffix=""
if [ -n "$VINA_EXHAUSTIVENESS" ]; then
    extra_vars=",VINA_EXHAUSTIVENESS=${VINA_EXHAUSTIVENESS}"
    suffix="-exhaustiveness${VINA_EXHAUSTIVENESS}"
fi
# Likewise only forwarded when set; the job defaults it to 1 (skip existing).
if [ -n "${SKIP_EXISTING:-}" ]; then
    extra_vars="${extra_vars},SKIP_EXISTING=${SKIP_EXISTING}"
fi

echo "Submitting ${#DESIGNS[@]} docking job(s)"
for prefix in "${DESIGNS[@]}"; do
    echo "Submitting docking job for ${prefix}${suffix}"
    qsub -N "docking_${prefix}${suffix}" \
         -v "PREFIX=${prefix},PROJECT_DIR=${PROJECT_DIR}${extra_vars}" \
         -o "$LOG_DIR/${prefix}${suffix}.log" \
         -j oe \
         "$JOB_SCRIPT"
done
