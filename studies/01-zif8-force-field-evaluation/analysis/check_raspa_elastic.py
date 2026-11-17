"""Check elastic properties reported in a RASPA output file."""

import sys
from pathlib import Path


def read_stiffness_matrix(lines):
    header = "Elastic constant (Voigt notation) [GPa]"
    start = next(
        i for i, line in enumerate(lines)
        if line.strip() == header
    )

    matrix = []
    for line in lines[start + 1:]:
        fields = line.split()

        if len(fields) == 6:
            try:
                matrix.append([float(x) for x in fields])
            except ValueError:
                continue

        if len(matrix) == 6:
            break

    if len(matrix) != 6:
        raise ValueError("Could not read the stiffness matrix")

    return matrix


def read_born_eigenvalues(lines):
    start = next(
        i for i, line in enumerate(lines)
        if line.strip() == "Born stability criteria [GPa]"
    )

    values = []
    for line in lines[start + 1:]:
        if line.strip().startswith("Eigenvalue:"):
            values.append(float(line.split(":")[1]))
        elif values:
            break

    if len(values) != 6:
        raise ValueError("Expected six stability eigenvalues")

    return values


def main(path):
    lines = path.read_text().splitlines()
    c = read_stiffness_matrix(lines)

    diagonal = c[0][0] + c[1][1] + c[2][2]
    off_diagonal = c[0][1] + c[0][2] + c[1][2]
    shear = c[3][3] + c[4][4] + c[5][5]

    bulk_voigt = (diagonal + 2 * off_diagonal) / 9
    shear_voigt = (diagonal - off_diagonal + 3 * shear) / 15

    eigenvalues = read_born_eigenvalues(lines)

    print(f"Bulk modulus (Voigt): {bulk_voigt:.6f} GPa")
    print(f"Shear modulus (Voigt): {shear_voigt:.6f} GPa")
    print(f"Smallest Born eigenvalue: {min(eigenvalues):.6f} GPa")
    print(f"All eigenvalues positive: {all(x > 0 for x in eigenvalues)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 check_raspa_elastic.py output.data")

    main(Path(sys.argv[1]))
