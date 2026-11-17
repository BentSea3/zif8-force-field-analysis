# Figure 7 — CG deformation sensitivity versus eigenmode-following

This folder reconstructs Figure 7(a–b) of:

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam,
"Evaluation of ZIF-8 flexible force fields for structural and mechanical
properties," *Microporous and Mesoporous Materials* **348** (2023), 112406.
https://doi.org/10.1016/j.micromeso.2022.112406

The reconstruction was compared with the **submitted-manuscript** PDFs
`zheng_Cii_box.pdf` and `zheng_Cii_bars.pdf`. It is not a recovered copy of the
original finished plotting code and is not guaranteed pixel-identical to the
journal's published version.

## Outputs

- `outputs/figure7a_elastic_constant_boxplot.pdf` and `.png`: 0 K diagonal
  elastic constants C11, C22 and C33 from the CG routine over eight
  box-deformation parameters, with eigenmode-following comparisons.
- `outputs/figure7b_c11_deformation_bars.pdf` and `.png`: C11 for the same
  eight CG parameters and a horizontal eigenmode-following reference.

All elastic constants are plotted in GPa. The x-axis text in panel (b)
follows the historical notebook and the submitted PDF ("Box deformation
parameter / Å"). The manuscript prose is not fully consistent in how it
labels the units of this parameter, so this reconstruction does not attempt
to reinterpret the physical parameter or units independently.

## Numerical provenance

`data/lammps/plottable_lammps` is **byte-for-byte copied** from:

`Documents/Repos/FF1_data/ECs_LAMMPS/0GPa/plottable_lammps`

within the author's historical PhD plotting backup. It contains eight rows
and fourteen numerical columns. The first column is the deformation
parameter, and the next nine columns are diagonal and off-diagonal stiffness
entries as used in cells 5–10 of the original `PlottingData.ipynb` notebook:

- Column 2 (1-based): C11, column 3: C22, column 4: C33.
- The eight deformation parameters are plotted in the **original notebook
  order**: `5e-5`, `5e-4`, `1e-4`, `5e-3`, `1e-3`, `5e-2`, `1e-2`, `1e-1`.
  They have not been sorted or relabeled.

`data/raspa/data_EC_zheng.dat` is **byte-for-byte copied** from:

`Documents/viajeFOA/ZIF-8 flexible FF characterization/EC_minimization/data_EC_zheng.dat`

within the original simulation/plotting backup. Its columns are pressure
(GPa), C11, C12, and C44 (GPa). At zero pressure the Zheng FF1 result is
**C11 = 11.86036 GPa**. For the cubic structure, C11, C22 and C33 are
symmetry-equivalent: the same zero-pressure reference is used for the three
red crosses in Figure 7(a), and for the horizontal red line in Figure 7(b).

The original notebook produces the CG plots but its surviving cells do **not**
include these red eigenmode-following markers; their value has been recovered
from the archived numerical RASPA results, rather than estimated from pixels.

The historical notebook remains unchanged in the main PhD repository at
[`../../historical-notebooks/PlottingData.ipynb`](../../historical-notebooks/PlottingData.ipynb).
The CG numerical results and RASPA results were **not recomputed** from
LAMMPS/RASPA simulation inputs as part of this reconstruction.

Input file SHA-256 hashes:

```
bb88e3d81b94c4661de7054b0532b9b95de4bcb38e88cddfd758febc77a2399b  data/lammps/plottable_lammps
7261fef4de2899edf9c038c92a70ad6b1217a04aede52488bcdad9f82c2e80ee  data/raspa/data_EC_zheng.dat
```

## Running it

With Python, NumPy, and Matplotlib installed:

```bash
python -m unittest discover -s tests -v
python plot_figure7.py
```

You may instead pass `--output-dir /path/to/output` to the plotting script.
The script uses paths relative to its own location and can run headlessly.

## Verification and limitations

- Eight automated tests check both data sources, expected values, the
  original parameter order, plot contents, and generation of all four
  output files.
- The generated box plot and bar chart have been visually inspected against
  the corresponding archived submitted PDFs.
- The original notebook uses `pandas.DataFrame.boxplot(whis=2.5)`. The
  reconstruction uses Matplotlib with the same 2.5-whisker convention and
  explicit points for all eight CG values; small stylistic differences remain.
- Reference values are traceable to the author's RASPA stiffness table.
  No claim of independently verified physical results or exact pixel-level
  equivalence to the published article is made.
- Before further redistribution, retain the citation to the underlying
  publication and assess any relevant third-party licensing constraints.
