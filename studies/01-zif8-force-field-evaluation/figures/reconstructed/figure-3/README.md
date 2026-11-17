# Paper 1 — Figure 3 reconstruction: ZIF-8 lattice parameter versus pressure

This is a **new, standalone Matplotlib reconstruction** of Figure 3 in:

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam, "Evaluation of ZIF-8 flexible force fields for structural and mechanical properties," *Microporous and Mesoporous Materials* **348** (2023), 112406. [DOI](https://doi.org/10.1016/j.micromeso.2022.112406).

It uses the archived numerical input tables and follows the plotting choices from **cell 7 of `Repos/pstability/Pstab_definitive.ipynb`**. The source notebook is not included here and has not been modified; the original code used absolute Windows paths. This is a rewritten, portable implementation, not a claim that the historical notebook was rerun unchanged.

## What the figure shows

- Five simulated ZIF-8 force fields: Zheng (2012; FF1), Hu (2012; FF2), Zhang (2013; FF3), Wu (2014; FF4), and Weng–Schmidt (2019; FF5).
- Experimental comparison points (Chapman et al. and Vervoorts et al.), preserved as the archived digitized numerical tables. The `Im` dataset is not displayed because its plotting line is commented out in the source notebook and does not appear in the submitted Figure 3.
- Pressure-induced drops in the calculated cell size for FF2–FF5.

## Recovered input data

All seven data files in `data/` are **byte-for-byte copies** of the original files in the user-supplied `plotting-repos-original.tar.gz` archive, as checked before packaging.

| File in this package | Original archived path | Columns |
|---|---|---|
| `data/sim/zheng2` | `Repos/pstability/sim/zheng2` | pressure [atm], three supercell lengths [Å], supercell volume [Å³] |
| `data/sim/hu2` | `Repos/pstability/sim/hu2` | same |
| `data/sim/zhang2` | `Repos/pstability/sim/zhang2` | same |
| `data/sim/wu2` | `Repos/pstability/sim/wu2` | same |
| `data/sim/schmidt2` | `Repos/pstability/sim/schmidt2` | same |
| `data/exp/chapman` | `Repos/pstability/exp/chapman` | pressure [GPa], unit-cell length [Å] |
| `data/exp/vervoorts` | `Repos/pstability/exp/vervoorts` | same |

The notebook converts simulated pressure from atm to GPa using `pressure_atm / 9869.23266716`, and converts the archived 2×2×2 supercell volume to a unit-cell length using `0.5 * volume_A3 ** (1/3)`. This formula follows the historical notebook. It assumes a cubic-equivalent length; it is not an independently recomputed lattice parameter from an anisotropic unit cell.

## Running

Using the parent PhD repository's active virtual environment (NumPy and Matplotlib):

```bash
python -m unittest discover -s tests -v
python plot_figure3.py
```

Run these from this directory. The script also works from any current directory, since file paths are relative to its source location:

```bash
python /path/to/plot_figure3.py --output-dir /tmp/figure3-test
```

The files created in `outputs/` are:

- `figure3_pressure_stability.png`
- `figure3_pressure_stability.pdf`

## Validation and limitations

- The figure was visually compared with `images/all_pstability.pdf` from the archived final manuscript in `ZIF8_2ndSubmission/AFTER RESUBMISSION/Submission files BIEN/Manuscript_Revised/`.
- The plotted series, numerical locations, legend, marker and line styles, and axis ranges match the published figure closely. Different Matplotlib versions may affect fonts, spacing, and rendering; pixel-identical reproduction is not asserted.
- Six automated tests cover all five simulation datasets, conversions, collapse behavior, experimental inputs, plotted series, and generated output files.
- Data are **archived historical analysis tables**; no molecular dynamics simulations have been rerun. Their provenance should be documented alongside the simulation inputs before claiming end-to-end reproducibility.
- The experimental data are historical digitizations of published results. Cite the original experimental sources and review any redistribution conditions when publishing the data files.
