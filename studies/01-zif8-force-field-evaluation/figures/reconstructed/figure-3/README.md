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
- The numerical tables are archived historical analysis data. The original full-length pressure-stability simulations have not been rerun. Shortened modern-LAMMPS validation runs are described below.
- The experimental data are historical digitizations of published results. Cite the original experimental sources and review any redistribution conditions when publishing the data files.

## Tracing the simulation data back to LAMMPS

The archived plotting tables were compared with the original pressure-stability simulations in the `ZIF-8-Definitive` backup.

The historical LAMMPS calculations used anisotropic NPT simulations. The main workflow consisted of minimization, equilibration, and production. For the standard runs inspected at 0.1 GPa, both MD stages contained 1,000,000 steps.

The pressure-directory labels are approximate. For example, `P_0.1GPa` corresponds to a target pressure of 1,000 atm (approximately 0.1013 GPa) in the LAMMPS input.

The simulations were not all performed at the same temperature. For example, the Zheng (2012) curve uses the 300 K calculations, rather than the separate 258 K calculations also present in the archive.

### Comparison with historical production averages

For Zheng (2012), Hu (2012), and Weng–Schmidt (2019), the Figure 3 numerical tables were compared with averages calculated from the archived production-data files. These files contain the thermodynamic measurements saved during the original simulations.

| Force field | Figure 3 points | Points matching archived averages |
|---|---:|---:|
| Zheng (2012) | 11 | 11 |
| Hu (2012) | 10 | 10 |
| Weng–Schmidt (2019) | 12 | 12 |

All 33 points agree within the rounding precision of the plotting tables: four decimal places for the supercell lengths and one decimal place for the volume.

The original averaging scripts used fixed line numbers and column positions to extract data from LAMMPS logs. A newer Python analysis script, [average_lammps_cell.py](../../../analysis/average_lammps_cell.py), identifies thermodynamic blocks by their headers and excludes the minimization stages.

The sampling intervals and lengths were not identical across all historical calculations. Some pressure points near structural transitions used 3,001 or 5,001 measurements instead of 1,001. For example, the archived Weng–Schmidt 1.0 GPa processed dataset contains 3,001 measurements covering steps 0–300,000.

### Wu (2014) and Zhang (2013)

The original LAMMPS logs were recovered for the investigated pressure-stability simulations, but the corresponding processed `.dat` files were not found in the inspected directories.

Production averages calculated directly from the logs are generally close to the Figure 3 values at lower pressures, but they do not consistently match to the rounding precision of the plotting tables.

Larger differences occur at some pressures near structural transitions. The exact historical source and processing procedure for these plotted values remain unresolved.

The archived Figure 3 tables have therefore been preserved without modification.

### Modern LAMMPS validation

Two shortened NPT simulations were also run using a LAMMPS build dated 22 July 2025 and four MPI ranks.

The historical Wu (2014) and Zhang (2013) inputs were copied into separate local working directories. Each of the two 1,000,000-step MD stages was shortened to 100,000 steps.

Both simulations completed successfully.

| Quantity | Wu (2014) | Zhang (2013) |
|---|---:|---:|
| Equilibration steps | 100,000 | 100,000 |
| Production steps | 100,000 | 100,000 |
| Mean production temperature (K) | 258.130 | 257.877 |
| Mean production pressure (atm) | 852.441 | 857.901 |
| Mean conventional-cell volume (Å³) | 4838.740 | 4876.596 |
| Historical conventional-cell volume at 0.1 GPa (Å³) | 4837.823 | 4873.711 |

These runs show that the historical force-field inputs, with shortened run lengths, can complete an NPT workflow using a newer LAMMPS version.

They do not establish statistical equivalence with the original production trajectories or reproduce the full pressure-induced transition behavior.

The pilot simulation outputs remain outside this public repository.
