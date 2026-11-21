"""Tests for the Figure 3 simulation provenance checker."""

import importlib.util
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "check_provenance.py"

spec = importlib.util.spec_from_file_location(
    "check_provenance", SCRIPT
)
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)


class TestProvenance(unittest.TestCase):

    def test_pressure_directory_names(self):
        """Different decimal formats should identify the same pressure."""
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)

            for name in (
                "P_0.0GPa",
                "P_0.500GPa",
                "P_0.57GPa",
            ):
                (base / name).mkdir()

            cases = {
                "0": "P_0.0GPa",
                "5000": "P_0.500GPa",
                "5700": "P_0.57GPa",
            }

            for pressure, expected in cases.items():
                with self.subTest(pressure=pressure):
                    directory = provenance.find_pressure_directory(
                        base, Decimal(pressure)
                    )
                    self.assertEqual(directory.name, expected)

    def test_ambiguous_pressure_directories(self):
        """Two labels representing the same pressure are ambiguous."""
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)

            (base / "P_0.5GPa").mkdir()
            (base / "P_0.500GPa").mkdir()

            with self.assertRaises(ValueError):
                provenance.find_pressure_directory(
                    base, Decimal("5000")
                )

    def test_production_averages(self):
        """Averages must use the correct historical data columns."""
        data = """\
0 300 900 40000 0 0 0 0 0 34 35 36 90 90 90
1000 302 1100 42000 0 0 0 0 0 36 37 38 90 90 90
"""

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "production.dat"
            path.write_text(data)

            averages, temperature, count = (
                provenance.read_production_averages(path)
            )

        self.assertEqual(count, 2)
        self.assertEqual(temperature, 301)
        self.assertEqual(
            averages,
            [35, 36, 37, 41000],
        )

    def test_rounding_tolerances(self):
        """Small rounding differences should not count as mismatches."""
        reference = [34.0, 35.0, 36.0, 40000.0]

        calculated = [
            34.00004,
            34.99997,
            36.00003,
            40000.04,
        ]

        matches, _, _ = provenance.compare_point(
            reference, calculated
        )
        self.assertTrue(matches)

        # A larger lattice-length difference should fail.
        calculated[0] = 34.001

        matches, _, _ = provenance.compare_point(
            reference, calculated
        )
        self.assertFalse(matches)

        # A larger volume difference should also fail.
        calculated[0] = 34.0
        calculated[3] = 40000.2

        matches, _, _ = provenance.compare_point(
            reference, calculated
        )
        self.assertFalse(matches)

    def test_duplicate_figure_pressures(self):
        """Duplicate pressures should be rejected."""
        data = """\
1000 34 35 36 40000
1000.0 34 35 36 40000
"""

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "figure.dat"
            path.write_text(data)

            with self.assertRaises(ValueError):
                provenance.read_figure_table(path)

    def test_invalid_production_data(self):
        """Incomplete or non-finite production records should fail."""
        invalid_cases = (
            "0 300 1000\n",
            "0 300 1000 nan 0 0 0 0 0 34 35 36\n",
            "",
        )

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "production.dat"

            for data in invalid_cases:
                with self.subTest(data=data):
                    path.write_text(data)

                    with self.assertRaises(ValueError):
                        provenance.read_production_averages(path)


if __name__ == "__main__":
    unittest.main()
