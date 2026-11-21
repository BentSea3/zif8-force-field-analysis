"""Check Figure 3 plotting data against archived LAMMPS production data."""

import argparse
import math
import re
from decimal import Decimal
from pathlib import Path
from statistics import mean


CASES = {
    "Zheng (2012)": (
        "zheng2",
        "1-Zheng2012/p_stability/anisotropic/300K",
        11,
    ),
    "Hu (2012)": (
        "hu2",
        "2-Hu2012/p_stability/anisotropic/1test",
        10,
    ),
    "Zhang (2013)": (
        "zhang2",
        "5-Zhang2013/p_stability/anisotropic/300K",
        9,
    ),
    "Wu (2014)": (
        "wu2",
        "3-Wu2014/p_stability/anisotropic/300K",
        10,
    ),
    "Weng-Schmidt (2019)": (
        "schmidt2",
        "6-Schmidt2019/p_stability/anisotropic/1runs",
        12,
    ),
}

PRESSURE_DIRECTORY = re.compile(r"P_(\d+(?:\.\d+)?)GPa")

FIGURE_DATA = (
    Path(__file__).resolve().parent / "data" / "sim"
)

LENGTH_TOLERANCE = 0.0000501
VOLUME_TOLERANCE = 0.0501


def read_figure_table(path):
    """Read pressure, supercell lengths, and volume from a plotting table."""
    rows = []
    pressures = set()

    for number, line in enumerate(path.read_text().splitlines(), 1):
        fields = line.split()

        if not fields or fields[0].startswith("#"):
            continue

        if len(fields) != 5:
            raise ValueError(f"{path}:{number}: expected five columns")

        pressure = Decimal(fields[0])
        values = [float(value) for value in fields[1:]]

        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"{path}:{number}: non-finite value")

        if pressure in pressures:
            raise ValueError(f"{path}:{number}: duplicate pressure")

        pressures.add(pressure)
        rows.append((pressure, values))

    return rows


def find_pressure_directory(base, pressure_atm):
    """Find a directory by numerical pressure, preserving label precision."""
    target_gpa = pressure_atm / Decimal("10000")
    matches = []

    for directory in base.iterdir():
        if not directory.is_dir():
            continue

        match = PRESSURE_DIRECTORY.fullmatch(directory.name)

        if match and Decimal(match.group(1)) == target_gpa:
            matches.append(directory)

    if len(matches) != 1:
        raise ValueError(
            f"{base}: pressure {pressure_atm} atm "
            f"has {len(matches)} matching directories"
        )

    return matches[0]


def read_production_averages(path):
    """Average the saved thermodynamic columns in a processed data file.

    Expected columns include:
    Step, Temp, Press, Volume, ..., Cella, Cellb, Cellc.
    """
    rows = []

    for number, line in enumerate(path.read_text().splitlines(), 1):
        fields = line.split()

        if not fields:
            continue

        if len(fields) < 12:
            raise ValueError(f"{path}:{number}: expected 12+ columns")

        values = [float(value) for value in fields[:12]]

        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"{path}:{number}: non-finite value")

        rows.append(values)

    if not rows:
        raise ValueError(f"{path}: no production measurements")

    averages = [
        mean(row[index] for row in rows)
        for index in (9, 10, 11, 3)
    ]

    temperature = mean(row[1] for row in rows)

    return averages, temperature, len(rows)


def compare_point(reference, calculated):
    """Compare averages using the plotting table's rounding precision."""
    length_difference = max(
        abs(a - b)
        for a, b in zip(reference[:3], calculated[:3])
    )

    volume_difference = reference[3] - calculated[3]

    matches = (
        length_difference <= LENGTH_TOLERANCE
        and abs(volume_difference) <= VOLUME_TOLERANCE
    )

    return matches, length_difference, volume_difference


def check_archive(archive, figure_data=FIGURE_DATA, details=False):
    """Check every Figure 3 point and return success or failure."""
    total_points = 0
    total_matches = 0
    problems = 0

    for name, (filename, relative_dir, expected_count) in CASES.items():
        figure_path = figure_data / filename
        base = archive / relative_dir

        figure_rows = read_figure_table(figure_path)

        if len(figure_rows) != expected_count:
            print(
                f"WARNING: {name} has {len(figure_rows)} points; "
                f"expected {expected_count}"
            )
            problems += 1

        matches = 0

        for pressure, reference in figure_rows:
            total_points += 1

            try:
                directory = find_pressure_directory(base, pressure)
                datafile = directory / f"{directory.name}.dat"

                averages, temperature, count = (
                    read_production_averages(datafile)
                )

                agrees, d_length, d_volume = compare_point(
                    reference, averages
                )

            except (OSError, ValueError) as error:
                print(f"  ERROR {name}, {pressure} atm: {error}")
                problems += 1
                continue

            if agrees:
                matches += 1
                total_matches += 1
            else:
                problems += 1
                print(
                    f"  DIFFERENT {name}, {pressure} atm: "
                    f"dL={d_length:.6f} Å, "
                    f"dV={d_volume:+.4f} Å³"
                )

            if details:
                status = "MATCH" if agrees else "DIFFERENT"

                print(
                    f"  {pressure:>7} atm "
                    f"{directory.name:<13} "
                    f"N={count:<5} "
                    f"T={temperature:.2f} K "
                    f"{status}"
                )

        print(f"{name:<22} {matches}/{len(figure_rows)} matches")

    print()
    print(f"Total: {total_matches}/{total_points} matching points")
    print(f"Problems: {problems}")

    return problems == 0 and total_matches == 52


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--archive",
        type=Path,
        required=True,
        help="Path to the historical ZIF-8-Definitive directory",
    )

    parser.add_argument(
        "--details",
        action="store_true",
        help="Print the result for every pressure point",
    )

    args = parser.parse_args()

    if not args.archive.is_dir():
        parser.error(f"Archive directory not found: {args.archive}")

    success = check_archive(args.archive, details=args.details)

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
