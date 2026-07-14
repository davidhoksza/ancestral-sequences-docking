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


def load_motif_residues(path):
    """1-indexed (start, end) residue ranges written by 01_identify_motif.py."""
    with open(path) as f:
        return json.load(f)["motif_residues"]
