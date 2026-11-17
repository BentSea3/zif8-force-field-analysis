"""Checks of the Figure 2 reconstruction from archived analysis tables."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import plot_figure2 as figure2


class TestFigure2(unittest.TestCase):
    def test_zif8_simulation_data(self):
        temperature, cell = figure2.load_simulation()
        self.assertEqual(len(temperature), 8)
        self.assertAlmostEqual(temperature[0], 100.0)
        self.assertAlmostEqual(temperature[-1], 800.0)
        self.assertTrue(np.all(np.diff(cell) > 0))

    def test_supercell_volume_conversion(self):
        temperature, cell = figure2.load_simulation()
        self.assertAlmostEqual(cell[0], 0.5 * np.cbrt(37539.8), places=10)

    def test_zero_temperature_linear_extrapolation(self):
        temperature, cell = figure2.load_simulation()
        zero_k = figure2.linear_interpolate_extrapolate(
            temperature, cell, np.array([0.0]))[0]
        self.assertAlmostEqual(zero_k, 16.7162418875, places=8)
        self.assertAlmostEqual(figure2.EIGENMODE_FOLLOWING_A, 16.7109528809, places=8)

    def test_experimental_data(self):
        temperature, cell = figure2.load_zhou()
        self.assertEqual(len(temperature), 5)
        self.assertAlmostEqual(temperature[0], 3.5)
        self.assertAlmostEqual(cell[-1], 17.0117, places=4)
        self.assertAlmostEqual(figure2.PARK_TEMPERATURE_K, 258.0)

    def test_figure_contains_expected_series(self):
        fig = figure2.create_figure()
        try:
            ax = fig.axes[0]
            self.assertEqual(len(ax.collections), 6)
            self.assertEqual(len(ax.lines), 1)
            self.assertEqual(ax.get_xlim(), (0.0, 850.0))
            self.assertTrue(np.allclose(ax.get_ylim(), (16.7, 17.05)))
            self.assertEqual(len(ax.get_legend().get_texts()), 6)
        finally:
            import matplotlib.pyplot as plt
            plt.close(fig)

    def test_generate_png_and_pdf(self):
        with tempfile.TemporaryDirectory() as folder:
            png, pdf = figure2.render(Path(folder))
            self.assertTrue(png.is_file() and png.stat().st_size > 5000)
            self.assertTrue(pdf.is_file() and pdf.stat().st_size > 5000)


if __name__ == "__main__":
    unittest.main()
