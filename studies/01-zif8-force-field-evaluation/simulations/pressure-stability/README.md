# ZIF-8 pressure-stability simulations

## Background

These are selected LAMMPS inputs from the pressure-stability calculations performed for:

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam (2023).
"Evaluation of ZIF-8 flexible force fields for structural and mechanical properties."
*Microporous and Mesoporous Materials*, 348, 112406.

[Publication DOI](https://doi.org/10.1016/j.micromeso.2022.112406)

I recovered the original input scripts and starting structures for five force fields at a target pressure of 1,000 atm (approximately 0.1013 GPa).

These calculations contributed to the pressure-dependent lattice parameters plotted in Figure 3 of the paper.

## Available calculations

| Force field | Directory | Temperature | Starting data file |
|---|---|---:|---|
| Zheng (2012) | `zheng2012/` | 300 K | `data.zheng2012.supercell.onlytopology` |
| Hu (2012) | `hu2012/` | 300 K | `data.hu2012.supercell.onlytopology` |
| Zhang (2013) | `zhang2013/` | 300 K | `data.zhang2013.supercell` |
| Wu (2014) | `wu2014/` | 300 K | `data.wu2014.supercell.onlytopology` |
| Weng–Schmidt (2019) | `schmidt2019/` | 298 K | `data.supercell222` |

Each directory contains:

- `sinput.in`: the original LAMMPS simulation input.
- A LAMMPS data file containing the initial structure, atom types, and molecular topology.

The force-field coefficients are defined in `sinput.in` for Zheng, Hu, and Wu. For Zhang and Weng–Schmidt, they are stored in the LAMMPS data file.

The inputs use a 2 × 2 × 2 ZIF-8 supercell with 2,208 atoms.

## Origin of the files

The starting data files were generated with Sahuaro, the Python program I developed to prepare molecular topology files for LAMMPS.

The force-field parameters were taken from the corresponding published models and incorporated into the simulation inputs used during my PhD.

The parameter sets and their implementation in LAMMPS and RASPA are also described in the [Supporting Information](https://pure.uva.nl/ws/files/177263524/1-s2.0-S1387181122007247-mmc1.pdf) accompanying our paper.

I recovered these files from the `ZIF-8-Definitive` research archive, under the following directories:

| Force field | Original directory |
|---|---|
| Zheng | `1-Zheng2012/p_stability/anisotropic/300K/P_0.1GPa` |
| Hu | `2-Hu2012/p_stability/anisotropic/1test/P_0.1GPa` |
| Zhang | `5-Zhang2013/p_stability/anisotropic/300K/P_0.1GPa` |
| Wu | `3-Wu2014/p_stability/anisotropic/300K/P_0.1GPa` |
| Weng–Schmidt | `6-Schmidt2019/p_stability/anisotropic/1runs/P_0.1GPa` |

The ten files included here are unchanged copies of the recovered inputs. Their SHA-256 checksums were verified against the archived files before inclusion.

## Simulation setup

The calculations use periodic boundary conditions and anisotropic pressure control.

The original workflows include energy minimization followed by NPT equilibration and production. The standard calculations inspected at this pressure used 1,000,000 MD steps for each NPT stage.

The exact interaction styles, force-field parameters, pressure-control settings, and other simulation parameters are preserved in the original input scripts and data files.

Some force fields use different interaction styles, cutoffs, or special-bond scaling. These differences have not been standardized.

## Running a calculation

LAMMPS with the required molecular interaction styles and MPI support is needed.

For example, from the `zheng2012/` directory:

```bash
mpirun -np 4 lmp -in sinput.in
```

The original input runs the historical minimization and MD workflow, which can be computationally expensive. It is not a short test calculation.

Outputs should preferably be generated in a separate working directory to avoid mixing new simulation results with the recovered inputs.

A generic [Slurm submission template](../../../../templates/slurm/) is also available, although it has not been validated through an actual HPC submission.

## Validation

I checked the five input pairs using LAMMPS dated 22 July 2025 with four MPI ranks.

For each calculation, I prepared a separate zero-step test from the original input. The tests retained the force-field definitions and starting structures, but stopped before minimization and dynamics.

All five initialization tests completed successfully.

These tests confirm that the recovered inputs can be read and their interactions initialized with the newer LAMMPS version. They do not establish that the original full-length trajectories can be reproduced.

I also performed shortened NPT simulations for Wu and Zhang using separate historical inputs at 258 K. Those runs are not direct reproductions of the 300 K calculations included here.

## Relationship to Figure 3

The plotting data in Figure 3 were traced to the historical pressure-stability simulations for all five force fields.

All 52 simulated data points were matched to the archived processed production averages within the precision of the plotting tables.

The complete comparison, including the historical source directories, sampling intervals, and temperature differences, is described in the [Figure 3 reconstruction documentation](../../figures/reconstructed/figure-3/).

The files in this directory provide representative starting inputs from that simulation series. They do not include the complete set of pressure points or the original simulation outputs.

## Limitations

The full historical calculations have not been rerun using the newer LAMMPS version.

The original force-field publications should be cited when these models are reused.

The recovered data files and input scripts preserve the historical research setup; they have not been redesigned or optimized for current LAMMPS versions.
