# Synthetic tabular training

LLM Descent on data Claude cannot know: a tabular dataset generated for this test from a known logistic model with
linear effects, thresholds, a U-shape, one interaction and some irrelevant features (`data.py`, described in
[PROTOCOL.md](PROTOCOL.md)). Twelve shuffled, standardised features named x0 to x11; a 242-parameter MLP
(`Linear(12, 16) → ReLU → Linear(16, 2)`); 1,000 rows of feedback and 10,000 test rows Claude never sees. It follows
the Titanic runs (`../titanic-training`), where Claude recognised the dataset even when anonymised.

Needs macOS on Apple silicon (MLX), [uv](https://docs.astral.sh/uv/) and an `ANTHROPIC_API_KEY`. The data is
generated, so there is nothing to download.

    uv run python baselines.py
    uv run python loop.py --run-id opus-p8-1 --steps 50 --plateau loss --patience 8 --min-gain 0.01 --min-steps 15 --hide-rule

## Results

Opus 5.5, effort high, three runs; the step with the lowest validation loss is scored. Test accuracy is on 10,000
rows (standard error about 0.4 points).

| Run | Steps | Best loss (step) | Scored test | Cost |
|---|---:|---:|---:|---:|
| opus-p8-1 | 40 | 0.455 (35) | 78.5% | $2.01 |
| opus-p8-2 | 47 | 0.474 (47) | 76.6% | $2.06 |
| opus-p8-3 | 21 | 0.506 (20) | 76.8% | $0.68 |

| Baseline | Test accuracy |
|---|---:|
| Everyone class 0 | 58.6% |
| Random search, 50 evaluations (5 seeds) | 62.3 to 70.2% |
| Adam, 50 steps (5 seeds) | 76.5 to 77.6% |
| Adam, 100 steps | 77.6 to 78.3% |
| Adam, 1,000 steps | 78.6 to 79.6% |
| Adam, 5,000 steps (overfits the 1,000 rows) | 78.1 to 79.0% |
| The true model (the ceiling) | 82.0% |

With no prior knowledge, LLM Descent lands where Adam is after 50 to 100 steps, and 3.5 to 5.4 points below the true
model.

## What happened

All three runs follow the same plan, which none was told:

1. **Measure each feature (steps 1 to 13).** One feature per step, as in the anonymised Titanic runs. Runs 1 and 2
   keep each feature that helps, so their probes build up a linear model as they go.
2. **Combine into a linear score**, carried through the ReLU layer as ReLU(z) − ReLU(−z), and tune its scale.
3. **Search for nonlinearity.** |x| terms (two ReLUs per feature) to test for U-shapes, first in groups, then one
   at a time.
4. **Search for interactions** (runs 1 and 3). Run 1 builds products from ReLUs, using
   u·v ≈ ½(|u + v| − |u − v|), then group-tests every interaction involving one feature and bisects the group, and
   runs each probe with both signs so the difference measures the effect without relying on its baseline estimate.

How close it got, against the generating model (column map in `data.PERMUTATION`):

- Run 1 found the one real interaction, member × flag (x7 · x4, negative), by group testing and bisection.
- All three runs got the signs of the linear effects right (member, spend, tier, visits, flag) and set all three
  pure-noise features (x3, x8, x10) to exactly zero. Run 2 also dropped the spend proxy, which has no effect of its
  own.
- None found the U-shape in distance (x2), which has no linear effect at all, or the bump for young accounts (x0).
  Some |x| terms they kept are on binary features, where |x| is only a re-encoding.
- Run 3 stopped at step 21, before any interaction search, and scored lowest on loss.
