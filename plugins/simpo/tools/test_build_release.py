"""Release artifacts must be deterministic, complete and immutable."""

import importlib.util
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "simpo_build_release", Path(__file__).with_name("build_release.py")
)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseBuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.plugin = self.root / "plugins/simpo"
        for name in release.NAMES:
            directory = self.plugin / "skills" / name
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text("Workflow")
            (directory / "__pycache__").mkdir()
            (directory / "__pycache__/test.pyc").write_bytes(b"cache")
        for directory in (self.plugin / ".claude-plugin", self.root / ".claude-plugin"):
            directory.mkdir(parents=True)
        (self.plugin / ".claude-plugin/plugin.json").write_text(
            '{"name":"simpo","version":"0.5.0"}'
        )
        (self.root / ".claude-plugin/marketplace.json").write_text(
            '{"plugins":[{"name":"simpo","version":"0.5.0"}]}'
        )
        (self.plugin / "release.json").write_text(
            '{"version":"0.1.8-skills.1","cli_min_version":"0.1.7"}'
        )

    def publish(self, **kwargs):
        return release.publish(plugin=self.plugin, root=self.root, **kwargs)

    def test_bundle_repeatable_excludes_caches_and_syncs_metadata(self):
        catalog = self.publish()
        artifact = self.plugin / "releases/SIMPOSkills_0.1.8-skills.1.zip"
        before = artifact.read_bytes()
        self.assertEqual(catalog["cli"], [])
        self.assertEqual(catalog, self.publish())
        self.assertEqual(before, artifact.read_bytes())
        with zipfile.ZipFile(artifact) as archive:
            self.assertEqual(len(archive.namelist()), 4)
        self.assertEqual(
            json.loads((self.plugin / ".claude-plugin/plugin.json").read_text())[
                "version"
            ],
            "0.1.8-skills.1",
        )

    def test_changed_skills_require_new_revision(self):
        self.publish()
        index = self.plugin / "releases/index.json"
        before = index.read_bytes()
        (self.plugin / "skills/simpo/SKILL.md").write_text("New workflow")
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.publish()
        self.assertEqual(index.read_bytes(), before)
        (self.plugin / "release.json").write_text(
            '{"version":"0.1.8-skills.2","cli_min_version":"0.1.7"}'
        )
        self.assertEqual(len(self.publish()["skills"]), 2)

    def test_independent_version_migrates_history_and_preserves_old_cli_catalog(self):
        old_catalog = self.publish()
        old_zip = self.plugin / "releases/SIMPOSkills_0.1.8-skills.1.zip"
        old_bytes = old_zip.read_bytes()
        legacy_path = self.plugin / "releases/index.json"
        legacy_bytes = legacy_path.read_bytes()
        # Simulate the first upgrade from a publisher that only wrote schema 1.
        (self.plugin / "releases/index-v2.json").unlink()
        (self.plugin / "release.json").write_text(
            '{"version":"1.0.0","cli_min_version":"0.1.9"}'
        )
        catalog = self.publish()
        self.assertEqual(catalog["schema_version"], 2)
        self.assertEqual([e["version"] for e in catalog["skills"]], ["0.1.8-skills.1", "1.0.0"])
        self.assertEqual(catalog["skills"][0], old_catalog["skills"][0])
        self.assertEqual(legacy_path.read_bytes(), legacy_bytes)
        self.assertEqual(old_zip.read_bytes(), old_bytes)
        self.assertEqual(catalog, self.publish())
        self.assertEqual(json.loads((self.plugin / ".claude-plugin/plugin.json").read_text())["version"], "1.0.0")
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        (directory / "SimpoCLI_0.1.9_amd64.deb").write_bytes(b"new CLI")
        catalog = self.publish(cli_versions=["0.1.9"])
        legacy = json.loads(legacy_path.read_text())
        self.assertEqual(legacy["cli"], catalog["cli"])
        self.assertEqual([e["version"] for e in legacy["skills"]], ["0.1.8-skills.1"])
        (self.plugin / "skills/simpo/SKILL.md").write_text("Different bytes")
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.publish()

    def test_numeric_versions_and_stable_release_order(self):
        versions = ["1.10.0", "1.2.0", "0.1.8-skills.10", "0.1.8-skills.2", "1.0.0-skills.100", "1.0.0"]
        self.assertEqual(sorted(versions, key=lambda v: release.version_key(v, skills=True)),
                         ["0.1.8-skills.2", "0.1.8-skills.10", "1.0.0-skills.100", "1.0.0", "1.2.0", "1.10.0"])
        for version in ("01.0.0", "1.0", "1.0.0-beta.1", "1.0.0+build", "0.1.8-skills.0", None):
            with self.subTest(version=version), self.assertRaises(ValueError):
                release.version_key(version, skills=True)

    def test_conflicting_history_fails_before_writing(self):
        self.publish()
        path = self.plugin / "releases/index-v2.json"
        before = path.read_bytes()
        legacy_path = self.plugin / "releases/index.json"
        legacy = json.loads(legacy_path.read_text())
        legacy["skills"][0]["artifact"]["sha256"] = "0" * 64
        legacy_path.write_text(json.dumps(legacy))
        with self.assertRaisesRegex(ValueError, "disagree on immutable"):
            self.publish()
        self.assertEqual(path.read_bytes(), before)

    def generated_manifest(self):
        files = {"release.json": hashlib.sha256((self.plugin / "release.json").read_bytes()).hexdigest()}
        for name in release.NAMES:
            key = f"skills/{name}/SKILL.md"
            files[key] = hashlib.sha256((self.plugin / key).read_bytes()).hexdigest()
        (self.plugin / "generated.json").write_text(json.dumps({"schema_version": 1, "target": "cli-public", "files": files}))

    def test_generated_public_package_rejects_unlisted_private_file(self):
        self.generated_manifest()
        self.publish()
        index = self.plugin / "releases/index.json"
        before = index.read_bytes()
        (self.plugin / "skills/simpo/private-note.md").write_text("Internal instructions")
        with self.assertRaisesRegex(ValueError, "allowlist"):
            self.publish()
        self.assertEqual(index.read_bytes(), before)

    def test_generated_package_rejects_edits_before_publishing(self):
        self.generated_manifest()
        (self.plugin / "skills/simpo/SKILL.md").write_text("Unreviewed edits")
        with self.assertRaisesRegex(ValueError, "Generated file changed"):
            self.publish()
        self.assertFalse((self.plugin / "releases/index.json").exists())

    def test_explicit_cli_versions_missing_installers_and_platform_merge(self):
        with self.assertRaisesRegex(ValueError, "No production installers"):
            self.publish(cli_versions=["0.1.8"])
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        linux = directory / "SimpoCLI_0.1.8_amd64.deb"
        linux.write_bytes(b"linux")
        self.assertEqual(self.publish()["cli"], [])
        self.assertEqual(
            set(self.publish(cli_versions=["0.1.8"])["cli"][0]["artifacts"]),
            {"linux-amd64"},
        )
        (directory / "SimpoCLI_0.1.8_windows_x64.exe").write_bytes(b"windows")
        self.assertEqual(
            len(self.publish(cli_versions=["0.1.8"])["cli"][0]["artifacts"]), 2
        )
        linux.write_bytes(b"different")
        with self.assertRaisesRegex(ValueError, "different bytes"):
            self.publish(cli_versions=["0.1.8"])


if __name__ == "__main__":
    unittest.main()
