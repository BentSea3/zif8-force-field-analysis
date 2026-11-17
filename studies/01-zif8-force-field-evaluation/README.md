# Evaluation of ZIF-8 flexible force fields for structural and mechanical properties

**Publication:** E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam (2023). *Microporous and Mesoporous Materials*, 348, 112406.

[Publication DOI](https://doi.org/10.1016/j.micromeso.2022.112406)

## About the study

This work evaluates five published flexible force fields for ZIF-8: Zheng (2012), Hu (2012), Wu (2014), Zhang (2013), and Weng–Schmidt (2019).

LAMMPS and RASPA were used to investigate structural and mechanical properties, including temperature and pressure dependence, elastic constants, and mechanical stability.

## Available analysis code and data

- [LAMMPS analysis](analysis/average_lammps_cell.py): extracts and averages lattice parameters, volume, and pressure from LAMMPS thermodynamic output.
- [RASPA elastic analysis](analysis/check_raspa_elastic.py): extracts the stiffness matrix and calculates Voigt elastic moduli.
- [RASPA elastic-property summary](results/raspa_elastic_summary.csv): Hill bulk and shear moduli recovered from archived minimization calculations.

These scripts were recovered and adapted from the historical research archive. They represent selected analysis workflows rather than a complete simulation pipeline.

## Publication figure reconstructions

Figures 2–7 have been reconstructed using numerical data and historical analysis code recovered from the original research archive.

The reconstructed scripts use relative paths, include automated tests, and generate figures without rerunning the underlying LAMMPS or RASPA simulations.

| Figure | Description | Reconstruction |
|---|---|---|
| 1 | ZIF-8 structure and pore windows | Original visualization workflow not yet recovered |
| 2 | Temperature-dependent unit-cell size | [Figure 2](figures/reconstructed/figure-2/) |
| 3 | Pressure-dependent unit-cell size | [Figure 3](figures/reconstructed/figure-3/) |
| 4 | Pressure-dependent elastic constants for five force fields | [Figure 4](figures/reconstructed/figure-4/) |
| 5 | Negative eigenvalues during minimization | [Figures 5–6](figures/reconstructed/figures-5-6/) |
| 6 | Energy evolution during minimization | [Figures 5–6](figures/reconstructed/figures-5-6/) |
| 7 | Elastic constants and deformation parameters | [Figure 7](figures/reconstructed/figure-7/) |

Each reconstruction directory contains plotting code, selected numerical inputs, tests, documentation, and generated figures.

The plotting workflows reproduce selected results from the publication. They should not be interpreted as independent reproduction of the simulations or complete validation of the published results.

### Historical plotting notebooks

The [original plotting notebooks](figures/historical-notebooks/) are preserved unchanged, including their code cells, saved outputs, and historical file paths.

These notebooks document the original exploratory analysis and figure-generation workflow. Some contain intermediate versions of plots or references to files that are no longer available at their original locations.

The historical notebooks are retained as research records and are not guaranteed to run in a modern Python environment.

They are maintained separately from the reconstructed, tested plotting scripts.

## Testing and validation

The LAMMPS analysis script was checked against archived Zheng (2012) results at approximately 0.1 and 0.2 GPa.

The RASPA analysis script was checked against an archived Zheng (2012) elastic calculation.

Automated tests cover these analysis scripts and the reconstructed figure-generation workflows.

From the repository root, run:

```bash
./scripts/run-tests.sh
```

The script executes the available test suites and returns a nonzero exit status if a test fails.

These tests check numerical calculations, data loading, expected properties of archived datasets, and figure generation. Passing tests does not independently validate the underlying simulation results.

## Reproducibility and provenance limitations

This repository is a curated research archive, not a complete reproduction of the published simulations.

- Most original simulation inputs, trajectories, restart files, and simulation outputs are not yet included.
- Figure 1's original visualization workflow has not been recovered.
- Figure 6 contains a reconstructed energy-convergence trajectory and a recovered CG-after-MD comparison. The alternating SD/CG reference remains unresolved.
- Some experimental comparison data were digitized from published sources.
- The correspondence between the archived RASPA elastic-property summary and the published tables has not yet been fully verified.
- Selected historical files and third-party numerical data still require provenance and redistribution-permission review.

These limitations are documented to distinguish archived research results, reconstructed analysis workflows, and independently reproducible calculations.

## Conference presentation

Results from this research were presented at the 14th International Conference on Fundamentals of Adsorption (FOA14), Broomfield, Colorado, USA, 22–27 May 2022.

**Presentation:** "Characterization of ZIF-8 flexible force fields according to their mechanical and structural properties."

**Format:** Oral presentation (pre-recorded).

## Related software

Some original LAMMPS topology files were generated using Sahuaro, a Python program developed to prepare molecular topology data.

The historical topology-generation notebooks are being reviewed separately before inclusion in this public repository.
