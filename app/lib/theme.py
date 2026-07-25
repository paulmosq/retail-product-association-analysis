"""Visual system for the app: a clean product-dashboard look on a soft
blue-gray canvas, white rounded cards with a soft shadow, one type family
(Plus Jakarta Sans) carrying both headings and numbers, and a vivid,
distinct color per product category.

`inject_theme()` loads the font + tokens once, including the CSS that turns
`st.container(border=True)` into the white shadow-card used throughout.
The render helpers (`kpi_row`, `stat_list`, `significance_pill`,
`category_legend`) keep that card language consistent across pages.
"""

import base64
from functools import lru_cache
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"

CATEGORY_COLORS = {
    "dairy": "#3B82F6",
    "meats": "#EF4444",
    "produce": "#14B8A6",
    "snacks": "#F59E0B",
    "cleaning": "#8B5CF6",
    "care": "#EC4899",
}


@lru_cache(maxsize=1)
def _font_b64(filename: str) -> str:
    return base64.b64encode((ASSETS_DIR / filename).read_bytes()).decode("ascii")


def inject_theme() -> None:
    jakarta = _font_b64("plusjakartasans-var.woff2")

    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'Plus Jakarta Sans';
            font-weight: 400 800;
            src: url(data:font/woff2;base64,{jakarta}) format('woff2-variations');
        }}

        :root {{
            --bg: #EEF3F8;
            --card: #FFFFFF;
            --ink: #16202A;
            --ink-soft: #5B6472;
            --ink-faint: #8B94A3;
            --line: #E4E9EF;
            --accent: #3B82F6;
            --good: #10B981;
            --neutral-pill: #94A3B8;
            --font: 'Plus Jakarta Sans', -apple-system, 'Segoe UI', sans-serif;
            --shadow: 0 1px 2px rgba(16,24,40,0.04), 0 8px 24px rgba(16,24,40,0.06);
            --radius-card: 20px;
        }}

        html, body, [class*="css"] {{
            font-family: var(--font);
        }}

        [data-testid="stAppViewContainer"] {{
            background: var(--bg);
            color: var(--ink);
        }}
        [data-testid="stSidebar"] {{
            background: var(--bg);
            border-right: none;
        }}
        [data-testid="stSidebarContent"] {{
            font-family: var(--font);
        }}

        h1, h2, h3 {{
            font-family: var(--font) !important;
            font-weight: 800 !important;
            letter-spacing: -0.01em;
            color: var(--ink) !important;
        }}
        p, span, div, label {{
            font-family: var(--font);
        }}

        /* Any st.container() whose first element is a card_title becomes the
           white shadow-card. Keyed off our own marker class rather than
           Streamlit's internal (build-hash-dependent) border implementation. */
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"]:first-child .card-title) {{
            background: var(--card);
            border-radius: var(--radius-card);
            box-shadow: var(--shadow);
            padding: 20px 24px 24px;
            margin-bottom: 20px;
        }}

        .card-title {{
            font-family: var(--font);
            font-weight: 700;
            font-size: 18px;
            color: var(--ink);
            margin: 4px 0 14px;
        }}

        [data-testid="stMetricValue"] {{
            font-family: var(--font) !important;
            font-weight: 800 !important;
        }}

        /* KPI numbers: bold black figure, muted label, optional colored sub-note */
        .kpi-row {{ display: flex; flex-wrap: wrap; gap: 28px 44px; margin: 2px 0 4px; }}
        .kpi-item {{ flex: 0 0 auto; }}
        .kpi-item .k-label {{ font-size: 13px; color: var(--ink-soft); margin: 0 0 4px; font-weight: 500; }}
        .kpi-item .k-value {{ font-weight: 800; font-size: 30px; color: var(--ink); margin: 0; line-height: 1.15; letter-spacing: -0.01em; }}
        .kpi-item .k-sub {{ font-size: 12.5px; color: var(--ink-faint); margin: 4px 0 0; }}

        /* plain stat rows: label left, value right, no leader dots */
        .stat-list {{ display: flex; flex-direction: column; gap: 10px; margin: 4px 0 6px; }}
        .stat-row {{ display: flex; align-items: baseline; justify-content: space-between; gap: 12px; font-size: 14px; }}
        .stat-row .lbl {{ color: var(--ink-soft); }}
        .stat-row .val {{ font-weight: 700; color: var(--ink); }}
        .stat-row .val.hot {{ color: var(--good); }}

        /* status pill, solid fill + white text, like a Success/Failed tag */
        .pill {{
            display: inline-flex; align-items: center; gap: 6px;
            font-weight: 600; font-size: 12.5px; color: #FFFFFF;
            padding: 4px 12px; border-radius: 999px; background: var(--neutral-pill);
        }}
        .pill.good {{ background: var(--good); }}

        /* category legend: colored dot + label, no chrome */
        .cat-row {{ display: flex; flex-wrap: wrap; column-gap: 20px; row-gap: 8px; margin: 4px 0 6px; }}
        .cat-chip {{ display: inline-flex; align-items: center; gap: 8px; font-weight: 500; font-size: 13.5px; color: var(--ink); }}
        .cat-chip .dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}

        [data-testid="stDataFrame"] {{ font-family: var(--font); }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def card_title(text: str) -> None:
    st.markdown(f'<p class="card-title">{text}</p>', unsafe_allow_html=True)


def kpi_row(items: list[tuple[str, str, str | None]]) -> None:
    """items: list of (label, value, optional sublabel)."""
    entries = []
    for label, value, sub in items:
        sub_html = f'<p class="k-sub">{sub}</p>' if sub else ""
        entries.append(
            f'<div class="kpi-item"><p class="k-label">{label}</p>'
            f'<p class="k-value">{value}</p>{sub_html}</div>'
        )
    st.markdown(f'<div class="kpi-row">{"".join(entries)}</div>', unsafe_allow_html=True)


def stat_list(items: list[tuple[str, str, bool]]) -> None:
    """items: list of (label, value, hot) where hot highlights the value in green."""
    rows = []
    for label, value, hot in items:
        cls = "val hot" if hot else "val"
        rows.append(
            f'<div class="stat-row"><span class="lbl">{label}</span>'
            f'<span class="{cls}">{value}</span></div>'
        )
    st.markdown(f'<div class="stat-list">{"".join(rows)}</div>', unsafe_allow_html=True)


def significance_pill(is_significant: bool, label: str | None = None) -> str:
    text = label or ("Significant" if is_significant else "Not significant")
    cls = "pill good" if is_significant else "pill"
    return f'<span class="{cls}">{text}</span>'


def category_legend(categories: list[str], color_key_map: dict[str, str], short_name_map: dict[str, str]) -> None:
    chips = []
    for cat in categories:
        color = CATEGORY_COLORS[color_key_map[cat]]
        chips.append(
            f'<span class="cat-chip"><span class="dot" style="background:{color}"></span>'
            f'{short_name_map.get(cat, cat)}</span>'
        )
    st.markdown(f'<div class="cat-row">{"".join(chips)}</div>', unsafe_allow_html=True)
