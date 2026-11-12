"""Оформлення книги: векторні мотиви у SVG.

Мотив — Клітинні поля: чорно-біла шахова дошка до обрію, червона блискавка
й зелений паросток (зелений — колір сили творення). Усі розміри — у десятих
частках міліметра (viewBox), тож 1480×2100 = сторінка A5.
"""
import math
import random

NIGHT = "#0b0b0d"
INK = "#1a1918"
CRIMSON = "#8e1b1f"
CRIMSON_LIGHT = "#c0392f"
SPROUT = "#6f9a4a"
IVORY = "#ece4d3"


def _pts(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def checker_floor(W, H, horizon, *, square, opacity=1.0, cells_bottom=7, focal=0.9, max_rows=90):
    """Шахова підлога в перспективі від нижнього краю до обрію: лише «темні» клітинки."""
    cx = W / 2
    hb = H - horizon
    F = W * focal
    s = W / (cells_bottom * hb)          # розмір клітинки у світі (висота камери = 1)
    z0 = F / hb
    polys = []
    for i in range(max_rows):
        za, zb = z0 + i * s, z0 + (i + 1) * s
        ya, yb = horizon + F / za, horizon + F / zb
        if ya - yb < 0.25:
            break
        xmax = (W / 2 + 10) * zb / F
        j0, j1 = math.floor(-xmax / s) - 1, math.ceil(xmax / s) + 1
        for j in range(j0, j1):
            if (i + j) % 2:
                continue
            X0, X1 = j * s, (j + 1) * s
            polys.append([(cx + F * X0 / za, ya), (cx + F * X1 / za, ya),
                          (cx + F * X1 / zb, yb), (cx + F * X0 / zb, yb)])
    body = "".join(f'<polygon points="{_pts(p)}"/>' for p in polys)
    return f'<g fill="{square}" fill-opacity="{opacity}">{body}</g>'


def lightning(x0, y0, x1, y1, seed=3, segments=16, spread=55):
    rnd = random.Random(seed)
    pts = [(x0, y0)]
    for k in range(1, segments):
        t = k / segments
        x = x0 + (x1 - x0) * t + rnd.uniform(-spread, spread) * (1 - t) ** 0.6
        y = y0 + (y1 - y0) * t + rnd.uniform(-8, 8)
        pts.append((x, y))
    pts.append((x1, y1))
    # одна гілка
    b0 = pts[segments // 3]
    branch = [b0]
    bx, by = b0
    for k in range(5):
        bx += rnd.uniform(12, 40) * (1 if seed % 2 else -1)
        by += rnd.uniform(25, 45)
        branch.append((bx, by))
    out = []
    for path, scale in ((pts, 1.0), (branch, 0.55)):
        d = _pts(path)
        out.append(f'<polyline points="{d}" fill="none" stroke="{CRIMSON}" stroke-opacity=".10" stroke-width="{26*scale}" stroke-linejoin="round" stroke-linecap="round"/>')
        out.append(f'<polyline points="{d}" fill="none" stroke="{CRIMSON_LIGHT}" stroke-opacity=".28" stroke-width="{11*scale}" stroke-linejoin="round" stroke-linecap="round"/>')
        out.append(f'<polyline points="{d}" fill="none" stroke="{CRIMSON_LIGHT}" stroke-width="{4.2*scale}" stroke-linejoin="round" stroke-linecap="round"/>')
        out.append(f'<polyline points="{d}" fill="none" stroke="#f6e2da" stroke-width="{1.4*scale}" stroke-linejoin="round" stroke-linecap="round"/>')
    return "".join(out)


def sprout(x, y, size=30, color=SPROUT):
    """Маленький паросток: стебло й два листки; (x, y) — точка, звідки росте."""
    s = size
    return (f'<g fill="{color}" stroke="none">'
            f'<path d="M{x:.1f},{y:.1f} C{x-1:.1f},{y-s*.45:.1f} {x+1:.1f},{y-s*.7:.1f} {x:.1f},{y-s*.9:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{s*.07:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x:.1f},{y-s*.62:.1f} C{x-s*.25:.1f},{y-s*.95:.1f} {x-s*.75:.1f},{y-s*.95:.1f} {x-s*.85:.1f},{y-s*.78:.1f} '
            f'C{x-s*.6:.1f},{y-s*.55:.1f} {x-s*.25:.1f},{y-s*.5:.1f} {x:.1f},{y-s*.62:.1f}Z"/>'
            f'<path d="M{x:.1f},{y-s*.8:.1f} C{x+s*.2:.1f},{y-s*1.1:.1f} {x+s*.65:.1f},{y-s*1.15:.1f} {x+s*.78:.1f},{y-s*1.0:.1f} '
            f'C{x+s*.55:.1f},{y-s*.75:.1f} {x+s*.22:.1f},{y-s*.7:.1f} {x:.1f},{y-s*.8:.1f}Z"/></g>')


def night_field(W, H, horizon, *, bolt=False, bolt_from=0, glow=True, seed=3, cells_bottom=7):
    """Нічне поле: небо, низькі хмари, шахова дошка, що тоне в темряві; за бажання — блискавка."""
    cx = W / 2
    rnd = random.Random(seed + 11)
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="none">',
         '<defs>',
         f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NIGHT}"/>'
         f'<stop offset="{horizon/H:.3f}" stop-color="#1a1a1e"/><stop offset="1" stop-color="{NIGHT}"/></linearGradient>',
         f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{NIGHT}" stop-opacity="1"/>'
         f'<stop offset=".35" stop-color="{NIGHT}" stop-opacity=".75"/>'
         f'<stop offset="1" stop-color="{NIGHT}" stop-opacity="0"/></linearGradient>',
         f'<linearGradient id="bottom" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{NIGHT}" stop-opacity="0"/><stop offset="1" stop-color="{NIGHT}" stop-opacity=".55"/></linearGradient>',
         f'<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CRIMSON_LIGHT}" stop-opacity=".45"/>'
         f'<stop offset=".4" stop-color="{CRIMSON}" stop-opacity=".18"/><stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></radialGradient>',
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # низькі нерухомі хмари
    for k in range(9):
        y = horizon - rnd.uniform(60, horizon * 0.75)
        w = rnd.uniform(W * 0.5, W * 1.2)
        g.append(f'<ellipse cx="{rnd.uniform(0, W):.0f}" cy="{y:.0f}" rx="{w/2:.0f}" ry="{rnd.uniform(14, 40):.0f}" '
                 f'fill="#d8d3c8" fill-opacity="{rnd.uniform(.015, .04):.3f}"/>')
    # підлога
    g.append(f'<rect y="{horizon}" width="{W}" height="{H-horizon}" fill="#121215"/>')
    g.append(checker_floor(W, H, horizon, square="#d9d4c8", opacity=0.82, cells_bottom=cells_bottom))
    g.append(f'<rect y="{horizon-1}" width="{W}" height="{(H-horizon)*0.62:.0f}" fill="url(#fade)"/>')
    g.append(f'<rect y="{horizon + (H-horizon)*0.5:.0f}" width="{W}" height="{(H-horizon)*0.5+1:.0f}" fill="url(#bottom)"/>')
    g.append(f'<line x1="0" y1="{horizon}" x2="{W}" y2="{horizon}" stroke="#d9d4c8" stroke-opacity=".12" stroke-width="1.2"/>')
    if bolt:
        if glow:
            g.append(f'<ellipse cx="{cx}" cy="{horizon}" rx="{W*0.32:.0f}" ry="{W*0.11:.0f}" fill="url(#glow)"/>')
        g.append(lightning(cx + 40, bolt_from, cx, horizon - 2, seed=seed))
        g.append(sprout(cx + 1, horizon + 1, size=34))
    g.append("</svg>")
    return "".join(g)


def light_field(W, H, horizon, cells_bottom=7):
    """Світлий варіант для білих сторінок DOCX: чорнильні клітинки тануть угору в білий."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" preserveAspectRatio="none">'
            f'<defs><linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset=".4" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="b" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset=".18" stop-color="#fff" stop-opacity="0"/><stop offset=".82" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="#fff"/>'
            + checker_floor(W, H, horizon, square=INK, opacity=0.9, cells_bottom=cells_bottom)
            + f'<rect y="{horizon-1}" width="{W}" height="{(H-horizon)*0.75:.0f}" fill="url(#f)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#b)"/>'
            + sprout(W / 2, horizon + 2, size=30) + '</svg>')


def cells_mark(color=INK, accent=CRIMSON, n=5, cell=22, gap=7):
    """Рядок клітинок під назвою розділу: ■ □ ■ □ ■, середня — червона."""
    W = n * cell + (n - 1) * gap
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 {W+4} {cell+4}" width="100%" height="100%">']
    for k in range(n):
        x = k * (cell + gap)
        if k == n // 2:
            out.append(f'<rect x="{x}" y="0" width="{cell}" height="{cell}" fill="{accent}"/>')
        elif k % 2 == 0:
            out.append(f'<rect x="{x}" y="0" width="{cell}" height="{cell}" fill="{color}" fill-opacity=".85"/>')
        else:
            out.append(f'<rect x="{x+1.5}" y="1.5" width="{cell-3}" height="{cell-3}" fill="none" stroke="{color}" stroke-width="3" stroke-opacity=".7"/>')
    out.append("</svg>")
    return "".join(out)


def scene_break(color=INK, accent=CRIMSON):
    """Розрив сцени: тонка лінія — три ромби (середній червоний) — тонка лінія."""
    W, H = 400, 40
    c = H / 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">',
           f'<line x1="40" y1="{c}" x2="140" y2="{c}" stroke="{color}" stroke-opacity=".35" stroke-width="2"/>',
           f'<line x1="260" y1="{c}" x2="360" y2="{c}" stroke="{color}" stroke-opacity=".35" stroke-width="2"/>']
    for k, x in enumerate((165, 200, 235)):
        d = 11 if k != 1 else 14
        pts = _pts([(x, c - d), (x + d, c), (x, c + d), (x - d, c)])
        if k == 1:
            out.append(f'<polygon points="{pts}" fill="{accent}"/>')
        else:
            out.append(f'<polygon points="{pts}" fill="none" stroke="{color}" stroke-opacity=".7" stroke-width="2.4"/>')
    out.append("</svg>")
    return "".join(out)


def sprout_mark(color=SPROUT, accent=CRIMSON):
    """Кінцівка: паросток на лінії обрію з червоною іскрою над ним."""
    W, H = 400, 120
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">'
            f'<line x1="60" y1="100" x2="340" y2="100" stroke="{INK}" stroke-opacity=".35" stroke-width="2"/>'
            + sprout(200, 100, size=78, color=color)
            + f'<polygon points="{_pts([(200, 4), (207, 14), (200, 24), (193, 14)])}" fill="{accent}"/></svg>')


# ------------------------------------------------------------ растр ----
# Фони малюються попіксельно (numpy): так перспектива точна, а переходи м'які.

def _hex(c):
    c = c.lstrip("#")
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def _bezier(p0, p1, p2, p3, n=24):
    out = []
    for k in range(n + 1):
        t = k / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def _draw_sprout(draw, x, y, s, color):
    draw.line(_bezier((x, y), (x - s * .03, y - s * .45), (x + s * .03, y - s * .7), (x, y - s * .9)), fill=color, width=max(2, int(s * .07)))
    left = _bezier((x, y - s * .62), (x - s * .25, y - s * .95), (x - s * .75, y - s * .95), (x - s * .85, y - s * .78)) + \
        _bezier((x - s * .85, y - s * .78), (x - s * .6, y - s * .55), (x - s * .25, y - s * .5), (x, y - s * .62))
    right = _bezier((x, y - s * .8), (x + s * .2, y - s * 1.1), (x + s * .65, y - s * 1.15), (x + s * .78, y - s * 1.0)) + \
        _bezier((x + s * .78, y - s * 1.0), (x + s * .55, y - s * .75), (x + s * .22, y - s * .7), (x, y - s * .8))
    draw.polygon(left, fill=color)
    draw.polygon(right, fill=color)


def field_image(W, H, horizon, *, dark=True, bolt=False, bolt_from=0, seed=3, cells_bottom=7, focal=0.9, ss=2):
    """Шахове поле до обрію (PIL Image). dark=True — нічна сторінка; False — чорнило на білому."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter

    w, h, hor = W * ss, H * ss, horizon * ss
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    bg = np.array(_hex(NIGHT) if dark else [255, 255, 255], np.float32)
    sq = np.array([217, 212, 200] if dark else _hex(INK), np.float32)
    floor_bg = np.array([18, 18, 21] if dark else [255, 255, 255], np.float32)

    img = np.empty((h, w, 3), np.float32)
    # небо
    t = np.clip(ys / max(hor, 1), 0, 1)[..., None]
    sky_top = bg
    sky_hor = np.array([30, 29, 34], np.float32) if dark else bg
    img[:] = sky_top * (1 - t ** 2.2) + sky_hor * t ** 2.2
    # підлога: z = F / (y - hor), X = (x - cx) * z / F
    F = w * focal
    hb = h - hor
    s = w / (cells_bottom * hb)
    below = ys > hor + 0.5
    dy = np.where(below, ys - hor, 1)
    z = F / dy
    X = (xs - w / 2) * z / F
    cell = (np.floor(X / s) + np.floor(z / s)) % 2 == 0
    floor = np.where(cell[..., None], sq, floor_bg)
    # далечінь сіріє (прибирає муар) і тоне в темряві/білому
    d = np.clip(dy / hb, 0, 1)[..., None]
    mean = (sq + floor_bg) / 2
    blur_k = np.clip(1 - d * 6, 0, 1) ** 1.5
    floor = floor * (1 - blur_k) + mean * blur_k
    fade = np.clip(d / (0.75 if dark else 0.75), 0, 1) ** (1.9 if dark else 1.0)
    edge = bg if dark else bg
    floor = edge * (1 - fade) + floor * fade
    if dark:
        floor = floor * (1 - 0.55 * d ** 1.6) + bg * 0.55 * d ** 1.6      # низ теж трохи тоне
    else:
        xf = np.abs(xs / w - .5)[..., None] * 2                       # боки тануть у білий
        k = np.clip((xf - .64) / .36, 0, 1) ** 1.4
        floor = floor * (1 - k) + bg * k
    img = np.where(below[..., None], floor, img)

    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")

    if dark:
        rnd = random.Random(seed + 11)
        clouds = Image.new("L", (w, h), 0)
        dc = ImageDraw.Draw(clouds)
        for _ in range(14):
            cy = hor - rnd.uniform(0.08, 0.8) * hor
            rx = rnd.uniform(.25, .7) * w
            ry = rnd.uniform(.012, .035) * h
            cx0 = rnd.uniform(0, w)
            dc.ellipse([cx0 - rx, cy - ry, cx0 + rx, cy + ry], fill=int(rnd.uniform(10, 26)))
        clouds = clouds.filter(ImageFilter.GaussianBlur(h * 0.012))
        im = Image.composite(Image.new("RGB", (w, h), (200, 196, 188)), im, clouds)

    if bolt:
        cx = w / 2
        # червоне сяйво в точці удару
        glow = Image.new("L", (w, h), 0)
        ImageDraw.Draw(glow).ellipse([cx - w * .34, hor - w * .09, cx + w * .34, hor + w * .09], fill=120)
        glow = glow.filter(ImageFilter.GaussianBlur(w * .06))
        im = Image.composite(Image.new("RGB", (w, h), tuple(_hex(CRIMSON_LIGHT))), im, glow)
        rnd = random.Random(seed)
        x0, y0, x1, y1 = cx + 40 * ss, bolt_from * ss, cx, hor
        segs = 18
        pts = [(x0, y0)]
        for k in range(1, segs):
            tt = k / segs
            pts.append((x0 + (x1 - x0) * tt + rnd.uniform(-1, 1) * 60 * ss * (1 - tt) ** .6,
                        y0 + (y1 - y0) * tt + rnd.uniform(-6, 6) * ss))
        pts.append((x1, y1))
        b = [pts[segs // 3]]
        for _ in range(6):
            b.append((b[-1][0] + rnd.uniform(10, 34) * ss, b[-1][1] + rnd.uniform(22, 40) * ss))
        for width, blur, col, alpha in ((40, 26, CRIMSON, 160), (14, 7, CRIMSON_LIGHT, 210), (6, 1.5, CRIMSON_LIGHT, 255), (2.2, 0, "#f7e6de", 255)):
            layer = Image.new("L", (w, h), 0)
            dl = ImageDraw.Draw(layer)
            dl.line(pts, fill=alpha, width=max(1, int(width * ss)), joint="curve")
            dl.line(b, fill=int(alpha * .8), width=max(1, int(width * ss * .5)), joint="curve")
            if blur:
                layer = layer.filter(ImageFilter.GaussianBlur(blur * ss))
            im = Image.composite(Image.new("RGB", (w, h), tuple(_hex(col))), im, layer)
        _draw_sprout(ImageDraw.Draw(im), cx + ss, hor + 2 * ss, 34 * ss, tuple(_hex(SPROUT)))
    elif not dark:
        _draw_sprout(ImageDraw.Draw(im), w / 2, hor + 0.16 * hb, 34 * ss, tuple(_hex(SPROUT)))

    return im.resize((W, H), Image.LANCZOS)
