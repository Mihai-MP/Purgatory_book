#!/usr/bin/env python3
"""Збирає книгу «Чистилище» (Акт 1) у PDF і DOCX.

Запуск:  python3 build/make_book.py
Потрібно: weasyprint, python-docx, Pillow, fonttools; для номерів сторінок
у змісті DOCX — LibreOffice (soffice) і pdftotext. Без них DOCX усе одно
збереться, а Word оновить зміст сам (F9).
Результат — у export/.
"""
import html
import os
import re
import shutil
import subprocess
import tempfile
import uuid
import zipfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import art  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
FONTS = BUILD / "fonts"
BOOK = ROOT / "book" / "act1"
OUT = ROOT / "export"

AUTHOR = "Мігель Ніколсон"
TITLE = "Чистилище"
ACT = "Акт перший"
SUBTITLE = "Початок світів"
BASENAME = "chystylyshche_akt1"
ASSETS = BUILD / "assets"
ILLU = ROOT / "sources" / "art" / "book"   # обкладинка, форзаци, зад (промпти — design/prompts.md)

ACCENT = art.CRIMSON   # кров і блискавка
INK = art.INK
PAPER = "#f8f5ee"
NIGHT = art.NIGHT
IVORY = art.IVORY


# ---------------------------------------------------------------- текст ----

def typo(s: str, short_words=True) -> str:
    """Друкарські дрібниці: апостроф, нерозривні пробіли біля тире."""
    s = s.replace("'", "’")
    s = re.sub(r"^— ", "—\u00a0", s)            # тире на початку репліки
    s = s.replace(" — ", "\u00a0— ")            # тире не починає рядок
    s = s.replace(" – ", "\u00a0— ")
    if short_words:
        s = re.sub(r"(?<=\s)([^\s—]{1,2}) ", lambda m: m.group(1) + "\u00a0", s)  # короткі слова не висять
    return s


def runs(s: str):
    """Розбиває абзац на [(текст, курсив)]."""
    out = []
    for i, part in enumerate(re.split(r"\*([^*]+)\*", s)):
        if part:
            out.append((part, i % 2 == 1))
    return out


def split_title(t: str):
    """«Розділ 1. Промінь» → («Розділ 1», «Промінь»)."""
    m = re.match(r"^(Пролог|Розділ \d+|Частина \S+)\.\s*(.+)$", t)
    return (m.group(1), m.group(2)) if m else ("", t)


def parse():
    """Повертає список частин книги: [{'kind': part/chapter, ...}]."""
    items = []
    for f in sorted(BOOK.glob("[0-9][0-9]_*.md")):
        lines = f.read_text(encoding="utf-8").splitlines()
        paras, buf = [], []

        def flush():
            if buf:
                paras.append(" ".join(x.strip() for x in buf))
                buf.clear()

        cur = None
        for ln in lines + [""]:
            if ln.startswith("#"):
                flush()
                level = len(ln) - len(ln.lstrip("#"))
                text = ln.lstrip("#").strip()
                label, name = split_title(text)
                if label.startswith("Частина"):
                    items.append({"kind": "part", "label": label, "name": name})
                else:
                    cur = {"kind": "chapter", "label": label, "name": name, "blocks": [], "id": f"ch{len(items)}",
                           "num": int(f.name[:2])}
                    items.append(cur)
                    paras = cur["blocks"]
                continue
            if ln.strip() == "---":
                flush()
                paras.append(None)       # розрив сцени
            elif not ln.strip():
                flush()
            else:
                buf.append(ln)
        flush()
    for it in items:
        if it["kind"] == "chapter":
            b = it["blocks"]
            while b and b[0] is None:
                b.pop(0)
            while b and b[-1] is None:
                b.pop()
    return items



# --------------------------------------------------------------- шрифти ----

def font(name):
    return str(FONTS / name)


# ------------------------------------------------------------ оформлення ----

def svg_to_png(svg, w_mm, h_mm, path, dpi=600):
    """Раструє невеликий SVG (орнамент) у PNG через WeasyPrint і pdftoppm — для DOCX."""
    from weasyprint import HTML
    with tempfile.TemporaryDirectory() as td:
        pdf = Path(td) / "o.pdf"
        HTML(string=f'<style>@page{{size:{w_mm}mm {h_mm}mm;margin:0}}body{{margin:0}}'
                    f'div{{width:{w_mm}mm;height:{h_mm}mm}}</style><div>{svg}</div>').write_pdf(pdf)
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", str(pdf), str(path.with_suffix(""))], check=True)
    return path


def make_assets(dpi=300):
    """Фони (растр) і орнаменти. Повертає словник шляхів у build/assets/."""
    ASSETS.mkdir(exist_ok=True)
    W, H = round(148 / 25.4 * dpi), round(210 / 25.4 * dpi)
    a = {}
    a["cover_bg"] = ASSETS / "cover_bg.jpg"
    art.field_image(W, H, int(H * 0.705), bolt=True, bolt_from=int(H * 0.47), seed=5).save(a["cover_bg"], quality=90)
    a["part_bg"] = ASSETS / "part_bg.jpg"
    art.field_image(W, H, int(H * 0.60), seed=8).save(a["part_bg"], quality=90)
    a["part_light"] = ASSETS / "part_light.png"
    pw, ph = round(110 / 25.4 * dpi), round(62 / 25.4 * dpi)
    art.field_image(pw, ph, int(ph * 0.22), dark=False).save(a["part_light"])
    a["cells"] = svg_to_png(art.cells_mark(), 14, 2.4, ASSETS / "cells.png")
    a["break"] = svg_to_png(art.scene_break(), 30, 3, ASSETS / "break.png")
    a["sprout"] = svg_to_png(art.sprout_mark(), 28, 8.4, ASSETS / "sprout.png")

    # обкладинка, форзаци й задня обкладинка автора (sources/art/book/…), якщо вже є
    if (src := find_art("cover")):
        a["cover_bg"] = plate(src, ASSETS / "cover_ill.jpg", W, H, top=.5)
    if (src := find_art("map")):
        a["map"] = plate(src, ASSETS / "map.jpg", W, H, top=0)
    if (src := find_art("endpaper_back")):
        a["endpaper_back"] = plate(src, ASSETS / "endpaper_back.jpg", W, H, top=0)
    a["back_bg"] = ASSETS / "back_bg.jpg"
    if (src := find_art("back")):
        plate(src, a["back_bg"], W, H, top=.62)
    else:
        art.field_image(W, H, int(H * 0.74), seed=12).save(a["back_bg"], quality=90)
    return a


def labels():
    """Підписи поверх карти/форзаців: design/labels.json → {"map": [{"x": мм, "y": мм, "text": …, "size": pt, "style": …}]}"""
    import json
    f = ROOT / "design" / "labels.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def annotation():
    f = BOOK / "annotation.md"
    if not f.exists():
        return []
    return [ln.strip() for ln in f.read_text(encoding="utf-8").split("\n\n") if ln.strip() and not ln.startswith("#")]


def find_art(name):
    for ext in ("png", "jpg", "jpeg", "webp"):
        f = ILLU / f"{name}.{ext}"
        if f.exists():
            return f
    return None


def plate(src, out, W, H, top=.55):
    """Обрізає ілюстрацію під A5 і (top>0) затемнює верх, щоб на ній читалася назва."""
    import numpy as np
    from PIL import Image
    im = Image.open(src).convert("RGB")
    r = W / H
    w, h = im.size
    if w / h > r:
        nw = int(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((W, H), Image.LANCZOS)
    if top:
        arr = np.asarray(im).astype(np.float32)
        y = np.linspace(0, 1, H)[:, None, None]
        k = np.clip(1 - y / top, 0, 1) ** 1.3 * .82          # зверху темніше
        k = np.maximum(k, np.clip((y - .9) / .1, 0, 1) * .5)  # і трохи знизу
        night = np.array(art._hex(NIGHT), np.float32)
        im = Image.fromarray((arr * (1 - k) + night * k).astype(np.uint8))
    im.save(out, quality=90)
    return out


# ------------------------------------------------------------------ PDF ----

CSS = r"""
@font-face { font-family: Text; src: url(FONTS/EBGaramond-400.ttf); }
@font-face { font-family: Text; font-style: italic; src: url(FONTS/EBGaramond-400i.ttf); }
@font-face { font-family: Text; font-weight: 600; src: url(FONTS/EBGaramond-600.ttf); }
@font-face { font-family: Disp; src: url(FONTS/CormorantGaramond-400.ttf); }
@font-face { font-family: Disp; font-weight: 500; src: url(FONTS/CormorantGaramond-500.ttf); }
@font-face { font-family: Disp; font-weight: 600; src: url(FONTS/CormorantGaramond-600.ttf); }
@font-face { font-family: Disp; font-weight: 700; src: url(FONTS/CormorantGaramond-700.ttf); }
@font-face { font-family: Disp; font-style: italic; src: url(FONTS/CormorantGaramond-400i.ttf); }
@font-face { font-family: Disp; font-style: italic; font-weight: 500; src: url(FONTS/CormorantGaramond-500i.ttf); }

@page {
  size: 148mm 210mm;
  margin: 19mm 15mm 21mm 15mm;
  background: PAPER;
}
@page :left  { margin-left: 15mm; margin-right: 20mm;
  @top-left { content: string(book, first-except); font: 500 7.2pt Disp; letter-spacing: .32em; color: #8a8276; }
  @bottom-left { content: counter(page); font: 500 9.5pt Disp; color: #6d665c; padding-top: 4mm; } }
@page :right { margin-left: 20mm; margin-right: 15mm;
  @top-right { content: string(chap, first-except); font: italic 9pt Disp; color: #8a8276; }
  @bottom-right { content: counter(page); font: 500 9.5pt Disp; color: #6d665c; padding-top: 4mm; } }
@page cover { margin: 0; background: NIGHT;
  @top-left { content: none } @top-right { content: none } @bottom-left { content: none } @bottom-right { content: none } }
@page front { @top-left { content: none } @top-right { content: none } @bottom-left { content: none } @bottom-right { content: none } }
@page part  { margin: 0; background: NIGHT;
  @top-left { content: none } @top-right { content: none } @bottom-left { content: none } @bottom-right { content: none } }
@page :blank { @top-left { content: none } @top-right { content: none } @bottom-left { content: none } @bottom-right { content: none } }

html { font-family: Text; font-size: 10.6pt; line-height: 1.42; color: INK; hyphens: auto; }
body { margin: 0; }

/* обкладинка: поле, блискавка, назва */
.cover { page: cover; position: relative; width: 148mm; height: 210mm; overflow: hidden; color: IVORY; text-align: center; }
.cover .bg { position: absolute; left: 0; top: 0; width: 148mm; height: 210mm; }
.cover .author { position: absolute; top: 19mm; left: 0; right: 0; font: 500 9.5pt Disp; letter-spacing: .42em; color: #b6ad9d; }
.cover .t { position: absolute; top: 37mm; left: 0; right: 0; font: 600 41pt Disp; letter-spacing: .16em; margin-right: -.16em; line-height: 1; }
.cover .rule { position: absolute; top: 59mm; left: 64mm; width: 20mm; height: .7pt; background: CRIMSON_LIGHT; }
.cover .act { position: absolute; top: 64mm; left: 0; right: 0; font: 500 8.5pt Disp; letter-spacing: .46em; color: #b6ad9d; }
.cover .s { position: absolute; top: 70mm; left: 0; right: 0; font: italic 500 19pt Disp; }

.front { page: front; break-before: page; text-align: center; }
.halftitle { padding-top: 64mm; }
.halftitle .t { font: 500 20pt Disp; letter-spacing: .3em; margin-right: -.3em; }
.halftitle .m { width: 14mm; height: 2.4mm; margin: 6mm auto 0; }

.titlepage { break-before: right; padding-top: 20mm; }
.titlepage .author { font: 500 10.5pt Disp; letter-spacing: .36em; color: #4b463f; margin-right: -.36em; }
.titlepage .t { font: 600 37pt Disp; letter-spacing: .15em; margin: 40mm -.15em 0 0; line-height: 1; }
.titlepage .rule { width: 20mm; height: .6pt; background: ACCENT; margin: 7mm auto 6mm; }
.titlepage .act { font: 500 9.5pt Disp; letter-spacing: .36em; color: #4b463f; margin-right: -.36em; }
.titlepage .s { font: italic 500 20pt Disp; margin-top: 2mm; }
.titlepage .m { width: 16mm; height: 2.8mm; margin: 44mm auto 0; }

.colophon { text-align: left; padding-top: 132mm; font-size: 8.4pt; line-height: 1.5; color: #5a544b; hyphens: manual; }
.colophon p { margin: 0 0 2.2mm; text-indent: 0; text-align: left; }

.epigraph { padding-top: 72mm; padding-left: 24mm; text-align: left; }
.epigraph p { font: italic 16pt Disp; line-height: 1.3; margin: 0; text-indent: 0; }
.epigraph .m { width: 12mm; height: 2mm; margin: 5mm 0 0; }

.toc { page: front; break-before: right; }
.toc h2 { font: 500 10.5pt Disp; letter-spacing: .4em; text-align: center; margin: 4mm -.4em 4mm 0; color: #3a362f; }
.toc .m { width: 12mm; height: 2mm; margin: 0 auto 7mm; }
.toc ul { list-style: none; padding: 0; margin: 0; }
.toc li { font-size: 9.6pt; line-height: 1.2; margin: 0 0 1.2mm; }
.toc li.tpart { font: 500 7.6pt Disp; letter-spacing: .22em; color: ACCENT; margin: 3.4mm 0 1.2mm; text-transform: uppercase; }
.toc li.tpart em { font: italic 500 10.5pt Disp; letter-spacing: 0; text-transform: none; color: #3a362f; }
.toc a { color: inherit; text-decoration: none; }
.toc a::after { content: leader('.') target-counter(attr(href url), page); color: #6d665c; font-family: Disp; font-weight: 500; }
.toc .lab { color: #8a8276; font: 500 8.6pt Disp; display: inline-block; width: 18mm; }

/* сторінка частини: ніч, поле до обрію */
.partpage { page: part; break-before: right; position: relative; width: 148mm; height: 210mm; overflow: hidden; color: IVORY; text-align: center; }
.partpage .bg { position: absolute; left: 0; top: 0; width: 148mm; height: 210mm; }
.partpage .lab { position: absolute; top: 58mm; left: 0; right: 0; font: 500 8.6pt Disp; letter-spacing: .46em; color: #c0574f; text-transform: uppercase; margin-right: -.46em; }
.partpage h1 { position: absolute; top: 66mm; left: 10mm; right: 10mm; font: 500 32pt Disp; margin: 0; line-height: 1.1; }
.partpage .num { position: absolute; top: 30mm; left: 0; right: 0; font: 600 12pt Disp; color: #6f675d; letter-spacing: .3em; }

.chapter { page: chapter; break-before: page; }
.chapter header { padding-top: 22mm; margin-bottom: 12mm; text-align: center; }
.chapter header .lab { font: 500 8.4pt Disp; letter-spacing: .4em; text-transform: uppercase; color: ACCENT; margin-right: -.4em; }
.chapter header h2 { font: 500 23pt Disp; line-height: 1.12; margin: 4mm 0 0; string-set: chap content(), book "ЧИСТИЛИЩЕ"; }
.chapter header .m { width: 11mm; height: 1.9mm; margin: 6mm auto 0; }

p { margin: 0; text-indent: 1.5em; text-align: justify; orphans: 2; widows: 2; }
p.noind { text-indent: 0; }
.dc { float: left; font-family: Disp; font-weight: 600; font-size: 56pt; line-height: 44pt; height: 44pt; margin: 3pt 4pt 0 -1pt; color: ACCENT; }
em { font-style: italic; }
.brk { width: 26mm; height: 2.6mm; margin: 4.4mm auto; break-after: avoid; }
.brk svg, .m svg { display: block; }

/* форзаци й задня обкладинка */
.endpaper, .backcover { page: cover; break-before: page; position: relative; width: 148mm; height: 210mm; overflow: hidden; }
.endpaper img.bg, .backcover img.bg { position: absolute; left: 0; top: 0; width: 148mm; height: 210mm; }
.endpaper .lbl { position: absolute; transform: translate(-50%, -50%); white-space: nowrap; color: IVORY; font-family: Disp; font-weight: 500; }
.endpaper .lbl.caps { text-transform: uppercase; letter-spacing: .28em; }
.endpaper .lbl.italic { font-style: italic; }
.endpaper .lbl.crimson { color: #d0645b; }
.backcover { color: IVORY; }
.backcover .blurb { position: absolute; top: 30mm; left: 22mm; right: 22mm; }
.backcover .blurb p { font: 10.4pt/1.5 Text; text-indent: 0; margin: 0 0 3.4mm; text-align: left; hyphens: manual; color: #e4dccb; }
.backcover .blurb p:first-child::first-letter { font: 600 15pt Disp; color: #d0645b; }
.backcover .blurb p:last-child { font: italic 500 12pt/1.35 Disp; color: #c9c0ae; margin-top: 5mm; }
.backcover .m { position: absolute; top: 24mm; left: 67mm; width: 14mm; height: 2.4mm; }
.backcover .bt { position: absolute; top: 138mm; left: 0; right: 0; text-align: center; font: 500 7.6pt Disp; letter-spacing: .4em; color: #8f877a; }
.end { break-before: page; text-align: center; padding-top: 66mm; page: front; }
.end .m { width: 28mm; height: 8.4mm; margin: 0 auto; }
.end .t { font: 500 8.6pt Disp; letter-spacing: .4em; color: #4b463f; margin: 7mm -.4em 0 0; text-transform: uppercase; }
.end .s { font: italic 500 15pt Disp; color: #3a362f; margin-top: 2mm; }
"""

PART_NUM = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def para_html(text):
    return "".join(f"<em>{html.escape(t)}</em>" if it else html.escape(t) for t, it in runs(typo(text)))


def build_html(items, assets):
    css = (CSS.replace("FONTS/", FONTS.as_uri() + "/").replace("CRIMSON_LIGHT", art.CRIMSON_LIGHT)
           .replace("ACCENT", ACCENT).replace("PAPER", PAPER)
           .replace("NIGHT", NIGHT).replace("IVORY", IVORY).replace("INK", INK))
    cells = f'<div class="m">{art.cells_mark()}</div>'
    brk = f'<div class="brk">{art.scene_break()}</div>'
    h = [f'<!doctype html><html lang="uk"><head><meta charset="utf-8"><title>{TITLE}. {ACT}. {SUBTITLE}</title>',
         f'<meta name="author" content="{AUTHOR}"><style>{css}</style></head><body>']
    h.append(f'''<section class="cover"><img class="bg" src="{assets["cover_bg"].as_uri()}">
      <div class="author">{AUTHOR.upper()}</div><div class="t">{TITLE.upper()}</div><div class="rule"></div>
      <div class="act">{ACT.upper()}</div><div class="s">{SUBTITLE}</div></section>''')
    if "map" in assets:
        h.append(endpaper_html(assets["map"], labels().get("map", [])))
    h.append(f'<section class="front halftitle" style="break-before: right"><div class="t">{TITLE.upper()}</div>{cells}</section>')
    h.append(f'''<section class="front titlepage"><div class="author">{AUTHOR.upper()}</div>
      <div class="t">{TITLE.upper()}</div><div class="rule"></div>
      <div class="act">{ACT.upper()}</div><div class="s">{SUBTITLE}</div>
      <div class="m">{art.cells_mark()}</div></section>''')
    h.append(f'''<section class="front colophon">
      <p>{AUTHOR}. {TITLE}. {ACT}: {SUBTITLE}.</p>
      <p>Книга у всесвіті гри «{TITLE}».</p>
      <p>Набрано шрифтами EB Garamond і Cormorant Garamond.</p>
      <p>© {AUTHOR}. Усі права застережено.</p></section>''')
    h.append(f'<section class="front epigraph" style="break-before: right"><p>Ми стали пам’яттю.</p>{cells}</section>')

    h.append(f'<section class="toc"><h2>ЗМІСТ</h2>{cells}<ul>')
    for it in items:
        if it["kind"] == "part":
            h.append(f'<li class="tpart">{html.escape(it["label"])} · <em>{html.escape(typo(it["name"]))}</em></li>')
        else:
            lab = it["label"].replace("Розділ ", "")
            h.append(f'<li><a href="#{it["id"]}"><span class="lab">{html.escape(lab)}</span>{html.escape(typo(it["name"]))}</a></li>')
    h.append("</ul></section>")

    pn = 0
    for it in items:
        if it["kind"] == "part":
            h.append(f'<section class="partpage"><img class="bg" src="{assets["part_bg"].as_uri()}">'
                     f'<div class="num">{PART_NUM[pn]}</div>'
                     f'<div class="lab">{html.escape(it["label"])}</div><h1>{html.escape(typo(it["name"]))}</h1></section>')
            pn += 1
            continue
        h.append(f'<section class="chapter" id="{it["id"]}">'
                 f'<header><div class="lab">{html.escape(it["label"])}</div>'
                 f'<h2>{html.escape(typo(it["name"]))}</h2>{cells}</header>')
        first = True
        for b in it["blocks"]:
            if b is None:
                h.append(brk)
                first = True
                continue
            cls = ""
            if first:
                cls = "noind"
                if b is it["blocks"][0] and b[0].isalpha():
                    cls = "noind drop"
                first = False
            body = para_html(b)
            if "drop" in cls:
                body = f'<span class="dc">{body[0]}</span>{body[1:]}'
            h.append(f'<p class="{cls}">{body}</p>' if cls else f"<p>{body}</p>")
        h.append("</section>")
    h.append(f'<section class="end"><div class="m">{art.sprout_mark()}</div><div class="t">Далі — акт другий</div>'
             f'<div class="s">Напівмертвий загін</div></section>')
    if "endpaper_back" in assets:
        h.append(endpaper_html(assets["endpaper_back"], labels().get("endpaper_back", [])))
    blurb = "".join(f"<p>{para_html(x)}</p>" for x in annotation())
    h.append(f'<section class="backcover"><img class="bg" src="{assets["back_bg"].as_uri()}">'
             f'<div class="m">{art.cells_mark(color=IVORY)}</div><div class="blurb">{blurb}</div>'
             f'<div class="bt">{AUTHOR.upper()} · {TITLE.upper()}</div></section>')
    h.append("</body></html>")
    return "\n".join(h)


def endpaper_html(img, lbls):
    out = [f'<section class="endpaper"><img class="bg" src="{img.as_uri()}">']
    for l in lbls:
        cls = " ".join(l.get("style", "").split())
        out.append(f'<div class="lbl {cls}" style="left:{l["x"]}mm; top:{l["y"]}mm; font-size:{l.get("size", 9)}pt">'
                   f'{html.escape(typo(l["text"]))}</div>')
    out.append("</section>")
    return "".join(out)


def build_pdf(items, assets, path):
    from weasyprint import HTML
    HTML(string=build_html(items, assets), base_url=str(ROOT)).write_pdf(path)


def page_jpg(pdf, page, path, dpi=250):
    """Сторінка PDF → JPEG: обкладинки й форзаци для DOCX (з усім текстом поверх)."""
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi), "-jpeg", "-jpegopt", "quality=92",
                    "-singlefile", str(pdf), str(path.with_suffix(""))], check=True)
    return path


def pdf_pages(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))


# ----------------------------------------------------------------- DOCX ----

def build_docx(items, pages_img, assets, path, toc_pages=None):
    from docx import Document
    from docx.enum.section import WD_SECTION
    from docx.enum.style import WD_STYLE_TYPE
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt, RGBColor, Emu

    TEXT, DISP = "EB Garamond", "Cormorant Garamond"
    accent = RGBColor.from_string(ACCENT[1:])
    grey = RGBColor.from_string("6D665C")
    ink = RGBColor.from_string(INK[1:])

    doc = Document()
    st = doc.styles

    def set_font(style_or_run, name, size=None, italic=None, bold=None, color=None):
        f = style_or_run.font
        f.name = name
        rpr = style_or_run.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), name)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        if size: f.size = Pt(size)
        if italic is not None: f.italic = italic
        if bold is not None: f.bold = bold
        if color is not None: f.color.rgb = color

    def spacing(el, pt):
        rpr = el.get_or_add_rPr()
        sp = OxmlElement("w:spacing"); sp.set(qn("w:val"), str(int(pt * 20))); rpr.append(sp)

    normal = st["Normal"]
    set_font(normal, TEXT, 11, color=ink)
    pf = normal.paragraph_format
    pf.space_before = Pt(0); pf.space_after = Pt(0)
    pf.line_spacing = 1.18
    pf.first_line_indent = Mm(5.5)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.widow_control = True
    # мова — для перенесень і перевірки правопису
    lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "uk-UA"); normal.element.get_or_add_rPr().append(lang)

    def pstyle(name, base="Normal", font_name=DISP, size=11, italic=False, bold=False, color=None,
               align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=0, indent=0, letter=0, caps=False, keep=True, outline=None):
        s = st[name] if name in [x.name for x in st] else st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = st[base]
        set_font(s, font_name, size, italic, bold, color)
        if letter: spacing(s.element, letter)
        if caps: s.font.all_caps = True
        p = s.paragraph_format
        p.alignment = align; p.space_before = Pt(before); p.space_after = Pt(after)
        p.first_line_indent = Mm(indent); p.keep_with_next = keep
        p.line_spacing = 1.0
        if outline is not None:
            ppr = s.element.get_or_add_pPr()
            ol = OxmlElement("w:outlineLvl"); ol.set(qn("w:val"), str(outline)); ppr.append(ol)
        return s

    pstyle("Body First", indent=0, font_name=TEXT, size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, keep=False).paragraph_format.line_spacing = 1.18
    pstyle("Scene Break", size=12, color=accent, before=7, after=7, letter=6)
    pstyle("Chapter Label", size=8.5, color=accent, before=60, after=6, letter=3, caps=True)
    h2 = pstyle("Heading 2", size=24, bold=False, color=ink, after=8, outline=1)
    h2.font.italic = False
    pstyle("Chapter Rule", size=10, color=RGBColor.from_string("B8AFA1"), after=26)
    pstyle("Part Label", size=9, color=accent, before=150, after=10, letter=4, caps=True)
    pstyle("Heading 1", size=32, color=ink, after=20, outline=0)
    pstyle("Ornament", size=16, color=accent)
    pstyle("Front Title", size=36, bold=True, letter=5, before=90, caps=True)
    pstyle("Front Small", size=10, letter=3, color=RGBColor.from_string("4B463F"), caps=True)
    pstyle("Front Sub", size=20, italic=True, before=4)
    pstyle("Colophon", font_name=TEXT, size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT, after=4, color=RGBColor.from_string("5A544B"), keep=False)
    pstyle("Epigraph", size=15, italic=True, before=200, align=WD_ALIGN_PARAGRAPH.LEFT, indent=0)
    pstyle("TOC Heading", size=11, letter=4, before=30, after=30, color=RGBColor.from_string("3A362F"), caps=True)
    pstyle("TOC Part", size=8, letter=2, color=accent, before=12, after=1, align=WD_ALIGN_PARAGRAPH.LEFT, caps=True)
    pstyle("Header Text", size=8, letter=1.5, color=RGBColor.from_string("8A8276"))
    pstyle("Footer Text", size=10, color=grey)
    for lvl, nm in ((1, "TOC 1"), (2, "TOC 2")):
        s = pstyle(nm, font_name=TEXT if lvl == 2 else DISP, size=10 if lvl == 2 else 10.5,
                   italic=(lvl == 1), align=WD_ALIGN_PARAGRAPH.LEFT, after=2 if lvl == 2 else 3, keep=False)
        ppr = s.element.get_or_add_pPr()
        tabs = OxmlElement("w:tabs"); tab = OxmlElement("w:tab")
        tab.set(qn("w:val"), "right"); tab.set(qn("w:leader"), "dot"); tab.set(qn("w:pos"), str(int(108 / 25.4 * 1440)))
        tabs.append(tab); ppr.append(tabs)

    # --- сторінка A5 з дзеркальними полями
    def page_setup(sec, cover=False):
        sec.page_width, sec.page_height = Mm(148), Mm(210)
        if cover:
            sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Mm(0)
            sec.header_distance = sec.footer_distance = Mm(0)
        else:
            sec.top_margin, sec.bottom_margin = Mm(19), Mm(21)
            sec.left_margin, sec.right_margin = Mm(20), Mm(15)   # при дзеркальних — внутрішнє / зовнішнє
            sec.header_distance, sec.footer_distance = Mm(9), Mm(10)

    def field(par, instr, cached=""):
        def r(tag, **attrs):
            run = OxmlElement("w:r")
            el = OxmlElement(tag)
            for k, v in attrs.items(): el.set(qn(k), v)
            run.append(el); par._p.append(run); return el
        r("w:fldChar", **{"w:fldCharType": "begin"})
        it = r("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {instr} "
        r("w:fldChar", **{"w:fldCharType": "separate"})
        par.add_run(cached)
        r("w:fldChar", **{"w:fldCharType": "end"})

    def headers(sec, title=None, numbers=True, first_blank=True):
        sec.header.is_linked_to_previous = False
        sec.footer.is_linked_to_previous = False
        sec.even_page_header.is_linked_to_previous = False
        sec.even_page_footer.is_linked_to_previous = False
        sec.first_page_header.is_linked_to_previous = False
        sec.first_page_footer.is_linked_to_previous = False
        sec.different_first_page_header_footer = first_blank
        for hdr, text in ((sec.header, title or ""), (sec.even_page_header, "ЧИСТИЛИЩЕ" if title else "")):
            p = hdr.paragraphs[0]; p.style = st["Header Text"]
            p.text = ""
            if text:
                run = p.add_run(text)
                run.italic = hdr is sec.header
                if hdr is sec.header: run.font.size = Pt(9.5)
        for ftr in (sec.footer, sec.even_page_footer, sec.first_page_footer):
            p = ftr.paragraphs[0]; p.style = st["Footer Text"]; p.text = ""
            if numbers:
                field(p, "PAGE", "")
        for hdr in (sec.first_page_header,):
            hdr.paragraphs[0].text = ""

    body = doc.sections[0]
    page_setup(body, cover=True)
    headers(body, numbers=False, first_blank=False)

    # --- обкладинка
    p = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
    p.style = st["Body First"]; p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_picture(str(pages_img["cover"]), width=Mm(148), height=Mm(209.6))

    def new_section(start=WD_SECTION.NEW_PAGE):
        s = doc.add_section(start); page_setup(s); return s

    def full_page(img):
        s = doc.add_section(WD_SECTION.NEW_PAGE); page_setup(s, cover=True); headers(s, numbers=False, first_blank=False)
        fp = doc.add_paragraph(style="Body First"); fp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.paragraph_format.line_spacing = 1.0
        fp.add_run().add_picture(str(img), width=Mm(148), height=Mm(209.6))

    if "map" in pages_img:
        full_page(pages_img["map"])

    # --- титул
    s = new_section(WD_SECTION.ODD_PAGE); headers(s, numbers=False, first_blank=False)
    doc.add_paragraph(AUTHOR, style="Front Small").paragraph_format.space_before = Pt(40)
    doc.add_paragraph(TITLE, style="Front Title")
    doc.add_paragraph("—", style="Ornament").runs[0].font.size = Pt(12)
    doc.add_paragraph(ACT, style="Front Small")
    doc.add_paragraph(SUBTITLE, style="Front Sub")
    o = doc.add_paragraph(style="Ornament"); o.paragraph_format.space_before = Pt(120)
    o.add_run().add_picture(str(assets["cells"]), width=Mm(16))
    s = new_section(); headers(s, numbers=False, first_blank=False)
    c = doc.add_paragraph(f"{AUTHOR}. {TITLE}. {ACT}: {SUBTITLE}.", style="Colophon")
    c.paragraph_format.space_before = Pt(360)
    doc.add_paragraph(f"Книга у всесвіті гри «{TITLE}».", style="Colophon")
    doc.add_paragraph("Набрано шрифтами EB Garamond і Cormorant Garamond.", style="Colophon")
    doc.add_paragraph(f"© {AUTHOR}. Усі права застережено.", style="Colophon")
    s = new_section(WD_SECTION.ODD_PAGE); headers(s, numbers=False, first_blank=False)
    ep = doc.add_paragraph("Ми стали пам’яттю.", style="Epigraph"); ep.paragraph_format.left_indent = Mm(26)

    # --- зміст (поле TOC з готовими рядками; Word оновить номери за F9)
    s = new_section(WD_SECTION.ODD_PAGE); headers(s, numbers=False, first_blank=False)
    doc.add_paragraph("Зміст", style="TOC Heading")
    toc_pages = toc_pages or {}
    first_entry = True
    for it in items:
        if it["kind"] == "part":
            par = doc.add_paragraph(style="TOC 1")
            par.paragraph_format.space_before = Pt(9)
            text = f'{it["label"]}. {typo(it["name"])}'
            key = it["label"]
        else:
            par = doc.add_paragraph(style="TOC 2")
            text = f'{it["label"]}. {typo(it["name"])}' if it["label"] == "Пролог" else f'{it["label"]}. {typo(it["name"])}'
            key = it["id"]
        if first_entry:
            for tag, val in (("begin", None), ("instr", None), ("separate", None)):
                run = OxmlElement("w:r")
                if tag == "instr":
                    el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = ' TOC \\o "1-2" \\h \\z '
                else:
                    el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag)
                run.append(el); par._p.append(run)
            first_entry = False
        par.add_run(text)
        par.add_run("\t" + str(toc_pages.get(key, "")))
        last = par
    run = OxmlElement("w:r"); el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), "end"); run.append(el); last._p.append(run)

    # --- текст
    pn = 0
    for it in items:
        if it["kind"] == "part":
            pn += 1
            s = new_section(WD_SECTION.ODD_PAGE); headers(s, numbers=False, first_blank=False)
            doc.add_paragraph(it["label"], style="Part Label")
            doc.add_paragraph(typo(it["name"]), style="Heading 1")
            o = doc.add_paragraph(style="Ornament"); o.paragraph_format.space_before = Pt(36)
            o.add_run().add_picture(str(assets["part_light"]), width=Mm(110))
            continue
        s = new_section(); headers(s, title=typo(it["name"]))
        doc.add_paragraph(it["label"], style="Chapter Label")
        doc.add_paragraph(typo(it["name"]), style="Heading 2")
        cr = doc.add_paragraph(style="Chapter Rule")
        cr.add_run().add_picture(str(assets["cells"]), width=Mm(11))
        first = True
        for b in it["blocks"]:
            if b is None:
                sb = doc.add_paragraph(style="Scene Break")
                sb.add_run().add_picture(str(assets["break"]), width=Mm(26))
                first = True
                continue
            par = doc.add_paragraph(style="Body First" if first else "Normal")
            rr = runs(typo(b, short_words=False))
            if first and b is it["blocks"][0] and b[0].isalpha():
                # ініціал: перша літера більша й червона, решта першого слова — капітеллю
                word, rest = re.match(r"(\S+)(.*)", rr[0][0], re.S).groups()
                rr[0] = (rest, rr[0][1])
                r = par.add_run(word[0]); set_font(r, DISP, 26, bold=True, color=accent)
                if len(word) > 1:
                    r = par.add_run(word[1:]); r.font.small_caps = True; spacing(r.element, 0.6)
            first = False
            for t, ital in rr:
                if t:
                    r = par.add_run(t)
                    if ital: r.italic = True

    s = new_section(); headers(s, numbers=False, first_blank=False)
    o = doc.add_paragraph(style="Ornament"); o.paragraph_format.space_before = Pt(180)
    o.add_run().add_picture(str(assets["sprout"]), width=Mm(28))
    e = doc.add_paragraph("Далі — акт другий", style="Front Small"); e.paragraph_format.space_before = Pt(14)
    doc.add_paragraph("Напівмертвий загін", style="Front Sub").runs[0].font.size = Pt(13)
    if "endpaper_back" in pages_img:
        full_page(pages_img["endpaper_back"])
    full_page(pages_img["back"])

    # --- налаштування документа: дзеркальні поля, парні/непарні колонтитули, вбудовані шрифти
    settings = doc.settings.element
    for tag in ("w:mirrorMargins", "w:evenAndOddHeaders", "w:embedTrueTypeFonts", "w:saveSubsetFonts", "w:autoHyphenation"):
        el = OxmlElement(tag)
        settings.insert(0, el)
    cp = doc.core_properties
    cp.title = f"{TITLE}. {ACT}. {SUBTITLE}"
    cp.author = AUTHOR
    cp.language = "uk-UA"
    doc.save(path)
    embed_fonts(path, {
        TEXT: {"Regular": "EBGaramond-400.ttf", "Italic": "EBGaramond-400i.ttf", "Bold": "EBGaramond-600.ttf"},
        DISP: {"Regular": "CormorantGaramond-500.ttf", "Italic": "CormorantGaramond-500i.ttf", "Bold": "CormorantGaramond-700.ttf"},
    })


def embed_fonts(docx_path, families):
    """Вбудовує TTF у DOCX (обфускація за ECMA-376 §17.8.1), щоб Word показував ті самі шрифти."""
    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    tmp = Path(str(docx_path) + ".tmp")
    zin = zipfile.ZipFile(docx_path)
    files = {n: zin.read(n) for n in zin.namelist()}
    zin.close()
    font_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                f'<w:fonts xmlns:w="{W}" xmlns:r="{R}">']
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    n = 0
    for fam, faces in families.items():
        font_xml.append(f'<w:font w:name="{fam}"><w:charset w:val="CC"/><w:family w:val="roman"/><w:pitch w:val="variable"/>')
        for face, fn in faces.items():
            n += 1
            guid = str(uuid.uuid4()).upper()
            key = guid.replace("-", "")
            kb = bytes(int(key[30 - 2 * i: 32 - 2 * i], 16) for i in range(16))
            data = bytearray((FONTS / fn).read_bytes())
            for i in range(32):
                data[i] ^= kb[i % 16]
            files[f"word/fonts/font{n}.odttf"] = bytes(data)
            font_xml.append(f'<w:embed{face} r:id="rIdF{n}" w:fontKey="{{{guid}}}"/>')
            rels.append(f'<Relationship Id="rIdF{n}" Type="{R}/font" Target="fonts/font{n}.odttf"/>')
        font_xml.append("</w:font>")
    for fam in ("Calibri", "Times New Roman"):
        font_xml.append(f'<w:font w:name="{fam}"/>')
    font_xml.append("</w:fonts>")
    rels.append("</Relationships>")
    files["word/fontTable.xml"] = "".join(font_xml).encode()
    files["word/_rels/fontTable.xml.rels"] = "".join(rels).encode()
    ct = files["[Content_Types].xml"].decode()
    if 'Extension="odttf"' not in ct:
        ct = ct.replace("<Default ", '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/><Default ', 1)
    files["[Content_Types].xml"] = ct.encode()
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ["[Content_Types].xml"] + [x for x in files if x != "[Content_Types].xml"]:
            z.writestr(name, files[name])
    tmp.replace(docx_path)


def docx_toc_pages(docx_path, items):
    """Рендерить DOCX через LibreOffice і шукає, на якій сторінці починається кожен розділ."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or not shutil.which("pdftotext"):
        return None
    with tempfile.TemporaryDirectory() as td:
        env = dict(os.environ, HOME=td)
        # шрифти мають бути видимі LibreOffice
        fdir = Path(td) / ".fonts"; fdir.mkdir()
        for f in FONTS.glob("*.ttf"):
            shutil.copy(f, fdir)
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", td, str(docx_path)],
                       check=True, env=env, capture_output=True, timeout=600)
        pdf = Path(td) / (Path(docx_path).stem + ".pdf")
        txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
        shutil.copy(pdf, BUILD / ".docx_preview.pdf")
    pages = txt.split("\f")
    # друкований номер сторінки — останнє число на сторінці (колонтитул); LibreOffice
    # може пропускати порожні сторінки, тож індекс у PDF не завжди дорівнює номеру
    printed = []
    for pg in pages:
        tail = [ln.strip() for ln in pg.strip().splitlines()[-2:]]
        nums = [int(t) for t in tail if t.isdigit()]
        printed.append(nums[-1] if nums else None)

    def number(i):
        for j in range(i, min(i + 4, len(pages))):
            if printed[j] is not None:
                return printed[j] - (j - i)
        return i + 1

    res, start = {}, 0
    norm = lambda s: re.sub(r"\s+", "", s).lower()
    for it in items:
        label = norm(it["label"])
        name = norm(typo(it["name"]))
        for i in range(start, len(pages)):
            pg = norm(pages[i])
            if i >= 5 and label in pg[:120] and name[:15] in pg[:200]:
                res[it["label"] if it["kind"] == "part" else it["id"]] = number(i)
                start = i
                break
    return res


def main():
    OUT.mkdir(exist_ok=True)
    items = parse()
    assets = make_assets()
    pdf = OUT / f"{BASENAME}.pdf"
    build_pdf(items, assets, pdf)
    print("PDF:", pdf)
    n = pdf_pages(pdf)
    imgs = {"cover": page_jpg(pdf, 1, OUT / f"{BASENAME}_cover.jpg"),
            "back": page_jpg(pdf, n, OUT / f"{BASENAME}_back.jpg")}
    if "map" in assets:
        imgs["map"] = page_jpg(pdf, 2, ASSETS / "map_page.jpg")
    if "endpaper_back" in assets:
        imgs["endpaper_back"] = page_jpg(pdf, n - 1, ASSETS / "endpaper_back_page.jpg")
    docx = OUT / f"{BASENAME}.docx"
    build_docx(items, imgs, assets, docx)
    pages = docx_toc_pages(docx, items)
    if pages:
        build_docx(items, imgs, assets, docx, pages)
        print("DOCX TOC pages:", pages)
    print("DOCX:", docx)


if __name__ == "__main__":
    main()
