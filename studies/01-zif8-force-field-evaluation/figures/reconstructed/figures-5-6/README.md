# ZIF-8 Paper 1: reconstructed Figures 5 and 6

Reconstruction of minimization plots used in Acuna-Yeomans et al., *Microporous and Mesoporous Materials* **348** (2023), 112406, https://doi.org/10.1016/j.micromeso.2022.112406.

**Provenance and limitations.** This Python program was written in November 2026 by reviewing archived numerical data and submitted-manuscript PDF figures. **It is not the original plotting code used to prepare the 2022 manuscript.** No simulations are rerun. The source dataset is preserved byte-for-byte, except for its `.txt` filename extension.

## Source data

`data/min_data_lammps_restart.txt`, originally:

`viajeFOA/ZIF-8 flexible FF characterization/EC_minimization/min analysis/zheng2012/min_data_lammps_restart`

The dataset has 71 rows, 6 columns. Identifications strongly supported by the manuscript and visual comparisons:

- Column 0: minimization iteration (0–70)
- Column 1: energy in Kelvin-equivalent units (convert by `KELVIN_PER_KCAL_MOL = 4184 / R`, with `R = 8.31446261815324` J/(mol K))
- Column 3: count of negative eigenvalues

Columns 2, 4 and 5 remain unlabeled because their scientific meaning has not been established here. For the two logarithmic figures, plotting begins at iteration 1, as in the original submitted graphs; iteration 0 is still retained for checks.

## Outputs and accuracy

Running `plot_figures.py` creates three plots, in PNG and vector PDF formats:

- `figure5_negative_eigenvalues`: reproduces the Figure 5 series and characteristic eigenvalue rebound near steps 38–51.
- `figure6a_energy_full`: reproduces the energy series from Figure 6a and includes one **provisional, inferred** CG reference at step-0 energy (−7957.934 kcal/mol). It agrees with the approximate teal dashed line in the submitted figure but is **not independently verified** to be the underlying CG minimum.
- `figure6b_energy_zoom`: reproduces the zoomed red energy curve (steps 30–70). The CG step-0 reference is outside its range.

The original figures also display two other horizontal energy comparisons: **alternating SD/CG** (blue), and **CG after 0.5 K MD** (purple). Their numeric values were **not recovered in the archive**. They are omitted by default. Do **not** infer them from plot pixels and present them as original scientific data. Once original values are found, supply them via the command-line arguments below. The code uses figure styles and ranges similar to the submitted plots, not a pixel-perfect reproduction.

## Run in WSL/Linux

Requires Python 3, NumPy, and Matplotlib:

```bash
python3 -m pip install numpy matplotlib
python3 plot_figures.py
python3 -m unittest discover -s tests -v
```

If `python3 -m pip` is constrained by your system environment, use a virtual environment (`python3 -m venv .venv`) and install there. No absolute filesystem paths are used.

If independently verified reference energies become available, rerun with:

```bash
python3 plot_figures.py \
  --sd-cg-energy-kcal MEASURED_VALUE \
  --cg-after-md-energy-kcal MEASURED_VALUE
```

Do not copy literal `MEASURED_VALUE`; use the verified numerical energy in kcal/mol.

To omit the provisional step-0 CG reference as well:

```bash
python3 plot_figures.py --no-inferred-cg
```

## Manuscript evidence used

The submission's `manuscript_main.tex` embeds `images/zheng_bakers.pdf` for Figure 5 and `images/zheng_bakers2.pdf`, `images/zheng_bakers2_zoom.pdf` for Figure 6. Its caption identifies the methods and red/teal/blue/purple conventions. The PDFs supplied in the historical archive were reviewed to choose axis limits, scales, and labels. They are **not bundled**, to separate archival reference material from reconstructed figure outputs.

This project can be placed later under `studies/01-zif8-force-field-evaluation/figures/reconstructed-fig-05-06/` in the local PhD repository. Publication to GitHub should follow the existing audit and attribution checks.
