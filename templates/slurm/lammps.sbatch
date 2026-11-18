#!/usr/bin/env bash

#SBATCH --job-name=lammps
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --mem=4G
#SBATCH --output=slurm-%j.out

set -euo pipefail

# Adjust the resource requests above for the target cluster.
# Load the appropriate LAMMPS module if necessary, for example:
# module load lammps

LAMMPS_BIN="${LAMMPS_BIN:-lmp}"
LAMMPS_INPUT="${LAMMPS_INPUT:?Set LAMMPS_INPUT when submitting the job}"

# Run from the directory where sbatch was submitted.
cd "${SLURM_SUBMIT_DIR:?This script must run through Slurm}"

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

if [[ ! -f "$LAMMPS_INPUT" ]]; then
    echo "Input file not found: $LAMMPS_INPUT" >&2
    exit 1
fi

if ! command -v "$LAMMPS_BIN" >/dev/null 2>&1; then
    echo "LAMMPS executable not found: $LAMMPS_BIN" >&2
    exit 1
fi

echo "Job ID: $SLURM_JOB_ID"
echo "Working directory: $PWD"
echo "LAMMPS executable: $LAMMPS_BIN"
echo "Input file: $LAMMPS_INPUT"
echo "MPI ranks: $SLURM_NTASKS"
echo "OpenMP threads per rank: $OMP_NUM_THREADS"

srun --ntasks="$SLURM_NTASKS" \
    "$LAMMPS_BIN" \
    -in "$LAMMPS_INPUT" \
    -log "log.${SLURM_JOB_ID}.lammps"
