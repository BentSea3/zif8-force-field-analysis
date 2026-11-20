# PhD computational research

This repository contains selected code, numerical data, and analysis workflows from my PhD research on molecular simulations of porous materials.

The aim is to document the computational methods behind my publications, preserve useful research code, and make the associated analyses easier to reproduce.

The archive is being developed one study at a time, with an emphasis on documenting the provenance of historical research materials and improving the reproducibility of selected workflows.

## Studies

### 01 — ZIF-8 flexible force-field evaluation

[Evaluation of ZIF-8 flexible force fields for structural and mechanical properties](studies/01-zif8-force-field-evaluation/)

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam (2023).

*Microporous and Mesoporous Materials*, 348, 112406.

[Publication DOI](https://doi.org/10.1016/j.micromeso.2022.112406)

This study compares five published flexible force fields for ZIF-8 using LAMMPS and RASPA simulations, focusing on structural properties, elastic constants, and mechanical stability.

The available materials include:

- Python scripts for analyzing LAMMPS and RASPA outputs.
- Selected numerical results recovered from archived calculations.
- [Reconstructed plotting workflows](studies/01-zif8-force-field-evaluation/figures/reconstructed/) for publication Figures 2–7, with numerical inputs, automated tests, and generated figures.
- [Historical Jupyter notebooks](studies/01-zif8-force-field-evaluation/figures/historical-notebooks/) preserved without modification.

Figure 1's original visualization workflow has not yet been recovered. The alternating SD/CG comparison-energy reference in Figure 6 remains unresolved.

See the [study documentation](studies/01-zif8-force-field-evaluation/) for the complete figure inventory, methodology, and limitations.

## Repository organization

- `studies/`: research materials organized by publication or study.
- `tests/`: automated tests for the analysis scripts.
- `scripts/`: repository-level utilities, including the test runner.
- `requirements.txt`: Python dependencies for the available analysis and plotting workflows.

Each study may contain original research files, reconstructed code, numerical data, and documentation. Historical materials and newly developed implementations are identified separately.

## Python environment

The available Python workflows have been tested with Python 3.12.

Create and activate a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Running the tests

Run all available analysis and figure-reconstruction tests from the repository root:

```bash
./scripts/run-tests.sh
```

The test runner discovers the available test suites and returns a nonzero exit status if any suite fails.

The tests cover numerical calculations, archived-data checks, and figure generation. Passing tests does not independently validate the underlying molecular simulations.

## Scope and provenance

This is a curated research archive, not a complete reproduction package for the original simulations.

The reconstructed plotting scripts generate selected publication figures from archived numerical data. They do not rerun the original LAMMPS or RASPA simulations.

The historical notebooks preserve parts of the original research workflow, including intermediate code and saved outputs. They are not necessarily executable in a modern environment.

Five representative pressure-stability input sets are included, but the full set of simulation inputs, trajectories, restart files, and outputs is not. Selected historical and third-party materials still require provenance and redistribution-permission review.

The repository is being developed incrementally, with the aim of improving documentation, testing, and reproducibility while retaining a clear distinction between original research materials and reconstructed software.
