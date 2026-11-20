# -*- coding: utf-8 -*-
"""Функции 9 класс: квадратичная, √x, |x|, свойства. 70/80/100 и SVG."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TASKS = ROOT / "public" / "tasks"
CLASS = "9 класс"
SUBJECT = "function"

PALETTE = {
    "Базовый": ("#1f4e79", "#e8f1fb", "#13243d", "#4eb5f1"),
    "Средний": ("#6b4c9a", "#f3eaff", "#2e1a4a", "#9b7ad6"),
    "Высокий": ("#8a3a4a", "#ffe8ee", "#3d1520", "#e07a8c"),
}

OX, OY, SCALE = 560.0, 355.0, 26.0


def item(q, ans, exp, kind, **params):
    return {
        "question": q,
        "answer": str(ans),
        "explanation": exp,
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


def minus(n: int) -> str:
    return str(n).replace("-", "−")


def fmt_ax2(a: int, n: int = 0) -> str:
    if a == 1:
        body = "x²"
    elif a == -1:
        body = "−x²"
    else:
        body = f"{minus(a)}x²"
    if n == 0:
        return f"y = {body}"
    if n > 0:
        return f"y = {body} + {n}"
    return f"y = {body} − {abs(n)}"


def fmt_quad(a: int, b: int, c: int) -> str:
    if a == 1:
        body = "x²"
    elif a == -1:
        body = "−x²"
    else:
        body = f"{minus(a)}x²"
    parts = [body]
    if b == 1:
        parts.append("+ x")
    elif b == -1:
        parts.append("− x")
    elif b > 0:
        parts.append(f"+ {b}x")
    elif b < 0:
        parts.append(f"− {abs(b)}x")
    if c > 0:
        parts.append(f"+ {c}")
    elif c < 0:
        parts.append(f"− {abs(c)}")
    return "y = " + " ".join(parts)


def fmt_sqrt(shift: int = 0, add: int = 0) -> str:
    if shift == 0:
        inner = "x"
    elif shift > 0:
        inner = f"x − {shift}"
    else:
        inner = f"x + {abs(shift)}"
    body = f"√({inner})" if shift != 0 else "√x"
    if add == 0:
        return f"y = {body}"
    if add > 0:
        return f"y = {body} + {add}"
    return f"y = {body} − {abs(add)}"


def fmt_abs(m: int = 0, n: int = 0) -> str:
    if m == 0:
        body = "|x|"
    elif m > 0:
        body = f"|x − {m}|"
    else:
        body = f"|x + {abs(m)}|"
    if n == 0:
        return f"y = {body}"
    if n > 0:
        return f"y = {body} + {n}"
    return f"y = {body} − {abs(n)}"


def header(level: str, index: int, total: int) -> str:
    accent, paper, ink, _ = PALETTE[level]
    return f"""
  <rect width="960" height="540" rx="28" fill="{paper}"/>
  <rect x="28" y="28" width="904" height="484" rx="20" fill="#fffdf8" stroke="{accent}" stroke-width="3"/>
  <text x="56" y="72" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="700" fill="{ink}">Функции · 9 класс</text>
  <text x="900" y="72" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="18" fill="{accent}">{escape(level)} · {index}/{total}</text>
"""


def footer(accent: str) -> str:
    return f'<text x="480" y="492" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="16" fill="{accent}">Матеум · тренажёр</text>'


def question_lines(question: str, ink: str, y0: int = 100) -> str:
    words = question.split()
    cur, lines = "", []
    for w in words:
        nxt = f"{cur} {w}".strip()
        if len(nxt) > 68 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = nxt
    if cur:
        lines.append(cur)
    return "".join(
        f'<text x="56" y="{y0 + 22 * i}" font-size="17" fill="{ink}" font-family="Segoe UI, Arial, sans-serif">{escape(line)}</text>'
        for i, line in enumerate(lines[:3])
    )


def wrap(svg_body: str, level: str, index: int, total: int, question: str) -> str:
    accent, _, ink, _ = PALETTE[level]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">
{header(level, index, total)}
{question_lines(question, ink)}
{svg_body}
{footer(accent)}
</svg>
"""


def plane(ink: str) -> str:
    xmin, xmax, ymin, ymax = -6, 8, -5, 7
    ox, oy, scale = OX, OY, SCALE
    parts = []
    for i in range(xmin, xmax + 1):
        x = ox + i * scale
        parts.append(
            f'<line x1="{x:.1f}" y1="{oy - ymax * scale:.1f}" x2="{x:.1f}" y2="{oy - ymin * scale:.1f}" stroke="#e4ebf5" stroke-width="1"/>'
        )
    for j in range(ymin, ymax + 1):
        y = oy - j * scale
        parts.append(
            f'<line x1="{ox + xmin * scale:.1f}" y1="{y:.1f}" x2="{ox + xmax * scale:.1f}" y2="{y:.1f}" stroke="#e4ebf5" stroke-width="1"/>'
        )
    x0, x1 = ox + xmin * scale, ox + xmax * scale
    y0, y1 = oy - ymin * scale, oy - ymax * scale
    parts.append(f'<line x1="{x0:.1f}" y1="{oy:.1f}" x2="{x1:.1f}" y2="{oy:.1f}" stroke="{ink}" stroke-width="2.5"/>')
    parts.append(f'<line x1="{ox:.1f}" y1="{y0:.1f}" x2="{ox:.1f}" y2="{y1:.1f}" stroke="{ink}" stroke-width="2.5"/>')
    parts.append(f'<polygon points="{x1:.1f},{oy - 6:.1f} {x1 + 12:.1f},{oy:.1f} {x1:.1f},{oy + 6:.1f}" fill="{ink}"/>')
    parts.append(f'<polygon points="{ox - 6:.1f},{y1:.1f} {ox:.1f},{y1 - 12:.1f} {ox + 6:.1f},{y1:.1f}" fill="{ink}"/>')
    parts.append(f'<text x="{x1 - 8:.1f}" y="{oy + 20:.1f}" font-size="14" fill="{ink}">x</text>')
    parts.append(f'<text x="{ox + 10:.1f}" y="{y1 + 16:.1f}" font-size="14" fill="{ink}">y</text>')
    for i in range(xmin, xmax + 1):
        if i == 0:
            continue
        x = ox + i * scale
        parts.append(f'<line x1="{x:.1f}" y1="{oy - 5:.1f}" x2="{x:.1f}" y2="{oy + 5:.1f}" stroke="{ink}" stroke-width="2"/>')
        parts.append(f'<text x="{x:.1f}" y="{oy + 18:.1f}" text-anchor="middle" font-size="11" fill="{ink}">{i}</text>')
    for j in range(ymin, ymax + 1):
        if j == 0:
            continue
        y = oy - j * scale
        parts.append(f'<line x1="{ox - 5:.1f}" y1="{y:.1f}" x2="{ox + 5:.1f}" y2="{y:.1f}" stroke="{ink}" stroke-width="2"/>')
        parts.append(f'<text x="{ox - 10:.1f}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="{ink}">{j}</text>')
    parts.append(f'<text x="{ox - 12:.1f}" y="{oy + 16:.1f}" font-size="11" fill="{ink}">0</text>')
    return "".join(parts)


def to_xy(x: float, y: float):
    return OX + x * SCALE, OY - y * SCALE


def mark(x, y, fill, ink, label=None):
    px, py = to_xy(x, y)
    s = f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{fill}" stroke="{ink}" stroke-width="2"/>'
    text = label if label is not None else f"({x}; {y})"
    s += f'<text x="{px + 10:.1f}" y="{py - 10:.1f}" font-size="15" fill="{ink}">{escape(str(text))}</text>'
    return s


def formula_label(text: str, ink: str) -> str:
    return f'<text x="70" y="430" font-size="20" font-weight="700" fill="{ink}" font-family="Georgia, serif">{escape(text)}</text>'


def polyline(xs_ys, fill: str) -> str:
    pts = []
    for x, y in xs_ys:
        if -5.3 <= y <= 7.3 and -6.3 <= x <= 8.3:
            px, py = to_xy(x, y)
            pts.append(f"{px:.1f},{py:.1f}")
    if not pts:
        return ""
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{fill}" stroke-width="3.5"/>'


def parabola_figure(p: dict, fill: str, ink: str) -> str:
    a, m, n = p.get("a", 1), p.get("m", 0), p.get("n", 0)
    samples = []
    for i in range(-80, 91):
        x = i / 10
        y = a * (x - m) ** 2 + n
        samples.append((x, y))
    svg = plane(ink) + polyline(samples, fill)
    svg += formula_label(p.get("formula") or fmt_ax2(a, n), ink)
    svg += mark(m, n, fill, ink, f"V({m}; {n})")
    if p.get("mx") is not None:
        svg += mark(p["mx"], p["my"], fill, ink)
    return svg


def sqrt_figure(p: dict, fill: str, ink: str) -> str:
    shift, add = p.get("shift", 0), p.get("add", 0)
    samples = []
    for i in range(0, 90):
        t = i / 10
        x = t + shift
        if t < 0:
            continue
        y = t ** 0.5 + add
        samples.append((x, y))
    svg = plane(ink) + polyline(samples, fill)
    svg += formula_label(p.get("formula") or fmt_sqrt(shift, add), ink)
    if p.get("mx") is not None:
        svg += mark(p["mx"], p["my"], fill, ink)
    return svg


def abs_figure(p: dict, fill: str, ink: str) -> str:
    m, n = p.get("m", 0), p.get("n", 0)
    samples = []
    for i in range(-70, 81):
        x = i / 10
        y = abs(x - m) + n
        samples.append((x, y))
    svg = plane(ink) + polyline(samples, fill)
    svg += formula_label(p.get("formula") or fmt_abs(m, n), ink)
    svg += mark(m, n, fill, ink, f"({m}; {n})")
    if p.get("mx") is not None:
        svg += mark(p["mx"], p["my"], fill, ink)
    return svg


def cubic_figure(p: dict, fill: str, ink: str) -> str:
    samples = []
    for i in range(-25, 26):
        x = i / 10
        y = x ** 3
        samples.append((x, y))
    svg = plane(ink) + polyline(samples, fill)
    svg += formula_label("y = x³", ink)
    if p.get("mx") is not None:
        svg += mark(p["mx"], p["my"], fill, ink)
    return svg


def table_figure(p: dict, fill: str, ink: str) -> str:
    xs, ys = p["xs"], p["ys"]
    hide = p.get("hide")
    n = len(xs)
    x0, y0, cw, rh = 160, 200, 90, 56
    w = cw * (n + 1)
    svg = f'<rect x="{x0}" y="{y0}" width="{w}" height="{rh * 2}" rx="10" fill="#fff" stroke="{ink}" stroke-width="3"/>'
    svg += f'<line x1="{x0}" y1="{y0 + rh}" x2="{x0 + w}" y2="{y0 + rh}" stroke="{ink}" stroke-width="2"/>'
    svg += f'<rect x="{x0}" y="{y0}" width="{cw}" height="{rh}" fill="{fill}" fill-opacity="0.25"/>'
    svg += f'<rect x="{x0}" y="{y0 + rh}" width="{cw}" height="{rh}" fill="{fill}" fill-opacity="0.25"/>'
    svg += f'<text x="{x0 + cw / 2:.0f}" y="{y0 + 36}" text-anchor="middle" font-size="22" fill="{ink}" font-weight="700">x</text>'
    svg += f'<text x="{x0 + cw / 2:.0f}" y="{y0 + rh + 36}" text-anchor="middle" font-size="22" fill="{ink}" font-weight="700">y</text>'
    for i, (xv, yv) in enumerate(zip(xs, ys)):
        cx = x0 + cw * (i + 1)
        svg += f'<line x1="{cx}" y1="{y0}" x2="{cx}" y2="{y0 + rh * 2}" stroke="{ink}" stroke-width="2"/>'
        svg += f'<text x="{cx + cw / 2:.0f}" y="{y0 + 36}" text-anchor="middle" font-size="22" fill="{ink}">{xv}</text>'
        label = "?" if hide == i else str(yv)
        color = fill if hide == i else ink
        svg += f'<text x="{cx + cw / 2:.0f}" y="{y0 + rh + 36}" text-anchor="middle" font-size="22" fill="{color}" font-weight="700">{label}</text>'
    svg += f'<text x="480" y="390" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{escape(p.get("formula", ""))}</text>'
    return svg


def draw(task: dict, level: str, index: int, total: int) -> str:
    _, _, ink, fill = PALETTE[level]
    kind, p = task["kind"], task["params"]
    if kind == "parabola":
        body = parabola_figure(p, fill, ink)
    elif kind == "sqrt":
        body = sqrt_figure(p, fill, ink)
    elif kind == "abs":
        body = abs_figure(p, fill, ink)
    elif kind == "cubic":
        body = cubic_figure(p, fill, ink)
    elif kind == "table":
        body = table_figure(p, fill, ink)
    else:
        body = parabola_figure({"a": 1, "m": 0, "n": 0}, fill, ink)
    return wrap(body, level, index, total, task["question"])


def take_unique(rows: list[dict], n: int, label: str) -> list[dict]:
    seen, out = set(), []
    for r in rows:
        if r["question"] not in seen:
            seen.add(r["question"])
            out.append(r)
        if len(out) >= n:
            break
    if len(out) < n:
        raise SystemExit(f"{label}: уникальных {len(out)} из {n}")
    return out[:n]


def disc(a, b, c):
    return b * b - 4 * a * c


def basic() -> list[dict]:
    rows = []
    for x in (0, 1, 4, 9, 16, 25, 36):
        y = int(x ** 0.5)
        rows.append(item(
            f"Дана функция y = √x. Найдите y при x = {x}.",
            y,
            f"Тема: квадратный корень. √{x} = {y}, потому что {y}² = {x}.",
            "sqrt", shift=0, add=0, mx=x if x <= 8 else 4, my=y if x <= 8 else 2, formula="y = √x",
        ))
    for x in range(-5, 6):
        y = abs(x)
        rows.append(item(
            f"Дана функция y = |x|. Найдите y при x = {x}.",
            y,
            f"Тема: модуль. |{x}| = {y}.",
            "abs", m=0, n=0, mx=x, my=y, formula="y = |x|",
        ))
    for x in (-2, -1, 0, 1, 2):
        y = x ** 3
        rows.append(item(
            f"Дана функция y = x³. Найдите y при x = {x}.",
            y,
            f"Тема: кубическая функция. {x}³ = {y}.",
            "cubic", mx=x, my=y,
        ))
    for a, b, c in [
        (1, -5, 6), (1, -3, 2), (1, -7, 12), (1, -9, 20),
        (1, -6, 8), (1, -4, 3), (1, 1, -6), (1, -1, -6),
        (1, -8, 15), (1, -10, 21), (1, 2, -8), (1, -2, -8),
    ]:
        formula = fmt_quad(a, b, c)
        d = disc(a, b, c)
        rows.append(item(
            f"Найдите дискриминант квадратного трёхчлена из {formula}.",
            d,
            f"Тема: D = b² − 4ac = ({b})² − 4×{a}×({c}) = {d}.",
            "parabola", a=a, m=0, n=c, formula=formula,
        ))
        nroots = 0 if d < 0 else (1 if d == 0 else 2)
        rows.append(item(
            f"Сколько точек пересечения с осью Ox у графика {formula}?",
            nroots,
            f"Тема: знак D. D = {d}, значит точек пересечения {nroots}.",
            "parabola", a=a, m=0, n=c, formula=formula,
        ))
        for x in (0, 1, 2, 3, -1):
            y = a * x * x + b * x + c
            rows.append(item(
                f"Для f(x) = {formula[4:]} найдите f({x}).",
                y,
                f"Тема: квадратичная. f({x}) = {a}×{x * x} + ({b})×{x} + ({c}) = {y}.",
                "parabola", a=a, m=0, n=c, mx=x, my=y, formula=formula,
            ))
    for r in (1, 2, 3, 4, 5, 6):
        rows.append(item(
            f"Уравнение x² = {r * r} задаёт нули функции y = x² − {r * r}. Укажите неотрицательный корень.",
            r,
            f"Тема: нули. x² − {r * r} = 0 → x = ±{r}. Неотрицательный {r}.",
            "parabola", a=1, m=0, n=-(r * r), mx=r, my=0, formula=fmt_ax2(1, -(r * r)),
        ))
    xs = [0, 1, 4, 9]
    ys = [0, 1, 2, 3]
    rows.append(item(
        "По таблице для y = √x найдите пропущенное y при x = 4.",
        2,
        "Тема: таблица. √4 = 2.",
        "table", xs=xs, ys=ys, hide=2, formula="y = √x",
    ))
    return take_unique(rows, 70, "basic")


def medium() -> list[dict]:
    rows = []
    for shift in range(0, 6):
        for add in (0, 1, 2, -1):
            formula = fmt_sqrt(shift, add)
            domain0 = shift
            rows.append(item(
                f"Найдите наименьшее целое x из области определения {formula}.",
                domain0,
                f"Тема: область √. Подкоренное выражение ≥ 0, поэтому x ≥ {shift}. Наименьшее целое {shift}.",
                "sqrt", shift=shift, add=add, formula=formula,
            ))
            x = shift + 4
            y = 2 + add
            rows.append(item(
                f"Дана функция {formula}. Найдите y при x = {x}.",
                y,
                f"Тема: √. √({x} − {shift}) + ({add}) = 2 + ({add}) = {y}.",
                "sqrt", shift=shift, add=add, mx=x, my=y, formula=formula,
            ))
    for m in range(-2, 5):
        for n in (0, 1, 2, -1):
            formula = fmt_abs(m, n)
            rows.append(item(
                f"Найдите наименьшее значение функции {formula}.",
                n,
                f"Тема: модуль. Минимум в x = {m}, он равен {n}.",
                "abs", m=m, n=n, formula=formula,
            ))
            x = m + 3
            y = 3 + n
            rows.append(item(
                f"Дана функция {formula}. Найдите y при x = {x}.",
                y,
                f"Тема: модуль. |{x} − {m}| + ({n}) = {y}.",
                "abs", m=m, n=n, mx=x, my=y, formula=formula,
            ))
    for a, b, c in [
        (1, -6, 8), (1, -4, 3), (1, -8, 12), (1, -2, -3),
        (1, 4, 3), (1, -10, 16), (1, 2, -8), (2, -8, 6),
        (1, -6, 5), (1, 0, -9),
    ]:
        formula = fmt_quad(a, b, c)
        if (-b) % (2 * a) != 0:
            continue
        vx = -b // (2 * a)
        vy = a * vx * vx + b * vx + c
        rows.append(item(
            f"Найдите абсциссу вершины {formula}.",
            vx,
            f"Тема: xᵥ = −b : 2a = {minus(b)} : {2 * a} = {vx}.",
            "parabola", a=a, m=vx, n=vy, formula=formula,
        ))
        rows.append(item(
            f"Найдите ординату вершины {formula}. Это наименьшее значение функции, если a > 0.",
            vy,
            f"Тема: yᵥ = f({vx}) = {vy}.",
            "parabola", a=a, m=vx, n=vy, formula=formula,
        ))
        rows.append(item(
            f"Функция {formula} возрастает при x ≥ xᵥ. Укажите xᵥ.",
            vx,
            f"Тема: промежуток возрастания параболы с a > 0: x ≥ {vx}.",
            "parabola", a=a, m=vx, n=vy, formula=formula,
        ))
        d = disc(a, b, c)
        rows.append(item(
            f"Вычислите дискриминант для {formula}.",
            d,
            f"Тема: D = {b}² − 4×{a}×({c}) = {d}.",
            "parabola", a=a, m=vx, n=vy, formula=formula,
        ))
    for x in (0, 1, 2, 4, 9):
        rows.append(item(
            f"Функция y = √x чётная? Ответьте да или нет.",
            "нет",
            "Тема: чётность. Область x ≥ 0 не симметрична, функция нечётная и не чётная.",
            "sqrt", shift=0, add=0, mx=x, my=int(x ** 0.5) if x in (0, 1, 4, 9) else 2, formula="y = √x",
        ))
        break
    rows.append(item(
        "Функция y = |x| чётная? Ответьте да или нет.",
        "да",
        "Тема: чётность. |−x| = |x|, график симметричен относительно оси Oy.",
        "abs", m=0, n=0, formula="y = |x|",
    ))
    rows.append(item(
        "Функция y = x³ нечётная? Ответьте да или нет.",
        "да",
        "Тема: нечётность. (−x)³ = −x³, график симметричен относительно начала координат.",
        "cubic", mx=2, my=8,
    ))
    rows.append(item(
        "Функция y = x² чётная? Ответьте да или нет.",
        "да",
        "Тема: чётность. (−x)² = x².",
        "parabola", a=1, m=0, n=0, formula="y = x²",
    ))
    return take_unique(rows, 80, "medium")


def high() -> list[dict]:
    rows = []
    quads = [
        (1, -5, 6), (1, -3, 2), (1, -7, 10), (1, -9, 14),
        (1, -8, 15), (1, -6, 8), (1, 1, -12), (1, -1, -12),
        (1, 4, -5), (1, -4, -5), (1, -10, 24), (1, -12, 35),
        (1, 6, 5), (1, -6, 5), (2, -10, 12), (1, 0, -16),
        (1, -2, -15), (1, 5, 6), (1, -11, 30), (1, 3, -10),
    ]
    for a, b, c in quads:
        formula = fmt_quad(a, b, c)
        d = disc(a, b, c)
        nroots = 0 if d < 0 else (1 if d == 0 else 2)
        rows.append(item(
            f"Сколько корней у уравнения {formula[4:]} = 0?",
            nroots,
            f"Тема: число корней. D = {d}, корней {nroots}.",
            "parabola", a=a, m=0, n=c, formula=formula,
        ))
        if (-b) % (2 * a) == 0:
            vx = -b // (2 * a)
            vy = a * vx * vx + b * vx + c
            rows.append(item(
                f"Найдите наименьшее значение функции {formula}." if a > 0
                else f"Найдите наибольшее значение функции {formula}.",
                vy,
                f"Тема: экстремум в вершине x = {vx}, f({vx}) = {vy}.",
                "parabola", a=a, m=vx, n=vy, formula=formula,
            ))
            rows.append(item(
                f"Укажите абсциссу вершины {formula}.",
                vx,
                f"Тема: xᵥ = −b/2a = {vx}.",
                "parabola", a=a, m=vx, n=vy, formula=formula,
            ))
            left = vx - 1
            rows.append(item(
                f"На промежутке возрастания {formula} наименьшее целое x, строго большее xᵥ, равно?",
                vx + 1,
                f"Тема: при a > 0 возрастает при x ≥ {vx}. Следующее целое после вершины: {vx + 1}."
                if a > 0 else
                f"Тема: при a < 0 возрастает при x ≤ {vx}.",
                "parabola", a=a, m=vx, n=vy, formula=formula,
            ))
        for x in (0, 1, 2, -1, 4, 5, -2):
            y = a * x * x + b * x + c
            rows.append(item(
                f"Для f(x) = {formula[4:]} найдите f({x}).",
                y,
                f"Тема: подстановка. f({x}) = {y}.",
                "parabola", a=a, m=0, n=c, mx=x, my=y, formula=formula,
            ))
        y0, y2 = c, a * 4 + b * 2 + c
        rows.append(item(
            f"Для f(x) = {formula[4:]} найдите f(0) + f(2).",
            y0 + y2,
            f"Тема: f(0) = {y0}, f(2) = {y2}, сумма {y0 + y2}.",
            "parabola", a=a, m=0, n=c, formula=formula,
        ))
    # factored zeros
    for p, q in [(2, 5), (1, 6), (3, 7), (4, 9), (-2, 5), (-3, 4), (1, 8), (2, 8), (-1, 9), (3, 5)]:
        a, b, c = 1, -(p + q), p * q
        formula = fmt_quad(a, b, c)
        rows.append(item(
            f"Нули функции {formula} равны {p} и {q}. Укажите больший нуль.",
            max(p, q),
            f"Тема: нули. Корни {p} и {q}, больший {max(p, q)}.",
            "parabola", a=1, m=(p + q) / 2, n=0, mx=max(p, q), my=0, formula=formula,
        ))
        rows.append(item(
            f"Нули функции {formula} равны {p} и {q}. Укажите меньший нуль.",
            min(p, q),
            f"Тема: нули. Меньший корень {min(p, q)}.",
            "parabola", a=1, m=(p + q) / 2, n=0, mx=min(p, q), my=0, formula=formula,
        ))
        rows.append(item(
            f"Произведение нулей {formula} по теореме Виета равно?",
            p * q,
            f"Тема: Виет. c/a = {p * q}.",
            "parabola", a=1, m=0, n=p * q, formula=formula,
        ))
        rows.append(item(
            f"Сумма нулей {formula} по теореме Виета равна?",
            p + q,
            f"Тема: Виет. −b/a = {p + q}.",
            "parabola", a=1, m=0, n=p * q, formula=formula,
        ))
    for shift in (0, 1, 2, 3, 4):
        for add in (0, 1, -1, 2):
            formula = fmt_sqrt(shift, add)
            x = shift + 9
            y = 3 + add
            rows.append(item(
                f"Для {formula} найдите y при x = {x}.",
                y,
                f"Тема: √. √({x - shift}) + ({add}) = {y}.",
                "sqrt", shift=shift, add=add, mx=min(x, 7), my=y, formula=formula,
            ))
    for m in (0, 1, 2, 3, -1):
        for x in (m - 4, m + 5, 0, 6):
            y = abs(x - m)
            rows.append(item(
                f"Для {fmt_abs(m)} найдите y при x = {x}.",
                y,
                f"Тема: модуль. |{x} − {m}| = {y}.",
                "abs", m=m, n=0, mx=x, my=y, formula=fmt_abs(m),
            ))
    for x in (-2, -1, 0, 1, 2, 3):
        rows.append(item(
            f"Для f(x) = x³ найдите f({x}).",
            x ** 3,
            f"Тема: куб. {x}³ = {x ** 3}.",
            "cubic", mx=x, my=x ** 3,
        ))
    return take_unique(rows, 100, "high")


def sql_escape(value: str) -> str:
    return str(value).replace("'", "''")


def write_pack(level: str, letter: str, slug: str, rows: list[dict], expected: int) -> None:
    if len(rows) != expected:
        raise SystemExit(f"{level}: {len(rows)} ≠ {expected}")
    TASKS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    csv_name = f"functions-9-{slug}.csv"
    sql_name = f"insert-functions-9-{slug}.sql"
    fieldnames = ["subject", "class_name", "level", "question", "answer", "image", "explanation_of_the_answer"]
    csv_rows, sql_values = [], []
    for i, row in enumerate(rows, start=1):
        filename = f"fn9-{letter}-{i:02d}.svg"
        image = f"/tasks/{filename}"
        (TASKS / filename).write_text(draw(row, level, i, len(rows)), encoding="utf-8")
        csv_rows.append({
            "subject": SUBJECT,
            "class_name": CLASS,
            "level": level,
            "question": row["question"],
            "answer": row["answer"],
            "image": image,
            "explanation_of_the_answer": row["explanation"],
        })
        sql_values.append(
            "  ('{s}', '{k}', '{lv}', '{q}', '{a}', '{img}', '{e}')".format(
                s=SUBJECT,
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
        f"-- Функции, {CLASS}, {level}, {len(rows)} задач.\n"
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
