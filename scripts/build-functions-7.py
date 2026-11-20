# -*- coding: utf-8 -*-
"""Функции 7 класс: линейная y = kx и y = kx + b. 70/80/100 задач и SVG."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TASKS = ROOT / "public" / "tasks"
CLASS = "7 класс"
SUBJECT = "function"

PALETTE = {
    "Базовый": ("#1f4e79", "#e8f1fb", "#13243d", "#4eb5f1"),
    "Средний": ("#6b4c9a", "#f3eaff", "#2e1a4a", "#9b7ad6"),
    "Высокий": ("#8a3a4a", "#ffe8ee", "#3d1520", "#e07a8c"),
}


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


def fmt_lin(k: int, b: int = 0) -> str:
    if k == 0:
        return f"y = {b}"
    if k == 1:
        body = "x"
    elif k == -1:
        body = "−x"
    else:
        body = f"{k}x".replace("-", "−")
    if b == 0:
        return f"y = {body}"
    if b > 0:
        return f"y = {body} + {b}"
    return f"y = {body} − {abs(b)}"


def header(level: str, index: int, total: int) -> str:
    accent, paper, ink, _ = PALETTE[level]
    return f"""
  <rect width="960" height="540" rx="28" fill="{paper}"/>
  <rect x="28" y="28" width="904" height="484" rx="20" fill="#fffdf8" stroke="{accent}" stroke-width="3"/>
  <text x="56" y="72" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="700" fill="{ink}">Функции · 7 класс</text>
  <text x="900" y="72" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="18" fill="{accent}">{escape(level)} · {index}/{total}</text>
"""


def footer(accent: str) -> str:
    return f'<text x="480" y="492" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="16" fill="{accent}">Матеум · тренажёр</text>'


def question_lines(question: str, ink: str, y0: int = 100) -> str:
    words = question.split()
    cur = ""
    lines = []
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


def plane(ink: str, ox: float = 560, oy: float = 340, scale: float = 28) -> str:
    xmin, xmax, ymin, ymax = -5, 7, -4, 6
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


def to_xy(x: float, y: float, ox: float = 560, oy: float = 340, scale: float = 28):
    return ox + x * scale, oy - y * scale


def line_figure(p: dict, fill: str, ink: str) -> str:
    k = p.get("k", 1)
    b = p.get("b", 0)
    ox, oy, scale = 560, 340, 28
    xs = [-4, 6]
    pts = []
    for x in xs:
        y = k * x + b
        y = max(-4, min(6, y))
        if k != 0:
            # keep x consistent if clipped
            pass
        px, py = to_xy(x, k * x + b, ox, oy, scale)
        py = max(oy - 6 * scale, min(oy + 4 * scale, py))
        pts.append((px, py))
    (x1, y1), (x2, y2) = pts
    svg = plane(ink, ox, oy, scale)
    svg += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{fill}" stroke-width="4"/>'
    formula = fmt_lin(k, b)
    svg += f'<text x="70" y="430" font-size="22" font-weight="700" fill="{ink}" font-family="Georgia, serif">{escape(formula)}</text>'
    mx, my = p.get("mx"), p.get("my")
    if mx is not None:
        px, py = to_xy(mx, my, ox, oy, scale)
        svg += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{fill}" stroke="{ink}" stroke-width="2"/>'
        svg += f'<text x="{px + 10:.1f}" y="{py - 10:.1f}" font-size="16" fill="{ink}">({mx}; {my})</text>'
    return svg


def table_figure(p: dict, fill: str, ink: str) -> str:
    xs = p["xs"]
    ys = p["ys"]
    hide = p.get("hide")
    n = len(xs)
    x0, y0, cw, rh = 180, 200, 90, 56
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
    formula = fmt_lin(p.get("k", 1), p.get("b", 0))
    svg += f'<text x="480" y="390" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{escape(formula)}</text>'
    return svg


def points_figure(p: dict, fill: str, ink: str) -> str:
    ox, oy, scale = 560, 340, 28
    svg = plane(ink, ox, oy, scale)
    for x, y, name in p.get("pts", []):
        px, py = to_xy(x, y, ox, oy, scale)
        svg += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{fill}" stroke="{ink}" stroke-width="2"/>'
        svg += f'<text x="{px + 10:.1f}" y="{py - 10:.1f}" font-size="16" fill="{ink}">{name}({x}; {y})</text>'
    return svg


def draw(task: dict, level: str, index: int, total: int) -> str:
    _, _, ink, fill = PALETTE[level]
    kind = task["kind"]
    p = task["params"]
    if kind == "line":
        body = line_figure(p, fill, ink)
    elif kind == "table":
        body = table_figure(p, fill, ink)
    elif kind == "points":
        body = points_figure(p, fill, ink)
    else:
        body = line_figure({"k": 1, "b": 0}, fill, ink)
    return wrap(body, level, index, total, task["question"])


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
        raise SystemExit(f"{label}: уникальных {len(out)} из {n}")
    return out[:n]


def basic() -> list[dict]:
    rows = []
    for k in range(1, 8):
        for x in range(0, 7):
            y = k * x
            rows.append(item(
                f"Дана функция {fmt_lin(k)}. Найдите y при x = {x}.",
                y,
                f"Тема: прямая пропорциональность. y = {k} × {x} = {y}.",
                "line", k=k, b=0, mx=x, my=y,
            ))
    for k in (2, 3, 4, 5):
        for b in (1, 2, 3, -1, -2):
            for x in (1, 2, 3):
                y = k * x + b
                rows.append(item(
                    f"Дана функция {fmt_lin(k, b)}. Найдите y при x = {x}.",
                    y,
                    f"Тема: линейная функция. y = {k} × {x} + ({b}) = {y}.",
                    "line", k=k, b=b, mx=x, my=y,
                ))
    for x, y in [(1, 4), (2, 6), (2, 10), (3, 9), (3, 12), (4, 8), (4, 12), (5, 10), (5, 15), (6, 18)]:
        k = y // x
        rows.append(item(
            f"График {fmt_lin(k)} проходит через точку ({x}; {y}). Чему равен коэффициент k?",
            k,
            f"Тема: y = kx. {y} = k × {x}, k = {y} : {x} = {k}.",
            "line", k=k, b=0, mx=x, my=y,
        ))
    for b in range(-3, 6):
        rows.append(item(
            f"Чему равна ордината точки пересечения графика {fmt_lin(2, b)} с осью Oy?",
            b,
            f"Тема: пересечение с Oy. При x = 0 получаем y = {b}.",
            "line", k=2, b=b, mx=0, my=b,
        ))
    for x, y in [(2, 5), (3, -2), (0, 4), (-1, 6), (5, 0), (4, -3), (-2, 1), (1, 0)]:
        rows.append(item(
            f"Точка A({x}; {y}). Чему равна абсцисса точки A?",
            x,
            f"Тема: координатная плоскость. Абсцисса — первое число: {x}.",
            "points", pts=[(x, y, "A")],
        ))
        rows.append(item(
            f"Точка B({x}; {y}). Чему равна ордината точки B?",
            y,
            f"Тема: координатная плоскость. Ордината — второе число: {y}.",
            "points", pts=[(x, y, "B")],
        ))
    for k, b in [(2, -6), (3, -9), (4, -8), (5, -10), (1, -5), (2, -4), (3, -6), (4, -12)]:
        x0 = -b // k
        rows.append(item(
            f"Найдите абсциссу точки пересечения графика {fmt_lin(k, b)} с осью Ox.",
            x0,
            f"Тема: нуль функции. {fmt_lin(k, b)} = 0 → {k}x = { -b} → x = {x0}.",
            "line", k=k, b=b, mx=x0, my=0,
        ))
    for k, b, xs in [
        (2, 0, [-1, 0, 1, 2]),
        (3, 1, [0, 1, 2, 3]),
        (1, -2, [0, 2, 4, 6]),
        (4, 0, [1, 2, 3, 4]),
        (2, 3, [-1, 0, 1, 2]),
        (5, -1, [0, 1, 2, 3]),
    ]:
        ys = [k * x + b for x in xs]
        hide = 2
        rows.append(item(
            f"Заполните таблицу для {fmt_lin(k, b)}. Найдите пропущенное значение y при x = {xs[hide]}.",
            ys[hide],
            f"Тема: таблица значений. y = {k} × {xs[hide]} + ({b}) = {ys[hide]}.",
            "table", k=k, b=b, xs=xs, ys=ys, hide=hide,
        ))
    return take_unique(rows, 70, "basic")


def medium() -> list[dict]:
    rows = []
    for k in (-3, -2, -1, 1, 2, 3, 4):
        for b in (-4, -2, 0, 1, 3, 5):
            for x in (-2, -1, 0, 2, 4):
                y = k * x + b
                rows.append(item(
                    f"Дана функция {fmt_lin(k, b)}. Найдите значение функции при x = {x}.",
                    y,
                    f"Тема: линейная функция. Подставьте x = {x}: y = {k} × ({x}) + ({b}) = {y}.",
                    "line", k=k, b=b, mx=x, my=y,
                ))
    for k, b, y in [(2, 1, 9), (3, -1, 8), (4, 2, 14), (5, 0, 20), (1, 7, 12), (2, -3, 5), (3, 4, 19), (-2, 6, 2), (-1, 5, 1), (4, -4, 8)]:
        x = (y - b) // k
        if k * x + b != y:
            continue
        rows.append(item(
            f"Для функции {fmt_lin(k, b)} найдите x, если y = {y}.",
            x,
            f"Тема: найти аргумент. {y} = {k}x + ({b}) → {k}x = {y - b} → x = {x}.",
            "line", k=k, b=b, mx=x, my=y,
        ))
    for x, y, k, b in [
        (1, 5, 2, 3), (2, 7, 2, 3), (3, 3, 1, 0), (2, 0, 2, -4),
        (1, 1, 3, -2), (4, 4, 1, 0), (0, 5, 2, 5), (-1, 1, 2, 3),
        (3, 10, 3, 1), (2, -1, -1, 1),
    ]:
        on = k * x + b == y
        rows.append(item(
            f"Принадлежит ли точка ({x}; {y}) графику {fmt_lin(k, b)}? Ответьте да или нет.",
            "да" if on else "нет",
            f"Тема: точка на графике. y = {k} × {x} + ({b}) = {k * x + b}. "
            + ("Совпало с ординатой — да." if on else "Не совпало — нет."),
            "line", k=k, b=b, mx=x, my=k * x + b,
        ))
    for k, b in [(2, 3), (3, -1), (4, 5), (-2, 4), (1, -6), (5, 2)]:
        rows.append(item(
            f"Укажите коэффициент k линейной функции {fmt_lin(k, b)}.",
            k,
            f"Тема: вид y = kx + b. Здесь k = {k}, свободный член b = {b}.",
            "line", k=k, b=b,
        ))
        rows.append(item(
            f"Укажите свободный член b линейной функции {fmt_lin(k, b)}.",
            b,
            f"Тема: вид y = kx + b. Свободный член — это b = {b}.",
            "line", k=k, b=b, mx=0, my=b,
        ))
    for x1, y1, x2, y2 in [(1, 2, 3, 6), (0, 1, 2, 5), (1, 5, 2, 8), (0, -2, 4, 6), (2, 3, 4, 7), (-1, 0, 1, 4)]:
        k = (y2 - y1) // (x2 - x1)
        if k * (x2 - x1) != (y2 - y1):
            continue
        rows.append(item(
            f"Прямая проходит через точки ({x1}; {y1}) и ({x2}; {y2}). Найдите угловой коэффициент k.",
            k,
            f"Тема: k = (y₂ − y₁) : (x₂ − x₁) = ({y2} − {y1}) : ({x2} − {x1}) = {k}.",
            "points", pts=[(x1, y1, "A"), (x2, y2, "B")],
        ))
    for k, xs in [(2, [-2, -1, 0, 1]), (3, [0, 1, 2, 3]), (-1, [-1, 0, 1, 2]), (4, [0, 1, 2, 3]), (1, [2, 3, 4, 5])]:
        ys = [k * x for x in xs]
        hide = 1
        rows.append(item(
            f"Таблица задаёт прямую пропорциональность {fmt_lin(k)}. Найдите пропущенный y при x = {xs[hide]}.",
            ys[hide],
            f"Тема: y = kx. y = {k} × {xs[hide]} = {ys[hide]}.",
            "table", k=k, b=0, xs=xs, ys=ys, hide=hide,
        ))
    return take_unique(rows, 80, "medium")


def formula_body(k: int, b: int) -> str:
    return fmt_lin(k, b)[4:]


def high() -> list[dict]:
    rows = []
    pairs = []
    for k in (-4, -3, -2, -1, 1, 2, 3, 4, 5):
        for b in (-6, -4, -2, -1, 0, 1, 3, 5, 7):
            for x1, x2 in [(0, 2), (1, 3), (2, 4), (-1, 2), (3, 5), (-2, 1)]:
                pairs.append((k, b, x1, x2))
    for k, b, x1, x2 in pairs:
        y1, y2 = k * x1 + b, k * x2 + b
        rows.append(item(
            f"Для f(x) = {formula_body(k, b)} найдите f({x1}) + f({x2}).",
            y1 + y2,
            f"Тема: значения функции. f({x1}) = {y1}, f({x2}) = {y2}, сумма {y1 + y2}.",
            "line", k=k, b=b, mx=x1, my=y1,
        ))
        rows.append(item(
            f"Для f(x) = {formula_body(k, b)} найдите f({x2}) − f({x1}).",
            y2 - y1,
            f"Тема: разность значений. f({x2}) − f({x1}) = {y2} − ({y1}) = {y2 - y1}.",
            "line", k=k, b=b, mx=x2, my=y2,
        ))
        rows.append(item(
            f"Найдите f(0) для функции f(x) = {formula_body(k, b)}.",
            b,
            f"Тема: значение в нуле. f(0) = b = {b}.",
            "line", k=k, b=b, mx=0, my=b,
        ))
        rows.append(item(
            f"На сколько изменится y у функции {fmt_lin(k, b)}, если x увеличить на 1?",
            k,
            f"Тема: угловой коэффициент. Прирост y на единицу x равен k = {k}.",
            "line", k=k, b=b,
        ))
    for x1, y1, x2, y2 in [
        (0, 2, 2, 8), (1, 1, 3, 7), (0, -1, 3, 5), (2, 0, 4, 6),
        (1, 4, 3, 0), (0, 5, 5, 0), (-1, 2, 1, 6), (1, -2, 4, 4),
        (0, 0, 3, 9), (2, 3, 5, 9), (-2, 1, 2, 5), (1, 5, 4, 11),
    ]:
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 or dy % dx != 0:
            continue
        k = dy // dx
        b = y1 - k * x1
        rows.append(item(
            f"Прямая проходит через ({x1}; {y1}) и ({x2}; {y2}). Найдите k в уравнении y = kx + b.",
            k,
            f"Тема: две точки. k = ({y2} − {y1}) : ({x2} − {x1}) = {k}.",
            "points", pts=[(x1, y1, "A"), (x2, y2, "B")],
        ))
        rows.append(item(
            f"Прямая проходит через ({x1}; {y1}) и ({x2}; {y2}). Найдите b в уравнении y = kx + b.",
            b,
            f"Тема: две точки. k = {k}, тогда b = {y1} − {k} × {x1} = {b}.",
            "line", k=k, b=b, mx=x1, my=y1,
        ))
    for k, b in [(2, 3), (3, -4), (-1, 6), (4, 1), (5, -5), (-2, 8), (1, -7), (2, -1)]:
        if k == 0 or (-b) % k != 0:
            continue
        x0 = -b // k
        rows.append(item(
            f"Найдите нуль функции {fmt_lin(k, b)} — значение x, при котором y = 0.",
            x0,
            f"Тема: нуль функции. {k}x + ({b}) = 0 → x = {x0}.",
            "line", k=k, b=b, mx=x0, my=0,
        ))
    for k1, b1, k2, b2 in [
        (2, 1, 1, 4), (3, 0, 1, 6), (4, -2, 2, 2), (1, 5, -1, 1),
        (2, -3, 3, -6), (5, 1, 2, 7), (3, 2, -1, 10), (4, 0, 1, 3),
    ]:
        if k1 == k2:
            continue
        # k1 x + b1 = k2 x + b2
        if (b2 - b1) % (k1 - k2) != 0:
            continue
        x = (b2 - b1) // (k1 - k2)
        y = k1 * x + b1
        rows.append(item(
            f"Найдите абсциссу точки пересечения графиков {fmt_lin(k1, b1)} и {fmt_lin(k2, b2)}.",
            x,
            f"Тема: система. {k1}x + ({b1}) = {k2}x + ({b2}) → x = {x}.",
            "line", k=k1, b=b1, mx=x, my=y,
        ))
        rows.append(item(
            f"Найдите ординату точки пересечения графиков {fmt_lin(k1, b1)} и {fmt_lin(k2, b2)}.",
            y,
            f"Тема: система. При x = {x} получаем y = {y}.",
            "line", k=k2, b=b2, mx=x, my=y,
        ))
    for k, b, x in [(2, 1, 4), (3, -2, 3), (-2, 5, 2), (4, 0, -1), (1, 6, 5), (5, -3, 2)]:
        y = k * x + b
        rows.append(item(
            f"График {fmt_lin(k, b)} проходит через точку ({x}; y). Найдите y.",
            y,
            f"Тема: подстановка в линейную функцию. y = {k} × ({x}) + ({b}) = {y}.",
            "line", k=k, b=b, mx=x, my=y,
        ))
    for k in (2, 3, 4, -1, -2):
        rows.append(item(
            f"Прямые {fmt_lin(k, 1)} и {fmt_lin(k, -3)} параллельны. Чему равен их общий угловой коэффициент k?",
            k,
            f"Тема: параллельные прямые имеют равные k. Здесь k = {k}.",
            "line", k=k, b=1,
        ))
    for k, b, xs in [
        (2, 1, [-1, 0, 1, 2]),
        (3, -2, [0, 1, 2, 3]),
        (-1, 4, [-2, 0, 2, 4]),
        (4, 1, [0, 1, 2, 3]),
        (1, -3, [1, 2, 3, 4]),
        (5, 0, [0, 1, 2, 3]),
    ]:
        ys = [k * x + b for x in xs]
        hide = 3
        rows.append(item(
            f"По таблице для {fmt_lin(k, b)} найдите пропущенное y при x = {xs[hide]}.",
            ys[hide],
            f"Тема: таблица. y = {k} × {xs[hide]} + ({b}) = {ys[hide]}.",
            "table", k=k, b=b, xs=xs, ys=ys, hide=hide,
        ))
    for k in range(1, 7):
        x, y = 3, k * 3
        rows.append(item(
            f"График прямой пропорциональности проходит через ({x}; {y}) и начало координат. Найдите k.",
            k,
            f"Тема: y = kx. Точка ({x}; {y}) даёт k = {y} : {x} = {k}.",
            "line", k=k, b=0, mx=x, my=y,
        ))
    return take_unique(rows, 100, "high")


def sql_escape(value: str) -> str:
    return str(value).replace("'", "''")


def write_pack(level: str, letter: str, slug: str, rows: list[dict], expected: int) -> None:
    if len(rows) != expected:
        raise SystemExit(f"{level}: {len(rows)} ≠ {expected}")
    TASKS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    csv_name = f"functions-7-{slug}.csv"
    sql_name = f"insert-functions-7-{slug}.sql"
    fieldnames = ["subject", "class_name", "level", "question", "answer", "image", "explanation_of_the_answer"]
    csv_rows = []
    sql_values = []
    for i, row in enumerate(rows, start=1):
        filename = f"fn7-{letter}-{i:02d}.svg"
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
