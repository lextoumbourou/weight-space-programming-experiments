"""Figures for the LLM Descent post that span all the experiments (MNIST, Titanic, synthetic tabular data).

The MNIST-only figures are made by mnist-training/blog_figures.py; this script reuses its style.

    cd mnist-training && uv run python ../post_figures.py --out ~/code/private-notes/public/notes/_media/llm-descent

Step labels (write / measure / build / tune) are hand labels in step-labels.json.
"""
import argparse
import importlib
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "mnist-training"))
import blog_figures as bf  # noqa: E402
from blog_figures import INK, MUTED, PAPER, PAPER_2, RULE, header, style_axes  # noqa: E402

PINK, YELLOW, GREEN, BLUE, TAN, TEAL = "#FF6FAE", "#FFE84D", "#BDEB7A", "#A9D6FF", "#E2C59C", "#2DD4BF"
ACTIONS = [("write", "write from what it knows", BLUE), ("measure", "measure (probe or test)", YELLOW),
           ("build", "build from measurements", GREEN), ("tune", "tune", TAN)]
COLOUR = {a: c for a, _, c in ACTIONS}
LABELS = json.loads((ROOT / "step-labels.json").read_text())


def project(folder):
    """Import a sub-project's data and network modules without name clashes (each folder has its own)."""
    for name in ("data", "network"):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(ROOT / folder))
    try:
        data = importlib.import_module("data")
        network = importlib.import_module("network")
    finally:
        sys.path.pop(0)
        for name in ("data", "network"):
            sys.modules.pop(name, None)
    return data, network


def results(folder, run):
    d = ROOT / folder / "results" / run
    return json.loads((d / "run.json").read_text()), json.loads((d / "history.json").read_text())


def weights(folder, run, step):
    return dict(np.load(ROOT / folder / "results" / run / "steps" / f"{step:02d}" / "weights.npz"))


def logit(w, x):
    h = np.maximum(x @ w["fc1.weight"].T + w["fc1.bias"], 0)
    out = h @ w["fc2.weight"].T + w["fc2.bias"]
    return out[:, 1] - out[:, 0]


def scored_step(folder, run):
    return results(folder, run)[0]["best_val_loss_step"]


# ------------------------------------------------------------------ step strips
STRIP_GROUPS = [
    ("Titanic", "it knows the answer", "titanic-training", ["opus-p8-1", "opus-p8-2", "opus-p8-3"]),
    ("Titanic, anonymised", "it recognises the data", "titanic-training", ["anon-p8-1", "anon-p8-2", "anon-p8-3"]),
    ("Synthetic data", "nothing to know", "synthetic-training", ["opus-p8-1", "opus-p8-2", "opus-p8-3"]),
    ("MNIST", "knows the domain, can't write it", "mnist-training", ["opus-p8-1", "opus-p8-2", "opus-p8-3"]),
]


def draw_strip(ax, labels, y, height=0.78, best=None, gap=0.08):
    for i, a in enumerate(labels):
        ax.add_patch(Rectangle((i + 0.5 + gap / 2, y - height / 2), 1 - gap, height, color=COLOUR[a], linewidth=0))
    if best:
        ax.add_patch(Rectangle((best - 0.5 + gap / 2, y - height / 2), 1 - gap, height, fill=False, edgecolor=INK,
                               linewidth=2.6))


def legend(fig, F, y, x0=0.04, size=15, char=0.0098):
    x = x0
    for _, text, colour in ACTIONS:
        fig.patches.append(Rectangle((x, y - 0.012), 0.016, 0.028, color=colour, transform=fig.transFigure))
        fig.text(x + 0.022, y, text, fontproperties=F["body"], fontsize=size, color=INK, va="center")
        x += 0.034 + char * len(text)


def fig_step_strips(F, out):
    fig = plt.figure(figsize=(16, 10.5), dpi=120, facecolor=PAPER)
    header(fig, F, "What Claude did at each step",
           "Twelve runs of Opus 5.5, one row each, one tile per step. The outlined tile is the network that was scored.")
    legend(fig, F, 0.79)
    ax = fig.add_axes([0.22, 0.08, 0.75, 0.66])
    ax.set_xlim(0.4, 50.6)
    ax.set_ylim(-(sum(len(g[3]) for g in STRIP_GROUPS) + 0.7 * (len(STRIP_GROUPS) - 1)) + 0.4, 0.6)
    y = 0
    yticks, ylabels = [], []
    for title, sub, folder, runs in STRIP_GROUPS:
        for i, run in enumerate(runs):
            draw_strip(ax, LABELS[f"{folder}/{run}"], y, best=scored_step(folder, run))
            yticks.append(y); ylabels.append(f"run {i + 1}")
            y -= 1
        y -= 0.7
    y = 0
    for title, sub, folder, runs in STRIP_GROUPS:
        mid = y - (len(runs) - 1) / 2
        fy = ax.transData.transform((0, mid))[1] / fig.bbox.height
        fig.text(0.015, fy + 0.014, title, fontproperties=F["display"], fontsize=17, color=INK, va="center")
        fig.text(0.015, fy - 0.018, sub, fontproperties=F["body"], fontsize=13, color=MUTED, va="center")
        y -= len(runs) + 0.7
    ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontproperties=F["mono"], fontsize=12, color=MUTED)
    ax.set_xticks([1, 10, 20, 30, 40, 50])
    ax.set_xticklabels([1, 10, 20, 30, 40, 50], fontproperties=F["mono"], fontsize=13, color=MUTED)
    ax.set_xlabel("step", fontproperties=F["body"], fontsize=15, color=INK)
    ax.set_facecolor(PAPER)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(length=0, axis="y")
    fig.savefig(out / "step-strips.png", facecolor=PAPER)
    plt.close(fig)


def fig_cover(F, out):
    """LinkedIn / og:image card, 1.91:1."""
    fig = plt.figure(figsize=(20, 10.47), dpi=120, facecolor=PAPER)
    fig.text(0.05, 0.86, "LLM Descent", fontproperties=F["display"], fontsize=92, color=INK, va="top")
    fig.text(0.05, 0.64, "Claude trains neural networks by writing every weight.\n"
             "What it does depends on what it already knows.",
             fontproperties=F["body"], fontsize=30, color=INK, va="top", linespacing=1.4)
    rows = [("Titanic", "titanic-training", "opus-p8-2"), ("synthetic data", "synthetic-training", "opus-p8-1"),
            ("MNIST", "mnist-training", "opus-p8-3")]
    ax = fig.add_axes([0.22, 0.13, 0.74, 0.33])
    ax.set_xlim(0.4, 50.6); ax.set_ylim(-2.6, 0.6); ax.axis("off")
    for i, (name, folder, run) in enumerate(rows):
        draw_strip(ax, LABELS[f"{folder}/{run}"], -i, height=0.74)
        fy = ax.transData.transform((0, -i))[1] / fig.bbox.height
        fig.text(0.05, fy, name, fontproperties=F["display"], fontsize=28, color=INK, va="center")
    legend(fig, F, 0.07, x0=0.22, size=20, char=0.0068)
    fig.text(0.95, 0.94, "notesbylex.com", fontproperties=F["display"], fontsize=22, color=MUTED, ha="right",
             va="top")
    fig.savefig(out / "cover.png", facecolor=PAPER)
    plt.close(fig)


# ------------------------------------------------------------------ Titanic: three runs, one answer
def fig_titanic_step1(F, out):
    data, _ = project("titanic-training")
    x, _ = data.load()["val"]

    def onehot(cols, on):
        def set_(z):
            z[:, cols] = 0
            if on is not None:
                z[:, on] = 1
        return set_

    def shift(col, d):
        def set_(z):
            known = z[:, 5] > 0.5 if col == 4 else slice(None)
            z[known, col] += d
        return set_
    contrasts = [  # label, change to "hi", change to "lo"
        ("female (vs male)", onehot([3], 3), onehot([3], None)),
        ("2nd class (vs 1st)", onehot([0, 1, 2], 1), onehot([0, 1, 2], 0)),
        ("3rd class (vs 1st)", onehot([0, 1, 2], 2), onehot([0, 1, 2], 0)),
        ("10 years older", shift(4, 0.5), shift(4, -0.5)),
        ("one more sibling or spouse", shift(6, 0.5), shift(6, -0.5)),
        ("one more parent or child", shift(7, 0.5), shift(7, -0.5)),
        ("fare 2.7 times higher", shift(8, 0.5), shift(8, -0.5)),
        ("cabin recorded (vs not)", onehot([12], 12), onehot([12], None)),
        ("Cherbourg (vs Southampton)", onehot([9, 10, 11], 9), onehot([9, 10, 11], 11)),
        ("Queenstown (vs Southampton)", onehot([9, 10, 11], 10), onehot([9, 10, 11], 11)),
    ]
    effects = []
    for run in ("opus-p8-1", "opus-p8-2", "opus-p8-3"):
        w = weights("titanic-training", run, 1)
        row = []
        for _, hi_set, lo_set in contrasts:
            hi, lo = x.copy(), x.copy()
            hi_set(hi); lo_set(lo)
            row.append(float(np.mean(logit(w, hi) - logit(w, lo))))
        effects.append(row)
    effects = np.array(effects)
    n = len(contrasts)
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "Step 1, three times: the same network from memory",
           "How much each change moves the survival log-odds in each run's first network, averaged over passengers.")
    ax = fig.add_axes([0.25, 0.1, 0.71, 0.68])
    shades = ["#FF6FAE", "#FF9CC8", "#FFC9E0"]
    for k in range(3):
        ax.barh(np.arange(n) + (k - 1) * 0.26, effects[k], height=0.26, color=shades[k], edgecolor=INK,
                linewidth=1.2, label=f"run {k + 1}")
    ax.axvline(0, color=INK, linewidth=1.5)
    style_axes(ax, F, "effect on the survival log-odds", "")
    ax.set_yticks(range(n)); ax.set_yticklabels([c[0] for c in contrasts], fontproperties=F["body"], fontsize=15,
                                                color=INK)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False); ax.grid(axis="x", color=RULE)
    leg = ax.legend(loc="lower right", frameon=False, prop=F["body"])
    for t in leg.get_texts():
        t.set_fontsize(15)
    fig.savefig(out / "titanic-step-1.png", facecolor=PAPER)
    plt.close(fig)


# ------------------------------------------------------------------ synthetic: what it found vs the truth
SYN_NAMES = {"member": "member (yes/no)", "tier": "tier (0, 1, 2)", "years": "years as customer", "visits": "visits",
             "spend": "spend", "flag": "flag (yes/no)", "spend_proxy": "spend proxy", "distance": "distance",
             "noise_bin": "noise (yes/no)", "noise_a": "noise", "noise_b": "noise", "weekend": "weekend (yes/no)"}


def synthetic_setup():
    data, _ = project("synthetic-training")
    rng = np.random.default_rng(data.SEED)
    raw = data.generate(data.N_VAL + data.N_TEST, rng)[: data.N_VAL]
    z = raw[:, data.PERMUTATION]
    mean, std = z.mean(0), z.std(0)
    return data, raw, (z - mean) / std, mean, std


def fig_synthetic_recovered(F, out):
    data, raw, z, mean, std = synthetic_setup()
    perm = data.PERMUTATION
    runs = {r: weights("synthetic-training", r, scored_step("synthetic-training", r))
            for r in ("opus-p8-1", "opus-p8-2", "opus-p8-3")}

    def curves(j, grid):
        d = perm[j]
        true, nets = [], {r: [] for r in runs}
        for g in grid:
            rr = raw.copy(); rr[:, d] = g * std[j] + mean[j]
            true.append(data.true_logit(rr).mean())
            zz = z.copy(); zz[:, j] = g
            for r, w in runs.items():
                nets[r].append(logit(w, zz.astype(np.float32)).mean())
        centre = lambda c: np.array(c) - np.mean(c)
        return centre(true), {r: centre(c) for r, c in nets.items()}

    order = sorted(range(12), key=lambda j: list(SYN_NAMES).index(data.DESIGN[perm[j]][0]))
    fig = plt.figure(figsize=(16, 11), dpi=120, facecolor=PAPER)
    header(fig, F, "What it found, against the hidden truth",
           "How each feature moves the log-odds (x axis: the feature in standard deviations). Ink: the true model. "
           "Pink: Claude's networks, run 1 thick.")
    for k, j in enumerate(order + [None]):
        ax = fig.add_axes([0.04 + (k % 5) * 0.193, 0.6 - (k // 5) * 0.255, 0.165, 0.18])
        ax.set_facecolor(PAPER)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(MUTED)
        ax.tick_params(labelsize=9, colors=MUTED)
        if j is None:  # the interaction panel
            m, f = order[0], order[5]
            mv, fv = np.unique(z[:, m]), np.unique(z[:, f])
            md, fd = perm[m], perm[f]

            def contrast(fn):
                vals = {}
                for a in (0, 1):
                    for b in (0, 1):
                        vals[a, b] = fn(a, b)
                return vals[1, 1] - vals[1, 0] - vals[0, 1] + vals[0, 0]

            def true_at(a, b):
                rr = raw.copy(); rr[:, md] = a; rr[:, fd] = b
                return data.true_logit(rr).mean()

            def net_at(w):
                def fn(a, b):
                    zz = z.copy(); zz[:, m] = mv[a]; zz[:, f] = fv[b]
                    return logit(w, zz.astype(np.float32)).mean()
                return fn
            vals = [contrast(true_at)] + [contrast(net_at(w)) for w in runs.values()]
            ax.bar(range(4), vals, color=[INK, PINK, "#FF9CC8", "#FF9CC8"], edgecolor=INK)
            ax.set_xticks(range(4)); ax.set_xticklabels(["truth", "run 1", "run 2", "run 3"], fontsize=10,
                                                        fontproperties=F["body"])
            ax.axhline(0, color=MUTED, linewidth=1)
            ax.set_title("member × flag", fontproperties=F["display"], fontsize=14, color=INK, loc="left")
            continue
        name = data.DESIGN[perm[j]][0]
        u = np.unique(z[:, j])
        grid = u if len(u) <= 3 else np.linspace(np.percentile(z[:, j], 2), np.percentile(z[:, j], 98), 25)
        true, nets = curves(j, grid)
        style = dict(marker="o", markersize=5) if len(u) <= 3 else {}
        for r, c in nets.items():
            ax.plot(grid, c, color=PINK, linewidth=4 if r == "opus-p8-1" else 1.6, alpha=1 if r == "opus-p8-1" else
                    0.7, **style)
        ax.plot(grid, true, color=INK, linewidth=2.2, **style)
        ax.set_title(f"x{j}: {SYN_NAMES[name]}", fontproperties=F["display"], fontsize=13, color=INK, loc="left")
        ax.set_ylim(-3.2, 3.2)
    fig.savefig(out / "synthetic-recovered.png", facecolor=PAPER)
    plt.close(fig)


# ------------------------------------------------------------------ synthetic: the interaction hunt
def fig_interaction_hunt(F, out):
    hist = {h["step"]: h["val_loss"] for h in results("synthetic-training", "opus-p8-1")[1]}
    fig = plt.figure(figsize=(16, 10), dpi=120, facecolor=PAPER)
    header(fig, F, "Hunting for an interaction, by halving",
           "Synthetic data, run 1. Each step tests x7 against a group of features at once; the loss says which half "
           "to keep.")
    ax = fig.add_axes([0, 0, 1, 0.8]); ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis("off")
    rows = [  # step, kept group, dropped group, prediction, colour
        (29, "x7 × all 11 others", None, "no interaction: about 0.489", YELLOW),
        (30, "x7 × {x0, x2, x3, x4, x5}", "{x6, x8, x10, x11}", "if it's in here: about 0.477", YELLOW),
        (31, "x7 × {x3, x4, x5}", "{x0, x2}", "if it's in here: about 0.472", YELLOW),
        (32, "x7 × x4", "{x3, x5}", "if it's x4: about 0.46", GREEN),
    ]
    for i, (step, kept, dropped, pred, colour) in enumerate(rows):
        y = 8.6 - i * 2.15
        ax.add_patch(FancyBboxPatch((0.6, y - 0.62), 6.6, 1.24, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    color=colour, linewidth=0))
        ax.text(0.85, y + 0.2, f"step {step}", fontproperties=F["mono"], fontsize=14, color=MUTED, va="center")
        ax.text(0.85, y - 0.25, kept, fontproperties=F["display"], fontsize=21, color=INK, va="center")
        ax.text(7.7, y + 0.22, f"predicted  {pred}", fontproperties=F["body"], fontsize=16, color=MUTED, va="center")
        ax.text(7.7, y - 0.26, f"got  {hist[step]:.3f}", fontproperties=F["display"], fontsize=20, color=INK,
                va="center")
        if dropped:
            ax.text(13.1, y, f"ruled out\n{dropped}", fontproperties=F["body"], fontsize=14, color=MUTED, va="center",
                    linespacing=1.3)
        if i < len(rows) - 1:
            ax.annotate("", xy=(2.2, y - 1.45), xytext=(2.2, y - 0.7), arrowprops=dict(
                arrowstyle="-|>,head_length=0.8,head_width=0.5", color=INK, linewidth=3))
    ax.text(0.85, 0.55, "x7 × x4 is member × flag: the one interaction hidden in the data.",
            fontproperties=F["display"], fontsize=20, color=INK)
    fig.savefig(out / "interaction-hunt.png", facecolor=PAPER)
    plt.close(fig)


# ------------------------------------------------------------------ all datasets: where they landed
def baseline_ranges(folder, name="baselines", steps=(50,)):
    b = ROOT / folder / "results" / name
    gd = json.loads((b / "gradient-descent.json").read_text())
    rs = json.loads((b / "random-search.json").read_text())
    adam = {s: [[c["test_accuracy"] for c in curve if c["step"] == s][0] for curve in gd.values()] for s in steps}
    return [c[-1]["test_accuracy"] for c in rs.values()], adam


def fig_all_scores(F, out):
    mdata, _ = project("mnist-training")
    _, ytest = mdata.load()["test"]
    panels = []
    rs, adam = baseline_ranges("mnist-training", steps=(50, 5000))
    panels.append(("MNIST", float(np.bincount(ytest).max() / len(ytest)), rs, adam[50], ("Adam, 5,000 steps", adam[5000]),
                   [results("mnist-training", f"opus-p8-{i}")[0]["best_val_loss_test_accuracy"] for i in (1, 2, 3)]))
    rules = json.loads((ROOT / "titanic-training/results/baselines/rules.json").read_text())
    rs, adam = baseline_ranges("titanic-training", steps=(50, 1000))
    panels.append(("Titanic", rules["everyone dies"]["test"], rs, adam[50], ("Adam, 1,000 steps", adam[1000]),
                   [results("titanic-training", f"opus-p8-{i}")[0]["best_val_loss_test_accuracy"] for i in (1, 2, 3)]))
    rs, adam = baseline_ranges("titanic-training", "baselines-anonymous", steps=(50, 1000))
    panels.append(("Titanic, anonymised", rules["everyone dies"]["test"], rs, adam[50], ("Adam, 1,000 steps", adam[1000]),
                   [results("titanic-training", f"anon-p8-{i}")[0]["best_val_loss_test_accuracy"] for i in (1, 2, 3)]))
    srules = json.loads((ROOT / "synthetic-training/results/baselines/rules.json").read_text())
    rs, adam = baseline_ranges("synthetic-training", steps=(50, 1000))
    panels.append(("Synthetic data", srules["everyone class 0"]["test"], rs, adam[50],
                   ("the true model", [srules["true model"]["test"]["accuracy"]]),
                   [results("synthetic-training", f"opus-p8-{i}")[0]["best_val_loss_test_accuracy"] for i in (1, 2, 3)]))
    rows = ["most common class", "random search, 50 tries", "Claude (3 runs)", "Adam, 50 steps", "ceiling"]
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=PAPER)
    header(fig, F, "The same pattern on every dataset",
           "Test accuracy; each dot is one run or seed. Claude beats random search everywhere, and on tabular data "
           "lands near a short run of Adam.")
    for k, (title, majority, rs, adam50, (ceil_name, ceil), claude) in enumerate(panels):
        ax = fig.add_axes([0.17 + k * 0.207, 0.13, 0.18, 0.62])
        ax.set_facecolor(PAPER)
        vals = [[majority], rs, claude, adam50, ceil]
        colours = [MUTED, MUTED, PINK, TEAL, INK]
        for r, (v, c) in enumerate(zip(vals, colours)):
            ax.plot([min(v), max(v)], [r, r], color=c, linewidth=3, alpha=0.5)
            ax.scatter(v, [r] * len(v), s=150 if c == PINK else 80, color=c, edgecolor=INK, linewidth=1.3, zorder=3)
        ax.set_ylim(len(rows) - 0.5, -0.5)
        ax.set_title(title, fontproperties=F["display"], fontsize=17, color=INK, loc="left")
        ax.text(max(ceil), len(rows) - 1 + 0.38, ceil_name, fontproperties=F["body"], fontsize=11, color=MUTED,
                ha="right")
        lo = min(min(v) for v in vals)
        ax.set_xlim(lo - 0.04, 1.0 if title == "MNIST" else 0.9)
        ticks = [t for t in np.arange(0, 1.01, 0.2 if title == "MNIST" else 0.1) if lo - 0.04 <= t <= ax.get_xlim()[1]]
        ax.set_xticks(ticks); ax.set_xticklabels([f"{t:.0%}" for t in ticks], fontproperties=F["mono"], fontsize=11,
                                                 color=MUTED)
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels(rows if k == 0 else [], fontproperties=F["body"], fontsize=14, color=INK)
        ax.grid(axis="x", color=RULE); ax.set_axisbelow(True)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(INK)
        ax.tick_params(length=0, axis="y")
    fig.savefig(out / "all-scores.png", facecolor=PAPER)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--fonts", default="~/code/private-notes/public/theme/static/fonts")
    args = ap.parse_args()
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    F = bf.fonts(args.fonts)
    fig_step_strips(F, out)
    fig_cover(F, out)
    fig_titanic_step1(F, out)
    fig_synthetic_recovered(F, out)
    fig_interaction_hunt(F, out)
    fig_all_scores(F, out)
    print("done")
