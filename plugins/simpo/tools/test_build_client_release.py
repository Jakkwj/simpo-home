"""Only complete, checked and immutable Client installers may be announced."""

import hashlib
import json
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

    def installer(self, platform="linux-amd64", version="1.5.2", data=b"installer"):
        suffix = "_amd64.deb" if platform == "linux-amd64" else ".exe"
        path = self.root / f"SimpoClient_{version}{suffix}"
        path.write_bytes(data)
        receipt = {
            "schema_version": 1, "product": "SimpoClient", "version": version,
            "protocol_version": "1.5.1", "platform": platform, "offline": True,
            "url_protocol": "simpoclient", "artifact": {"filename": path.name,
                "size": len(data), "sha256": hashlib.sha256(data).hexdigest()},
        }
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
        publish([linux], catalog_path=self.catalog)
        self.assertEqual(before, self.catalog.read_bytes())
        result = publish([self.installer("windows-x64")], catalog_path=self.catalog)
        self.assertEqual(set(result["client"][0]["artifacts"]), {"linux-amd64", "windows-x64"})
        self.assertEqual(result["cli"], history["cli"])
        self.assertEqual(result["skills"], history["skills"])

    def test_old_client_cannot_be_announced_as_upgradable(self):
        before = self.catalog.read_bytes()
        with self.assertRaisesRegex(ValueError, "before 1.5.2"):
            publish([self.installer(version="1.5.1")], catalog_path=self.catalog)
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
        with self.assertRaisesRegex(ValueError, "already published"):
            publish([self.installer(data=b"new checked bytes")], catalog_path=self.catalog)
        self.assertEqual(before, self.catalog.read_bytes())

    def test_all_receipts_checked_before_catalog_write(self):
        path = self.installer()
        missing = self.root / "SimpoClient_1.5.2.exe"
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
