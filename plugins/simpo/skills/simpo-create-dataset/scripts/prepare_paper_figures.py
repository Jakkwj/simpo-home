#!/usr/bin/env python3
"""Render PDF pages for reproducible paper figure digitization.

The script intentionally uses Poppler command-line tools instead of adding a
Python PDF dependency to the Skill. It writes a JSON manifest describing the
rendered pages and the commands used.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise RuntimeError(f"required command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"command failed with exit code {exc.returncode}: {' '.join(command)}") from exc


def page_count(pdf: Path) -> int | None:
    if shutil.which("pdfinfo") is None:
        return None
    result = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, capture_output=True)
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="source paper PDF")
    parser.add_argument("--output-dir", type=Path, required=True, help="directory for rendered pages")
    parser.add_argument("--dpi", type=int, default=300, help="render DPI (default: 300)")
    parser.add_argument("--first-page", type=int, default=1, help="first page to render, 1-based")
    parser.add_argument("--last-page", type=int, help="last page to render, inclusive")
    args = parser.parse_args()

    pdf = args.pdf.expanduser().resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        parser.error(f"PDF not found: {pdf}")
    if args.dpi < 72 or args.dpi > 1200:
        parser.error("--dpi must be between 72 and 1200")
    if args.first_page < 1:
        parser.error("--first-page must be at least 1")
    if args.last_page is not None and args.last_page < args.first_page:
        parser.error("--last-page must not be before --first-page")
    if shutil.which("pdftoppm") is None:
        parser.error("pdftoppm is required; install Poppler before rendering the paper")

    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    last_page = args.last_page or page_count(pdf)
    if last_page is not None and args.first_page > last_page:
        parser.error(f"first page {args.first_page} exceeds PDF page count {last_page}")

    prefix = output_dir / "page"
    command = [
        "pdftoppm",
        "-png",
        "-r",
        str(args.dpi),
        "-f",
        str(args.first_page),
    ]
    if last_page is not None:
        command.extend(["-l", str(last_page)])
    command.extend([str(pdf), str(prefix)])
    run(command)

    pages = sorted(str(path.relative_to(output_dir)) for path in output_dir.glob("page-*.png"))
    manifest = {
        "source_pdf": str(pdf),
        "dpi": args.dpi,
        "first_page": args.first_page,
        "last_page": last_page,
        "render_command": command,
        "pages": pages,
        "digitization_note": "Record figure/panel, axis calibration, series, units, and uncertainty for every imported series.",
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(output_dir), "manifest": str(manifest_path), "pages": pages}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
