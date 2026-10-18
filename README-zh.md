# dsh-sop-sync-check — 作业规程与 FMEA／控制计划一致性核对

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-sop-sync-check` 读取一份作业规程台账——产品表头加每道工序一行——核对它与台账所引 PFMEA、控制计划之间的机械一致性：每道工序是否声明了规程编号、是否引用了 PFMEA 或控制计划、行内引用的版本与台账记录的现行版本是否一致、填了工艺参数的是否填了参数公差、工序号是否重复、表头是否写明产品、修订日期是否可解析且不晚于核对日。它不判断工艺参数设置是否合理、控制计划是否覆盖了全部失效模式、PFMEA 的风险分析是否到位；无法执行的检查会列在 `skipped` 中，而不是静默通过。

## Install

```sh
dsh plugin --profile <name> add dsh-sop-sync-check
dsh --profile <name> --dump-config | grep 'dsh-sop-sync-check'
```

## 实际输出长什么样

![Terminal demo of dsh-sop-sync-check: real output over its SS-005 fixture](https://raw.githubusercontent.com/PerryLink/dsh-sop-sync-check/main/docs/assets/dsh-sop-sync-check-hero.png)

![Animated terminal demo of dsh-sop-sync-check](https://raw.githubusercontent.com/PerryLink/dsh-sop-sync-check/main/docs/assets/dsh-sop-sync-check-demo.gif)

本插件对自己 `SS-005` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文，因此每条发现都会同时写明所引条款，以及该条款原文本次未取得。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 某道工序行的规程编号栏是空的。 | `SS-001` 会报出该行：本条要求凡带规程编号栏的行都必须填写，且只核对是否填写，不判断这份规程是不是该工序该用的那一份。材料里根本没有这一栏时，本条报告「不适用」，而不是静默通过。 |
| 这份作业指导书对应哪份 PFMEA、哪份控制计划，没人写。 | `SS-002` 要求每行的 PFMEA编号与控制计划编号至少填写一项。它只核对「至少引用了一个」，不判断引用得是否恰当，也不核对引用的是不是现行版本——那是 `SS-003` 的事。 |
| 规程里引用的还是上一版 PFMEA，能查出来吗？ | 能。`SS-003` 从单独的版本栏，或从引用文本尾部提取版本串（如 `PFMEA-2026-003 V2`），版本串需要 `V`、`VER`、`REV`、`版本`、`版次` 这类明确提示，因此文件编号末尾的数字不会被误当成版本；版本串与文件现行版本不一致的引用会逐行报出。它只比对版本串，不判断该引用应当指向哪一版。两处都取不到可比版本串时，本条报告「无法执行」。 |
| 工艺参数栏填了，参数公差栏空着。 | `SS-004` 会报出该行，但只在参数栏已填写时才要求公差栏，因此本工序确实无需参数的行不会被报出。它只核对公差栏是否填写，不判断该参数与公差设置是否合理。 |
| 同一个工序号在两行里都出现了。 | `SS-005` 会报出重复的工序号，并指出它第一次出现在哪一行；比较时忽略空白字符。重复通常意味着重复登记或工序号抄错，哪一行是对的仍由人工确认。材料里没有工序号栏时，本条报告「不适用」，而不是通过。 |
| 修订日期写成 `2026/3/8`，另有一行写的是下个月。 | `SS-007` 会报出无法解析为日期的修订日期，也会报出晚于核对日的日期。它只核对日期是否可解析、是否不晚于核对日，不判断修订是否及时。 |

## 依据的标准

本规则库不引用任何公开标准：核查未取得 IATF 16949 与汽车行业核心工具手册的逐字条文，因此每条规则的 `basis` 都如实写明这一点，`kind` 一律为 derived-from-principle，严重度封顶 `warn`。它依据的是台账自己写的编号与版本——规程编号栏里的编号、PFMEA／控制计划引用旁记录的版本、参数旁的公差、修订日期——以及它们之间的相互比对。

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| IATF 16949／汽车行业核心工具手册 | 现行版本与条号本次未核实 | SS-001, SS-002, SS-003, SS-004, SS-005, SS-006, SS-007 |

**边界（中文译文，以英文原文为准）：** 本插件核对一份 **作业规程台账** 与其 **PFMEA** 及 **控制计划（control plan）** 的机械一致性——是否记录编号，是否引用 PFMEA 与控制计划，规程所引版本是否与文档的当前版本一致，参数是否带有公差，工序编号是否唯一，台账是否写明其产品，以及修订日期是否可解析。它**不**判定工艺参数是否正确、控制计划是否覆盖每一个失效模式，或 PFMEA 分析是否充分。**这些属于工艺与质量工程师的判断。**

> ### ⚠️ 在相信报告中的引文之前，请先读这一节（以英文原文为准）
>
> **本插件规则库中的每一个 `excerpt` 都明文写着：条款原文本次未取得。** 该制度见于 IATF 16949 与汽车行业核心工具手册（APQP、PFMEA、控制计划）。核验环节无法从这些文件中取得逐字条款原文，因此规则库没有去转述一段引文，而是在 `excerpt` 字段本身写明这一缺口，并把诚实的推理写进 `note`。因此每条规则都是 `warn` 或 `info`，且有测试断言：没有任何规则声称拥有它实际没有的引文。**待取得原文后，必须做两件事：把每个 `excerpt` 换成真实条款，并把 `kind` 提到 `direct`。**
>
> `SS-003` 是最能体现价值的一条：**作业规程仍在引用上一版 PFMEA**，是这三份文件彼此脱节最常见、也最危险的方式。它要么从专门的栏读取版本，要么从引用文字末尾的版本标记（`PFMEA-2026-003 V2`）读取，并且需要一个明确的提示词——`V`、`VER`、`REV`、`版本`、`版次`——这样*文档编号*末尾的数字就永远不会被误认为版本号。两种来源都不可用时，它把自己记入 `skipped`。

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-rc.2`。**已声明 `engines.dsh`**：0.2.1 起由宿主单独裁决，范围为 `>=0.2.1-0 <0.3.0` |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/sop-sync-check.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-sop-sync-check
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-sop-sync-check contributors.
