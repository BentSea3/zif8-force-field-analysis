# ZIF-8 Paper 1: reconstructed Figures 5 and 6

Reconstruction of minimization plots used in Acuna-Yeomans et al., *Microporous and Mesoporous Materials* **348** (2023), 112406, https://doi.org/10.1016/j.micromeso.2022.112406.

**Provenance and limitations.** This Python program was written in November 2026 by reviewing archived numerical data and submitted-manuscript PDF figures. **It is not the original plotting code used to prepare the 2022 manuscript.** No simulations are rerun. The source dataset is preserved byte-for-byte, except for its `.txt` filename extension.

## Source data

`data/min_data_lammps_restart.txt`, originally:

`viajeFOA/ZIF-8 flexible FF characterization/EC_minimization/min analysis/zheng2012/min_data_lammps_restart`

The dataset has 71 rows and six columns. All 426 numerical entries match the iteration records in the archived original RASPA output:

- Column 0: minimization iteration (0–70)
- Column 1: energy in K (convert using `KELVIN_PER_KCAL_MOL = 4184 / R`, where `R = 8.31446261815324` J/(mol K))
- Column 2: simulation-cell volume in Å³
- Column 3: number of negative Hessian eigenvalues
- Column 4: RMS gradient (units not independently established)
- Column 5: maximum gradient (units not independently established) For the two logarithmic figures, plotting begins at iteration 1, as in the original submitted graphs; iteration 0 is still retained for checks.

## Outputs and accuracy

Running `plot_figures.py` creates three plots, in PNG and vector PDF formats:

- `figure5_negative_eigenvalues`: reproduces the Figure 5 series and characteristic eigenvalue rebound near steps 38–51.
- `figure6a_energy_full`: reproduces the energy series and includes the teal step-0 CG-structure reference (−7957.934126 kcal/mol), evaluated by RASPA. The matching CG structure is established, but the equivalent LAMMPS energy differs because the programs' energy conventions have not been fully reconciled.
- `figure6b_energy_zoom`: reproduces the zoomed red energy curve (steps 30–70). The CG step-0 reference is outside its range.

The **CG after 0.5 K MD** reference (purple) is now included by default at **−8063.30080162371 kcal/mol**, as reported in an archived LAMMPS final CG minimization with `units real`. Its relaxed lattice parameter (16.712274 Å) agrees with the manuscript (16.7122 Å).

The **alternating SD/CG** reference (blue) remains omitted: the matching 16.725 Å source structure was identified, but the archived candidate energies do not establish which value was plotted. Do **not** infer the missing value from plot pixels and present it as original numerical data. The plot styles and ranges approximate the submitted manuscript; pixel-perfect reproduction is not claimed.

## Run in WSL/Linux

Requires Python 3, NumPy, and Matplotlib:

```bash
python3 -m pip install numpy matplotlib
python3 plot_figures.py
python3 -m unittest discover -s tests -v
```

If `python3 -m pip` is constrained by your system environment, use a virtual environment (`python3 -m venv .venv`) and install there. No absolute filesystem paths are used.

The purple reference is plotted automatically. You can override it using `--cg-after-md-energy-kcal VALUE` for comparison. If the blue reference is independently established, supply its verified value:

```bash
python3 plot_figures.py --sd-cg-energy-kcal VERIFIED_VALUE
```

Do not substitute an image-derived estimate for `VERIFIED_VALUE`.

To omit the provisional step-0 CG reference as well:

```bash
python3 plot_figures.py --no-inferred-cg
```

## Manuscript evidence used

The submission's `manuscript_main.tex` embeds `images/zheng_bakers.pdf` for Figure 5 and `images/zheng_bakers2.pdf`, `images/zheng_bakers2_zoom.pdf` for Figure 6. Its caption identifies the methods and red/teal/blue/purple conventions. The PDFs supplied in the historical archive were reviewed to choose axis limits, scales, and labels. They are **not bundled**, to separate archival reference material from reconstructed figure outputs.

## Original calculation provenance (private archives)

- **Red trajectory and teal initial energy:** `ZIF-8/22March/RASPA_wLAMMPS_output/zheng2012/1_minimizations_noMD/0GPa/Output/System_0/output_ZIF-8_2.2.2_298.000000_0.data` in the 2021 ZIF-8 backup.
- **Purple reference:** `ZIF-8/lammps/ZIF-8-Definitive/1-Zheng2012/march22/2_minimizations_afterMD/0GPa/log.lammps` (final CG energy, after 0.5 K MD).
- **Blue source structure:** `ZIF-8/lammps/ZIF-8-Definitive/1-Zheng2012/march22/1_minimizations_noMD/0GPa/with_nreset_atoms_relax_first/log.lammps` (mean cell edge 16.724974 Å). Its final energy was −8065.914066 kcal/mol, but is **not** assigned to the blue reference because the original plotted value is unverified.

The complete historical LAMMPS/RASPA outputs remain in private backup archives pending provenance and redistribution review. These source paths document how the reconstructed values were traced; the source outputs are not packaged here.
