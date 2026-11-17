"""Reconstruct the two 0 K elastic-constant panels of ZIF-8 Paper 1 Fig. 7.

Archived LAMMPS CG data and RASPA eigenmode-following reference are loaded
from the included original numerical files. This is reconstructed plotting
code, NOT the unmodified historical notebook.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

# Keep the original eight rows in exactly the order plotted in the notebook.
DEFORMATION_VALUES = np.array(
    [5e-5, 5e-4, 1e-4, 5e-3, 1e-3, 5e-2, 1e-2, 1e-1], dtype=float
)
DEFORMATION_LABELS = (
    "5e-5", "5e-4", "1e-4", "5e-3", "1e-3", "5e-2", "1e-2", "1e-1"
)
C_DIAGONAL = ((1, "C11"), (2, "C22"), (3, "C33"))


def load_cg_data(path: Path = DATA / "lammps" / "plottable_lammps") -> np.ndarray:
    """Read archived deformation parameter and thirteen LAMMPS output columns."""
    table = np.loadtxt(path, dtype=float, ndmin=2)
    if table.shape != (8, 14):
        raise ValueError(f"Expected 8 x 14 numerical CG table in {path}")
    if not np.isfinite(table).all():
        raise ValueError(f"Non-finite values in {path}")
    if not np.allclose(table[:, 0], DEFORMATION_VALUES, rtol=1e-12, atol=0):
        raise ValueError("Unexpected deformation parameters or archived row order")
    return table


def load_eigenmode_reference(
    path: Path = DATA / "raspa" / "data_EC_zheng.dat",
) -> float:
    """Return 0 GPa RASPA C11 (GPa): the cubic diagonal benchmark."""
    table = np.loadtxt(path, dtype=float, ndmin=2)
    if table.ndim != 2 or table.shape[1] != 4 or not np.isfinite(table).all():
        raise ValueError(f"Expected finite P/C11/C12/C44 RASPA table in {path}")
    idx = np.flatnonzero(np.isclose(table[:, 0], 0.0, rtol=0, atol=1e-12))
    if len(idx) != 1:
        raise ValueError("Expected exactly one RASPA row at zero pressure")
    return float(table[idx[0], 1])


def plot_boxplot(cg: np.ndarray, eigenmode_c11: float):
    """Panel 7a: CG elastic constants at eight deformation magnitudes."""
    fig, ax = plt.subplots(figsize=(6, 5))
    diag = [cg[:, column] for column, _ in C_DIAGONAL]
    bp = ax.boxplot(
        diag, whis=2.5, widths=0.30, patch_artist=False,
        boxprops={"color": "tab:blue", "linewidth": 1.15},
        whiskerprops={"color": "tab:blue", "linewidth": 1.15},
        capprops={"color": "black", "linewidth": 1.15},
        medianprops={"color": "green", "linewidth": 1.15},
        flierprops={"marker": "", "markersize": 0},
    )
    del bp  # The eight CG measurements are shown explicitly below.

    for x, vals in enumerate(diag, start=1):
        ax.scatter(
            np.full(len(vals), x), vals, marker="o", color="blue",
            s=53, zorder=3, label="CG routine" if x == 1 else None,
        )
    # The reference RASPA file reports cubic C11 at zero pressure. The
    # diagonal elastic constants C11, C22, C33 are equal by cubic symmetry.
    ax.scatter(
        [1, 2, 3], [eigenmode_c11] * 3, marker="x", color="red",
        s=180, linewidths=3, zorder=4, label="Eigenmode-following",
    )
    ax.set_xticks((1, 2, 3), ("C11", "C22", "C33"))
    ax.set_ylim(9.65, 15.35)
    ax.set_yticks(np.arange(10, 16, 1))
    ax.set_xlabel("Elastic constant", fontsize=19)
    ax.set_ylabel("Value / GPa", fontsize=19)
    ax.tick_params(labelsize=16)
    ax.grid(False)
    ax.legend(fontsize=13, loc="upper right")
    return fig, ax


def plot_bars(cg: np.ndarray, eigenmode_c11: float):
    """Panel 7b: C11 for each unsorted historical deformation setting."""
    fig, ax = plt.subplots(figsize=(7, 5))
    x = np.arange(len(DEFORMATION_LABELS))
    ax.bar(x, cg[:, 1], color="#80afd0", label="CG routine")
    ax.axhline(eigenmode_c11, color="red", linewidth=2,
               label="C11 Eigenmode-following")
    ax.set_xticks(x, DEFORMATION_LABELS)
    ax.set_xlim(-0.5, len(x) - 0.5)
    ax.set_ylim(8.5, 13.4)
    ax.set_yticks(np.arange(9, 14, 1))
    ax.set_xlabel("Box deformation parameter / Å", fontsize=19)
    ax.set_ylabel("C11 value / GPa", fontsize=19)
    ax.tick_params(labelsize=15)
    ax.legend(fontsize=12, loc="upper center")
    return fig, ax


def generate_figures(output_dir: Path) -> list[Path]:
    """Write both paper panels as PNG and vector PDF."""
    cg = load_cg_data()
    ref = load_eigenmode_reference()
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for name, plot_function in (
        ("figure7a_elastic_constant_boxplot", plot_boxplot),
        ("figure7b_c11_deformation_bars", plot_bars),
    ):
        fig, _ax = plot_function(cg, ref)
        for extension in ("pdf", "png"):
            path = output_dir / f"{name}.{extension}"
            fig.savefig(path, bbox_inches="tight", dpi=200 if extension == "png" else None)
            results.append(path)
        plt.close(fig)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=HERE / "outputs")
    args = parser.parse_args()
    files = generate_figures(args.output_dir)
    print(f"Saved {len(files)} Figure 7 files to {args.output_dir.resolve()}")
    print(f"Zero-pressure RASPA eigenmode-following reference: {load_eigenmode_reference():.5f} GPa")


if __name__ == "__main__":
    main()
