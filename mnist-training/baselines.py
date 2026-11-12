"""Reference points on the same network and splits, written to results/baselines/.

adam.json: Adam (lr 1e-3, batch 64) trained on the same 10,000 training images Claude gets feedback on. Test
    accuracy after 0, 50, 100, 500, 1,000 and 5,000 gradient steps, three seeds.
random-search.json: a (1+1) evolution strategy with Claude's budget of 50 evaluations on the training set. Each
    evaluation scores a random perturbation of the best weights so far and keeps it if the training loss is lower.
    The step size follows the 1/5th success rule. Five seeds.

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


def scores(weights, splits):
    train, test = network.evaluate(weights, *splits["train"]), network.evaluate(weights, *splits["test"])
    return dict(train_loss=train["loss"], train_accuracy=train["accuracy"], test_accuracy=test["accuracy"])


def adam(splits, seed, steps=CHECKPOINTS[-1]):
    """Returns the learning curve and the final weights."""
    params = network.to_mx(network.pytorch_init(seed))
    optimizer = optim.Adam(learning_rate=1e-3)
    x, y = splits["train"]
    rng = np.random.default_rng(seed)
    loss_and_grad = mx.value_and_grad(lambda p, xb, yb: network.cross_entropy(network.forward(p, xb), yb))
    curve = []
    for step in range(steps + 1):
        if step in CHECKPOINTS:
            curve.append(dict(step=step, **scores({k: np.array(v) for k, v in params.items()}, splits)))
            print(f"adam seed {seed} step {step}: test {curve[-1]['test_accuracy']:.4f}", flush=True)
        if step == steps:
            break
        batch = rng.integers(0, len(y), 64)
        _, grads = loss_and_grad(params, mx.array(x[batch]), mx.array(y[batch]))
        optimizer.update(params, grads)
        mx.eval(params, optimizer.state)
    return curve, {k: np.array(v) for k, v in params.items()}


def random_search(splits, seed, evaluations=50):
    rng = np.random.default_rng(1_000 + seed)
    best = network.pytorch_init(seed)
    best_loss = network.evaluate(best, *splits["train"])["loss"]
    sigma = 0.02
    curve = [dict(evaluation=1, **scores(best, splits))]
    for evaluation in range(2, evaluations + 1):
        candidate = {k: (v + rng.normal(0, sigma, v.shape)).astype(np.float32) for k, v in best.items()}
        loss = network.evaluate(candidate, *splits["train"])["loss"]
        if loss < best_loss:
            best, best_loss, sigma = candidate, loss, sigma * 1.5
        else:
            sigma *= 1.5 ** -0.25  # 1/5th success rule
        curve.append(dict(evaluation=evaluation, **scores(best, splits)))
    print(f"random search seed {seed}: test {curve[-1]['test_accuracy']:.4f}", flush=True)
    return curve


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    splits = data.load()
    curves = {}
    for seed in range(3):
        curves[f"seed-{seed}"], weights = adam(splits, seed)
        if seed == 0:
            np.savez(OUT / "adam-seed-0-5000-steps.npz", **weights)  # for the filters figure
    (OUT / "adam.json").write_text(json.dumps(curves, indent=2))
    rs = {f"seed-{s}": random_search(splits, s) for s in range(5)}
    (OUT / "random-search.json").write_text(json.dumps(rs, indent=2))
