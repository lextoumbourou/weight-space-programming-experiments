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
# Measurement steps whose loss stays low: run 1's template tournaments, whose ten outputs are variants of a digit
# rather than the ten digits (see their replies).
EXTRA_PROBES = {"fable-a-1": {6, 7}}


def is_probe(run, step):
    return step["train_loss"] > PROBE_LOSS or step["step"] in EXTRA_PROBES.get(run, ())


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


def runs(prefix):
    """Runs named <prefix>-<n>, for example runs("a") for Opus 5.5 and runs("fable-a") for Fable 5.2."""
    out = []
    for path in sorted(RESULTS.glob(f"{prefix}-[0-9]*/run.json")):
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


def fig_descent(F, out, prefix="fable-a"):
    """Best training loss so far for each run of one condition, with each step's loss and the probe steps."""
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "The descent", "Line: best training loss so far. Dots: each step's loss. Ticks at the top: probe "
           "steps, where the network measured its own features instead of classifying.")
    ceiling = 2.6
    ax = fig.add_axes([0.07, 0.11, 0.74, 0.66])
    ends, last = [], 0
    for i, (r, colour) in enumerate(zip(runs(prefix), [PINK, TEAL, ORANGE])):
        h = [s for s in r["history"] if s["ok"]]
        x = np.array([s["step"] for s in h]); loss = np.array([s["train_loss"] for s in h])
        probe = np.array([is_probe(r["name"], s) for s in h])
        best = np.minimum.accumulate(np.where(probe, np.inf, loss))
        ax.scatter(x[~probe], np.minimum(loss[~probe], ceiling), s=40, color=colour, alpha=0.6, edgecolor=INK,
                   linewidth=1, zorder=2)
        ax.scatter(x[probe], [ceiling - 0.06 - 0.09 * i] * probe.sum(), marker="|", s=260, color=colour,
                   linewidth=3, zorder=2)
        ax.step(x, best, where="post", color=colour, linewidth=3.5, path_effects=OUTLINE, zorder=3)
        ends.append((best[-1], f"run {i + 1}: {r['run']['best_test_accuracy']:.0%} test", colour))
        last = max(last, x[-1])
    for (y, text, colour), y_label in zip(ends, spread([e[0] for e in ends], 0.1)):
        ax.plot([last + 1.0], [y_label], marker="o", markersize=12, color=colour, markeredgecolor=INK,
                markeredgewidth=2, clip_on=False)
        ax.text(last + 1.8, y_label, text, fontproperties=F["display"], fontsize=16, color=INK, va="center")
    style_axes(ax, F, "step (one reply, one round of feedback)", "training loss (cross-entropy)")
    ax.set_xlim(0.5, last + 0.6); ax.set_ylim(0.2, ceiling)
    fig.savefig(out / "loss-by-step.png", facecolor=PAPER)
    plt.close(fig)


def fig_final_scores(F, out):
    rs = json.loads((RESULTS / "baselines" / "random-search.json").read_text())
    groups = [("random search\n(50 evaluations)", [c[-1]["test_accuracy"] for c in rs.values()], MUTED),
              ("Opus 5.5", [r["run"]["best_test_accuracy"] for r in runs("a")], LILAC),
              ("Fable 5.2", [r["run"]["best_test_accuracy"] for r in runs("fable-a")], PINK),
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


STORY_RUN = "fable-a-1"
STORY_STAGES = [(1, 3, "templates", "#A9D6FF"), (4, 9, "testing\ndetectors", YELLOW),
                (10, 18, "corners", LILAC), (19, 30, "measuring strokes", "#BDEB7A"),
                (31, 40, "rebuilt from\nmeasurements", TEAL), (41, 50, "calibration", "#E2C59C")]


def fig_story(F, out, run=STORY_RUN):
    """One run's test accuracy at every step, on bands for each classical technique it moved through."""
    h = json.loads((RESULTS / run / "history.json").read_text())
    x = np.array([s["step"] for s in h if s["ok"]]); acc = np.array([s["test_accuracy"] for s in h if s["ok"]])
    probe = np.array([is_probe(run, s) for s in h if s["ok"]])
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Fable 5.2, run 1, step by step", "Test accuracy of every network it wrote. Probe steps, which measure "
           "features instead of classifying, are marked along the bottom.")
    ax = fig.add_axes([0.07, 0.11, 0.9, 0.62])
    for a, b, label, colour in STORY_STAGES:
        ax.axvspan(a - 0.5, b + 0.5, color=colour, alpha=0.35, linewidth=0)
        ax.text((a + b) / 2, 1.02, label, fontproperties=F["display"], fontsize=13 if b - a < 4 else 15, color=INK,
                ha="center", va="bottom", transform=ax.get_xaxis_transform())
    ax.plot(x[~probe], acc[~probe], color=PINK, linewidth=3.5, path_effects=OUTLINE, marker="o", markersize=7,
            markeredgecolor=INK, zorder=3)
    ax.scatter(x[probe], [0.04] * probe.sum(), marker="|", s=300, color=INK, linewidth=3, zorder=3)
    best = json.loads((RESULTS / run / "run.json").read_text())["best_step"]
    ax.annotate(f"best: {acc[list(x).index(best)]:.1%}", xy=(best, acc[list(x).index(best)]), xytext=(best - 9, 0.74),
                fontproperties=F["display"], fontsize=16, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.8, shrinkA=4, shrinkB=6))
    level = float(np.mean(adam(50)))
    ax.axhline(level, color=INK, linestyle=":", linewidth=2)
    ax.text(1, level + 0.015, f"Adam, 50 gradient steps ({level:.0%})", fontproperties=F["body"], fontsize=13,
            color=MUTED)
    style_axes(ax, F, "step", "test accuracy")
    ax.set_ylim(0, 1); ax.set_xlim(0.5, x[-1] + 0.5)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([f"{v:.0%}" for v in ax.get_yticks()], fontproperties=F["mono"])
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    fig.savefig(out / "fable-run-1-story.png", facecolor=PAPER)
    plt.close(fig)


def best_weights(run):
    r = json.loads((RESULTS / run / "run.json").read_text())
    return dict(np.load(RESULTS / run / "steps" / f"{r['best_step']:02d}" / "weights.npz"))


def fig_filters(F, out, run, step=1):
    """Fable's first layer at the step the article discusses (step 1: four line detectors, four filters still empty),
    against Adam's after 5,000 steps."""
    written = step_weights(run, step)["conv1.weight"]
    learned = np.load(RESULTS / "baselines" / "adam-seed-0-5000-steps.npz")["conv1.weight"]
    cmap = LinearSegmentedColormap.from_list("signed", [PINK, PAPER_2, TEAL])
    fig = plt.figure(figsize=(16, 6.4), dpi=120, facecolor=PAPER)
    header(fig, F, "The first layer: written by Fable 5.2, and learned by Adam",
           f"Eight 5 × 5 filters each: Fable's at step {step}, Adam's after 5,000 steps. Teal is positive, pink negative.")
    for row, (name, w) in enumerate([(f"Fable 5.2 (step {step})", written), ("Adam (learned)", learned)]):
        fig.text(0.04, 0.6 - row * 0.36, name, fontproperties=F["display"], fontsize=18, color=INK, va="center")
        for c in range(8):
            ax = fig.add_axes([0.27 + c * 0.088, 0.46 - row * 0.36, 0.075, 0.28])
            m = np.abs(w[c, 0]).max()
            ax.imshow(w[c, 0] if m else np.zeros((5, 5)), cmap=cmap, vmin=-(m or 1), vmax=m or 1)
            if not m:
                ax.text(2, 2, "empty", ha="center", va="center", fontproperties=F["body"], fontsize=12, color=MUTED)
            ax.set_xticks([]); ax.set_yticks([])
            for side in ax.spines.values():
                side.set_color(RULE)
    fig.savefig(out / "filters-written-vs-learned.png", facecolor=PAPER)
    plt.close(fig)


def fig_confusions(F, out, run, steps):
    cmap = LinearSegmentedColormap.from_list("pink", [PAPER_2, PINK])
    fig = plt.figure(figsize=(16, 7.2), dpi=120, facecolor=PAPER)
    header(fig, F, "What Claude sees: the training confusion matrix",
           f"Fable 5.2, run {run[-1]}. Rows are the true digit, columns the predicted digit; darker means more images.")
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


# ---------------------------------------------------------------------------------------------------------------
# Explainer figures for the 1990s pipeline: built from run 1's own weights and results.
# ---------------------------------------------------------------------------------------------------------------
CORNERS = [("top-left", 4, PINK), ("top-right", 5, TEAL), ("bottom-left", 6, ORANGE), ("bottom-right", 7, LILAC)]
LOOP_SIZES = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (3, 2), (3, 3)]  # step 5's conv2 channels 8 to 15


def step_weights(run, step):
    return dict(np.load(RESULTS / run / "steps" / f"{step:02d}" / "weights.npz"))


def activations(w, img):
    """conv1 -> ReLU, pooled, and conv2 -> ReLU for one 28 x 28 image, in numpy (same maths as network.py)."""
    from scipy.signal import correlate2d
    r1 = np.stack([np.maximum(correlate2d(img, w["conv1.weight"][k, 0], "valid") + w["conv1.bias"][k], 0)
                   for k in range(8)])
    p1 = r1.reshape(8, 12, 2, 12, 2).max(axis=(2, 4))
    r2 = np.stack([np.maximum(sum(correlate2d(p1[i], w["conv2.weight"][o, i], "valid") for i in range(8))
                              + w["conv2.bias"][o], 0) for o in range(16)])
    return r1, p1, r2


def _digit_axes(ax, img):
    ax.imshow(img, cmap=LinearSegmentedColormap.from_list("ink", [PAPER, "#8A8880"]), vmin=0, vmax=1,
              extent=(-0.5, 27.5, 27.5, -0.5))
    ax.set_xlim(-0.5, 27.5); ax.set_ylim(27.5, -0.5)
    ax.set_xticks([]); ax.set_yticks([])
    for side in ax.spines.values():
        side.set_color(RULE)


def _loops(r2):
    """The strongest loop found in the upper and the lower half: (strength, (top, left, bottom, right)) in pixels."""
    found = []
    for half in (range(0, 4), range(4, 8)):
        best = (0.0, None)
        for c, (sy, sx) in enumerate(LOOP_SIZES):
            for i in half:
                for j in range(8):
                    if r2[8 + c, i, j] > best[0]:
                        r0, c0 = (4 - sy) // 2, (4 - sx) // 2
                        px = lambda m: 2 * m + 2.5
                        best = (float(r2[8 + c, i, j]),
                                (px(i + r0), px(j + c0), px(i + r0 + sy), px(j + c0 + sx)))
        found.append(best)
    return found


def fig_loop_detector(F, out, run=STORY_RUN, step=5, eight=1184, one=367):
    from matplotlib.patches import Rectangle
    import data
    x, y = data.load()["train"]
    w = step_weights(run, step)
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "A hand-built loop detector",
           f"Fable 5.2, run {run[-1]}, step {step}. Four corner filters have to fire around a blank middle.")
    cmap = LinearSegmentedColormap.from_list("signed", [PINK, PAPER_2, INK])
    for n, (name, k, colour) in enumerate(CORNERS):
        ax = fig.add_axes([0.05 + (n % 2) * 0.14, 0.46 - (n // 2) * 0.3, 0.11, 0.2])
        m = np.abs(w["conv1.weight"][k, 0]).max()
        ax.imshow(w["conv1.weight"][k, 0], cmap=cmap, vmin=-m, vmax=m)
        ax.set_xticks([]); ax.set_yticks([])
        for side in ax.spines.values():
            side.set_color(colour); side.set_linewidth(5)
        ax.set_title(name, fontproperties=F["display"], fontsize=16, color=INK, pad=8)
    fig.text(0.05, 0.08, "Grey: ink should be here.\nPink: must be blank.", fontproperties=F["body"], fontsize=14,
             color=MUTED)
    for n, (idx, caption) in enumerate([(eight, "An 8: a loop at the top and the bottom"),
                                        (one, "A 1: no corners, so it stays silent")]):
        img = x[idx, 0]
        r1, _, r2 = activations(w, img)
        ax = fig.add_axes([0.37 + n * 0.32, 0.1, 0.28, 0.62])
        _digit_axes(ax, img)
        for strength, box in _loops(r2):
            if box:
                t, l, b, r = box
                ax.add_patch(Rectangle((l, t), r - l, b - t, fill=False, edgecolor=INK, linewidth=3,
                                       linestyle=(0, (3, 2)), zorder=3))
                for (cy, cx), (_, _, colour) in zip([(t, l), (t, r), (b, l), (b, r)], CORNERS):
                    ax.scatter([cx], [cy], s=420, color=colour, edgecolor=INK, linewidth=2, zorder=4)
        found = sum(1 for s, _ in _loops(r2) if s > 0)
        ax.set_title(caption, fontproperties=F["display"], fontsize=17, color=INK, pad=10)
        ax.text(13.5, 29.8, f"loop detector: {'fires' if found else 'silent'}", fontproperties=F["body"],
                fontsize=15, color=MUTED, ha="center", va="top")
    fig.savefig(out / "loop-detector.png", facecolor=PAPER)
    plt.close(fig)


def submission_locals(run, step, before):
    """Run a step's build_weights() up to the line starting with `before` and return its local variables, so a
    figure can draw what Claude wrote (its digit skeletons, say) from Claude's own code."""
    import math
    src = (RESULTS / run / "steps" / f"{step:02d}" / "submission.py").read_text()
    cut = src.index(before)
    src = src[:cut] + "    return locals()\n"
    scope = {"np": np, "math": math}
    exec(compile(src, f"{run}-step-{step}", "exec"), scope)
    return scope["build_weights"]()


ORIENTATIONS = ["horizontal", "/", "vertical", "\\"]


def fig_templates(F, out, run=STORY_RUN, step=1, digit=2, image=None):
    import data
    import network
    from scipy.special import softmax
    v = submission_locals(run, step, "    fc_w = np.zeros((10, 256)")
    x, y = data.load()["train"]
    w = step_weights(run, step)
    probs = softmax(network.logits(w, x), axis=1)
    if image is None:  # a typical 2 that the step-1 network gets right with a clear margin
        right = np.flatnonzero((y == digit) & (probs.argmax(1) == digit))
        image = int(right[np.argsort(probs[right, digit])[len(right) // 2]])
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Hand-drawn templates",
           f"Fable 5.2, run {run[-1]}, step {step}. Every digit drawn as strokes in code, then turned into a table of "
           "where each stroke direction should be.")
    for d in range(10):
        ax = fig.add_axes([0.04 + d * 0.094, 0.6, 0.08, 0.17])
        ax.set_facecolor(PAPER_2)
        strokes, shear = v["digits"][d]
        for weight, pts in v["place"](strokes, shear):
            ax.plot(pts[:, 0], pts[:, 1], color=PINK if d == digit else INK, linewidth=4 if weight >= 0.35 else 2,
                    alpha=1 if weight >= 0.35 else 0.45, solid_capstyle="round")
        ax.set_xlim(-0.5, 27.5); ax.set_ylim(27.5, -0.5); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for side in ax.spines.values():
            side.set_visible(False)
    strokes, shear = v["digits"][digit]
    P = v["P_LO"] + (v["P_HI"] - v["P_LO"]) * v["render"](v["place"](strokes, shear))
    fig.text(0.04, 0.5, f"The table for {digit}: how likely each stroke direction is in each 4 × 4 cell",
             fontproperties=F["display"], fontsize=17, color=INK)
    cmap = LinearSegmentedColormap.from_list("p", [PAPER_2, PINK])
    for k in range(4):
        ax = fig.add_axes([0.04 + k * 0.125, 0.12, 0.11, 0.3])
        ax.imshow(P[k], cmap=cmap, vmin=0, vmax=1)
        ax.set_xticks([]); ax.set_yticks([])
        for side in ax.spines.values():
            side.set_color(RULE)
        ax.set_title(ORIENTATIONS[k], fontproperties=F["display"], fontsize=16, color=INK, pad=6)
    ax = fig.add_axes([0.57, 0.12, 0.13, 0.3])
    _digit_axes(ax, x[image, 0])
    ax.set_title("a real 2", fontproperties=F["display"], fontsize=16, color=INK, pad=6)
    bx = fig.add_axes([0.76, 0.12, 0.21, 0.3])
    p = probs[image]
    bx.bar(range(10), p * 100, color=[PINK if d == digit else LILAC for d in range(10)], width=0.7)
    bx.set_xticks(range(10)); bx.set_ylim(0, 100)
    style_axes(bx, F, "score against each table", "")
    bx.text(digit, p[digit] * 100 + 3, f"{p[digit]:.0%}", ha="center", fontproperties=F["display"], fontsize=15,
            color=INK)
    _arrow(fig.add_axes([0.705, 0.25, 0.05, 0.05], frameon=False, xlim=(0, 1), ylim=(0, 1), xticks=[], yticks=[]),
           0.05, 0.5, 0.95, 0.5)
    fig.savefig(out / "hand-drawn-templates.png", facecolor=PAPER)
    plt.close(fig)


def fig_measured_rates(F, out, run=STORY_RUN, step=31):
    from matplotlib.patches import Rectangle
    v = submission_locals(run, step, "    # ------------------------------------------------------------------\n    # conv1, filters 0..3")
    ori = list(v["ORI_P"].items())
    zones = list(v["ZONE_P"].items())
    rates = np.array([r for _, r in ori] + [r for _, r in zones]).T  # (10 digits, 40 features)
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Rebuilt from measurements",
           f"Fable 5.2, run {run[-1]}, step {step}. How often each feature fires for each digit, measured with probes "
           "and written into its code.")
    ax = fig.add_axes([0.06, 0.14, 0.9, 0.58])
    ax.imshow(rates, cmap=LinearSegmentedColormap.from_list("p", [PAPER_2, PINK]), vmin=0, vmax=1, aspect="auto")
    ax.set_yticks(range(10)); ax.set_xticks([])
    for label in ax.get_yticklabels():
        label.set_fontproperties(F["mono"]); label.set_color(INK); label.set_fontsize(15)
    ax.tick_params(length=0)
    ax.set_ylabel("true digit", fontproperties=F["body"], fontsize=15, color=INK)
    for side in ax.spines.values():
        side.set_visible(False)
    groups = [(ORIENTATIONS[k] + " strokes", 8) for k in range(4)] + [("corners", 8)]
    start = 0
    for name, n in groups:
        ax.plot([start - 0.3, start + n - 0.7], [-0.9, -0.9], color=INK, linewidth=2, clip_on=False)
        ax.text(start + n / 2 - 0.5, -1.1, name, ha="center", va="bottom", fontproperties=F["display"], fontsize=16,
                color=INK)
        if start:
            ax.axvline(start - 0.5, color=PAPER, linewidth=4)
        start += n
    col = next(i for i, (key, _) in enumerate(ori) if key == (0, 3, 1))
    ax.add_patch(Rectangle((col - 0.5, -0.5), 1, 10, fill=False, edgecolor=INK, linewidth=3, clip_on=False))
    ax.text(col, 10.0, f"a horizontal stroke near the bottom: {rates[0, col]:.1%} of 0s, {rates[1, col]:.1%} of 1s",
            ha="left", va="top", fontproperties=F["body"], fontsize=15, color=INK)
    ax.set_ylim(9.5, -0.5)
    fig.text(0.96, 0.05, "pale: rarely fires   pink: almost always", ha="right", fontproperties=F["body"], fontsize=14,
             color=MUTED)
    fig.savefig(out / "measured-rates.png", facecolor=PAPER)
    plt.close(fig)


GO_BLACK = [(2, 2), (2, 3), (3, 2), (4, 5), (5, 4), (6, 5), (6, 2), (3, 6)]
GO_WHITE = [(5, 5), (2, 6), (3, 7), (6, 6), (7, 6), (6, 7)]


def _liberties(group, stones):
    out = set()
    for r, c in group:
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (r + dr, c + dc)
            if 0 <= q[0] < 9 and 0 <= q[1] < 9 and q not in stones:
                out.add(q)
    return out


def _board(ax, F, title):
    ax.set_facecolor("#F3E3B8")
    for i in range(9):
        ax.plot([0, 8], [i, i], color=INK, linewidth=1.2, zorder=1)
        ax.plot([i, i], [0, 8], color=INK, linewidth=1.2, zorder=1)
    ax.set_xlim(-0.7, 8.7); ax.set_ylim(8.7, -0.7); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title(title, fontproperties=F["display"], fontsize=19, color=INK, pad=10)


def _stones(ax):
    for (r, c) in GO_BLACK:
        ax.scatter([c], [r], s=1300, color=INK, zorder=3)
    for (r, c) in GO_WHITE:
        ax.scatter([c], [r], s=1300, color="white", edgecolor=INK, linewidth=2, zorder=3)


def fig_go_concepts(F, out):
    """Illustrative only: two classical Go-program ideas on a made-up 9 x 9 position."""
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Two staples of classical Go programs",
           "An illustrative position, not taken from Astra's games.")
    stones = set(GO_BLACK) | set(GO_WHITE)
    ax = fig.add_axes([0.05, 0.06, 0.42, 0.72])
    _board(ax, F, "Liberties: empty points next to a group")
    _stones(ax)
    group = [(2, 2), (2, 3), (3, 2)]
    libs = _liberties(group, stones)
    for r, c in libs:
        ax.scatter([c], [r], s=260, color=TEAL, edgecolor=INK, linewidth=1.5, zorder=4)
    (r, c), = _liberties([(5, 5)], stones)
    ax.scatter([c], [r], s=320, color=PINK, edgecolor=INK, linewidth=1.5, marker="X", zorder=4)
    ax.text(1.0, 8.25, f"black group: {len(libs)} liberties, safe", ha="left", va="center", fontproperties=F["body"],
            fontsize=14, color=INK, bbox=dict(facecolor=PAPER, edgecolor="none", pad=3))
    ax.text(8.6, 3.95, "white stone in atari:\none liberty left, so\nblack can capture here",
            ha="right", va="center", fontproperties=F["body"], fontsize=13, color=INK, zorder=5,
            bbox=dict(facecolor=PAPER, edgecolor="none", pad=3))
    bx = fig.add_axes([0.53, 0.06, 0.42, 0.72])
    _board(bx, F, "Influence: each stone radiates, fading with distance")
    rr, cc = np.mgrid[-0.5:8.5:91j, -0.5:8.5:91j]
    infl = np.zeros(rr.shape)
    for sign, group in ((1, GO_BLACK), (-1, GO_WHITE)):
        for r, c in group:
            infl += sign * 0.5 ** (np.abs(rr - r) + np.abs(cc - c))
    cmap = LinearSegmentedColormap.from_list("infl", [PINK, "#F3E3B8", TEAL])
    m = np.abs(infl).max()
    bx.imshow(infl, cmap=cmap, vmin=-m, vmax=m, extent=(-0.5, 8.5, 8.5, -0.5), zorder=0, alpha=0.85,
              interpolation="bicubic")
    bx.set_xlim(-0.7, 8.7); bx.set_ylim(8.7, -0.7)
    _stones(bx)
    fig.text(0.53, 0.035, "teal: black's area   pink: white's area", fontproperties=F["body"], fontsize=14,
             color=MUTED)
    fig.savefig(out / "go-liberties-influence.png", facecolor=PAPER)
    plt.close(fig)


# One figure per stage of run 1: what each layer holds, and which layers changed in that stage.
STAGES = [  # (stage, title, representative step, layers changed in the stage, conv2 roles by channel)
    (1, "Hand-drawn templates", 1, {"conv1", "conv2", "fc"}, ["stroke"] * 4 + ["cap"] * 4 + ["empty"] * 8),
    (2, "Unit-testing the loop detector", 5, {"conv1", "conv2", "fc"}, ["stroke"] * 4 + ["cap"] * 4 + ["loop"] * 8),
    (3, "Corners", 18, {"conv1", "conv2", "fc"}, ["stroke"] * 4 + ["cap"] * 4 + ["loop"] * 4 + ["corner"] * 4),
    (4, "Measuring every stroke", 24, {"fc"}, ["stroke"] * 4 + ["cap"] * 4 + ["loop"] * 4 + ["corner"] * 4),
    (5, "Rebuilt from measurements", 31, {"fc"}, ["stroke"] * 4 + ["cap"] * 4 + ["loop"] * 4 + ["corner"] * 4),
    (6, "Calibration", 50, {"fc"}, ["stroke"] * 4 + ["cap"] * 4 + ["loop"] * 4 + ["corner"] * 4),
]
ROLE = {"stroke": ("stroke", TEAL), "cap": ("cap", "#A9D6FF"), "loop": ("loop", YELLOW),
        "corner": ("corner", ORANGE), "empty": ("empty", PAPER_2)}


def _panel(fig, F, box, title, changed):
    from matplotlib.patches import FancyBboxPatch
    x, y, w, h = box
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.01",
                                      transform=fig.transFigure, facecolor="none", zorder=0,
                                      edgecolor=PINK if changed else RULE, linewidth=6 if changed else 2))
    fig.text(x + 0.012, y + h - 0.035, title, fontproperties=F["display"], fontsize=19, color=INK, va="top")
    fig.text(x + 0.012, y + h - 0.085, "changed in this stage" if changed else "unchanged", fontproperties=F["body"],
             fontsize=14, color=PINK if changed else MUTED, va="top")


def fig_network_stages(F, out, run=STORY_RUN):
    from matplotlib.patches import Rectangle
    cmap = LinearSegmentedColormap.from_list("signed", [PINK, PAPER_2, INK])
    for stage, title, step, changed, roles in STAGES:
        w = step_weights(run, step)
        fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
        header(fig, F, f"Stage {stage}: {title}",
               f"Fable 5.2, run 1, step {step}. Pink border: the layers it changed in this stage.")
        # conv1: the eight 5 x 5 filters
        _panel(fig, F, (0.03, 0.12, 0.25, 0.62), "conv1: 8 filters", "conv1" in changed)
        for k in range(8):
            ax = fig.add_axes([0.045 + (k % 4) * 0.058, 0.43 - (k // 4) * 0.17, 0.05, 0.089])
            f = w["conv1.weight"][k, 0]
            m = np.abs(f).max()
            ax.imshow(f if m else np.zeros((5, 5)), cmap=cmap, vmin=-(m or 1), vmax=m or 1)
            ax.set_xticks([]); ax.set_yticks([])
            for side in ax.spines.values():
                side.set_color(RULE)
            if not m:
                ax.text(2, 2, "empty", ha="center", va="center", fontproperties=F["body"], fontsize=10, color=MUTED)
        fig.text(0.155, 0.16, "lines" + ("  ·  corners" if w["conv1.weight"][4:].any() else ""),
                 ha="center", fontproperties=F["body"], fontsize=14, color=INK)
        # conv2: what its 16 channels are for
        _panel(fig, F, (0.31, 0.12, 0.2, 0.62), "conv2: 16 channels", "conv2" in changed)
        ax = fig.add_axes([0.325, 0.2, 0.17, 0.43]); ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(4, 0)
        for c, role in enumerate(roles):
            label, colour = ROLE[role]
            if role == "stroke":
                label = ["horiz.", "/", "vert.", "\\"][c]
            ax.add_patch(Rectangle((c % 4 + 0.06, c // 4 + 0.06), 0.88, 0.88, facecolor=colour, edgecolor=INK,
                                   linewidth=1.5))
            ax.text(c % 4 + 0.5, c // 4 + 0.5, label, ha="center", va="center", fontproperties=F["body"],
                    fontsize=10.5, color=MUTED if role == "empty" else INK)
        # fc: the 10 x 256 final layer, as a heatmap
        _panel(fig, F, (0.54, 0.12, 0.43, 0.62), "fc: 10 × 256 weights", "fc" in changed)
        ax = fig.add_axes([0.575, 0.25, 0.38, 0.35])
        fc = w["fc.weight"]
        m = np.percentile(np.abs(fc), 99) or 1
        ax.imshow(fc, cmap=cmap, vmin=-m, vmax=m, aspect="auto", interpolation="nearest")
        for g in range(1, 16):
            ax.axvline(g * 16 - 0.5, color=PAPER, linewidth=1.2)
        ax.set_yticks(range(10)); ax.set_xticks([])
        for label in ax.get_yticklabels():
            label.set_fontproperties(F["mono"]); label.set_fontsize(11); label.set_color(MUTED)
        ax.tick_params(length=0)
        for side in ax.spines.values():
            side.set_visible(False)
        for c, role in enumerate(roles):   # which conv2 channel each block of 16 columns reads
            ax.add_patch(Rectangle((c * 16 - 0.5, 10.0), 16, 0.6, facecolor=ROLE[role][1], edgecolor=INK,
                                   linewidth=0.8, clip_on=False))
        ax.set_ylim(10.7, -0.5)
        fig.text(0.765, 0.17, "one row per digit · each block of 16 columns reads one conv2 channel",
                 ha="center", fontproperties=F["body"], fontsize=13, color=INK2 if False else MUTED)
        fig.savefig(out / f"network-stage-{stage}.png", facecolor=PAPER)
        plt.close(fig)


PROBE_COLUMNS = ["no\nloop", "1", "2", "3", "4", "1", "2", "3", "4", "-"]


def fig_probe(F, out, run=STORY_RUN, step=4):
    m = json.loads((RESULTS / run / "steps" / f"{step:02d}" / "metrics.json").read_text())["train"]
    cm = np.array(m["confusion"], dtype=float)
    fires = 1 - cm[:, 0] / cm.sum(1)
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Turning the confusion matrix into a measurement",
           f"Fable 5.2, run {run[-1]}, step {step}. The \"predicted digit\" columns now mean how much loop it found.")
    ax = fig.add_axes([0.06, 0.1, 0.42, 0.62])
    ax.imshow(cm / cm.sum(1, keepdims=True), cmap=LinearSegmentedColormap.from_list("p", [PAPER_2, PINK]),
              vmin=0, vmax=1, aspect="auto")
    for i in range(10):
        for j in range(10):
            ax.text(j, i, f"{int(cm[i, j])}", ha="center", va="center", fontproperties=F["mono"], fontsize=9.5,
                    color=INK if cm[i, j] else MUTED)
    ax.set_xticks(range(10), PROBE_COLUMNS); ax.set_yticks(range(10))
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(F["mono"]); label.set_color(INK); label.set_fontsize(12)
    ax.set_ylabel("true digit", fontproperties=F["body"], fontsize=14, color=INK)
    ax.tick_params(length=0)
    ax.set_facecolor(PAPER)
    for side in ax.spines.values():
        side.set_visible(False)
    for x0, x1, text in [(0.6, 4.4, "loop in the upper half,\nweak to strong"),
                         (4.6, 8.4, "loop in the lower half,\nweak to strong")]:
        ax.plot([x0, x1], [10.15, 10.15], color=INK, linewidth=2, clip_on=False)
        ax.text((x0 + x1) / 2, 10.35, text, ha="center", va="top", fontproperties=F["body"], fontsize=13,
                color=INK)
    ax.set_ylim(9.5, -0.5)
    _arrow(fig.add_axes([0.49, 0.38, 0.06, 0.08], frameon=False, xlim=(0, 1), ylim=(0, 1), xticks=[], yticks=[]),
           0.05, 0.5, 0.95, 0.5)
    bx = fig.add_axes([0.6, 0.1, 0.36, 0.62])
    order = np.argsort(fires)
    bx.barh(range(10), fires[order] * 100, color=[PINK if fires[d] > 0.5 else LILAC for d in order], height=0.7)
    for k, d in enumerate(order):
        bx.text(fires[d] * 100 + 1.5, k, f"{fires[d]:.0%}", va="center", fontproperties=F["display"], fontsize=15,
                color=INK)
    bx.set_yticks(range(10), [str(d) for d in order])
    bx.set_xlim(0, 100)
    style_axes(bx, F, "how often the loop detector fires (%)", "")
    bx.tick_params(axis="y", labelsize=16, length=0)
    bx.grid(axis="y", visible=False); bx.grid(axis="x", color=RULE)
    bx.set_title("decoded: fire rate per digit", fontproperties=F["display"], fontsize=17, color=INK, pad=10)
    fig.savefig(out / "probe-trick.png", facecolor=PAPER)
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
    fig_story(F, out)
    fig_filters(F, out, STORY_RUN)
    fig_confusions(F, out, STORY_RUN, (1, 18, json.loads((RESULTS / STORY_RUN / "run.json").read_text())["best_step"]))
    fig_loop_detector(F, out)
    fig_probe(F, out)
    fig_templates(F, out)
    fig_measured_rates(F, out)
    fig_go_concepts(F, out)
    print("done")
