#!/bin/bash -l
# Rishant Prakash - AST 5765C - HW2 - 2026-09-09
#SBATCH --job-name=hw2_prakash
#SBATCH --output=hw2_prakash_stokes-%j.out
#SBATCH --error=hw2_prakash_stokes-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=00:10:00

set -eo pipefail
module load anaconda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ast5765
set -u

cd "${SLURM_SUBMIT_DIR:?Submit with sbatch from the homework directory}"
printf 'Stokes execution started: '
date
hostname
python --version
python hw2_prakash.py
printf 'Stokes execution completed: '
date
