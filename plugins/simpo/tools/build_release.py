"""Build immutable Skills bundles and the public CLI/Skills release catalog.

Prepare the local catalog after building production installers. Upload and verify
the installer bytes before pushing the catalog to GitHub. The catalog and Skills
ZIPs themselves are committed to this repository. --cli-only registers CLI builds
without requiring a Skills export. No credentials or upload operations are used.
Only index-v2.json is read and updated; legacy index.json files are left untouched.
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
LEGACY_VERSION = re.compile(
    r"((?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))-skills\.([1-9][0-9]*)"
)
CLI_VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")
NAMES = (
    "simpo",
    "simpo-create-biomodel",
    "simpo-create-dataset",
    "simpo-create-project",
    "calculation-result-analysis",
)
RAW_BASE = (
    "https://raw.githubusercontent.com/Jakkwj/simpo-home/master/plugins/simpo/releases/"
)
CLI_BASE = "https://gitee.com/Jakkwj/simpo-home/releases/download/package/"


def version_key(value, *, skills=False):
    if isinstance(value, str) and CLI_VERSION.fullmatch(value):
        parts = tuple(map(int, value.split(".")))
        return (*parts, 1, 0) if skills else parts
    legacy = LEGACY_VERSION.fullmatch(value) if skills and isinstance(value, str) else None
    if legacy:
        return (*version_key(legacy[1]), 0, int(legacy[2]))
    raise ValueError(f"Invalid {'Skills' if skills else 'CLI'} version: {value!r}")


def read_catalog(path):
    catalog = (
        json.loads(path.read_text(encoding="utf-8"))
        if path.exists()
        else {"schema_version": 2, "cli": [], "skills": []}
    )
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 2:
        raise ValueError(f"Unsupported release catalog schema: {path}")
    for kind in ("cli", "skills"):
        entries = catalog.get(kind)
        if not isinstance(entries, list):
            raise ValueError(f"Invalid {kind} catalog: {path}")
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"Invalid release entry: {path}")
            version = entry.get("version")
            version_key(version, skills=kind == "skills")
            if version in seen:
                raise ValueError(f"Duplicate release {version}: {path}")
            seen.add(version)
            if kind == "skills":
                version_key(entry.get("cli_min_version"))
    return catalog


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


def verify_generated(plugin: Path):
    """Only publish exact allowlisted artifacts exported by SimpoSkills."""
    path = plugin / "generated.json"
    if not path.exists():
        return  # Legacy release fixtures/checkouts predating generated packages.
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("target") != "cli-public":
        raise ValueError("Invalid public generated manifest.")
    expected = manifest["files"]
    actual = {
        file.relative_to(plugin).as_posix()
        for file in (plugin / "skills").rglob("*")
        if file.is_file() and "__pycache__" not in file.parts and file.suffix not in {".pyc", ".pyo"}
    } | {"release.json"}
    if actual != set(expected):
        raise ValueError("Public Skill files differ from the allowlist; rebuild/export from SimpoSkills.")
    for name, digest in expected.items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or "\\" in name:
            raise ValueError("Unsafe generated file path.")
        file = plugin / relative
        if any(part.is_symlink() for part in [file, *file.parents]):
            raise ValueError("Do not publish linked generated files.")
        if hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Generated file changed: {name}; edit the SimpoSkills source and export again.")


def cli_entries(catalog, cli_versions, *, cli_directory=None, root=ROOT, platforms=()):
    """Validate selected immutable production artifacts before any catalog write."""
    entries = []
    available = (("linux-amd64", "amd64.deb"), ("windows-x64", "windows_x64.exe"))
    if set(platforms) - {name for name, _ in available}:
        raise ValueError("Unknown CLI platform.")
    for cli_version in cli_versions:
        version_key(cli_version)
        installers = {}
        for target, suffix in available:
            if platforms and target not in platforms:
                continue
            path = (cli_directory or root / "resource/cli") / f"SimpoCLI_{cli_version}_{suffix}"
            if path.is_file():
                details = artifact(path, CLI_BASE)
                if details["size"] > 512 * 1024 * 1024:
                    raise ValueError("CLI installer exceeds the updater's 512 MiB limit.")
                installers[target] = details
        if not installers or (platforms and set(platforms) - set(installers)):
            raise ValueError(f"No production installers found for CLI {cli_version} on the requested platforms.")
        previous = next((entry for entry in catalog["cli"] if entry["version"] == cli_version), None)
        combined = dict(previous["artifacts"]) if previous else {}
        for target, details in installers.items():
            if target in combined and combined[target] != details:
                raise ValueError(f"CLI {cli_version}/{target} already published with different bytes.")
            combined[target] = details
        entries.append({"version": cli_version, "artifacts": combined})
    return entries


def write_catalog(catalog, output):
    write_atomic(output / "index-v2.json", encode(catalog))


def publish_cli(*, cli_versions, cli_directory=None, platforms=(), plugin=PLUGIN, root=ROOT):
    """Register CLI independently of Skills source/export/package availability."""
    if not cli_versions:
        raise ValueError("Select at least one CLI version explicitly.")
    output = plugin / "releases"
    catalog = read_catalog(output / "index-v2.json")
    entries = cli_entries(catalog, cli_versions, cli_directory=cli_directory, root=root, platforms=platforms)
    for entry in entries:
        catalog["cli"] = [old for old in catalog["cli"] if old["version"] != entry["version"]] + [entry]
    catalog["cli"].sort(key=lambda entry: version_key(entry["version"]))
    write_catalog(catalog, output)
    return catalog


def publish(
    *,
    cli_versions=(),
    cli_directory: Path | None = None,
    plugin: Path = PLUGIN,
    root: Path = ROOT,
) -> dict:
    verify_generated(plugin)
    config = json.loads((plugin / "release.json").read_text(encoding="utf-8"))
    version, minimum = config["version"], config["cli_min_version"]
    version_key(version, skills=True)
    version_key(minimum)
    output = plugin / "releases"
    output.mkdir(parents=True, exist_ok=True)
    index_path = output / "index-v2.json"
    catalog = read_catalog(index_path)
    filename = f"SIMPOSkills_{version}.zip"
    with tempfile.TemporaryDirectory(prefix=".bundle-", dir=output) as temporary:
        built = Path(temporary) / filename
        build_bundle(built, plugin / "skills")
        destination = output / filename
        if destination.exists() and destination.read_bytes() != built.read_bytes():
            raise ValueError(
                f"Published Skills {version} are immutable; increment the Skill package version in SimpoSkills."
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
                "Existing release metadata differs; increment the Skill package version."
            )
        # Validate every requested installer before changing the catalog or plugin metadata.
        installers = cli_entries(catalog, cli_versions, cli_directory=cli_directory, root=root)
        if not destination.exists():
            write_atomic(destination, built.read_bytes())
    catalog["skills"] = [
        entry for entry in catalog["skills"] if entry["version"] != version
    ] + [release]
    for entry in installers:
        catalog["cli"] = [
            old for old in catalog["cli"] if old["version"] != entry["version"]
        ] + [entry]
    catalog["cli"].sort(key=lambda entry: version_key(entry["version"]))
    catalog["skills"].sort(key=lambda entry: version_key(entry["version"], skills=True))
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
    write_catalog(catalog, output)
    return catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cli-version",
        action="append",
        default=[],
        help="Prepare a selected CLI release locally; upload installers before pushing the catalog. Repeatable.",
    )
    parser.add_argument(
        "--cli-directory",
        type=Path,
        help="Directory containing built production installers; defaults to resource/cli.",
    )
    parser.add_argument("--cli-only", action="store_true", help="Register CLI installers without packaging Skills.")
    parser.add_argument("--platform", action="append", choices=("linux-amd64", "windows-x64"), default=[], help="CLI-only: register only the selected built platforms; repeatable.")
    args = parser.parse_args()
    if args.platform and not args.cli_only:
        parser.error("--platform requires --cli-only")
    try:
        if args.cli_only:
            catalog = publish_cli(cli_versions=args.cli_version, cli_directory=args.cli_directory, platforms=args.platform)
        else:
            catalog = publish(cli_versions=args.cli_version, cli_directory=args.cli_directory)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Release build failed: {error}\n")
    if args.cli_only:
        print(f"Updated local CLI catalog ({len(catalog['cli'])} release(s)); Skills and Client history preserved. Upload installers before pushing the catalog.")
    else:
        print(
            f"Built {len(catalog['skills'])} Skills release(s), {len(catalog['cli'])} CLI release(s). Commit plugins/simpo/releases and both plugin metadata files after uploading the announced CLI installers."
        )


if __name__ == "__main__":
    main()
