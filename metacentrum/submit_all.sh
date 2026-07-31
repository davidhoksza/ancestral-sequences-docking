#!/bin/bash
# Master script: submits one PBS job per protein, each docking all of that
# protein's configs (rigid, flexible, relaxed replicates -- everything
# matching its prefix) via metacentrum/run_docking_job.pbs.
#
# Usage (run on a frontend node, from anywhere -- paths below are absolute):
#   bash metacentrum/submit_all.sh              # submit all of PROTEINS below
#   bash metacentrum/submit_all.sh prot2 prot5   # submit only these
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/storage/praha5-elixir/home/davidhoksza/projects/ancestral-docking}"
JOB_SCRIPT="$PROJECT_DIR/metacentrum/run_docking_job.pbs"
LOG_DIR="$PROJECT_DIR/metacentrum/logs"

PROTEINS=(prot1 prot2 prot3 prot4 prot5 prot6 prot7 prot8)
if [ "$#" -gt 0 ]; then
    PROTEINS=("$@")
fi

if [ ! -d "$PROJECT_DIR/envs/docking" ]; then
    echo "No environment at $PROJECT_DIR/envs/docking -- run metacentrum/setup_env.sh first" >&2
    exit 1
fi

mkdir -p "$LOG_DIR"

for prefix in "${PROTEINS[@]}"; do
    echo "Submitting docking job for $prefix"
    qsub -N "docking_${prefix}" \
         -v "PREFIX=${prefix},PROJECT_DIR=${PROJECT_DIR}" \
         -o "$LOG_DIR/${prefix}.log" \
         -j oe \
         "$JOB_SCRIPT"
done
