# Luo Meta Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**用于设计、重构和评估可复用 Agent Skill 的 Agent Skill。**

[English](README.md) | [简体中文](README.zh-CN.md)

> 本译文对应英文版 `README.md`，最后同步：2026-10-19。

> [!IMPORTANT]
> 早期公开版本（`0.1.0`）。文本、结构和引用检查已完成；尚未跨所有 harness（agent 运行时）评估运行时行为。详见下文「状态」。

## 为什么需要它

多数弱 skill 的问题不是正文写得太少，而是：范围过宽；`description` 写成流程摘要，而不是触发边界；正文加载得太晚；或者从未用真实请求测试过。

Luo Meta Skill 是一套处理这些决策的方法。它帮助 agent 判断是否值得做成 skill、研究领域、设计运行时结构、写精确指令，并验证结果，而不是把项目变成一堆文档。

## 它做什么

- **先判断是否值得做成 skill。** 区分可复用 skill、一次性任务、仓库约定和可确定性检查。
- **先研究再写。** 用两个锚点：代表性任务与能力缺口，加上系统的领域知识。
- **设计运行时结构。** 覆盖范围、引用路由、脚本与素材、harness 兼容性和主路径。
- **写精确指令。** 先定语义，再按行为脆弱性选择约束强度；把 `description` 当作路由契约。
- **按风险验证。** 使用触发用例、真实产物、前后对比，并如实报告未测试的内容。

## 快速开始

### 环境要求

**harness** 指发现、加载并运行 skill 的 agent 运行时，例如 Claude Code、Codex CLI、DeepSeek Harness。

- 支持 Agent Skills 的 harness，能加载 `SKILL.md` 并读取相对路径的 Markdown 引用。
- 不需要运行时依赖、包管理器或 API Key。本 skill 没有脚本。

### 安装

克隆仓库：

~~~bash
git clone https://github.com/FengZhiHen1/luo-meta-skill.git
~~~

把目录放到 harness 用来发现 skill 的位置，目录名保持 `luo-meta-skill`。具体路径取决于 harness。本 skill 只使用 `SKILL.md` 和 Markdown 引用。

### 验证

在一个新的 agent 会话中提问：

> 为「审查 Terraform 变更」创建一个 skill，包含触发边界、引用路由和验证方案。

配置正确时，agent 会加载 `luo-meta-skill`，判断任务类型，并产出带清晰 description 和验证方案的 `SKILL.md`。如果 harness 会列出可用 skill，确认其中出现 `luo-meta-skill`。

如果 skill 没有加载，检查 harness 是否读取了 `SKILL.md` 中的 `description`，以及目录是否在 harness 的 skill 发现路径中。

## 示例：一个能正确路由的 description

`description` 是多数 harness 在决定是否加载 skill 前会读的文本。如果它写成流程摘要，agent 可能照着摘要执行，跳过正文。

弱：

> 用于代码审查——先跑 lint，再做安全扫描，最后写报告。

好：

> 审查代码变更的正确性、安全性和测试缺口。在准备合并请求或审查变更时使用。不用于编写新功能或修复构建失败。

好版本说明任务和边界，不描述执行顺序。完整规则见 [SKILL.md](SKILL.md) 和 [references/instruction-craft.md](references/instruction-craft.md)。

## 仓库内容

~~~text
luo-meta-skill/
├── SKILL.md
├── references/
│   ├── research-and-synthesis.md
│   ├── skill-architecture.md
│   ├── instruction-craft.md
│   └── iteration-and-evaluation.md
├── docs/
│   └── skill-design.md
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
└── LICENSE
~~~

运行时使用 `SKILL.md` 和 `references/`；`docs/` 记录设计意图与来源取舍；其余是仓库配置。

## 设计原则

- **description 是路由契约。** harness 在加载正文前读取 name 和 description；触发条件应放在这里。
- **能力优先于文档数量。** skill 应改变 agent 的判断或行动，而不是增加文件。
- **只在有消费方时加 schema。** 产出的 skill 如果有结构化产物，只保留一份权威 schema（例如 `schemas/`），且仅当代码、测试或校验器消费它时才加；代码和测试从 schema 派生。
- **形态只是起点。** 流程、知识、工具、判断和创作是组织形态；按任务调整。
- **用两个锚点研究。** 代表性任务与能力缺口，加上系统的领域知识。
- **验证强度与风险匹配。** 措辞做文本检查，行为看真实产物，路由用触发用例。
- **默认不绑定 harness。** 除非目标 harness 验证过，否则不使用 provider-specific 机制。
- **运行时英文，目标 skill 可用任意语言。** 本 skill 的指令是英文；目标 skill 跟随它的受众。

## 兼容性

Luo Meta Skill 面向实现了 [Agent Skills 规范](https://agentskills.io/specification) 的 harness：带 YAML frontmatter 的 `SKILL.md`、通过 `references/` 渐进披露、使用相对路径。

它不使用脚本、hooks、subagents、provider-specific frontmatter 或网络访问。实际行为取决于 harness 的 skill 加载器和模型；尚未跨所有 harness 评估运行时行为。

## 状态

- `0.1.0`，早期公开版本。
- 文本、结构和引用检查已完成。
- 尚未跨 harness 评估运行时行为。
- 不包含 CLI、评测平台或治理系统。
- 运行时指令为英文；目标 skill 可以使用任意语言。

## 安全

安全问题不要通过公开 Issue 报告，请按 [SECURITY.md](SECURITY.md) 处理。

## 贡献

欢迎用英文或中文提交 Issue 和 PR。较大的改动先读 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果贡献主要由 AI 生成，请在 PR 描述中声明。不要声称没有运行过的测试。

## 致谢

本方法综合了 Agent Skills 规范，以及 Sentry、OpenAI、Anthropic、Superpowers、Skillet、Yao Meta Skill 的公开 skill-authoring 方法。[docs/skill-design.md](docs/skill-design.md#source-trade-offs) 记录了采用与未采用的部分。

## 许可证

[MIT](LICENSE) © 2026 FengZhiHen1
