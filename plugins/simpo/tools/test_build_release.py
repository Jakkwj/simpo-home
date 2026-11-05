"""Release artifacts must be deterministic, complete and immutable."""

import importlib.util
import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

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
        self.assertFalse((self.plugin / "releases/index.json").exists())
        with zipfile.ZipFile(artifact) as archive:
            self.assertEqual(set(archive.namelist()),
                             {f"{name}/SKILL.md" for name in release.NAMES})
            self.assertIn("calculation-result-analysis/SKILL.md", archive.namelist())

    def test_balance_reference_is_bundled_and_required_entrypoint_checked(self):
        directory = self.plugin / "skills/calculation-result-analysis"
        (directory / "references").mkdir()
        (directory / "references/balance-analysis.md").write_text("Shared accounting rules")
        artifact = self.root / "test-balance.zip"
        release.build_bundle(artifact, self.plugin / "skills")
        with zipfile.ZipFile(artifact) as archive:
            self.assertEqual(archive.read("calculation-result-analysis/references/balance-analysis.md"),
                             b"Shared accounting rules")
        (directory / "SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing Skill: calculation-result-analysis"):
            release.build_bundle(self.root / "missing-balance.zip", self.plugin / "skills")

    def test_bundle_updates_plugin_version(self):
        self.publish()
        self.assertEqual(
            json.loads((self.plugin / ".claude-plugin/plugin.json").read_text())[
                "version"
            ],
            "0.1.8-skills.1",
        )

    def test_changed_skills_require_new_revision(self):
        self.publish()
        index = self.plugin / "releases/index-v2.json"
        before = index.read_bytes()
        (self.plugin / "skills/simpo/SKILL.md").write_text("New workflow")
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.publish()
        self.assertEqual(index.read_bytes(), before)
        (self.plugin / "release.json").write_text(
            '{"version":"0.1.8-skills.2","cli_min_version":"0.1.7"}'
        )
        self.assertEqual(len(self.publish()["skills"]), 2)

    def test_skills_publishing_preserves_client_release_history(self):
        catalog = self.publish()
        clients = [{"version": "1.5.2", "offline": True, "artifacts": {}}]
        catalog["client"] = clients
        (self.plugin / "releases/index-v2.json").write_text(json.dumps(catalog))
        self.assertEqual(self.publish()["client"], clients)

    def test_independent_version_preserves_v2_history_and_existing_bundles(self):
        old_catalog = self.publish()
        old_zip = self.plugin / "releases/SIMPOSkills_0.1.8-skills.1.zip"
        old_bytes = old_zip.read_bytes()
        (self.plugin / "release.json").write_text(
            '{"version":"1.0.0","cli_min_version":"0.1.9"}'
        )
        catalog = self.publish()
        self.assertEqual(catalog["schema_version"], 2)
        self.assertEqual([e["version"] for e in catalog["skills"]], ["0.1.8-skills.1", "1.0.0"])
        self.assertEqual(catalog["skills"][0], old_catalog["skills"][0])
        self.assertEqual(old_zip.read_bytes(), old_bytes)
        self.assertEqual(catalog, self.publish())
        self.assertEqual(json.loads((self.plugin / ".claude-plugin/plugin.json").read_text())["version"], "1.0.0")
        self.assertFalse((self.plugin / "releases/index.json").exists())
        index = self.plugin / "releases/index-v2.json"
        before = index.read_bytes()
        (self.plugin / "skills/simpo/SKILL.md").write_text("Different bytes")
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.publish()
        self.assertEqual(index.read_bytes(), before)

    def test_numeric_versions_and_stable_release_order(self):
        versions = ["1.10.0", "1.2.0", "0.1.8-skills.10", "0.1.8-skills.2", "1.0.0-skills.100", "1.0.0"]
        self.assertEqual(sorted(versions, key=lambda v: release.version_key(v, skills=True)),
                         ["0.1.8-skills.2", "0.1.8-skills.10", "1.0.0-skills.100", "1.0.0", "1.2.0", "1.10.0"])
        for version in ("01.0.0", "1.0", "1.0.0-beta.1", "1.0.0+build", "0.1.8-skills.0", None):
            with self.subTest(version=version), self.assertRaises(ValueError):
                release.version_key(version, skills=True)

    def test_both_publishers_ignore_existing_legacy_catalog_without_rewriting_it(self):
        catalog = self.publish()
        catalog["client"] = [{"version": "1.5.2", "offline": True, "artifacts": {}}]
        index = self.plugin / "releases/index-v2.json"
        legacy_path = self.plugin / "releases/index.json"
        legacy = json.loads(json.dumps(catalog))
        legacy["schema_version"] = 1
        legacy.pop("client")
        legacy["skills"][0]["artifact"]["sha256"] = "0" * 64
        legacy["skills"].append({
            "version": "0.1.7-skills.1", "cli_min_version": "0.1.7",
            "artifact": legacy["skills"][0]["artifact"],
        })
        legacy["cli"] = [{"version": "0.1.7", "artifacts": {}}]
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        (directory / "SimpoCLI_0.1.9_amd64.deb").write_bytes(b"linux")
        publishers = {
            "skills": lambda: self.publish(cli_versions=["0.1.9"]),
            "cli": lambda: release.publish_cli(cli_versions=["0.1.9"], root=self.root, plugin=self.plugin),
        }
        legacy_contents = {
            "conflicting_and_legacy_only_releases": json.dumps(legacy).encode(),
            "malformed": b"not valid JSON\n",
        }
        for name, publish in publishers.items():
            for state, contents in legacy_contents.items():
                with self.subTest(publisher=name, legacy=state):
                    index.write_text(json.dumps(catalog))
                    legacy_path.write_bytes(contents)
                    result = publish()
                    self.assertEqual(result["skills"], catalog["skills"])
                    self.assertEqual(result["client"], catalog["client"])
                    self.assertEqual([entry["version"] for entry in result["cli"]], ["0.1.9"])
                    self.assertEqual(json.loads(index.read_text()), result)
                    self.assertEqual(legacy_path.read_bytes(), contents)

    def test_missing_v2_does_not_recover_releases_from_legacy_catalog(self):
        legacy = self.publish()
        legacy["schema_version"] = 1
        legacy["cli"] = [{"version": "0.1.7", "artifacts": {}}]
        legacy_path = self.plugin / "releases/index.json"
        legacy_bytes = json.dumps(legacy).encode()
        legacy_path.write_bytes(legacy_bytes)
        (self.plugin / "release.json").write_text(
            '{"version":"1.0.0","cli_min_version":"0.1.9"}'
        )
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        (directory / "SimpoCLI_0.1.9_amd64.deb").write_bytes(b"linux")
        publishers = {
            "skills": (lambda: self.publish(cli_versions=["0.1.9"]), ["1.0.0"]),
            "cli": (lambda: release.publish_cli(cli_versions=["0.1.9"], root=self.root, plugin=self.plugin), []),
        }
        index = self.plugin / "releases/index-v2.json"
        for name, (publish, skills_versions) in publishers.items():
            with self.subTest(publisher=name):
                index.unlink()
                result = publish()
                self.assertEqual(result["schema_version"], 2)
                self.assertEqual([entry["version"] for entry in result["cli"]], ["0.1.9"])
                self.assertEqual([entry["version"] for entry in result["skills"]], skills_versions)
                self.assertEqual(json.loads(index.read_text()), result)
                self.assertEqual(legacy_path.read_bytes(), legacy_bytes)

    def test_invalid_v2_is_rejected_without_legacy_fallback(self):
        catalog = self.publish()
        catalog["schema_version"] = 1
        legacy_bytes = json.dumps(catalog).encode()
        index = self.plugin / "releases/index-v2.json"
        legacy_path = index.with_name("index.json")
        legacy_path.write_bytes(legacy_bytes)
        invalid_catalogs = {
            "legacy_schema": (legacy_bytes, "Unsupported release catalog schema"),
            "malformed_json": (b"not valid JSON\n", "Expecting value"),
            "invalid_entries": (b'{"schema_version":2,"cli":[],"skills":null}', "Invalid skills catalog"),
        }
        for name, publish in {
            "skills": self.publish,
            "cli": lambda: release.publish_cli(cli_versions=["0.1.9"], root=self.root, plugin=self.plugin),
        }.items():
            for state, (contents, message) in invalid_catalogs.items():
                with self.subTest(publisher=name, invalid_v2=state):
                    index.write_bytes(contents)
                    with self.assertRaisesRegex(ValueError, message):
                        publish()
                    self.assertEqual(index.read_bytes(), contents)
                    self.assertEqual(legacy_path.read_bytes(), legacy_bytes)

    def generated_manifest(self):
        files = {"release.json": hashlib.sha256((self.plugin / "release.json").read_bytes()).hexdigest()}
        for name in release.NAMES:
            key = f"skills/{name}/SKILL.md"
            files[key] = hashlib.sha256((self.plugin / key).read_bytes()).hexdigest()
        (self.plugin / "generated.json").write_text(json.dumps({"schema_version": 1, "target": "cli-public", "files": files}))

    def test_generated_public_package_rejects_unlisted_private_file(self):
        self.generated_manifest()
        self.publish()
        index = self.plugin / "releases/index-v2.json"
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
        self.assertFalse((self.plugin / "releases/index-v2.json").exists())
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

    def test_cli_only_does_not_require_or_touch_skills_exports(self):
        catalog = self.publish()
        catalog["client"] = [{"version": "1.5.2", "offline": True, "artifacts": {}}]
        index = self.plugin / "releases/index-v2.json"
        index.write_text(json.dumps(catalog))
        # Deliberately corrupt the Skills export. A CLI-only release must remain
        # independent and must not rewrite ZIPs, generated files or metadata.
        (self.plugin / "release.json").write_text("not a Skills release")
        self.generated_manifest()
        protected = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file() and path.name not in {"index-v2.json", "index.json"}}
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        (directory / "SimpoCLI_0.1.9_amd64.deb").write_bytes(b"linux")
        (directory / "SimpoCLI_0.1.9_windows_x64.exe").write_bytes(b"windows")
        result = release.publish_cli(cli_versions=["0.1.9"], platforms=["linux-amd64"], root=self.root, plugin=self.plugin)
        self.assertEqual(set(result["cli"][0]["artifacts"]), {"linux-amd64"})
        result = release.publish_cli(cli_versions=["0.1.9"], platforms=["windows-x64"], root=self.root, plugin=self.plugin)
        self.assertEqual(set(result["cli"][0]["artifacts"]), {"linux-amd64", "windows-x64"})
        self.assertEqual(result["skills"], catalog["skills"])
        self.assertEqual(result["client"], catalog["client"])
        self.assertFalse(index.with_name("index.json").exists())
        for path, before in protected.items():
            self.assertEqual(path.read_bytes(), before)

    def test_cli_only_failures_leave_v2_and_existing_legacy_file_unchanged(self):
        self.publish()
        (self.plugin / "releases/index.json").write_bytes(b"Frozen legacy catalog\n")
        indexes = [self.plugin / "releases" / name for name in ("index.json", "index-v2.json")]
        before = [path.read_bytes() for path in indexes]
        for versions, platforms in (([], []), (["0.1.9"], ["windows-x64"]), (["0.1.9"], ["unknown"])):
            with self.subTest(versions=versions, platforms=platforms), self.assertRaises(ValueError):
                release.publish_cli(cli_versions=versions, platforms=platforms, root=self.root, plugin=self.plugin)
            self.assertEqual([path.read_bytes() for path in indexes], before)
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        installer = directory / "SimpoCLI_0.1.9_amd64.deb"
        installer.write_bytes(b"first installer")
        release.publish_cli(cli_versions=["0.1.9"], root=self.root, plugin=self.plugin)
        before = [path.read_bytes() for path in indexes]
        installer.write_bytes(b"replacement of same version")
        with self.assertRaisesRegex(ValueError, "different bytes"):
            release.publish_cli(cli_versions=["0.1.9"], root=self.root, plugin=self.plugin)
        self.assertEqual([path.read_bytes() for path in indexes], before)

    def test_cli_replacement_updates_only_selected_version_and_platform(self):
        catalog = self.publish()
        catalog["client"] = [{"version": "1.6.0", "offline": True, "artifacts": {}}]
        index = self.plugin / "releases/index-v2.json"
        index.write_text(json.dumps(catalog))
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        for version in ("0.1.9", "0.2.0"):
            for suffix in ("amd64.deb", "windows_x64.exe"):
                (directory / f"SimpoCLI_{version}_{suffix}").write_bytes(f"{version}/{suffix}".encode())
        before = release.publish_cli(
            cli_versions=["0.1.9", "0.2.0"], root=self.root, plugin=self.plugin,
        )
        before["cli"][1]["offline"] = False
        index.write_text(json.dumps(before))
        linux = directory / "SimpoCLI_0.2.0_amd64.deb"
        linux.write_bytes(b"rebuilt Linux installer")
        # Another platform on disk may also have changed, but it is not selected.
        (directory / "SimpoCLI_0.2.0_windows_x64.exe").write_bytes(b"unselected Windows installer")
        saved = index.read_bytes()
        with self.assertRaisesRegex(ValueError, "local catalog.*--replace-existing"):
            release.publish_cli(
                cli_versions=["0.2.0"], platforms=["linux-amd64"],
                root=self.root, plugin=self.plugin,
            )
        self.assertEqual(index.read_bytes(), saved)
        result = release.publish_cli(
            cli_versions=["0.2.0"], platforms=["linux-amd64"],
            root=self.root, plugin=self.plugin, replace_existing=True,
        )
        expected = json.loads(json.dumps(before))
        expected["cli"][1]["artifacts"]["linux-amd64"] = release.artifact(linux, release.CLI_BASE)
        self.assertEqual(result, expected)
        self.assertEqual(json.loads(index.read_text()), expected)
        self.assertFalse(index.with_name("index.json").exists())

    def test_cli_replacement_validates_all_versions_before_catalog_write(self):
        self.publish()
        directory = self.root / "resource/cli"
        directory.mkdir(parents=True)
        installer = directory / "SimpoCLI_0.2.0_amd64.deb"
        installer.write_bytes(b"first installer")
        release.publish_cli(cli_versions=["0.2.0"], root=self.root, plugin=self.plugin)
        index = self.plugin / "releases/index-v2.json"
        before = index.read_bytes()
        installer.write_bytes(b"replacement installer")
        for invalid_version, contents, message in (
            ("0.2.1", None, "No production installers"),
            ("0.2.1", b"", "Empty artifact"),
            ("invalid-version", None, "Invalid CLI version"),
        ):
            with self.subTest(version=invalid_version, contents=contents):
                if contents is not None:
                    (directory / f"SimpoCLI_{invalid_version}_amd64.deb").write_bytes(contents)
                with self.assertRaisesRegex(ValueError, message):
                    release.publish_cli(
                        cli_versions=["0.2.0", invalid_version],
                        platforms=["linux-amd64"], root=self.root, plugin=self.plugin,
                        replace_existing=True,
                    )
                self.assertEqual(index.read_bytes(), before)

    def test_cli_parser_forwards_replacement_and_rejects_it_for_skills(self):
        with (
            mock.patch.object(sys, "argv", [
                "build_release.py", "--cli-only", "--cli-version", "0.2.0",
                "--platform", "windows-x64", "--replace-existing",
            ]),
            mock.patch.object(release, "publish_cli", return_value={"cli": []}) as cli,
            mock.patch.object(release, "publish") as skills,
            mock.patch("sys.stdout", new_callable=io.StringIO),
        ):
            release.main()
            cli.assert_called_once_with(
                cli_versions=["0.2.0"], cli_directory=None,
                platforms=["windows-x64"], replace_existing=True,
            )
            skills.assert_not_called()
        with (
            mock.patch.object(sys, "argv", ["build_release.py", "--replace-existing"]),
            mock.patch.object(release, "publish_cli") as cli,
            mock.patch.object(release, "publish") as skills,
            mock.patch("sys.stderr", new_callable=io.StringIO) as errors,
        ):
            with self.assertRaises(SystemExit) as error:
                release.main()
            self.assertEqual(error.exception.code, 2)
            self.assertIn("--replace-existing requires --cli-only", errors.getvalue())
            cli.assert_not_called()
            skills.assert_not_called()


if __name__ == "__main__":
    unittest.main()
