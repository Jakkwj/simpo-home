#!/usr/bin/env python3
"""Compatibility entrypoint: export the internal build from private SimpoSkills.

Skill sources moved to SimpoSkills. This script never reconstructs Web Skills
from the public CLI package. --skill is retained for old maintenance commands;
the full internal package is exported together to keep its catalog consistent.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT.parent / "SimpoSkills")
    parser.add_argument("--backend-root", type=Path, default=ROOT.parent / "SimpoBackend/backend/litestar")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--skill", choices=["all", "simpo-create-biomodel", "simpo-create-dataset", "simpo-create-project"], default="all")
    args = parser.parse_args()
    exporter = args.source_root / "tools/export.py"
    if not exporter.is_file():
        parser.error("The private SimpoSkills checkout is required for Web Skill maintenance; pass --source-root.")
    if args.skill != "all":
        print("Exporting the complete web-internal package, including the selected Skill.")
    command = [sys.executable, str(exporter), "--target", "web-internal", "--backend-root", str(args.backend_root)]
    if args.check:
        command.append("--check")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
