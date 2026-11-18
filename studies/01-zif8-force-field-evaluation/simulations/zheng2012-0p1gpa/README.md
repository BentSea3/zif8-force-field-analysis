
# Revisiting a Zheng (2012) ZIF-8 Minimization

## Background

As part of organizing the simulation work from my PhD, I wanted to check whether some of the original calculations could still be run with a newer version of LAMMPS.

This example comes from the force-field comparison published in:

Acuna-Yeomans et al. (2023), *Microporous and Mesoporous Materials*, 348, 112406.
https://doi.org/10.1016/j.micromeso.2022.112406

I started with a relatively simple case: minimizing a ZIF-8 structure using the Zheng (2012) force field at 0.1 GPa.

The aim was not to reproduce the entire paper, but to recover one calculation, run it again, and see how closely the results matched.

## The calculation

The system is a 2 x 2 x 2 ZIF-8 supercell containing 2,208 atoms. The original calculation used conjugate-gradient minimization with anisotropic box relaxation, targeting a pressure of 986.923 atm (approximately 0.1 GPa).

I recovered the original LAMMPS input script and the starting structure generated with Sahuaro. Both files were checked against the historical archive and found to be identical.

For the comparison, I used:

- **Original run:** LAMMPS 29 Oct 2020
- **New run:** LAMMPS 22 Jul 2025, using 4 MPI ranks

The original script allowed up to one million minimization iterations per stage. For the new run, I reduced that limit to 3,000 iterations and 30,000 force evaluations per stage. The force field, pressure target, minimization method, and zero tolerances were left unchanged.

## Comparing the results

Both LAMMPS versions reached similar final energies, pressures, and cell dimensions.

| Quantity | Original (2020) | New run (2025) |
|---|---:|---:|
| Final energy (kcal/mol) | -7961.375 | -7967.224 |
| Final pressure (atm) | 1019.945 | 1003.716 |
| Supercell volume (Å³) | 39136.460 | 39038.797 |
| First minimization iterations | 2398 | 2639 |
| Second minimization iterations | 1 | 1 |

One interesting detail is that neither calculation stopped because it reached a force tolerance. Both ended when the line search could no longer find a usable step.

This means that, while the original behavior was reproduced, neither result should automatically be considered fully converged.

## Comparing the structures

Matching energies and lattice parameters is useful, but I also wanted to know whether the atoms ended up in similar positions.

I wrote a small Python script to compare the two final LAMMPS data files. It matches atoms by ID, checks their types, molecule IDs, and charges, and accounts for periodic boundaries.

Because the final simulation boxes are slightly different, the comparison uses fractional coordinates and maps the atomic displacements into the original reference cell.

The results were:

| Measurement | Difference |
|---|---:|
| RMS atomic displacement | 0.002507 Å |
| Mean displacement | 0.002255 Å |
| 95th percentile | 0.004020 Å |
| Maximum displacement | 0.004088 Å |
| Relative cell-volume change | -0.2495% |

All 2,208 atoms could be matched, and removing a global translation made essentially no difference.

The atomic positions are therefore very similar once the difference in cell dimensions is accounted for. The reported RMS displacement measures differences in the internal configuration, rather than the overall deformation of the box.

## Running the comparison

The comparison script requires Python and NumPy.

```bash
python3 compare_structures.py \
    /path/to/original/data.min \
    /path/to/new/data.min
```

At the moment, the script works with orthogonal LAMMPS cells and assumes that corresponding atoms have the same IDs. It does not attempt to match structures through symmetry operations or atom permutations.

## What I found

The main result is that this calculation could be recovered and rerun with a newer version of LAMMPS, producing a structure very close to the original one.

Both runs report inconsistent image flags warning, which are common in periodic bonded frameworks such as ZIF-8. This warning does not normally affect the energy minimization, however, image flags can matter for operations like unwrapping coordinates or replicating a system within LAMMPS.

There are still some differences in energy, pressure, and cell dimensions. These could be related to numerical differences between LAMMPS versions or their minimization paths, but I haven't established the exact cause.

For now, I consider this a successful check of the historical workflow, rather than proof that the minimization reached a fully converged structure.

## Files and next steps

The comparison script is included here so that the procedure can be inspected and reused.

The original simulation inputs and the two sets of outputs are currently kept in my local research archive while I review their provenance and redistribution status. This means the numerical comparison cannot yet be reproduced using only the files in this repository.

The next steps are to make a small, self-contained simulation example available, add automated tests for the structural comparison, and document how to run the calculation on an HPC cluster.
