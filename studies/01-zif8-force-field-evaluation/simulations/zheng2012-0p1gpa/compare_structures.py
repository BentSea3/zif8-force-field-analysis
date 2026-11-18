#!/usr/bin/env python3
"""Compare orthogonal LAMMPS atom_style full structures."""

from pathlib import Path
import sys

import numpy as np


def load_structure(filename):
    lines = Path(filename).read_text().splitlines()

    bounds = {}
    tilt = np.zeros(3)

    for line in lines:
        fields = line.split("#")[0].split()

        if len(fields) == 4 and fields[2] in ("xlo", "ylo", "zlo"):
            axis = fields[2][0]
            bounds[axis] = (float(fields[0]), float(fields[1]))

        if len(fields) == 6 and fields[3:] == ["xy", "xz", "yz"]:
            tilt = np.array([float(x) for x in fields[:3]])

    if len(bounds) != 3:
        raise ValueError(f"Missing box bounds in {filename}")

    if not np.allclose(tilt, 0, atol=1e-12):
        raise ValueError("This comparison supports orthogonal cells only")

    origin = np.array([bounds[a][0] for a in "xyz"])
    lengths = np.array([
        bounds[a][1] - bounds[a][0] for a in "xyz"
    ])

    section = next(
        i for i, line in enumerate(lines)
        if line.strip().startswith("Atoms # full")
    )

    atoms = {}

    for line in lines[section + 1:]:
        fields = line.split("#")[0].split()

        if not fields:
            continue

        if not fields[0].isdigit():
            break

        if len(fields) < 7:
            raise ValueError(f"Invalid atom record: {line}")

        atom_id = int(fields[0])

        if atom_id in atoms:
            raise ValueError(f"Duplicate atom ID: {atom_id}")

        molecule = int(fields[1])
        atom_type = int(fields[2])
        charge = float(fields[3])
        xyz = np.array([float(x) for x in fields[4:7]])

        atoms[atom_id] = (molecule, atom_type, charge, xyz)

    return origin, lengths, atoms


def minimum_image(displacement):
    return (displacement + 0.5) % 1.0 - 0.5


def print_statistics(label, distances):
    rms = np.sqrt(np.mean(distances**2))

    print(f"{label}:")
    print(f"  RMS displacement: {rms:.6f} Å")
    print(f"  Mean displacement: {np.mean(distances):.6f} Å")
    print(f"  95th percentile: {np.percentile(distances, 95):.6f} Å")
    print(f"  Maximum displacement: {np.max(distances):.6f} Å")


def main(reference_file, comparison_file):
    ref_origin, ref_box, ref_atoms = load_structure(reference_file)
    new_origin, new_box, new_atoms = load_structure(comparison_file)

    ids = sorted(ref_atoms)

    if set(ids) != set(new_atoms):
        raise ValueError("Atom IDs differ between structures")

    if not ids:
        raise ValueError("No atoms found")

    for atom_id in ids:
        old = ref_atoms[atom_id]
        new = new_atoms[atom_id]

        if old[:2] != new[:2]:
            raise ValueError(
                f"Atom {atom_id}: molecule or type differs"
            )

        if not np.isclose(old[2], new[2], rtol=0, atol=1e-8):
            raise ValueError(f"Atom {atom_id}: charge differs")

    ref_xyz = np.array([ref_atoms[i][3] for i in ids])
    new_xyz = np.array([new_atoms[i][3] for i in ids])

    ref_fractional = (ref_xyz - ref_origin) / ref_box
    new_fractional = (new_xyz - new_origin) / new_box

    delta = minimum_image(new_fractional - ref_fractional)

    # Compare after mapping both configurations into the
    # reference cell. This removes uniform cell deformation.
    raw_distances = np.linalg.norm(delta * ref_box, axis=1)

    # Estimate one global periodic translation in each direction.
    phase = np.mean(np.exp(2j * np.pi * delta), axis=0)
    translation = np.angle(phase) / (2 * np.pi)

    aligned_delta = minimum_image(delta - translation)
    aligned_distances = np.linalg.norm(
        aligned_delta * ref_box, axis=1
    )

    print(f"Number of matching atoms: {len(ids)}")
    print(f"Reference box (Å): {ref_box}")
    print(f"New box (Å):       {new_box}")
    print(f"Relative volume change: "
          f"{(np.prod(new_box) / np.prod(ref_box) - 1) * 100:.4f}%")
    print()

    print_statistics("Without translation alignment", raw_distances)
    print()
    print_statistics("After translation alignment", aligned_distances)

    print()
    print("Estimated fractional translation:", translation)
    print("Translation coherence:", np.abs(phase))

    if np.any(np.abs(phase) < 0.3):
        print("WARNING: Global translation estimate may be unreliable")

    print()
    print("Five largest aligned atomic displacements:")
    for index in np.argsort(aligned_distances)[-5:][::-1]:
        atom_id = ids[index]
        atom_type = ref_atoms[atom_id][1]
        print(
            f"  ID {atom_id:5d}  type {atom_type:2d}"
            f"  displacement {aligned_distances[index]:.6f} Å"
        )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: compare_structures.py reference.data new.data"
        )

    main(sys.argv[1], sys.argv[2])
