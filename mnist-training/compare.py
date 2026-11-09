"""Compare models across runs: a table (results/comparison.md) and a chart (results/plots/models.png).

    uv run python compare.py
"""
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
STEPS = 15
MODELS = [("claude-haiku-5-5", "Haiku 5.5"), ("claude-sonnet-5-5", "Sonnet 5.5"),
          ("claude-opus-4-6", "Opus 4.6"), ("claude-opus-4-8", "Opus 4.8"),
          ("claude-opus-5-5", "Opus 5.5"), ("claude-fable-5-1", "Fable 5.1"),
          ("claude-fable-5-2", "Fable 5.2")]
# Keyword check for fitting or sampling inside the submitted code; every hit still needs reading by a person.
SUSPECT = re.compile(r"\brng\b|random|lstsq|linalg\.solve|linalg\.inv|np\.cov|pinv|svd")


def runs_for(model):
    out = []
    for run_json in sorted(RESULTS.glob("*/run.json")):
        run = json.loads(run_json.read_text())
        # Only the strict 15-step comparison runs; the loss-plateau and other follow-ups are reported separately.
        if run.get("model") == model and "-high-strict-" in run_json.parent.name and len(json.loads((run_json.parent / "history.json").read_text())) >= STEPS:
            history = json.loads((run_json.parent / "history.json").read_text())
            hits = sorted({int(p.parent.name) for p in run_json.parent.glob("steps/*/submission.py")
                           if SUSPECT.search(p.read_text())})
            out.append(dict(run=run, history=history, suspect_steps=hits))
    return out


def main():
    lines = ["| Model | Runs | Step 1 (one-shot) | Step 15 | Mean step 15 | Cost per run | Minutes per run | Keyword hits |",
             "|---|---:|---|---|---:|---|---|---|"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for model, name in MODELS:
        runs = runs_for(model)
        if not runs:
            continue
        for r in runs:  # compare at the shared 15-step budget, even for runs extended later
            r["history"] = r["history"][:STEPS]
        first = [r["history"][0]["test_accuracy"] or 0 for r in runs]
        final = [r["history"][-1]["test_accuracy"] or 0 for r in runs]
        cost = [sum(h["cost_usd"] for h in r["history"]) for r in runs]
        minutes = [sum(h["seconds"] for h in r["history"]) / 60 for r in runs]
        hits = sum(len(r["suspect_steps"]) for r in runs)
        fmt = lambda xs: " / ".join(f"{x:.1%}" for x in xs)
        lines.append(f"| {name} | {len(runs)} | {fmt(first)} | {fmt(final)} | {np.mean(final):.1%} | "
                     f"{' / '.join(f'${c:.2f}' for c in cost)} | {' / '.join(f'{m:.0f}' for m in minutes)} | {hits} |")
        curves = np.array([[h["test_accuracy"] if h["ok"] else np.nan for h in r["history"]] for r in runs])
        steps = np.arange(1, curves.shape[1] + 1)
        line, = ax.plot(steps, np.nanmean(curves, 0), marker="o", ms=3, label=f"{name} (mean of {len(runs)})")
        ax.fill_between(steps, np.nanmin(curves, 0), np.nanmax(curves, 0), color=line.get_color(), alpha=0.15)
    rs = json.loads((RESULTS / "baselines" / "random-search.json").read_text())
    mean = np.mean([[c["test_accuracy"] for c in curve] for curve in rs.values()], axis=0)[:15]
    ax.plot(range(1, 16), mean, color="grey", ls="--", label="random search, same evaluations")
    ax.set_xlabel("step (one reply, one validation result)")
    ax.set_ylabel("test accuracy (never shown to the model)")
    ax.set_ylim(0, 1)
    ax.set_xlim(0.5, 15.5)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Writing MNIST weights from validation feedback (shaded: min to max of runs)", fontsize=9)
    fig.tight_layout()
    (RESULTS / "plots").mkdir(exist_ok=True)
    fig.savefig(RESULTS / "plots" / "models.png", dpi=150)
    (RESULTS / "comparison.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
