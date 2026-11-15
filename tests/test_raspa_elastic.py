"""Tests for the RASPA elastic analysis."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "analysis/check_raspa_elastic.py"
)


class TestRaspaElastic(unittest.TestCase):

    def test_elastic_properties(self):
        output_text = """Elastic constant (Voigt notation) [GPa]
------------------------------
14 5 5 0 0 0
5 14 5 0 0 0
5 5 14 0 0 0
0 0 0 4 0 0
0 0 0 0 4 0
0 0 0 0 0 4

Born stability criteria [GPa]
-----------------------------
Eigenvalue: 9
Eigenvalue: 9
Eigenvalue: 24
Eigenvalue: 4
Eigenvalue: 4
Eigenvalue: 4
"""

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "output.data"
            output.write_text(output_text)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(output)],
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertIn("Bulk modulus (Voigt): 8.000000 GPa", result.stdout)
        self.assertIn("Shear modulus (Voigt): 4.200000 GPa", result.stdout)
        self.assertIn("Smallest Born eigenvalue: 4.000000 GPa", result.stdout)
        self.assertIn("All eigenvalues positive: True", result.stdout)


if __name__ == "__main__":
    unittest.main()
