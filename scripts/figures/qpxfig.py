"""Shared style for the QPX paper figures.

Scientific Data / Nature figure rules: sans-serif type (Arial metrics via Liberation Sans),
5-7 pt text, bold lower-case panel letters in the type size of the panel titles (Scientific
Data: "in the same type-size as used elsewhere in the figure"), white background, editable
embedded fonts,
an accessible palette (Okabe-Ito, Wong 2011), axis lines with ticks and units in parentheses.
"""

from pathlib import Path

import matplotlib as mpl
import numpy as np
from matplotlib.text import Text
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / "figures"

MM = 1 / 25.4
SINGLE = 89 * MM
DOUBLE = 183 * MM

# Processing routes, in the order and with the names of Table 3.
ROUTES = ["ID only", "DIA-NN", "OpenMS"]
ROUTE_COLOURS = {"ID only": "#0072B2", "DIA-NN": "#E69F00", "OpenMS": "#009E73"}

INK = "#1a1a1a"
MUTED = "#595959"
RULE = "#bfbfbf"
PANEL_FILL = "#f2f2f2"
LABEL_SIZE = 6.5  # panel letters and panel titles
MIN_TEXT = 5  # smallest type size the journal accepts
MONO = "Liberation Mono"  # column and file names

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica"],
    "font.size": 6,
    "axes.titlesize": LABEL_SIZE,
    "axes.labelsize": 6,
    "xtick.labelsize": 5.5,
    "ytick.labelsize": 5.5,
    "legend.fontsize": 6,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 2,
    "ytick.major.size": 2,
    "xtick.minor.width": 0.4,
    "xtick.minor.size": 1.2,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "text.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlelocation": "left",
    "axes.titlepad": 3,
    "legend.frameon": False,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})


def label_panels(fig, axes, titles, letters="abcdefgh"):
    """Put a bold panel label and a title above each axes. Panels that share a grid column
    start their labels at the same x, the leftmost edge of the column (tick labels included)."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    width, height = fig.get_size_inches() * 25.4
    left = {}
    for ax in axes:
        column = round(ax.get_position().x0, 3)
        x0 = inv.transform(ax.get_tightbbox(renderer).p0)[0]
        left[column] = min(left.get(column, x0), x0)
    for ax, letter, title in zip(axes, letters, titles):
        x0 = left[round(ax.get_position().x0, 3)]
        y = ax.get_position().y1 + 2.5 / height
        fig.text(x0, y, letter, fontsize=LABEL_SIZE, fontweight="bold", va="baseline")
        fig.text(x0 + 2.8 / width, y, title, fontsize=LABEL_SIZE, va="baseline")


def route_strip(ax, values, note=None, seed=1):
    """One row per processing route: a jittered point per dataset and a bar at the route median.
    values maps a route to its per-dataset values; a route without values shows the note."""
    rng = np.random.default_rng(seed)
    for i, route in enumerate(ROUTES):
        y0 = len(ROUTES) - 1 - i
        v = np.asarray(values.get(route, []), dtype=float)
        if len(v) == 0:
            if note:
                ax.text(0.5, y0, note, transform=ax.get_yaxis_transform(), ha="center",
                        va="center", fontsize=5.5, color=MUTED)
            continue
        ax.scatter(v, y0 + rng.uniform(-0.22, 0.22, len(v)), s=5, color=ROUTE_COLOURS[route],
                   edgecolors="white", linewidths=0.3, zorder=3)
        m = np.median(v)
        ax.plot([m, m], [y0 - 0.32, y0 + 0.32], color=INK, lw=0.8, zorder=4)
    ax.set_yticks(range(len(ROUTES))[::-1], ROUTES)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_ylim(-0.6, len(ROUTES) - 0.4)


def thousands(x, _pos=None):
    """Tick formatter: plain numbers with comma thousands separators."""
    return f"{x:,.0f}"


def log_axis(ax, values):
    """Log x axis spanning whole decades around the values, labelled 1, 10, 100, 1,000, ..."""
    lo, hi = np.floor(np.log10(np.min(values))), np.ceil(np.log10(np.max(values)))
    ax.set_xscale("log")
    ax.set_xlim(10 ** lo / 1.25, 10 ** max(hi, lo + 1) * 1.25)
    ax.xaxis.set_major_locator(LogLocator(base=10))
    ax.xaxis.set_major_formatter(FuncFormatter(thousands))
    ax.xaxis.set_minor_formatter(NullFormatter())


def check_text(fig):
    """Fail if any drawn text is smaller than the journal minimum or reaches outside the
    canvas. Texts are collected while drawing, which skips tick labels outside the axis limits."""
    drawn = []
    draw = Text.draw

    def record(text, renderer):
        drawn.append(text)
        return draw(text, renderer)

    Text.draw = record
    try:
        fig.canvas.draw()
    finally:
        Text.draw = draw
    renderer = fig.canvas.get_renderer()
    canvas = fig.bbox
    for text in drawn:
        if not text.get_visible() or not text.get_text().strip():
            continue
        if text.get_fontsize() < MIN_TEXT:
            raise SystemExit(f"text {text.get_text()!r} is {text.get_fontsize()} pt")
        box = text.get_window_extent(renderer)
        if (box.x0 < canvas.x0 - 1 or box.y0 < canvas.y0 - 1 or box.x1 > canvas.x1 + 1
                or box.y1 > canvas.y1 + 1):
            raise SystemExit(f"text {text.get_text()!r} reaches outside the figure")


def save(fig, name):
    """Write the PDF used by the LaTeX build and a 450 dpi PNG used by the docx build."""
    check_text(fig)
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / f"{name}.pdf")
    fig.savefig(FIGURES / f"{name}.png", dpi=450)
