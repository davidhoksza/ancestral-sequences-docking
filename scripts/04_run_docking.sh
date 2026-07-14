#!/bin/bash
# Run AutoDock Vina on every generated config in data/intermediate/vina_configs/.
# Run from the repository root: scripts/04_run_docking.sh [vina_binary]
set -euo pipefail

VINA_BIN="vina"
CONFIG_DIR="data/intermediate/vina_configs"
OUT_DIR="data/output/vina_poses"

mkdir -p "$OUT_DIR"

shopt -s nullglob
configs=("$CONFIG_DIR"/*.txt)

for config in "${configs[@]}"; do
    base_name=$(basename "$config" _config.txt)
    log_file="$OUT_DIR/${base_name}_vina_log.txt"
    echo "=== Docking with $config ==="
    "$VINA_BIN" --config "$config" 2>&1 | tee "$log_file"
done

echo "Docking complete. Results in $OUT_DIR/"
