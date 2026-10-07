/**
 * dsh-sop-sync-check — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'sop_sync_check'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  sopNo: ['规程编号', '文件编号', '作业指导书编号', 'sopNo', 'docNo'],
  sopName: ['规程名称', '文件名称', '作业指导书名称', 'sopName', 'title'],
  sopVersion: ['规程版本', '文件版本', '版本', 'sopVersion'],
  processNo: ['工序号', '工序编号', '工位', 'processNo'],
  processName: ['工序名称', '工序', '工位名称', 'processName'],
  equipment: ['设备', '设备型号', '使用设备', 'equipment'],
  parameter: ['工艺参数', '关键参数', '参数', 'parameter'],
  tolerance: ['参数公差', '公差', '规格要求', 'tolerance'],
  pfmeaRef: ['FMEA编号', 'PFMEA编号', 'PFMEA引用', 'pfmeaRef'],
  /**
   * The PFMEA's *current* revision, which a row may state directly.
   *
   * `SS-003` compares the revision a procedure cites against this. It is a row
   * column as well as a header field because a register may record the revision
   * once for the whole set or per process row; whichever it uses, the rule finds it.
   */
  pfmeaVersion: ['PFMEA现行版本', 'PFMEA版本', 'FMEA版本', 'pfmeaVersion'],
  controlPlanRef: ['控制计划编号', '控制计划引用', 'controlPlanRef'],
  controlPlanVersion: ['控制计划现行版本', '控制计划版本', 'controlPlanVersion'],
  revisedAt: ['修订日期', '版本日期', '生效日期', 'revisedAt'],
  owner: ['编制人', '责任人', 'owner'],
  status: ['状态', '文件状态', 'status'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'sops', '规程'],
  columns: COLUMNS,
  header: {
  productNo: ['productNo', '产品编号', '零件号'],
  productName: ['productName', '产品名称'],
  pfmeaVersion: ['pfmeaVersion', 'PFMEA版本'],
  controlPlanVersion: ['controlPlanVersion', '控制计划版本'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '规程编号',
  'sopNo',
  '工序号',
  'processNo',
  '工艺参数',
  'parameter',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
