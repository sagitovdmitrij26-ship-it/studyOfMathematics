# -*- coding: utf-8 -*-
"""Функции 8 класс: y = ax², сдвиги, вершина, y = k/x. 70/80/100 и SVG."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TASKS = ROOT / "public" / "tasks"
CLASS = "8 класс"
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


def fmt_vertex(a: int, m: int, n: int) -> str:
    if m == 0:
        inner = "x"
    elif m > 0:
        inner = f"(x − {m})"
    else:
        inner = f"(x + {abs(m)})"
    if a == 1:
        body = f"{inner}²"
    elif a == -1:
        body = f"−{inner}²"
    else:
        body = f"{minus(a)}{inner}²"
    if n == 0:
        return f"y = {body}"
    if n > 0:
        return f"y = {body} + {n}"
    return f"y = {body} − {abs(n)}"


def fmt_inv(k: int) -> str:
    if k == 1:
        return "y = 1/x"
    if k == -1:
        return "y = −1/x"
    return f"y = {minus(k)}/x"


def fmt_quad(a: int, b: int, c: int) -> str:
    parts = [fmt_ax2(a)[4:]]  # x² without y =
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
    return "y = " + " ".join(parts).replace("+ −", "−")


def header(level: str, index: int, total: int) -> str:
    accent, paper, ink, _ = PALETTE[level]
    return f"""
  <rect width="960" height="540" rx="28" fill="{paper}"/>
  <rect x="28" y="28" width="904" height="484" rx="20" fill="#fffdf8" stroke="{accent}" stroke-width="3"/>
  <text x="56" y="72" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="700" fill="{ink}">Функции · 8 класс</text>
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
    xmin, xmax, ymin, ymax = -6, 7, -5, 7
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
    s += f'<text x="{px + 10:.1f}" y="{py - 10:.1f}" font-size="15" fill="{ink}">{escape(text)}</text>'
    return s


def parabola_figure(p: dict, fill: str, ink: str) -> str:
    a, m, n = p.get("a", 1), p.get("m", 0), p.get("n", 0)
    pts = []
    for i in range(-80, 81):
        x = i / 10
        y = a * (x - m) ** 2 + n
        if -5.2 <= y <= 7.2 and -6.2 <= x <= 7.2:
            px, py = to_xy(x, y)
            pts.append(f"{px:.1f},{py:.1f}")
    svg = plane(ink)
    if pts:
        svg += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{fill}" stroke-width="3.5"/>'
    formula = p.get("formula") or fmt_vertex(a, m, n)
    svg += f'<text x="70" y="430" font-size="20" font-weight="700" fill="{ink}" font-family="Georgia, serif">{escape(formula)}</text>'
    svg += mark(m, n, fill, ink, f"V({m}; {n})")
    if p.get("mx") is not None:
        svg += mark(p["mx"], p["my"], fill, ink)
    return svg


def hyperbola_figure(p: dict, fill: str, ink: str) -> str:
    k = p.get("k", 2)
    svg = plane(ink)
    for sign in (-1, 1):
        pts = []
        for i in range(8, 81):
            x = sign * i / 10
            y = k / x
            if -5.2 <= y <= 7.2:
                px, py = to_xy(x, y)
                pts.append(f"{px:.1f},{py:.1f}")
        if pts:
            svg += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{fill}" stroke-width="3.5"/>'
    formula = fmt_inv(k)
    svg += f'<text x="70" y="430" font-size="20" font-weight="700" fill="{ink}" font-family="Georgia, serif">{escape(formula)}</text>'
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
    formula = p.get("formula", "")
    svg += f'<text x="480" y="390" text-anchor="middle" font-size="22" fill="{ink}" font-family="Georgia, serif">{escape(formula)}</text>'
    return svg


def draw(task: dict, level: str, index: int, total: int) -> str:
    _, _, ink, fill = PALETTE[level]
    kind, p = task["kind"], task["params"]
    if kind == "parabola":
        body = parabola_figure(p, fill, ink)
    elif kind == "hyperbola":
        body = hyperbola_figure(p, fill, ink)
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


def basic() -> list[dict]:
    rows = []
    for a in (1, 2, 3, -1):
        for x in range(-3, 5):
            y = a * x * x
            rows.append(item(
                f"Дана функция {fmt_ax2(a)}. Найдите y при x = {x}.",
                y,
                f"Тема: парабола. y = {a} × ({x})² = {a} × {x * x} = {y}.",
                "parabola", a=a, m=0, n=0, mx=x, my=y, formula=fmt_ax2(a),
            ))
    for n in range(-3, 5):
        for x in (0, 1, 2, -2):
            y = x * x + n
            rows.append(item(
                f"Дана функция {fmt_ax2(1, n)}. Найдите y при x = {x}.",
                y,
                f"Тема: сдвиг параболы. y = ({x})² + ({n}) = {y}.",
                "parabola", a=1, m=0, n=n, mx=x, my=y, formula=fmt_ax2(1, n),
            ))
    for n in range(-4, 5):
        rows.append(item(
            f"Найдите ординату вершины параболы {fmt_ax2(1, n)}.",
            n,
            f"Тема: вершина y = x² + n. Вершина в точке (0; {n}).",
            "parabola", a=1, m=0, n=n, formula=fmt_ax2(1, n),
        ))
        rows.append(item(
            f"Найдите абсциссу вершины параболы {fmt_ax2(1, n)}.",
            0,
            f"Тема: вершина y = x² + n лежит на оси Oy, x = 0.",
            "parabola", a=1, m=0, n=n, formula=fmt_ax2(1, n),
        ))
    for a, x, y in [(1, 2, 4), (1, 3, 9), (2, 2, 8), (3, 2, 12), (1, -2, 4), (2, 3, 18), (4, 1, 4), (5, 1, 5)]:
        rows.append(item(
            f"График {fmt_ax2(a)} проходит через точку ({x}; {y}). Чему равен коэффициент a?",
            a,
            f"Тема: y = ax². {y} = a × {x * x}, a = {a}.",
            "parabola", a=a, m=0, n=0, mx=x, my=y, formula=fmt_ax2(a),
        ))
    for k in (2, 3, 4, 6, 8, 12, -4, -6):
        for x in (1, 2, 3, 4, -1, -2):
            if x == 0 or k % x != 0:
                continue
            y = k // x
            rows.append(item(
                f"Дана функция {fmt_inv(k)}. Найдите y при x = {x}.",
                y,
                f"Тема: обратная пропорциональность. y = {k} : {x} = {y}.",
                "hyperbola", k=k, mx=x, my=y,
            ))
    for a, xs in [
        (1, [-2, -1, 0, 1, 2]),
        (2, [-1, 0, 1, 2]),
        (1, [0, 1, 2, 3]),
        (-1, [-2, -1, 0, 1]),
    ]:
        ys = [a * x * x for x in xs]
        hide = 2 if len(xs) > 2 else 1
        rows.append(item(
            f"Заполните таблицу для {fmt_ax2(a)}. Найдите пропущенное y при x = {xs[hide]}.",
            ys[hide],
            f"Тема: таблица. y = {a} × ({xs[hide]})² = {ys[hide]}.",
            "table", xs=xs, ys=ys, hide=hide, formula=fmt_ax2(a),
        ))
    return take_unique(rows, 70, "basic")


def medium() -> list[dict]:
    rows = []
    for m in range(-3, 5):
        for n in (-2, -1, 0, 1, 2, 3):
            formula = fmt_vertex(1, m, n)
            rows.append(item(
                f"Найдите абсциссу вершины параболы {formula}.",
                m,
                f"Тема: y = (x − m)² + n. Вершина V({m}; {n}), абсцисса {m}.",
                "parabola", a=1, m=m, n=n, formula=formula,
            ))
            rows.append(item(
                f"Найдите ординату вершины параболы {formula}.",
                n,
                f"Тема: вершина V({m}; {n}), ордината {n}.",
                "parabola", a=1, m=m, n=n, formula=formula,
            ))
            x = m + 1
            y = (x - m) ** 2 + n
            rows.append(item(
                f"Дана функция {formula}. Найдите y при x = {x}.",
                y,
                f"Тема: сдвиг. y = ({x} − {m})² + ({n}) = {y}.",
                "parabola", a=1, m=m, n=n, mx=x, my=y, formula=formula,
            ))
    for a in (1, 2, -1, -2):
        rows.append(item(
            f"Ветви параболы {fmt_ax2(a)} направлены вверх? Ответьте да или нет.",
            "да" if a > 0 else "нет",
            f"Тема: знак a. При a = {a} ветви {'вверх' if a > 0 else 'вниз'}.",
            "parabola", a=a, m=0, n=0, formula=fmt_ax2(a),
        ))
    for a, n, x, y in [
        (1, 0, 2, 4), (1, 3, 1, 4), (1, -2, 2, 2), (2, 0, 1, 2),
        (1, 0, 3, 8), (1, 1, 0, 1), (-1, 4, 1, 3), (1, -1, 2, 2),
    ]:
        real = a * x * x + n
        on = real == y
        rows.append(item(
            f"Принадлежит ли точка ({x}; {y}) графику {fmt_ax2(a, n)}? Ответьте да или нет.",
            "да" if on else "нет",
            f"Тема: точка на параболе. y = {a}×{x * x}+({n}) = {real}. "
            + ("Совпало — да." if on else "Не совпало — нет."),
            "parabola", a=a, m=0, n=n, mx=x, my=real, formula=fmt_ax2(a, n),
        ))
    for k in (6, 8, 12, 24, -12, 18):
        for x in (2, 3, 4, -2, -3, 6):
            if x == 0 or k % x != 0:
                continue
            y = k // x
            rows.append(item(
                f"Для {fmt_inv(k)} найдите x, если y = {y}.",
                x,
                f"Тема: y = k/x. {y} = {k}/x → x = {k}/{y} = {x}.",
                "hyperbola", k=k, mx=x, my=y,
            ))
    for c in (4, 9, 16, 25, 36, 1):
        root = int(c ** 0.5)
        rows.append(item(
            f"График {fmt_ax2(1, -c)} пересекает ось Ox. Укажите положительную абсциссу пересечения.",
            root,
            f"Тема: x² − {c} = 0 → x = ±{root}. Положительный корень {root}.",
            "parabola", a=1, m=0, n=-c, mx=root, my=0, formula=fmt_ax2(1, -c),
        ))
    for a, xs in [
        (1, [-2, -1, 0, 1, 2]),
        (2, [-1, 0, 1, 2]),
        (-1, [-2, 0, 1, 2]),
        (1, [1, 2, 3, 4]),
    ]:
        n = 2
        ys = [a * x * x + n for x in xs]
        hide = 1
        formula = fmt_ax2(a, n)
        rows.append(item(
            f"По таблице для {formula} найдите пропущенное y при x = {xs[hide]}.",
            ys[hide],
            f"Тема: таблица. y = {a}×({xs[hide]})² + {n} = {ys[hide]}.",
            "table", xs=xs, ys=ys, hide=hide, formula=formula,
        ))
    return take_unique(rows, 80, "medium")


def high() -> list[dict]:
    rows = []
    for a in (1, 2, -1):
        for m in range(-3, 4):
            for n in range(-2, 4):
                formula = fmt_vertex(a, m, n)
                rows.append(item(
                    f"Для {formula} найдите абсциссу вершины.",
                    m,
                    f"Тема: вершина V({m}; {n}). Абсцисса {m}.",
                    "parabola", a=a, m=m, n=n, formula=formula,
                ))
                rows.append(item(
                    f"Для {formula} найдите ординату вершины.",
                    n,
                    f"Тема: вершина V({m}; {n}). Ордината {n}.",
                    "parabola", a=a, m=m, n=n, formula=formula,
                ))
                x = m + 2
                y = a * (x - m) ** 2 + n
                rows.append(item(
                    f"Для f(x) = {formula[4:]} найдите f({x}).",
                    y,
                    f"Тема: подстановка. f({x}) = {a}×({x}−{m})² + ({n}) = {y}.",
                    "parabola", a=a, m=m, n=n, mx=x, my=y, formula=formula,
                ))
    for a, b, c in [
        (1, -6, 8), (1, -4, 3), (1, -2, -3), (1, 2, -8),
        (1, -8, 15), (1, -10, 21), (1, 4, 3), (1, -6, 5),
        (2, -8, 6), (1, 0, -9), (1, -2, 1), (1, 6, 5),
    ]:
        formula = fmt_quad(a, b, c)
        vx = -b // (2 * a) if (2 * a) != 0 and (-b) % (2 * a) == 0 else None
        if vx is not None:
            vy = a * vx * vx + b * vx + c
            rows.append(item(
                f"Найдите абсциссу вершины параболы {formula}.",
                vx,
                f"Тема: xᵥ = −b : 2a = {minus(b)} : {2 * a} = {vx}.",
                "parabola", a=a, m=vx, n=vy, formula=formula,
            ))
            rows.append(item(
                f"Найдите ординату вершины параболы {formula}.",
                vy,
                f"Тема: подставьте x = {vx} в {formula}: y = {vy}.",
                "parabola", a=a, m=vx, n=vy, formula=formula,
            ))
        for x in (0, 1, 2, -1, 3, 4):
            y = a * x * x + b * x + c
            rows.append(item(
                f"Для f(x) = {formula[4:]} найдите f({x}).",
                y,
                f"Тема: квадратичная функция. f({x}) = {a}×{x * x} + ({b})×{x} + ({c}) = {y}.",
                "parabola", a=a, m=vx or 0, n=a * (vx or 0) ** 2 + b * (vx or 0) + c, mx=x, my=y, formula=formula,
            ))
        y0, y1 = c, a + b + c
        rows.append(item(
            f"Для f(x) = {formula[4:]} найдите f(0) + f(1).",
            y0 + y1,
            f"Тема: f(0) = {y0}, f(1) = {y1}, сумма {y0 + y1}.",
            "parabola", a=a, m=0, n=c, mx=0, my=c, formula=formula,
        ))
    for k in (6, 12, 24, -8, 18, 30):
        for x in (2, 3, -2, 4, 6, -3):
            if x == 0 or k % x != 0:
                continue
            y = k // x
            rows.append(item(
                f"Гипербола {fmt_inv(k)} проходит через ({x}; y). Найдите y.",
                y,
                f"Тема: y = k/x. y = {k} : {x} = {y}.",
                "hyperbola", k=k, mx=x, my=y,
            ))
    for a, n in [(1, -4), (1, -9), (1, -16), (1, 0), (2, -8), (-1, 4)]:
        rows.append(item(
            f"Найдите наименьшее значение функции {fmt_ax2(a, n)}." if a > 0
            else f"Найдите наибольшее значение функции {fmt_ax2(a, n)}.",
            n,
            f"Тема: вершина. При a = {a} экстремум равен n = {n}.",
            "parabola", a=a, m=0, n=n, formula=fmt_ax2(a, n),
        ))
    return take_unique(rows, 100, "high")


def sql_escape(value: str) -> str:
    return str(value).replace("'", "''")


def write_pack(level: str, letter: str, slug: str, rows: list[dict], expected: int) -> None:
    if len(rows) != expected:
        raise SystemExit(f"{level}: {len(rows)} ≠ {expected}")
    TASKS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    csv_name = f"functions-8-{slug}.csv"
    sql_name = f"insert-functions-8-{slug}.sql"
    fieldnames = ["subject", "class_name", "level", "question", "answer", "image", "explanation_of_the_answer"]
    csv_rows, sql_values = [], []
    for i, row in enumerate(rows, start=1):
        filename = f"fn8-{letter}-{i:02d}.svg"
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
