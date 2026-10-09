# dsh-sop-sync-check — 作业规程与 FMEA／控制计划一致性核对

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-sop-sync-check` 读取一份作业规程台账——产品表头加每道工序一行——核对它与台账所引 PFMEA、控制计划之间的机械一致性：每道工序是否声明了规程编号、是否引用了 PFMEA 或控制计划、行内引用的版本与台账记录的现行版本是否一致、填了工艺参数的是否填了参数公差、工序号是否重复、表头是否写明产品、修订日期是否可解析且不晚于核对日。它不判断工艺参数设置是否合理、控制计划是否覆盖了全部失效模式、PFMEA 的风险分析是否到位；无法执行的检查会列在 `skipped` 中，而不是静默通过。

## 实际输出长什么样

![Terminal demo of dsh-sop-sync-check: real output over its SS-005 fixture](https://raw.githubusercontent.com/PerryLink/dsh-sop-sync-check/main/docs/assets/dsh-sop-sync-check-demo.png)

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

**Boundary:** this plugin checks a **作业规程台账** for mechanical consistency with its **PFMEA** and
**control plan** — that a number is recorded, that the PFMEA and control plan are cited, that the revision a
procedure cites matches the document's current revision, that a parameter has a tolerance, that process
numbers are unique, that the register names its product, and that revision dates parse. It does **not** judge
whether the process parameters are right, whether the control plan covers every failure mode, or whether the
PFMEA analysis is adequate. **Those are the process and quality engineers' judgements.**

> ### ⚠️ Read this before trusting a citation in the report
>
> **Every `excerpt` in this plugin's rule pack says, in so many words, that the clause text was not
> obtained.** The regime lives in IATF 16949 and the automotive core-tools handbooks (APQP, PFMEA, control
> plan). The verification pass could not retrieve verbatim clause text from them, so rather than paraphrase a
> quotation the pack states the gap in the `excerpt` field itself and puts the honest reasoning in `note`.
> Every rule is therefore `warn` or `info`, and a test asserts that no rule claims a quotation it does not
> have. **When the texts are in hand, two things must be done: replace each `excerpt` with the real clause,
> and raise `kind` to `direct`.**
>
> `SS-003` is the one that earns its keep: **a procedure still citing the previous PFMEA revision** is the
> commonest and most dangerous way the three documents drift apart. It reads the revision either from a
> dedicated column or from a version marker at the tail of the reference text (`PFMEA-2026-003 V2`), and it
> needs an explicit cue — `V`, `VER`, `REV`, `版本`, `版次` — so that the trailing digits of a *document
> number* are never mistaken for a revision. With neither source available it reports itself in `skipped`.

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-sop-sync-check
dsh --profile <name> --dump-config | grep 'dsh-sop-sync-check'
```

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
