#!/usr/bin/env python3
"""Locate the P-loop (Walker A) motif in a reference structure.

Parses SEQRES records from the reference PDB, regex-searches for the motif,
and writes the matching 1-indexed residue ranges to
data/intermediate/motif_residues.json for use by 03_prepare_docking.py.
"""
import argparse
import json
import re
from pathlib import Path

from paths import REFERENCE_STRUCTURE, MOTIF_RESIDUES_FILE
from pdb_utils import seqres_sequence

MOTIF_PATTERN = r'G.{4}GK[TS]'  # Walker A / P-loop: G-x(4)-GK-[T/S]


def find_motif_residues(sequence, pattern=MOTIF_PATTERN):
    """1-indexed (start, end) residue ranges for each pattern match."""
    return [(m.start() + 1, m.end()) for m in re.finditer(pattern, sequence)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=REFERENCE_STRUCTURE,
                         help="Reference PDB with SEQRES records (default: %(default)s)")
    parser.add_argument("--pattern", default=MOTIF_PATTERN,
                         help="Regex motif to search for (default: %(default)s)")
    parser.add_argument("--out", type=Path, default=MOTIF_RESIDUES_FILE,
                         help="Where to write the matched residue ranges (default: %(default)s)")
    args = parser.parse_args()

    sequence = seqres_sequence(args.reference)
    matches = find_motif_residues(sequence, args.pattern)
    if not matches:
        raise SystemExit(f"No match for pattern {args.pattern!r} in {args.reference}")

    print(f"Sequence length: {len(sequence)}")
    for start, end in matches:
        print(f"  {sequence[start - 1:end]}: residues {start}-{end}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(
            {"pattern": args.pattern, "reference": str(args.reference), "motif_residues": matches},
            f, indent=2,
        )
    print(f"Wrote {len(matches)} motif range(s) to {args.out}")


if __name__ == "__main__":
    main()
