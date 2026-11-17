# PhD computational research

This repository contains selected code, numerical data, and analysis workflows from my PhD research on molecular simulations of porous materials.

The aim is to document the computational methods behind my publications, preserve useful research code, and make the associated analyses easier to reproduce.

The archive is being developed one study at a time. It currently focuses on the evaluation of flexible force fields for ZIF-8.

## Studies

### 01 — ZIF-8 flexible force-field evaluation

[Evaluation of ZIF-8 flexible force fields for structural and mechanical properties](studies/01-zif8-force-field-evaluation/)

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam (2023).

*Microporous and Mesoporous Materials*, 348, 112406.

[Publication](https://doi.org/10.1016/j.micromeso.2022.112406)

The study compares five published flexible force fields for ZIF-8 using LAMMPS and RASPA simulations, focusing on structural properties, elastic constants, and mechanical stability.

## Repository contents

- `analysis/`: Python scripts for extracting lattice parameters from LAMMPS logs and elastic properties from RASPA output.
- `results/`: elastic-property results recovered from archived calculations.
- `tests/`: automated tests for the analysis scripts.
- `studies/01-zif8-force-field-evaluation/figures/`: reconstructed plotting workflows, numerical inputs, tests, and generated figures.

The analysis and results directories will be moved under their corresponding study as the repository is reorganized.

## Python environment

Requires Python 3.12.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Tests

Run the analysis tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

Run the reconstructed Figures 5–6 tests:

```bash
python -m unittest discover \
    -s studies/01-zif8-force-field-evaluation/figures/reconstructed/figures-5-6/tests -v
```

## Scope and provenance

This is a curated research archive, not a complete reproduction package for the original simulations.

The numerical analyses and reconstructed plotting workflows are being validated against archived research data. The underlying molecular dynamics simulations have not been rerun as part of this repository.

Historical code, simulation inputs, and third-party scientific files are being reviewed for provenance and redistribution permissions before inclusion.

The documentation distinguishes recovered original data from newly written or reconstructed code.
