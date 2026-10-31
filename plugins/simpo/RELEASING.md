# CLI and Skills releases

CLI releases use `X.Y.Z`. All four Skills share one bundle version:
`X.Y.Z-skills.N`, where `X.Y.Z` is the CLI release baseline and `N` starts at 1.
A Skills-only change increments `N`; it does not require a new CLI installer.
The independent `cli_min_version` field describes compatibility. Compare the
numeric CLI tuple and numeric revision, not generic SemVer prerelease ordering.

The updater uses the public catalog at
`https://raw.githubusercontent.com/Jakkwj/simpo-home/master/plugins/simpo/releases/index.json`.
Skills ZIPs live beside that catalog. CLI installers keep the existing Gitee
`package` release URLs used by the website. All artifacts include SHA-256 and
size; downloads require HTTPS. The CLI does not query an update service during
ordinary commands and never sends an API Token to release hosts.

## Skills version source of truth

For a Skills release, **manually edit only the version in
`plugins/simpo/release.json`**. The other three version-bearing JSON files are
updated by `python3 plugins/simpo/tools/build_release.py`:

| File | Version maintenance |
| --- | --- |
| `plugins/simpo/release.json` | Maintainer sets the shared Skills `version`; change `cli_min_version` only when the minimum CLI compatibility requirement changes. |
| `.claude-plugin/marketplace.json` | Builder synchronizes the `simpo` plugin version. |
| `plugins/simpo/.claude-plugin/plugin.json` | Builder synchronizes the plugin version. |
| `plugins/simpo/releases/index.json` | Builder adds the Skills version, compatibility requirement, download URL, size and SHA-256. |

For example, after changing Skills based on CLI `0.1.8`, advance the revision
from `0.1.8-skills.1` to `0.1.8-skills.2`. If compatibility is unchanged, keep
`cli_min_version` as it is:

```json
{
  "version": "0.1.8-skills.2",
  "cli_min_version": "0.1.8"
}
```

Run the builder from the SimpoHome root after finishing the source changes.
It generates `plugins/simpo/releases/SIMPOSkills_0.1.8-skills.2.zip` and updates
the three derived JSON files. Commit the modified Skills source, all four JSON
files and the new ZIP together, then push to `master`. Keep previous release
ZIPs and catalog entries. A Skills-only release needs no CLI rebuild or
`--cli-version` argument; announcing CLI installers follows the separate
Publish CLI procedure below.

## Publish Skills

1. Edit `plugins/simpo/release.json`: increment the Skills revision, or start at
   revision 1 for a new CLI baseline. Adjust `cli_min_version` only if required.
2. Complete Skill, reference and helper-script changes before building.
3. Run from the SimpoHome repository root:

   ```bash
   python3 plugins/simpo/tools/build_release.py
   python3 -m unittest discover -s plugins/simpo/tools -p 'test_build_release.py'
   ```

4. Review and commit `release.json`, the Skills source, generated `releases/`,
   `.claude-plugin/marketplace.json`, and `plugins/simpo/.claude-plugin/plugin.json`.
   Push to `master` to make the catalog and ZIP accessible to clients. Publish
   source, ZIP and catalog in the same commit.

The builder synchronizes the Claude Marketplace plugin version with the bundle
version. Existing release ZIPs/metadata are immutable; changed bytes require a
new revision. Caches, `.pyc` files and local installation metadata are excluded.

## Publish CLI

1. Update `SimpoClient/client/source/cli/config.py`, both CLI builder configs,
   and the Inno Setup fallback version. Build/test the production installers
   using `SimpoClient/client/builder/cli/README.md`. New private modules must be
   included in **both** builders' `CLI_PACKAGE_MODULES` lists.
2. Upload validated production `.deb` / `.exe` files to the existing Gitee
   `Jakkwj/simpo-home` release named `package`. Verify the public download URLs
   against the local files. Never announce an installer before uploading it.
3. Explicitly announce the uploaded version (the script reads local artifacts):

   ```bash
   python3 plugins/simpo/tools/build_release.py --cli-version 0.1.8
   ```

   Default installer directory: `resource/cli`. Override with `--cli-directory`.
   Only available platforms for the selected version are added. A later run can
   add the second platform without changing the first one's checksum. CLI
   builds alone do not alter the catalog. Development installers are excluded.
4. Update website download links when ready; commit and push the generated
   catalog after upload. A platform keeps its last published version until its
   own newer artifact is announced.

## Client behavior

```bash
simpo update --check
simpo update
simpo skills list --target codex
simpo skills install --target codex
simpo skills update --target codex --check
simpo skills update --target codex
simpo skills install --target claude
```

CLI update supports Debian/Ubuntu amd64 and Windows x64. Linux runs `dpkg`
through `sudo` when needed and verifies the installed version. Windows returns
`scheduled`, then a detached system PowerShell waits for the CLI/Python launcher
to exit, starts Inno Setup with UAC elevation, and verifies the new CLI. Check
the returned `status_file` (`installed` / `failed`) and `installer_log`; scheduling
is not a successful-install claim. Windows PowerShell is required. No automatic
restart or forced termination of other applications is requested.

Skills install/update requires an explicit target. Codex respects `CODEX_HOME`;
Claude respects `CLAUDE_CONFIG_DIR`. Defaults are `~/.codex/skills` and
`~/.claude/skills`. `claude-code` is accepted as an alias for `claude`. Installing
Project adds its three dependencies. With no names, install selects all four;
update selects installed Skills and their Project dependencies. `--version`
selects a published version; downgrades are refused. If the latest Skills
require a newer CLI, upgrade the CLI or select a compatible Skills version.

Existing manual/Skill Installer installations are unmanaged. To migrate, use
`simpo skills install --target codex --force` (or `claude`); the returned backup
directory retains the original files. Updates reject modified files unless
`--force` is supplied. Files are staged/validated first; all replacements roll
back on an ordinary installation failure. Replaced unmodified files are removed,
including scripts deleted in the new bundle. Per-target directory locks prevent
concurrent Skills updates; a hard-killed process may leave a lock requiring
manual removal and a backup directory to recover. Start a new assistant session
after changing Skills.

Claude Marketplace installations remain managed through Claude's `/plugin`
manager. The CLI reports a registered `simpo@…` plugin and refuses local
installation alongside it; uninstall the plugin first to switch to local
Skills. Local Skills use `/simpo` and `/simpo-create-project`, while the plugin
uses `/simpo:simpo` and `/simpo:simpo-create-project`.
