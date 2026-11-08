"""A synthetic tabular dataset, made for this test, so the model cannot know it in advance.

Twelve features of mixed kinds (binary, ordinal, counts, skewed and normal continuous), some correlated, three pure
noise. The label is drawn from a known logistic model with linear effects, two nonlinear effects and one interaction
(`true_logit`), so the best possible loss and accuracy are known. The columns are shuffled and standardised before the
network sees them, and are named x0 to x11.

Splits (seed 2026): val 1,000 rows, the feedback the LLM sees (and the gradient baselines' training data);
test 10,000 rows, never shown to the LLM.
"""
import hashlib

import numpy as np

N_VAL, N_TEST = 1_000, 10_000
SEED = 2026

# Design names, in generation order. The model only ever sees x0..x11 in the shuffled order below.
DESIGN = [
    ("member", "binary, 40% ones; strong positive effect"),
    ("tier", "ordinal 0, 1, 2; negative effect per level"),
    ("years", "normal-ish continuous; positive bump only for low values (below about -1 sd)"),
    ("visits", "count, Poisson(1.2); negative effect only beyond 2"),
    ("spend", "log-normal, skewed; positive effect on log scale"),
    ("flag", "binary, 20% ones; no effect alone, strongly negative together with member"),
    ("spend_proxy", "correlated with log spend; no direct effect"),
    ("distance", "normal continuous; U-shaped effect (positive in both tails)"),
    ("noise_bin", "binary, 50% ones; no effect"),
    ("noise_a", "normal; no effect"),
    ("noise_b", "uniform; no effect"),
    ("weekend", "binary, 50% ones; weak positive effect"),
]
PERMUTATION = [int(i) for i in np.random.default_rng(SEED + 1).permutation(len(DESIGN))]  # column j = design PERMUTATION[j]


def generate(n, rng):
    member = (rng.random(n) < 0.4).astype(float)
    tier = rng.choice([0.0, 1.0, 2.0], n, p=[0.3, 0.4, 0.3])
    years = rng.gamma(4.0, 2.0, n)  # mean 8, skewed a little
    visits = rng.poisson(1.2, n).astype(float)
    spend = np.exp(rng.normal(3.0, 0.8, n))
    flag = (rng.random(n) < 0.2).astype(float)
    spend_proxy = 0.7 * np.log(spend) + rng.normal(0, 0.5, n)
    distance = rng.normal(0, 1, n)
    noise_bin = (rng.random(n) < 0.5).astype(float)
    noise_a = rng.normal(0, 1, n)
    noise_b = rng.uniform(0, 1, n)
    weekend = (rng.random(n) < 0.5).astype(float)
    x = np.stack([member, tier, years, visits, spend, flag, spend_proxy, distance, noise_bin, noise_a, noise_b, weekend], 1)
    return x


INTERCEPT, STRENGTH = -0.4, 1.8  # tuned below for about 40% positives


def true_logit(x):
    member, tier, years, visits, spend, flag, _, distance, _, _, _, weekend = x.T
    return INTERCEPT + STRENGTH * (
            + 1.8 * member
            - 0.7 * tier
            + 0.45 * np.maximum(4.0 - years, 0)       # young accounts (under 4 years) get a bump
            - 0.9 * np.maximum(visits - 2, 0)          # each visit beyond 2 hurts
            + 0.8 * (np.log(spend) - 3.0)
            - 2.6 * member * flag                      # flagged members lose most of the member bonus
            + 0.6 * (np.abs(distance) - 0.8)           # U-shape
            + 0.3 * weekend)


def load(anonymous=True):
    """Return {"val": (x, y), "test": (x, y)} with x shuffled and standardised (val statistics), plus true probabilities."""
    rng = np.random.default_rng(SEED)
    x = generate(N_VAL + N_TEST, rng)
    p = 1 / (1 + np.exp(-true_logit(x)))
    y = (rng.random(len(p)) < p).astype(np.int64)
    z = x[:, PERMUTATION]
    mean, std = z[:N_VAL].mean(0), z[:N_VAL].std(0)
    z = ((z - mean) / std).astype(np.float32)
    return {"val": (z[:N_VAL], y[:N_VAL]), "test": (z[N_VAL:], y[N_VAL:]),
            "p_val": p[:N_VAL], "p_test": p[N_VAL:]}


def _digest():
    s = load()
    return hashlib.sha256(b"".join(np.ascontiguousarray(s[k][i]).tobytes() for k in ("val", "test") for i in (0, 1))).hexdigest()


def bayes(split="test"):
    """Loss and accuracy of the true model: the best any classifier can do on average."""
    s = load()
    (x, y), p = s[split], s["p_" + split]
    loss = float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return dict(loss=loss, accuracy=float(((p > 0.5) == y).mean()))


SHA256 = _digest()  # of the generated splits; the data is generated, not downloaded


if __name__ == "__main__":
    s = load()
    for k in ("val", "test"):
        x, y = s[k]
        print(k, x.shape, "positive rate", round(y.mean(), 3), "bayes", bayes(k))
    print("permutation", PERMUTATION, "sha256", SHA256)
