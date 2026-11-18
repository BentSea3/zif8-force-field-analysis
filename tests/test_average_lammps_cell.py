"""Tests for the LAMMPS cell analysis."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "studies/01-zif8-force-field-evaluation/analysis/average_lammps_cell.py"
)


class TestAverageLammpsCell(unittest.TestCase):

    def test_last_thermo_block(self):
        log_text = """Step Temp Press Volume Cella Cellb Cellc
0 300 0 40000 34 34 34
Loop time of 1.0 on 1 procs for 1000 steps

Step Temp Press Volume Cella Cellb Cellc
0 300 990 37400 33.4 33.6 33.5
1000 300 1010 37600 33.6 33.4 33.5
Loop time of 1.0 on 1 procs for 1000 steps
"""

        with tempfile.TemporaryDirectory() as folder:
            logfile = Path(folder) / "log.lammps"
            logfile.write_text(log_text)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(logfile)],
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertIn("Measurements: 2", result.stdout)
        self.assertIn("Press: 1000.0000", result.stdout)
        self.assertIn("Cella: 33.5000", result.stdout)
        self.assertIn("Cellb: 33.5000", result.stdout)
        self.assertIn("Volume: 37500.0000", result.stdout)

    def test_all_blocks_with_repeated_timesteps(self):
        log_text = """\
Step Temp Press Volume Cella Cellb Cellc
0 300 900 40000 34 34 34
1000 300 1100 39000 33 33 33
Loop time of 1.0 on 1 procs for 1000 steps

Step Temp Press Volume Cella Cellb Cellc
0 300 950 38000 33.5 33.5 33.5
1000 300 1050 37000 33.4 33.4 33.4
Loop time of 1.0 on 1 procs for 1000 steps
"""

        with tempfile.TemporaryDirectory() as folder:
            logfile = Path(folder) / "log.lammps"
            logfile.write_text(log_text)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(logfile),
                    "--all-blocks",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertIn("Completed MD blocks: 2", result.stdout)
        self.assertIn(
            "Block 1: 2 measurements, steps 0-1000",
            result.stdout,
        )
        self.assertIn(
            "Block 2: 2 measurements, steps 0-1000",
            result.stdout,
        )
        self.assertIn(
            "Volume: mean=37500.0000",
            result.stdout,
        )

    def test_incomplete_final_block_is_ignored(self):
        log_text = """\
Step Temp Press Volume Cella Cellb Cellc
0 300 1000 38000 33 33 33
Loop time of 1.0 on 1 procs for 1000 steps

Step Temp Press Volume Cella Cellb Cellc
0 300 2000 50000 40 40 40
"""

        with tempfile.TemporaryDirectory() as folder:
            logfile = Path(folder) / "log.lammps"
            logfile.write_text(log_text)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(logfile)],
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertIn("Measurements: 1", result.stdout)
        self.assertIn("Press: 1000.0000", result.stdout)
        self.assertIn("Volume: 38000.0000", result.stdout)

if __name__ == "__main__":
    unittest.main()
