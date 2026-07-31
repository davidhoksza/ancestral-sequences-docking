#!/bin/bash
# One-time setup of the mamba environment for the docking pipeline on Metacentrum.
#
# Run this on a frontend node (e.g. elmo.metacentrum.cz, whose storage maps to
# /storage/praha5-elixir/home/...) AFTER copying this repo to $PROJECT_DIR --
# it only downloads/installs packages, so it doesn't need a compute allocation.
#
# Usage: bash metacentrum/setup_env.sh
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/storage/praha5-elixir/home/davidhoksza/projects/ancestral-docking}"
ENV_DIR="$PROJECT_DIR/envs/docking"

module add mambaforge

mamba env create --prefix "$ENV_DIR" -f "$PROJECT_DIR/metacentrum/environment.yml"

echo
echo "Environment created at $ENV_DIR"
echo
echo "Rosetta (needed for scripts/02_relax_structures.py) is provided as a"
echo "Metacentrum module, not part of this env:"
echo "  module avail rosetta/"
echo "You must first join the 'lic_rosetta' group via the e-INFRA portal to use"
echo "it -- see https://docs.metacentrum.cz/en/docs/software/sw-list/rosetta"
echo
echo "Verify the docking tools:"
echo "  mamba activate $ENV_DIR"
echo "  vina --help && mk_prepare_ligand.py --help && obabel -V"
