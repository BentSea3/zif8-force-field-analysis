"""Tests of ZIF-8 Paper 1 Figure 3 reconstruction."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np

SCRIPT = Path(__file__).resolve().parents[1] / "plot_figure3.py"
SPEC = importlib.util.spec_from_file_location("plot_figure3", SCRIPT)
FIG3 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIG3)


class TestFigure3(unittest.TestCase):
    def test_all_five_force_fields_load(self):
        for name, _, _ in FIG3.SIM_SERIES:
            with self.subTest(name=name):
                pressure, size = FIG3.load_simulation(name)
                self.assertGreaterEqual(len(pressure), 9)
                self.assertEqual(pressure.shape, size.shape)
                self.assertTrue(np.all(np.diff(pressure) >= 0))
                self.assertTrue(np.all((size > 14) & (size < 18)))

    def test_pressure_and_volume_unit_conversions(self):
        pressure, size = FIG3.load_simulation("zheng2")
        self.assertAlmostEqual(pressure[1], 1000.0 / FIG3.ATM_PER_GPA, places=10)
        self.assertAlmostEqual(size[0], 0.5 * 37829.2 ** (1/3), places=10)

    def test_hu_pressure_induced_cell_collapse(self):
        pressure, size = FIG3.load_simulation("hu2")
        self.assertAlmostEqual(pressure[-1], 7000.0 / FIG3.ATM_PER_GPA, places=10)
        self.assertGreater(size[-2] - size[-1], 0.4)
        self.assertGreater(size[-3] - size[-2], 0.8)

    def test_two_experimental_datasets(self):
        for name, _, _, _ in FIG3.EXPERIMENT_SERIES:
            p, l = FIG3.load_experiment(name)
            self.assertGreaterEqual(len(p), 4)
            self.assertTrue(np.all(p < 0.5))
            self.assertTrue(np.all((l > 16) & (l < 18)))

    def test_plot_contains_expected_series_and_limits(self):
        figure = FIG3.create_figure()
        try:
            ax = figure.axes[0]
            self.assertEqual(len(ax.collections), 7)  # five force fields and two experimental series
            self.assertEqual(tuple(ax.get_xlim()), (0.0, 1.1))
            self.assertEqual(tuple(ax.get_ylim()), (14.0, 17.3))
            self.assertEqual(
                [item.get_text() for item in ax.get_legend().get_texts()],
                ["Guide", "FF1", "FF2", "FF3", "FF4", "FF5", "Chapman et al.", "Vervoorts et al."],
            )
        finally:
            FIG3.plt.close(figure)

    def test_generate_png_and_pdf(self):
        with tempfile.TemporaryDirectory() as folder:
            png, pdf = FIG3.render(Path(folder))
            self.assertGreater(png.stat().st_size, 10000)
            self.assertGreater(pdf.stat().st_size, 5000)


if __name__ == "__main__":
    unittest.main()
