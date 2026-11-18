# Running LAMMPS with Slurm

This directory contains a Slurm submission script for running
LAMMPS calculations on an HPC cluster.

I originally ran most of my simulations using shell scripts and
MPI. The template here provides a starting point for running similar
calculations on systems that use Slurm.

It is intentionally generic, since different HPC clusters have
different resource limits, software modules, and MPI configurations.

## Submitting a calculation

Make sure LAMMPS is available on the cluster, either through a
software module or an installed executable.

Submit the job from the directory containing the LAMMPS input
script and any files it reads:

```bash
sbatch --export=ALL,LAMMPS_INPUT=sinput.in \
    /path/to/lammps.sbatch
```

Replace `/path/to/lammps.sbatch` with the location of the template.

The input filename is passed through `LAMMPS_INPUT`, rather than
hardcoded in the submission script.

If the executable has a different name, it can also be specified:

```bash
sbatch --export=ALL,LAMMPS_INPUT=sinput.in,LAMMPS_BIN=lmp_mpi \
    /path/to/lammps.sbatch
```

## Resources

The template currently requests:

- One compute node
- Four MPI tasks
- One CPU per task
- Four gigabytes of memory
- A 30-minute time limit

These settings are only starting values. They should be adjusted
based on the calculation, available hardware, and cluster rules.

The number of OpenMP threads is taken from `SLURM_CPUS_PER_TASK`.

## Cluster-specific settings

Depending on the cluster, you may need to:

- Load a LAMMPS module inside the submission script.
- Specify a partition or allocation account.
- Adjust the number of nodes, MPI tasks, memory, and time limit.
- Configure the MPI launch method supported by the cluster.

The script uses `srun`, but some installations may require
additional MPI options.

## Output files

Slurm writes the job's standard output to:

`slurm-<jobid>.out`

LAMMPS also writes its log to:

`log.<jobid>.lammps`

The job ID helps keep the outputs of separate submissions apart.

## Notes

The Zheng (2012) force field minimization described elsewhere in this
repository was validated locally using four MPI ranks.

Simulation input files and any required structure or force-field
data must be provided separately.
