# Paper 1 — Figure 2: ZIF-8 unit-cell size versus temperature

This directory contains a **new, standalone reconstruction** of Figure 2 from:

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam (2023), "Evaluation of ZIF-8 flexible force fields for structural and mechanical properties", *Microporous and Mesoporous Materials* **348**, 112406. [DOI](https://doi.org/10.1016/j.micromeso.2022.112406).

The original notebook is preserved separately at `figures/historical-notebooks/tstability/tstab-16-june.ipynb` in the PhD repository. **This script is newly written code, not the original plotting implementation.** It follows notebook cells 2–8, especially the cell labeled `# Plotting FF (manuscript)`, and was compared visually against `zheng_tstab_new.pdf` in the archived revised manuscript.

## Data provenance

| Package file | Archived source | Meaning |
|---|---|---|
| `data/zheng_tstability` | `Repos/tstability/zheng_tstability` | Temperature (K), 2×2×2 supercell volume (Å³) for Zheng (2012) FF1 |
| `data/zhou.txt` | `ZIF8_2ndSubmission/AFTER RESUBMISSION/Changes/Including experimental data/VvsT/wu digitized/zhou.txt` | Five digitized experimental temperature (K) and cell-length (Å) values attributed in the manuscript to Zhou et al. (2008) |

`zheng_tstability` is copied byte-for-byte from the original archived table. `zhou.txt` contains the same numerical values, with **Windows CRLF line endings normalized to LF** for the Git repository. Cite the original experimental sources, and review redistribution conditions for digitized data before public release.

The three 0 K minimization values and the Park et al. (2006) experimental point are taken from **hardcoded values in the historical notebook**, not from separate independently recovered raw output files:

| Source / method | Unit-cell size (Å) |
|---|---:|
| Serial CG with box relaxation | 16.954967 |
| Alternating SD and CG with box relaxation | 16.8182815 |
| Eigenmode-following | 16.71095288 |
| Park et al. experimental point at 258 K | 16.991 |

These original notebook values should be linked to primary calculation files if subsequently recovered.

## Numerical method

- The notebook converts Zheng (2012) supercell volumes to cubic-equivalent unit-cell size using `L = 0.5 * cbrt(V)`.
- A piecewise-linear spline (`k=1` in the original SciPy notebook) is reproduced using NumPy linear interpolation and endpoint extrapolation. SciPy is not required for the reconstruction.
- The extrapolated unit-cell size at 0 K is **16.716242 Å**; the eigenmode-following value is **16.710953 Å**, consistent with the published caption.
- Marker types, plotting ranges, and series labels follow the archived notebook. Exact font rendering can differ by Matplotlib version.

## Run in the PhD repository virtual environment

```bash
python -m unittest discover -s tests -v
python plot_figure2.py
```

These commands can be run from this package directory. The script also works from elsewhere because it resolves input files relative to its own location:

```bash
python /path/to/plot_figure2.py --output-dir /tmp/figure2-output
```

Generated files:

- `outputs/figure2_temperature_stability.png`
- `outputs/figure2_temperature_stability.pdf`

Six automated tests check the archived data, unit conversions, 0 K extrapolation, experimental points, plotted series and file generation.

## Scope and limitations

This reconstructs the **figure-generation step**, not the full molecular dynamics simulations or the complete provenance of each experimental digitization. The archived notebook was not rerun unchanged; it contains absolute Windows paths and historical exploratory code. The original experimental papers and force-field references should be cited when the reconstructed data are redistributed.
