"""Build immutable Skills bundles and the public CLI/Skills release catalog.

Run after uploading production CLI installers to the existing Gitee package release.
The catalog and Skills ZIPs themselves are committed to this GitHub repository.
Only explicitly selected CLI versions are announced; building a package alone never
announces it. No credentials or upload operations are performed by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins/simpo"
VERSION = re.compile(
    r"((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))-skills\.([1-9]\d*)"
)
CLI_VERSION = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
NAMES = (
    "simpo",
    "simpo-create-biomodel",
    "simpo-create-dataset",
    "simpo-create-project",
)
RAW_BASE = (
    "https://raw.githubusercontent.com/Jakkwj/simpo-home/master/plugins/simpo/releases/"
)
CLI_BASE = "https://gitee.com/Jakkwj/simpo-home/releases/download/package/"


def write_atomic(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".release-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(data)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()


def artifact(path: Path, base: str):
    checksum = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            checksum.update(chunk)
    if path.stat().st_size <= 0:
        raise ValueError(f"Empty artifact: {path}")
    return {
        "url": base + path.name,
        "size": path.stat().st_size,
        "sha256": checksum.hexdigest(),
    }


def build_bundle(destination: Path, source: Path):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in NAMES:
            if not (source / name / "SKILL.md").is_file():
                raise ValueError(f"Missing Skill: {name}")
            for path in sorted((source / name).rglob("*")):
                if path.is_symlink():
                    raise ValueError(f"Do not publish linked files: {path}")
                if (
                    not path.is_file()
                    or "__pycache__" in path.parts
                    or path.suffix in {".pyc", ".pyo"}
                    or path.name in {".DS_Store", ".simpo-skill.json"}
                ):
                    continue
                # Fixed timestamps/modes make repeated builds byte-identical.
                info = zipfile.ZipInfo(
                    path.relative_to(source).as_posix(), (2020, 1, 1, 0, 0, 0)
                )
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())


def publish(
    *,
    cli_versions=(),
    cli_directory: Path | None = None,
    plugin: Path = PLUGIN,
    root: Path = ROOT,
) -> dict:
    config = json.loads((plugin / "release.json").read_text(encoding="utf-8"))
    version, minimum = config["version"], config["cli_min_version"]
    if not VERSION.fullmatch(version) or not CLI_VERSION.fullmatch(minimum):
        raise ValueError("Expected X.Y.Z-skills.N and an X.Y.Z minimum CLI version.")
    output = plugin / "releases"
    output.mkdir(parents=True, exist_ok=True)
    index_path = output / "index.json"
    catalog = (
        json.loads(index_path.read_text(encoding="utf-8"))
        if index_path.exists()
        else {"schema_version": 1, "cli": [], "skills": []}
    )
    if catalog.get("schema_version") != 1:
        raise ValueError("Unsupported release catalog schema")
    filename = f"SIMPOSkills_{version}.zip"
    with tempfile.TemporaryDirectory(prefix=".bundle-", dir=output) as temporary:
        built = Path(temporary) / filename
        build_bundle(built, plugin / "skills")
        destination = output / filename
        if destination.exists() and destination.read_bytes() != built.read_bytes():
            raise ValueError(
                f"Published Skills {version} are immutable; increment the Skills revision in release.json."
            )
        release = {
            "version": version,
            "cli_min_version": minimum,
            "artifact": artifact(built, RAW_BASE),
        }
        old = next(
            (entry for entry in catalog["skills"] if entry["version"] == version), None
        )
        if old and old != release:
            raise ValueError(
                "Existing release metadata differs; increment the Skills revision."
            )
        # Validate every requested installer before changing the catalog or plugin metadata.
        cli_entries = []
        for cli_version in cli_versions:
            if not CLI_VERSION.fullmatch(cli_version):
                raise ValueError(f"Invalid CLI version: {cli_version}")
            installers = {}
            for platform, suffix in (
                ("linux-amd64", "amd64.deb"),
                ("windows-x64", "windows_x64.exe"),
            ):
                path = (
                    cli_directory or root / "resource/cli"
                ) / f"SimpoCLI_{cli_version}_{suffix}"
                if path.is_file():
                    installers[platform] = artifact(path, CLI_BASE)
            if not installers:
                raise ValueError(
                    f"No production installers found for CLI {cli_version}."
                )
            previous = next(
                (entry for entry in catalog["cli"] if entry["version"] == cli_version),
                None,
            )
            combined = dict(previous["artifacts"]) if previous else {}
            for platform, details in installers.items():
                if platform in combined and combined[platform] != details:
                    raise ValueError(
                        f"CLI {cli_version}/{platform} already published with different bytes."
                    )
                combined[platform] = details
            cli_entries.append({"version": cli_version, "artifacts": combined})
        if not destination.exists():
            write_atomic(destination, built.read_bytes())
    catalog["skills"] = [
        entry for entry in catalog["skills"] if entry["version"] != version
    ] + [release]
    for entry in cli_entries:
        catalog["cli"] = [
            old for old in catalog["cli"] if old["version"] != entry["version"]
        ] + [entry]
    catalog["cli"].sort(key=lambda entry: tuple(map(int, entry["version"].split("."))))
    catalog["skills"].sort(
        key=lambda entry: (
            *map(int, VERSION.fullmatch(entry["version"])[1].split(".")),
            int(VERSION.fullmatch(entry["version"])[2]),
        )
    )
    metadata_path = plugin / ".claude-plugin/plugin.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["version"] = version
    marketplace_path = root / ".claude-plugin/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    for entry in marketplace["plugins"]:
        if entry["name"] == "simpo":
            entry["version"] = version
    write_atomic(metadata_path, encode(metadata))
    write_atomic(marketplace_path, encode(marketplace))
    write_atomic(index_path, encode(catalog))
    return catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cli-version",
        action="append",
        default=[],
        help="Announce a CLI version whose installers have already been uploaded. Repeatable.",
    )
    parser.add_argument(
        "--cli-directory",
        type=Path,
        help="Directory containing uploaded production installers; defaults to resource/cli.",
    )
    args = parser.parse_args()
    try:
        catalog = publish(
            cli_versions=args.cli_version, cli_directory=args.cli_directory
        )
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Release build failed: {error}\n")
    print(
        f"Built {len(catalog['skills'])} Skills release(s), {len(catalog['cli'])} CLI release(s). Commit plugins/simpo/releases and both plugin metadata files after uploading the announced CLI installers."
    )


if __name__ == "__main__":
    main()
