"""Reconstruct ZIF-8 paper 1 figures 5 and 6 from archived RASPA output.

This is a new reconstruction, NOT the original 2022 plotting script.

Example:
    python plot_figures.py
    python plot_figures.py --sd-cg-energy-kcal VALUE --cg-after-md-energy-kcal VALUE
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save figures without a GUI/display.
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FormatStrFormatter, NullFormatter

HERE = Path(__file__).resolve().parent
DEFAULT_DATA = HERE / "data" / "min_data_lammps_restart.txt"
DEFAULT_OUTPUT = HERE / "outputs"

# Kelvin-equivalent energies to kcal/mol: E(kcal/mol) = E(K) * R / 4184.
# R is in J mol^-1 K^-1; 4184 J = 1 thermochemical kcal.
R_J_PER_MOL_K = 8.31446261815324
KELVIN_PER_KCAL_MOL = 4184.0 / R_J_PER_MOL_K

# Final energy from the archived LAMMPS CG run after 0.5 K MD (units real).
# See README.md for the original log path and structural cross-check.
CG_AFTER_MD_ENERGY_KCAL = -8063.30080162371


@dataclass(frozen=True)
class MinimizationData:
    steps: np.ndarray
    energy_kcal_mol: np.ndarray
    negative_eigenvalues: np.ndarray

    @property
    def starting_cg_energy_kcal_mol(self) -> float:
        """Step-0 energy; use as a *provisional* CG reference only."""
        return float(self.energy_kcal_mol[0])


def load_minimization_data(path: Path = DEFAULT_DATA) -> MinimizationData:
    """Read archived 6-column table without modifying any values.

    Established from manuscript/data comparisons:
      col 0: minimization step (0 to 70)
      col 1: energy in kelvin-equivalent units
      col 3: negative Hessian eigenvalue count
      col 2: supercell volume (Angstrom cubed)
      col 4: RMS gradient (source units unverified)
      col 5: maximum gradient (source units unverified)
    """
    raw = np.loadtxt(path, ndmin=2)
    if raw.ndim != 2 or raw.shape[1] != 6:
        raise ValueError("Expected six whitespace-separated numerical columns")
    if not np.all(np.isfinite(raw)):
        raise ValueError("Input contains non-finite values")
    if np.any(np.diff(raw[:, 0]) <= 0):
        raise ValueError("Minimization steps must increase")
    if np.any(raw[:, 3] < 0) or not np.allclose(raw[:, 3], np.rint(raw[:, 3])):
        raise ValueError("Negative-eigenvalue counts must be nonnegative integers")
    return MinimizationData(
        steps=raw[:, 0],
        energy_kcal_mol=raw[:, 1] / KELVIN_PER_KCAL_MOL,
        negative_eigenvalues=raw[:, 3].astype(int),
    )


def style_axes(ax: plt.Axes) -> None:
    ax.tick_params(axis="both", which="major", labelsize=13, width=1.0)
    ax.tick_params(axis="both", which="minor", width=0.7)
    for spine in ax.spines.values():
        spine.set_linewidth(1)


def save_figure(fig: plt.Figure, output_dir: Path, name: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output_dir / f"{name}.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def figure_5(data: MinimizationData, output_dir: Path) -> None:
    # The archival PDF uses a logarithmic x-axis, so step 0 is intentionally omitted.
    valid = data.steps >= 1
    fig, ax = plt.subplots(figsize=(5.0, 4.9))
    ax.plot(data.steps[valid], data.negative_eigenvalues[valid], color="red",
            linewidth=2.8, label="Eigenmode-following")
    ax.set_xscale("log")
    ax.set_xlim(1, 70)
    ax.set_ylim(-2, 160)
    ax.xaxis.set_major_locator(FixedLocator([1, 10]))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_yticks([0, 40, 80, 120, 160])
    ax.set_xlabel("Minimization iteration", fontsize=17)
    ax.set_ylabel("Number of negative eigenvalues", fontsize=17)
    ax.legend(loc="upper right", frameon=True, fontsize=12)
    style_axes(ax)
    save_figure(fig, output_dir, "figure5_negative_eigenvalues")


def add_energy_references(
    ax: plt.Axes,
    data: MinimizationData,
    *,
    show_inferred_cg: bool,
    sd_cg_energy_kcal: float | None,
    cg_after_md_energy_kcal: float | None,
    include_cg: bool,
) -> None:
    if show_inferred_cg and include_cg:
        ax.axhline(data.starting_cg_energy_kcal_mol, color="teal", linestyle="--",
                   linewidth=1.5, label="CG initial energy (inferred)")
    if cg_after_md_energy_kcal is not None:
        ax.axhline(cg_after_md_energy_kcal, color="purple", linestyle="--",
                   linewidth=1.6, label="CG after MD (0.5 K)")
    if sd_cg_energy_kcal is not None:
        ax.axhline(sd_cg_energy_kcal, color="blue", linestyle="-",
                   linewidth=1.6, label="Alternating SD & CG")


def figure_6a(
    data: MinimizationData,
    output_dir: Path,
    *,
    show_inferred_cg: bool = True,
    sd_cg_energy_kcal: float | None = None,
    cg_after_md_energy_kcal: float | None = CG_AFTER_MD_ENERGY_KCAL,
) -> None:
    valid = data.steps >= 1
    fig, ax = plt.subplots(figsize=(5.9, 4.6))
    add_energy_references(ax, data, show_inferred_cg=show_inferred_cg,
                          sd_cg_energy_kcal=sd_cg_energy_kcal,
                          cg_after_md_energy_kcal=cg_after_md_energy_kcal,
                          include_cg=True)
    ax.plot(data.steps[valid], data.energy_kcal_mol[valid], color="red",
            linewidth=3, label="Eigenmode-following")
    ax.set_xscale("log")
    ax.set_xlim(1, 70)
    ax.set_ylim(-8070, -7950)
    ax.set_yticks([-8070, -8040, -8010, -7980, -7950])
    ax.xaxis.set_major_locator(FixedLocator([1, 10]))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Minimization step", fontsize=17)
    ax.set_ylabel(r"Energy, $E$ / kcal mol$^{-1}$", fontsize=17)
    ax.legend(loc="center right", frameon=True, fontsize=10)
    style_axes(ax)
    save_figure(fig, output_dir, "figure6a_energy_full")


def figure_6b(
    data: MinimizationData,
    output_dir: Path,
    *,
    sd_cg_energy_kcal: float | None = None,
    cg_after_md_energy_kcal: float | None = CG_AFTER_MD_ENERGY_KCAL,
) -> None:
    valid = (data.steps >= 30) & (data.steps <= 70)
    fig, ax = plt.subplots(figsize=(5.9, 4.6))
    # CG step-0 energy lies above this zoomed range and is deliberately omitted.
    add_energy_references(ax, data, show_inferred_cg=False,
                          sd_cg_energy_kcal=sd_cg_energy_kcal,
                          cg_after_md_energy_kcal=cg_after_md_energy_kcal,
                          include_cg=False)
    ax.plot(data.steps[valid], data.energy_kcal_mol[valid], color="red",
            linewidth=3, label="Eigenmode-following")
    ax.set_xlim(30, 70)
    ax.set_ylim(-8067, -8063)
    ax.set_xticks([30, 40, 50, 60, 70])
    ax.set_yticks([-8067, -8066, -8065, -8064, -8063])
    ax.set_xlabel("Minimization step", fontsize=17)
    ax.set_ylabel(r"Energy, $E$ / kcal mol$^{-1}$", fontsize=17)
    ax.legend(loc="lower left", frameon=True, fontsize=10)
    style_axes(ax)
    save_figure(fig, output_dir, "figure6b_energy_zoom")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Source 6-column table")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Figure destination")
    parser.add_argument("--no-inferred-cg", action="store_true",
                        help="Do not plot the provisional CG reference inferred from step 0")
    parser.add_argument("--sd-cg-energy-kcal", type=float, default=None,
                        help="Measured alternating steepest-descent/CG reference energy")
    parser.add_argument("--cg-after-md-energy-kcal", type=float, default=CG_AFTER_MD_ENERGY_KCAL,
                        help="Measured CG reference energy after 0.5 K MD")
    args = parser.parse_args()
    data = load_minimization_data(args.data)
    figure_5(data, args.output)
    figure_6a(data, args.output, show_inferred_cg=not args.no_inferred_cg,
              sd_cg_energy_kcal=args.sd_cg_energy_kcal,
              cg_after_md_energy_kcal=args.cg_after_md_energy_kcal)
    figure_6b(data, args.output, sd_cg_energy_kcal=args.sd_cg_energy_kcal,
              cg_after_md_energy_kcal=args.cg_after_md_energy_kcal)
    print(f"Saved three figures (PDF + PNG) to: {args.output.resolve()}")
    print(f"Initial energy (provisional CG reference): {data.starting_cg_energy_kcal_mol:.6f} kcal/mol")
    print(f"Final eigenmode-following energy: {data.energy_kcal_mol[-1]:.6f} kcal/mol")
    if args.sd_cg_energy_kcal is None:
        print("Warning: blue SD/CG reference remains unverified; see README.md")


if __name__ == "__main__":
    main()
