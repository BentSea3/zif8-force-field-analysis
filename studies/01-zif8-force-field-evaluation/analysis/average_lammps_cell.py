"""Calculate cell properties from completed LAMMPS MD runs."""

import argparse
from pathlib import Path
from statistics import mean, stdev


REQUIRED_COLUMNS = {
    "Step", "Temp", "Press", "Volume",
    "Cella", "Cellb", "Cellc",
}


def read_thermo_blocks(path):
    """Return completed MD thermo blocks in their original order.

    Each block is a (columns, rows) tuple. Timestep numbers may
    restart between blocks, so blocks are identified by their
    headers and LAMMPS completion lines, not by step values.
    """
    blocks = []
    columns = None
    rows = []

    with path.open() as handle:
        for line in handle:
            fields = line.split()

            if fields and fields[0] == "Step":
                if REQUIRED_COLUMNS.issubset(fields):
                    columns = fields
                    rows = []
                else:
                    columns = None
                    rows = []
                continue

            if fields[:3] == ["Loop", "time", "of"]:
                if columns is not None and rows:
                    blocks.append((columns, rows))

                columns = None
                rows = []
                continue

            if columns is None or len(fields) != len(columns):
                continue

            try:
                values = [float(value) for value in fields]
            except ValueError:
                continue

            rows.append(values)

    return blocks


def read_last_thermo_block(path):
    """Return the last completed MD block (legacy interface)."""
    blocks = read_thermo_blocks(path)

    if not blocks:
        raise ValueError("No completed MD thermodynamic data found")

    return blocks[-1]


def print_averages(columns, rows):
    """Print mean cell properties using the historical CLI format."""
    for column in ("Press", "Cella", "Cellb", "Cellc", "Volume"):
        index = columns.index(column)
        average = mean(row[index] for row in rows)
        print(f"{column}: {average:.4f}")


def print_all_blocks(path):
    """Summarize each completed MD block separately."""
    blocks = read_thermo_blocks(path)

    if not blocks:
        raise ValueError("No completed MD thermodynamic data found")

    print(f"File: {path}")
    print(f"Completed MD blocks: {len(blocks)}")

    for number, (columns, rows) in enumerate(blocks, start=1):
        indices = {name: i for i, name in enumerate(columns)}

        first_step = rows[0][indices["Step"]]
        last_step = rows[-1][indices["Step"]]

        print()
        print(
            f"Block {number}: {len(rows)} measurements, "
            f"steps {first_step:g}-{last_step:g}"
        )

        for column in (
            "Temp", "Press", "Volume",
            "Cella", "Cellb", "Cellc",
        ):
            values = [row[indices[column]] for row in rows]
            average = mean(values)

            if len(values) > 1:
                spread = f"{stdev(values):.4f}"
            else:
                spread = "n/a"

            print(
                f"  {column}: mean={average:.4f}, "
                f"sample_SD={spread}"
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "logfile",
        type=Path,
        help="LAMMPS log file",
    )
    parser.add_argument(
        "--all-blocks",
        action="store_true",
        help="Report every completed MD block separately",
    )

    args = parser.parse_args()

    if args.all_blocks:
        print_all_blocks(args.logfile)
        return

    columns, rows = read_last_thermo_block(args.logfile)

    print(f"File: {args.logfile}")
    print(f"Measurements: {len(rows)}")
    print_averages(columns, rows)


if __name__ == "__main__":
    main()
