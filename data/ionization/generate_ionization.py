#!/usr/bin/env python3
"""Generate docs and portable Skill parameter tables from the adjacent ionization.json.

Run from any directory. --check detects drift without writing. A sibling
SimpoSkills checkout receives the shared reference; build/export its targets
after changing data. Legacy checkouts without generated packages retain the old
backend/installed-copy flags. Only marked parameter blocks are replaced.
"""

import argparse
import hashlib
import json
import math
import re
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path("data/ionization/ionization.json")
CLI_REFERENCE = Path(
    "plugins/simpo/skills/simpo-create-biomodel/references/ionization-derivation.md"
)
AI_REFERENCE = Path(
    "app/services/ai/skills/simpo-create-biomodel/references/ionization-derivation.md"
)
DOCS = {
    "en": Path("src/docs/Tutorials/BioModel/Edit.mdx"),
    "zh": Path(
        "src/i18n/zh/docusaurus-plugin-content-docs/current/Tutorials/BioModel/Edit.mdx"
    ),
}


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate(data):
    if type(data.get("version")) is not int or data["version"] < 1:
        raise ValueError("version must be a positive integer")
    if not isinstance(data.get("source_url"), str) or not data["source_url"].startswith(
        "https://"
    ):
        raise ValueError("source_url must be an HTTPS URL")
    if not number(data.get("pKw")):
        raise ValueError("pKw must be a finite number")
    if not isinstance(data.get("ions"), list) or not data["ions"]:
        raise ValueError("ions must be a nonempty list")
    seen = set()
    for row in data["ions"]:
        key = row.get("id", "")
        if (
            not isinstance(key, str)
            or not re.fullmatch(r"[a-z][a-z0-9_]*", key)
            or key in seen
        ):
            raise ValueError(f"invalid or duplicate ion id: {key}")
        seen.add(key)
        for locale in DOCS:
            label = row.get("name", {}).get(locale)
            if (
                not isinstance(label, str)
                or not label.strip()
                or any(c in label for c in "|\n\r<>{}")
            ):
                raise ValueError(f"invalid {locale} name: {key}")
        if row.get("compound") not in (
            "Strong Acid",
            "Weak Acid",
            "Strong Base",
            "Weak Base",
        ):
            raise ValueError(f"invalid Compound: {key}")
        if row.get("step") not in ("Mono", "Di", "Tri"):
            raise ValueError(f"invalid Step: {key}")
        strong = row["compound"].startswith("Strong")
        mode = (
            "Complete"
            if strong
            else "One Step"
            if row["step"] == "Mono"
            else "Stepwise"
        )
        count = 0 if strong else {"Mono": 1, "Di": 2, "Tri": 3}[row["step"]]
        constants = row.get("pK")
        if (
            row.get("ionization") != mode
            or not isinstance(constants, list)
            or len(constants) != 3
        ):
            raise ValueError(f"invalid Ionization or pK shape: {key}")
        if not all(number(v) for v in constants[:count]) or any(
            v is not None for v in constants[count:]
        ):
            raise ValueError(f"invalid required/unused pK values: {key}")
        if (
            type(row.get("factor_denominator")) is not int
            or row["factor_denominator"] <= 0
        ):
            raise ValueError(f"invalid Factor denominator: {key}")


def scalar(value):
    return "" if value is None else str(value)


def table(data, locale=None):
    factor_label = "Factor（mol/mg）" if locale == "zh" else "Factor (mol/mg)"
    columns = [
        "Species" if locale is None else "Symbol",
        "Compound",
        "Step",
        "Ionization",
        factor_label,
        "pK1",
        "pK2",
        "pK3",
    ]
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * 8) + " |"]
    for row in data["ions"]:
        label = row["name"]["en"]
        if locale == "zh":
            label = f"{row['name']['zh']}（{label}）"
        elif locale is None:
            label += " / " + row["name"]["zh"]
        denominator = row["factor_denominator"]
        factor = f"1/{denominator}"
        if locale:
            mass = (
                format(Decimal(denominator) / 1000, "f").rstrip("0").rstrip(".")
                if denominator % 1000
                else str(denominator // 1000)
            )
            factor = f"1/({mass}*1000)"
        lines.append(
            "| "
            + " | ".join(
                [
                    label,
                    row["compound"],
                    row["step"],
                    row["ionization"],
                    factor,
                    *map(scalar, row["pK"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def generated_content(data, locale=None):
    raw = json.dumps(
        data, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    digest = hashlib.sha256(raw).hexdigest()
    note = f"Generated from SimpoHome/{SOURCE.as_posix()}; version {data['version']}; sha256 {digest}. Do not edit this block."
    if locale:
        return "{/* " + note + " */}\n\n" + table(data, locale)
    return (
        "<!-- " + note + " -->\n\n"
        f"SIMPO built-in parameter set v{data['version']}. "
        f"[Documentation]({data['source_url']}). Default pKw: **{scalar(data['pKw'])}**.\n\n"
        "These are approved SIMPO reference defaults for derivation, not dummy examples. "
        "The primary values outside parentheses in the source table are selected; "
        "do not average or substitute the parenthetical alternatives. "
        "Use these local values without a live webpage lookup.\n\n" + table(data)
    )


def replace_block(original, content, *, mdx=False):
    begin = (
        "{/* BEGIN GENERATED IONIZATION */}"
        if mdx
        else "<!-- BEGIN GENERATED IONIZATION -->"
    )
    end = (
        "{/* END GENERATED IONIZATION */}"
        if mdx
        else "<!-- END GENERATED IONIZATION -->"
    )
    if original.count(begin) != 1 or original.count(end) != 1:
        raise ValueError("expected exactly one generated Ionization block")
    before, remainder = original.split(begin)
    _, after = remainder.split(end)
    return before + begin + "\n" + content + "\n" + end + after


def generate(root=ROOT, *, backend_root=None, skills_root=None, source_root=None, check=False):
    data = json.loads((root / SOURCE).read_text(encoding="utf-8"))
    validate(data)
    targets = [(root / path, locale) for locale, path in DOCS.items()]
    if source_root is None:
        sibling = root.parent / "SimpoSkills"
        if (sibling / "skills/simpo-create-biomodel/skill.json").is_file():
            source_root = sibling
    if source_root is not None:
        if backend_root is not None or skills_root is not None:
            raise ValueError("Update the SimpoSkills source, then build/export; direct edits to generated or installed copies are disabled.")
        targets.append((source_root / "skills/simpo-create-biomodel/references/ionization-derivation.md", None))
    else:
        if (root / "plugins/simpo/generated.json").is_file():
            raise ValueError("Generated Skills require the private SimpoSkills checkout; pass --source-root.")
        targets.append((root / CLI_REFERENCE, None))
        if backend_root is None:
            sibling = root.parent / "SimpoBackend/backend/litestar"
            if sibling.is_dir():
                backend_root = sibling
        if backend_root is not None:
            targets.append((backend_root / AI_REFERENCE, None))
    if skills_root is not None:
        targets.append(
            (
                skills_root
                / "simpo-create-biomodel/references/ionization-derivation.md",
                None,
            )
        )
    # Validate every target before writing any, including explicitly selected copies.
    changes = []
    for path, locale in targets:
        original = path.read_text(encoding="utf-8")
        rendered = replace_block(
            original, generated_content(data, locale), mdx=locale is not None
        )
        if locale:
            rendered, count = re.subn(
                r"\{/\* SIMPO_PKW \*/\}.*?\{/\* /SIMPO_PKW \*/\}",
                "{/* SIMPO_PKW */}" + scalar(data["pKw"]) + "{/* /SIMPO_PKW */}",
                rendered,
            )
            if count != 1:
                raise ValueError(f"expected exactly one pKw value marker: {path}")
        if original != rendered:
            changes.append((path, rendered))
    for path, rendered in changes:
        if not check:
            path.write_text(rendered, encoding="utf-8")
        print(("Out of date: " if check else "Updated: ") + str(path))
    if not changes:
        print(
            f"Ionization references are current ({len(targets)} files, {len(data['ions'])} species)."
        )
    return bool(changes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--source-root", type=Path, help="Private SimpoSkills checkout; updates source instead of generated copies")
    parser.add_argument(
        "--backend-root", type=Path, help="SimpoBackend/backend/litestar directory"
    )
    parser.add_argument(
        "--skills-root", type=Path, help="Installed skills directory (explicit opt-in)"
    )
    args = parser.parse_args()
    try:
        changed = generate(
            backend_root=args.backend_root,
            skills_root=args.skills_root,
            source_root=args.source_root,
            check=args.check,
        )
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Ionization generation failed: {exc}\n")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
