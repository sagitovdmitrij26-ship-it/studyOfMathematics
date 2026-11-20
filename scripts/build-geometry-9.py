# -*- coding: utf-8 -*-
"""Геометрия 9 класс: 70/80/100 задач и схемы SVG."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TASKS = ROOT / "public" / "tasks"
CLASS = "9 класс"

PALETTE = {
    "Базовый": ("#2f6b4f", "#e8f6ee", "#1c3d2e", "#3d9a6a"),
    "Средний": ("#8a6a12", "#fff6d6", "#4a3a08", "#d4a017"),
    "Высокий": ("#9a4a28", "#ffe8dc", "#4a2214", "#e07a4c"),
}


def polish(question: str, answer: str, explanation: str) -> str:
    text = explanation.strip()
    if text.startswith("Тема:"):
        text = text[5:].strip()
    if text.endswith("."):
        text = text[:-1]
    short = len(text) < 28 or text.replace(",", "").replace("-", "").replace(" ", "") == str(answer).replace(",", "").replace("-", "")
    if short:
        return (
            f"Смотрим на числа в условии и применяем нужную формулу "
            f"(длина вектора, расстояние, площадь или теорема). "
            f"После вычисления получается {answer}."
        )
    return f"{text}. Ответ: {answer}."


def item(q, ans, exp, kind, **params):
    answer = str(ans)
    return {
        "question": q,
        "answer": answer,
        "explanation": polish(q, answer, exp),
        "kind": kind,
        "params": params,
    }


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
  <text x="56" y="72" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="700" fill="{ink}">Геометрия · 9 класс</text>
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
    scale = max_side / max(a, b, 1)
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


def circle_figure(r: int, fill: str, ink: str, show_d: bool = False) -> str:
    label = f"d = {2 * r} см" if show_d else f"r = {r} см"
    return f"""
  <circle cx="480" cy="300" r="110" fill="{fill}" fill-opacity="0.35" stroke="{ink}" stroke-width="4"/>
  <line x1="480" y1="300" x2="{480 + 110 if show_d else 590}" y2="300" stroke="{ink}" stroke-width="3"/>
  <circle cx="480" cy="300" r="5" fill="{ink}"/>
  <text x="480" y="440" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{label}</text>
"""


def angle_figure(deg: int, fill: str, ink: str) -> str:
    rad = math.radians(min(max(deg, 15), 170))
    x2, y2 = 480 + 180 * math.cos(rad), 360 - 180 * math.sin(rad)
    return f"""
  <line x1="300" y1="360" x2="700" y2="360" stroke="{ink}" stroke-width="4"/>
  <line x1="300" y1="360" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ink}" stroke-width="4"/>
  <path d="M 380 360 A 80 80 0 0 0 {300 + 80 * math.cos(rad):.1f} {360 - 80 * math.sin(rad):.1f}" fill="none" stroke="{fill}" stroke-width="6"/>
  <text x="430" y="330" font-size="28" fill="{ink}" font-family="Georgia, serif">{deg}°</text>
"""


def parallelogram(a: int, h: int, fill: str, ink: str) -> str:
    return f"""
  <polygon points="360,360 700,360 760,220 420,220" fill="{fill}" fill-opacity="0.4" stroke="{ink}" stroke-width="4"/>
  <line x1="420" y1="220" x2="420" y2="360" stroke="{ink}" stroke-dasharray="6 5"/>
  <text x="530" y="392" text-anchor="middle" font-size="22" fill="{ink}">{a} см</text>
  <text x="432" y="300" font-size="22" fill="{ink}">h={h}</text>
"""


def isosceles_figure(base: int, equal: int, fill: str, ink: str) -> str:
    return f"""
  <polygon points="320,380 640,380 480,170" fill="{fill}" fill-opacity="0.4" stroke="{ink}" stroke-width="4"/>
  <text x="480" y="412" text-anchor="middle" font-size="22" fill="{ink}">{base} см</text>
  <text x="300" y="270" font-size="22" fill="{ink}">{equal}</text>
  <text x="640" y="270" font-size="22" fill="{ink}">{equal}</text>
"""


def _scale(values: list[float]) -> float:
    m = max((abs(v) for v in values if v is not None), default=1)
    return 200 / max(m, 1)


def _xy(x: float, y: float, ox: float, oy: float, scale: float) -> tuple[float, float]:
    return ox + x * scale, oy - y * scale


def _head(x1: float, y1: float, x2: float, y2: float, color: str, size: float = 14) -> str:
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    p1 = (x2 - ux * size + px * size * 0.45, y2 - uy * size + py * size * 0.45)
    p2 = (x2 - ux * size - px * size * 0.45, y2 - uy * size - py * size * 0.45)
    return f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>'


def axes(ink: str, ox: float = 340, oy: float = 390) -> str:
    return f"""
  <line x1="170" y1="{oy}" x2="790" y2="{oy}" stroke="{ink}" stroke-width="2"/>
  <line x1="{ox}" y1="150" x2="{ox}" y2="450" stroke="{ink}" stroke-width="2"/>
  {_head(170, oy, 790, oy, ink, 12)}
  {_head(ox, 450, ox, 150, ink, 12)}
  <text x="778" y="{oy + 22:.0f}" font-size="18" fill="{ink}">x</text>
  <text x="{ox + 12:.0f}" y="168" font-size="18" fill="{ink}">y</text>
  <text x="{ox - 18:.0f}" y="{oy + 22:.0f}" font-size="16" fill="{ink}">O</text>
"""


def arrow(ox: float, oy: float, x: float, y: float, scale: float, color: str, name: str, ink: str) -> str:
    x1, y1 = ox, oy
    x2, y2 = _xy(x, y, ox, oy, scale)
    lx, ly = (x1 + x2) / 2 + 10, (y1 + y2) / 2 - 8
    return f"""
  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="5"/>
  {_head(x1, y1, x2, y2, color)}
  <text x="{lx:.1f}" y="{ly:.1f}" font-size="20" fill="{ink}" font-family="Georgia, serif">{escape(name)}</text>
"""


def vector_figure(p: dict, fill: str, ink: str) -> str:
    ox, oy = 340, 390
    ax = p.get("ax", p.get("vx", 3))
    ay = p.get("ay", p.get("vy", 4))
    bx, by = p.get("bx"), p.get("by")
    nums = [ax, ay]
    if bx is not None:
        nums += [bx, by]
    scale = _scale(nums)
    svg = axes(ink, ox, oy)
    svg += arrow(ox, oy, ax, ay, scale, ink, f"a ({ax}; {ay})", ink)
    if bx is not None:
        svg += arrow(ox, oy, bx, by, scale, fill, f"b ({bx}; {by})", ink)
    return svg


def points_figure(p: dict, fill: str, ink: str) -> str:
    ox, oy = 340, 390
    x1, y1 = p.get("x1", 0), p.get("y1", 0)
    x2, y2 = p.get("x2", 4), p.get("y2", 3)
    scale = _scale([x1, y1, x2, y2])
    a = _xy(x1, y1, ox, oy, scale)
    b = _xy(x2, y2, ox, oy, scale)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    mid = ""
    if p.get("mid"):
        mid = f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="6" fill="{fill}" stroke="{ink}" stroke-width="2"/>'
        mid += f'<text x="{mx + 12:.1f}" y="{my - 8:.1f}" font-size="18" fill="{ink}">M</text>'
    return f"""
  {axes(ink, ox, oy)}
  <line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{fill}" stroke-width="4"/>
  {_head(a[0], a[1], b[0], b[1], fill)}
  <circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="6" fill="{ink}"/>
  <circle cx="{b[0]:.1f}" cy="{b[1]:.1f}" r="6" fill="{ink}"/>
  <text x="{a[0] + 10:.1f}" y="{a[1] - 10:.1f}" font-size="18" fill="{ink}">A({x1}; {y1})</text>
  <text x="{b[0] + 10:.1f}" y="{b[1] - 10:.1f}" font-size="18" fill="{ink}">B({x2}; {y2})</text>
  {mid}
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
    elif kind == "iso":
        body = isosceles_figure(p["base"], p["equal"], fill, ink)
    elif kind == "right":
        body = right_triangle(p["a"], p["b"], p["c"], fill, ink)
    elif kind == "circle":
        body = circle_figure(p["r"], fill, ink, p.get("d", False))
    elif kind == "angle":
        body = angle_figure(p["deg"], fill, ink)
    elif kind == "para":
        body = parallelogram(p["a"], p["h"], fill, ink)
    elif kind == "vector":
        body = vector_figure(p, fill, ink)
    elif kind == "points":
        body = points_figure(p, fill, ink)
    else:
        body = f'<text x="480" y="300" text-anchor="middle" font-size="28" fill="{ink}">{escape(task["question"][:80])}</text>'
    words = task["question"].split()
    cur = ""
    q_lines = []
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


def take_unique(rows: list[dict], n: int, label: str) -> list[dict]:
    seen = set()
    out = []
    for r in rows:
        if r["question"] not in seen:
            seen.add(r["question"])
            out.append(r)
        if len(out) >= n:
            break
    if len(out) < n:
        raise SystemExit(f"{label} unique {len(out)}")
    return out[:n]


def basic() -> list[dict]:
    rows = []
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17), (7, 24, 25)]
    for a, b, c in triples:
        rows.append(item(
            f"Расстояние от (0; 0) до ({a}; {b}).",
            c,
            f"Расстояние от начала координат до точки ({a}; {b}) считают так: корень из ({a}×{a} + {b}×{b}). {a*a} + {b*b} = {c*c}, корень равен {c}.",
            "points", x1=0, y1=0, x2=a, y2=b,
        ))
        rows.append(item(
            f"Вектор a = ({a}; {b}). Найдите длину вектора a.",
            c,
            f"Длина вектора с координатами ({a}; {b}) — это корень из суммы квадратов: {a}×{a} + {b}×{b} = {c*c}, корень равен {c}.",
            "vector", vx=a, vy=b,
        ))
        rows.append(item(
            f"Точки A(0; 0) и B({a}; {b}). Координата x вектора AB.",
            a,
            f"Координаты вектора AB равны разности координат конца и начала. Из (0; 0) в ({a}; {b}) получается x = {a} − 0 = {a}.",
            "vector", vx=a, vy=b,
        ))
        rows.append(item(
            f"Точки A(0; 0) и B({a}; {b}). Координата y вектора AB.",
            b,
            f"Координата y вектора AB: {b} − 0 = {b}.",
            "vector", vx=a, vy=b,
        ))
    for x1, y1, x2, y2 in [(2, 4, 8, 10), (0, 6, 12, 2), (1, 1, 7, 9), (3, 5, 11, 5), (4, 0, 4, 8), (-2, 4, 8, 10), (5, 3, 9, 11)]:
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        if (x1 + x2) % 2 or (y1 + y2) % 2:
            continue
        rows.append(item(
            f"Середина отрезка ({x1}; {y1}) и ({x2}; {y2}). Абсцисса середины.",
            mx,
            f"Абсцисса середины — среднее арифметическое абсцисс концов: ({x1} + {x2}) : 2 = {mx}.",
            "points", x1=x1, y1=y1, x2=x2, y2=y2, mid=True,
        ))
        rows.append(item(
            f"Середина отрезка ({x1}; {y1}) и ({x2}; {y2}). Ордината середины.",
            my,
            f"Ордината середины — среднее ординат концов: ({y1} + {y2}) : 2 = {my}.",
            "points", x1=x1, y1=y1, x2=x2, y2=y2, mid=True,
        ))
    for ax, ay, bx, by in [(2, 3, 4, 1), (5, 0, 0, 7), (1, 8, 3, -2), (6, 4, -1, 5), (3, 3, 3, 3)]:
        rows.append(item(
            f"Векторы a=({ax}; {ay}) и b=({bx}; {by}). Найдите x-координату суммы.",
            ax + bx,
            f"При сложении векторов координаты складывают отдельно. x = {ax} + {bx} = {ax + bx}.",
            "vector", vx=ax, vy=ay, ax=ax, ay=ay, bx=bx, by=by,
        ))
        rows.append(item(
            f"Векторы a=({ax}; {ay}) и b=({bx}; {by}). Найдите y-координату суммы.",
            ay + by,
            f"y-координата суммы: {ay} + {by} = {ay + by}.",
            "vector", vx=ax, vy=ay, ax=ax, ay=ay, bx=bx, by=by,
        ))
        rows.append(item(
            f"Вектор a=({ax}; {ay}). Найдите x-координату вектора 2a.",
            2 * ax,
            f"Умножение вектора на 2 удваивает каждую координату. x становится 2 × {ax} = {2 * ax}.",
            "vector", vx=2 * ax, vy=2 * ay, ax=ax, ay=ay,
        ))
    for r in (3, 4, 5, 6, 7, 10, 14, 21):
        if r in (7, 14, 21):
            rows.append(item(
                f"Окружность r={r} см, π=22/7. Длина окружности в см.",
                2 * 22 * r // 7,
                f"Длина окружности: 2 × π × r. Берём π = 22/7: 2 × 22/7 × {r} = {2 * 22 * r // 7}.",
                "circle", r=r, d=False,
            ))
            rows.append(item(
                f"Круг r={r} см, π=22/7. Площадь в см².",
                22 * r * r // 7,
                f"Площадь круга: π × r × r. π = 22/7, r = {r}, поэтому 22/7 × {r*r} = {22 * r * r // 7}.",
                "circle", r=r, d=False,
            ))
        else:
            rows.append(item(
                f"Окружность r={r} см, π=3. Длина окружности.",
                6 * r,
                f"Длина окружности ≈ 2 × 3 × r = 6 × {r} = {6 * r}.",
                "circle", r=r, d=False,
            ))
    rows += [
        item("sin 30° = 1/2. Запишите знаменатель дроби 1/n.", 2, "Тема: sin 30°=1/2.", "angle", deg=30),
        item("cos 60° = 1/2. Знаменатель дроби 1/n.", 2, "Тема: cos 60°=1/2.", "angle", deg=60),
        item("sin 90° равен?", 1, "Тема: 1.", "angle", deg=90),
        item("cos 0° равен?", 1, "Тема: 1.", "angle", deg=15),
        item("sin 0° равен?", 0, "Тема: 0.", "angle", deg=15),
        item("cos 90° равен?", 0, "Тема: 0.", "angle", deg=90),
        item("tg 45° равен?", 1, "Тема: 1.", "angle", deg=45),
        item("tg 0° равен?", 0, "Тема: 0.", "angle", deg=15),
        item("sin 150° = sin 30° = 1/2. Знаменатель 1/n.", 2, "Тема: sin(180−30)=sin 30.", "angle", deg=150),
        item("cos 120° = −1/2. Запишите числитель со знаком: −1.", -1, "Тема: cos 120°=−1/2.", "angle", deg=120),
        item("Стороны a=6, b=8, угол C=90°. Площадь 1/2 ab sin C. sin 90=1. Площадь?", 24, "Тема: 6×8/2=24.", "right", a=6, b=8, c=10),
        item("Стороны 10 и 10, угол 30°, sin 30=1/2. Площадь 1/2 ab sin C?", 25, "Тема: 100/2×1/2=25.", "iso", base=10, equal=10),
        item("Стороны 8 и 10, угол 90°. Площадь?", 40, "Тема: 8×10/2=40.", "right", a=8, b=10, c=13),
        item("Теорема синусов: a/sin A = 2R. a=10, угол A=30°, sin=1/2. 2R?", 20, "Тема: 10/(1/2)=20.", "circle", r=10, d=True),
        item("a=10, A=30°, 2R=20. Радиус описанной окружности R?", 10, "Тема: R=10.", "circle", r=10, d=False),
        item("Диаметр 16. Радиус?", 8, "Тема: 8.", "circle", r=8, d=True),
        item("Радиус 9. Диаметр?", 18, "Тема: 18.", "circle", r=9, d=True),
        item("Точка M(3; 5) перенесена на вектор (2; −1). Новая абсцисса?", 5, "Тема: 3+2=5.", "vector", vx=2, vy=-1),
        item("Точка M(3; 5) перенесена на вектор (2; −1). Новая ордината?", 4, "Тема: 5−1=4.", "vector", vx=2, vy=-1),
        item("Коллинеарные векторы (2; 4) и (1; k). Найдите k.", 2, "Тема: 2/1=4/k, k=2.", "vector", vx=1, vy=2),
        item("Коллинеарные (3; 6) и (2; k). k?", 4, "Тема: 3/2=6/k, k=4.", "vector", vx=2, vy=4),
        item("Перпендикулярные векторы: скалярное произведение 0. a=(3; 1), b=(−1; k). k?", 3, "Тема: −3+k=0, k=3.", "vector", vx=-1, vy=3),
        item("Векторы a=(4; 2) и b=(1; -2). Найдите скалярное произведение.", 0, "Тема: 4-4=0, векторы перпендикулярны.", "vector", vx=1, vy=-2),
        item("Векторы a=(5; 0) и b=(0; 7). Найдите скалярное произведение.", 0, "Тема: 0.", "vector", vx=0, vy=7),
        item("Векторы a=(2; 3) и b=(4; 1). Найдите скалярное произведение.", 11, "Тема: 8+3=11.", "vector", vx=4, vy=1),
        item("Центр окружности (0; 0), радиус 5. Точка (3; 4) лежит на окружности. Проверка: 9+16?", 25, "Тема: r²=25.", "circle", r=5, d=False),
        item("Уравнение x²+y²=49. Радиус?", 7, "Тема: r=7.", "circle", r=7, d=False),
        item("Уравнение x²+y²=36. Радиус?", 6, "Тема: 6.", "circle", r=6, d=False),
        item("Центр (0; 0), точка (8; 15) на окружности. Радиус?", 17, "Тема: 8-15-17.", "circle", r=17, d=False),
        item("Правильный шестиугольник, сторона 7. Периметр?", 42, "Тема: 42.", "square", a=7),
        item("Правильный восьмиугольник, сторона 5. Периметр?", 40, "Тема: 40.", "square", a=5),
        item("Внешний угол правильного шестиугольника?", 60, "Тема: 360/6=60.", "angle", deg=60),
        item("Внешний угол правильного восьмиугольника?", 45, "Тема: 45.", "angle", deg=45),
        item("Сумма внешних углов выпуклого многоугольника?", 360, "Тема: 360°.", "square", a=6),
        item("Гомотетия с коэффициентом 2, отрезок 9 см. Образ отрезка?", 18, "Тема: ×2.", "triangle", base=18, height=8),
        item("Гомотетия k=3, периметр 12. Периметр образа?", 36, "Тема: ×3.", "triangle", base=12, height=6),
        item("Поворот на 90° вокруг начала: точка (3; 0). Новая абсцисса точки (0; 3) после поворота (x;y)→(−y;x). Для (3;0)?", 0, "Тема: (−0; 3), x=0.", "vector", vx=0, vy=3),
        item("Поворот на 90°: (3; 0) → (−0; 3). Новая ордината?", 3, "Тема: 3.", "vector", vx=0, vy=3),
        item("Симметрия относительно оси Ox: точка (4; 5). Ордината образа?", -5, "Тема: (4; −5).", "vector", vx=4, vy=-5),
        item("Симметрия относительно оси Oy: точка (4; 5). Абсцисса образа?", -4, "Тема: (−4; 5).", "vector", vx=-4, vy=5),
        item("Длина окружности 44, π=22/7. Радиус?", 7, "Тема: 2πr=44.", "circle", r=7, d=False),
        item("Длина 88, π=22/7. Диаметр?", 28, "Тема: πd=88, d=28.", "circle", r=14, d=True),
        item("Площадь круга 154, π=22/7. Радиус?", 7, "Тема: πr²=154, r=7.", "circle", r=7, d=False),
        item("Четверть круга r=14, π=22/7. Длина дуги 90°?", 22, "Тема: 88/4=22.", "circle", r=14, d=False),
        item("Катет против 30° при гипотенузе 16?", 8, "Тема: половина гипотенузы.", "right", a=8, b=14, c=16),
        item("Гипотенуза 20, угол 30°. Катет против 30°?", 10, "Тема: 10.", "right", a=10, b=17, c=20),
        item("Прямоугольный 6-8-10. sin угла напротив 6 равен 6/10. Знаменатель несократимой 3/n?", 5, "Тема: 3/5.", "right", a=6, b=8, c=10),
        item("cos угла при катете 8 в 6-8-10 равен 8/10=4/5. Числитель?", 4, "Тема: 4/5.", "right", a=6, b=8, c=10),
        item("Найдите длину нулевого вектора.", 0, "Тема: длина нулевого вектора равна 0.", "vector", vx=0, vy=0),
        item("Противоположный к (5; −2). Координата x.", -5, "Тема: (−5; 2).", "vector", vx=-5, vy=2),
        item("Противоположный к (5; −2). Координата y.", 2, "Тема: 2.", "vector", vx=-5, vy=2),
        item("Разность a=(7; 4) и b=(3; 1). Координата x.", 4, "Тема: 7−3=4.", "vector", vx=4, vy=3),
        item("Разность a=(7; 4) и b=(3; 1). Координата y.", 3, "Тема: 4−1=3.", "vector", vx=4, vy=3),
        item("Треугольник (0;0), (6;0), (0;8). Площадь?", 24, "Тема: 6×8/2=24.", "triangle", base=6, height=8),
        item("Треугольник (0;0), (10;0), (0;4). Площадь?", 20, "Тема: 20.", "triangle", base=10, height=4),
        item("Прямоугольник вершины (0;0) и (5;3) противоположны. Площадь?", 15, "Тема: 5×3=15.", "rect", a=5, b=3),
    ]
    return take_unique(rows, 70, "basic")


def medium() -> list[dict]:
    rows = []
    # cosine theorem: b=c, angle 60 -> a=b, equilateral; angle 90 pythagoras; angle 120
    for b, c in [(5, 5), (6, 6), (8, 8), (10, 10)]:
        rows.append(item(
            f"Стороны {b} и {c} см, угол между ними 60°, cos 60=1/2. Третья сторона (теорема косинусов).",
            b,
            f"Теорема косинусов: квадрат третьей стороны = {b}×{b} + {c}×{c} − 2×{b}×{c}×(1/2). Получается {b*b}, сторона равна {b} (равносторонний треугольник).",
            "iso", base=b, equal=b,
        ))
    for a, b, c in [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]:
        rows.append(item(
            f"Стороны {a} и {b}, угол 90°. Третья сторона (косинусы, cos 90=0).",
            c,
            f"Угол 90°, cos 90° = 0, поэтому теорема косинусов совпадает с Пифагором: {a}×{a} + {b}×{b} = {c*c}, третья сторона {c}.",
            "right", a=a, b=b, c=c,
        ))
        rows.append(item(
            f"a={c}, b={a}, A=90° в прямоугольном. sin A=1, теорема синусов a/sin A=2R. 2R?",
            c,
            f"В прямоугольном треугольнике диаметр описанной окружности равен гипотенузе {c}, значит 2R = {c}.",
            "right", a=a, b=b, c=c,
        ))
    dots = [
        (2, 3, 4, 1, 11),
        (5, 2, 1, 4, 13),
        (6, 1, 2, 3, 15),
        (3, 3, 1, 2, 9),
        (8, -2, 1, 3, 2),
        (4, 0, 0, 5, 0),
        (7, 1, -1, 7, 0),
        (9, 2, 2, -4, 10),
    ]
    for ax, ay, bx, by, prod in dots:
        rows.append(item(
            f"Векторы a=({ax}; {ay}) и b=({bx}; {by}). Найдите скалярное произведение a и b.",
            prod,
            f"Скалярное произведение: перемножаем одноимённые координаты и складываем. {ax}×{bx} + {ay}×{by} = {prod}.",
            "vector", vx=ax, vy=ay, ax=ax, ay=ay, bx=bx, by=by,
        ))
    for r, deg, arc in [(14, 90, 22), (7, 180, 22), (21, 60, 22), (14, 180, 44), (7, 90, 11)]:
        rows.append(item(
            f"Дуга {deg}°, r={r} см, π=22/7. Длина дуги в см.",
            arc,
            f"Длина дуги — это часть длины окружности. Сначала C = 2×(22/7)×{r}, затем берём {deg}/360 этой длины и получаем {arc} см.",
            "circle", r=r, d=False,
        ))
    for r, deg, s in [(14, 90, 154), (7, 180, 77), (21, 90, 346.5), (14, 180, 308)]:
        if s == 346.5:
            ans = "346,5"
        elif s == 77:
            ans = 77
        else:
            ans = int(s) if float(s) == int(s) else s
        rows.append(item(
            f"Сектор {deg}°, r={r} см, π=22/7. Площадь сектора.",
            ans,
            f"Площадь сектора — доля площади круга: {deg}/360. Подставляем r = {r} и π = 22/7, выходит {ans}.",
            "circle", r=r, d=False,
        ))
    rows += [
        item("Сектор 90°, r=14, π=22/7. Площадь сектора?", 154, "Тема: 616/4=154.", "circle", r=14, d=False),
        item("Сектор 180°, r=14, π=22/7. Площадь полукруга?", 308, "Тема: 616/2=308.", "circle", r=14, d=False),
        item("Круг r=10, π=3,14. Площадь?", 314, "Тема: 314.", "circle", r=10, d=False),
        item("Круг r=10, π=3,14. Длина. Ответ через запятую.", "62,8", "Тема: 62,8.", "circle", r=10, d=False),
        item("Стороны 5 и 5 см, угол 120°. Квадрат третьей стороны (теорема косинусов).", 75, "Тема: 25+25+25=75.", "iso", base=8, equal=5),
        item("Стороны 5 и 5, угол 120°. Квадрат третьей стороны a² (косинусы).", 75, "Тема: 25+25+25=75.", "iso", base=8, equal=5),
        item("Стороны 7 и 8, угол 60°. a²=49+64−56. a²?", 57, "Тема: 113−56=57.", "triangle", base=8, height=6),
        item("Стороны 10 и 6, прямой угол. Квадрат гипотенузы.", 136, "Тема: 100+36=136.", "right", a=10, b=6, c=12),
        item("Вектор a = (3; 4). Найдите длину вектора a.", 5, "Тема: корень из (9+16)=5.", "vector", vx=3, vy=4),
        item("Вектор a = (5; 12). Найдите длину вектора a.", 13, "Тема: корень из (25+144)=13.", "vector", vx=5, vy=12),
        item("Единичный вектор в направлении (6; 8). Координата x (6/10=0,6). Запишите 3/5 числитель.", 3, "Тема: (3/5; 4/5).", "vector", vx=3, vy=4),
        item("Единичный вдоль (6; 8). Координата y как 4/5. Числитель?", 4, "Тема: 4/5.", "vector", vx=3, vy=4),
        item("cos угла между a=(1; 0) и b=(1; 0) равен?", 1, "Тема: 1.", "vector", vx=1, vy=0),
        item("Угол между (1; 0) и (0; 1) в градусах?", 90, "Тема: скалярное 0.", "vector", vx=0, vy=1),
        item("Окружность (x−3)²+(y−4)²=25. Центр, абсцисса?", 3, "Тема: (3; 4).", "circle", r=5, d=False),
        item("Окружность (x−3)²+(y−4)²=25. Ордината центра?", 4, "Тема: 4.", "circle", r=5, d=False),
        item("Окружность (x−3)²+(y−4)²=25. Радиус?", 5, "Тема: 5.", "circle", r=5, d=False),
        item("(x+2)²+(y−1)²=16. Абсцисса центра?", -2, "Тема: (−2; 1).", "circle", r=4, d=False),
        item("(x+2)²+(y−1)²=16. Радиус?", 4, "Тема: 4.", "circle", r=4, d=False),
        item("Точки A(0;0), B(8;0), C(0;6). Сумма абсцисс вершин для центроида (числитель дроби 8/3).", 8, "Тема: (0+8+0)/3=8/3.", "triangle", base=8, height=6),
        item("Точки A(0;0), B(8;0), C(0;6). Сумма абсцисс вершин. Затем разделите на 3: запишите числитель дроби x=8/3.", 8, "Тема: 8/3.", "triangle", base=8, height=6),
        item("A(0;0), B(6;0), C(0;9). Ордината центроида как 9/3.", 3, "Тема: (0+0+9)/3=3.", "triangle", base=6, height=9),
        item("A(2;2), B(8;2), C(2;8). Абсцисса центроида?", 4, "Тема: (2+8+2)/3=4.", "triangle", base=6, height=6),
        item("Гомотетия k=−2 относительно O. Точка (3; 1). Абсцисса образа?", -6, "Тема: −2×3=−6.", "vector", vx=-6, vy=-2),
        item("Гомотетия k=−2, точка (3; 1). Ордината образа?", -2, "Тема: −2.", "vector", vx=-6, vy=-2),
        item("Гомотетия k=1/2, отрезок 18. Образ?", 9, "Тема: 9.", "triangle", base=9, height=6),
        item("Подобие k=2, площадь малого 15. Площадь большого?", 60, "Тема: ×4.", "triangle", base=12, height=8),
        item("Площади подобных 4 и 36. Коэффициент линейный?", 3, "Тема: √9=3.", "triangle", base=18, height=9),
        item("Теорема синусов: a=12, A=30°, B=90°. Сторона b=2R=a/sin A. b?", 24, "Тема: 12/(1/2)=24.", "right", a=12, b=21, c=24),
        item("В треугольнике A=30°, B=60°, C=90°, a=7 против 30°. Гипотенуза?", 14, "Тема: 14.", "right", a=7, b=12, c=14),
        item("Катет против 30° равен 8 см. Гипотенуза в прямоугольном треугольнике?", 16, "Тема: 16.", "right", a=8, b=14, c=16),
        item("Площадь 1/2·7·8·sin C, sin C=1/2. Площадь?", 14, "Тема: 28×1/2=14.", "triangle", base=8, height=4),
        item("Площадь 1/2·12·12·sin 90°. Площадь?", 72, "Тема: 72.", "iso", base=12, equal=12),
        item("Параллелограмм стороны 6 и 10, sin угла 1/2. Площадь ab sin?", 30, "Тема: 60×1/2=30.", "para", a=10, h=3),
        item("Параллелограмм 8 и 5, угол 90°. Площадь?", 40, "Тема: 40.", "para", a=8, h=5),
        item("Ромб сторона 13, sin угла 12/13. Площадь 13·13·12/13?", 156, "Тема: 13×12=156.", "para", a=13, h=12),
        item("Вектор AB из A(1; 2) в B(6; 8). x?", 5, "Тема: 5.", "vector", vx=5, vy=6),
        item("Вектор AB из A(1; 2) в B(6; 8). y?", 6, "Тема: 6.", "vector", vx=5, vy=6),
        item("A(1; 2) и B(6; 8). Квадрат длины AB.", 61, "Тема: 25+36=61.", "vector", vx=5, vy=6),
        item("Расстояние (2; 3) и (8; 11).", 10, "Тема: Δx=6, Δy=8, 10.", "right", a=6, b=8, c=10),
        item("Расстояние (−1; 4) и (4; 16).", 13, "Тема: 5 и 12.", "right", a=5, b=12, c=13),
        item("Пересечение хорд: 3 и 8, 4 и x. x?", 6, "Тема: 3×8=4x, x=6.", "circle", r=10, d=False),
        item("Касательная 9, внешняя часть секущей 3. Вся секущая?", 27, "Тема: 81=3s, s=27.", "circle", r=12, d=False),
        item("Вписанный угол 36°. Дуга?", 72, "Тема: 72°.", "circle", r=8, d=False),
        item("Центральный 140°. Вписанный?", 70, "Тема: 70°.", "circle", r=8, d=False),
        item("Поворот 180° вокруг O: точка (5; −3). Абсцисса образа?", -5, "Тема: (−5; 3).", "vector", vx=-5, vy=3),
        item("Поворот 180°: (5; −3). Ордината образа?", 3, "Тема: 3.", "vector", vx=-5, vy=3),
        item("Поворот 90°: (0; 4) → (−4; 0). Абсцисса?", -4, "Тема: (−y; x)=(−4; 0).", "vector", vx=-4, vy=0),
        item("Симметрия относительно начала: (7; 2). Абсцисса?", -7, "Тема: (−7; −2).", "vector", vx=-7, vy=-2),
        item("Параллельный перенос на (3; −4) точки (10; 10). Ордината?", 6, "Тема: 10−4=6.", "vector", vx=3, vy=-4),
        item("Равнобедренный треугольник, основание 6 см, высота 4 см. Площадь?", 12, "Тема: 6×4/2=12.", "iso", base=6, equal=5),
        item("Равнобедренный основание 16, боковые 10. Высота?", 6, "Тема: 8²+h²=100, h=6.", "iso", base=16, equal=10),
        item("Медиана к гипотенузе 10. Длина медианы?", 5, "Тема: половина гипотенузы.", "right", a=6, b=8, c=10),
        item("Медиана к гипотенузе 26?", 13, "Тема: 13.", "right", a=10, b=24, c=26),
        item("r вписанной (a+b−c)/2 для 9-12-15?", 3, "Тема: (9+12−15)/2=3.", "right", a=9, b=12, c=15),
        item("R описанной для 9-12-15?", "7,5", "Тема: c/2=7,5.", "right", a=9, b=12, c=15),
        item("Дуга 60°, r=21, π=22/7. Длина дуги?", 22, "Тема: 132/6=22.", "circle", r=21, d=False),
        item("Полный оборот в радианах как π: сколько π в 2π? Запишите 2.", 2, "Тема: 2π.", "circle", r=7, d=False),
        item("90° в радианах как π/n. Знаменатель n?", 2, "Тема: π/2.", "angle", deg=90),
        item("180° в радианах — коэффициент при π?", 1, "Тема: π.", "angle", deg=180),
        item("360° — коэффициент при π?", 2, "Тема: 2π.", "angle", deg=360),
        item("60° = π/n. n?", 3, "Тема: π/3.", "angle", deg=60),
        item("30° = π/n. n?", 6, "Тема: π/6.", "angle", deg=30),
        item("45° = π/n. n?", 4, "Тема: π/4.", "angle", deg=45),
    ]
    extra = []
    for n in range(3, 18):
        extra.append(item(
            f"Правильный {n}-угольник, сторона 9 см. Периметр.",
            9 * n,
            f"У правильного {n}-угольника все стороны равны 9 см. Периметр = {n} × 9 = {9 * n} см.",
            "square", a=9,
        ))
        extra.append(item(
            f"Вектор ({n}; {2 * n}). Найдите квадрат его длины.",
            n * n + 4 * n * n,
            f"Квадрат длины = {n}×{n} + {2*n}×{2*n} = {n*n} + {4*n*n} = {5*n*n}.",
            "vector", vx=n, vy=2 * n,
        ))
    rows.extend(extra)
    for r in rows:
        if isinstance(r["answer"], float):
            r["answer"] = str(r["answer"]).replace(".", ",")
    return take_unique(rows, 80, "medium")


def high() -> list[dict]:
    rows = []
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
    for a, b, c in triples:
        rows.append(item(
            f"Точки (0;0) и ({a}; {b}). Расстояние.",
            c,
            f"Расстояние считают по формуле корня из суммы квадратов: {a}×{a} + {b}×{b} = {c*c}, корень равен {c}.",
            "points", x1=0, y1=0, x2=a, y2=b,
        ))
        rows.append(item(
            f"Вектор a = ({a}; {b}). Найдите длину вектора a.",
            c,
            f"Длина вектора ({a}; {b}) = корень из ({a*a} + {b*b}) = {c}.",
            "vector", vx=a, vy=b,
        ))
        rows.append(item(
            f"Прямоугольный {a}-{b}-{c}. Радиус описанной окружности (половина гипотенузы). Дробь через запятую.",
            str(c / 2).replace(".", ",") if c % 2 else c // 2,
            f"В прямоугольном треугольнике центр описанной окружности — середина гипотенузы. Радиус = {c} : 2.",
            "right", a=a, b=b, c=c,
        ))
    rows += [
        item("Косинусы: стороны 13, 14, 15. Угол против 15: cos C=(13²+14²−15²)/(2·13·14). Числитель 169+196−225.", 140, "Тема: 140, cos=140/364=5/13.", "triangle", base=15, height=12),
        item("Для сторон 13,14,15 cos C=5/13. Знаменатель дроби 5/n?", 13, "Тема: 5/13.", "triangle", base=15, height=12),
        item("Площадь треугольника 13,14,15 при высоте 12 к стороне 14?", 84, "Тема: 84.", "triangle", base=14, height=12),
        item("1/2·13·14·sin C = 84. sin C=84·2/(13·14). sin C=12/13. Числитель?", 12, "Тема: 12/13.", "triangle", base=14, height=12),
        item("Векторы a=(6; 8) и b=(8; -6). Найдите скалярное произведение.", 0, "Тема: 48-48=0.", "vector", vx=8, vy=-6),
        item("Длины векторов a и b равны 10, скалярное произведение равно 0. Угол между ними в градусах?", 90, "Тема: 90°.", "vector", vx=8, vy=-6),
        item("Векторы a=(1; 2) и b=(2; 4) сонаправлены. Угол между ними в градусах?", 0, "Тема: 0°.", "vector", vx=2, vy=4),
        item("Векторы a=(1; 0) и b=(-1; 0). Угол между ними в градусах?", 180, "Тема: 180°.", "vector", vx=-1, vy=0),
        item("Длина a равна 5, длина b равна 4, угол 60°, cos 60° = 1/2. Скалярное произведение?", 10, "Тема: 5×4×1/2=10.", "vector", vx=3, vy=4),
        item("Длина a равна 6, длина b равна 8, угол 90°. Скалярное произведение?", 0, "Тема: 0.", "vector", vx=6, vy=8),
        item("Длина a равна 3, длина b равна 3, угол 120°, cos 120° = -1/2. Скалярное произведение. Ответ через запятую.", "-4,5", "Тема: 9×(-1/2)=-4,5.", "vector", vx=-2, vy=2),
        item("Проекция a на ось: a=(8; 6) на Ox. Длина проекции?", 8, "Тема: |x|=8.", "vector", vx=8, vy=6),
        item("Координатный метод: A(0;0), B(4;0), C(0;3). AB²+AC² и BC². BC?", 5, "Тема: 5.", "right", a=3, b=4, c=5),
        item("Площадь по координатам A(0;0), B(6;0), C(2;8). S=1/2|6·8−0·2|?", 24, "Тема: 24.", "triangle", base=6, height=8),
        item("A(1;1), B(5;1), C(1;7). Площадь?", 12, "Тема: 4×6/2=12.", "triangle", base=4, height=6),
        item("A(0;0), B(7;0), C(1;6). S=1/2·7·6=21, если высота 6 к основанию 7? C не над основанием ровно — формула 1/2|x1(y2-y3)+x2(y3-y1)+x3(y1-y2)| = 1/2|0+7·6+1·0|=21.", 21, "Тема: 21.", "triangle", base=7, height=6),
        item("Окружность x²+y²−6x−8y=0. Дополните до (x−3)²+(y−4)²=r². r²=9+16.", 25, "Тема: r=5, r²=25.", "circle", r=5, d=False),
        item("После выделения квадратов центр (3; 4). Радиус?", 5, "Тема: 5.", "circle", r=5, d=False),
        item("x²+y²+4x−2y−4=0. Центр (−2; 1), r²=4+1+4=9. Радиус?", 3, "Тема: 3.", "circle", r=3, d=False),
        item("Из точки (8; 0) к окружности x²+y²=16. Квадрат длины касательной.", 48, "Тема: 64−16=48.", "circle", r=4, d=False),
        item("Из (8;0) к окружности x²+y²=16 длина касательной. Квадрат длины.", 48, "Тема: 64−16=48.", "circle", r=4, d=False),
        item("Из (13;0) к x²+y²=25. Квадрат длины касательной.", 144, "Тема: 169−25=144.", "circle", r=5, d=False),
        item("Длина касательной из (13;0) к x²+y²=25?", 12, "Тема: 12.", "circle", r=5, d=False),
        item("Хорды пересекаются: 4·9=6·x. x?", 6, "Тема: 36=6x.", "circle", r=10, d=False),
        item("5·12=6·x. x?", 10, "Тема: 10.", "circle", r=12, d=False),
        item("Касательная 12, внешняя секущей 8. Вся секущая?", 18, "Тема: 144=8s, s=18.", "circle", r=10, d=False),
        item("Внутренний отрезок секущей при касательной 12 и внешней 8?", 10, "Тема: 18−8=10.", "circle", r=10, d=False),
        item("Две касательные из точки равны. Одна 17. Вторая?", 17, "Тема: 17.", "circle", r=8, d=False),
        item("Угол между касательной и хордой равен вписанному. Дуга 84°. Угол?", 42, "Тема: 42°.", "circle", r=8, d=False),
        item("Вписанный четырёхугольник, углы 80° и 70° соседние. Противоположный к 80°?", 100, "Тема: 100°.", "rect", a=8, b=6),
        item("Описанный четырёхугольник стороны 9, 12, 15, x. x?", 12, "Тема: 9+15=12+x, x=12.", "para", a=15, h=8),
        item("Теорема синусов: a=15, A=150°, sin 150=1/2. 2R=a/sin A?", 30, "Тема: 30.", "circle", r=15, d=True),
        item("R=15 при a=15 и A=150°. Проверка 2R?", 30, "Тема: 30.", "circle", r=15, d=True),
        item("Стороны 7 и 24, угол 90°. Площадь?", 84, "Тема: 84.", "right", a=7, b=24, c=25),
        item("1/2·15·20·sin 90°?", 150, "Тема: 150.", "right", a=15, b=20, c=25),
        item("1/2·10·10·sin 120°, sin 120=√3/2. Площадь 25√3. Коэффициент при √3?", 25, "Тема: 25√3.", "iso", base=10, equal=10),
        item("Параллелограмм 9 и 12, sin=1/3. Площадь?", 36, "Тема: 108×1/3=36.", "para", a=12, h=3),
        item("Ромб диагонали 16 и 30. Площадь?", 240, "Тема: 240.", "para", a=16, h=15),
        item("Ромб диагонали 16 и 30. Сторона?", 17, "Тема: 8-15-17.", "para", a=30, h=16),
        item("Трапеция 9 и 21, h=8. Площадь?", 120, "Тема: 15×8=120.", "para", a=21, h=8),
        item("Средняя линия трапеции 14, h=9. Площадь?", 126, "Тема: 126.", "para", a=14, h=9),
        item("Гомотетия k=4, площадь малого 5. Площадь большого?", 80, "Тема: ×16.", "triangle", base=20, height=8),
        item("k=1/3, площадь большого 90. Площадь малого?", 10, "Тема: 90×1/9=10.", "triangle", base=6, height=6),
        item("Периметры 21 и 35. k большего к меньшему как 5/3. Числитель?", 5, "Тема: 35:21=5/3.", "triangle", base=15, height=8),
        item("Векторный: точка делит AB в отношении 1:2 от A. A(0;0), B(9;6). Абсцисса?", 3, "Тема: 9×1/3=3.", "vector", vx=3, vy=2),
        item("Деление AB 1:2 от A, B(9;6). Ордината?", 2, "Тема: 2.", "vector", vx=3, vy=2),
        item("Середина A(−4; 7) и B(10; −1). Абсцисса?", 3, "Тема: 3.", "rect", a=14, b=8),
        item("Середина A(−4; 7) и B(10; −1). Ордината?", 3, "Тема: 3.", "rect", a=14, b=8),
        item("Поворот 90°: (5; 2) → (−2; 5). Ордината образа?", 5, "Тема: (−y; x).", "vector", vx=-2, vy=5),
        item("Поворот 90° по часовой (x;y)→(y; −x): (5; 2). Абсцисса?", 2, "Тема: (2; −5).", "vector", vx=2, vy=-5),
        item("Симметрия относительно оси Ox, затем Oy, точка (4; −3). Абсцисса образа?", -4, "Тема: Ox даёт (4; 3), Oy даёт (−4; 3).", "vector", vx=-4, vy=3),
        item("Симметрия относительно O точки (4; −3). Ордината?", 3, "Тема: (−4; 3).", "vector", vx=-4, vy=3),
        item("Дуга 40°, r=18, π=3. Длина дуги? C=108, 40/360=1/9, 12.", 12, "Тема: 12.", "circle", r=18, d=False),
        item("Сектор 40°, r=18, π=3. Площадь? S=3·324=972, /9=108.", 108, "Тема: 108.", "circle", r=18, d=False),
        item("Кольцо R=10, r=6, π=3. Площадь 3(100−36)?", 192, "Тема: 3×64=192.", "circle", r=10, d=False),
        item("Кольцо R=14, r=7, π=22/7. Площадь 22/7 (196−49)=22/7×147.", 462, "Тема: 462.", "circle", r=14, d=False),
        item("Формула площади 1/2 R² (α в радианах). α=π, R=7, π=22/7. Полукруг?", 77, "Тема: 77.", "circle", r=7, d=False),
        item("sin 15° не табличный. sin 180=0. Запишите 0.", 0, "Тема: sin 180°=0.", "angle", deg=180),
        item("cos 180° равен?", -1, "Тема: −1.", "angle", deg=180),
        item("sin 270° равен?", -1, "Тема: −1.", "angle", deg=90),
        item("cos 270° равен?", 0, "Тема: 0.", "angle", deg=90),
        item("tg 180° равен?", 0, "Тема: 0.", "angle", deg=180),
        item("Период синуса в градусах?", 360, "Тема: 360°.", "angle", deg=360),
        item("sin(180−α)=sin α. α=40. sin 140°. Если sin 40=0,64 не. Равенство: sin 140 / sin 40 = ?", 1, "Тема: 1.", "angle", deg=140),
        item("cos(180−α)=−cos α. Для α=0, cos 180?", -1, "Тема: −1.", "angle", deg=180),
        item("Треугольник со сторонами 9, 10 и 17 см. Периметр?", 36, "Тема: 36.", "triangle", base=17, height=6),
        item("Неравенство треугольника: 3, 4, x максимум строго меньше 7. Наибольшее целое x?", 6, "Тема: x<7.", "triangle", base=6, height=4),
        item("3, 4, x минимум больше 1. Наименьшее целое x?", 2, "Тема: x>1.", "triangle", base=3, height=4),
        item("Скалярное произведение единичных векторов i и j?", 0, "Тема: 0.", "vector", vx=0, vy=1),
        item("Скалярное произведение вектора i самого на себя?", 1, "Тема: 1.", "vector", vx=1, vy=0),
        item("Вектор a = 3i + 4j. Найдите длину вектора a.", 5, "Тема: корень из (9+16)=5.", "vector", vx=3, vy=4),
        item("Вектор a = 12i - 5j. Найдите длину вектора a.", 13, "Тема: корень из (144+25)=13.", "vector", vx=12, vy=-5),
        item("Сила F=(3; 4), перемещение s=(2; 1). Скалярное произведение F и s?", 10, "Тема: 6+4=10.", "vector", vx=2, vy=1),
        item("Сила F=(5; 0), перемещение (0; 6). Скалярное произведение F и s?", 0, "Тема: 0.", "vector", vx=0, vy=6),
        item("Высота к стороне 20 при площади 80. Высота?", 8, "Тема: 20·h/2=80.", "triangle", base=20, height=8),
        item("Основание 18, площадь 54. Высота?", 6, "Тема: 6.", "triangle", base=18, height=6),
        item("Диагонали ромба 20 и 21. Площадь?", 210, "Тема: 210.", "para", a=21, h=10),
        item("Ромб с диагоналями 12 см и 16 см. Сторона в см?", 10, "Тема: половины 6 и 8, сторона 10.", "para", a=16, h=12),
        item("Ромб диагонали 12 и 16. Сторона?", 10, "Тема: 10.", "para", a=16, h=12),
        item("Правильный шестиугольник сторона 4. Длинная диагональ (2a)?", 8, "Тема: 8.", "square", a=4),
        item("Правильный шестиугольник сторона 5. Радиус описанной (равен стороне)?", 5, "Тема: R=a=5.", "circle", r=5, d=False),
        item("Правильный шестиугольник сторона 6. Радиус вписанной 3√3. Периметр?", 36, "Тема: 36.", "square", a=6),
        item("Площадь правильного шестиугольника 6 равносторонних со стороной 2. Один равносторонний S=√3. Шесть — коэффициент при √3?", 6, "Тема: 6√3 при a=2, S=√3 для одного.", "square", a=2),
        item("Шесть равносторонних со стороной 2, площадь одного √3. Суммарная площадь как k√3. k?", 6, "Тема: 6.", "square", a=2),
        item("Длина окружности 2πR = 10π. Радиус?", 5, "Тема: 5.", "circle", r=5, d=False),
        item("Площадь πR²=49π. Радиус?", 7, "Тема: 7.", "circle", r=7, d=False),
        item("Площадь 36π. Радиус?", 6, "Тема: 6.", "circle", r=6, d=False),
        item("Длина 14π. Диаметр?", 14, "Тема: 14.", "circle", r=7, d=True),
    ]
    for n in range(4, 16):
        rows.append(item(
            f"Вектор ({n}; 0). Найдите длину.",
            n,
            f"Вторая координата равна 0, поэтому длина равна модулю первой координаты: {n}.",
            "vector", vx=n, vy=0,
        ))
        rows.append(item(
            f"Точки (0; 0) и ({n}; {n}). Найдите квадрат расстояния.",
            2 * n * n,
            f"Квадрат расстояния = {n}×{n} + {n}×{n} = {2 * n * n}.",
            "right", a=n, b=n, c=n,
        ))
        rows.append(item(
            f"Гомотетия с коэффициентом {min(n, 9)}. Отрезок 3 см. Длина образа?",
            3 * min(n, 9),
            f"При гомотетии длины умножаются на коэффициент: 3 × {min(n, 9)} = {3 * min(n, 9)} см.",
            "triangle", base=3 * min(n, 9), height=6,
        ))
    for r in rows:
        if isinstance(r["answer"], float):
            val = r["answer"]
            if val == int(val):
                r["answer"] = str(int(val))
            else:
                r["answer"] = str(val).replace(".", ",")
    return take_unique(rows, 100, "high")


def sql_escape(value: str) -> str:
    return str(value).replace("'", "''")


def write_pack(level: str, letter: str, slug: str, rows: list[dict], expected: int) -> None:
    if len(rows) != expected:
        raise SystemExit(f"{level}: {len(rows)} ≠ {expected}")
    TASKS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    csv_name = f"geometry-9-{slug}.csv"
    sql_name = f"insert-geometry-9-{slug}.sql"
    fieldnames = ["subject", "class_name", "level", "question", "answer", "image", "explanation_of_the_answer"]
    csv_rows = []
    sql_values = []
    for i, row in enumerate(rows, start=1):
        filename = f"ge9-{letter}-{i:02d}.svg"
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
