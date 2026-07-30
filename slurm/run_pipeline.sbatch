#!/bin/bash
#SBATCH --job-name=neurodataops
#SBATCH --output=logs/neurodataops_%j.out
#SBATCH --error=logs/neurodataops_%j.err
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

set -euo pipefail

PROJECT_ROOT="/path/to/neurodataops-bids-qc"
BIDS_ROOT="/path/to/ds008477"

cd "$PROJECT_ROOT"
mkdir -p logs outputs

module load python/3.11
source .venv/bin/activate

export BIDS_ROOT="$BIDS_ROOT"
export OUTPUT_ROOT="outputs"
export DATABASE_PATH="outputs/neurodataops.db"

python -m neurodataops.pipeline
