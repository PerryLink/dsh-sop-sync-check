#!/usr/bin/env python3
"""README visuals for dsh-sop-sync-check, derived from the plugin's real data.

Two figures, both read off this repository's own material:

  hero 1440×576 (Pillow, 4 files: zh/en × light/dark)
      One ledger row and the two documents it cites.  The row is OP20 from
      tests/fixtures/SS-003/SS-003-unsafe.json: SOP no. WI-2026-018, PFMEA
      citation ``PFMEA-2026-003 V1``.  The register's header records the
      PFMEA's current revision as V2, so the PFMEA rail shows V1 ≠ V2 (the
      SS-003 finding); the control-plan citation is V2 and its current
      revision is V2, so that rail is in sync.  The actual run of that
      material yields issueCount 1 and skippedCount 1 (SS-004 is not
      applicable because the material has no parameter row), which is the
      report strip under the document rails.

  flow 1100×660 (hand-written SVG, 2 files: light/dark)
      A three-way alignment bench, not a generic node chain:
        01  the ledger row with its PFMEA and control-plan citations,
            drawn against the two document plates that carry the current
            revisions;
        02  the shipped rule pack, seven rules grouped by what they read
            (completeness / version match / in-row consistency), with the
            exact check kinds from rules/sop-sync-check.yaml;
        03  the two exits the engine actually writes: issues[] with a
            locator, found, expected and fix, and skipped[] with a reason.
      The sample outcome is the same real run as the hero: SS-003 warns,
      SS-004 is skipped, the other five run without reporting a difference.

Text values are taken from:
  tests/fixtures/SS-003/SS-003-unsafe.json   (WI-2026-018, OP20,
      PFMEA-2026-003 V1, CP-2026-003 V2, PFMEA/CP current V2)
  rules/sop-sync-check.yaml                  (SS-001..SS-007, check kinds)
  the sampled run of that fixture            (SS-003 issue, SS-004 skipped)

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
"""
from __future__ import annotations

import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _path in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")

FONT_FILES = {
    "cjk": FONT_CJK,
    "cjk_bold": FONT_CJK_BOLD,
    "mono": FONT_MONO,
    "mono_bold": FONT_MONO_BOLD,
}
RADIUS = 20
SHADOW = 24

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", card_edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent_soft="#eef1fa", accent_edge="#cdd6ee",
        violet="#6F5AB5", violet_soft="#f3f0fc", violet_edge="#ddd5f3",
        teal="#2F7F76", teal_soft="#eef8f6", teal_edge="#c9e6e1",
        warn="#B45309", warn_soft="#fdf3e9", warn_edge="#eccba8",
        green="#15803D", green_soft="#e9f7ef", green_edge="#c8e8d4",
        band="#f6f4fb", grid="#e9e6f1",
        shadow=(32, 26, 64),
        report="#1e2942", report_text="#f4f6fc", report_sub="#b9c5e6",
        report_green="#7fe0a6",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", card_edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent_soft="#232c46", accent_edge="#3a4562",
        violet="#b3a6ff", violet_soft="#282442", violet_edge="#443d6a",
        teal="#5fcfc0", teal_soft="#1b2d2c", teal_edge="#2f5450",
        warn="#d9a441", warn_soft="#2a2216", warn_edge="#5a4520",
        green="#3fb950", green_soft="#142a1d", green_edge="#295038",
        band="#202839", grid="#262f42",
        shadow=(0, 0, 0),
        report="#242f49", report_text="#f4f6fc", report_sub="#b9c5e6",
        report_green="#8ee6a8",
    ),
}

# --------------------------------------------------------------------------- hero data
# Every character below is a real value from this repository; see module docstring.
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 核对器",
        value=["规程、PFMEA、控制计划", "逐行对到同一个版本"],
        sub=["交一份作业规程台账，核对规程编号、PFMEA／控制计划引用与版本；",
             "每条差异落到行号与字段——原件不改，结论留给人。"],
        meta="SS-001…SS-007 · 规则即数据 · skipped 逐条说明 · 不联网",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        version="v0.2.9",
        tab="台账",
        reg_title="作业规程台账 · 第 1 行",
        product="P-2026-001 · 前支架",
        headers=["工序", "规程编号", "工艺参数", "公差", "修订日期"],
        widths=[54, 132, 150, 82, 150],
        cells=["OP20", "WI-2026-018", "—", "—", "2026-03-08"],
        note="依据：表头 pfmeaVersion = V2；PFMEA 引用尾部 V1",
        p_tag="PFMEA", p_no="PFMEA-2026-003", p_ref="PFMEA-2026-003 V1",
        p_ref_label="PFMEA 引用",
        c_tag="控制计划", c_no="CP-2026-003", c_ref="CP-2026-003 V2",
        c_ref_label="控制计划 引用",
        p_cited="引用 V1", p_current="现行 V2", p_badge="SS-003 · warn",
        p_note="版本取自引用尾部；只比对版本串，不判断应指向哪一版",
        c_cited="引用 V2", c_current="现行 V2", c_badge="同版",
        c_note="引用编号与版本均已填写，且与现行版本一致",
        report_left="issues[] 1 · skipped[] 1",
        report_mid="SS-003 · 第 1 行 · pfmeaRef",
        report_right="结论留给人",
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · checker",
        value=["SOPs, PFMEA, control plan", "one version, line by line"],
        sub=["Hand in a works-instruction register: it compares procedure numbers,",
             "citations and revisions across PFMEA and the control plan.",
             "Every finding lands on a row and a field; the verdict stays with you."],
        meta="SS-001…SS-007 · rules as data · skipped always explained · offline",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        version="v0.2.9",
        tab="SOP",
        reg_title="works-instruction register · row 1",
        product="P-2026-001 · front bracket",
        headers=["Op.", "SOP no.", "Parameter", "Tolerance", "Revised"],
        widths=[54, 132, 150, 82, 150],
        cells=["OP20", "WI-2026-018", "—", "—", "2026-03-08"],
        note="pfmeaVersion V2 from the header; V1 parsed from the citation tail",
        p_tag="PFMEA", p_no="PFMEA-2026-003", p_ref="PFMEA-2026-003 V1",
        p_ref_label="PFMEA citation",
        c_tag="Control plan", c_no="CP-2026-003", c_ref="CP-2026-003 V2",
        c_ref_label="Control-plan citation",
        p_cited="cited V1", p_current="current V2", p_badge="SS-003 · warn",
        p_note="Version parsed from the citation tail; string compare only",
        c_cited="cited V2", c_current="current V2", c_badge="in sync",
        c_note="Citation number and revision are filled and match the current one",
        report_left="issues[] 1 · skipped[] 1",
        report_mid="SS-003 · row 1 · pfmeaRef",
        report_right="verdict stays human",
    ),
}


def font(size: int, kind: str = "cjk_bold") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], size)


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: int, kind: str) -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def require_w(text: str, size: int, kind: str, max_w: float, what: str) -> None:
    width = measure(text, size, kind)
    if width > max_w + 0.4:
        raise SystemExit(
            f"FATAL: {what} overflows: {text!r} needs {width:.1f}px > {max_w}px")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    size = start
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    raise SystemExit(f"FATAL: text does not fit {max_w}px at >= {minimum}px: {text!r}")


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    return min(fit(line, kind, max_w, start, minimum) for line in lines)


def hx(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.22 * (y / h) + 0.78 * (y / h) ** 1.25
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: tuple,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(10, 0, -1):
        rr = r * i / 10
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                     fill=color + (int(alpha * (1 - i / 11)),))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def dots(img: Image.Image, color: str, alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for y in range(18, img.height, 26):
        for x in range(18, img.width, 26):
            if x < 700:
                continue
            draw.ellipse([x, y, x + 2, y + 2], fill=hx(color) + (alpha,))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
         radius: int = RADIUS, shadow: int = SHADOW,
         fill: str | None = None, outline: str | None = None) -> Image.Image:
    """A soft-shadowed rounded card on the gradient background."""
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -2):
        sd.rounded_rectangle(
            [x0 - i // 7, y0 + i // 2, x1 + i // 7, y1 + i],
            radius=radius + i // 7,
            fill=s["shadow"] + (int(8 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(11)))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius,
                           fill=hx(fill or s["card"]),
                           outline=hx(outline or s["card_edge"]), width=2)
    return base.convert("RGB")


def chip(img: Image.Image, xy: tuple[int, int], text: str, size: int,
         fg: str, bg: str, border: str | None = None, height: int | None = None,
         padx: int = 10, kind: str = "cjk", bold: bool = False) -> tuple[int, int]:
    draw = ImageDraw.Draw(img)
    f = font(size, "cjk_bold" if bold else kind)
    width = draw.textlength(text, font=f)
    h = height or size + 12
    x, y = xy
    draw.rounded_rectangle(
        [x, y, x + width + padx * 2, y + h], radius=h // 2,
        fill=hx(bg), outline=hx(border) if border else None,
        width=1 if border else 0)
    draw.text((x + padx, y + h / 2), text, font=f, fill=hx(fg), anchor="lm")
    return int(width + padx * 2), h


def pill(img: Image.Image, xy: tuple[int, int], text: str, s: dict,
         size: int = 14, fg: str | None = None, bg: str | None = None,
         border: str | None = None, height: int | None = None) -> tuple[int, int]:
    return chip(img, xy, text, size, fg or s["accent"], bg or s["accent_soft"],
                border or s["accent_edge"], height or size + 18, 14, "cjk", True)


def put(draw: ImageDraw.ImageDraw, x: float, y: float, text: str,
        size: int, kind: str, fill: str, anchor: str = "la") -> None:
    draw.text((x, y), text, font=font(size, kind), fill=hx(fill), anchor=anchor)


def put_right(draw: ImageDraw.ImageDraw, xr: float, y: float, text: str,
              size: int, kind: str, fill: str) -> None:
    draw.text((xr, y), text, font=font(size, kind), fill=hx(fill), anchor="ra")


def draw_header(img: Image.Image, lang: str, s: dict) -> Image.Image:
    H = HERO[lang]
    draw = ImageDraw.Draw(img)
    x = 72

    pw, ph = pill(img, (x, 52), H["kicker"], s, size=14)
    draw = ImageDraw.Draw(img)

    title_size = fit("dsh-sop-sync-check", "mono_bold", 596, 56, 48)
    put(draw, x - 2, 104, "dsh-sop-sync-check", title_size, "mono_bold", s["text"])

    value_size = fit_lines(H["value"], "cjk_bold", 596, 40, 34)
    for index, line in enumerate(H["value"]):
        require_w(line, value_size, "cjk_bold", 596, "hero value")
        put(draw, x, 204 + index * 56, line, value_size, "cjk_bold", s["text"])

    for index, line in enumerate(H["sub"]):
        require_w(line, 17, "cjk", 596, "hero sub")
        put(draw, x + 1, 330 + index * 31, line, 17, "cjk", s["sub"])

    require_w(H["meta"], 14, "cjk", 596, "hero meta")
    put(draw, x + 1, 438, H["meta"], 14, "cjk", s["faint"])

    draw.line([x + 1, 486, x + 596, 486], fill=hx(s["grid"]), width=2)
    put(draw, x + 1, 500, H["foot"], 13, "cjk", s["faint"])
    put_right(draw, x + 596, 500, H["version"], 13, "mono", s["faint"])
    return img


def draw_register(img: Image.Image, lang: str, s: dict) -> Image.Image:
    H = HERO[lang]
    img = card(img, (752, 92, 1368, 260), s, radius=20, shadow=24)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([776, 92, 812, 96], radius=2, fill=hx(s["accent"]))
    tab_w, _ = chip(img, (776, 104), H["tab"], 11, s["accent"], s["accent_soft"],
                    s["accent_edge"], 22, 10, "cjk", False)
    draw = ImageDraw.Draw(img)
    require_w(H["reg_title"], 14.5, "cjk_bold", 330, "hero register title")
    put(draw, 776 + tab_w + 10, 106, H["reg_title"], 14.5, "cjk_bold", s["text"])
    require_w(H["product"], 11.5, "cjk", 210, "hero register product")
    put_right(draw, 1344, 108, H["product"], 11.5, "cjk", s["faint"])

    x0, table_w = 776, sum(H["widths"])
    draw.rounded_rectangle([x0 - 4, 134, x0 + table_w + 4, 156], radius=8,
                           fill=hx(s["band"]))
    xs = []
    acc = x0
    for width in H["widths"]:
        xs.append(acc)
        acc += width
    for index, head in enumerate(H["headers"]):
        require_w(head, 11, "cjk", H["widths"][index] - 14, "hero table header")
        put(draw, xs[index] + 7, 139, head, 11, "cjk", s["sub"])

    # The one empty pair of cells is the parameter/tolerance pair; SS-004 skips
    # it, while the citation blocks below carry the versions SS-003 reads.
    for index, value in enumerate(H["cells"]):
        kind = "mono" if index in (1, 4) else "cjk"
        size = 13
        require_w(value, size, kind, H["widths"][index] - 16, "hero table cell")
        put(draw, xs[index] + 7, 161, value, size, kind, s["text"])

    # Two citation blocks under the table.
    blocks = [
        (776, 282, H["p_ref_label"], H["p_ref"], s["warn"],
         s["warn_soft"], s["warn_edge"]),
        (1066, 278, H["c_ref_label"], H["c_ref"], s["teal"],
         s["teal_soft"], s["teal_edge"]),
    ]
    for bx, bw, label, number, color, soft, edge in blocks:
        draw.rounded_rectangle([bx, 186, bx + bw, 224], radius=10, fill=hx(soft),
                               outline=hx(edge), width=1)
        draw.rounded_rectangle([bx + 10, 196, bx + 14, 214], radius=2, fill=hx(color))
        put(draw, bx + 22, 190, label, 11, "cjk", s["sub"])
        require_w(number, 13, "mono", bw - 34, "hero citation number")
        prefix = number.rsplit(" ", 1)[0] + " "
        put(draw, bx + 22, 204, prefix, 13, "mono", s["text"])
        put(draw, bx + 22 + measure(prefix, 13, "mono"), 204,
            number[len(prefix):], 13, "mono_bold", color)

    require_w(H["note"], 11.5, "cjk", 568, "hero register note")
    put(draw, 776, 234, H["note"], 11.5, "cjk", s["faint"])
    return img


def revision_token(label: str) -> str:
    """`引用 V1` / `cited V1` / `现行 V2` -> `V1` / `V2`."""
    return label.rsplit(" ", 1)[-1]


def draw_document_rail(img: Image.Image, lang: str, s: dict, *,
                       y: int, tag: str, number: str, cited: str,
                       current: str, badge: str, note: str,
                       color: str, soft: str, edge: str,
                       badge_color: str, badge_soft: str) -> Image.Image:
    img = card(img, (752, y, 1368, y + 104), s, radius=20, shadow=22)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([776, y, 816, y + 4], radius=2, fill=hx(color))
    chip(img, (776, y + 14), tag, 11, color, soft, edge, 22, 10, "cjk", False)
    draw = ImageDraw.Draw(img)
    require_w(number, 17, "mono_bold", 250, "hero document number")
    put(draw, 776, y + 42, number, 17, "mono_bold", s["text"])

    require_w(badge, 11.5, "cjk", 118, "hero document badge")
    chip(img, (1226, y + 14), badge, 11.5, badge_color, badge_soft, None, 22, 10,
         "cjk", True)
    draw = ImageDraw.Draw(img)

    # Version rail: cited revision → current revision.
    cw, _ = chip(img, (1036, y + 38), cited, 13, color, soft, edge, 30, 11,
                 "cjk", True)
    draw = ImageDraw.Draw(img)
    same_revision = revision_token(cited) == revision_token(current)
    symbol = "=" if same_revision else "≠"
    symbol_color = s["green"] if same_revision else s["warn"]
    put(draw, 1036 + cw + 10, y + 42, symbol, 20, "cjk_bold", symbol_color)
    nw, _ = chip(img, (1036 + cw + 38, y + 38), current, 13, color,
                 soft, edge, 30, 11, "cjk", True)
    draw = ImageDraw.Draw(img)
    if same_revision:
        # Repaint the equal chip with green text and a green fill.
        draw.rounded_rectangle([1036 + cw + 38, y + 38,
                                1036 + cw + 38 + nw, y + 68],
                               radius=15, fill=hx(s["green_soft"]),
                               outline=hx(s["green_edge"]), width=1)
        put(draw, 1036 + cw + 38 + 11, y + 53, current, 13, "cjk_bold",
            s["green"], "lm")
    else:
        # The cited revision is the one that disagrees; keep it warm.
        draw.rounded_rectangle([1036 + cw + 38, y + 38,
                                1036 + cw + 38 + nw, y + 68],
                               radius=15, fill=hx(color))
        put(draw, 1036 + cw + 38 + 11, y + 53, current, 13, "cjk_bold",
            "#ffffff", "lm")

    require_w(note, 11.5, "cjk", 568, "hero document note")
    put(draw, 776, y + 77, note, 11.5, "cjk", s["faint"])
    return img


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    H = HERO[lang]
    width, height = 1440, 576
    img = gradient(width, height, s["bg_from"], s["bg_to"])
    img = glow(img, 1240, 60, 430, hx(s["violet"]), 18 if skin == "light" else 30)
    img = glow(img, 90, 600, 310, hx(s["accent"]), 8 if skin == "light" else 16)
    img = dots(img, s["grid"], 90 if skin == "light" else 55)

    draw = ImageDraw.Draw(img)
    draw.line([716, 92, 716, 562], fill=hx(s["grid"]), width=1)

    img = draw_header(img, lang, s)
    img = draw_register(img, lang, s)
    img = draw_document_rail(
        img, lang, s, y=274, tag=H["p_tag"], number=H["p_no"],
        cited=H["p_cited"], current=H["p_current"], badge=H["p_badge"],
        note=H["p_note"], color=s["violet"], soft=s["violet_soft"],
        edge=s["violet_edge"], badge_color=s["warn"], badge_soft=s["warn_soft"])
    img = draw_document_rail(
        img, lang, s, y=392, tag=H["c_tag"], number=H["c_no"],
        cited=H["c_cited"], current=H["c_current"], badge=H["c_badge"],
        note=H["c_note"], color=s["teal"], soft=s["teal_soft"],
        edge=s["teal_edge"], badge_color=s["green"], badge_soft=s["green_soft"])

    img = card(img, (752, 508, 1368, 552), s, radius=18, shadow=18,
               fill=s["report"], outline=s["report"])
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([768, 521, 772, 539], radius=2,
                           fill=hx(s["report_green"]))
    put(draw, 782, 522, H["report_left"], 13, "mono_bold", s["report_text"])
    left_w = measure(H["report_left"], 13, "mono_bold")
    require_w(H["report_mid"], 12.5, "cjk", 260, "hero report mid")
    put(draw, 782 + left_w + 24, 523, H["report_mid"], 12.5, "cjk",
        s["report_sub"])
    require_w(H["report_right"], 13, "cjk_bold", 180, "hero report right")
    put_right(draw, 1350, 522, H["report_right"], 13, "cjk_bold",
              s["report_green"])

    name = f"dsh-sop-sync-check-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name} ({width}x{height})")


# --------------------------------------------------------------------------- flow SVG
FLOW = {
    "light": dict(
        bg1="#f9f6fd", bg2="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent_soft="#eef1fa", accent_edge="#cdd6ee",
        violet="#6F5AB5", violet_soft="#f3f0fc", violet_edge="#ddd5f3",
        teal="#2F7F76", teal_soft="#eef8f6", teal_edge="#c9e6e1",
        warn="#B45309", warn_soft="#fdf3e9", warn_edge="#eccba8",
        green="#15803D", green_soft="#e9f7ef", green_edge="#c8e8d4",
        band="#f6f4fb", grid="#e9e6f1", dot="#d4cde6",
        shadow="#2b2440", shadow_opacity="0.12",
    ),
    "dark": dict(
        bg1="#131a2a", bg2="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent_soft="#232c46", accent_edge="#3a4562",
        violet="#b3a6ff", violet_soft="#282442", violet_edge="#443d6a",
        teal="#5fcfc0", teal_soft="#1b2d2c", teal_edge="#2f5450",
        warn="#d9a441", warn_soft="#2a2216", warn_edge="#5a4520",
        green="#3fb950", green_soft="#142a1d", green_edge="#295038",
        band="#202839", grid="#262f42", dot="#2c3550",
        shadow="#000000", shadow_opacity="0.45",
    ),
}
CJK_STACK = ("'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',"
             "'Source Han Sans SC','Segoe UI',sans-serif")
MONO_STACK = "Consolas,'SFMono-Regular',Menlo,'Courier New',monospace"


def svg_text(x: float, y: float, text: str, size: float, fill: str,
             *, weight: int = 400, anchor: str = "start",
             mono: bool = False, opacity: float = 1.0) -> str:
    family = MONO_STACK if mono else CJK_STACK
    extra = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{extra}>{escape(text)}</text>')


def svg_chip(x: float, y: float, text: str, size: float, fg: str, bg: str,
             *, border: str | None = None, height: float = 24,
             padx: float = 9, mono: bool = False, bold: bool = True,
             width: float | None = None) -> str:
    """A chip with a caller-supplied width (SVG has no text metric here)."""
    if width is None:
        width = len(text) * size * (0.60 if mono else 0.92) + padx * 2
    stroke = (f' stroke="{border}" stroke-width="1"' if border else "")
    weight = 700 if bold else 400
    family = MONO_STACK if mono else CJK_STACK
    return (f'<g><rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" '
            f'height="{height:.1f}" rx="{height / 2:.1f}" fill="{bg}"{stroke}/>'
            f'<text x="{x + width / 2:.1f}" y="{y + height / 2 + size * 0.36:.1f}" '
            f'font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fg}" text-anchor="middle">{escape(text)}</text></g>')


def svg_pill(x: float, y: float, text: str, size: float, fg: str, bg: str,
             border: str, *, width: float | None = None,
             height: float = 26) -> str:
    if width is None:
        width = len(text) * size * 0.92 + 22
    return svg_chip(x, y, text, size, fg, bg, border=border, height=height,
                    padx=0, width=width)


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    w, h = 1100, 660
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="dsh-sop-sync-check structure">',
        '<title>dsh-sop-sync-check · 三份文件，逐行对齐</title>',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="0.18" y2="1">'
        f'<stop offset="0" stop-color="{s["bg1"]}"/>'
        f'<stop offset="1" stop-color="{s["bg2"]}"/></linearGradient>',
        f'<radialGradient id="ha" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0" stop-color="{s["violet"]}" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="{s["violet"]}" stop-opacity="0"/>'
        f'</radialGradient>',
        f'<radialGradient id="hb" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0" stop-color="{s["accent"]}" stop-opacity="0.10"/>'
        f'<stop offset="1" stop-color="{s["accent"]}" stop-opacity="0"/>'
        f'</radialGradient>',
        f'<pattern id="dots" width="27" height="27" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.4" cy="1.4" r="1.15" fill="{s["dot"]}" opacity="0.55"/>'
        f'</pattern>',
        f'<filter id="soft" x="-25%" y="-25%" width="150%" height="170%">'
        f'<feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="{s["shadow"]}" '
        f'flood-opacity="{s["shadow_opacity"]}"/></filter>',
        f'<filter id="softsm" x="-30%" y="-30%" width="160%" height="185%">'
        f'<feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="{s["shadow"]}" '
        f'flood-opacity="{s["shadow_opacity"]}"/></filter>',
        '</defs>',
        f'<rect width="{w}" height="{h}" rx="22" fill="url(#bg)"/>',
        f'<rect width="{w}" height="{h}" rx="22" fill="url(#dots)" opacity="0.5"/>',
        f'<circle cx="990" cy="40" r="330" fill="url(#ha)"/>',
        f'<circle cx="70" cy="620" r="280" fill="url(#hb)"/>',
    ]

    # ---------------------------------------------------------------- header
    parts += [
        f'<rect x="40" y="28" width="28" height="4" rx="2" fill="{s["accent"]}"/>',
        svg_text(40, 58, "三份文件，逐行对齐", 27, s["text"], weight=700),
        svg_text(40, 82, "sop_sync_check：同一条台账行，两处引用，七条检查，两个出口",
                 13.5, s["sub"]),
        svg_chip(822, 31, "rules 2026.1 · 7 条 · warn / info", 11.5,
                 s["violet"], s["violet_soft"], border=s["violet_edge"],
                 height=25, width=238),
        svg_text(1060, 80, "只读 · 不联网 · 不改原件", 11.5, s["faint"],
                 anchor="end"),
        f'<line x1="40" y1="96" x2="1060" y2="96" stroke="{s["grid"]}" />',
    ]

    # ---------------------------------------------------------------- 01 objects
    parts += [
        svg_text(40, 120, "01", 11.5, s["accent"], weight=700, mono=True),
        svg_text(64, 120, "对照对象", 12, s["text"], weight=700),
        svg_text(1060, 120,
                 "现行版本取自表头；引用版本只认 V / VER / REV / 版本 / 版次",
                 11, s["faint"], anchor="end"),
        f'<rect x="40" y="132" width="520" height="142" rx="18" fill="{s["card"]}" '
        f'stroke="{s["edge"]}" stroke-width="1.5" filter="url(#soft)"/>',
        svg_text(60, 156, "作业规程台账 · rows[0]", 14, s["text"], weight=700),
        svg_text(540, 156, "P-2026-001 · 前支架", 11.5, s["faint"],
                 anchor="end"),
        f'<rect x="52" y="168" width="496" height="22" rx="8" fill="{s["band"]}"/>',
    ]
    cols = [60, 110, 250, 370, 440]
    heads = ["工序", "规程编号", "工艺参数", "公差", "修订日期"]
    for x, head in zip(cols, heads):
        parts.append(svg_text(x + 6, 184, head, 11, s["sub"], weight=600))
    values = [("OP20", "cjk"), ("WI-2026-018", "mono"), ("—", "cjk"),
              ("—", "cjk"), ("2026-03-08", "mono")]
    for x, (value, kind) in zip(cols, values):
        parts.append(svg_text(x + 6, 207, value, 13, s["text"],
                              weight=700 if kind == "cjk" else 400,
                              mono=kind == "mono"))

    # Citation blocks inside the register card.
    for bx, label, number, color, soft, edge in (
        (52, "PFMEA 引用", "PFMEA-2026-003 V1", s["warn"], s["warn_soft"], s["warn_edge"]),
        (306, "控制计划引用", "CP-2026-003 V2", s["teal"], s["teal_soft"], s["teal_edge"]),
    ):
        parts += [
            f'<rect x="{bx}" y="220" width="242" height="42" rx="10" '
            f'fill="{soft}" stroke="{edge}" stroke-width="1"/>',
            f'<rect x="{bx + 10}" y="230" width="4" height="22" rx="2" fill="{color}"/>',
            svg_text(bx + 22, 237, label, 11, s["sub"]),
            svg_text(bx + 22, 254, number, 13, s["text"], mono=True),
        ]

    # Two document plates on the right: current revision lives here.
    for top, tag, number, cited, current, badge, note, color, soft, edge, badge_color, badge_bg in (
        (132, "PFMEA", "PFMEA-2026-003", "引用 V1", "现行 V2", "SS-003 · warn",
         "版本取自引用尾部；只比对版本串，不判断应指向哪一版",
         s["violet"], s["violet_soft"], s["violet_edge"], s["warn"], s["warn_soft"]),
        (212, "控制计划", "CP-2026-003", "引用 V2", "现行 V2", "同版",
         "引用编号与版本均已填写，且与现行版本一致",
         s["teal"], s["teal_soft"], s["teal_edge"], s["green"], s["green_soft"]),
    ):
        same_revision = revision_token(cited) == revision_token(current)
        symbol = "=" if same_revision else "≠"
        symbol_color = s["green"] if same_revision else s["warn"]
        current_bg = s["green_soft"] if same_revision else color
        current_fg = s["green"] if same_revision else "#ffffff"
        current_border = s["green_edge"] if same_revision else None
        parts += [
            f'<rect x="584" y="{top}" width="476" height="72" rx="18" '
            f'fill="{s["card"]}" stroke="{s["edge"]}" stroke-width="1.5" '
            f'filter="url(#softsm)"/>',
            f'<rect x="584" y="{top}" width="40" height="4" rx="2" fill="{color}"/>',
            svg_text(600, top + 19, tag, 11.5, color, weight=700),
            svg_text(600, top + 42, number, 14, s["text"], weight=700, mono=True),
            svg_text(1044, top + 19, current, 14, color, weight=700, anchor="end"),
            svg_chip(600, top + 50, cited, 12, color, soft, border=edge,
                     height=19, padx=6, width=58),
            svg_text(664, top + 64, symbol, 16, symbol_color, weight=700),
            svg_chip(686, top + 50, current, 12.5, current_fg, current_bg,
                     border=current_border, height=19, padx=6, width=74),
            svg_chip(948, top + 50, badge, 11, badge_color, badge_bg,
                     height=20, padx=6, width=96),
        ]
    parts += [
        svg_text(584, 298,
                 "现行版本取自表头；引用版本只认 V / VER / REV / 版本 / 版次",
                 11, s["faint"]),
        # A small fork: the same row cites both documents.
        f'<path d="M560 243 H572 V168 H584" fill="none" stroke="{s["accent"]}" '
        f'stroke-width="1.5" opacity="0.55"/>',
        f'<path d="M572 243 V248 H584" fill="none" stroke="{s["accent"]}" '
        f'stroke-width="1.5" opacity="0.55"/>',
        f'<circle cx="584" cy="168" r="2.6" fill="{s["accent"]}" opacity="0.7"/>',
        f'<circle cx="584" cy="248" r="2.6" fill="{s["accent"]}" opacity="0.7"/>',
    ]

    # ---------------------------------------------------------------- 02 rules
    parts += [
        svg_text(40, 320, "02", 11.5, s["accent"], weight=700, mono=True),
        svg_text(64, 320, "七条检查 · 规则即数据", 12, s["text"], weight=700),
        svg_text(1060, 320, "加载期校验 excerpt 逐字 · severity 封顶 warn / info",
                 11, s["faint"], anchor="end"),
        f'<rect x="40" y="332" width="1020" height="150" rx="18" fill="{s["card"]}" '
        f'stroke="{s["edge"]}" stroke-width="1.5" filter="url(#soft)"/>',
        svg_text(60, 356, "rules/sop-sync-check.yaml", 13, s["text"],
                 weight=700, mono=True),
        svg_text(278, 356, "· 7 条", 11.5, s["faint"]),
        svg_text(1040, 356, "换 YAML 即换规则集", 11, s["faint"], anchor="end"),
    ]
    group_heads = [
        (60, "是否写得全", "3 条"),
        (388, "版本是否同版", "1 条"),
        (716, "行内是否自洽", "3 条"),
    ]
    for gx, title, count in group_heads:
        parts.append(svg_text(gx, 378, title, 13, s["text"], weight=700))
        count_x = gx + 292 if gx != 716 else gx + 316
        parts.append(svg_text(count_x, 378, count, 11, s["faint"], anchor="end"))

    def rule_row(y: float, gx: float, rid: str, title: str, kind: str,
                 *, accent: str | None = None) -> list[str]:
        bg = s["band"] if accent is None else s[accent + "_soft"]
        edge = s["edge"] if accent is None else s[accent + "_edge"]
        fg = s["sub"] if accent is None else s[accent]
        return [
            f'<rect x="{gx}" y="{y}" width="300" height="26" rx="8" '
            f'fill="{bg}" stroke="{edge}" stroke-width="1"/>',
            f'<rect x="{gx + 8}" y="{y + 7}" width="50" height="12" rx="6" '
            f'fill="{s["card"]}" stroke="{edge}" stroke-width="1"/>',
            svg_text(gx + 12, y + 17, rid, 11, fg, weight=700, mono=True),
            svg_text(gx + 64, y + 17.5, title, 13, s["text"], weight=600),
            svg_text(gx + 292, y + 17.5, kind, 11, s["faint"],
                     anchor="end", mono=True),
        ]

    for y, rid, title, kind in (
        (388, "SS-001", "规程编号", "presence"),
        (420, "SS-002", "PFMEA/CP 引用", "presenceAny"),
        (452, "SS-006", "表头产品", "headerPresence"),
    ):
        parts += rule_row(y, 60, rid, title, kind)

    # The version group is the one carrying the live finding.
    parts += [
        f'<rect x="388" y="388" width="300" height="84" rx="12" '
        f'fill="{s["warn_soft"]}" stroke="{s["warn_edge"]}" stroke-width="1.5"/>',
        f'<rect x="400" y="398" width="54" height="14" rx="7" '
        f'fill="{s["card"]}" stroke="{s["warn_edge"]}" stroke-width="1"/>',
        svg_text(405, 409, "SS-003", 11, s["warn"], weight=700, mono=True),
        svg_text(462, 409, "引用版本 = 现行版本", 13, s["text"], weight=600),
        svg_text(400, 431, "V1 ≠ V2 → 1 条差异", 13, s["warn"], weight=700),
        svg_text(400, 450, "V / VER / REV / 版本 / 版次 才当版本标记",
                 11, s["sub"]),
        svg_text(400, 466, "两处都取不到 → skipped", 11, s["faint"]),
    ]

    for y, rid, title, kind, accent in (
        (388, "SS-004", "参数 → 公差", "conditionalPresence", "warn"),
        (420, "SS-005", "工序号唯一", "unique", None),
        (452, "SS-007", "修订日期可解析", "date", None),
    ):
        parts += rule_row(y, 716, rid, title, kind, accent=accent)

    # ---------------------------------------------------------------- 03 exits
    parts += [
        svg_text(40, 500, "03", 11.5, s["accent"], weight=700, mono=True),
        svg_text(64, 500, "两个出口", 12, s["text"], weight=700),
        svg_text(1060, 500, "结论不在报告里", 11, s["faint"], anchor="end"),
        f'<path d="M550 482 V496 H350 V512" fill="none" stroke="{s["accent"]}" '
        f'stroke-width="1.5" opacity="0.65"/>',
        f'<path d="M550 496 H870 V512" fill="none" stroke="{s["accent"]}" '
        f'stroke-width="1.5" opacity="0.65"/>',
        f'<circle cx="350" cy="512" r="2.6" fill="{s["accent"]}"/>',
        f'<circle cx="870" cy="512" r="2.6" fill="{s["accent"]}"/>',
        # issues tray
        f'<rect x="40" y="512" width="620" height="104" rx="18" fill="{s["card"]}" '
        f'stroke="{s["edge"]}" stroke-width="1.5" filter="url(#soft)"/>',
        svg_text(60, 534, "issues[] · 1 条", 13.5, s["text"], weight=700),
        svg_chip(176, 520, "warn", 11, s["warn"], s["warn_soft"],
                 border=s["warn_edge"], height=20, padx=6, width=48),
        svg_text(640, 534, "locator：row 1 · field pfmeaRef", 11,
                 s["faint"], anchor="end", mono=True),
        svg_text(60, 556, "SS-003 第 1 行引用的版本「1」与文件现行版本「2」不一致",
                 13, s["text"]),
        svg_text(60, 576, "期望：引用的版本应与该文件的现行版本一致",
                 11, s["sub"]),
        svg_text(60, 594, "建议：核对是否还停在上一版", 11, s["faint"]),
        # skipped tray
        f'<rect x="680" y="512" width="380" height="104" rx="18" fill="{s["card"]}" '
        f'stroke="{s["edge"]}" stroke-width="1.5" filter="url(#soft)"/>',
        svg_text(700, 534, "skipped[] · 1 条", 13.5, s["text"], weight=700),
        svg_chip(812, 520, "SS-004", 11, s["warn"], s["warn_soft"],
                 border=s["warn_edge"], height=20, padx=6, width=60),
        svg_text(700, 556, "没有满足「parameter」条件的行，本条不适用",
                 13, s["text"]),
        svg_text(700, 576, "空结果 ≠ 没问题", 12, s["warn"], weight=700),
        svg_text(700, 594, "停用、only 收窄、缺列都写明原因", 11, s["faint"]),
        # footer
        f'<line x1="40" y1="628" x2="1060" y2="628" stroke="{s["grid"]}"/>',
        svg_text(40, 646, "只列字面差异 · 不改原件 · 不判合规 · 不联网",
                 12, s["sub"]),
        svg_text(1060, 646, "结论留给工艺与质量工程师", 12, s["accent"],
                 weight=700, anchor="end"),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            hero(lang, skin)
    for skin in ("light", "dark"):
        name = f"dsh-sop-sync-check-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as handle:
            handle.write(flow_svg(skin))
        print(f"wrote {name} (1100x660)")


if __name__ == "__main__":
    main()
