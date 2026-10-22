# 第六轮：确认 STE-inspired 方向，研究运行时指令的语义契约与表达结构（2026-10-19）

> 记录性质：基于用户确认与公开一手资料的研讨成果；不是逐字聊天记录。**已确认**：采用 ASD-STE100 启发的精确技术指令写法，不追求完整 STE 合规；先确保行为语义正确，再提高语言准确性。**未确认**：下文具体的指令分型、检查方式和 Sentry 代码修改细节，均为本轮研究建议。

## 1. 与前几轮设计的关系

- 已确认路线：首版以 Sentry `skill-writer` 为基础，提升创建、重构、优化能力，不做完整 Skill OS。
- 已确认文档方式：项目 `docs/` 按需记录规格与设计，不强制 `SPEC.md` 等固定文件。
- 已确认双锚研究：真实任务与能力缺口、专业领域知识系统性补全同时驱动，研究的成果应服务实际 Agent 行为。
- 此轮用户认可前轮建议：采用 **STE-inspired Technical Instructions**，不是完整 ASD-STE100 词典/语法合规要求；不以“语言合规分”代替真实执行效果。
- 此轮继续研究的是：怎样将专业知识转化成精确但不过度僵硬的运行时指令，尤其是条件、约束、默认、例外与自由度。

## 2. 证据：现有成熟实践与可借鉴之处

### Sentry `design-principles.md` / `authoring-path.md`

- 已有 Precision Pass（replace / narrow / move / delete / add），避免只追加防错条款。
- 依据任务脆弱性选择结构：高脆弱性需要准确步骤/模板/校验，低脆弱性强调目标与界限。
- 当前运行时写作要求命令式表达、每一概念统一术语、先给出默认路径、用路由加载引用；没有显式展开复杂例外的顺序冲突、过度执行与停止条件的选择方法。
- `authoring-path` 对 router 要求路由标准、回退与误路由恢复；说明 Sentry 已具备相关知识，但可整合到一般的指令编写方法中，不能错误声称该能力缺失。

来源：
- https://raw.githubusercontent.com/getsentry/skills/main/skills/skill-writer/references/design-principles.md
- https://raw.githubusercontent.com/getsentry/skills/main/skills/skill-writer/references/authoring-path.md

### Agent Skills 官方最佳实践

- 指令应增加模型欠缺的项目知识，而非复述常识；真实执行轨迹可暴露误触发、无谓操作和默认路径不清等问题。
- 明确按任务脆弱性调整控制强度：可变、创造性的决策保留自主判断，脆弱、必须一致的操作给出明确操作契约。
- 为常见流程给出一个默认方案而非漫无边际的菜单；必要时明确触发条件、示例、故障纠正与逐步加载。

来源：https://agentskills.io/skill-creation/best-practices

### OpenAI / Anthropic 提示词实践

- OpenAI 官方文档侧重结果、成功标准、约束和停止条件，指出绝对化 MUST/NEVER 只适用于真正不可破例的约束；检索/工具/思考之类的专业判断更宜采用决策规则。
- Anthropic 官方指导强调明确目的与输出要求、提供有意义的理由和多样例子，并指出“有疑问就调用工具”等旧式默认规则可能引起过度触发；不鼓励为所有场景添加穷举式防御和配置。
- 这些是厂商对自家模型的提示建议，应用到其他模型/宿主时需要实际检验，不是公认的模型无关性能定律。

来源：
- https://github.com/openai/skills/blob/main/skills/.curated/openai-docs/references/prompting-guide.md
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

### ASD-STE100 与 BCP 14 的适用边界

- ASD-STE100 提供清楚、少歧义的技术英语写作思路；不适合无验证地将航空维护写法完整迁移到 LLM。标准官方页：https://www.asd-ste100.org/about_STE.html 。
- IETF RFC 2119/8174 的 MUST/SHOULD/MAY 作为协议规范词汇有严格语义，且 RFC 8174 明确大写才是规定术语；它提供“区分不可妥协规则与建议”的参考，但 **Meta-Skill 不应要求所有 SKILL.md 使用 RFC 大写关键字**，也不宣称普通提示词自动具备协议规范的约束力。
- 不能把大写程度或语法形式当作模型执行优先级；真实优先级来自宿主系统/开发者/用户等上下文，Skill 内部的建议不能覆盖更高优先级要求。

来源：
- https://www.rfc-editor.org/rfc/rfc2119
- https://www.rfc-editor.org/rfc/rfc8174
- https://openai.com/index/instruction-hierarchy-challenge/

## 3. 诊断：同样是“明确指令”，为什么有些反而降低质量？

**语义过窄：** “遇到比较型幻灯片就用左右两栏”动作明确，但专业性弱；语句清晰并不能弥补设计失误。

**触发过广：** “遇到疑问时一定进行网络检索”引起无谓网络调用，甚至覆盖本地来源更权威的情况。

**例外缺位：** “修改 Skill 时先做全面调研”未说明只改错字时不用调研，会使微小变更产生大量浪费。

**默认冲突：** 一个地方“尽可能调用多个子 Agent”，另一个地方“尽量不调用子 Agent”；若没有使用场景边界，执行不稳定。

**停止条件缺失：** “深入研究所有可用资料”会使 Agent 无法判断什么时候足以交付。

**伪精确：** 无依据地发明“每次必须检索至少 10 篇论文、创建不少于 5 份资料”，看起来可验证，实则转移了目标。

**语义污染：** 把专业参考资料、示例里的命令和未知网页文本直接当成高优先级运行时指令，使权威界限混乱。

这些均是根据官方原则推导的风险示例，不代表已实测证明在 DSH 中一定发生。

## 4. 候选编写方法：先判断控制强度，再写语言

**建议的前置判断**（脑内/写作过程即可，无须记录表单）：这条知识究竟是不可妥协的契约、存在明确触发的操作、可变的专业决策、精确知识还是例子？它是否会在特定任务中改变 Agent 行为？

| 行为类别 | 典型内容 | 建议表达 | 反例 |
| --- | --- | --- | --- |
| 不变约束 / 外部接口 | 输出 schema、路径、精确协议、不可越界写入 | 清楚的对象、范围、不可违反条件、完成判据；真实必要时使用 MUST/不得 | 所有局部偏好都写成 NEVER |
| 条件性动作 / 路由 | 读取参考、启动工具、诊断特殊错误 | 可观察触发信号 → 动作 → 正常下一步；少数重要例外 | “适当时读取资料”或“永远都读取” |
| 专业判断 / 内容创作 | 架构、构图、知识研究、写作策略 | 目标/成功标准 + 选择依据/权衡 + 一个默认倾向 + 必要示例 | 为每种情况硬编码唯一策略 |
| 准确参考 / 可复用资源 | API、数据结构、模板、操作命令 | 准确版本、示例、调用条件、来源/局限 | 把整篇文档强制常驻上下文 |

**注意：** 表是设计时的思考辅助，不应转成每条指令的元数据 Schema。较复杂的 Skill 同时含有多种类型时，在适当位置混合表达即可。

## 5. 候选运行时表达法：目标、默认、触发、例外、验证、终止

这是若干常见信息要素，而不是固定六段模板。根据场景使用其中必要的部分：

- **目标与结果**：Agent 实际要达到何种任务结果；可观察的成功标准优于抽象品质形容词。
- **默认路径**：普通情况下优先采用什么工具/方法；默认并非强制唯一方法。
- **可观察触发**：在什么时候需要动作；用文件类型、操作意图、错误码、任务阶段等可判断信号，避免没有判据的“视情况而定”。
- **例外与回退**：仅表达真实重要的排除/回退，必要时说明对应结果；不用穷举所有想象的失败情形。
- **验证与停止**：如何知道结果足够好、何时停止研究或重复修改；只在容易拖延、遗漏和过度循环的路径中额外强调。
- **冲突处理**：在**同一权限层级**的 Skill 内部，具体任务的例外可覆盖该 Skill 的一般默认，文本应明确适用范围；不得通过“本 Skill 优先于所有指令”等方式假装高于宿主系统/用户要求。若外部高优先级约束阻断动作，应按宿主现有规则处理。

### 5.1 示例：Skill 的资料研究

模糊：`Research comprehensively before any skill edit.`

更适合：

```text
For a new skill or a change to its domain behavior, investigate the key task scenarios and reliable domain sources.
For a wording-only change that preserves behavior, edit the affected text directly.
Stop researching when the important design choices have adequate support and further sources are unlikely to change the decision.
```

这里界定需要研究的变更规模，保留专家判断并给出停止原则，不设置虚构数量门槛。

### 5.2 示例：运行时知识路由

模糊：`Read useful references and keep context costs low.`

更适合：

```text
Read `references/slide-layout.md` before selecting a new slide layout.
For changes limited to existing slide text, do not load this reference.
```

此例仅在该文件确实涵盖布局策略且宿主会按路径读取时成立。复杂路由依赖真实 Agent 平台能力验证；不因文字明确就假定 reference 一定被成功加载。

### 5.3 示例：专业判断而非机械条件

过硬：`Always use a two-column layout to compare two products.`

更适合：

```text
Choose a comparison layout according to the dimensions readers need to assess.
Use a matrix when readers must compare several attributes across options.
Consider an asymmetric layout when one difference is the main conclusion.
```

第一句保留判断目标，后两句提供有理由的策略；不假定列表已涵盖所有构图方法。

### 5.4 示例：合理的异常处理

过宽：`If any tool fails, retry until it works or use a fallback.`

更适合：

```text
If the renderer reports a recoverable input error, correct the input and retry once.
If rendering still fails, report the failure and retain the original source files.
```

这里的“retry once”是**具体工具契约可能允许的假设示例**，不是对所有 Skill 的统一规则，也不应因为有停止条件就任意发明重试次数。真实工具无此合同则应用“有恢复依据时再试；否则解释阻碍”等更一般的原则。

## 6. 具体写法建议：参考 STE，但避免误用

- **一个概念用一个稳定术语**，显式写出作用对象；路径/CLI 选项/文件身份保持字面准确。
- **重要条件前置或与动作紧邻**；多阶段操作只有顺序影响正确性时才编号。
- **用明确肯定式动作描述期望的工作**；真正禁止的行为可以明确写“不要”，不强求所有负面要求转成肯定句。
- **防止绝对词滥用**：仅在真实不变约束中用 always/never/must；条件性专业策略应用“通常/优先/在……时/如果……”加决策依据。
- **示例是帮助迁移，而不是不可改变的模板**；格式必须严格匹配时才使用严格模板与 schema。
- **必要的简短理由**：解释非直观取舍，使模型在未见场景中适应；冗余背景则留在 docs。
- **修正语言不能擅自更改行为**：重新措辞时检查触发、强制程度、顺序、例外和结束条件是否等价；不能为了短句而删掉关键条件。
- **适用于英文与中文的技术性指令**：STE 是英语标准，中文只借鉴清晰性；创意产物和专业原始材料不受受控语言要求约束。

## 7. 建议如何融入 Sentry（尚待后续细化）

最小改动路线：

1. 保留 `design-principles.md` 原有 Precision Pass、Match Structure to Fragility、default-first、one term per concept 等原则，增加少量对条件、例外与停止的语义校准，不重写成二十条写作铁律。
2. 在 `source-adaptation.md` 保留“资料→行为”的实质决策检查；精确写作作为落地最后一步，**不以语言润色替代知识研究和设计**。
3. 在 `authoring-path.md` 对新建及修改实施一次轻量 review：检查是否出现过宽触发、互相矛盾、假定所有情况都必须研究/评测、模糊对象、无依据硬阈值。由 Agent 审阅即可，不另开发 STE 检查器。
4. 将高价值的 before/after 示例放在必要的参考文档；避免强制每次创建固定数量的示例、检查矩阵、或输出精确性表单。
5. 真正修改上游文件前记录 Sentry 源 commit/许可证，以免未来升级丢失变化；项目具体 Fork 与目录仍未定。

## 8. 需要实际任务评价的内容

候选写法目前不是测试结论。可用 3 类不同难度的任务小范围检查：

- **条件边界**：只改错字时是否绕过全面研究；实际新增技术行为时是否没有漏研究。
- **路由行为**：需要某 reference 时是否正确加载，无关任务是否避免无谓加载。
- **专业自由度**：PPT 对比页面是否能根据目的选择合理构图，而不是统一两栏或随机选型。

检查优先关注真实执行轨迹、最终成品及不必要操作，必要时旧版/新版对照；不默认每轮新建持续评测工程。不同模型/宿主（DSH、Codex 等）的效果需单独检验。

## 9. 本轮取舍状态与下一步

**已确认：** STE-inspired 方向、语义优先、对技术运行时指令进行精确表达、不强制完整 STE、支持中文相似原则。

**建议但未确认：** 采用“目标/默认/触发/例外/验证/终止”的松散语义检查方法，并依契约脆弱性区分精确步骤和专业自由度；使用轻量审阅而非机器可读 Schema。

**建议下一焦点：** 用户认可上述“精确语义但不过度规定形式”的方法后，选择一个 Sentry 源文件切入改造（优先 `source-adaptation.md` + `design-principles.md`），在真实 Skill（如 PPT 或 LaTeX）中试运行，判断改造的实际效果，而不是继续空转元规范。
