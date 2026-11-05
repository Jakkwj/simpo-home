"""Add explicitly selected Client installers and application packages to the shared release catalog.

The Client builder invokes this after creating its checked installer and
<installer>.build.json. This tool prepares local metadata only. Upload and
verify the exact installer bytes BEFORE pushing the catalog to GitHub; this
tool never uploads files or updates deployed services.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_release import CLI_BASE, PLUGIN, artifact, encode, read_catalog, version_key, write_atomic


def checked_release(installer: Path) -> tuple[str, str, dict, dict | None]:
    installer = Path(installer)
    receipt_path = installer.with_name(installer.name + ".build.json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (receipt.get("schema_version") != 1 or receipt.get("product") != "SimpoClient"
            or receipt.get("url_protocol") != "simpoclient"):
        raise ValueError("A checked SimpoClient build receipt is required.")
    split = receipt.get("distribution") == "split"
    if not split and receipt.get("offline") is not True:
        raise ValueError("A complete offline SimpoClient build receipt is required.")
    version = receipt.get("version")
    if version_key(version) < (1, 5, 2):
        raise ValueError("Client releases before 1.5.2 do not support command-line upgrades.")
    version_key(receipt.get("protocol_version"))
    platform = receipt.get("platform")
    filenames = {
        "linux-amd64": f"SimpoClient_{version}_amd64.deb",
        "windows-x64": f"SimpoClient_{version}.exe",
    }
    if platform not in filenames or installer.name != filenames[platform]:
        raise ValueError("Installer name does not match the receipt version and platform.")
    details = artifact(installer, CLI_BASE)
    expected = {"filename": installer.name, "size": details["size"], "sha256": details["sha256"]}
    if receipt.get("artifact") != expected:
        raise ValueError("Installer bytes differ from its checked build receipt.")
    if details["size"] > 4 * 1024 ** 3:
        raise ValueError("Installer exceeds the Client updater's 4 GiB limit.")
    package = None
    if split:
        name = "package.tar.xz" if platform == "linux-amd64" else "package.zip"
        package = artifact(installer.parent / name, CLI_BASE)
        expected = {"filename": name, "size": package["size"], "sha256": package["sha256"]}
        if receipt.get("package") != expected:
            raise ValueError("Application package bytes differ from its checked build receipt.")
        if package["size"] > 4 * 1024 ** 3:
            raise ValueError("Application package exceeds the Client updater's 4 GiB limit.")
    return version, platform, details, package


def publish(installers, *, catalog_path: Path = PLUGIN / "releases/index-v2.json") -> dict:
    if not installers:
        raise ValueError("Select at least one built installer explicitly.")
    catalog = read_catalog(catalog_path, 2)
    clients = catalog.setdefault("client", [])
    if not isinstance(clients, list):
        raise ValueError("Invalid Client release catalog.")
    entries = {}
    for entry in clients:
        version = entry["version"]
        version_key(version)
        if version in entries or not (entry.get("offline") is True or entry.get("distribution") == "split"):
            raise ValueError("Duplicate or unsupported Client release in catalog.")
        entries[version] = entry
    # Check every receipt and immutable platform before any catalog write.
    for installer in installers:
        version, platform, details, package = checked_release(Path(installer))
        split = package is not None
        default = {"version": version, "offline": not split, "artifacts": {}}
        if split:
            default.update(distribution="split", packages={})
        entry = entries.setdefault(version, default)
        if (entry.get("distribution") == "split") != split:
            raise ValueError(f"Client {version} already uses a different distribution format.")
        if split:
            previous_package = entry["packages"].get(platform)
            if previous_package and previous_package != package:
                raise ValueError(f"Client {version}/{platform} package already published with different bytes.")
            entry["packages"][platform] = package
        previous = entry["artifacts"].get(platform)
        if previous and previous != details:
            raise ValueError(f"Client {version}/{platform} already published with different bytes.")
        entry["artifacts"][platform] = details
    catalog["client"] = sorted(entries.values(), key=lambda entry: version_key(entry["version"]))
    write_atomic(catalog_path, encode(catalog))
    return catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("installers", nargs="+", type=Path)
    parser.add_argument("--catalog", type=Path, default=PLUGIN / "releases/index-v2.json")
    args = parser.parse_args()
    publish(args.installers, catalog_path=args.catalog)
    print(f"Updated local Client catalog: {args.catalog}")


if __name__ == "__main__":
    main()
