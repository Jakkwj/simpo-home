[English](https://github.com/Jakkwj/simpo-home) |[简体中文](https://github.com/Jakkwj/simpo-home/blob/master/README-zh.md)

# <p align="center">SIMPO WATER Home Page</p>

<div align="center">

![Static Badge](https://img.shields.io/badge/SimpoClient-v1.0.1-blue)

</div>

- This is the home page of [SIMPO WATER](https://www.simpowater.org/), which is built with [Docusaurus](https://docusaurus.io/).
- Installation: `yarn`.
- Local Development: `yarn start`.

## SIMPO Skill development

The public user documentation describes installation and usage only. The
Marketplace manifests and Skill source are maintained in this repository:

```text
SimpoHome/
├── .claude-plugin/marketplace.json
└── plugins/simpo/
    ├── .claude-plugin/plugin.json
    └── skills/
        ├── simpo/
        │   ├── SKILL.md
        │   ├── agents/openai.yaml
        │   └── references/
        ├── simpo-create-biomodel/
            ├── SKILL.md
            ├── agents/openai.yaml
            └── references/
        └── simpo-create-project/
            ├── SKILL.md
            ├── agents/openai.yaml
            ├── references/
            └── scripts/
```

- `.claude-plugin/plugin.json` and the root `.claude-plugin/marketplace.json`
  publish all Skills as the `simpo` plugin for Claude Code.
- Codex installs each Skill directory directly under `$CODEX_HOME/skills`.
- Each directory under `plugins/simpo/skills/` is a complete portable Skill;
  keep its `references/` directory with `SKILL.md` when installing it.
- Leading-dot directories are hidden by many file browsers but must remain
  tracked by Git.

After changing the Claude Code Plugin, validate its manifest and Marketplace,
then reinstall or update the Plugin. After changing a Codex Skill, reinstall the
Skill and test it in a new Codex session. The Docusaurus user pages live under
`src/docs/Tutorials/SimpoCLI/`; Chinese translations live under
`src/i18n/zh/docusaurus-plugin-content-docs/current/Tutorials/SimpoCLI/`.
The SimpoCLI Skill provides the on-demand `$simpo` workflow in Codex and
`/simpo:simpo` in Claude Code; it keeps the CLI manual out of unrelated
conversations and reads only the relevant command reference when invoked.

### DataSet Skill synchronization with SimpoAI

The CLI Skill at `plugins/simpo/skills/simpo-create-dataset/` is the shared rule
source. The AI port retains the complete workflow, all four references and both
optional helpers; its `adapter.md` maps execution to browser tools and review.
From this repository root, run `python3 plugins/simpo/tools/sync_dataset_skill.py`
and then the same command with `--check`. The sibling backend is selected by
default; use `--backend-root /path/to/SimpoBackend/backend/litestar` otherwise.
The read-only check fails on missing or changed generated files.

## Shared Ionization parameters

The data, generator, tests, and [maintenance guide](data/ionization/README.md)
are kept together in `data/ionization/`.

Maintain the website/Skill constants only in `data/ionization/ionization.json`. The table
uses the primary values outside parentheses; preserve explicit workbook/user
overrides. From this repository root:

```bash
python3 data/ionization/generate_ionization.py
python3 data/ionization/generate_ionization.py --check
python3 -m unittest discover -s data/ionization -p 'test_generate_ionization.py'
```

Generation updates the marked tables in both BioModel Edit translations and
the portable CLI Skill reference. It also updates the SimpoAI reference when a
sibling `SimpoBackend/backend/litestar` checkout is present. For another checkout,
pass `--backend-root /path/to/SimpoBackend/backend/litestar`. To refresh parameter
blocks in an installed Skill with these generation markers, also pass
`--skills-root /path/to/skills`; use the normal Skill update for instruction changes.
Generated copies remain self-contained and do not fetch the website at runtime.
Increment the data version when changing reference values; the generated content
also includes a source hash. Review and commit all affected repositories together.
Website `npm run build` and CI check for stale local copies; standalone deployments
do not need the other repository. `npm run references:generate` and
`npm run references:check` expose the same commands from `src/`.

## Resource

- Join us in building and enhancing [Paper Resource](https://www.simpowater.org/resource) with the help of powerful **AI tools** (such as: **Geimini**). Your contributions can significantly enhance and expand the collection, making it more valuable for the entire community.
- We appreciate your support and collaboration, fork and pull request are welcome.

### 1. Fork

- Fork this repository: [simpo-home](https://github.com/Jakkwj/simpo-home).

### 2. Find the folder

- Make the paper content you want to submit in the `src/resource` folder.
- For now, the structure of the folder is as follows:
  - 1st level: the issue year.
  - 2nd level: the name of the journal/conference written in `mdx` syntax.

### 3. Ask AI

- The following questions will be asked to **AI** to understand each paper:
  - What problem does this paper attempt to solve?
  - What are the relevant studies?
  - How the paper solves this problem?
  - What experiments were done for the paper?
  - What are the points that can be explored further?
  - Summarize the main points of the paper.
  <!-- - These are just a few basic FAQs for understanding a paper with Kimi. if you would like to discuss the paper further with it, click [here](https://kimi.moonshot.cn/) to jump to the Kimi web version and start a new session related to the paper. -->

### 4. Pull

- Make a pull request to this repository: [simpo-home](https://github.com/Jakkwj/simpo-home).
