"""Reconstruct five ZIF-8 pressure-dependent elastic-constant panels (Fig. 4).

Scientific data are from the archived `Repos/ecs/` plotting tables. Reference
points are transcribed from the unchanged `ecs_raspa.ipynb` notebook, cell 3.
This is a reconstruction, not recovered original plotting code.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Generate figures without a graphical session.
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

# The force-field numbering and panel order follow the submitted manuscript.
FORCE_FIELDS = (
    ("FF1", "zheng2012", "zheng.dat"),
    ("FF2", "hu2012", "hu.dat"),
    ("FF3", "zhang2013", "zhang.dat"),
    ("FF4", "wu2014", "wu.dat"),
    ("FF5", "schmidt2019", "schmidt.dat"),
)

# Archival notebook cell 3: [pressure (GPa), C11, C12, C44 (GPa)].
# According to the submitted manuscript, DFT-B3LYP and Brillouin
# values were taken from Tan et al. (2012), with Brillouin at 295 K.
B3LYP = np.array([0.0, 11.038, 8.325, 0.943], dtype=float)
BRILLOUIN = np.array([0.0, 9.52, 6.87, 0.97], dtype=float)

CONSTANTS = (
    (1, "C11", "black", "o"),
    (2, "C12", "red", "s"),
    (3, "C44", "blue", "^"),
)


def load_table(path: Path) -> np.ndarray:
    """Load pressure and C11/C12/C44 in GPa from an archived four-column file."""
    table = np.loadtxt(path, dtype=float, ndmin=2)
    if table.ndim != 2 or table.shape[1] != 4 or not len(table):
        raise ValueError(f"Expected four numerical columns in {path}")
    if not np.isfinite(table).all():
        raise ValueError(f"Non-finite values in {path}")
    if np.any(np.diff(table[:, 0]) <= 0):
        raise ValueError(f"Pressure values must increase in {path}")
    return table


def load_input_data() -> tuple[dict[str, np.ndarray], np.ndarray]:
    """Load five force-field tables and the M06-2X reference table."""
    force_fields = {
        name: load_table(DATA / "sim" / filename)
        for _ff_label, name, filename in FORCE_FIELDS
    }
    maul = load_table(DATA / "reference" / "maulDFT.dat")
    return force_fields, maul


def plot_panel(
    ff_label: str, values: np.ndarray, maul: np.ndarray
) -> tuple[plt.Figure, plt.Axes]:
    """Draw one of the five manuscript panels using the notebook's conventions."""
    fig, ax = plt.subplots(figsize=(7, 5))

    for column, constant_name, color, marker in CONSTANTS:
        # Force-field values: filled symbols, thin solid connecting line.
        ax.plot(
            values[:, 0], values[:, column],
            color="black", linewidth=1, zorder=1,
        )
        ax.scatter(
            values[:, 0], values[:, column],
            marker=marker, c=color, edgecolors="black",
            linewidths=1.5, s=120, zorder=3, clip_on=False,
            label=f"{constant_name} {ff_label}",
        )

        # Maul et al. M06-2X: open symbols and dashed connecting line.
        ax.plot(
            maul[:, 0], maul[:, column],
            color="black", linestyle="--", linewidth=1, zorder=1,
        )
        ax.scatter(
            maul[:, 0], maul[:, column],
            marker=marker, facecolors="none", edgecolors=color,
            linewidths=1.5, s=120, zorder=2, clip_on=False,
            label=f"{constant_name} M06-2X",
        )

        # B3LYP: crosses at 0 GPa.
        ax.scatter(
            [B3LYP[0]], [B3LYP[column]],
            marker="x", color=color, linewidths=2.5, s=120,
            zorder=5, clip_on=False, label=f"{constant_name} B3LYP",
        )
        # Brillouin: filled triangles with green outlines at 0 GPa.
        ax.scatter(
            [BRILLOUIN[0]], [BRILLOUIN[column]],
            marker="^", c=color, edgecolors="forestgreen",
            linewidths=2.5, s=120, zorder=4, clip_on=False,
            label=f"{constant_name} Brillouin",
        )

    # The FF5 panel in the submitted version starts at -0.2 GPa.
    left = -0.20 if ff_label == "FF5" else -0.40
    ax.set_xlim(left, 0.42)
    ax.set_ylim(0, 12.5)
    ax.set_xticks(np.arange(left, 0.41, 0.1))
    ax.set_yticks(np.arange(0, 13, 2))
    ax.tick_params(labelsize=14)
    ax.set_xlabel(r"Pressure, $P$ / $\mathrm{GPa}$", fontsize=18)
    ax.set_ylabel(r"Elastic constant / $\mathrm{GPa}$", fontsize=18)

    if ff_label == "FF1":
        ax.text(0.02, 0.03, ff_label, transform=ax.transAxes,
                fontsize=18, fontweight="bold")
    else:
        ax.text(0.90, 0.93, ff_label, transform=ax.transAxes,
                fontsize=18, fontweight="bold")
    return fig, ax


def generate_figures(output_dir: Path) -> list[Path]:
    """Write five PDF panels and five PNG panels, in FF1--FF5 order."""
    force_fields, maul = load_input_data()
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for ff_label, name, _filename in FORCE_FIELDS:
        fig, _ax = plot_panel(ff_label, force_fields[name], maul)
        stem = f"figure4_{ff_label.lower()}_{name}"
        for extension in ("pdf", "png"):
            path = output_dir / f"{stem}.{extension}"
            fig.savefig(path, bbox_inches="tight", dpi=200 if extension == "png" else None)
            generated.append(path)
        plt.close(fig)
    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=HERE / "outputs",
        help="Where to write PNG and PDF panels (default: outputs/ beside script)",
    )
    args = parser.parse_args()
    paths = generate_figures(args.output_dir)
    print(f"Saved {len(paths)} files ({len(FORCE_FIELDS)} PNG and PDF panels) to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
