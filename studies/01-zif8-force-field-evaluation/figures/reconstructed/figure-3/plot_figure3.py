"""Reconstruct Figure 3 (ZIF-8 lattice parameter versus pressure).

Based on the archived plotting notebook `pstability/Pstab_definitive.ipynb`,
plotting cell 7. Original archived numerical tables are kept byte-for-byte.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Run without a display / in CI.
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
ATM_PER_GPA = 9869.23266716  # Atmospheric pressures in 1 GPa, notebook convention.
SIM_SERIES = (
    ("zheng2", "FF1", "red"),
    ("hu2", "FF2", "blue"),
    ("zhang2", "FF3", "forestgreen"),
    ("wu2", "FF4", "orange"),
    ("schmidt2", "FF5", "purple"),
)
EXPERIMENT_SERIES = (
    ("chapman", "Chapman et al.", "+", "tan"),
    ("vervoorts", "Vervoorts et al.", "x", "teal"),
)


def load_simulation(name: str, root: Path = DATA_DIR) -> tuple[np.ndarray, np.ndarray]:
    """Return pressure in GPa and ZIF-8 unit-cell length in Å.

    Archived columns: pressure (atm), three supercell lengths (Å),
    supercell volume (Å³). The historical notebook converts the
    volume to unit-cell length using 0.5 * volume ** (1/3).
    """
    data = np.loadtxt(root / "sim" / name, ndmin=2)
    if data.ndim != 2 or data.shape[1] != 5 or not np.all(np.isfinite(data)):
        raise ValueError(f"Unexpected simulation data in {name}: expected 5 finite columns")
    if np.any(data[:, 4] <= 0):
        raise ValueError(f"Nonpositive volume in {name}")
    pressure = data[:, 0] / ATM_PER_GPA
    unit_cell_size = 0.5 * np.cbrt(data[:, 4])
    return pressure, unit_cell_size


def load_experiment(name: str, root: Path = DATA_DIR) -> tuple[np.ndarray, np.ndarray]:
    """Return pressure (GPa) and unit-cell size (Å) from a digitized table."""
    data = np.loadtxt(root / "exp" / name, ndmin=2)
    if data.ndim != 2 or data.shape[1] != 2 or not np.all(np.isfinite(data)):
        raise ValueError(f"Unexpected experimental data in {name}: expected 2 finite columns")
    return data[:, 0], data[:, 1]


def create_figure(root: Path = DATA_DIR) -> plt.Figure:
    """Reproduce archived notebook plotting choices for manuscript Figure 3."""
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    ax.set_xlabel(r"Pressure, $P$ / $\mathrm{GPa}$", fontsize=18)
    ax.set_ylabel(r"Unit cell size, $L_{p}$ / $\mathrm{\AA}$", fontsize=18)
    ax.set_xlim(0.0, 1.10)
    ax.set_ylim(14.0, 17.3)
    ax.set_xticks(np.arange(0.0, 1.10, 0.15))
    ax.set_yticks(np.arange(14.0, 17.3, 1.0))
    ax.tick_params(labelsize=14)

    for name, label, color in SIM_SERIES:
        pressure, cell_size = load_simulation(name, root)
        ax.scatter(
            pressure, cell_size, marker="o", color=color,
            edgecolor="black", linewidth=1.0, s=90,
            zorder=2, label=label, clip_on=False,
        )
        ax.plot(
            pressure, cell_size, linestyle="--", color="black",
            linewidth=0.7, zorder=1,
            label="Guide" if name == "zheng2" else None,
        )

    # As in the submitted figure, Im et al. data in the original notebook
    # are commented out; only Chapman and Vervoorts are plotted.
    for name, label, marker, color in EXPERIMENT_SERIES:
        pressure, cell_size = load_experiment(name, root)
        ax.scatter(
            pressure, cell_size, marker=marker, color=color,
            linewidth=2.5, s=100, label=label,
            zorder=1, clip_on=False,
        )

    # Notebook legend has "Guide" first because its plotting call was
    # attached to the first plotted series; reorder for exact legend order.
    handles, labels = ax.get_legend_handles_labels()
    guide = labels.index("Guide")
    order = [guide] + [i for i in range(len(labels)) if i != guide]
    ax.legend(
        [handles[i] for i in order], [labels[i] for i in order],
        facecolor="white", fontsize=13, framealpha=0.8,
    )
    return fig


def render(output_dir: Path = DEFAULT_OUTPUT_DIR, root: Path = DATA_DIR) -> tuple[Path, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure = create_figure(root)
    png_path = output_dir / "figure3_pressure_stability.png"
    pdf_path = output_dir / "figure3_pressure_stability.pdf"
    figure.savefig(png_path, bbox_inches="tight", dpi=500)
    figure.savefig(pdf_path, bbox_inches="tight")
    plt.close(figure)
    return png_path, pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    png, pdf = render(args.output_dir)
    print(f"Saved Figure 3: {png} and {pdf}")


if __name__ == "__main__":
    main()
