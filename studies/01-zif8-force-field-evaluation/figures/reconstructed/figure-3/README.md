# Paper 1 — Figure 3 reconstruction: ZIF-8 lattice parameter versus pressure

This is a **new, standalone Matplotlib reconstruction** of Figure 3 in:

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and D. Dubbeldam, "Evaluation of ZIF-8 flexible force fields for structural and mechanical properties," *Microporous and Mesoporous Materials* **348** (2023), 112406. [DOI](https://doi.org/10.1016/j.micromeso.2022.112406).

It uses the archived numerical input tables and follows the original plotting choices. The source notebook is not included here and has not been modified; the original code used absolute Windows paths. This is a rewritten, portable implementation, not a claim that the historical notebook was rerun unchanged.

## What the figure shows

- Five simulated ZIF-8 force fields: Zheng (2012; FF1), Hu (2012; FF2), Zhang (2013; FF3), Wu (2014; FF4), and Weng–Schmidt (2019; FF5).
- Experimental comparison points (Chapman et al. and Vervoorts et al.), preserved as the archived digitized numerical tables. The `Im` dataset is not displayed because its plotting line is commented out in the source notebook and does not appear in the submitted Figure 3.
- Pressure-induced drops in the calculated cell size for FF2–FF5.

## Recovered input data

All seven data files in `data/` are **byte-for-byte copies** of the original files from my archive.

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

I compared the archived plotting tables with the original pressure-stability calculations in the `ZIF-8-Definitive` backup.

The historical calculations used anisotropic NPT simulations, with minimization followed by equilibration and production. In the standard runs inspected at 0.1 GPa, both MD stages contained 1,000,000 steps.

The pressure-directory labels are approximate. For example, `P_0.1GPa` corresponds to a target pressure of 1,000 atm (approximately 0.1013 GPa) in the LAMMPS input.

### Historical sources of the plotted data

All 52 simulated points in Figure 3 were matched to averages calculated from the archived production-data files.

| Force field | Historical directory under `ZIF-8-Definitive` | Matching points |
|---|---|---:|
| Zheng (2012) | `1-Zheng2012/p_stability/anisotropic/300K` | 11/11 |
| Hu (2012) | `2-Hu2012/p_stability/anisotropic/1test` | 10/10 |
| Zhang (2013) | `5-Zhang2013/p_stability/anisotropic/300K` | 9/9 |
| Wu (2014) | `3-Wu2014/p_stability/anisotropic/300K` | 10/10 |
| Weng–Schmidt (2019) | `6-Schmidt2019/p_stability/anisotropic/1runs` | 12/12 |
| **Total** | | **52/52** |

For every point, the mean supercell lengths agree with the plotting table within its four-decimal-place precision, and the mean supercell volume agrees within its one-decimal-place precision.

The comparisons use historical processed thermodynamic data, such as `P_0.1GPa.dat`, recovered from the simulation directories. They identify the numerical sources of the plotting tables, but do not constitute independent reruns of the original simulations.

### Simulation temperatures

The source directories were important for identifying the correct calculations.

Zheng (2012), Wu (2014), and Zhang (2013) each have archived anisotropic simulations at both 258 K and 300 K. The Figure 3 curves correspond to the **300 K calculations**.

The initially inspected 258 K Wu and Zhang trajectories gave similar volumes at lower pressures, but did not reproduce the Figure 3 values to the precision of the plotting tables. The 300 K datasets match all plotted points, including the additional pressures investigated near structural transitions.

At 1,000 atm, the recovered Hu simulation was run at 300 K, while the Weng–Schmidt simulation was run at 298 K.

### Historical averaging and sampling

The original averaging scripts used fixed line numbers and column positions to extract lattice parameters from LAMMPS logs.

The newer Python script [average_lammps_cell.py](../../../analysis/average_lammps_cell.py) identifies thermodynamic blocks by their headers and excludes minimization stages. It can report equilibration and production blocks separately, even when their timestep numbers restart at zero.

The historical datasets did not all use the same sampling intervals or numbers of measurements.

Most processed datasets contain 1,001 measurements, but several pressure points near structural transitions contain 3,001 or 5,001 measurements. Examples include:

- Hu (2012): 5,300, 5,900, and 5,950 atm — 5,001 measurements.
- Wu (2014): 5,700 atm — 5,001 measurements; 6,400 and 6,600 atm — 3,001 measurements.
- Zhang (2013): 5,600 atm — 3,001 measurements.
- Weng–Schmidt (2019): 8,900 and 10,000 atm — 3,001 measurements.

The Weng–Schmidt 1.0 GPa processed file, for example, contains 3,001 measurements covering steps 0–300,000.

These differences should be considered when comparing the statistical quality of the averages. Matching the archived means does not independently establish equilibration or convergence.

### Modern LAMMPS validation

Two shortened NPT simulations were run using a LAMMPS build dated 22 July 2025 and four MPI ranks.

The historical Wu (2014) and Zhang (2013) inputs from the **258 K simulations** were copied into separate local working directories. Each of the two original 1,000,000-step MD stages was shortened to 100,000 steps.

Both simulations completed successfully.

| Quantity | Wu (2014) | Zhang (2013) |
|---|---:|---:|
| Equilibration steps | 100,000 | 100,000 |
| Production steps | 100,000 | 100,000 |
| Mean production temperature (K) | 258.130 | 257.877 |
| Mean production pressure (atm) | 852.441 | 857.901 |
| Mean conventional-cell volume (Å³) | 4838.740 | 4876.596 |
| Historical 258 K production mean at 1,000 atm (Å³) | 4837.823 | 4873.711 |

The production volumes are close to those obtained from the corresponding historical 258 K simulations.

These pilot runs demonstrate that the historical inputs, with shortened run lengths, can complete minimization, equilibration, and production using a newer LAMMPS version.

They are **not direct reproductions of the Figure 3 curves**, which use the separate 300 K Wu and Zhang calculations.

The pilots also do not establish statistical equivalence with the historical trajectories or reproduce the full pressure-induced transition behavior.

The pilot outputs remain outside this public repository.
