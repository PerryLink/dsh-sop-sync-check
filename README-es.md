# dsh-sop-sync-check — Registro de instrucciones de trabajo y verificación de sincronía con el PFMEA / plan de control

`dsh-sop-sync-check` lee un registro de instrucciones de trabajo —la cabecera de producto más una fila por operación— y comprueba la coherencia mecánica de ese registro con el PFMEA y el plan de control que cita: que cada fila de operación lleve número de procedimiento, que se cite el PFMEA o el plan de control, que la revisión citada en la fila coincida con la revisión que el registro da como vigente, que un parámetro declarado lleve tolerancia, que no se repita ningún número de operación, que la cabecera identifique el producto y que la fecha de revisión se pueda analizar y no sea posterior a la fecha de comprobación. No juzga si los parámetros de proceso son correctos, si el plan de control cubre todos los modos de fallo ni si el análisis PFMEA es adecuado; una comprobación que no puede ejecutarse se lista en `skipped` en lugar de pasar en silencio.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fila de operación no tiene número de procedimiento en la columna 规程编号. | `SS-001` informa de esa fila: la regla exige que la columna del número de procedimiento esté rellena en toda fila que la traiga, y solo comprueba la presencia, no que el procedimiento sea el que corresponde a esa operación. Si el material no tiene esa columna, la regla informa de que no aplica en lugar de pasar en silencio. |
| Nadie anotó a qué PFMEA o a qué plan de control pertenece esta instrucción de trabajo. | `SS-002` exige que se rellene en cada fila al menos uno de PFMEA编号 y 控制计划编号. Solo comprueba que se cite al menos uno, no que la referencia sea acertada ni que su revisión sea la vigente; esa comparación es `SS-003`. |
| El procedimiento sigue citando la revisión anterior del PFMEA. ¿Se detecta? | Sí. `SS-003` toma la revisión de una columna propia o de un marcador de versión al final del texto de la referencia (`PFMEA-2026-003 V2`); el marcador necesita una señal explícita como `V`, `VER`, `REV`, `版本` o `版次`, de modo que los dígitos finales de un número de documento nunca se tomen por una revisión. Informa de la referencia cuyo texto de versión difiere de la revisión vigente del documento, y solo compara cadenas de versión: no decide a qué revisión debería apuntar la referencia. Cuando no hay ni columna de revisión ni cadena legible, se informa a sí misma en `skipped`. |
| La columna de parámetros está rellena, pero la de 参数公差 está vacía. | `SS-004` informa de esa fila, pero solo cuando la columna de parámetros está rellena, así que una operación que realmente no lleva parámetro no se señala. Comprueba que la columna de tolerancia esté rellena, no que el parámetro y su tolerancia sean razonables. |
| El mismo número de operación aparece en dos filas. | `SS-005` informa del 工序号 repetido y nombra la primera fila en que apareció; en la comparación se ignoran los espacios. La repetición suele significar un registro duplicado o un número mal copiado: qué fila es la correcta sigue siendo decisión humana. Sin columna de número de operación, la regla informa de que no aplica en lugar de pasar. |
| Una fecha de revisión figura como `2026/3/8` y otra fila lleva la del mes que viene. | `SS-007` informa de una 修订日期 que no puede analizar y de una fecha posterior a la fecha de comprobación. Comprueba que la fecha se analice y no caiga después de la fecha de comprobación; no juzga si la revisión se hizo a tiempo. |

## Normas que sigue

Este paquete de reglas no cita ninguna norma pública: la verificación no obtuvo el texto literal de las cláusulas de IATF 16949 ni de los manuales de herramientas básicas del sector automotriz, de modo que el `basis` de cada regla lo dice con todas las letras, todas son `derived-from-principle` y ninguna supera `warn`. En lo que sí se apoyan las comprobaciones es en los números y revisiones que el propio registro declara —el número de procedimiento de su columna, la revisión anotada junto a la referencia del PFMEA o del plan de control, la tolerancia junto a un parámetro, la fecha de revisión— comparados entre sí.

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-sop-sync-check
dsh --profile <name> --dump-config | grep 'dsh-sop-sync-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/sop-sync-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-sop-sync-check
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-sop-sync-check contributors.
