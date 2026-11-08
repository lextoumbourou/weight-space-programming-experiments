"""Reference points for the LLM's steps, on the same network and splits.

rules.json: everyone is class 0 (the majority class), and the true generating model (the best possible).
gradient-descent.json: Adam (lr 1e-3, batch 64) on the same 1,000 validation rows the LLM gets feedback on. Test accuracy after 0, 50, 100, 500, 1,000 and 5,000
    gradient steps, five seeds.
random-search.json: a (1+1) evolution strategy with the same budget as the LLM, 50 validation evaluations.
    Each evaluation scores a random perturbation of the best weights so far on the validation set and keeps it if
    the loss is lower. The step size follows the 1/5th success rule. Five seeds.

    uv run python baselines.py
"""
import json
from pathlib import Path

import mlx.core as mx
import mlx.optimizers as optim
import numpy as np

import data
import network

OUT = Path(__file__).resolve().parent / "results" / "baselines"
CHECKPOINTS = [0, 50, 100, 500, 1_000, 5_000]


def rule_scores(splits):
    """Everyone is class 0 (the majority class), and the true generating model (the best possible on average)."""
    out = {"everyone class 0": {k: float((splits[k][1] == 0).mean()) for k in ("val", "test")}}
    out["true model"] = {k: data.bayes(k) for k in ("val", "test")}
    return out


def gradient_descent(splits, seed):
    params = network.to_mx(network.pytorch_init(seed))
    optimizer = optim.Adam(learning_rate=1e-3)
    x, y = splits["val"]
    rng = np.random.default_rng(seed)
    loss_and_grad = mx.value_and_grad(lambda p, xb, yb: network.cross_entropy(network.forward(p, xb), yb))
    curve = []
    for step in range(CHECKPOINTS[-1] + 1):
        if step in CHECKPOINTS:
            weights = {k: np.array(v) for k, v in params.items()}
            val, test = network.evaluate(weights, *splits["val"]), network.evaluate(weights, *splits["test"])
            curve.append(dict(step=step, val_loss=val["loss"], val_accuracy=val["accuracy"],
                              test_loss=test["loss"], test_accuracy=test["accuracy"]))
            print(f"gradient descent seed {seed} step {step}: val {val['accuracy']:.4f} test {test['accuracy']:.4f}", flush=True)
        if step == CHECKPOINTS[-1]:
            break
        batch = rng.integers(0, len(y), 64)
        _, grads = loss_and_grad(params, mx.array(x[batch]), mx.array(y[batch]))
        optimizer.update(params, grads)
        mx.eval(params, optimizer.state)
    return curve


def random_search(splits, seed, evaluations=50):
    rng = np.random.default_rng(1_000 + seed)
    best = network.pytorch_init(seed)
    best_val = network.evaluate(best, *splits["val"])
    sigma = 0.02
    curve = [dict(evaluation=1, val_loss=best_val["loss"], val_accuracy=best_val["accuracy"],
                  test_accuracy=network.evaluate(best, *splits["test"])["accuracy"], sigma=sigma)]
    for evaluation in range(2, evaluations + 1):
        candidate = {k: (v + rng.normal(0, sigma, v.shape)).astype(np.float32) for k, v in best.items()}
        val = network.evaluate(candidate, *splits["val"])
        if val["loss"] < best_val["loss"]:
            best, best_val, sigma = candidate, val, sigma * 1.5
        else:
            sigma *= 1.5 ** -0.25  # 1/5th success rule
        curve.append(dict(evaluation=evaluation, val_loss=best_val["loss"], val_accuracy=best_val["accuracy"],
                          test_accuracy=network.evaluate(best, *splits["test"])["accuracy"], sigma=sigma))
    print(f"random search seed {seed}: best val {best_val['accuracy']:.4f}, test {curve[-1]['test_accuracy']:.4f}", flush=True)
    return curve


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    splits = data.load()
    rules = rule_scores(splits)
    print(json.dumps(rules, indent=2))
    (OUT / "rules.json").write_text(json.dumps(rules, indent=2))
    gd = {f"seed-{s}": gradient_descent(splits, s) for s in range(5)}
    (OUT / "gradient-descent.json").write_text(json.dumps(gd, indent=2))
    rs = {f"seed-{s}": random_search(splits, s) for s in range(5)}
    (OUT / "random-search.json").write_text(json.dumps(rs, indent=2))
