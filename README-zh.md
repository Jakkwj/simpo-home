[English](https://github.com/Jakkwj/simpo-home) |[简体中文](https://github.com/Jakkwj/simpo-home/blob/master/README-zh.md)

# <p align="center">SIMPO WATER Home Page</p>

<div align="center">

![Static Badge](https://img.shields.io/badge/SimpoClient-v1.0.1-blue)

</div>

- 这是 [SIMPO WATER](https://www.simpowater.com/) 的主页，本主页使用 [Docusaurus](https://docusaurus.io/) 构建。
- 安装：`yarn`。
- 本地开发：`yarn start`。

## SIMPO Skill 开发

公开用户文档只说明安装和使用方法。Marketplace 清单与 Skill 源码维护在本仓库：

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

- `.claude-plugin/plugin.json` 和根目录的 `.claude-plugin/marketplace.json` 用于向
  Claude Code 以 `simpo` 插件发布全部 Skill。
- Codex 将每个 Skill 目录直接安装到 `$CODEX_HOME/skills`。
- `plugins/simpo/skills/` 下的每个目录都是完整、可移植的 Skill；安装时必须让
  `references/` 与 `SKILL.md` 保持在同一个 Skill 目录中。
- 以点号开头的目录在很多文件管理器中默认隐藏，但必须由 Git 跟踪。

修改 Claude Code Plugin 后，应校验插件清单和 Marketplace，再重新安装或更新插件；
修改 Codex Skill 后，应重新安装 Skill，并在新的 Codex 会话中测试。Docusaurus 英文用户文档位于
`src/docs/Tutorials/SimpoCLI/`，中文翻译位于
`src/i18n/zh/docusaurus-plugin-content-docs/current/Tutorials/SimpoCLI/`。
SimpoCLI Skill 提供按需加载的 `$simpo`（Codex）和
`/simpo:simpo`（Claude Code）工作流；调用时只读取相关命令参考，不会把完整
CLI 说明书带入无关对话。

## Resource

- 加入我们，使用强大的**AI 工具**（如：**Geimini**）来构建和增强[论文资源](https://www.simpowater.com/resource)。您的贡献可以显著提升和扩展资源库，使其对整个社区更有价值。
- 感谢您的支持与合作，欢迎 fork 和 pull。
- 目前，对于每篇论文，我们将通过 **AI** 提出以下问题：
  - 本论文试图解决什么问题？
  - 相关的研究有哪些？
  - 本论文是如何解决这个问题的？
  - 本论文进行了哪些实验？
  - 哪些方面还可以进一步探索？
  - 概括论文的主要观点。

### 1. Fork

- Fork 这个仓库：[simpo-home](https://github.com/Jakkwj/simpo-home)。

### 2. 找到文件夹

- 将您想要提交的论文内容写入`src/resource`文件夹中。
- 目前，该文件夹的结构如下：
  - 第一级：发行年份。
  - 第二级：使用 mdx 语法编写的期刊/会议名称。

### 3. 询问 AI

- 为了更好地理解每篇论文，我们将通过 **AI** 回答以下问题：
  - 这篇论文试图解决什么问题？
  - 有哪些相关研究？
  - 论文如何解决这个问题？
  - 论文做了哪些实验？
  - 有什么可以进一步探索的点？
  - 总结论文的主要内容。

### 4. Pull

- 将结果 Pull 到 [simpo-home](https://github.com/Jakkwj/simpo-home)。
