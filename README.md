# ZIF-8 force-field analysis

Selected Python analysis scripts and results from my PhD research on the structural and mechanical properties of ZIF-8.

## Publication

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, D. Dubbeldam (2023).

"Evaluation of ZIF-8 flexible force fields for structural and mechanical properties."

*Microporous and Mesoporous Materials*, 348, 112406.

[Publication](https://doi.org/10.1016/j.micromeso.2022.112406)

## Research

The study evaluates five published flexible force fields for ZIF-8 using molecular dynamics and energy minimization calculations in LAMMPS and RASPA.

The calculations investigate lattice parameters, pressure and temperature dependence, elastic constants, and mechanical stability.

Results from this work were also presented in an oral presentation at the 14th Fundamentals of Adsorption conference (FOA14), Colorado, USA, in 2022.

## Contents

- `analysis/average_lammps_cell.py`: calculates average lattice parameters, volume, and pressure from LAMMPS thermodynamic output.
- `analysis/check_raspa_elastic.py`: reads a RASPA stiffness matrix, calculates Voigt elastic moduli, and reports stability eigenvalues.
- `results/raspa_elastic_summary.csv`: Hill bulk and shear moduli recovered from archived RASPA minimizations for five force fields.
- `tests/`: automated tests using synthetic LAMMPS and RASPA output data.

## Running the tests

Requires Python 3. No additional Python packages are needed.

```bash
python3 -B -m unittest discover -s tests -v
```

## Using the analysis scripts

```bash
python3 analysis/average_lammps_cell.py path/to/log.lammps
python3 analysis/check_raspa_elastic.py path/to/output.data
```

## Scope

This repository contains selected analysis code and results, not the complete simulation archive.

The original simulations have not been rerun, and most historical inputs, trajectories, restart files, and simulation outputs are not included.

The results CSV contains values extracted from archived calculations. Their correspondence with the published tables has not yet been fully verified.
