"""Client catalog writes require checked builds and explicit draft replacements."""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from build_client_release import publish


class ClientReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.catalog = self.root / "index-v2.json"
        self.catalog.write_text(json.dumps({"schema_version": 2, "cli": [], "skills": [], "client": []}))

    def installer(self, platform="linux-amd64", version="1.6.0", data=b"installer",
                  package_data=None):
        suffix = "_amd64.deb" if platform == "linux-amd64" else ".exe"
        path = self.root / f"SimpoClient_{version}{suffix}"
        path.write_bytes(data)
        receipt = {
            "schema_version": 1, "product": "SimpoClient", "version": version,
            "protocol_version": "1.5.1", "platform": platform, "offline": True,
            "url_protocol": "simpoclient", "artifact": {"filename": path.name,
                "size": len(data), "sha256": hashlib.sha256(data).hexdigest()},
        }
        if package_data is not None:
            package_name = "package.tar.xz" if platform == "linux-amd64" else "package.zip"
            (path.parent / package_name).write_bytes(package_data)
            receipt.update(distribution="split", offline=False, package={
                "filename": package_name, "size": len(package_data),
                "sha256": hashlib.sha256(package_data).hexdigest(),
            })
        path.with_name(path.name + ".build.json").write_text(json.dumps(receipt))
        return path

    def test_merge_platforms_and_preserve_cli_skills(self):
        history = {"schema_version": 2,
                   "cli": [{"version": "0.1.9", "artifacts": {}}],
                   "skills": [{"version": "1.0.0", "cli_min_version": "0.1.9", "artifact": {}}],
                   "client": []}
        self.catalog.write_text(json.dumps(history))
        linux = self.installer()
        result = publish([linux], catalog_path=self.catalog)
        before = self.catalog.read_bytes()
        self.assertTrue(result["client"][0]["offline"])
        self.assertEqual(result["client"][0]["version"], "1.6.0")
        publish([linux], catalog_path=self.catalog)
        self.assertEqual(before, self.catalog.read_bytes())
        result = publish([self.installer("windows-x64")], catalog_path=self.catalog)
        self.assertEqual(set(result["client"][0]["artifacts"]), {"linux-amd64", "windows-x64"})
        self.assertEqual(result["cli"], history["cli"])
        self.assertEqual(result["skills"], history["skills"])

    def test_old_client_cannot_be_announced_as_upgradable(self):
        before = self.catalog.read_bytes()
        for version in ("1.5.1", "1.5.2", "1.5.9"):
            with self.subTest(version=version):
                with self.assertRaisesRegex(ValueError, r"before 1\.6\.0"):
                    publish([self.installer(version=version)], catalog_path=self.catalog)
                self.assertEqual(before, self.catalog.read_bytes())

    def test_modified_installer_and_immutable_release_fail_before_writing(self):
        path = self.installer()
        before = self.catalog.read_bytes()
        path.write_bytes(b"different bytes")
        with self.assertRaisesRegex(ValueError, "differ from"):
            publish([path], catalog_path=self.catalog)
        self.assertEqual(before, self.catalog.read_bytes())
        publish([self.installer()], catalog_path=self.catalog)
        before = self.catalog.read_bytes()
        with self.assertRaisesRegex(ValueError, "already registered in local catalog.*--replace-existing"):
            publish([self.installer(data=b"new checked bytes")], catalog_path=self.catalog)
        self.assertEqual(before, self.catalog.read_bytes())

    def test_split_changes_require_explicit_replacement(self):
        publish([self.installer(package_data=b"package")], catalog_path=self.catalog)
        before = self.catalog.read_bytes()
        for data, package in ((b"installer", b"new package"), (b"new installer", b"package")):
            with self.subTest(data=data, package=package):
                path = self.installer(data=data, package_data=package)
                with self.assertRaisesRegex(ValueError, "already registered in local catalog.*--replace-existing"):
                    publish([path], catalog_path=self.catalog)
                self.assertEqual(before, self.catalog.read_bytes())

    def test_replace_selected_split_platform_preserves_other_metadata(self):
        history = {"schema_version": 2,
                   "cli": [{"version": "0.2.0", "artifacts": {}}],
                   "skills": [{"version": "1.0.1", "cli_min_version": "0.2.0", "artifact": {}}],
                   "client": []}
        self.catalog.write_text(json.dumps(history))
        publish([self.installer(package_data=b"linux package"),
                 self.installer("windows-x64", package_data=b"windows package"),
                 self.installer(version="1.7.0")], catalog_path=self.catalog)
        before = json.loads(self.catalog.read_text())
        path = self.installer("windows-x64", data=b"new installer", package_data=b"new package")
        result = publish([path], catalog_path=self.catalog, replace_existing=True)
        expected = json.loads(json.dumps(before))
        for field, data in (("artifacts", b"new installer"), ("packages", b"new package")):
            expected["client"][0][field]["windows-x64"].update(
                size=len(data), sha256=hashlib.sha256(data).hexdigest(),
            )
        self.assertEqual(expected, result)
        self.assertEqual(expected, json.loads(self.catalog.read_text()))

    def test_replacement_still_validates_receipt_and_distribution(self):
        publish([self.installer(package_data=b"package")], catalog_path=self.catalog)
        before = self.catalog.read_bytes()
        for invalid in ("installer", "package", "protocol", "version", "platform", "distribution"):
            with self.subTest(invalid=invalid):
                path = self.installer(data=b"new installer", package_data=b"new package")
                receipt_path = path.with_name(path.name + ".build.json")
                receipt = json.loads(receipt_path.read_text())
                if invalid == "installer":
                    path.write_bytes(b"tampered installer")
                elif invalid == "package":
                    (path.parent / "package.tar.xz").write_bytes(b"tampered package")
                elif invalid == "protocol":
                    receipt["url_protocol"] = "wrong-protocol"
                elif invalid == "version":
                    receipt["version"] = "1.5.2"
                elif invalid == "platform":
                    receipt["platform"] = "windows-x64"
                else:
                    receipt.pop("distribution")
                    receipt.pop("package")
                    receipt["offline"] = True
                receipt_path.write_text(json.dumps(receipt))
                with self.assertRaises(ValueError):
                    publish([path], catalog_path=self.catalog, replace_existing=True)
                self.assertEqual(before, self.catalog.read_bytes())

    def test_invalid_second_build_does_not_write_first_replacement(self):
        publish([self.installer(package_data=b"package"),
                 self.installer("windows-x64", package_data=b"package")], catalog_path=self.catalog)
        before = self.catalog.read_bytes()
        linux = self.installer(data=b"new installer", package_data=b"new package")
        windows = self.installer("windows-x64", data=b"new installer", package_data=b"new package")
        (windows.parent / "package.zip").write_bytes(b"tampered package")
        with self.assertRaisesRegex(ValueError, "Application package bytes differ"):
            publish([linux, windows], catalog_path=self.catalog, replace_existing=True)
        self.assertEqual(before, self.catalog.read_bytes())

    def test_command_line_replaces_checked_local_build(self):
        publish([self.installer()], catalog_path=self.catalog)
        path = self.installer(data=b"new installer")
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("build_client_release.py")),
             str(path), "--catalog", str(self.catalog), "--replace-existing"],
            capture_output=True, text=True, check=True,
        )
        self.assertIn("Updated local Client catalog", completed.stdout)
        details = json.loads(self.catalog.read_text())["client"][0]["artifacts"]["linux-amd64"]
        self.assertEqual(details["sha256"], hashlib.sha256(b"new installer").hexdigest())

    def test_all_receipts_checked_before_catalog_write(self):
        path = self.installer()
        missing = self.root / "SimpoClient_1.6.0.exe"
        missing.write_bytes(b"unreviewed")
        before = self.catalog.read_bytes()
        with self.assertRaises(FileNotFoundError):
            publish([path, missing], catalog_path=self.catalog)
        self.assertEqual(before, self.catalog.read_bytes())

    def test_nonoffline_receipt_is_rejected(self):
        path = self.installer()
        receipt_path = path.with_name(path.name + ".build.json")
        receipt = json.loads(receipt_path.read_text())
        receipt.pop("offline")
        receipt_path.write_text(json.dumps(receipt))
        before = self.catalog.read_bytes()
        with self.assertRaisesRegex(ValueError, "offline"):
            publish([path], catalog_path=self.catalog)
        self.assertEqual(before, self.catalog.read_bytes())


if __name__ == "__main__":
    unittest.main()
