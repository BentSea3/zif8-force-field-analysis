"""Data and plotting regression checks for paper 1 minimization figures."""

from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_figures import (  # noqa: E402
    DEFAULT_DATA, KELVIN_PER_KCAL_MOL, load_minimization_data,
    figure_5, figure_6a, figure_6b,
)


class TestArchivedData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_minimization_data(DEFAULT_DATA)

    def test_archived_array_shape(self):
        self.assertEqual(self.data.steps.size, 71)
        np.testing.assert_array_equal(self.data.steps, np.arange(71))

    def test_figure5_negative_eigenvalue_behavior(self):
        count = self.data.negative_eigenvalues
        self.assertEqual(int(count[0]), 170)
        self.assertEqual(int(count[1]), 155)
        self.assertEqual(int(np.flatnonzero(count == 0)[0]), 15)
        self.assertTrue(np.any(count[38:52] > 0))
        self.assertEqual(int(count[52]), 0)

    def test_energy_conversion_and_convergence(self):
        self.assertAlmostEqual(KELVIN_PER_KCAL_MOL, 503.21953, places=4)
        self.assertAlmostEqual(self.data.starting_cg_energy_kcal_mol, -7957.9341, places=3)
        self.assertAlmostEqual(float(self.data.energy_kcal_mol[70]), -8066.1942, places=3)
        self.assertLess(self.data.energy_kcal_mol[70], self.data.energy_kcal_mol[1])

    def test_generate_six_files(self):
        with TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            figure_5(self.data, output_dir)
            figure_6a(self.data, output_dir)
            figure_6b(self.data, output_dir)
            for name in ("figure5_negative_eigenvalues", "figure6a_energy_full", "figure6b_energy_zoom"):
                for ext in ("pdf", "png"):
                    p = output_dir / f"{name}.{ext}"
                    self.assertTrue(p.exists())
                    self.assertGreater(p.stat().st_size, 4000)

    def test_optional_comparison_lines_can_be_supplied(self):
        # Numeric inputs below are test fixtures, NOT recovered scientific values.
        with TemporaryDirectory() as tmp:
            figure_6a(self.data, Path(tmp), sd_cg_energy_kcal=-8066.0,
                      cg_after_md_energy_kcal=-8063.3)
            figure_6b(self.data, Path(tmp), sd_cg_energy_kcal=-8066.0,
                      cg_after_md_energy_kcal=-8063.3)
            self.assertTrue((Path(tmp) / 'figure6b_energy_zoom.png').exists())


if __name__ == "__main__":
    unittest.main()
