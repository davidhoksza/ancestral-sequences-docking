#!/bin/bash
# Run AutoDock Vina on every generated config in data/intermediate/vina_configs/.
# Run from the repository root: scripts/04_run_docking.sh [prefix]
#
# With a prefix argument, only runs the configs for that name -- matched on
# underscore-separated name boundaries, not as a raw string prefix:
#   prot_2_1       -> prot_2_1_config.txt, prot_2_1_flex_config.txt,
#                     prot_2_1_relaxed_0001_config.txt, ...
#                     (NOT prot_2_10.., prot_2_19.., which a raw string
#                      prefix would wrongly sweep in)
#   prot_2         -> every design in round 2
#   prot_2_1_flex  -> only prot_2_1_flex_config.txt
# Omit the prefix to run every config.
#
# Set VINA_CPU to cap how many CPUs Vina uses per config (passed as --cpu);
# useful on a shared machine/HPC node where Vina's own auto-detection would
# otherwise see -- and try to use -- every CPU on the node, not just the
# ones actually allocated to this job.
#
# Set VINA_EXHAUSTIVENESS to override the exhaustiveness baked into the
# configs by 03_prepare_docking.py (passed as --exhaustiveness, which Vina
# lets take precedence over the config file), without regenerating them.
# Each config's `out =` path is fixed, so to keep runs at different
# settings from overwriting each other, poses and logs then go to
# data/output/vina_poses-exhaustiveness<N>/ instead of data/output/vina_poses/
# -- point steps 5/6 at it with --vina-poses-dir.
#
# Set SKIP_EXISTING=1 to skip every config whose pose file already exists
# (non-empty), so re-running/resubmitting only docks what's missing; if
# everything is present, it exits without running Vina at all. The pose
# file is the completion marker, not the log: Vina writes poses only once
# docking finishes, whereas the log is tee'd as it runs and a killed run
# leaves a partial one behind.
set -euo pipefail

VINA_BIN="vina"
CONFIG_DIR="data/intermediate/vina_configs"
OUT_DIR="data/output/vina_poses"
PREFIX="${1:-}"
VINA_CPU="${VINA_CPU:-}"
VINA_EXHAUSTIVENESS="${VINA_EXHAUSTIVENESS:-}"
SKIP_EXISTING="${SKIP_EXISTING:-}"

if [ -n "$VINA_EXHAUSTIVENESS" ]; then
    if ! [[ "$VINA_EXHAUSTIVENESS" =~ ^[1-9][0-9]*$ ]]; then
        echo "VINA_EXHAUSTIVENESS must be a positive integer, got '$VINA_EXHAUSTIVENESS'" >&2
        exit 1
    fi
    OUT_DIR="${OUT_DIR}-exhaustiveness${VINA_EXHAUSTIVENESS}"
fi

mkdir -p "$OUT_DIR"

shopt -s nullglob
configs=()
if [ -z "$PREFIX" ]; then
    configs=("$CONFIG_DIR"/*_config.txt)
    pattern="$CONFIG_DIR/*_config.txt"
else
    # Two globs rather than one "${PREFIX}"* so the match ends on a name
    # boundary: the exact config for this name, plus the configs of anything
    # derived from it (_flex, _relaxed_000N). Design indices are open-ended
    # and run past 9, so a raw string prefix would make prot_<r>_1 also pick
    # up prot_<r>_10 .. prot_<r>_19.
    #
    # The exact config is tested with -e rather than left to the glob:
    # having no wildcard, it is a literal word that nullglob can't drop, and
    # it legitimately doesn't exist when PREFIX names a whole round
    # (prot_<r>) or when that structure's receptor prep failed.
    if [ -e "$CONFIG_DIR/${PREFIX}_config.txt" ]; then
        configs+=("$CONFIG_DIR/${PREFIX}_config.txt")
    fi
    derived=("$CONFIG_DIR/${PREFIX}"_*_config.txt)
    if [ ${#derived[@]} -gt 0 ]; then
        configs+=("${derived[@]}")
    fi
    pattern="$CONFIG_DIR/${PREFIX}[_]*_config.txt"
fi

if [ ${#configs[@]} -eq 0 ]; then
    echo "No config files matching '$pattern' -- run 03_prepare_docking.py first" >&2
    exit 1
fi

cpu_args=()
if [ -n "$VINA_CPU" ]; then
    cpu_args=(--cpu "$VINA_CPU")
fi

ran=0
skipped=0
for config in "${configs[@]}"; do
    base_name=$(basename "$config" _config.txt)
    log_file="$OUT_DIR/${base_name}_vina_log.txt"
    # Command-line options take precedence over the config file, so these
    # override its exhaustiveness and redirect its `out =` into OUT_DIR
    # (same file name, so steps 5/6 still pair poses with logs/configs).
    ex_args=()
    if [ -n "$VINA_EXHAUSTIVENESS" ]; then
        out_file="$OUT_DIR/${base_name}_vina_output.pdbqt"
        ex_args=(--exhaustiveness "$VINA_EXHAUSTIVENESS" --out "$out_file")
    else
        # Wherever the config's own `out =` line sends the poses (stripping
        # comments, whitespace and any CRLF), falling back to the convention.
        out_file=$(sed -n 's/#.*//; s/\r$//; s/^[[:space:]]*out[[:space:]]*=[[:space:]]*//p' "$config" \
                   | sed 's/[[:space:]]*$//' | head -n 1)
        out_file="${out_file:-$OUT_DIR/${base_name}_vina_output.pdbqt}"
    fi
    if [ "$SKIP_EXISTING" = 1 ] && [ -s "$out_file" ]; then
        echo "=== Skipping $config -- $out_file already exists ==="
        skipped=$((skipped + 1))
        continue
    fi
    echo "=== Docking with $config ==="
    "$VINA_BIN" --config "$config" "${cpu_args[@]}" "${ex_args[@]}" 2>&1 | tee "$log_file"
    ran=$((ran + 1))
done

if [ "$ran" -eq 0 ]; then
    echo "All ${skipped} config(s) already have results in $OUT_DIR/ -- nothing to dock."
    exit 0
fi
echo "Docking complete (${ran} run, ${skipped} skipped). Results in $OUT_DIR/"
