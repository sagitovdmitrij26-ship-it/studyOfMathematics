# -*- coding: utf-8 -*-
"""Геометрия 5–6 класс: 70/80/100 задач и схемы SVG."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TASKS = ROOT / "public" / "tasks"
CLASS = "5–6 класс"

PALETTE = {
    "Базовый": ("#2f6b4f", "#e8f6ee", "#1c3d2e", "#3d9a6a"),
    "Средний": ("#8a6a12", "#fff6d6", "#4a3a08", "#d4a017"),
    "Высокий": ("#9a4a28", "#ffe8dc", "#4a2214", "#e07a4c"),
}


def item(q, ans, exp, kind, **params):
    return {"question": q, "answer": str(ans), "explanation": exp, "kind": kind, "params": params}


def escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def header(level: str, index: int, total: int) -> str:
    accent, paper, ink, _ = PALETTE[level]
    return f"""
  <rect width="960" height="540" rx="28" fill="{paper}"/>
  <rect x="28" y="28" width="904" height="484" rx="20" fill="#fffdf8" stroke="{accent}" stroke-width="3"/>
  <text x="56" y="72" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="700" fill="{ink}">Геометрия · 5–6 класс</text>
  <text x="900" y="72" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="18" fill="{accent}">{escape(level)} · {index}/{total}</text>
"""


def footer(accent: str) -> str:
    return f'<text x="480" y="492" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="16" fill="{accent}">Матеум · тренажёр</text>'


def wrap(svg_body: str, level: str, index: int, total: int) -> str:
    accent, _, _, _ = PALETTE[level]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">
{header(level, index, total)}
{svg_body}
{footer(accent)}
</svg>
"""


def rect_figure(a: int, b: int, fill: str, ink: str, unit: str = "см") -> str:
    max_side = 280
    scale = max_side / max(a, b)
    w, h = a * scale, b * scale
    x, y = 480 - w / 2, 290 - h / 2
    return f"""
  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="{fill}" fill-opacity="0.35" stroke="{ink}" stroke-width="4"/>
  <text x="480" y="{y - 16:.1f}" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{a} {unit}</text>
  <text x="{x + w + 18:.1f}" y="{y + h / 2:.1f}" font-size="22" fill="{ink}" font-family="Georgia, serif">{b} {unit}</text>
"""


def square_figure(a: int, fill: str, ink: str) -> str:
    return rect_figure(a, a, fill, ink)


def triangle_figure(base: int, height: int, fill: str, ink: str) -> str:
    w, h = 320, 220
    x1, y1 = 480 - w / 2, 360
    x2, y2 = 480 + w / 2, 360
    x3, y3 = 480, 360 - h
    return f"""
  <polygon points="{x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f} {x3:.0f},{y3:.0f}" fill="{fill}" fill-opacity="0.4" stroke="{ink}" stroke-width="4"/>
  <line x1="480" y1="{y3:.0f}" x2="480" y2="{y1:.0f}" stroke="{ink}" stroke-dasharray="7 6" stroke-width="2"/>
  <text x="480" y="392" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{base} см</text>
  <text x="498" y="270" font-size="22" fill="{ink}" font-family="Georgia, serif">h = {height} см</text>
"""


def right_triangle(a: int, b: int, c: int, fill: str, ink: str) -> str:
    w, h = 280, 200
    x, y = 340, 360
    return f"""
  <polygon points="{x},{y} {x + w},{y} {x},{y - h}" fill="{fill}" fill-opacity="0.4" stroke="{ink}" stroke-width="4"/>
  <rect x="{x}" y="{y - 22}" width="22" height="22" fill="none" stroke="{ink}" stroke-width="2"/>
  <text x="{x + w / 2:.0f}" y="{y + 32}" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{a} см</text>
  <text x="{x - 28}" y="{y - h / 2:.0f}" text-anchor="end" font-size="22" fill="{ink}" font-family="Georgia, serif">{b} см</text>
  <text x="{x + w / 2 + 30:.0f}" y="{y - h / 2:.0f}" font-size="22" fill="{ink}" font-family="Georgia, serif">{c} см</text>
"""


def cube_figure(a: int, fill: str, ink: str) -> str:
    s, dx, dy = 140, 50, 28
    x, y = 400, 200
    front = f"{x},{y + dy} {x + s},{y + dy} {x + s},{y + dy + s} {x},{y + dy + s}"
    top = f"{x},{y + dy} {x + dx},{y} {x + s + dx},{y} {x + s},{y + dy}"
    side = f"{x + s},{y + dy} {x + s + dx},{y} {x + s + dx},{y + s} {x + s},{y + dy + s}"
    return f"""
  <polygon points="{top}" fill="{fill}" fill-opacity="0.55" stroke="{ink}" stroke-width="3"/>
  <polygon points="{side}" fill="{fill}" fill-opacity="0.25" stroke="{ink}" stroke-width="3"/>
  <polygon points="{front}" fill="{fill}" fill-opacity="0.4" stroke="{ink}" stroke-width="3"/>
  <text x="{x + s / 2:.0f}" y="{y + dy + s + 36:.0f}" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{a} см</text>
"""


def circle_figure(r: int, fill: str, ink: str, show_d: bool = False) -> str:
    label = f"d = {2 * r} см" if show_d else f"r = {r} см"
    return f"""
  <circle cx="480" cy="300" r="110" fill="{fill}" fill-opacity="0.35" stroke="{ink}" stroke-width="4"/>
  <line x1="480" y1="300" x2="{480 + 110 if show_d else 590}" y2="300" stroke="{ink}" stroke-width="3"/>
  <circle cx="480" cy="300" r="5" fill="{ink}"/>
  <text x="480" y="440" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{label}</text>
"""


def angle_figure(deg: int, fill: str, ink: str) -> str:
    rad = math.radians(deg)
    x2, y2 = 480 + 180 * math.cos(rad), 360 - 180 * math.sin(rad)
    return f"""
  <line x1="300" y1="360" x2="700" y2="360" stroke="{ink}" stroke-width="4"/>
  <line x1="300" y1="360" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ink}" stroke-width="4"/>
  <path d="M 380 360 A 80 80 0 0 0 {300 + 80 * math.cos(rad):.1f} {360 - 80 * math.sin(rad):.1f}" fill="none" stroke="{fill}" stroke-width="6"/>
  <text x="430" y="330" font-size="28" fill="{ink}" font-family="Georgia, serif">{deg}°</text>
"""


def l_shape(fill: str, ink: str, w1: int, h1: int, w2: int, h2: int) -> str:
    return f"""
  <path d="M 340 160 H 620 V 280 H 500 V 400 H 340 Z" fill="{fill}" fill-opacity="0.4" stroke="{ink}" stroke-width="4"/>
  <text x="480" y="148" text-anchor="middle" font-size="20" fill="{ink}">{w1} см</text>
  <text x="632" y="230" font-size="20" fill="{ink}">{h1} см</text>
  <text x="328" y="300" text-anchor="end" font-size="20" fill="{ink}">{h2} см</text>
  <text x="420" y="422" text-anchor="middle" font-size="20" fill="{ink}">{w2} см</text>
"""


def parallelogram(a: int, h: int, fill: str, ink: str) -> str:
    return f"""
  <polygon points="360,360 700,360 760,220 420,220" fill="{fill}" fill-opacity="0.4" stroke="{ink}" stroke-width="4"/>
  <line x1="420" y1="220" x2="420" y2="360" stroke="{ink}" stroke-dasharray="6 5"/>
  <text x="530" y="392" text-anchor="middle" font-size="22" fill="{ink}">{a} см</text>
  <text x="432" y="300" font-size="22" fill="{ink}">h={h}</text>
"""


def draw(task: dict, level: str, index: int, total: int) -> str:
    accent, _, ink, fill = PALETTE[level]
    kind = task["kind"]
    p = task["params"]
    if kind == "rect":
        body = rect_figure(p["a"], p["b"], fill, ink)
    elif kind == "square":
        body = square_figure(p["a"], fill, ink)
    elif kind == "triangle":
        body = triangle_figure(p["base"], p["height"], fill, ink)
    elif kind == "right":
        body = right_triangle(p["a"], p["b"], p["c"], fill, ink)
    elif kind == "cube":
        body = cube_figure(p["a"], fill, ink)
    elif kind == "box":
        body = cube_figure(p["a"], fill, ink) + f'<text x="480" y="455" text-anchor="middle" font-size="18" fill="{ink}">{p["a"]}×{p["b"]}×{p["c"]} см</text>'
    elif kind == "circle":
        body = circle_figure(p["r"], fill, ink, p.get("d", False))
    elif kind == "angle":
        body = angle_figure(p["deg"], fill, ink)
    elif kind == "l":
        body = l_shape(fill, ink, p["w1"], p["h1"], p["w2"], p["h2"])
    elif kind == "para":
        body = parallelogram(p["a"], p["h"], fill, ink)
    else:
        body = f'<text x="480" y="300" text-anchor="middle" font-size="28" fill="{ink}">{escape(task["question"][:80])}</text>'
    q = escape(task["question"])
    q_lines = []
    words = task["question"].split()
    cur = ""
    for w in words:
        nxt = f"{cur} {w}".strip()
        if len(nxt) > 70 and cur:
            q_lines.append(cur)
            cur = w
        else:
            cur = nxt
    if cur:
        q_lines.append(cur)
    q_svg = "".join(
        f'<text x="56" y="{100 + 22 * i}" font-size="17" fill="{ink}" font-family="Segoe UI, Arial, sans-serif">{escape(line)}</text>'
        for i, line in enumerate(q_lines[:2])
    )
    return wrap(q_svg + body, level, index, total)


def basic() -> list[dict]:
    rows = []
    for a, b in [(8, 3), (10, 4), (12, 5), (7, 6), (15, 2), (9, 4), (11, 5), (14, 3), (16, 4), (13, 6), (20, 5), (18, 7), (17, 3), (19, 4)]:
        rows.append(item(
            f"Прямоугольник {a} см и {b} см. Найдите периметр в см.",
            2 * (a + b),
            f"Тема: периметр. 2 × ({a} + {b}) = {2 * (a + b)}.",
            "rect", a=a, b=b,
        ))
        if a != b:
            rows.append(item(
                f"Прямоугольник {a} см и {b} см. Найдите площадь в см².",
                a * b,
                f"Тема: площадь. {a} × {b} = {a * b}.",
                "rect", a=a, b=b,
            ))
    for a in range(2, 16):
        rows.append(item(
            f"Квадрат со стороной {a} см. Найдите периметр в см.",
            4 * a,
            f"Тема: периметр квадрата. 4 × {a} = {4 * a}.",
            "square", a=a,
        ))
        rows.append(item(
            f"Квадрат со стороной {a} см. Найдите площадь в см².",
            a * a,
            f"Тема: площадь квадрата. {a}² = {a * a}.",
            "square", a=a,
        ))
    for sides in [(5, 5, 6), (7, 8, 9), (4, 7, 8), (10, 10, 6), (3, 4, 5), (6, 6, 6), (8, 15, 17), (2, 3, 4)]:
        per = sum(sides)
        rows.append(item(
            f"Треугольник со сторонами {sides[0]}, {sides[1]} и {sides[2]} см. Периметр в см.",
            per,
            f"Тема: периметр. {per}.",
            "triangle", base=sides[0], height=max(3, min(sides)),
        ))
    rows += [
        item("Сколько рёбер у куба?", 12, "Тема: куб. 12 рёбер.", "cube", a=4),
        item("Сколько граней у куба?", 6, "Тема: куб. 6 граней.", "cube", a=4),
        item("Сколько вершин у куба?", 8, "Тема: куб. 8 вершин.", "cube", a=4),
        item("Сколько сторон у шестиугольника?", 6, "Тема: 6 сторон.", "square", a=6),
        item("Сколько сторон у пятиугольника?", 5, "Тема: 5 сторон.", "square", a=5),
        item("Сколько вершин у треугольника?", 3, "Тема: 3 вершины.", "triangle", base=6, height=5),
        item("Сколько прямых углов у прямоугольника?", 4, "Тема: 4 прямых угла.", "rect", a=8, b=5),
        item("Сколько диагоналей у квадрата?", 2, "Тема: 2 диагонали.", "square", a=6),
        item("Прямой угол в градусах?", 90, "Тема: 90°.", "angle", deg=90),
        item("Развёрнутый угол в градусах?", 180, "Тема: 180°.", "angle", deg=180),
        item("Острый угол 40°. Смежный с ним?", 140, "Тема: 180−40=140.", "angle", deg=40),
        item("Острый угол 25°. Смежный?", 155, "Тема: 180−25=155.", "angle", deg=25),
        item("Угол 70°. Смежный?", 110, "Тема: 180−70=110.", "angle", deg=70),
        item("Угол 15°. Смежный?", 165, "Тема: 180−15=165.", "angle", deg=15),
        item("Сторона квадрата 1 дм. Периметр в см.", 40, "Тема: 4×10=40.", "square", a=10),
        item("Отрезок 3 дм. Сколько см?", 30, "Тема: 30 см.", "rect", a=15, b=3),
        item("2 м 15 см. Сколько всего см?", 215, "Тема: 200+15=215.", "rect", a=20, b=5),
        item("Равносторонний треугольник, сторона 9 см. Периметр?", 27, "Тема: 27.", "triangle", base=9, height=7),
        item("Ромб, сторона 7 см. Периметр?", 28, "Тема: 28.", "para", a=7, h=5),
        item("Равносторонний, сторона 11 см. Периметр?", 33, "Тема: 33.", "triangle", base=11, height=8),
    ]
    seen = set()
    out = []
    for r in rows:
        if r["question"] not in seen:
            seen.add(r["question"])
            out.append(r)
        if len(out) >= 70:
            break
    if len(out) < 70:
        raise SystemExit(f"basic unique {len(out)}")
    return out[:70]


def medium() -> list[dict]:
    rows = []
    for b, h in [(8, 5), (10, 6), (12, 7), (9, 4), (14, 5), (16, 3), (11, 8), (15, 6), (7, 6), (18, 4)]:
        rows.append(item(
            f"Треугольник: основание {b} см, высота {h} см. Площадь в см².",
            b * h // 2 if (b * h) % 2 == 0 else b * h / 2,
            f"Тема: S = a·h/2 = {b}×{h}/2 = {b * h // 2 if (b*h)%2==0 else b*h/2}.",
            "triangle", base=b, height=h,
        ))
    for a, h in [(10, 4), (12, 5), (9, 6), (15, 3), (8, 7), (14, 4)]:
        rows.append(item(
            f"Параллелограмм: основание {a} см, высота {h} см. Площадь в см².",
            a * h,
            f"Тема: S = a·h = {a * h}.",
            "para", a=a, h=h,
        ))
    for a, b, c in [(3, 4, 2), (5, 4, 3), (6, 2, 3), (4, 4, 5), (8, 3, 2), (10, 4, 2), (5, 5, 4), (7, 3, 2)]:
        rows.append(item(
            f"Прямоугольный параллелепипед {a}×{b}×{c} см. Объём в см³.",
            a * b * c,
            f"Тема: V = {a}×{b}×{c} = {a*b*c}.",
            "box", a=a, b=b, c=c,
        ))
    for a in (3, 4, 5, 6, 8):
        rows.append(item(
            f"Куб с ребром {a} см. Объём в см³.",
            a ** 3,
            f"Тема: V = {a}³ = {a**3}.",
            "cube", a=a,
        ))
        rows.append(item(
            f"Куб с ребром {a} см. Площадь поверхности в см².",
            6 * a * a,
            f"Тема: 6a² = {6*a*a}.",
            "cube", a=a,
        ))
    for r in (3, 4, 5, 6, 7, 10):
        rows.append(item(
            f"Окружность радиуса {r} см, π возьмите 3. Длина окружности в см.",
            2 * 3 * r,
            f"Тема: C = 2πr ≈ 6×{r} = {6*r}.",
            "circle", r=r, d=False,
        ))
    rows.append(item(
        "Фигура «уголок»: 8×6 см, вырезан прямоугольник 4×3. Найдите площадь оставшегося в см².",
        48 - 12,
        "Тема: составная. 48 − 12 = 36.",
        "l", w1=8, h1=6, w2=4, h2=3,
    ))
    rows.append(item(
        "Г-образная фигура из прямоугольников 10×4 и 4×6 (без двойного счёта общей 4×4). Площадь?",
        40 + 24 - 16,
        "Тема: 10×4 + 4×6 − 4×4 = 48.",
        "l", w1=10, h1=4, w2=4, h2=6,
    ))
    for a, b in [(6, 8), (5, 12), (9, 12)]:
        rows.append(item(
            f"Прямоугольный треугольник с катетами {a} и {b} см. Площадь в см².",
            a * b // 2,
            f"Тема: S = {a}×{b}/2 = {a*b//2}.",
            "right", a=a, b=b, c=int(math.hypot(a, b)),
        ))
    rows.append(item("Диаметр 10 см. Радиус в см.", 5, "Тема: r = d/2.", "circle", r=5, d=True))
    rows.append(item("Радиус 8 см. Диаметр в см.", 16, "Тема: d = 2r.", "circle", r=8, d=True))
    rows.append(item("Угол треугольника 40° и 60°. Третий угол?", 80, "Тема: сумма 180°.", "triangle", base=10, height=6))
    rows.append(item("Равнобедренный, углы при основании по 50°. Угол при вершине?", 80, "Тема: 180−100=80.", "triangle", base=8, height=7))
    rows.append(item("Масштаб 1:100. 5 см на плане — сколько метров в реальности?", 5, "Тема: 5 см × 100 = 500 см = 5 м.", "rect", a=10, b=5))
    rows.append(item("Масштаб 1:50. 4 см на плане — сколько метров?", 2, "Тема: 4×50=200 см=2 м.", "rect", a=8, b=4))
    rows.append(item("Сторона квадрата увеличили в 2 раза. Во сколько раз выросла площадь?", 4, "Тема: площадь ×4.", "square", a=6))
    rows.append(item("Периметр квадрата 36 см. Сторона в см.", 9, "Тема: 36:4=9.", "square", a=9))
    rows.append(item("Площадь квадрата 81 см². Сторона в см.", 9, "Тема: √81=9.", "square", a=9))
    rows.append(item("Площадь прямоугольника 48 см², одна сторона 8 см. Другая?", 6, "Тема: 48:8=6.", "rect", a=8, b=6))
    rows.append(item("Комната 6 м на 4 м. Площадь в м².", 24, "Тема: 6×4=24.", "rect", a=6, b=4))
    rows.append(item("Рамка: внешний квадрат 10 см, внутренний 6 см. Площадь рамки в см².", 64, "Тема: 100−36=64.", "square", a=10))
    while len(rows) < 80:
        i = len(rows)
        a, b = 5 + i % 8, 3 + i % 6
        rows.append(item(
            f"Прямоугольник {a}×{b} см. Найдите полупериметр (P/2) в см.",
            a + b,
            f"Тема: полупериметр {a}+{b}={a+b}.",
            "rect", a=a, b=b,
        ))
    seen = set()
    out = []
    for r in rows:
        ans = r["answer"]
        if isinstance(ans, float):
            r["answer"] = str(ans).replace(".", ",")
        if r["question"] not in seen:
            seen.add(r["question"])
            out.append(r)
        if len(out) >= 80:
            break
    return out[:80]


def high() -> list[dict]:
    rows = []
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
    for a, b, c in triples:
        rows.append(item(
            f"Катеты {a} см и {b} см. Найдите гипотенузу в см.",
            c,
            f"Тема: Пифагор. {a}²+{b}²={c}².",
            "right", a=a, b=b, c=c,
        ))
        rows.append(item(
            f"Гипотенуза {c} см, катет {a} см. Второй катет в см.",
            b,
            f"Тема: Пифагор. √({c}²−{a}²)={b}.",
            "right", a=a, b=b, c=c,
        ))
    for r in (7, 10, 5, 14):
        rows.append(item(
            f"Круг радиуса {r} см, π = 22/7 если делится, иначе 3,14. Найдите длину окружности. Для r=7: 2×22/7×7.",
            44 if r == 7 else round(2 * 3.14 * r, 2),
            f"Тема: C=2πr.",
            "circle", r=r, d=False,
        ))
    # fix circle answers as strings
    rows[-4] = item("Круг r=7 см, π=22/7. Длина окружности в см.", 44, "Тема: 2×22/7×7=44.", "circle", r=7, d=False)
    rows[-3] = item("Круг r=10 см, π=3,14. Длина окружности. Ответ через запятую.", "62,8", "Тема: 2×3,14×10=62,8.", "circle", r=10, d=False)
    rows[-2] = item("Круг r=5 см, π=3,14. Длина окружности. Ответ через запятую.", "31,4", "Тема: 31,4.", "circle", r=5, d=False)
    rows[-1] = item("Круг r=14 см, π=22/7. Длина окружности в см.", 88, "Тема: 2×22/7×14=88.", "circle", r=14, d=False)
    for r, s in [(7, 154), (14, 616)]:
        rows.append(item(
            f"Круг r={r} см, π=22/7. Площадь в см².",
            s,
            f"Тема: πr² = 22/7 × {r}² = {s}.",
            "circle", r=r, d=False,
        ))
    rows.append(item("Круг r=10, π=3,14. Площадь в см².", 314, "Тема: 3,14×100=314.", "circle", r=10, d=False))
    rows.append(item(
        "Катет 8, гипотенуза 10. Площадь прямоугольного треугольника в см².",
        24,
        "Тема: второй катет 6, S=8×6/2=24.",
        "right", a=8, b=6, c=10,
    ))
    rows.append(item(
        "Дом: прямоугольник 10×6 и треугольная крыша основание 10 высота 4. Площадь фасада в м².",
        80,
        "Тема: 60 + 20 = 80.",
        "l", w1=10, h1=6, w2=10, h2=4,
    ))
    rows.append(item(
        "Дорожка вокруг квадратной клумбы 6×6, ширина 1 м. Площадь дорожки в м².",
        28,
        "Тема: 8×8 − 6×6 = 28.",
        "square", a=8,
    ))
    rows.append(item("Куб V=125 см³. Ребро в см.", 5, "Тема: ∛125=5.", "cube", a=5))
    rows.append(item("Куб S пов.=150 см². Площадь одной грани.", 25, "Тема: 150:6=25.", "cube", a=5))
    rows.append(item("Параллелепипед 5×4×3. Площадь поверхности в см².", 94, "Тема: 2(20+15+12)=94.", "box", a=5, b=4, c=3))
    rows.append(item("Параллелепипед 6×5×2. Площадь поверхности.", 104, "Тема: 2(30+12+10)=104.", "box", a=6, b=5, c=2))
    rows.append(item("Трапеция основания 6 и 10, высота 4. Площадь.", 32, "Тема: (6+10)/2 ×4=32.", "para", a=10, h=4))
    rows.append(item("Трапеция 8 и 12, h=5. Площадь.", 50, "Тема: 10×5=50.", "para", a=12, h=5))
    rows.append(item("Ромб диагонали 6 и 8. Площадь.", 24, "Тема: d1·d2/2=24.", "para", a=8, h=6))
    rows.append(item("Ромб диагонали 10 и 24. Площадь.", 120, "Тема: 10×24/2=120.", "para", a=10, h=12))
    rows.append(item("Сектор не нужен. 1/4 круга r=14, π=22/7. Длина дуги?", 22, "Тема: четверть из 88 = 22.", "circle", r=14, d=False))
    rows.append(item("Подобие: треугольник 3,4,5 увеличен в 3 раза. Большая сторона?", 15, "Тема: 5×3=15.", "right", a=9, b=12, c=15))
    rows.append(item("Подобие: стороны 6 и 9, меньший треугольник сторона 4. Соответствующая?", 6, "Тема: k=4/6=2/3, 9×2/3=6.", "triangle", base=9, height=6))
    rows.append(item("Координатная не: сетка 5×5 клеток по 2 см. Площадь большого квадрата?", 100, "Тема: сторона 10, S=100.", "square", a=10))
    rows.append(item("Сколько квадратов 2×2 в квадрате 8×8?", 16, "Тема: 64:4=16.", "square", a=8))
    rows.append(item("Развёртка куба ребро 4. Площадь развёртки?", 96, "Тема: 6×16=96.", "cube", a=4))
    rows.append(item("Цилиндр не: банка — круглое дно r=7, π=22/7. Площадь дна?", 154, "Тема: πr²=154.", "circle", r=7, d=False))
    rows.append(item("Углы треугольника в отношении 1:2:3. Наибольший угол в градусах.", 90, "Тема: 6 частей, 180/6=30, наибольший 90.", "right", a=6, b=8, c=10))
    rows.append(item("Внешний угол треугольника равен сумме двух внутренних несмежных. Внешний 110, один внутренний 40. Второй?", 70, "Тема: 110−40=70.", "triangle", base=10, height=6))
    rows.append(item("Средняя линия треугольника параллельна основанию 12 см. Длина средней линии?", 6, "Тема: половина основания.", "triangle", base=12, height=8))
    rows.append(item("Основания трапеции 5 и 11. Средняя линия?", 8, "Тема: (5+11)/2=8.", "para", a=11, h=4))
    rows.append(item("Катет 9, катет 12. Площадь?", 54, "Тема: 9×12/2=54.", "right", a=9, b=12, c=15))
    rows.append(item("Равносторонний треугольник сторона 6. Высота √27? Для 5–6: высота ≈5,2 не. Периметр?", 18, "Тема: 18.", "triangle", base=6, height=5))
    rows.append(item("Прямоугольник вписали в... Периметр 28, одна сторона 8. Площадь?", 48, "Тема: вторая 6, S=48.", "rect", a=8, b=6))
    rows.append(item("Из квадрата 10×10 вырезали 4 квадрата 2×2 по углам. Остаток площади?", 84, "Тема: 100−16=84.", "square", a=10))
    rows.append(item("Лестница 5 м по вертикали, 12 м от стены. Длина лестницы (Пифагор).", 13, "Тема: 5-12-13.", "right", a=5, b=12, c=13))
    rows.append(item("Экран 16:9 не. Диагональ прямоугольника 15, сторона 9. Другая?", 12, "Тема: √(225−81)=12.", "right", a=9, b=12, c=15))
    rows.append(item("Объём комнаты 5×4×3 м. Сколько м³ воздуха?", 60, "Тема: 60.", "box", a=5, b=4, c=3))
    rows.append(item("Бассейн 10×5 м, глубина 2 м. Объём в м³.", 100, "Тема: 100.", "box", a=10, b=5, c=2))
    rows.append(item("Сетка: прямоугольник 12 на 5 клеток. Клеток всего?", 60, "Тема: 12×5=60.", "rect", a=12, b=5))
    rows.append(item("Угол 1° — какая часть развёрнутого? Запишите знаменатель дроби 1/n.", 180, "Тема: 1/180.", "angle", deg=1))
    rows.append(item("Сколько градусов в 1/6 полного оборота?", 60, "Тема: 360/6=60.", "angle", deg=60))
    rows.append(item("Полный оборот в градусах?", 360, "Тема: 360°.", "angle", deg=360))
    rows.append(item("Смежные, относятся 2:3. Меньший угол?", 72, "Тема: 5 частей=180, часть 36, меньший 72.", "angle", deg=72))
    rows.append(item("Вертикальные углы равны. Один 55°. Второй?", 55, "Тема: вертикальные равны.", "angle", deg=55))
    pad = []
    for a, b, h in [(6, 8, 5), (10, 14, 6), (7, 9, 4), (12, 16, 5), (5, 9, 8), (11, 13, 7), (8, 10, 9), (15, 20, 6)]:
        pad.append(item(
            f"Трапеция с основаниями {a} и {b} см, высота {h} см. Площадь в см².",
            (a + b) * h // 2,
            f"Тема: ({a}+{b})/2 × {h} = {(a+b)*h//2}.",
            "para", a=b, h=h,
        ))
    for a in range(3, 12):
        pad.append(item(
            f"Куб ребро {a} см. Сумма длин всех рёбер в см.",
            12 * a,
            f"Тема: 12×{a}={12*a}.",
            "cube", a=a,
        ))
        pad.append(item(
            f"Квадрат {a} см. Диагональ не ищем: периметр минус сторона (3 стороны) в см.",
            3 * a,
            f"Тема: 3×{a}={3*a}.",
            "square", a=a,
        ))
    for n in range(3, 12):
        pad.append(item(
            f"Правильный {n}-угольник, сторона 5 см. Периметр в см.",
            5 * n,
            f"Тема: {n}×5={5*n}.",
            "square", a=5,
        ))
    pad += [
        item("Шоколадка 4×6 долек. Сколько долек?", 24, "Тема: 24.", "rect", a=6, b=4),
        item("Плитка 3×3. Сколько маленьких квадратов?", 9, "Тема: 9.", "square", a=3),
        item("Поле 8×8 как шахматы. Сколько клеток?", 64, "Тема: 64.", "square", a=8),
        item("Рамка 12×8, дырка 8×4. Площадь рамки?", 64, "Тема: 96−32=64.", "rect", a=12, b=8),
        item("Два одинаковых квадрата 5 см склеены стороной. Периметр фигуры?", 30, "Тема: 40−10=30.", "square", a=5),
        item("Три квадрата 4 см в ряд. Периметр «ленты»?", 32, "Тема: 12×4 − 2×8? 48−16=32.", "rect", a=12, b=4),
        item("Катет 20, катет 21. Гипотенуза?", 29, "Тема: 400+441=841, √841=29.", "right", a=20, b=21, c=29),
        item("Круг d=14, π=22/7. Длина окружности?", 44, "Тема: πd=22/7×14=44.", "circle", r=7, d=True),
        item("Сектор — четверть круга r=7, π=22/7. Площадь сектора?", 38.5, "Тема: 154/4=38,5.", "circle", r=7, d=False),
        item("Угол 1/8 полного оборота. Градусы?", 45, "Тема: 360/8=45.", "angle", deg=45),
    ]
    for r in pad[-2:]:
        if r["answer"] == "38.5":
            r["answer"] = "38,5"
    rows.extend(pad)
    seen = set()
    out = []
    for r in rows:
        if r["question"] not in seen:
            seen.add(r["question"])
            out.append(r)
        if len(out) >= 100:
            break
    if len(out) < 100:
        raise SystemExit(f"high unique {len(out)}")
    return out[:100]


def sql_escape(value: str) -> str:
    return str(value).replace("'", "''")


def write_pack(level: str, letter: str, slug: str, rows: list[dict], expected: int) -> None:
    if len(rows) != expected:
        raise SystemExit(f"{level}: {len(rows)} ≠ {expected}")
    TASKS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    csv_name = f"geometry-5-6-{slug}.csv"
    sql_name = f"insert-geometry-5-6-{slug}.sql"
    fieldnames = ["subject", "class_name", "level", "question", "answer", "image", "explanation_of_the_answer"]
    csv_rows = []
    sql_values = []
    for i, row in enumerate(rows, start=1):
        filename = f"ge56-{letter}-{i:02d}.svg"
        image = f"/tasks/{filename}"
        (TASKS / filename).write_text(draw(row, level, i, len(rows)), encoding="utf-8")
        csv_rows.append({
            "subject": "geometry",
            "class_name": CLASS,
            "level": level,
            "question": row["question"],
            "answer": row["answer"],
            "image": image,
            "explanation_of_the_answer": row["explanation"],
        })
        sql_values.append(
            "  ('geometry', '{k}', '{lv}', '{q}', '{a}', '{img}', '{e}')".format(
                k=sql_escape(CLASS),
                lv=sql_escape(level),
                q=sql_escape(row["question"]),
                a=sql_escape(row["answer"]),
                img=sql_escape(image),
                e=sql_escape(row["explanation"]),
            )
        )
    with (DATA / csv_name).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(csv_rows)
    sql = (
        f"-- Геометрия, {CLASS}, {level}, {len(rows)} задач.\n"
        "INSERT INTO arithmetic_tasks (subject, class_name, level, question, answer, image, explanation_of_the_answer)\n"
        "VALUES\n" + ",\n".join(sql_values) + ";\n"
    )
    (DATA / sql_name).write_text(sql, encoding="utf-8")
    print(csv_name, len(rows))


def main() -> None:
    write_pack("Базовый", "b", "basic", basic(), 70)
    write_pack("Средний", "m", "medium", medium(), 80)
    write_pack("Высокий", "h", "high", high(), 100)


if __name__ == "__main__":
    main()
