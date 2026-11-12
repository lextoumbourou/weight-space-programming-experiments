# Cats vs. dogs training without gradients

The [MNIST experiment](../mnist-training/) on a harder problem: the Kaggle Dogs vs. Cats photos at 64x64. An LLM
writes all 24,898 weights of a fixed CNN and improves them from loss, accuracy and a 2x2 confusion matrix. The design
is in [PROTOCOL.md](PROTOCOL.md).

## Setup

Needs macOS on Apple silicon (MLX), [uv](https://docs.astral.sh/uv/), an `ANTHROPIC_API_KEY` and a Kaggle account
that has accepted the competition rules.

```sh
cd catdog-training
uv sync
kaggle competitions download dogs-vs-cats -f train.zip -p data/download
uv run python baselines.py
uv run python loop.py --run-id plumbing --fake --steps 3
```

## Running

```sh
uv run python loop.py --run-id opus-1 --steps 50 --plateau loss --patience 8 --min-gain 0.01 --min-steps 15 --hide-rule
```

The files and saved results follow `../mnist-training/README.md`.

## Results

One run per model on 10 November 2026, with the command above (up to 50 steps, scored on the lowest-validation-loss
step). Test accuracy on the 5,000 held-out photos, which the model never sees.

| Model | Run | Best test accuracy | Steps | Output tokens | Cost |
|---|---|---:|---:|---:|---:|
| Opus 5.5 | `results/opus-1` | 64.4% | 17 | 41K | $1.28 |
| Fable 5.2 | `results/fable52-1` | 62.9% | 15 | 150K | $7.72 |

Both runs were interrupted by a dropped connection and resumed with `--resume`. Random search with the same number of
evaluations reaches about 51%; Adam reaches about 55% after 500 gradient steps and 74% after 5,000
(`results/baselines/`). One run per model cannot separate the two.
