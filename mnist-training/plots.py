"""Figures for the write-up, regenerated from saved results.

    uv run python plots.py opus-high-1 [more run ids]

Writes to results/plots/:
  curve.png                  test accuracy per step for each run, with the baselines
  <run>-filters.png          conv1's 8 filters at selected steps
  <run>-confusion.png        validation confusion matrices at selected steps
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
OUT = RESULTS / "plots"


def load_history(run_id):
    return json.loads((RESULTS / run_id / "history.json").read_text())


def selected_steps(history, n=6):
    ok = [h["step"] for h in history if h["ok"]]
    if len(ok) <= n:
        return ok
    return sorted({ok[round(i * (len(ok) - 1) / (n - 1))] for i in range(n)})


def curve(run_ids):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    last = max(len(load_history(r)) for r in run_ids)
    for run_id in run_ids:
        h = [x for x in load_history(run_id) if x["ok"]]
        ax.plot([x["step"] for x in h], [x["test_accuracy"] for x in h], marker="o", ms=3, label=run_id)
    baselines = RESULTS / "baselines"
    if (baselines / "random-search.json").exists():
        rs = json.loads((baselines / "random-search.json").read_text())
        mean = np.mean([[c["test_accuracy"] for c in curve_] for curve_ in rs.values()], axis=0)[:last]
        ax.plot(range(1, len(mean) + 1), mean, color="grey", ls="--", label="random search, same evaluations (mean of 5)")
    if (baselines / "gradient-descent.json").exists():
        gd = json.loads((baselines / "gradient-descent.json").read_text())
        at = lambda step: np.mean([[c["test_accuracy"] for c in s if c["step"] == step][0] for s in gd.values()])
        ax.axhline(at(50), color="green", ls=":", label=f"Adam, 50 gradient steps ({at(50):.3f})")
        ax.axhline(at(5000), color="green", ls="-.", label=f"Adam, 5,000 gradient steps ({at(5000):.3f})")
    ax.set_xlim(0.5, last + 0.5)
    ax.set_xlabel("step (one reply, one validation result)")
    ax.set_ylabel("test accuracy (never shown to the model)")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "curve.png", dpi=150)


def filters(run_id):
    steps = selected_steps(load_history(run_id))
    fig, axes = plt.subplots(len(steps), 8, figsize=(8, 1.1 * len(steps)), squeeze=False)
    for r, step in enumerate(steps):
        w = np.load(RESULTS / run_id / "steps" / f"{step:02d}" / "weights.npz")["conv1.weight"]
        for c in range(8):
            ax = axes[r, c]
            m = np.abs(w[c, 0]).max() or 1
            ax.imshow(w[c, 0], cmap="RdBu_r", vmin=-m, vmax=m)
            ax.set_xticks([])
            ax.set_yticks([])
        axes[r, 0].set_ylabel(f"step {step}", rotation=0, ha="right", va="center")
    fig.suptitle(f"{run_id}: conv1 filters (red positive, blue negative)", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f"{run_id}-filters.png", dpi=150)


def confusions(run_id):
    steps = selected_steps(load_history(run_id), n=4)
    fig, axes = plt.subplots(1, len(steps), figsize=(3.2 * len(steps), 3.2), squeeze=False)
    for ax, step in zip(axes[0], steps):
        m = json.loads((RESULTS / run_id / "steps" / f"{step:02d}" / "metrics.json").read_text())["val"]
        ax.imshow(np.array(m["confusion"]), cmap="Blues")
        ax.set_title(f"step {step}: {m['accuracy']:.3f}", fontsize=9)
        ax.set_xlabel("predicted")
        ax.set_ylabel("true")
        ax.set_xticks(range(10))
        ax.set_yticks(range(10))
    fig.tight_layout()
    fig.savefig(OUT / f"{run_id}-confusion.png", dpi=150)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    runs = sys.argv[1:]
    curve(runs)
    for run_id in runs:
        filters(run_id)
        confusions(run_id)
    print("wrote", sorted(p.name for p in OUT.iterdir()))
