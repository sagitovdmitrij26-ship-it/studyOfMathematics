# -*- coding: utf-8 -*-
"""Геометрия 8 класс: 70/80/100 задач и схемы SVG."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TASKS = ROOT / "public" / "tasks"
CLASS = "8 класс"

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
  <text x="56" y="72" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="700" fill="{ink}">Геометрия · 8 класс</text>
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
    for a, b in [(7, 5), (9, 4), (11, 6), (8, 3), (12, 5), (13, 7), (10, 6), (15, 4), (14, 8), (16, 9)]:
        rows.append(item(
            f"Параллелограмм со сторонами {a} см и {b} см. Периметр в см.",
            2 * (a + b),
            f"Тема: 2×({a}+{b})={2*(a+b)}.",
            "para", a=a, h=max(3, b),
        ))
        rows.append(item(
            f"В параллелограмме сторона {a} см. Противоположная сторона в см.",
            a,
            f"Тема: противоположные стороны равны. {a}.",
            "para", a=a, h=b,
        ))
    for d in (40, 50, 55, 60, 70, 75, 80, 100, 110, 120, 130, 140):
        rows.append(item(
            f"В параллелограмме угол {d}°. Противоположный угол?",
            d,
            f"Тема: противоположные углы равны. {d}°.",
            "para", a=10, h=6,
        ))
        rows.append(item(
            f"В параллелограмме угол {d}°. Соседний угол?",
            180 - d,
            f"Тема: сумма соседних 180°. {180-d}°.",
            "angle", deg=d,
        ))
        rows.append(item(
            f"В прямоугольнике один угол {d}° быть не может, если не 90. Угол прямоугольника?",
            90,
            "Тема: все углы прямоугольника 90°.",
            "rect", a=10, b=6,
        ))
    for a in (5, 6, 7, 8, 9, 10, 12, 15):
        rows.append(item(
            f"Ромб со стороной {a} см. Периметр в см.",
            4 * a,
            f"Тема: 4×{a}={4*a}.",
            "para", a=a, h=a - 1 if a > 3 else 3,
        ))
        rows.append(item(
            f"Квадрат со стороной {a} см. Периметр в см.",
            4 * a,
            f"Тема: 4×{a}={4*a}.",
            "square", a=a,
        ))
        rows.append(item(
            f"Квадрат со стороной {a} см. Площадь в см².",
            a * a,
            f"Тема: {a}²={a*a}.",
            "square", a=a,
        ))
    for a, h in [(8, 3), (10, 4), (12, 5), (9, 6), (14, 4), (15, 5), (11, 7), (16, 3)]:
        rows.append(item(
            f"Параллелограмм: основание {a} см, высота {h} см. Площадь в см².",
            a * h,
            f"Тема: S=a·h={a*h}.",
            "para", a=a, h=h,
        ))
    for b, h in [(8, 6), (10, 4), (12, 8), (14, 6), (9, 8), (16, 5)]:
        if (b * h) % 2:
            continue
        rows.append(item(
            f"Треугольник: основание {b} см, высота {h} см. Площадь в см².",
            b * h // 2,
            f"Тема: S=a·h/2={b*h//2}.",
            "triangle", base=b, height=h,
        ))
    for a, b in [(6, 10), (4, 12), (5, 15), (8, 14), (7, 13), (9, 17)]:
        rows.append(item(
            f"Трапеция с основаниями {a} см и {b} см. Средняя линия в см.",
            (a + b) // 2,
            f"Тема: ({a}+{b})/2={(a+b)//2}.",
            "para", a=b, h=5,
        ))
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]
    for a, b, c in triples:
        rows.append(item(
            f"Катеты {a} см и {b} см. Гипотенуза в см.",
            c,
            f"Тема: теорема Пифагора. {c}.",
            "right", a=a, b=b, c=c,
        ))
    rows += [
        item("Диагонали прямоугольника равны. Одна 10 см. Вторая?", 10, "Тема: диагонали прямоугольника равны.", "rect", a=8, b=6),
        item("Диагонали ромба взаимно перпендикулярны. Угол между ними?", 90, "Тема: 90°.", "para", a=8, h=6),
        item("Диагонали параллелограмма точкой пересечения делятся пополам. Отрезок 12 см, половина?", 6, "Тема: 6.", "para", a=10, h=5),
        item("Все стороны ромба равны. Сторона 9. Соседняя сторона?", 9, "Тема: все стороны равны.", "para", a=9, h=5),
        item("В квадрате диагонали равны и перпендикулярны. Угол между ними?", 90, "Тема: 90°.", "square", a=8),
        item("Сумма углов выпуклого четырёхугольника?", 360, "Тема: 360°.", "rect", a=8, b=6),
        item("Каждый угол прямоугольника?", 90, "Тема: 90°.", "rect", a=8, b=5),
        item("Каждый угол квадрата?", 90, "Тема: 90°.", "square", a=6),
        item("В равнобедренной трапеции углы при основании равны. Один 70°. Второй при том же основании?", 70, "Тема: равны.", "para", a=12, h=5),
        item("В трапеции сумма углов при боковой стороне 180°. Угол 65°. Второй при этой боковой?", 115, "Тема: 180−65=115.", "para", a=12, h=5),
        item("Средняя линия треугольника параллельна основанию 18 см. Длина средней линии?", 9, "Тема: половина основания.", "triangle", base=18, height=8),
        item("Основание треугольника 24 см. Средняя линия?", 12, "Тема: 12.", "triangle", base=24, height=9),
        item("Подобные треугольники, коэффициент 2. Сторона 7 см. Соответствующая?", 14, "Тема: 7×2=14.", "triangle", base=14, height=8),
        item("Подобные, стороны 5 см и 15 см. Коэффициент большего к меньшему?", 3, "Тема: 15:5=3.", "triangle", base=15, height=8),
        item("Центральный угол 80°. Вписанный, опирающийся на ту же дугу?", 40, "Тема: вписанный вдвое меньше.", "circle", r=8, d=False),
        item("Центральный угол 120°. Вписанный на ту же дугу?", 60, "Тема: 60°.", "circle", r=8, d=False),
        item("Вписанный угол опирается на диаметр. Чему он равен?", 90, "Тема: угол в полуокружности.", "circle", r=8, d=True),
        item("Диаметр 16 см. Радиус?", 8, "Тема: 8.", "circle", r=8, d=True),
        item("Радиус 11 см. Диаметр?", 22, "Тема: 22.", "circle", r=11, d=True),
        item("Касательная перпендикулярна радиусу. Угол?", 90, "Тема: 90°.", "circle", r=7, d=False),
        item("Две касательные из одной точки. Одна 13 см. Вторая?", 13, "Тема: отрезки касательных равны.", "circle", r=6, d=False),
        item("sin 30° равен 1/2. Запишите числитель дроби 1/n: чему n?", 2, "Тема: sin 30°=1/2.", "right", a=1, b=2, c=2),
        item("cos 60° равен 1/2. Знаменатель дроби 1/n?", 2, "Тема: cos 60°=1/2.", "right", a=1, b=2, c=2),
        item("tg 45° равен?", 1, "Тема: tg 45°=1.", "right", a=5, b=5, c=7),
        item("В прямоугольном треугольнике sin α = противолежащий/гипотенуза. Катет 3, гипотенуза 6. sin?", "0,5", "Тема: 3/6=0,5.", "right", a=3, b=4, c=6),
        item("Катет против 30° равен половине гипотенузы 10. Этот катет?", 5, "Тема: 5.", "right", a=5, b=9, c=10),
        item("Гипотенуза 14, угол 30°. Катет против 30°?", 7, "Тема: 7.", "right", a=7, b=12, c=14),
        item("Прямоугольник 6×8. Диагональ?", 10, "Тема: 6-8-10.", "rect", a=6, b=8),
        item("Прямоугольник 5×12. Диагональ?", 13, "Тема: 5-12-13.", "rect", a=5, b=12),
        item("Квадрат сторона 8. Площадь?", 64, "Тема: 64.", "square", a=8),
        item("Ромб диагонали 6 и 8. Площадь?", 24, "Тема: d1·d2/2=24.", "para", a=8, h=6),
        item("Трапеция основания 6 и 10, высота 4. Площадь?", 32, "Тема: (6+10)/2×4=32.", "para", a=10, h=4),
        item("Параллелограмм углы 2x и 100, соседние. Найдите x.", 40, "Тема: 2x+100=180, x=40.", "para", a=10, h=5),
        item("В ромбе угол 50°. Соседний?", 130, "Тема: 130°.", "para", a=8, h=5),
        item("В ромбе угол 50°. Противоположный?", 50, "Тема: 50°.", "para", a=8, h=5),
        item("Теорема Фалеса: параллельная средняя режет стороны пополам. Отрезок 10, соответствующий?", 10, "Тема: равные отношения 1:1.", "triangle", base=10, height=8),
        item("Стороны 8 и 12 разделены пропорционально 1:1. Меньший отрезок на стороне 8?", 4, "Тема: 4.", "triangle", base=8, height=6),
        item("Выпуклый четырёхугольник, три угла 80, 90 и 110. Четвёртый?", 80, "Тема: 360−280=80.", "rect", a=8, b=6),
        item("Сколько сторон у восьмиугольника?", 8, "Тема: 8.", "square", a=8),
        item("Правильный шестиугольник, внутренний угол?", 120, "Тема: 120°.", "square", a=6),
        item("Сумма углов шестиугольника?", 720, "Тема: (6−2)×180=720.", "square", a=6),
        item("Диагоналей у четырёхугольника?", 2, "Тема: 2.", "rect", a=8, b=6),
        item("Окружность описана около прямоугольника 6×8. Диаметр равен диагонали. Диаметр?", 10, "Тема: 10.", "rect", a=6, b=8),
        item("Вписанная в квадрат сторона 10. Радиус?", 5, "Тема: r=a/2=5.", "square", a=10),
        item("В квадрат со стороной 6 см вписана окружность. Радиус в см?", 3, "Тема: r=a/2=3.", "square", a=6),
    ]
    return take_unique(rows, 70, "basic")


def medium() -> list[dict]:
    rows = []
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17), (7, 24, 25)]
    for a, b, c in triples:
        rows.append(item(
            f"Гипотенуза {c} см, катет {a} см. Второй катет в см.",
            b,
            f"Тема: √({c}²−{a}²)={b}.",
            "right", a=a, b=b, c=c,
        ))
        rows.append(item(
            f"Катеты {a} и {b}. Площадь прямоугольного треугольника в см².",
            a * b // 2,
            f"Тема: {a*b//2}.",
            "right", a=a, b=b, c=c,
        ))
        rows.append(item(
            f"Прямоугольный {a}-{b}-{c}. Периметр в см.",
            a + b + c,
            f"Тема: {a+b+c}.",
            "right", a=a, b=b, c=c,
        ))
    for d1, d2 in [(6, 8), (10, 24), (12, 16), (8, 10), (14, 48), (18, 24)]:
        rows.append(item(
            f"Ромб с диагоналями {d1} см и {d2} см. Площадь в см².",
            d1 * d2 // 2,
            f"Тема: d1·d2/2={d1*d2//2}.",
            "para", a=d2, h=d1,
        ))
    for a, b, h in [(5, 11, 4), (6, 14, 5), (8, 12, 6), (7, 13, 8), (4, 16, 5), (9, 15, 4), (10, 18, 3)]:
        rows.append(item(
            f"Трапеция основания {a} и {b} см, высота {h} см. Площадь в см².",
            (a + b) * h // 2,
            f"Тема: ({a}+{b})/2×{h}={(a+b)*h//2}.",
            "para", a=b, h=h,
        ))
    for k, side in [(2, 6), (3, 5), (4, 7), (2, 9), (5, 4), (3, 8)]:
        rows.append(item(
            f"Подобие, коэффициент {k}. Сторона {side} см. Соответствующая в большем?",
            k * side,
            f"Тема: {k}×{side}={k*side}.",
            "triangle", base=k * side, height=8,
        ))
        rows.append(item(
            f"Подобие k={k}. Периметр малого {4*side}. Периметр большого?",
            k * 4 * side,
            f"Тема: периметры как k. {k*4*side}.",
            "triangle", base=k * side, height=7,
        ))
        rows.append(item(
            f"Подобие k={k}. Площадь малого 10. Площадь большого?",
            10 * k * k,
            f"Тема: площади как k². {10*k*k}.",
            "triangle", base=k * 6, height=8,
        ))
    for r in (7, 14, 21):
        rows.append(item(
            f"Окружность r={r} см, π=22/7. Длина окружности в см.",
            2 * 22 * r // 7,
            f"Тема: 2πr={2*22*r//7}.",
            "circle", r=r, d=False,
        ))
        rows.append(item(
            f"Круг r={r} см, π=22/7. Площадь в см².",
            22 * r * r // 7,
            f"Тема: πr²={22*r*r//7}.",
            "circle", r=r, d=False,
        ))
    rows += [
        item("Круг r=10, π=3,14. Площадь?", 314, "Тема: 3,14×100=314.", "circle", r=10, d=False),
        item("Круг r=10, π=3,14. Длина окружности. Ответ через запятую.", "62,8", "Тема: 2×3,14×10=62,8.", "circle", r=10, d=False),
        item("Центральный 70°. Вписанный на ту же дугу?", 35, "Тема: 35°.", "circle", r=8, d=False),
        item("Вписанный 42°. Центральный на ту же дугу?", 84, "Тема: 84°.", "circle", r=8, d=False),
        item("Дуга 100°. Вписанный на эту дугу?", 50, "Тема: 50°.", "circle", r=8, d=False),
        item("Хорда 16 см, расстояние от центра 6 см. Радиус?", 10, "Тема: 6²+8²=100.", "circle", r=10, d=False),
        item("Хорда 10 см, радиус 13 см. Расстояние от центра?", 12, "Тема: 5-12-13.", "circle", r=13, d=False),
        item("Диаметр делит хорду пополам и перпендикулярен ей. Хорда 12. Половина?", 6, "Тема: 6.", "circle", r=10, d=True),
        item("Средняя линия трапеции 11, высота 6. Площадь?", 66, "Тема: m·h=66.", "para", a=11, h=6),
        item("Средняя линия трапеции 9, высота 8. Площадь?", 72, "Тема: 72.", "para", a=9, h=8),
        item("Основания трапеции 3x и x, средняя линия 16. Большее основание?", 24, "Тема: 2x=16, x=8, большее 24.", "para", a=24, h=5),
        item("Равнобедренная трапеция основания 6 и 14, боковая 5. Высота?", 3, "Тема: вынос 4, треугольник 3-4-5.", "right", a=3, b=4, c=5),
        item("Ромб диагонали 12 и 16. Сторона?", 10, "Тема: половины 6 и 8, гипотенуза 10.", "para", a=16, h=12),
        item("Ромб сторона 13, высота 5. Площадь?", 65, "Тема: a·h=65.", "para", a=13, h=5),
        item("Параллелограмм стороны 7 и 10, высота к стороне 10 равна 6. Площадь?", 60, "Тема: 10×6=60.", "para", a=10, h=6),
        item("Площадь параллелограмма 48, основание 8. Высота?", 6, "Тема: 48:8=6.", "para", a=8, h=6),
        item("Площадь треугольника 36, основание 12. Высота?", 6, "Тема: 12·h/2=36, h=6.", "triangle", base=12, height=6),
        item("Площадь треугольника 45, высота 9. Основание?", 10, "Тема: a·9/2=45, a=10.", "triangle", base=10, height=9),
        item("Прямоугольник 9×12. Диагональ?", 15, "Тема: 9-12-15.", "rect", a=9, b=12),
        item("Прямоугольник 8×15. Диагональ?", 17, "Тема: 8-15-17.", "rect", a=8, b=15),
        item("Квадрат площадь 121. Сторона?", 11, "Тема: √121=11.", "square", a=11),
        item("Периметр ромба 56. Сторона?", 14, "Тема: 14.", "para", a=14, h=7),
        item("В параллелограмме угол 2x+10, соседний 3x−5. Найдите x.", 35, "Тема: 5x+5=180, x=35.", "para", a=10, h=6),
        item("Противоположные углы параллелограмма 3x−6 и 54. x?", 20, "Тема: 3x=60, x=20.", "para", a=10, h=6),
        item("Подобие: периметры 18 и 27. Коэффициент большего к меньшему?", "1,5", "Тема: 27:18=1,5.", "triangle", base=27, height=9),
        item("Подобие k=2, площадь большого 40. Площадь малого?", 10, "Тема: 40:4=10.", "triangle", base=10, height=8),
        item("Стороны треугольника 6, 8, 10 увеличены в 3 раза. Большая сторона?", 30, "Тема: 10×3=30.", "right", a=18, b=24, c=30),
        item("sin 30° · гипотенуза 16. Противолежащий катет?", 8, "Тема: 16×1/2=8.", "right", a=8, b=8, c=16),
        item("cos 60° · гипотенуза 20. Прилежащий катет?", 10, "Тема: 20×1/2=10.", "right", a=10, b=17, c=20),
        item("tg 45° = 1. Катет прилежащий 9. Противолежащий?", 9, "Тема: равны.", "right", a=9, b=9, c=13),
        item("Катет 5, гипотенуза 13. cos острого при этом катете как 5/13. Числитель?", 5, "Тема: прилежащий/гипотенуза.", "right", a=5, b=12, c=13),
        item("Около прямоугольного треугольника 5-12-13 описана окружность. Радиус?", "6,5", "Тема: R=c/2=6,5.", "right", a=5, b=12, c=13),
        item("Гипотенуза 26. Радиус описанной окружности?", 13, "Тема: 13.", "right", a=10, b=24, c=26),
        item("Вписанная в прямоугольный: r=(a+b−c)/2. Для 6-8-10 r?", 2, "Тема: (6+8−10)/2=2.", "right", a=6, b=8, c=10),
        item("Для 5-12-13 радиус вписанной?", 2, "Тема: (5+12−13)/2=2.", "right", a=5, b=12, c=13),
        item("Высота к гипотенузе 6-8-10. Площадь 24, h?", "4,8", "Тема: 10·h/2=24, h=4,8.", "right", a=6, b=8, c=10),
        item("Теорема Фалеса: на стороне отрезки 3 и 6, на другой меньший 4. Больший?", 8, "Тема: 4:8=3:6.", "triangle", base=12, height=8),
        item("Пропорция 2:5 = 6:x. Найдите x.", 15, "Тема: x=15.", "triangle", base=15, height=6),
        item("Пропорция 4:7 = 12:x. x?", 21, "Тема: 21.", "triangle", base=21, height=8),
        item("Правильный восьмиугольник, сумма внутренних углов?", 1080, "Тема: (8−2)×180=1080.", "square", a=8),
        item("Каждый угол правильного восьмиугольника?", 135, "Тема: 1080/8=135.", "square", a=8),
        item("Диагоналей у восьмиугольника?", 20, "Тема: n(n−3)/2=20.", "square", a=8),
        item("Диагоналей у десятиугольника?", 35, "Тема: 35.", "square", a=10),
        item("Сумма внешних углов выпуклого многоугольника?", 360, "Тема: всегда 360°.", "square", a=6),
        item("Четверть круга r=14, π=22/7. Длина дуги?", 22, "Тема: 88/4=22.", "circle", r=14, d=False),
        item("Четверть круга r=7, π=22/7. Площадь сектора. Ответ 38,5", "38,5", "Тема: 154/4=38,5.", "circle", r=7, d=False),
        item("Сектор 90°, r=14, π=22/7. Площадь сектора?", 154, "Тема: 616/4=154.", "circle", r=14, d=False),
        item("Из квадрата 12×12 вырезали 4×4. Остаток площади?", 128, "Тема: 144−16=128.", "square", a=12),
        item("Рамка: внешний квадрат 10, внутренний 6. Площадь рамки?", 64, "Тема: 100−36=64.", "square", a=10),
        item("Дом: прямоугольник 12×5 и треугольная крыша основание 12 высота 4. Площадь фасада?", 84, "Тема: 60+24=84.", "rect", a=12, b=5),
        item("Лестница: высота 9, от стены 12. Длина?", 15, "Тема: 9-12-15.", "right", a=9, b=12, c=15),
        item("Экран: диагональ 25, сторона 7. Другая сторона?", 24, "Тема: 7-24-25.", "right", a=7, b=24, c=25),
        item("Расстояние между точками (0;0) и (6;8)?", 10, "Тема: √(36+64)=10.", "right", a=6, b=8, c=10),
        item("Расстояние (0;0) и (5;12)?", 13, "Тема: 13.", "right", a=5, b=12, c=13),
        item("Середина отрезка от (0;0) до (8;4). Ордината середины?", 2, "Тема: 4/2=2.", "rect", a=8, b=4),
        item("Середина от (2;2) до (8;10). Абсцисса середины?", 5, "Тема: (2+8)/2=5.", "rect", a=8, b=6),
        item("Точки A(1;0) и B(7;0). Длина отрезка AB?", 6, "Тема: 6.", "rect", a=6, b=2),
        item("В равнобедренном основание 12, боковые 10. Высота к основанию?", 8, "Тема: 6-8-10.", "iso", base=12, equal=10),
        item("Основание 20, боковые 26. Высота?", 24, "Тема: 10-24-26.", "iso", base=20, equal=26),
        item("Прямоугольник со сторонами 6 см и 8 см. Периметр в см?", 28, "Тема: 28.", "rect", a=6, b=8),
    ]
    for n in range(3, 16):
        rows.append(item(
            f"Правильный {n}-угольник со стороной 8 см. Периметр в см.",
            8 * n,
            f"Тема: {n}×8={8*n}.",
            "square", a=8,
        ))
        rows.append(item(
            f"Параллелограмм стороны {n+2} и {n} см. Периметр.",
            2 * (2 * n + 2),
            f"Тема: 2({n+2}+{n})={2*(2*n+2)}.",
            "para", a=n + 2, h=n,
        ))
    return take_unique(rows, 80, "medium")


def high() -> list[dict]:
    rows = []
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 35, 37), (9, 40, 41)]
    for a, b, c in triples:
        rows.append(item(
            f"Катеты {a} и {b} см. Гипотенуза в см.",
            c,
            f"Тема: Пифагор. {c}.",
            "right", a=a, b=b, c=c,
        ))
        rows.append(item(
            f"Гипотенуза {c}, катет {b}. Второй катет?",
            a,
            f"Тема: {a}.",
            "right", a=a, b=b, c=c,
        ))
        rows.append(item(
            f"Прямоугольник {a}×{b}. Диагональ?",
            c,
            f"Тема: {c}.",
            "rect", a=a, b=b,
        ))
    rows += [
        item("Пересекающиеся хорды: отрезки 4 и 6, третий 3. Четвёртый?", 8, "Тема: 4×6=3×x, x=8.", "circle", r=10, d=False),
        item("Хорды: 5 и 8, третий 4. Четвёртый?", 10, "Тема: 5×8=4×x, x=10.", "circle", r=12, d=False),
        item("Хорды: 6 и 9, третий 2. Четвёртый?", 27, "Тема: 6×9=2×x, x=27.", "circle", r=14, d=False),
        item("Касательная 6, внешняя часть секущей 4. Вся секущая?", 9, "Тема: 6²=4·s, s=9.", "circle", r=8, d=False),
        item("Касательная 8, внешняя часть секущей 4. Вся секущая?", 16, "Тема: 64=4s, s=16.", "circle", r=10, d=False),
        item("Касательная 10, внешняя часть 5. Внутренний отрезок секущей?", 15, "Тема: 100=5(5+x), 20=5+x, x=15.", "circle", r=12, d=False),
        item("Вписанный четырёхугольник: сумма противоположных углов 180. Угол 70°. Противоположный?", 110, "Тема: 110°.", "rect", a=8, b=6),
        item("Вписанный четырёхугольник, угол 95°. Противоположный?", 85, "Тема: 85°.", "rect", a=9, b=6),
        item("Описанный четырёхугольник: суммы противоположных сторон равны. Стороны 5, 8, 7, x. x?", 4, "Тема: 5+7=8+x, x=4.", "para", a=8, h=5),
        item("Описанный: стороны 6, 9, 10, x. x?", 7, "Тема: 6+10=9+x, x=7.", "para", a=10, h=6),
        item("Ромб диагонали 18 и 24. Сторона?", 15, "Тема: 9-12-15.", "para", a=24, h=18),
        item("Ромб диагонали 10 и 24. Сторона?", 13, "Тема: 5-12-13.", "para", a=24, h=10),
        item("Площадь ромба 96, одна диагональ 12. Вторая?", 16, "Тема: 12·d/2=96, d=16.", "para", a=16, h=12),
        item("Площадь ромба 120, диагональ 10. Вторая?", 24, "Тема: 24.", "para", a=24, h=10),
        item("Трапеция 5 и 19, h=7. Площадь?", 84, "Тема: 12×7=84.", "para", a=19, h=7),
        item("Трапеция 8 и 20, h=9. Площадь?", 126, "Тема: 14×9=126.", "para", a=20, h=9),
        item("Средняя линия трапеции 13, h=8. Площадь?", 104, "Тема: 104.", "para", a=13, h=8),
        item("Подобие k=3, площадь малого 12. Площадь большого?", 108, "Тема: 12×9=108.", "triangle", base=18, height=12),
        item("Подобие: площади 16 и 64. Коэффициент линейный?", 2, "Тема: √(64/16)=2.", "triangle", base=16, height=8),
        item("Подобие: площади 9 и 81. k большего к меньшему?", 3, "Тема: 3.", "triangle", base=18, height=9),
        item("Периметры подобных 20 и 50. Сторона 8 в меньшем. Соответствующая?", 20, "Тема: k=2,5, 8×2,5=20.", "triangle", base=20, height=8),
        item("Прямоугольный, угол 30°, гипотенуза 18. Катет против 30°?", 9, "Тема: 9.", "right", a=9, b=16, c=18),
        item("В треугольнике 30°-60°-90° катет против 30° равен 6. Гипотенуза?", 12, "Тема: 12.", "right", a=6, b=10, c=12),
        item("В треугольнике 30°-60°-90° гипотенуза 16. Катет против 30°?", 8, "Тема: 8.", "right", a=8, b=14, c=16),
        item("tg α = 3/4, прилежащий катет 8. Противолежащий?", 6, "Тема: 3/4=x/8, x=6.", "right", a=6, b=8, c=10),
        item("sin α = 5/13, гипотенуза 26. Противолежащий катет?", 10, "Тема: 26×5/13=10.", "right", a=10, b=24, c=26),
        item("cos α = 12/13, гипотенуза 26. Прилежащий катет?", 24, "Тема: 24.", "right", a=10, b=24, c=26),
        item("Высота к гипотенузе: катеты 9 и 12, гипотенуза 15. h=S·2/c. h?", "7,2", "Тема: S=54, h=108/15=7,2.", "right", a=9, b=12, c=15),
        item("Проекция катета 6 на гипотенузу 10 в треугольнике 6-8-10. Проекция катета 6?", "3,6", "Тема: a²=c·p, 36=10p, p=3,6.", "right", a=6, b=8, c=10),
        item("Проекция катета 8 на гипотенузу 10?", "6,4", "Тема: 64=10p, p=6,4.", "right", a=6, b=8, c=10),
        item("Параллелограмм стороны 13 и 14, диагональ 15. Можно ли 13-14-15? Периметр?", 54, "Тема: 2(13+14)=54.", "para", a=14, h=8),
        item("Площадь параллелограмма 72, высоты 8 и 9. Сторона, к которой высота 8?", 9, "Тема: a·8=72, a=9.", "para", a=9, h=8),
        item("Сторона, к которой высота 9, при S=72?", 8, "Тема: 72:9=8.", "para", a=8, h=9),
        item("Равнобедренная трапеция основания 10 и 26, высота 6. Боковая сторона?", 10, "Тема: вынос 8, 6-8-10.", "right", a=6, b=8, c=10),
        item("Основания 4 и 20, высота 6. Площадь?", 72, "Тема: 12×6=72.", "para", a=20, h=6),
        item("Вписанный угол 18°. Дуга?", 36, "Тема: дуга вдвое больше.", "circle", r=8, d=False),
        item("Центральный 154°. Вписанный?", 77, "Тема: 77°.", "circle", r=8, d=False),
        item("Угол между касательной и хордой равен вписанному. Хорда стягивает дугу 70°. Угол?", 35, "Тема: 35°.", "circle", r=8, d=False),
        item("Равные хорды. Одна удалена на 7. Другая?", 7, "Тема: равны расстояния.", "circle", r=12, d=False),
        item("Диаметр 26, хорда 10, dist? Половина хорды 5, r=13, dist 12.", 12, "Тема: 5-12-13.", "circle", r=13, d=True),
        item("Круг r=21, π=22/7. Площадь?", 1386, "Тема: 22/7×441=1386.", "circle", r=21, d=False),
        item("Длина окружности 88, π=22/7. Радиус?", 14, "Тема: 2πr=88, r=14.", "circle", r=14, d=False),
        item("Длина 44, π=22/7. Диаметр?", 14, "Тема: πd=44, d=14.", "circle", r=7, d=True),
        item("Сектор 60° круга r=21, π=22/7. Площадь сектора? 1386/6.", 231, "Тема: 60/360=1/6, 1386/6=231.", "circle", r=21, d=False),
        item("Дуга 60°, r=21, π=22/7. Длина дуги? C=132, шестая часть.", 22, "Тема: 132/6=22.", "circle", r=21, d=False),
        item("Сектор 90°, r=14, π=22/7. Периметр сектора (два радиуса и дуга)?", 50, "Тема: 28+22=50.", "circle", r=14, d=False),
        item("Координаты A(1;2), B(4;6). Длина AB?", 5, "Тема: √(9+16)=5.", "right", a=3, b=4, c=5),
        item("A(0;0), B(9;12). Длина?", 15, "Тема: 15.", "right", a=9, b=12, c=15),
        item("Середина A(−2;4) и B(8;10). Абсцисса середины?", 3, "Тема: (−2+8)/2=3.", "rect", a=8, b=6),
        item("Середина A(−2;4) и B(8;10). Ордината?", 7, "Тема: (4+10)/2=7.", "rect", a=8, b=6),
        item("Прямоугольник вершины (0;0),(8;0),(8;6). Площадь?", 48, "Тема: 8×6=48.", "rect", a=8, b=6),
        item("Треугольник (0;0),(10;0),(0;6). Площадь?", 30, "Тема: 10×6/2=30.", "triangle", base=10, height=6),
        item("Дорожка вокруг квадрата 8×8, ширина 2. Площадь дорожки?", 80, "Тема: 12²−8²=80.", "square", a=12),
        item("Из прямоугольника 15×8 вырезали 5×3. Остаток?", 105, "Тема: 120−15=105.", "rect", a=15, b=8),
        item("Три квадрата 6 см в ряд. Периметр ленты?", 48, "Тема: 4×18−2×12=48.", "rect", a=18, b=6),
        item("Два квадрата 7 см общей стороной. Периметр фигуры?", 42, "Тема: 56−14=42.", "square", a=7),
        item("Квадрат из 12 клеток по стороне, клетка 2 см. Сторона квадрата в см?", 24, "Тема: 12×2=24.", "square", a=24),
        item("Сколько квадратов 3×3 в квадрате 12×12?", 16, "Тема: 16.", "square", a=12),
        item("Правильный 12-угольник, сторона 5. Периметр?", 60, "Тема: 60.", "square", a=5),
        item("Сумма углов 10-угольника?", 1440, "Тема: 8×180=1440.", "square", a=10),
        item("Каждый угол правильного 10-угольника?", 144, "Тема: 1440/10=144.", "square", a=10),
        item("Диагоналей у 12-угольника?", 54, "Тема: 12×9/2=54.", "square", a=12),
        item("Внешний угол правильного шестиугольника?", 60, "Тема: 360/6=60.", "square", a=6),
        item("Внешний угол правильного восьмиугольника?", 45, "Тема: 360/8=45.", "angle", deg=45),
        item("Внешний угол правильного 9-угольника?", 40, "Тема: 360/9=40.", "angle", deg=40),
        item("Параллельные прямые, секущая. Соответственные 5x−10 и 2x+20. x?", 10, "Тема: 5x−10=2x+20, x=10.", "para", a=10, h=6),
        item("Накрест лежащие 4x+8 и 6x−12. x?", 10, "Тема: 4x+8=6x−12, x=10.", "para", a=10, h=6),
        item("Односторонние 7x и 2x+9. Больший угол? 9x+9=180, x=19, больший 133.", 133, "Тема: 7×19=133.", "angle", deg=133),
        item("Углы подобных относятся как 1. Угол 47° в одном. Соответственный?", 47, "Тема: углы равны.", "triangle", base=10, height=7),
        item("Высоты подобных как k. k=4, высота малого 3. Высота большого?", 12, "Тема: 12.", "triangle", base=16, height=12),
        item("Медианы подобных как k. k=2, медиана 9 в малом. В большом?", 18, "Тема: 18.", "triangle", base=16, height=10),
        item("Равносторонний треугольник со стороной 6 см. Периметр?", 18, "Тема: 18.", "iso", base=6, equal=6),
        item("Равносторонний треугольник со стороной 12 см. Периметр?", 36, "Тема: 36.", "iso", base=12, equal=12),
        item("Площадь равнобедренного основание 16 высота 15?", 120, "Тема: 16×15/2=120.", "iso", base=16, equal=17),
        item("Треугольник со стороной 14 см и высотой к ней 12 см. Площадь?", 84, "Тема: 14×12/2=84.", "triangle", base=14, height=12),
        item("Параллелограмм площадь 60, диагонали не. Основание 12. Высота?", 5, "Тема: 5.", "para", a=12, h=5),
        item("Трапеция с прямой боковой 5 (высота) и основаниями 9 и 16. Площадь?", "62,5", "Тема: 12,5×5=62,5.", "para", a=16, h=5),
        item("Прямоугольная трапеция основания 8 и 14, высота 6. Площадь?", 66, "Тема: 11×6=66.", "para", a=14, h=6),
        item("Боковая наклонная: вынос 8, высота 6. Длина боковой?", 10, "Тема: 6-8-10.", "right", a=6, b=8, c=10),
        item("sin 90° равен?", 1, "Тема: 1.", "angle", deg=90),
        item("cos 0° равен?", 1, "Тема: 1.", "angle", deg=15),
        item("sin 0° равен?", 0, "Тема: 0.", "angle", deg=15),
        item("cos 90° равен?", 0, "Тема: 0.", "angle", deg=90),
        item("tg 0° равен?", 0, "Тема: 0.", "angle", deg=15),
        item("Угол, для которого tg=1, в первой четверти?", 45, "Тема: 45°.", "angle", deg=45),
        item("Два подобных прямоугольных: катеты 6 и 8, в большом катет 12. Второй катет большого?", 16, "Тема: k=2.", "right", a=12, b=16, c=20),
        item("Гипотенуза малого 10, k=3. Гипотенуза большого?", 30, "Тема: 30.", "right", a=18, b=24, c=30),
    ]
    for a in range(4, 18):
        rows.append(item(
            f"Ромб со стороной {a} см. Периметр в см.",
            4 * a,
            f"Тема: {4*a}.",
            "para", a=a, h=max(3, a - 2),
        ))
        rows.append(item(
            f"Квадрат со стороной {a} см. Площадь в см².",
            a * a,
            f"Тема: {a*a}.",
            "square", a=a,
        ))
        rows.append(item(
            f"Правильный шестиугольник сторона {a} см. Периметр.",
            6 * a,
            f"Тема: {6*a}.",
            "square", a=a,
        ))
    for r in rows:
        if r["answer"] in ("4.8", "3.6", "6.4", "7.2", "6.5", "1.5", "62.5"):
            r["answer"] = r["answer"].replace(".", ",")
    return take_unique(rows, 100, "high")


def sql_escape(value: str) -> str:
    return str(value).replace("'", "''")


def write_pack(level: str, letter: str, slug: str, rows: list[dict], expected: int) -> None:
    if len(rows) != expected:
        raise SystemExit(f"{level}: {len(rows)} ≠ {expected}")
    TASKS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    csv_name = f"geometry-8-{slug}.csv"
    sql_name = f"insert-geometry-8-{slug}.sql"
    fieldnames = ["subject", "class_name", "level", "question", "answer", "image", "explanation_of_the_answer"]
    csv_rows = []
    sql_values = []
    for i, row in enumerate(rows, start=1):
        filename = f"ge8-{letter}-{i:02d}.svg"
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
