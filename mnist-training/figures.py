"""Figures for the Notes by Lex post, in the blog's style (paper, Shantell Sans labels, Atkinson text).

    uv run python figures.py --out ~/code/private-notes/public/notes/_media/llm-descent

Everything is read from results/, so run loop.py and baselines.py first.
"""
import argparse
import json
import shutil
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties

RESULTS = Path(__file__).resolve().parent / "results"
PAPER, PAPER_2, INK, MUTED, RULE = "#FBFAF6", "#F2F0E8", "#141414", "#5C5B57", "#DCD9CF"
PINK, TEAL, YELLOW, LILAC, ORANGE = "#FF6FAE", "#2DD4BF", "#FFE84D", "#C4B2FF", "#FFB866"
CONDITION = {"a": ("numbers only", PINK), "b": ("with images", TEAL)}
OUTLINE = [patheffects.withStroke(linewidth=5.5, foreground=INK)]
PROBE_LOSS = 10  # probe steps aren't classifiers; their training loss is in the hundreds or thousands


def spread(ys, gap):
    """Nudge label heights apart so no two are closer than `gap`, keeping their order."""
    order = np.argsort(ys)
    out = np.array(ys, dtype=float)
    for a, b in zip(order, order[1:]):
        out[b] = max(out[b], out[a] + gap)
    return out


def fonts(folder):
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    cache = Path(tempfile.mkdtemp(prefix="blog-fonts."))

    def load(name, weight):
        src = Path(folder).expanduser() / f"{name}-latin-wght-normal.woff2"
        if not src.exists():
            return FontProperties()
        font = instantiateVariableFont(TTFont(src), {"wght": weight}, inplace=False)
        font.flavor = None
        dest = cache / f"{name}-{weight}.ttf"
        font.save(dest)
        return FontProperties(fname=dest)
    return dict(display=load("shantell-sans", 700), body=load("atkinson-hyperlegible-next", 400),
                mono=load("atkinson-hyperlegible-mono", 400))


def runs(condition):
    out = []
    for path in sorted(RESULTS.glob(f"{condition}-*/run.json")):
        out.append(dict(name=path.parent.name, run=json.loads(path.read_text()),
                        history=json.loads((path.parent / "history.json").read_text())))
    return out


def adam(step):
    curves = json.loads((RESULTS / "baselines" / "adam.json").read_text())
    return [next(c["test_accuracy"] for c in curve if c["step"] == step) for curve in curves.values()]


def header(fig, F, title, subtitle):
    fig.text(0.04, 0.94, title, fontproperties=F["display"], fontsize=26, color=INK, va="top")
    fig.text(0.04, 0.865, subtitle, fontproperties=F["body"], fontsize=15, color=MUTED, va="top")


def style_axes(ax, F, xlabel, ylabel):
    ax.set_facecolor(PAPER)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK)
    ax.tick_params(colors=MUTED, labelsize=13)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(F["mono"])
    ax.set_xlabel(xlabel, fontproperties=F["body"], fontsize=15, color=INK)
    ax.set_ylabel(ylabel, fontproperties=F["body"], fontsize=15, color=INK)
    ax.grid(axis="y", color=RULE, linewidth=1)
    ax.set_axisbelow(True)


def fig_mnist(F, out):
    import data
    x, y = data.load()["train"]
    cmap = LinearSegmentedColormap.from_list("ink", [PAPER, INK])
    fig = plt.figure(figsize=(16, 4.4), dpi=120, facecolor=PAPER)
    for d in range(10):
        for r, i in enumerate(np.flatnonzero(y == d)[:2]):
            ax = fig.add_axes([0.02 + d * 0.098, 0.52 - r * 0.47, 0.088, 0.42])
            ax.imshow(x[i, 0], cmap=cmap, vmin=0, vmax=1)
            ax.set_xticks([]); ax.set_yticks([])
            for side in ax.spines.values():
                side.set_color(RULE)
    fig.savefig(out / "mnist-examples.png", facecolor=PAPER)
    plt.close(fig)


def _block(ax, F, x, y, w, h, text, colour, angle, size=30):
    from matplotlib.patches import Rectangle
    from matplotlib.transforms import Affine2D
    r = Rectangle((x - w / 2, y - h / 2), w, h, color=colour, linewidth=0)
    r.set_transform(Affine2D().rotate_deg_around(x, y, angle) + ax.transData)
    ax.add_patch(r)
    ax.text(x, y, text, fontproperties=F["display"], fontsize=size, color=INK, ha="center", va="center",
            rotation=angle, linespacing=1.15)


def _arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>,head_length=1.2,head_width=0.7", color=INK, linewidth=6,
                                shrinkA=0, shrinkB=0))


def fig_loop(F, out):
    """Cut-paper diagram of one step of the loop."""
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")
    _block(ax, F, 3.3, 5.6, 4.6, 1.9, "Claude writes\nbuild_weights()", PINK, 1.5)
    _block(ax, F, 8.3, 7.0, 4.2, 1.6, "sandbox sets all\n5,994 weights", YELLOW, -1.2)
    _block(ax, F, 12.6, 5.6, 4.4, 1.9, "10,000 training\nimages", TEAL, 1.0)
    _block(ax, F, 8.0, 3.0, 5.2, 1.7, "loss, accuracy,\nconfusion matrix", LILAC, -1.5)
    _block(ax, F, 12.9, 1.5, 4.0, 1.4, "test set:\nnever shown", PAPER_2, 1.2, size=24)
    _arrow(ax, 5.0, 6.5, 6.3, 6.95)
    _arrow(ax, 10.4, 6.9, 11.2, 6.4)
    _arrow(ax, 11.6, 4.6, 10.4, 3.5)
    _arrow(ax, 5.4, 3.0, 3.6, 4.5)
    ax.text(3.0, 3.0, "next step", fontproperties=F["display"], fontsize=22, color=MUTED, ha="center")
    ax.text(0.6, 8.4, "One step of LLM Descent", fontproperties=F["display"], fontsize=26, color=INK)
    fig.savefig(out / "loop.png", facecolor=PAPER)
    plt.close(fig)


def fig_descent(F, out):
    """Best training loss so far for every run, numbers only (left) and with images (right)."""
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "The descent", "Line: best training loss so far. Dots: each step's loss. Ticks at the top: probe "
           "steps, where the network measured its own features instead of classifying.")
    ceiling = 2.6
    for k, condition in enumerate("ab"):
        label, colour = CONDITION[condition]
        ax = fig.add_axes([0.07 + k * 0.47, 0.11, 0.42, 0.62])
        ends = []
        for i, r in enumerate(runs(condition)):
            h = [s for s in r["history"] if s["ok"]]
            x = np.array([s["step"] for s in h]); loss = np.array([s["train_loss"] for s in h])
            probe = loss > PROBE_LOSS
            best = np.minimum.accumulate(np.where(probe, np.inf, loss))
            shade = [1.0, 0.75, 0.5][i]
            ax.scatter(x[~probe], np.minimum(loss[~probe], ceiling), s=28, color=colour, alpha=0.5 * shade,
                       edgecolor=INK, linewidth=0.6, zorder=2)
            ax.scatter(x[probe], [ceiling - 0.05 - 0.09 * i] * probe.sum(), marker="|", s=200, color=colour,
                       linewidth=3, zorder=2)
            ax.step(x, best, where="post", color=colour, linewidth=3.2, alpha=shade, path_effects=OUTLINE, zorder=3)
            ends.append((x[-1], best[-1], f"run {r['name']}: {r['run']['best_test_accuracy']:.0%}"))
        for (x_end, y, text), y_label in zip(ends, spread([e[1] for e in ends], 0.09)):
            ax.text(x_end + 0.8, y_label, text, fontproperties=F["display"], fontsize=14, color=INK, va="center")
        style_axes(ax, F, "step", "training loss" if k == 0 else "")
        ax.set_title(label, fontproperties=F["display"], fontsize=20, color=INK, loc="left", pad=14)
        ax.set_xlim(0.5, 60); ax.set_ylim(0.5, ceiling)
    fig.savefig(out / "loss-by-step.png", facecolor=PAPER)
    plt.close(fig)


def fig_final_scores(F, out):
    rs = json.loads((RESULTS / "baselines" / "random-search.json").read_text())
    groups = [("random search\n(50 evaluations)", [c[-1]["test_accuracy"] for c in rs.values()], MUTED),
              ("Opus 5.5\nnumbers only", [r["run"]["best_test_accuracy"] for r in runs("a")], PINK),
              ("Opus 5.5\nwith images", [r["run"]["best_test_accuracy"] for r in runs("b")], TEAL),
              ("Adam\n50 steps", adam(50), ORANGE), ("Adam\n5,000 steps", adam(5_000), ORANGE)]
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Where it landed", "Test accuracy on 10,000 MNIST images. Each dot is one run or seed; the bar "
           "is the mean. Claude's runs are scored on their lowest-training-loss network.")
    ax = fig.add_axes([0.07, 0.16, 0.9, 0.6])
    for i, (label, vals, colour) in enumerate(groups):
        ax.bar(i, np.mean(vals), width=0.6, color=colour, edgecolor=INK, linewidth=2, alpha=0.85)
        ax.scatter([i] * len(vals), vals, s=70, color=PAPER, edgecolor=INK, linewidth=2, zorder=3)
        ax.text(i, np.mean(vals) + 0.03, f"{np.mean(vals):.0%}", fontproperties=F["display"], fontsize=20,
                color=INK, ha="center")
    style_axes(ax, F, "", "test accuracy")
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([f"{v:.0%}" for v in ax.get_yticks()], fontproperties=F["mono"])
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([g[0] for g in groups], fontproperties=F["display"], fontsize=15, color=INK)
    fig.savefig(out / "final-scores.png", facecolor=PAPER)
    plt.close(fig)


def best_weights(run):
    r = json.loads((RESULTS / run / "run.json").read_text())
    return dict(np.load(RESULTS / run / "steps" / f"{r['best_step']:02d}" / "weights.npz"))


def fig_filters(F, out, run):
    written = best_weights(run)["conv1.weight"]
    learned = np.load(RESULTS / "baselines" / "adam-seed-0-5000-steps.npz")["conv1.weight"]
    cmap = LinearSegmentedColormap.from_list("signed", [PINK, PAPER_2, TEAL])
    fig = plt.figure(figsize=(16, 6.4), dpi=120, facecolor=PAPER)
    header(fig, F, "The first layer: written by Opus 5.5, and learned by Adam",
           "Eight 5 × 5 filters each. Teal is positive, pink negative; each filter has its own scale.")
    for row, (name, w) in enumerate([("Opus 5.5 (written)", written), ("Adam (learned)", learned)]):
        fig.text(0.04, 0.6 - row * 0.36, name, fontproperties=F["display"], fontsize=18, color=INK, va="center")
        for c in range(8):
            ax = fig.add_axes([0.27 + c * 0.088, 0.46 - row * 0.36, 0.075, 0.28])
            m = np.abs(w[c, 0]).max() or 1
            ax.imshow(w[c, 0], cmap=cmap, vmin=-m, vmax=m)
            ax.set_xticks([]); ax.set_yticks([])
            for side in ax.spines.values():
                side.set_color(RULE)
    fig.savefig(out / "filters-written-vs-learned.png", facecolor=PAPER)
    plt.close(fig)


def fig_confusions(F, out, run, steps):
    cmap = LinearSegmentedColormap.from_list("pink", [PAPER_2, PINK])
    fig = plt.figure(figsize=(16, 7.2), dpi=120, facecolor=PAPER)
    header(fig, F, "What Claude sees: the training confusion matrix",
           f"Run {run}. Rows are the true digit, columns the predicted digit; darker means more images.")
    for k, step in enumerate(steps):
        m = json.loads((RESULTS / run / "steps" / f"{step:02d}" / "metrics.json").read_text())["train"]
        cm = np.array(m["confusion"], dtype=float)
        ax = fig.add_axes([0.06 + k * 0.31, 0.08, 0.26, 0.62])
        ax.imshow(cm / cm.sum(1, keepdims=True), cmap=cmap, vmin=0, vmax=1)
        ax.set_title(f"step {step}: {m['accuracy']:.0%} training accuracy", fontproperties=F["display"],
                     fontsize=17, color=INK, pad=10)
        ax.set_xticks(range(10)); ax.set_yticks(range(10))
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(F["mono"]); label.set_color(MUTED)
        ax.set_xlabel("predicted", fontproperties=F["body"], fontsize=13, color=INK)
        if k == 0:
            ax.set_ylabel("true", fontproperties=F["body"], fontsize=13, color=INK)
        for side in ax.spines.values():
            side.set_visible(False)
    fig.savefig(out / "confusion-over-steps.png", facecolor=PAPER)
    plt.close(fig)


def copy_images_shown(out, run, step):
    """The exact images condition B saw: its 50 examples, and one step's mistakes."""
    shutil.copy(RESULTS / run / "steps" / "01" / "examples.png", out / "condition-b-examples.png")
    shutil.copy(RESULTS / run / "steps" / f"{step:02d}" / "mistakes.png", out / "condition-b-mistakes.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--fonts", default="~/code/private-notes/public/theme/static/fonts")
    args = ap.parse_args()
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    F = fonts(args.fonts)
    fig_mnist(F, out)
    fig_loop(F, out)
    fig_descent(F, out)
    fig_final_scores(F, out)
    best_a = min(runs("a"), key=lambda r: r["run"]["best_train_loss"])["name"]
    fig_filters(F, out, best_a)
    fig_confusions(F, out, best_a, (1, 6, json.loads((RESULTS / best_a / "run.json").read_text())["best_step"]))
    copy_images_shown(out, "b-1", 16)
    print("best numbers-only run:", best_a, sorted(p.name for p in out.glob("*.png")))
