#!/usr/bin/env python3
"""Normalize a digitizer CSV into an auditable point-series JSON file."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path


def numeric(value: str, row_number: int, column: str) -> float:
    try:
        result = float(value.strip())
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"row {row_number}: {column} is not numeric: {value!r}") from exc
    if not math.isfinite(result):
        raise ValueError(f"row {row_number}: {column} must be finite")
    return result


def choose_column(fieldnames: list[str], preferred: str, fallback_index: int) -> str:
    lowered = {name.strip().lower(): name for name in fieldnames}
    if preferred.lower() in lowered:
        return lowered[preferred.lower()]
    if fallback_index >= len(fieldnames):
        raise ValueError(f"CSV has no column for {preferred}")
    return fieldnames[fallback_index]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV exported by a digitizer")
    parser.add_argument("--output", type=Path, required=True, help="normalized JSON output")
    parser.add_argument("--figure", required=True, help="paper figure/panel, for example Fig. 4b")
    parser.add_argument("--series", required=True, help="legend or series label")
    parser.add_argument("--x-name", required=True, help="x-axis variable name")
    parser.add_argument("--y-name", required=True, help="y-axis variable name")
    parser.add_argument("--x-unit", default="", help="x-axis unit")
    parser.add_argument("--y-unit", default="", help="y-axis unit")
    parser.add_argument("--x-axis", choices=("linear", "log"), default="linear")
    parser.add_argument("--y-axis", choices=("linear", "log"), default="linear")
    parser.add_argument("--uncertainty", default="", help="estimated reading uncertainty")
    parser.add_argument("--x-column", default="X", help="CSV x column (default: X)")
    parser.add_argument("--y-column", default="Y", help="CSV y column (default: Y)")
    args = parser.parse_args()

    csv_file = args.csv_file.expanduser().resolve()
    if not csv_file.is_file():
        parser.error(f"CSV not found: {csv_file}")
    try:
        with csv_file.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
            if len(fieldnames) < 2:
                raise ValueError("CSV must contain at least two columns")
            x_column = choose_column(fieldnames, args.x_column, 0)
            y_column = choose_column(fieldnames, args.y_column, 1)
            points = []
            for row_number, row in enumerate(reader, start=2):
                if not any((value or "").strip() for value in row.values()):
                    continue
                points.append({
                    "x": numeric(row.get(x_column, ""), row_number, x_column),
                    "y": numeric(row.get(y_column, ""), row_number, y_column),
                })
    except (OSError, csv.Error, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not points:
        print("error: CSV contains no data points", file=sys.stderr)
        return 1

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "source_csv": str(csv_file),
        "figure": args.figure,
        "series": args.series,
        "x": {"name": args.x_name, "unit": args.x_unit, "axis": args.x_axis},
        "y": {"name": args.y_name, "unit": args.y_unit, "axis": args.y_axis},
        "uncertainty": args.uncertainty,
        "classification": "digitized",
        "point_count": len(points),
        "points": points,
        "review_required": True,
        "note": "Review the exported points against the rendered figure before mapping them to a DataSet table.",
    }
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "point_count": len(points)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
