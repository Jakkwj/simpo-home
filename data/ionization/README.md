# Ionization 共用参数与生成工具

中英文网页、SimpoCLI Skill 和 SimpoAI Skill 的电离参考参数统一维护在本目录的
[ionization.json](ionization.json) 中。修改这一份数据，再运行生成脚本更新文档与 SimpoSkills 共用参考，随后构建并导出两端产物。
生成文件随各端发布，运行时无需联网读取网页。

## 文件说明

```text
data/ionization/
├── ionization.json               # 唯一参数数据源
├── generate_ionization.py        # 生成与一致性检查
├── test_generate_ionization.py   # 生成器回归测试
└── README.md                     # 本说明
```

脚本只使用 Python 3 标准库，无需安装额外依赖。路径根据脚本在 SimpoHome 中的位置定位，
与执行命令时的工作目录无关；请保留本目录在仓库中的相对位置。

## 常用命令

在本目录执行：

```bash
python3 generate_ionization.py
python3 generate_ionization.py --check
python3 -m unittest discover -s . -p 'test_generate_ionization.py'
```

在 **SimpoHome 仓库根目录**执行同样的操作：

```bash
python3 data/ionization/generate_ionization.py
python3 data/ionization/generate_ionization.py --check
python3 -m unittest discover -s data/ionization -p 'test_generate_ionization.py'
```

在网站 `src/` 目录也可使用：

```bash
npm run references:generate
npm run references:check
npm run references:test
```

生成命令写入需要更新的文件；重复执行不会产生额外变化。`--check` 只检查，不写入文件：

| 退出码 | 含义 | 处理方式 |
| --- | --- | --- |
| `0` | 检查通过，或生成成功 | 继续构建、审阅和发布 |
| `1` | `--check` 发现生成内容过期 | 运行不带 `--check` 的生成命令 |
| `2` | 数据无效、文件缺失或生成标记异常 | 根据错误定位并修正后重试 |

## 会更新哪些文件

下表路径相对于对应仓库根目录：

| 使用方 | 生成目标 | 如何使用 |
| --- | --- | --- |
| 英文网页 | `SimpoHome/src/docs/Tutorials/BioModel/Edit.mdx` | 构建网站时渲染英文表格 |
| 中文网页 | `SimpoHome/src/i18n/zh/docusaurus-plugin-content-docs/current/Tutorials/BioModel/Edit.mdx` | 构建网站时渲染中文表格 |
| Skill 共用源 | `SimpoSkills/skills/simpo-create-biomodel/references/ionization-derivation.md` | 两端构建时复用，导出后运行时读取本地副本 |

网页使用各自语言的名称，Skill 参考表包含中英文名称。网页保留 `1/(14*1000)` 形式的
Factor 展示，Skill 使用可直接解析的 `1/14000`；两者由同一分母生成。网页中的默认 pKw
也由数据源更新。

脚本只替换 `BEGIN GENERATED IONIZATION` 与 `END GENERATED IONIZATION` 之间的内容，
以及网页中 `SIMPO_PKW` 标记包围的值。保留标记本身和区域外的手写说明。每个生成区域
携带数据版本及 SHA-256 摘要，便于检查来源。

### 统一 Skill 源与后续导出

默认寻找同级私有 `SimpoSkills` 仓库；也可用 `--source-root /path/to/SimpoSkills`
明确指定。生成器只更新网站文档及共用源，不直接改写两端生成产物。
然后在 SimpoSkills 根目录执行：

```bash
python3 tools/build.py
python3 tools/check.py --dist
python3 tools/export.py
```

也可在 SimpoSkills 运行 `python3 tools/update_ionization.py`，仅更新共用参考。
已安装用户副本通过正常发布和 `simpo skills update` 更新。

旧版尚未迁移的仓库仍支持 `--backend-root`、`--skills-root`。使用统一源后不再
允许这些选项直接修改下游副本；已存在公开生成清单却找不到源仓库时会明确报错。
所有生成目标先完整读取和验证，再开始写入。

## 数据维护规则

当前数据包含 24 类参考物种。只在 [ionization.json](ionization.json) 中维护参数，
不要分别编辑网页和 Skill 的生成表格。

| 字段 | 约定 |
| --- | --- |
| `version` | 正整数；参考参数发生变化时递增 |
| `source_url` | 原始文档的 HTTPS 地址，用于来源说明；生成时不访问该网址 |
| `pKw` | 有限数值，当前为 `14` |
| `ions[].id` | 唯一标识，小写字母开头，后续可含小写字母、数字和下划线 |
| `ions[].name.en` / `name.zh` | 中英文名称 |
| `ions[].compound` | `Strong Acid`、`Weak Acid`、`Strong Base` 或 `Weak Base` |
| `ions[].step` | `Mono`、`Di` 或 `Tri` |
| `ions[].ionization` | 强酸／强碱使用 `Complete`；单步弱酸／弱碱使用 `One Step`；多步使用 `Stepwise` |
| `ions[].factor_denominator` | 正整数，Factor 为 `1 / factor_denominator`，单位为 mol/mg |
| `ions[].pK` | 固定三个位置，依次对应 pK1、pK2、pK3；未使用的位置写 `null` |

采用原表**括号外**的数值，不将括号内备选值写成字符串或取平均值。强酸／强碱的三个
pK 均为 `null`；弱酸／弱碱按 Mono、Di、Tri 分别提供一、二、三个数值。

这些数据是 SIMPO 的内置参考默认值。生成工具不改变模型的固定格式，不覆盖用户或
工作簿明确提供的参数，也不会直接修改已保存的 BioModel。物种匹配、浓度基准及适用性
仍由对应 Skill 的推导规则处理。

## 修改后的检查与发布

1. 修改 `ionization.json`；参数变化时递增 `version`。
2. 运行生成命令。需要 SimpoAI 时，确认同级后端存在或使用 `--backend-root`。
3. 运行 `--check` 和生成器测试，审阅所有受影响仓库中的差异。
4. 提交各端生成文件，按各自流程构建和发布网站、更新 CLI Skill、部署 SimpoAI 后端。

网站 `npm run build` 的 `prebuild` 和 `.github/workflows/ionization-reference.yml`
会执行一致性检查；它们不会代替生成命令修复过期文件。只检出 SimpoHome 的 CI 默认
检查该仓库内的三个目标；要同时检查后端，需要检出后端并指定路径，或使用同级目录结构。

修改 JSON 不会自动更新在线网站或正在部署的 Skill。本地生成、检查与线上发布是独立步骤。
