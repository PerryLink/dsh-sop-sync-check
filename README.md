# dsh-sop-sync-check — Works-instruction register and PFMEA / control plan sync check

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-sop-sync-check` reads one works-instruction register — the product header plus one row per process — and checks that register's mechanical consistency with the PFMEA and control plan it cites: that each process row carries a procedure number, that the PFMEA or control plan is cited at all, that the revision a row cites matches the revision the register records as the document's current one, that a stated parameter carries a tolerance, that no process number is repeated, that the header names its product, and that the revision date parses and is not later than the check date. It does not judge whether the process parameters are right, whether the control plan covers every failure mode, or whether the PFMEA analysis is adequate; a check that cannot run is listed in `skipped` instead of passing silently.

## What it looks like

![Terminal demo of dsh-sop-sync-check: real output over its SS-005 fixture](https://raw.githubusercontent.com/PerryLink/dsh-sop-sync-check/main/docs/assets/dsh-sop-sync-check-demo.png)

Real output from this plugin over its own `SS-005` test fixture — not a mock-up. The rule pack ships no invented quotations, so a finding names both the clause it applied and the fact that the clause text was not obtained.

## What it answers

| You ask | What it answers |
|---|---|
| A process row has no procedure number in the 规程编号 column. | `SS-001` reports that row: the rule requires the procedure-number column to be filled on every row that carries it, and it checks presence only — not whether the procedure is the right one for that process. If the material has no such column at all, the rule reports that it does not apply instead of passing silently. |
| Nobody wrote down which PFMEA or control plan this works instruction belongs to. | `SS-002` requires at least one of PFMEA编号 and 控制计划编号 to be filled on each row. It checks only that at least one is cited — not whether the reference is apt, and not whether the revision it names is the current one; that comparison is `SS-003`. |
| The procedure still cites the previous PFMEA revision. Will that be caught? | Yes. `SS-003` reads the revision from a dedicated revision column or from a version marker at the tail of the reference text (`PFMEA-2026-003 V2`); the marker needs an explicit cue such as `V`, `VER`, `REV`, `版本` or `版次`, so the trailing digits of a document number are never mistaken for a revision. It reports the reference whose version string differs from the document's current revision, and it compares version strings only — it does not decide which revision the reference should point to. When neither a revision column nor a readable version string is available it reports itself in `skipped`. |
| The parameter column is filled but the 参数公差 column is empty. | `SS-004` reports that row — but only when the parameter column is filled, so a process that genuinely carries no parameter is not flagged. It checks that the tolerance column is filled, not that the parameter and its tolerance are reasonable. |
| The same process number appears on two rows. | `SS-005` reports the repeated 工序号 and names the first row it saw with that number; whitespace is ignored in the comparison. Repetition usually means a double registration or a mistyped process number — which row is right stays a human decision. With no process-number column at all the rule reports that it does not apply rather than passing. |
| A revision date reads `2026/3/8`, and one row is dated next month. | `SS-007` reports a 修订日期 it cannot parse, and a date later than the check date. It checks that the date parses and does not fall after the check date; it does not judge whether the revision was made promptly. |

## Standards it follows

This rule pack cites no public standard: the verification obtained no verbatim clause text from IATF 16949 or the automotive core-tools handbooks, so every rule's `basis` says so in as many words, each is `derived-from-principle`, and none rises above `warn`. What the checks rest on instead is the register's own stated numbers and revisions — the procedure number it writes in its own column, the revision it records against the PFMEA or control plan reference, the tolerance beside a parameter, the revision date — compared with one another.

| Document | Number | Cited by rules |
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

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a full works-instruction set use `ptc` |

## What it does

Registers the `sop_sync_check` tool. It reads one works-instruction register — the product header plus one row
per process — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `SS-001` | every process declares a procedure number | warn | principle |
| `SS-002` | the procedure cites its PFMEA or control plan | warn | principle |
| `SS-003` | the cited revision matches the document's current revision | warn | principle |
| `SS-004` | a stated parameter carries a tolerance | warn | principle |
| `SS-005` | process numbers are unique | warn | principle |
| `SS-006` | the register names its product | warn | principle |
| `SS-007` | the revision date parses and is not in the future | warn | principle |

## Install

```sh
dsh plugin --profile <name> add dsh-sop-sync-check
dsh --profile <name> --dump-config | grep 'dsh-sop-sync-check'
```

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/sop-sync-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `SS-003` `referenceField` / `actualVersionField` / `sameVersionField` — where the cited revision and the
  document's current revision live. `actualVersionField` takes a list; the first non-empty candidate wins,
  and a bare version (`V2`) or a reference carrying one (`PFMEA-2026-003 V2`) both work. If your register
  keeps the cited revision in its own column, name it in `sameVersionField`.
- `SS-004` `conditionField` / `requiredFields` — which column triggers the requirement, and what it needs.

## Material format

The tool accepts JSON or YAML:

```yaml
productNo: P-2026-001
productName: 前支架
rows:
  - { 规程编号: WI-2026-018, 工序号: OP20, 工序名称: 精车外圆,
      工艺参数: 主轴转速 1200 r/min, 参数公差: ±50 r/min,
      PFMEA编号: PFMEA-2026-003 V2, PFMEA现行版本: V2,
      控制计划编号: CP-2026-003 V2, 控制计划现行版本: V2, 修订日期: 2026-03-08 }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own
column names are kept, so a finding names the column it read. Dates may be `2026-03-08` or
`2026-03-08 09:30`.

## Rule sources

Rule data lives in `rules/sop-sync-check.yaml`. The pack's header states the citation gap in full, and each
rule's `note` repeats the part that matters for that rule. The load-time guard that normally enforces "an
excerpt must be a real quotation of at least eight characters" cannot tell a quotation from a description —
so this pack leans on the header, the per-rule notes and a test that asserts every `excerpt` admits the gap.

## Troubleshooting

- **`SS-003` reports itself as skipped.** Neither the cited revision nor the document's current revision could
  be read. Give the register a `PFMEA现行版本` column, or put the revision in the reference text as `V2`.
- **`SS-003` does not fire although I know the revisions differ.** Check that the revision column resolved as
  the current version: the first non-empty candidate column wins, so a stale column listed earlier will mask
  a later one.
- **`SS-003` fires on a reference with no revision.** That is the check — a reference that does not say which
  revision it is on cannot be compared.
- **`SS-004` fires on a process with no tolerance.** Either the parameter genuinely has one and it is missing,
  or the process carries no parameter and the parameter column should be empty.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-sop-sync-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-sop-sync-check   # refresh src/shared from ../src
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and
the check engine, and the rule pack declares every check.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-sop-sync-check contributors.
