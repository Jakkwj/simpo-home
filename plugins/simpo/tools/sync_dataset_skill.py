#!/usr/bin/env python3
"""Mirror complete CLI creation workflows/resources into the SimpoAI port.

Only adapter.md is maintained in the backend. Scientific rules stay in the CLI
Skill; --check detects omissions and source drift without rewriting files.
"""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
NAME = "simpo-create-dataset"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sync(backend, *, check=False, name=NAME):
    begin = f"<!-- BEGIN CLI {name.removeprefix('simpo-create-').upper()} WORKFLOW -->"
    end = begin.replace("BEGIN", "END")
    source = ROOT / "plugins/simpo/skills" / name
    target = backend / "app/services/ai/skills" / name
    files = sorted(path for path in source.rglob("*") if path.is_file()
                   and "__pycache__" not in path.parts and path.suffix != ".pyc")
    originals = {
        path.relative_to(source).as_posix(): path.read_bytes() for path in files
    }
    workflow = originals["SKILL.md"].decode().split("---", 2)[2].strip()
    adapter = (target / "adapter.md").read_text(encoding="utf-8").strip()
    expected = {name: data for name, data in originals.items() if name != "SKILL.md"}
    expected["SKILL.md"] = (
        originals["SKILL.md"].decode().split("---", 2)[0] + "---" + originals["SKILL.md"].decode().split("---", 2)[1] + "---\n\n"
        + adapter + "\n\n" + begin + "\n" + workflow + "\n" + end + "\n"
    ).encode()
    expected["source.json"] = (
        json.dumps(
            {
                "source": "SimpoHome/plugins/simpo/skills/" + name,
                "files": {name: sha(data) for name, data in originals.items()},
                "workflow_sha256": sha(workflow.encode()),
                "adapter_sha256": sha(adapter.encode()),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    ).encode()
    changes = [
        name
        for name, data in expected.items()
        if not (target / name).is_file() or (target / name).read_bytes() != data
    ]
    previous = target / "source.json"
    stale = set(json.loads(previous.read_text()).get("files", {})) - set(originals) if previous.is_file() else set()
    for name in stale:
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError("Invalid generated resource path")
        print(("Stale: " if check else "Removed generated resource: ") + str(target / name))
        if not check:
            (target / name).unlink(missing_ok=True)
    for name in changes:
        path = target / name
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected[name])
        print(("Out of date: " if check else "Updated: ") + str(path))
    if not changes and not stale:
        print(
            f"{name} is current: complete CLI workflow and {len(files) - 1} resources."
        )
    return bool(changes or stale)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--backend-root",
        type=Path,
        default=ROOT.parent / "SimpoBackend/backend/litestar",
    )
    parser.add_argument("--check", action="store_true")
    supported = ["simpo-create-biomodel", "simpo-create-dataset", "simpo-create-project"]
    parser.add_argument("--skill", choices=[*supported, "all"], default="all")
    args = parser.parse_args()
    try:
        names = supported if args.skill == "all" else [args.skill]
        changed = any([sync(args.backend_root, check=args.check, name=name) for name in names])
    except (OSError, ValueError, IndexError) as error:
        parser.exit(2, f"Creation Skill sync failed: {error}\n")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
