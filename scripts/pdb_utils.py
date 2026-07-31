"""Shared helpers for reading PDB structures, used across the docking pipeline."""
import json

import numpy as np

THREE_TO_ONE = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
}


def seqres_sequence(pdb_path):
    """Return the single-letter sequence built from a PDB's SEQRES records."""
    residues = []
    with open(pdb_path) as f:
        for line in f:
            if line.startswith('SEQRES'):
                residues.extend(line[19:].split())
    return ''.join(THREE_TO_ONE[r] for r in residues)


def ca_coords(pdb_path, res_start, res_end):
    """CA atom coordinates for residues in [res_start, res_end] as an (N, 3) array."""
    coords = []
    with open(pdb_path) as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                res_num = int(line[22:26])
                if res_start <= res_num <= res_end:
                    coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(coords) if coords else None


def bounding_box(coords, padding=10.0):
    """(center, size) for a padded axis-aligned bounding box around coords."""
    if coords is None or len(coords) == 0:
        return None, None
    center = coords.mean(axis=0)
    size = coords.max(axis=0) - coords.min(axis=0) + padding
    return center, size


def residue_names(pdb_path, res_start, res_end):
    """{res_num: (chain_id, three_letter_resname)} for residues in [res_start, res_end]."""
    residues = {}
    with open(pdb_path) as f:
        for line in f:
            if line.startswith('ATOM'):
                res_num = int(line[22:26])
                if res_start <= res_num <= res_end and res_num not in residues:
                    residues[res_num] = (line[21].strip(), line[17:20].strip())
    return residues


def flexible_ploop_residues(pdb_path, motif_residues):
    """(chain, res_num) pairs eligible for Vina flexible-sidechain docking.

    For each motif range, excludes the first and last residue of the range,
    and excludes any residue that is actually Glycine in *this* structure
    (Gly has no side chain to flex) -- residue identity is read from
    pdb_path itself rather than assumed from the reference/regex pattern,
    since ancestral variants aren't guaranteed to match it at every position.
    """
    flexible = []
    for start, end in motif_residues:
        names = residue_names(pdb_path, start, end)
        for res_num in range(start, end + 1):
            if res_num in (start, end):
                continue
            entry = names.get(res_num)
            if entry is None:
                continue
            chain_id, resname = entry
            if resname == 'GLY':
                continue
            flexible.append((chain_id, res_num))
    return flexible


def load_motif_residues(path):
    """1-indexed (start, end) residue ranges written by 01_identify_motif.py."""
    with open(path) as f:
        return json.load(f)["motif_residues"]
