"""Tests for the archived ZIF-8 Figure 4 elastic-constant reconstruction."""
import sys
import tempfile
import unittest
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_figure4 import (  # noqa: E402
    B3LYP, BRILLOUIN, CONSTANTS, FORCE_FIELDS,
    generate_figures, load_input_data, load_table, plot_panel,
)


class TestFigure4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.simulation, cls.maul = load_input_data()

    def test_five_force_field_panels_in_paper_order(self):
        self.assertEqual(
            [(label, name) for label, name, _ in FORCE_FIELDS],
            [("FF1", "zheng2012"), ("FF2", "hu2012"),
             ("FF3", "zhang2013"), ("FF4", "wu2014"),
             ("FF5", "schmidt2019")],
        )

    def test_five_tables_are_finite_and_have_four_columns(self):
        self.assertEqual(len(self.simulation), 5)
        for data in self.simulation.values():
            self.assertEqual(data.shape[1], 4)
            self.assertTrue(np.isfinite(data).all())
            self.assertTrue(np.all(np.diff(data[:, 0]) > 0))

    def test_zero_pressure_force_field_values(self):
        expected = {
            "zheng2012": (11.86036, 6.67962, 2.63927),
            "hu2012": (7.81435, 7.19910, 0.66948),
            "zhang2013": (9.75101, 7.70654, 0.67239),
            "wu2014": (9.89915, 7.73490, 0.69216),
            "schmidt2019": (6.56625, 4.57677, 0.91167),
        }
        for name, triplet in expected.items():
            zero = self.simulation[name][self.simulation[name][:, 0] == 0.0]
            self.assertEqual(len(zero), 1)
            np.testing.assert_allclose(zero[0, 1:], triplet, atol=1e-8)

    def test_reference_tables_and_labels(self):
        self.assertEqual(self.maul.shape, (8, 4))
        np.testing.assert_allclose(B3LYP, [0.0, 11.038, 8.325, 0.943])
        np.testing.assert_allclose(BRILLOUIN, [0.0, 9.52, 6.87, 0.97])
        self.assertEqual([constant for _, constant, _, _ in CONSTANTS],
                         ["C11", "C12", "C44"])

    def test_panel_has_three_constants_and_comparison_series(self):
        fig, ax = plot_panel("FF2", self.simulation["hu2012"], self.maul)
        try:
            self.assertEqual(len(ax.lines), 6)  # sim + M06-2X for each Cij
            self.assertEqual(len(ax.collections), 12)  # four marker sets per Cij
            self.assertAlmostEqual(ax.get_xlim()[0], -0.4)
            self.assertAlmostEqual(ax.get_ylim()[1], 12.5)
            self.assertEqual(ax.texts[0].get_text(), "FF2")
        finally:
            plt.close(fig)

    def test_ff5_pressure_range_follows_submitted_panel(self):
        fig, ax = plot_panel("FF5", self.simulation["schmidt2019"], self.maul)
        try:
            self.assertAlmostEqual(ax.get_xlim()[0], -0.2)
        finally:
            plt.close(fig)

    def test_reject_malformed_table(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong.dat"
            path.write_text("0 1 2\n1 2 3\n")
            with self.assertRaises(ValueError):
                load_table(path)

    def test_write_ten_figure_files(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = generate_figures(Path(directory))
            self.assertEqual(len(paths), 10)
            self.assertEqual(len(list(Path(directory).glob("*.pdf"))), 5)
            self.assertEqual(len(list(Path(directory).glob("*.png"))), 5)
            self.assertTrue(all(p.stat().st_size > 1000 for p in paths))


if __name__ == "__main__":
    unittest.main()
