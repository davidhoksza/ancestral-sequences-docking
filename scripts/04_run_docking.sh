#!/bin/bash
# Run AutoDock Vina on every generated config in data/intermediate/vina_configs/.
# Run from the repository root: scripts/04_run_docking.sh [prefix]
#
# With a prefix argument, only runs configs whose filename starts with it,
# e.g. `04_run_docking.sh prot1` runs prot1_config.txt, prot1_flex_config.txt,
# prot1_relaxed_0001_config.txt, etc.; `04_run_docking.sh prot1_flex` runs
# only prot1_flex_config.txt. Omit it to run every config.
#
# Set VINA_CPU to cap how many CPUs Vina uses per config (passed as --cpu);
# useful on a shared machine/HPC node where Vina's own auto-detection would
# otherwise see -- and try to use -- every CPU on the node, not just the
# ones actually allocated to this job.
set -euo pipefail

VINA_BIN="vina"
CONFIG_DIR="data/intermediate/vina_configs"
OUT_DIR="data/output/vina_poses"
PREFIX="${1:-}"
VINA_CPU="${VINA_CPU:-}"

mkdir -p "$OUT_DIR"

shopt -s nullglob
configs=("$CONFIG_DIR/${PREFIX}"*.txt)

if [ ${#configs[@]} -eq 0 ]; then
    echo "No config files matching '$CONFIG_DIR/${PREFIX}*.txt' -- run 03_prepare_docking.py first" >&2
    exit 1
fi

cpu_args=()
if [ -n "$VINA_CPU" ]; then
    cpu_args=(--cpu "$VINA_CPU")
fi

for config in "${configs[@]}"; do
    base_name=$(basename "$config" _config.txt)
    log_file="$OUT_DIR/${base_name}_vina_log.txt"
    echo "=== Docking with $config ==="
    "$VINA_BIN" --config "$config" "${cpu_args[@]}" 2>&1 | tee "$log_file"
done

echo "Docking complete. Results in $OUT_DIR/"
