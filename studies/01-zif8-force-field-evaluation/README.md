
# Evaluation of ZIF-8 flexible force fields for structural and mechanical properties

**Publication:** E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam (2023). *Microporous and Mesoporous Materials*, 348, 112406.

[Publication DOI](https://doi.org/10.1016/j.micromeso.2022.112406)

## About the study

This work evaluates five published flexible force fields for ZIF-8: Zheng (2012), Hu (2012), Wu (2014), Zhang (2013), and Weng–Schmidt (2019).

LAMMPS and RASPA were used to investigate structural and mechanical properties, including temperature and pressure dependence, elastic constants, and mechanical stability.

## Available code and data

- [LAMMPS analysis](analysis/average_lammps_cell.py): averages lattice parameters, volume, and pressure from LAMMPS thermodynamic output.
- [RASPA elastic analysis](analysis/check_raspa_elastic.py): extracts the stiffness matrix and calculates Voigt elastic moduli.
- [RASPA elastic-property summary](results/raspa_elastic_summary.csv): Hill bulk and shear moduli recovered from archived minimization calculations.
- [Reconstructed Figures 5 and 6](figures/reconstructed/figures-5-6/): Matplotlib plotting code, archived numerical data, tests, and generated figures.

## Validation

The LAMMPS analysis script was checked against archived Zheng (2012) results at approximately 0.1 and 0.2 GPa.

The RASPA analysis script was checked against an archived Zheng (2012) elastic calculation.

Both scripts have automated tests in the repository's root `tests/` directory.

## Figure reconstruction

The figure-generation workflows are being reconstructed from historical notebooks, numerical data, and figures preserved in the original research archive.

Figures 5 and 6 were reconstructed from an archived Zheng (2012) minimization dataset.

The original plotting script was not recovered. The new implementation reproduces the negative-eigenvalue behavior and energy-convergence trajectory, but two comparison-energy reference lines in Figure 6 remain unresolved.

See the [figure reconstruction documentation](figures/reconstructed/figures-5-6/README.md) for details.

## Conference presentation

Results from this research were presented at the 14th International Conference on Fundamentals of Adsorption (FOA14), Broomfield, Colorado, USA, 22–27 May 2022.

**Presentation:** "Characterization of ZIF-8 flexible force fields according to their mechanical and structural properties."

**Format:** Oral presentation (pre-recorded).

## Related software

Some original LAMMPS topology files were generated using Sahuaro, a Python program developed to prepare molecular topology data.

The historical topology-generation notebooks are being reviewed separately before inclusion in this public repository.

## Limitations

This is a curated archive, not a complete reproduction of the published simulations.

Most simulation inputs, trajectories, restart files, and original simulation outputs are not yet included.

The correspondence between the archived RASPA elastic-property summary and the published tables has not yet been fully verified.

Original historical research files are being reviewed for provenance and redistribution permissions before publication.

