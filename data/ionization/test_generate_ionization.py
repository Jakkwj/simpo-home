"""Reference generation, drift detection, and preservation of handwritten text."""

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import generate_ionization as gen


class IonizationGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "SimpoHome"
        self.backend = Path(self.temp.name) / "SimpoBackend/backend/litestar"
        self.installed = Path(self.temp.name) / "skills"
        self.data = json.loads((gen.ROOT / gen.SOURCE).read_text())
        (self.root / gen.SOURCE).parent.mkdir(parents=True)
        self.write_data()
        self.targets = [
            *(self.root / p for p in gen.DOCS.values()),
            self.root / gen.CLI_REFERENCE,
            self.backend / gen.AI_REFERENCE,
            self.installed
            / "simpo-create-biomodel/references/ionization-derivation.md",
        ]
        for path in self.targets:
            path.parent.mkdir(parents=True, exist_ok=True)
            begin, end = (
                (
                    "{/* BEGIN GENERATED IONIZATION */}",
                    "{/* END GENERATED IONIZATION */}",
                )
                if path.suffix == ".mdx"
                else (
                    "<!-- BEGIN GENERATED IONIZATION -->",
                    "<!-- END GENERATED IONIZATION -->",
                )
            )
            pkw = (
                "Default pKw: {/* SIMPO_PKW */}14{/* /SIMPO_PKW */}\n"
                if path.suffix == ".mdx"
                else ""
            )
            path.write_text(
                f"Handwritten before\n{pkw}{begin}\nold\n{end}\nHandwritten after\n"
            )

    def write_data(self):
        (self.root / gen.SOURCE).write_text(json.dumps(self.data))

    def generate(self, check=False):
        with redirect_stdout(io.StringIO()):
            return gen.generate(self.root, skills_root=self.installed, check=check)

    def test_primary_values_and_all_species(self):
        gen.validate(self.data)
        self.assertEqual(len(self.data["ions"]), 24)
        rows = {r["id"]: r for r in self.data["ions"]}
        self.assertEqual(rows["nitrite"]["pK"], [3.15, None, None])
        self.assertEqual(rows["sulfide"]["pK"], [7.02, 13.9, None])
        self.assertEqual(rows["oxalate"]["pK"], [1.25, 4.72, None])
        self.assertEqual(rows["ammonium"]["pK"], [4.76, None, None])
        self.assertEqual(self.data["pKw"], 14)

    def test_unified_source_updates_without_touching_generated_copies(self):
        source = self.root.parent / "SimpoSkills"
        reference = source / "skills/simpo-create-biomodel/references/ionization-derivation.md"
        reference.parent.mkdir(parents=True)
        reference.write_bytes(self.targets[2].read_bytes())
        (reference.parent.parent / "skill.json").write_text("{}")
        old_copies = {p: p.read_bytes() for p in self.targets[2:]}
        with redirect_stdout(io.StringIO()):
            self.assertTrue(gen.generate(self.root))
            self.assertFalse(gen.generate(self.root, check=True))
        self.assertIn("SIMPO built-in parameter set", reference.read_text())
        self.assertEqual(old_copies, {p: p.read_bytes() for p in self.targets[2:]})
        with self.assertRaisesRegex(ValueError, "direct edits"):
            gen.generate(self.root, backend_root=self.backend)

    def test_generated_checkout_requires_source_before_any_writes(self):
        marker = self.root / "plugins/simpo/generated.json"
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("{}")
        before = self.targets[0].read_bytes()
        with self.assertRaisesRegex(ValueError, "private SimpoSkills"):
            gen.generate(self.root)
        self.assertEqual(before, self.targets[0].read_bytes())

    def test_check_is_read_only_and_generation_is_idempotent(self):
        before = {p: p.read_bytes() for p in self.targets}
        self.assertTrue(self.generate(check=True))
        self.assertEqual(before, {p: p.read_bytes() for p in self.targets})
        self.assertTrue(self.generate())
        self.assertFalse(self.generate(check=True))
        after = {p: p.read_bytes() for p in self.targets}
        self.assertFalse(self.generate())
        self.assertEqual(after, {p: p.read_bytes() for p in self.targets})
        for path in self.targets:
            text = path.read_text()
            self.assertTrue(text.startswith("Handwritten before\n"))
            self.assertTrue(text.endswith("Handwritten after\n"))
        self.assertEqual(self.targets[2].read_text(), self.targets[3].read_text())
        self.assertEqual(self.targets[2].read_text(), self.targets[4].read_text())

    def test_one_source_change_updates_every_copy_and_detects_local_drift(self):
        self.generate()
        self.data["ions"][1]["pK"][0] = 3.123456  # synthetic update, never real data
        self.data["pKw"] = 14.123456
        self.data["version"] += 1
        self.write_data()
        self.assertTrue(self.generate(check=True))
        self.generate()
        for path in self.targets:
            self.assertIn("3.123456", path.read_text())
            self.assertIn("14.123456", path.read_text())
        altered = self.targets[3]
        altered.write_text(altered.read_text().replace("3.123456", "9.87654"))
        self.assertTrue(self.generate(check=True))
        self.generate()
        self.assertNotIn("9.87654", altered.read_text())

    def test_factors_are_parser_ready_in_skills_and_keep_website_notation(self):
        reference = gen.table(self.data)
        english = gen.table(self.data, "en")
        self.assertIn("1/10800", reference)
        self.assertIn("1/35500", reference)
        self.assertNotIn("1/(", reference)
        self.assertIn("1/(10.8*1000)", english)
        self.assertIn("1/(35.5*1000)", english)
        self.assertNotIn("9.24(9.23)", english)

    def test_invalid_source_or_missing_target_does_not_partially_write(self):
        for update in (
            {"pK": ["3.15(3.35)", None, None]},
            {"factor_denominator": 0},
            {"ionization": "Complete"},
            {"name": {"en": "bad|name", "zh": "坏"}},
        ):
            data = copy.deepcopy(self.data)
            data["ions"][1].update(update)
            with self.assertRaises(ValueError):
                gen.validate(data)
        before = self.targets[0].read_bytes()
        self.targets[-1].unlink()
        with self.assertRaises(FileNotFoundError):
            self.generate()
        self.assertEqual(before, self.targets[0].read_bytes())


if __name__ == "__main__":
    unittest.main()
