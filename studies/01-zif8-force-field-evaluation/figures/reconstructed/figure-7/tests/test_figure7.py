"""Numerical and plot-level checks for the Figure 7 reconstruction."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("plot_figure7", ROOT / "plot_figure7.py")
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class TestFigure7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cg = module.load_cg_data()
        cls.reference = module.load_eigenmode_reference()

    def test_cg_shape_and_finite_values(self):
        self.assertEqual(self.cg.shape, (8, 14))
        self.assertTrue(np.isfinite(self.cg).all())

    def test_original_deformation_parameter_order(self):
        np.testing.assert_allclose(self.cg[:, 0], module.DEFORMATION_VALUES, rtol=1e-12)
        self.assertGreater(self.cg[1, 0], self.cg[2, 0])  # original order, NOT sorted
        self.assertGreater(self.cg[3, 0], self.cg[4, 0])
        self.assertGreater(self.cg[5, 0], self.cg[6, 0])

    def test_cg_numeric_checkpoints(self):
        self.assertAlmostEqual(self.cg[0, 1], 12.8092851686841, places=11)
        self.assertAlmostEqual(self.cg[2, 1], 9.97382366928521, places=11)
        self.assertAlmostEqual(self.cg[-1, 1], 13.1960132461115, places=11)
        self.assertAlmostEqual(self.cg[2, 2], 15.0276856926388, places=11)

    def test_zero_pressure_raspa_benchmark(self):
        self.assertAlmostEqual(self.reference, 11.86036, places=5)
        values = np.loadtxt(module.DATA / "raspa" / "data_EC_zheng.dat")
        self.assertEqual(np.sum(values[:, 0] == 0), 1)
        np.testing.assert_allclose(values[values[:, 0] == 0, 1], [self.reference])

    def test_boxplot_contains_eight_points_per_constant_and_three_crosses(self):
        fig, ax = module.plot_boxplot(self.cg, self.reference)
        self.assertEqual([label.get_text() for label in ax.get_xticklabels()],
                         ["C11", "C22", "C33"])
        self.assertEqual(len(ax.collections), 4)  # 3 CG scatter collections + red reference
        for index in range(3):
            points = ax.collections[index].get_offsets()
            self.assertEqual(points.shape, (8, 2))
            np.testing.assert_allclose(points[:, 1], self.cg[:, index + 1])
        ref_points = ax.collections[3].get_offsets()
        np.testing.assert_allclose(ref_points[:, 1], np.repeat(self.reference, 3))
        plt.close(fig)

    def test_barplot_preserves_row_order_and_reference_line(self):
        fig, ax = module.plot_bars(self.cg, self.reference)
        self.assertEqual([tick.get_text() for tick in ax.get_xticklabels()],
                         list(module.DEFORMATION_LABELS))
        self.assertEqual(len(ax.patches), 8)
        np.testing.assert_allclose([patch.get_height() for patch in ax.patches], self.cg[:, 1])
        self.assertEqual(len(ax.lines), 1)
        np.testing.assert_allclose(ax.lines[0].get_ydata(),
                                   [self.reference, self.reference])
        plt.close(fig)

    def test_rejects_invalid_cg_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong.dat"
            np.savetxt(path, self.cg[:, :4])
            with self.assertRaises(ValueError):
                module.load_cg_data(path)
            bad = self.cg.copy()
            bad[1, 0] = 7e-4
            np.savetxt(path, bad)
            with self.assertRaises(ValueError):
                module.load_cg_data(path)

    def test_four_outputs_are_generated(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs = module.generate_figures(Path(directory))
            self.assertEqual(len(outputs), 4)
            for p in outputs:
                self.assertTrue(p.exists())
                self.assertGreater(p.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
