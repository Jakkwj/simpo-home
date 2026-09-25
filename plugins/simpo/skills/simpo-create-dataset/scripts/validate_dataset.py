#!/usr/bin/env python3
"""Validate AI-generated SIMPO DataSet JSON before CLI submission."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


REQUIRED_TABLES = (
    "Unit", "Target", "Tank", "Pump", "Measured", "Inflow", "Flow", "Connection"
)
RESERVED_NAMES = {"Tank", "Inflow", "Flow", "Target", "Pump", "Outflow", "Wasted"}
HEADERS = {
    "Unit": ["Time", "Volume", "Flow", "Area", "Height"],
    "Target": ["Symbol", "Unit", "Name", "Description", "Oxygen", "TSS"],
    "Tank": [
        "Name", "Type", "BioCalculated", "Volume", "ConstantVolume",
        "SettlingFactor", "DiffuserNumber", "DiffuserDepth", "AlphaFactor", "BetaFactor",
    ],
    "Pump": ["Name", "Type", "SOTEa", "SOTEb", "SOTEc"],
    "Connection": ["From", "Flow", "Into"],
}
IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class Validator:
    def __init__(self, document: Any) -> None:
        self.document = document
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @staticmethod
    def _is_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    def _check_row_keys(self, table: str, row: Any, row_number: int, width: int | None = None) -> bool:
        if not isinstance(row, dict):
            self.error(f"{table} row {row_number} must be a JSON object.")
            return False
        expected = [str(index) for index in range(len(row))]
        actual = list(row.keys())
        if actual != expected:
            self.error(
                f"{table} row {row_number} keys must be consecutive and naturally ordered: "
                f"expected {expected}, got {actual}."
            )
        if width is not None and len(row) != width:
            self.error(f"{table} row {row_number} must contain {width} columns, got {len(row)}.")
        return True

    def _table(self, name: str, *, allow_empty: bool = False) -> list[dict[str, Any]]:
        value = self.document.get(name) if isinstance(self.document, dict) else None
        if not isinstance(value, list):
            self.error(f"{name} must be an array of row objects.")
            return []
        if not allow_empty and not value:
            self.error(f"{name} must not be empty.")
        for index, row in enumerate(value, 1):
            self._check_row_keys(name, row, index)
        return value

    def _fixed_table(self, name: str, *, allow_empty: bool = False) -> list[dict[str, Any]]:
        rows = self._table(name, allow_empty=allow_empty)
        if not rows:
            return rows
        header = HEADERS[name]
        for index, row in enumerate(rows, 1):
            self._check_row_keys(name, row, index, len(header))
        actual = [rows[0].get(str(index)) for index in range(len(header))]
        if actual != header:
            self.error(f"{name} header must be {header}, got {actual}.")
        return rows

    def validate(self) -> None:
        if not isinstance(self.document, dict):
            self.error("The JSON root must be an object.")
            return
        allowed = set(REQUIRED_TABLES) | {"jointGraphJson"}
        missing = [name for name in REQUIRED_TABLES if name not in self.document]
        if missing:
            self.error(f"Missing required top-level tables: {', '.join(missing)}.")
        extras = sorted(set(self.document) - allowed)
        if extras:
            self.error(f"Unsupported top-level fields: {', '.join(extras)}.")
        graph = self.document.get("jointGraphJson")
        if graph is not None and not isinstance(graph, dict):
            self.error("jointGraphJson must be an object or null.")

        unit = self._fixed_table("Unit")
        target = self._fixed_table("Target")
        tank = self._fixed_table("Tank")
        pump = self._fixed_table("Pump", allow_empty=True)
        measured = self._table("Measured", allow_empty=True)
        inflow = self._table("Inflow", allow_empty=True)
        flow = self._table("Flow", allow_empty=True)
        connection = self._fixed_table("Connection")

        self._validate_unit(unit)
        target_names = self._validate_target(target)
        tanks, tank_types, constant_tanks = self._validate_tank(tank)
        pumps = self._validate_pump(pump)
        measured_points = set(tanks)
        for name, kind in tank_types.items():
            if kind == "Point Settling":
                measured_points.discard(name)
                measured_points.update({f"{name}_Outlet", f"{name}_Blanket"})
        if measured:
            self._validate_blocks(
                "Measured", measured, "Tank", target_names, measured_points,
                require_complete_targets=True,
            )
        inflows = (
            self._validate_blocks(
                "Inflow", inflow, "Inflow", target_names, None,
                require_complete_targets=True,
            )
            if inflow else set()
        )
        flow_names, initial_flows = self._validate_flow(flow) if flow else (set(), {})
        self._validate_connections(
            connection, tanks, tank_types, constant_tanks, pumps, inflows,
            flow_names, initial_flows,
        )

    def _validate_unit(self, rows: list[dict[str, Any]]) -> None:
        if len(rows) != 2:
            self.error(f"Unit must contain exactly the header and value rows, got {len(rows)} rows.")
            return
        expected = ["day", "m3", "m3/d", "m2", "m"]
        actual = [rows[1].get(str(index)) for index in range(5)]
        if actual != expected:
            self.error(f"Unit values must be {expected}, got {actual}.")

    def _validate_target(self, rows: list[dict[str, Any]]) -> set[str]:
        names: set[str] = set()
        oxygen: list[str] = []
        tss: list[str] = []
        if len(rows) < 2:
            self.error("Target must contain at least one data row.")
            return names
        for index, row in enumerate(rows[1:], 2):
            symbol = row.get("0")
            unit = row.get("1")
            if not isinstance(symbol, str) or not IDENTIFIER.fullmatch(symbol):
                self.error(f"Target row {index} Symbol must be an ASCII identifier.")
                continue
            if symbol in RESERVED_NAMES:
                self.error(f"Target row {index} uses reserved Symbol {symbol!r}.")
            if symbol in names:
                self.error(f"Duplicate Target Symbol {symbol!r}.")
            names.add(symbol)
            if not isinstance(unit, str) or not unit.strip():
                self.error(f"Target {symbol!r} must have a nonempty Unit.")
            for key, label, collection in (("4", "Oxygen", oxygen), ("5", "TSS", tss)):
                marker = row.get(key)
                if not isinstance(marker, bool):
                    self.error(f"Target {symbol!r} {label} must be a JSON boolean.")
                elif marker:
                    collection.append(symbol)
        if len(oxygen) != 1:
            self.error(f"Exactly one Target must have Oxygen=true, got {oxygen}.")
        if len(tss) != 1:
            self.error(f"Exactly one Target must have TSS=true, got {tss}.")
        return names

    def _validate_tank(
        self, rows: list[dict[str, Any]]
    ) -> tuple[set[str], dict[str, str], set[str]]:
        names: set[str] = set()
        types: dict[str, str] = {}
        constant: set[str] = set()
        if len(rows) < 2:
            self.error("Tank must contain at least one data row.")
            return names, types, constant
        for index, row in enumerate(rows[1:], 2):
            name, kind = row.get("0"), row.get("1")
            if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
                self.error(f"Tank row {index} Name must be an ASCII identifier.")
                continue
            if name in RESERVED_NAMES or name in names:
                self.error(f"Tank row {index} has reserved or duplicate Name {name!r}.")
            names.add(name)
            types[name] = str(kind)
            bio, const = row.get("2"), row.get("4")
            if not isinstance(bio, bool) or not isinstance(const, bool):
                self.error(f"Tank {name!r} BioCalculated and ConstantVolume must be booleans.")
            if const is True:
                constant.add(name)
            if kind == "CSTR":
                if bio is not True:
                    self.error(f"CSTR {name!r} must have BioCalculated=true.")
                if not self._is_number(row.get("3")) or row["3"] < 0:
                    self.error(f"CSTR {name!r} Volume must be a nonnegative number.")
                if row.get("5") is not None:
                    self.error(f"CSTR {name!r} SettlingFactor must be null.")
                for key, label in (("6", "DiffuserNumber"), ("7", "DiffuserDepth")):
                    if not self._is_number(row.get(key)) or row[key] < 0:
                        self.error(f"CSTR {name!r} {label} must be nonnegative.")
                if self._is_number(row.get("6")) and int(row["6"]) != row["6"]:
                    self.error(f"CSTR {name!r} DiffuserNumber must be an integer.")
                for key, label in (("8", "AlphaFactor"), ("9", "BetaFactor")):
                    if not self._is_number(row.get(key)) or not 0 <= row[key] <= 1:
                        self.error(f"CSTR {name!r} {label} must be between 0 and 1.")
            elif kind == "Point Settling":
                if bio is not False:
                    self.error(f"Point Settling tank {name!r} must have BioCalculated=false.")
                volume = row.get("3")
                if not (
                    isinstance(volume, list) and len(volume) == 2
                    and all(self._is_number(item) and item >= 0 for item in volume)
                ):
                    self.error(f"Point Settling tank {name!r} Volume must be two nonnegative numbers.")
                factor = row.get("5")
                if not self._is_number(factor) or not 0 <= factor <= 1:
                    self.error(f"Point Settling tank {name!r} SettlingFactor must be between 0 and 1.")
                if any(row.get(key) is not None for key in ("6", "7", "8", "9")):
                    self.error(f"Point Settling tank {name!r} diffuser and alpha/beta fields must be null.")
            else:
                self.error(f"Tank {name!r} Type must be 'CSTR' or 'Point Settling'.")
        return names, types, constant

    def _validate_pump(self, rows: list[dict[str, Any]]) -> set[str]:
        names: set[str] = set()
        if not rows:
            return names
        for index, row in enumerate(rows[1:], 2):
            name = row.get("0")
            if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
                self.error(f"Pump row {index} Name must be an ASCII identifier.")
                continue
            if name in RESERVED_NAMES or name in names:
                self.error(f"Pump row {index} has reserved or duplicate Name {name!r}.")
            names.add(name)
            if row.get("1") != "Air":
                self.error(f"Pump {name!r} Type must be 'Air' in this workflow.")
            for key, label in (("2", "SOTEa"), ("3", "SOTEb"), ("4", "SOTEc")):
                if not self._is_number(row.get(key)):
                    self.error(f"Pump {name!r} {label} must be numeric.")
        return names

    def _validate_blocks(
        self,
        table: str,
        rows: list[dict[str, Any]],
        separator: str,
        target_names: set[str],
        allowed_names: set[str] | None,
        require_complete_targets: bool = False,
    ) -> set[str]:
        names: set[str] = set()
        if len(rows) < 3:
            self.error(f"{table} must contain two header rows and at least one data row.")
            return names
        width = len(rows[0])
        for index, row in enumerate(rows, 1):
            self._check_row_keys(table, row, index, width)
        first, second = rows[0], rows[1]
        starts = [index for index in range(width) if first.get(str(index)) == separator]
        if not starts or starts[0] != 0:
            self.error(f"{table} first row must start with {separator!r}.")
            return names
        starts.append(width)
        for block_index in range(len(starts) - 1):
            start, end = starts[block_index], starts[block_index + 1]
            if end - start < 2:
                self.error(f"{table} block at column {start} has no target columns.")
                continue
            if second.get(str(start)) != "Target":
                self.error(f"{table} column {start} second-row separator must be 'Target'.")
            block_names = {first.get(str(column)) for column in range(start + 1, end)}
            if len(block_names) != 1 or not isinstance(next(iter(block_names)), str):
                self.error(f"{table} block at column {start} must repeat one point name.")
                continue
            name = next(iter(block_names))
            if not IDENTIFIER.fullmatch(name) or name in RESERVED_NAMES:
                self.error(f"{table} block uses invalid or reserved name {name!r}.")
            if allowed_names is not None and name not in allowed_names:
                self.error(f"{table} references unknown monitoring point {name!r}.")
            if name in names:
                self.error(f"{table} repeats block name {name!r}.")
            names.add(name)
            block_targets = [second.get(str(column)) for column in range(start + 1, end)]
            if len(block_targets) != len(set(block_targets)):
                self.error(f"{table} block {name!r} repeats a Target.")
            for target in block_targets:
                if target not in target_names:
                    self.error(f"{table} block {name!r} references unknown Target {target!r}.")
            if require_complete_targets and set(block_targets) != target_names:
                missing = sorted(target_names - set(block_targets))
                extra = sorted(set(block_targets) - target_names)
                self.error(
                    f"{table} block {name!r} must contain every Target exactly once; "
                    f"missing={missing}, extra={extra}."
                )
            for row_number, row in enumerate(rows[2:], 3):
                time_value = row.get(str(start))
                if not self._is_number(time_value) or time_value < 0:
                    self.error(f"{table} row {row_number} block {name!r} time must be nonnegative.")
                for column in range(start + 1, end):
                    value = row.get(str(column))
                    if value is not None and not self._is_number(value):
                        self.error(f"{table} row {row_number} column {column} must be numeric or null.")
        return names

    def _validate_flow(self, rows: list[dict[str, Any]]) -> tuple[set[str], dict[str, float]]:
        names: set[str] = set()
        initial: dict[str, float] = {}
        if len(rows) < 2:
            self.error("Flow must contain a header row and at least one data row.")
            return names, initial
        width = len(rows[0])
        if width % 2:
            self.error("Flow must contain complete time/value column pairs.")
        for index, row in enumerate(rows, 1):
            self._check_row_keys("Flow", row, index, width)
        for column in range(0, width, 2):
            if rows[0].get(str(column)) != "Flow":
                self.error(f"Flow header column {column} must be 'Flow'.")
            name = rows[0].get(str(column + 1))
            if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
                self.error(f"Flow name at column {column + 1} must be an ASCII identifier.")
                continue
            if name in RESERVED_NAMES or name in names:
                self.error(f"Flow has reserved or duplicate name {name!r}.")
            names.add(name)
            found_initial = False
            for row_number, row in enumerate(rows[1:], 2):
                time_value, value = row.get(str(column)), row.get(str(column + 1))
                if not self._is_number(time_value) or time_value < 0:
                    self.error(f"Flow row {row_number} for {name!r} has invalid time.")
                if value is not None and not self._is_number(value):
                    self.error(f"Flow row {row_number} for {name!r} must be numeric or null.")
                if time_value == 0 and self._is_number(value):
                    initial[name] = float(value)
                    found_initial = True
            if not found_initial:
                self.error(f"Flow {name!r} must have a numeric value at time 0.")
        return names, initial

    def _parse_expression(self, expression: Any, row_number: int) -> dict[str, int]:
        if not isinstance(expression, str):
            self.error(f"Connection row {row_number} Flow must be a string expression.")
            return {}
        compact = expression.replace(" ", "")
        if not compact or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*(?:[+-][A-Za-z][A-Za-z0-9_]*)*", compact):
            self.error(
                f"Connection row {row_number} has unsupported Flow expression {expression!r}; "
                "use defined names with + and - only."
            )
            return {}
        result: dict[str, int] = defaultdict(int)
        sign = 1
        for token in re.split(r"([+-])", compact):
            if token == "+":
                sign = 1
            elif token == "-":
                sign = -1
            elif token:
                result[token] += sign
        return {name: coefficient for name, coefficient in result.items() if coefficient}

    def _validate_connections(
        self,
        rows: list[dict[str, Any]],
        tanks: set[str],
        tank_types: dict[str, str],
        constant_tanks: set[str],
        pumps: set[str],
        inflows: set[str],
        flow_names: set[str],
        initial_flows: dict[str, float],
    ) -> None:
        if len(rows) < 2:
            self.error("Connection must contain at least one data row.")
            return
        balances: dict[str, dict[str, int]] = {name: defaultdict(int) for name in tanks}
        used_flows: set[str] = set()
        used_inflows: set[str] = set()
        used_pumps: set[str] = set()

        def source_tank(node: str) -> str | None:
            if node in tanks:
                return node
            for tank, kind in tank_types.items():
                if kind == "Point Settling" and node in {f"{tank}_Outlet", f"{tank}_Blanket"}:
                    return tank
            return None

        valid_sources = set(tanks) | pumps | inflows
        for tank, kind in tank_types.items():
            if kind == "Point Settling":
                valid_sources.update({f"{tank}_Outlet", f"{tank}_Blanket"})
        valid_destinations = set(tanks) | {"Outflow", "Wasted"}

        for row_number, row in enumerate(rows[1:], 2):
            from_node, expression, into_node = row.get("0"), row.get("1"), row.get("2")
            if from_node not in valid_sources:
                self.error(f"Connection row {row_number} has unknown From node {from_node!r}.")
            if into_node not in valid_destinations:
                self.error(f"Connection row {row_number} has unknown Into node {into_node!r}.")
            coefficients = self._parse_expression(expression, row_number)
            unknown = set(coefficients) - flow_names
            if unknown:
                self.error(f"Connection row {row_number} uses undefined Flows: {sorted(unknown)}.")
            used_flows.update(coefficients)
            if from_node in inflows:
                used_inflows.add(from_node)
            if from_node in pumps:
                used_pumps.add(from_node)
                if into_node not in tanks:
                    self.error(f"Pump connection row {row_number} must lead to a Tank.")
                continue
            origin = source_tank(str(from_node))
            destination = str(into_node) if into_node in tanks else None
            for name, coefficient in coefficients.items():
                if origin:
                    balances[origin][name] -= coefficient
                if destination:
                    balances[destination][name] += coefficient

        for tank in sorted(constant_tanks):
            residual = {name: value for name, value in balances[tank].items() if value}
            if residual:
                rendered = " + ".join(f"{value:+d}*{name}" for name, value in sorted(residual.items()))
                self.error(f"Constant-volume Tank {tank!r} is not symbolically balanced: {rendered}.")
            if all(name in initial_flows for name in balances[tank]):
                numeric = sum(coefficient * initial_flows[name] for name, coefficient in balances[tank].items())
                scale = max(1.0, sum(abs(coefficient * initial_flows[name]) for name, coefficient in balances[tank].items()))
                if abs(numeric) > 1e-8 * scale:
                    self.error(f"Constant-volume Tank {tank!r} initial flow residual is {numeric:g} m3/d.")

        for name in sorted(inflows - used_inflows):
            self.warn(f"Inflow {name!r} is not used by Connection.")
        for name in sorted(pumps - used_pumps):
            self.warn(f"Pump {name!r} is not used by Connection.")
        for name in sorted(flow_names - used_flows):
            self.warn(f"Flow {name!r} is not used by Connection.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path, help="Path to the DataSet detail JSON")
    args = parser.parse_args()
    try:
        document = json.loads(args.json_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"ERROR: cannot read valid UTF-8 JSON: {error}", file=sys.stderr)
        return 2

    validator = Validator(document)
    validator.validate()
    for warning in validator.warnings:
        print(f"WARNING: {warning}")
    for error in validator.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if validator.errors:
        print(f"FAILED: {len(validator.errors)} error(s), {len(validator.warnings)} warning(s).", file=sys.stderr)
        return 1
    print(f"OK: DataSet JSON passed local checks with {len(validator.warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
