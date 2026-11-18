"""Tests for the LAMMPS structure comparison script."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "compare_structures.py"


def write_structure(
    path, positions, origin=(0, 0, 0),
    lengths=(10, 10, 10), types=None, charges=None
):
    """Write a minimal orthogonal LAMMPS data file for testing."""

    types = types or [1] * len(positions)
    charges = charges or [-0.1] * len(positions)

    lines = [
        "LAMMPS data file for testing",
        "",
        f"{len(positions)} atoms",
        "2 atom types",
        "",
    ]

    for axis, lo, length in zip("xyz", origin, lengths):
        lines.append(f"{lo} {lo + length} {axis}lo {axis}hi")

    lines.extend(["", "Atoms # full", ""])

    for atom_id, (xyz, atom_type, charge) in enumerate(
        zip(positions, types, charges), start=1
    ):
        x, y, z = xyz
        lines.append(
            f"{atom_id} 1 {atom_type} {charge} {x} {y} {z}"
        )

    path.write_text("\n".join(lines) + "\n")


class TestStructureComparison(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)

        directory = Path(self.tempdir.name)
        self.reference = directory / "reference.data"
        self.comparison = directory / "comparison.data"

        self.positions = [
            (1.0, 2.0, 3.0),
            (9.0, 8.0, 7.0),
            (4.0, 5.0, 6.0),
        ]

    def compare(self):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(self.reference),
                str(self.comparison),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_identical_structures(self):
        write_structure(self.reference, self.positions)
        write_structure(self.comparison, self.positions)

        result = self.compare()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Number of matching atoms: 3", result.stdout)
        self.assertIn("RMS displacement: 0.000000 Å", result.stdout)

    def test_periodic_wrapping(self):
        write_structure(self.reference, self.positions)

        # Equivalent positions in neighboring periodic images.
        wrapped = [
            (11.0, 2.0, 3.0),
            (-1.0, 8.0, 7.0),
            (14.0, 5.0, 6.0),
        ]
        write_structure(self.comparison, wrapped)

        result = self.compare()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "Without translation alignment:\n"
            "  RMS displacement: 0.000000 Å",
            result.stdout,
        )

    def test_uniform_cell_rescaling(self):
        write_structure(self.reference, self.positions)

        # Same fractional coordinates in a larger, shifted box.
        origin = (1.0, -2.0, 3.0)
        scaled = [
            tuple(origin[i] + 2 * xyz[i] for i in range(3))
            for xyz in self.positions
        ]

        write_structure(
            self.comparison,
            scaled,
            origin=origin,
            lengths=(20, 20, 20),
        )

        result = self.compare()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Relative volume change: 700.0000%", result.stdout)
        self.assertIn("RMS displacement: 0.000000 Å", result.stdout)

    def test_global_translation_alignment(self):
        write_structure(self.reference, self.positions)

        # Translate all atoms by 2 Å in x, wrapping into the box.
        shifted = [
            ((xyz[0] + 2) % 10, xyz[1], xyz[2])
            for xyz in self.positions
        ]
        write_structure(self.comparison, shifted)

        result = self.compare()

        self.assertEqual(result.returncode, 0, result.stderr)

        self.assertIn(
            "Without translation alignment:\n"
            "  RMS displacement: 2.000000 Å",
            result.stdout,
        )
        self.assertIn(
            "After translation alignment:\n"
            "  RMS displacement: 0.000000 Å",
            result.stdout,
        )

    def test_rejects_mismatched_atom_types(self):
        write_structure(self.reference, self.positions)

        write_structure(
            self.comparison,
            self.positions,
            types=[1, 2, 1],
        )

        result = self.compare()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "Atom 2: molecule or type differs",
            result.stderr,
        )

    def test_rejects_mismatched_charges(self):
        write_structure(self.reference, self.positions)

        write_structure(
            self.comparison,
            self.positions,
            charges=[-0.1, -0.2, -0.1],
        )

        result = self.compare()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Atom 2: charge differs", result.stderr)


if __name__ == "__main__":
    unittest.main()
