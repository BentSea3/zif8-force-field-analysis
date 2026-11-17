# Figure 4 — Elastic constants versus pressure

This directory reconstructs the **five panels of Figure 4** in:

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, D. Dubbeldam,
"Evaluation of ZIF-8 flexible force fields for structural and mechanical
properties," *Microporous and Mesoporous Materials* **348** (2023), 112406.
https://doi.org/10.1016/j.micromeso.2022.112406

## What is original and what is reconstructed?

- `data/sim/`: the archived four-column `Repos/ecs/` tables for five force
  fields. Their numerical contents are preserved; the files are not new
  calculations and do not reproduce the underlying RASPA simulations.
- `data/reference/maulDFT.dat`: the archived M06-2X DFT numerical table
  (line endings normalized from Windows CRLF to LF; numbers unchanged).
- `plot_figure4.py`: **new reconstruction** of plotting logic. The original
  plotting notebook `ecs/ecs_raspa.ipynb` was preserved separately under
  `figures/historical-notebooks/`; its surviving active plot is only for FF2.
- `outputs/`: five generated PDFs and five PNGs (one pair per force field).
- `tests/`: automated checks for scientific input tables, series, panel order,
  units, and figure generation.

The plotted components are C11 (black), C12 (red), and C44 (blue), all in GPa,
versus pressure in GPa. Force-field results use filled symbols; M06-2X DFT uses
open symbols and dashed connecting lines. Additional points at 0 GPa show
B3LYP DFT (crosses) and Brillouin-scattering measurements (green-edged triangles).

### Panel mapping

| Panel | Force field | Simulation data file |
|---|---|---|
| FF1 | Zheng (2012) | `data/sim/zheng.dat` |
| FF2 | Hu (2012) | `data/sim/hu.dat` |
| FF3 | Zhang (2013) | `data/sim/zhang.dat` |
| FF4 | Wu (2014) | `data/sim/wu.dat` |
| FF5 | Weng–Schmidt (2019) | `data/sim/schmidt.dat` |

The submitted paper's LaTeX combined five separate PDFs named
`zheng2_upd.pdf`, `hu_corr.pdf`, `zhang2_upd.pdf`, `wu2_upd.pdf`, and
`schmidt2_upd.pdf`. This reconstruction writes separate panels of the same
scientific content rather than recreating the original paper's composite layout.

## Data provenance and citations

The numeric B3LYP and Brillouin points are transcribed from cell 3 of the
archived `ecs_raspa.ipynb`:

- B3LYP: `[0.0, 11.038, 8.325, 0.943]`
- Brillouin: `[0.0, 9.52, 6.87, 0.97]`

Each array lists pressure, C11, C12, C44 in GPa. In the submitted manuscript,
the B3LYP DFT and Brillouin values are credited to **Tan et al. (2012)**,
with Brillouin measurements at **295 K**. The M06-2X data are credited to
**Maul et al. (2019)**. These are comparative results derived from prior
publications, not original experimental measurements made in this work.

Original input: the author's historical PhD backup (`Documents/Repos/ecs/`).
The numerical tables were examined, but the RASPA calculations were **not
rerun**. Redistribution of reference points should be checked against the
original sources and applicable licensing requirements.

## Running the reconstruction

From this directory, with NumPy and Matplotlib installed:

```bash
python -m unittest discover -s tests -v
python plot_figure4.py
```

Or select an output directory:

```bash
python plot_figure4.py --output-dir /path/to/output
```

The script uses only relative data paths and works without a display.
The generated PNG and vector PDF files are found in `outputs/`.

## Verification and limitations

- The five output panels have been visually compared with the separate PDFs
  referenced in the archived submitted manuscript.
- Automated tests verify the archived tabular shapes, specific zero-pressure
  values, panel mapping, marker series, and generation of ten output files.
- Plot styling and placement were reconstructed from the surviving FF2 notebook
  plot and the archived PDFs. **Pixel-for-pixel identity is not claimed.**
- The archival notebook uses hardcoded Windows paths and should not be treated
  as the currently runnable implementation.
