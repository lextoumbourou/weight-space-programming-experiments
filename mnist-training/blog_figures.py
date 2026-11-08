"""Figures for the Notes by Lex post, in the blog's style (paper, Shantell Sans labels, Atkinson numbers, highlighters).

    uv run python blog_figures.py --out ~/code/private-notes/public/notes/_media/llm-descent \
        --fonts ~/code/private-notes/public/theme/static/fonts

Everything is read from results/. The Adam filters are retrained here (seed 0, 5,000 steps, about 10 seconds).
"""
import argparse
import json
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties

RESULTS = Path(__file__).resolve().parent / "results"
PAPER, PAPER_2, INK, MUTED, RULE = "#FBFAF6", "#F2F0E8", "#141414", "#5C5B57", "#DCD9CF"
MODELS = [  # (model id, label, colour, generation)
    ("claude-opus-4-6", "Opus 4.6", "#E2C59C", "older"),
    ("claude-opus-4-8", "Opus 4.8", "#FFB866", "older"),
    ("claude-fable-5-1", "Fable 5.1", "#C4B2FF", "older"),
    ("claude-haiku-5-5", "Haiku 5.5", "#A9D6FF", "5.5"),
    ("claude-sonnet-5-5", "Sonnet 5.5", "#BDEB7A", "5.5"),
    ("claude-opus-5-5", "Opus 5.5", "#FF6FAE", "5.5"),
]
OUTLINE = [patheffects.withStroke(linewidth=5.5, foreground=INK)]


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


def runs(model, min_steps=15):
    out = []
    for run_json in sorted(RESULTS.glob("*/run.json")):
        run = json.loads(run_json.read_text())
        history = json.loads((run_json.parent / "history.json").read_text())
        if run.get("model") == model and run.get("status") == "finished" and len(history) >= min_steps \
                and "loose" not in run_json.parent.name:
            out.append(dict(name=run_json.parent.name, run=run, history=history))
    return out


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


def header(fig, F, title, subtitle):
    fig.text(0.04, 0.94, title, fontproperties=F["display"], fontsize=26, color=INK, va="top")
    fig.text(0.04, 0.865, subtitle, fontproperties=F["body"], fontsize=15, color=MUTED, va="top")


def percent_axis(ax, F):
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([f"{v:.0%}" for v in ax.get_yticks()], fontproperties=F["mono"])


def adam_level(steps):
    gd = json.loads((RESULTS / "baselines" / "gradient-descent.json").read_text())
    return float(np.mean([[c["test_accuracy"] for c in s if c["step"] == steps][0] for s in gd.values()]))


def random_search(n):
    rs = json.loads((RESULTS / "baselines" / "random-search.json").read_text())
    return np.mean([[c["test_accuracy"] for c in curve] for curve in rs.values()], axis=0)[:n]


def fig_models(F, out):
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Test accuracy after each round of feedback",
           "Mean of three runs per model (one for Opus 4.6); shading spans the lowest to highest run.")
    ax = fig.add_axes([0.07, 0.11, 0.66, 0.68])
    steps = np.arange(1, 16)
    labels = []
    for model, label, colour, _ in MODELS:
        rs = runs(model)
        if not rs:
            continue
        curves = np.array([[h["test_accuracy"] or 0 for h in r["history"][:15]] for r in rs])
        ax.fill_between(steps, curves.min(0), curves.max(0), color=colour, alpha=0.35, linewidth=0)
        ax.plot(steps, curves.mean(0), color=colour, linewidth=3.5, path_effects=OUTLINE, zorder=3)
        labels.append((curves.mean(0)[-1], f"{label}  {curves.mean(0)[-1]:.0%}"))
    for (y, text), y_label in zip(labels, spread([l[0] for l in labels], 0.04)):
        ax.text(15.35, y_label, text, fontproperties=F["display"], fontsize=16, color=INK, va="center")
    ax.plot(steps, random_search(15), color=MUTED, linestyle="--", linewidth=2)
    ax.text(15.3, random_search(15)[-1], "random search  12%", fontproperties=F["body"], fontsize=14,
            color=MUTED, va="center")
    style_axes(ax, F, "step (one reply, one round of feedback)", "test accuracy")
    percent_axis(ax, F)
    ax.set_xlim(0.7, 15.2)
    ax.set_xticks([1, 5, 10, 15])
    ax.set_xticklabels([1, 5, 10, 15], fontproperties=F["mono"])
    fig.savefig(out / "models-by-step.png", facecolor=PAPER)
    plt.close(fig)


def fig_step15(F, out):
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Accuracy after 15 steps, by model",
           "Each dot is one run. The line is the mean. Older models on the left, the 5.5 generation on the right.")
    ax = fig.add_axes([0.07, 0.16, 0.9, 0.63])
    for i, (model, label, colour, gen) in enumerate(MODELS):
        rs = runs(model)
        vals = [r["history"][14]["test_accuracy"] for r in rs]
        cost = np.mean([sum(h["cost_usd"] for h in r["history"][:15]) for r in rs])
        jitter = np.linspace(-0.1, 0.1, len(vals)) if len(vals) > 1 else [0]
        ax.plot([i - 0.28, i + 0.28], [np.mean(vals)] * 2, color=INK, linewidth=3, zorder=2)
        ax.scatter(np.array(jitter) + i, vals, s=260, color=colour, edgecolor=INK, linewidth=2, zorder=3)
        ax.text(i + 0.33, np.mean(vals), f"{np.mean(vals):.0%}", fontproperties=F["display"], fontsize=18,
                color=INK, va="center")
        ax.text(i, 0.04, f"${cost:.2f} per run", fontproperties=F["body"], fontsize=13, color=MUTED, ha="center")
    ax.axvline(2.5, color=RULE, linewidth=2)
    ax.axhline(adam_level(50), color=INK, linestyle=":", linewidth=2)
    ax.text(5.45, adam_level(50) + 0.015, f"Adam, 50 gradient steps ({adam_level(50):.0%})", fontproperties=F["body"],
            fontsize=13, color=MUTED, ha="right")
    style_axes(ax, F, "", "test accuracy at step 15")
    percent_axis(ax, F)
    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels([m[1] for m in MODELS], fontproperties=F["display"], fontsize=17, color=INK)
    ax.set_xlim(-0.6, len(MODELS) - 0.4)
    fig.savefig(out / "step-15-by-model.png", facecolor=PAPER)
    plt.close(fig)


def fig_opus_until_flat(F, out):
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Opus 5.5, kept going until it flattened",
           "Three runs. After step 15 each was told it had more steps, and that a 5-step plateau would end the run.")
    ax = fig.add_axes([0.07, 0.11, 0.8, 0.68])
    colours = ["#FF6FAE", "#2DD4BF", "#FFB866"]
    last, ends = 0, []
    for i, colour in zip((1, 2, 3), colours):
        h = json.loads((RESULTS / f"opus-high-strict-{i}" / "history.json").read_text())
        x = [s["step"] for s in h]
        ax.plot(x, [s["test_accuracy"] or 0 for s in h], color=colour, linewidth=3.5, path_effects=OUTLINE,
                marker="o", markersize=6, markeredgecolor=INK)
        ends.append((h[-1]["test_accuracy"], f"run {i}: {h[-1]['test_accuracy']:.0%} at step {x[-1]}", colour))
        last = max(last, x[-1])
    for (y, text, colour), y_label in zip(ends, spread([e[0] for e in ends], 0.045)):
        ax.plot([last + 0.9], [y_label], marker="o", markersize=12, color=colour, markeredgecolor=INK,
                markeredgewidth=2, clip_on=False)
        ax.text(last + 1.5, y_label, text, fontproperties=F["display"], fontsize=16, color=INK, va="center")
    ax.axvline(15.5, color=MUTED, linestyle="--", linewidth=2)
    ax.text(15.7, 0.05, "budget extended", fontproperties=F["body"], fontsize=14, color=MUTED)
    ax.plot(range(1, last + 1), random_search(last), color=MUTED, linestyle=":", linewidth=2)
    ax.text(last + 0.8, random_search(last)[-1], "random search", fontproperties=F["body"], fontsize=14,
            color=MUTED, va="center")
    ax.axhline(adam_level(50), color=INK, linestyle=":", linewidth=2)
    ax.text(1, adam_level(50) + 0.015, f"Adam, 50 gradient steps ({adam_level(50):.0%})", fontproperties=F["body"],
            fontsize=13, color=MUTED)
    style_axes(ax, F, "step", "test accuracy")
    percent_axis(ax, F)
    ax.set_xlim(0.5, last + 7.5)
    fig.savefig(out / "opus-until-flat.png", facecolor=PAPER)
    plt.close(fig)


def fig_confusions(F, out, run="opus-high-strict-1", steps=(1, 9, 26)):
    cmap = LinearSegmentedColormap.from_list("pink", [PAPER_2, "#FF6FAE"])
    fig = plt.figure(figsize=(16, 7.2), dpi=120, facecolor=PAPER)
    header(fig, F, "What the model sees: the training confusion matrix",
           f"Opus 5.5, {run.split('-')[-1] and 'run ' + run.split('-')[-1]}. Rows are the true digit, columns the predicted digit; darker means more images.")
    for k, step in enumerate(steps):
        m = json.loads((RESULTS / run / "steps" / f"{step:02d}" / "metrics.json").read_text())["val"]
        cm = np.array(m["confusion"], dtype=float)
        ax = fig.add_axes([0.06 + k * 0.31, 0.08, 0.26, 0.62])
        ax.imshow(cm / cm.sum(1, keepdims=True), cmap=cmap, vmin=0, vmax=1)
        ax.set_title(f"step {step}: {m['accuracy']:.0%} training accuracy", fontproperties=F["display"], fontsize=17, color=INK, pad=10)
        ax.set_xticks(range(10))
        ax.set_yticks(range(10))
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(F["mono"])
            label.set_color(MUTED)
        ax.set_xlabel("predicted", fontproperties=F["body"], fontsize=13, color=INK)
        if k == 0:
            ax.set_ylabel("true", fontproperties=F["body"], fontsize=13, color=INK)
        for side in ax.spines.values():
            side.set_visible(False)
    fig.savefig(out / "confusion-over-steps.png", facecolor=PAPER)
    plt.close(fig)


def adam_filters():
    import data
    from baselines import train_weights
    return train_weights(data.load(), seed=0, steps=5_000)["conv1.weight"]


def fig_filters(F, out, run="opus-high-strict-1"):
    hist = json.loads((RESULTS / run / "history.json").read_text())
    written = np.load(RESULTS / run / "steps" / f"{hist[-1]['step']:02d}" / "weights.npz")["conv1.weight"]
    learned = adam_filters()
    cmap = LinearSegmentedColormap.from_list("signed", ["#FF6FAE", PAPER_2, "#2DD4BF"])
    fig = plt.figure(figsize=(16, 6.4), dpi=120, facecolor=PAPER)
    header(fig, F, "The first layer: written by Opus 5.5, and learned by Adam",
           "Eight 5 × 5 filters each. Teal is positive, pink negative; each filter has its own scale.")
    for row, (name, w) in enumerate([("Opus 5.5 (written)", written), ("Adam (learned)", learned)]):
        fig.text(0.04, 0.6 - row * 0.36, name, fontproperties=F["display"], fontsize=18, color=INK, va="center")
        for c in range(8):
            ax = fig.add_axes([0.27 + c * 0.088, 0.46 - row * 0.36, 0.075, 0.28])
            m = np.abs(w[c, 0]).max() or 1
            ax.imshow(w[c, 0], cmap=cmap, vmin=-m, vmax=m)
            ax.set_xticks([])
            ax.set_yticks([])
            for side in ax.spines.values():
                side.set_color(RULE)
    fig.savefig(out / "filters-written-vs-learned.png", facecolor=PAPER)
    plt.close(fig)


def fig_loose(F, out):
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Without the no-fitting rule",
           "Opus 5.5. The loose run fitted a classifier to synthetic digits it generated itself, from step 4.")
    ax = fig.add_axes([0.07, 0.11, 0.78, 0.68])
    for name, label, colour in [("opus-high-loose-rules-stopped", "fitting allowed", "#FFB866"),
                                ("opus-high-strict-1", "fitting forbidden", "#FF6FAE")]:
        h = json.loads((RESULTS / name / "history.json").read_text())[:15]
        ax.plot([s["step"] for s in h], [s["test_accuracy"] or 0 for s in h], color=colour, linewidth=3.5,
                path_effects=OUTLINE, marker="o", markersize=6, markeredgecolor=INK)
        ax.text(h[-1]["step"] + 0.3, h[-1]["test_accuracy"], label, fontproperties=F["display"], fontsize=16,
                color=INK, va="center")
    style_axes(ax, F, "step", "test accuracy")
    percent_axis(ax, F)
    ax.set_xlim(0.5, 17.5)
    fig.savefig(out / "loose-vs-strict.png", facecolor=PAPER)
    plt.close(fig)


def fig_loss_runs(F, out, prefix="opus-p8-", name="Opus 5.5"):
    """Best training loss so far (the descent; the 10,000 images Claude gets feedback on, called val in the code), with each step's loss and the probe steps marked."""
    paths = sorted(RESULTS.glob(f"{prefix}*/history.json"))
    if not paths:
        return
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, f"{name}: the descent",
           "Line: best training loss so far. Dots: each step's loss. Ticks at the top: probe steps, "
           "where the network measured its own features instead of classifying.")
    ax = fig.add_axes([0.07, 0.11, 0.7, 0.66])
    colours = ["#FF6FAE", "#2DD4BF", "#FFB866", "#C4B2FF", "#A9D6FF"]
    ceiling, ends, last = 2.6, [], 0
    for k, (path, colour) in enumerate(zip(paths, colours)):
        h = [s for s in json.loads(path.read_text()) if s["ok"]]
        x = np.array([s["step"] for s in h])
        loss = np.array([s["val_loss"] for s in h])
        probe = np.array([s["val_loss"] > 10 for s in h])  # see is_probe
        best = np.minimum.accumulate(loss)
        ax.scatter(x[~probe], np.minimum(loss[~probe], ceiling), s=40, color=colour, edgecolor=INK, linewidth=1,
                   alpha=0.6, zorder=2)
        ax.scatter(x[probe], [ceiling - 0.06 - 0.08 * k] * probe.sum(), marker="|", s=260, color=colour,
                   linewidth=3, zorder=2)
        ax.step(x, best, where="post", color=colour, linewidth=3.5, path_effects=OUTLINE, zorder=3)
        run = json.loads((path.parent / "run.json").read_text())
        acc = run.get("best_val_loss_test_accuracy") or h[int(np.argmin(loss))]["test_accuracy"]
        ends.append((best[-1], f"run {path.parent.name.split('-')[-1]}: {best[-1]:.2f} ({acc:.0%} test)", colour))
        last = max(last, x[-1])
    for (y, text, colour), y_label in zip(ends, spread([e[0] for e in ends], 0.12)):
        ax.plot([last + 1.2], [y_label], marker="o", markersize=12, color=colour, markeredgecolor=INK,
                markeredgewidth=2, clip_on=False)
        ax.text(last + 2.2, y_label, text, fontproperties=F["display"], fontsize=16, color=INK, va="center")
    style_axes(ax, F, "step (one reply, one round of feedback)", "training loss (cross-entropy)")
    ax.set_xlim(0.5, last + 0.8)
    ax.set_ylim(0, ceiling)
    fig.savefig(out / "loss-by-step.png", facecolor=PAPER)
    plt.close(fig)


# ---------------------------------------------------------------- LLM Descent post (final runs)
STORY_RUN = "opus-p8-3"


def is_probe(step):
    """Probe steps are deliberately not classifiers. Every step Claude described as a probe has training loss
    above 10 (19.8 to 2,042); every genuine classifier stays below 2.4."""
    return step["val_loss"] > 10
PHASES = [(1, 13, "hand-drawn templates", "#A9D6FF"), (14, 20, "first probes", "#FFE84D"),
          (21, 42, "naive Bayes from measured features", "#BDEB7A"), (43, 50, "calibration", "#E2C59C")]


def story_history(run=STORY_RUN):
    return json.loads((RESULTS / run / "history.json").read_text())


def fig_cover(F, out):
    """The first, MNIST-only LinkedIn card (the post now uses post_figures.py's cover.png)."""
    h = [s for s in story_history() if s["ok"]]
    x = np.array([s["step"] for s in h]); loss = np.array([s["val_loss"] for s in h])
    probe = np.array([is_probe(s) for s in h])
    fig = plt.figure(figsize=(20, 10.47), dpi=120, facecolor=PAPER)
    fig.text(0.05, 0.80, "LLM Descent", fontproperties=F["display"], fontsize=96, color=INK, va="top")
    fig.text(0.05, 0.56, "Claude trained a neural network\nto 86% on MNIST\nwithout a single gradient.",
             fontproperties=F["body"], fontsize=34, color=INK, va="top", linespacing=1.35)
    fig.text(0.05, 0.12, "notesbylex.com", fontproperties=F["display"], fontsize=24, color=MUTED)
    ax = fig.add_axes([0.53, 0.14, 0.43, 0.7])
    ax.set_facecolor(PAPER)
    best = np.minimum.accumulate(loss)
    ax.step(x, best, where="post", color="#FF6FAE", linewidth=7, path_effects=[patheffects.withStroke(
        linewidth=11, foreground=INK)], zorder=3)
    ax.scatter(x[probe], [2.05] * probe.sum(), marker="|", s=900, color=INK, linewidth=4)
    ax.text(x[probe][0] - 0.5, 2.25, "probes", fontproperties=F["display"], fontsize=26, color=INK)
    ax.text(x[0], best[0] + 0.12, f"{h[0]['test_accuracy']:.0%}", fontproperties=F["display"], fontsize=30,
            color=INK, ha="left")
    ax.text(x[-1], best[-1] + 0.12, f"{h[-1]['test_accuracy']:.0%}", fontproperties=F["display"], fontsize=30,
            color=INK, ha="right")
    ax.set_ylim(0, 2.4); ax.set_xlim(0, 51)
    ax.set_xticks([]); ax.set_yticks([])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK); ax.spines[side].set_linewidth(3)
    ax.set_xlabel("50 steps of feedback", fontproperties=F["display"], fontsize=24, color=INK)
    ax.set_ylabel("training loss", fontproperties=F["display"], fontsize=24, color=INK)
    fig.savefig(out / "cover-mnist.png", facecolor=PAPER)
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
    _block(ax, F, 3.3, 5.6, 4.6, 1.9, "Claude writes\nbuild_weights()", "#FF6FAE", 1.5)
    _block(ax, F, 8.3, 7.0, 4.2, 1.6, "sandbox sets all\n5,994 weights", "#FFE84D", -1.2)
    _block(ax, F, 12.6, 5.6, 4.4, 1.9, "10,000 training\nimages", "#2DD4BF", 1.0)
    _block(ax, F, 8.0, 3.0, 5.2, 1.7, "loss, accuracy,\nconfusion matrix", "#C4B2FF", -1.5)
    _block(ax, F, 12.9, 1.5, 4.0, 1.4, "test set:\nnever shown", "#F2F0E8", 1.2, size=24)
    _arrow(ax, 5.0, 6.5, 6.3, 6.95)
    _arrow(ax, 10.4, 6.9, 11.2, 6.4)
    _arrow(ax, 11.6, 4.6, 10.4, 3.5)
    _arrow(ax, 5.4, 3.0, 3.6, 4.5)
    ax.text(3.0, 3.0, "next step", fontproperties=F["display"], fontsize=22, color=MUTED, ha="center")
    ax.text(0.6, 8.4, "One step of LLM Descent", fontproperties=F["display"], fontsize=26, color=INK)
    fig.savefig(out / "loop.png", facecolor=PAPER)
    plt.close(fig)


def fig_run3_story(F, out):
    h = story_history()
    x = np.array([s["step"] for s in h]); acc = np.array([s["test_accuracy"] for s in h])
    probe = np.array([is_probe(s) for s in h])
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Fifty steps, four strategies",
           "Opus 5.5, run 3. Test accuracy of every classifier it wrote; probe steps marked along the bottom.")
    ax = fig.add_axes([0.07, 0.11, 0.9, 0.62])
    for a, b, label, colour in PHASES:
        ax.axvspan(a - 0.5, b + 0.5, color=colour, alpha=0.35, linewidth=0)
        ax.text((a + b) / 2, 1.02, label, fontproperties=F["display"], fontsize=15, color=INK, ha="center",
                va="bottom", transform=ax.get_xaxis_transform())
    ax.plot(x[~probe], acc[~probe], color="#FF6FAE", linewidth=3.5, path_effects=OUTLINE, marker="o",
            markersize=6, markeredgecolor=INK, zorder=3)
    ax.scatter(x[probe], [0.03] * probe.sum(), marker="|", s=300, color=INK, linewidth=3, zorder=3)
    arrow = dict(arrowstyle="-|>", color=INK, linewidth=1.8, shrinkA=4, shrinkB=6)
    ax.annotate("stuck at about 67%", xy=(13, acc[12]), xytext=(4.5, 0.80), fontproperties=F["display"],
                fontsize=15, color=INK, arrowprops=arrow)
    ax.annotate("\"I have no direct view of the features,\nso this step spends one evaluation\non measuring them.\"",
                xy=(14, 0.03), xytext=(1.5, 0.2), fontproperties=F["display"], fontsize=14, color=INK,
                arrowprops=arrow)
    i21 = list(x).index(21)
    ax.annotate("naive Bayes on\nmeasured features", xy=(21, acc[i21]), xytext=(23.5, 0.56),
                fontproperties=F["display"], fontsize=15, color=INK, arrowprops=arrow)
    ax.annotate(f"{acc[-1]:.0%}", xy=(50, acc[-1]), xytext=(47.2, 0.72), fontproperties=F["display"],
                fontsize=22, color=INK, arrowprops=arrow)
    ax.axhline(adam_level(50), color=INK, linestyle=":", linewidth=2)
    ax.text(1, adam_level(50) + 0.015, f"Adam, 50 gradient steps ({adam_level(50):.0%})", fontproperties=F["body"],
            fontsize=13, color=MUTED)
    style_axes(ax, F, "step", "test accuracy")
    percent_axis(ax, F)
    ax.set_xlim(0.5, 50.5)
    fig.savefig(out / "run-3-story.png", facecolor=PAPER)
    plt.close(fig)


def fig_probe(F, out, step=22):
    m = json.loads((RESULTS / STORY_RUN / "steps" / f"{step:02d}" / "metrics.json").read_text())["val"]
    cm = np.array(m["confusion"], dtype=float)[:, :8]
    rows = cm / cm.sum(1, keepdims=True)
    names = ["top bar", "bottom bar", "upper-left\nvertical"]
    decoded = np.array([[rows[d, [k for k in range(8) if k >> bit & 1]].sum() for bit in range(3)]
                        for d in range(10)])
    cmap = LinearSegmentedColormap.from_list("yellow", [PAPER_2, "#FFE84D"])
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "A probe: using the confusion matrix as a measuring instrument",
           f"Step {step}. Output = top bar + 2 × bottom bar + 4 × upper-left vertical, so each digit's row is a "
           "histogram of three features.")
    ax = fig.add_axes([0.07, 0.12, 0.48, 0.6])
    ax.imshow(rows, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    codes = ["none", "T", "B", "T+B", "V", "T+V", "B+V", "all"]
    ax.set_xticks(range(8)); ax.set_xticklabels(codes, fontproperties=F["mono"], fontsize=12, color=MUTED)
    ax.set_yticks(range(10)); ax.set_yticklabels(range(10), fontproperties=F["mono"], fontsize=12, color=MUTED)
    ax.set_xlabel("output the probe network chose", fontproperties=F["body"], fontsize=14, color=INK)
    ax.set_ylabel("true digit", fontproperties=F["body"], fontsize=14, color=INK)
    ax.set_title("what came back", fontproperties=F["display"], fontsize=18, color=INK, pad=10)
    for side in ax.spines.values():
        side.set_visible(False)
    ax2 = fig.add_axes([0.66, 0.12, 0.3, 0.6])
    ax2.imshow(decoded, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    for d in range(10):
        for b in range(3):
            ax2.text(b, d, f"{decoded[d, b]:.0%}", fontproperties=F["mono"], fontsize=13, color=INK,
                     ha="center", va="center")
    ax2.set_xticks(range(3)); ax2.set_xticklabels(names, fontproperties=F["body"], fontsize=12, color=INK)
    ax2.set_yticks(range(10)); ax2.set_yticklabels(range(10), fontproperties=F["mono"], fontsize=12, color=MUTED)
    ax2.set_title("what it learned", fontproperties=F["display"], fontsize=18, color=INK, pad=10)
    for side in ax2.spines.values():
        side.set_visible(False)
    fig.patches.append(plt.matplotlib.patches.FancyArrowPatch((0.565, 0.42), (0.625, 0.42), transform=fig.transFigure,
                       arrowstyle="-|>,head_length=12,head_width=8", color=INK, linewidth=5))
    fig.text(0.595, 0.47, "decode", fontproperties=F["display"], fontsize=16, color=INK, ha="center")
    fig.savefig(out / "probe.png", facecolor=PAPER)
    plt.close(fig)


def fig_final_scores(F, out):
    rs = json.loads((RESULTS / "baselines" / "random-search.json").read_text())
    loose = json.loads((RESULTS / "opus-high-loose-rules-stopped" / "history.json").read_text())
    entries = [("random search\n(50 evaluations)", np.mean([c[-1]["test_accuracy"] for c in rs.values()]), MUTED)]
    for i in (1, 2, 3):
        r = json.loads((RESULTS / f"opus-p8-{i}" / "run.json").read_text())
        entries.append((f"Opus 5.5\nrun {i}", r["best_val_loss_test_accuracy"], "#FF6FAE"))
    entries += [("Opus 5.5, fitting\nallowed (14 steps)", loose[-1]["test_accuracy"], "#FFB866"),
                ("Adam\n50 steps", adam_level(50), "#2DD4BF"), ("Adam\n5,000 steps", adam_level(5000), "#2DD4BF")]
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Where it landed",
           "Test accuracy on 10,000 MNIST images. Opus runs are scored on their lowest-training-loss network.")
    ax = fig.add_axes([0.07, 0.16, 0.9, 0.6])
    for i, (label, v, colour) in enumerate(entries):
        ax.bar(i, v, width=0.62, color=colour, edgecolor=INK, linewidth=2)
        ax.text(i, v + 0.02, f"{v:.0%}", fontproperties=F["display"], fontsize=20, color=INK, ha="center")
    style_axes(ax, F, "", "test accuracy")
    percent_axis(ax, F)
    ax.set_xticks(range(len(entries)))
    ax.set_xticklabels([e[0] for e in entries], fontproperties=F["display"], fontsize=14, color=INK)
    fig.savefig(out / "final-scores.png", facecolor=PAPER)
    plt.close(fig)


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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--fonts", default="~/code/private-notes/public/theme/static/fonts")
    args = ap.parse_args()
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    F = fonts(args.fonts)
    fig_cover(F, out)
    fig_mnist(F, out)
    fig_loop(F, out)
    fig_loss_runs(F, out)
    fig_run3_story(F, out)
    fig_probe(F, out)
    fig_final_scores(F, out)
    fig_confusions(F, out, run=STORY_RUN, steps=(1, 13, 50))
    fig_filters(F, out, run=STORY_RUN)
    print(sorted(p.name for p in out.glob("*.png")))
