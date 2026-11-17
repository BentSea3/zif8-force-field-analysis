"""Reconstruct Figure 2: ZIF-8 cell size versus temperature (Zheng FF1).

Reference: archived `tstability/tstab-16-june.ipynb`, cells 2-8.
This standalone script is new work; it does not execute the old notebook.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"

# Values copied from original notebook (cell 4), in Å for the unit cell.
SERIAL_CG_BOX_RELAX_A = 33.909934 / 2
ALTERNATING_SD_CG_BOX_RELAX_A = 33.636563 / 2
EIGENMODE_FOLLOWING_A = 33.4219057618165 / 2

# Original notebook cell 3: Park et al. (2006), manually entered point.
PARK_TEMPERATURE_K = 258.0
PARK_CELL_A = 16.991


def load_simulation(directory: Path = DATA) -> tuple[np.ndarray, np.ndarray]:
    """Read temperature [K], 2x2x2 supercell volume [Å^3]; return unit-cell Å."""
    values = np.loadtxt(directory / "zheng_tstability", ndmin=2)
    if values.ndim != 2 or values.shape[1] != 2 or len(values) < 2:
        raise ValueError("Simulation file must have two columns and at least two rows")
    if not np.all(np.isfinite(values)) or np.any(values[:, 1] <= 0):
        raise ValueError("Simulation data must be finite with positive volumes")
    if np.any(np.diff(values[:, 0]) <= 0):
        raise ValueError("Temperatures must be strictly increasing")
    return values[:, 0], 0.5 * np.cbrt(values[:, 1])


def load_zhou(directory: Path = DATA) -> tuple[np.ndarray, np.ndarray]:
    """Read archived digitized temperature [K], unit-cell parameter [Å]."""
    values = np.loadtxt(directory / "zhou.txt", ndmin=2)
    if values.ndim != 2 or values.shape[1] != 2 or not np.all(np.isfinite(values)):
        raise ValueError("Zhou file must contain two finite numerical columns")
    return values[:, 0], values[:, 1]


def linear_interpolate_extrapolate(
    x: np.ndarray, y: np.ndarray, sample: np.ndarray
) -> np.ndarray:
    """Piecewise-linear interpolation, with endpoint linear extrapolation.

    Equivalent to the original InterpolatedUnivariateSpline(..., k=1)
    for these ordered, unique temperatures, without requiring SciPy.
    """
    sample = np.asarray(sample, dtype=float)
    result = np.interp(sample, x, y)
    left = sample < x[0]
    right = sample > x[-1]
    left_slope = (y[1] - y[0]) / (x[1] - x[0])
    right_slope = (y[-1] - y[-2]) / (x[-1] - x[-2])
    result[left] = y[0] + (sample[left] - x[0]) * left_slope
    result[right] = y[-1] + (sample[right] - x[-1]) * right_slope
    return result


def create_figure(directory: Path = DATA) -> plt.Figure:
    temperature, cell = load_simulation(directory)
    zhou_temperature, zhou_cell = load_zhou(directory)

    # Notebook uses 5000 points from 0 to 1050 K, despite x-axis limit at 850 K.
    dense_temperature = np.linspace(0.0, 1050.0, 5000)
    dense_cell = linear_interpolate_extrapolate(temperature, cell, dense_temperature)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlabel(r"Temperature, $T$ / $\mathrm{K}$", fontsize=18)
    ax.set_ylabel(r"Unit cell size, $L_{p}$ / $\mathrm{\AA}$", fontsize=18)
    ax.set_xlim(0.0, 850.0)
    ax.set_ylim(16.7, 17.05)
    ax.set_xticks(np.arange(0, 850, 200))
    ax.set_yticks(np.arange(16.7, 17.05, 0.05))
    ax.tick_params(labelsize=14)

    ax.scatter(temperature, cell, marker="s", facecolor="white",
               edgecolor="black", linewidth=1, s=100, zorder=2, label="FF1 MD")
    ax.plot(dense_temperature, dense_cell, color="black", linewidth=1, zorder=1)
    ax.scatter(0, SERIAL_CG_BOX_RELAX_A, marker="s", color="red",
               edgecolor="black", linewidth=1.5, s=90, zorder=2,
               clip_on=False, label="Serial CG w/box relax")
    ax.scatter(0, ALTERNATING_SD_CG_BOX_RELAX_A, marker="s", color="orange",
               edgecolor="black", linewidth=1.5, s=100, zorder=2,
               clip_on=False, label="Alternating SD & CG w/box relax")
    ax.scatter(0, EIGENMODE_FOLLOWING_A, marker="o", color="blue",
               edgecolor="black", linewidth=1.5, s=100, zorder=2,
               clip_on=False, label="Eigenmode-following")
    ax.scatter(zhou_temperature, zhou_cell, marker="^", color="white",
               edgecolor="black", linewidth=1.5, s=100, zorder=2,
               clip_on=False, label="Zhou et al.")
    ax.scatter(PARK_TEMPERATURE_K, PARK_CELL_A, marker="p", color="white",
               edgecolor="black", linewidth=1.5, s=100, zorder=2,
               clip_on=False, label="Park et al.")
    ax.legend(facecolor="white", fontsize=10, framealpha=1)
    return fig


def render(output_dir: Path = OUTPUTS, directory: Path = DATA) -> tuple[Path, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig = create_figure(directory)
    png = output_dir / "figure2_temperature_stability.png"
    pdf = output_dir / "figure2_temperature_stability.pdf"
    fig.savefig(png, bbox_inches="tight", dpi=400)
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return png, pdf


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUTS)
    args = parser.parse_args()
    png, pdf = render(args.output_dir)
    t, cell = load_simulation()
    l0 = linear_interpolate_extrapolate(t, cell, np.array([0.0]))[0]
    print(f"Saved Figure 2: {png} and {pdf}")
    print(f"Linear extrapolation to 0 K: {l0:.6f} Å")
    print(f"Eigenmode-following 0 K: {EIGENMODE_FOLLOWING_A:.6f} Å")


if __name__ == "__main__":
    main()
