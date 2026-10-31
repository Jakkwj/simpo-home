"""Release artifacts must be deterministic, complete and immutable."""

import importlib.util
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
