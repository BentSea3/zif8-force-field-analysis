"""Calculate average cell properties from a LAMMPS log file."""

import sys
from pathlib import Path
from statistics import mean


def read_last_thermo_block(path):
    columns = None
    rows = []
    last_block = None

    for line in path.read_text().splitlines():
        fields = line.split()

        if fields[:2] == ["Step", "Temp"]:
            columns = fields
            rows = []

        elif columns and fields[:2] == ["Loop", "time"]:
            if rows:
                last_block = (columns, rows)
            columns = None
            rows = []

        elif columns and len(fields) == len(columns):
            try:
                rows.append([float(value) for value in fields])
            except ValueError:
                continue

    if columns and rows:
        last_block = (columns, rows)

    if last_block is None:
        raise ValueError("No thermodynamic data found")

    return last_block


def main(path):
    columns, rows = read_last_thermo_block(path)

    print(f"File: {path}")
    print(f"Measurements: {len(rows)}")

    for column in ("Press", "Cella", "Cellb", "Cellc", "Volume"):
        index = columns.index(column)
        average = mean(row[index] for row in rows)
        print(f"{column}: {average:.4f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 average_lammps_cell.py log.lammps")

    main(Path(sys.argv[1]))
