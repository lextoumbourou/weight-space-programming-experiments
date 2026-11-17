"""The cats-vs-dogs figure for the Notes by Lex post, in the blog's style (borrowed from ../mnist-training/figures.py).

    uv run python figures.py --out ~/code/private-notes/public/notes/_media/llm-descent

Everything is read from results/, so run loop.py and baselines.py first.
"""
import argparse
import importlib.util
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
_spec = importlib.util.spec_from_file_location("mnist_figures", HERE.parent / "mnist-training" / "figures.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

RUN = "fable-1"
# Fable's single-feature probe steps in run 1: (step, feature, which class the feature votes for, kept in its best
# network). Each probe's network uses one feature alone, so the confusion matrix says how often it fires per class.
# Steps 3 and 8 are left out: their thresholds were badly centred and Fable re-ran or dropped them.
PROBES = [
    (1, "pointed-ear detector", 0, False),
    (2, "green (grass)", 1, True),
    (4, "texture (edge energy)", 1, True),
    (5, "brightness", 1, False),
    (6, "texture in the centre", 1, False),
    (7, "vertical minus horizontal edges", 1, True),
    (11, "edge polarity", 1, False),
    (13, "vertical minus horizontal, mid scale", 1, False),
    (14, "vertical minus horizontal, coarse", 1, False),
]


def fig_catdog(F, out, run=RUN):
    r = json.loads((RESULTS / run / "run.json").read_text())
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=base.PAPER)
    base.header(fig, F, "Cats vs dogs: what Fable 5.2 measured",
                f"Run 1. Each probe step tested one feature on its own. Its best network (step {r['best_step']}) "
                "kept three: green, texture and edge direction.")
    ax = fig.add_axes([0.25, 0.1, 0.38, 0.66])
    for row, (step, name, votes, kept) in enumerate(PROBES):
        c = np.array(json.loads((RESULTS / run / "steps" / f"{step:02d}" / "metrics.json").read_text())
                     ["train"]["confusion"])
        cats, dogs = c[0, votes] / c[0].sum() * 100, c[1, votes] / c[1].sum() * 100
        y = len(PROBES) - 1 - row
        ax.plot([cats, dogs], [y, y], color=base.INK if kept else base.RULE, linewidth=3, zorder=1)
        ax.scatter([cats], [y], s=170, color=base.LILAC, edgecolor=base.INK, linewidth=1.5, zorder=2)
        ax.scatter([dogs], [y], s=170, color=base.ORANGE, edgecolor=base.INK, linewidth=1.5, zorder=2)
        fig.text(0.24, 0.1 + (y + 0.5) / len(PROBES) * 0.66, f"{name}\nstep {step}", ha="right", va="center",
                 fontproperties=F["display" if kept else "body"], fontsize=14, color=base.INK if kept else base.MUTED,
                 linespacing=1.1)
    ax.set_ylim(-0.5, len(PROBES) - 0.5); ax.set_yticks([]); ax.set_xlim(30, 80)
    base.style_axes(ax, F, "% of photos the feature fires on", "")
    ax.grid(axis="y", visible=False); ax.grid(axis="x", color=base.RULE)
    ax.spines["left"].set_visible(False)
    ax.scatter([], [], s=170, color=base.LILAC, edgecolor=base.INK, label="cats")
    ax.scatter([], [], s=170, color=base.ORANGE, edgecolor=base.INK, label="dogs")
    leg = ax.legend(loc="lower right", frameon=False, prop=F["body"], fontsize=14)
    for t in leg.get_texts():
        t.set_fontsize(14)

    bx = fig.add_axes([0.8, 0.1, 0.17, 0.66])
    adam = json.loads((RESULTS / "baselines" / "adam.json").read_text())
    rs = json.loads((RESULTS / "baselines" / "random-search.json").read_text())
    at = lambda s: [next(c["test_accuracy"] for c in curve if c["step"] == s) for curve in adam.values()]
    bars = [("random search", [c[-1]["test_accuracy"] for c in rs.values()], base.RULE),
            ("Adam, 50 steps", at(50), base.RULE),
            ("Adam, 500 steps", at(500), base.RULE),
            ("Fable 5.2", [r["best_test_accuracy"]], base.PINK),
            ("Adam, 5,000 steps", at(5_000), base.TEAL)]
    for k, (name, vals, colour) in enumerate(bars):
        y = len(bars) - 1 - k
        bx.barh(y, np.mean(vals) * 100, color=colour, height=0.65)
        bx.text(np.mean(vals) * 100 + 1, y, f"{np.mean(vals):.0%}", va="center", fontproperties=F["display"],
                fontsize=15, color=base.INK)
    bx.axvline(50, color=base.INK, linestyle=(0, (2, 2)), linewidth=1.5)
    bx.text(50, len(bars) - 0.35, "coin flip", ha="center", va="bottom", fontproperties=F["body"], fontsize=13,
            color=base.MUTED)
    bx.set_yticks(range(len(bars)), [b[0] for b in bars][::-1])
    bx.set_xlim(40, 85); bx.set_ylim(-0.5, len(bars) - 0.1)
    base.style_axes(bx, F, "test accuracy (%)", "")
    bx.grid(axis="y", visible=False)
    for label in bx.get_yticklabels():
        label.set_fontproperties(F["body"]); label.set_fontsize(14); label.set_color(base.INK)
    bx.tick_params(axis="y", length=0)
    fig.savefig(out / "cats-vs-dogs.png", facecolor=base.PAPER)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--fonts", default="~/code/private-notes/public/theme/static/fonts")
    args = ap.parse_args()
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    fig_catdog(base.fonts(args.fonts), out)
    print("done")
