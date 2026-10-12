#!/usr/bin/env python3
"""Rank docked structures by their best pose's binding affinity.

Parses every data/output/vina_poses/<name>_vina_log.txt (written by
scripts/04_run_docking.sh) for its per-mode affinity table, takes each
structure's best (lowest/most negative) affinity, and prints -- and writes to
a CSV -- a ranking from strongest to weakest predicted binder.
"""
import argparse
import csv
import re
from pathlib import Path

from paths import VINA_POSES_DIR, DOCKING_SCORES_FILE, natural_key

# Matches a Vina mode-table row, e.g. "   1       -5.745          0          0"
MODE_LINE = re.compile(r"^\s*\d+\s+(-?\d+\.\d+)\s+", re.MULTILINE)


def parse_best_affinity(log_path):
    """Lowest (best) affinity in kcal/mol from a Vina log's mode table, or None."""
    affinities = [float(m.group(1)) for m in MODE_LINE.finditer(log_path.read_text())]
    return min(affinities) if affinities else None


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--vina-poses-dir", type=Path, default=VINA_POSES_DIR)
    parser.add_argument("--out", type=Path, default=DOCKING_SCORES_FILE)
    args = parser.parse_args()

    log_files = sorted(args.vina_poses_dir.glob("*_vina_log.txt"), key=natural_key)
    if not log_files:
        raise SystemExit(
            f"No *_vina_log.txt files in {args.vina_poses_dir} -- run 04_run_docking.sh first"
        )

    results = []
    for log_path in log_files:
        name = log_path.stem[: -len("_vina_log")]
        best = parse_best_affinity(log_path)
        if best is None:
            print(f"WARNING: no mode table found in {log_path}, skipping")
            continue
        results.append((best, name))

    # Equal affinities tie-break on the natural name order (prot_2_9 before
    # prot_2_10), not on the raw string.
    results.sort(key=lambda r: (r[0], natural_key(r[1])))

    # Width follows the actual names -- they grow with the design numbering
    # (prot_<round>_<index>, plus _relaxed_000N/_flex suffixes).
    name_width = max([len("Receptor")] + [len(name) for _, name in results])
    header = f"{'Receptor':<{name_width}} {'Best affinity (kcal/mol)':>25}"
    print(header)
    print("-" * len(header))
    for best, name in results:
        print(f"{name:<{name_width}} {best:>25.3f}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["receptor", "best_affinity_kcal_mol"])
        writer.writerows((name, f"{best:.3f}") for best, name in results)
    print(f"\nWrote {len(results)} scores to {args.out}")


if __name__ == "__main__":
    main()
