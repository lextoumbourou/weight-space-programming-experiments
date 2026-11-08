# Titanic training

Can an LLM train a small tabular network by writing its weights, guided only by validation loss, accuracy and a
confusion matrix? The same LLM Descent harness as `../mnist-training`, on Kaggle's Titanic data: a 258-parameter
MLP (`Linear(13, 16) → ReLU → Linear(16, 2)`), 600 passengers for feedback and 291 for a test set Claude never sees.
The design is in [PROTOCOL.md](PROTOCOL.md).

Needs macOS on Apple silicon (MLX), [uv](https://docs.astral.sh/uv/), an `ANTHROPIC_API_KEY`, and `train.csv` from
the [Kaggle competition](https://www.kaggle.com/c/titanic) unzipped into `data/download/` (it is not redistributed).

    uv run python baselines.py
    uv run python loop.py --run-id opus-p8-1 --steps 50 --plateau loss --patience 8 --min-gain 0.01 --min-steps 15 --hide-rule

## Results

Opus 5.5, effort high, three runs. The step with the lowest validation loss is the one scored.

| Run | Steps | Step 1 loss | Best loss (step) | Step 1 test | Scored test | Cost |
|---|---:|---:|---:|---:|---:|---:|
| opus-p8-1 | 15 | 0.4197 | 0.4130 (11) | 84.2% | 84.5% | $0.58 |
| opus-p8-2 | 15 | 0.4303 | 0.4127 (9) | 82.5% | 83.8% | $0.71 |
| opus-p8-3 | 16 | 0.4331 | 0.4098 (11) | 81.4% | 85.2% | $0.75 |

Baselines (`results/baselines/`), test accuracy on the same 291 passengers:

| Method | Validation loss | Test accuracy |
|---|---:|---:|
| Everyone dies | | 61.5% |
| Women survive, men die | | 81.8% |
| Random search, 50 evaluations (5 seeds) | | 69.8 to 78.4% |
| Adam, 50 steps (5 seeds) | 0.47 to 0.51 | 75.9 to 82.5% |
| Adam, 100 steps | 0.44 to 0.46 | 82.1 to 85.2% |
| Adam, 1,000 steps | 0.38 to 0.41 | 84.2 to 85.2% |
| Adam, 5,000 steps | 0.35 to 0.38 | 83.5 to 85.2% |

Adam trains on the same 600 passengers, so its validation loss is its training loss.

## What happened

- **Prior knowledge does the work at step 1.** All three runs independently wrote the same first network: a
  hand-set logistic-regression score from known Titanic facts (women, class, age, family size, Cherbourg, a recorded
  cabin), carried through the ReLU layer as ReLU(s) − ReLU(−s), plus a few interaction units such as "woman in third
  class" (penalty) and "child" (bonus). Step 1's loss (0.42 to 0.43) already beats Adam after 100 steps.
- **Then manual coordinate descent.** No run probed. Each step changes one or two settings (men's baseline, the age
  slope, the cabin or fare weight, a new interaction unit), reads the loss, keeps or reverts, and bisects between
  the two best values. Two runs test calibration by scaling every logit by 1.15 (worse both times).
- **Feedback helps a little.** The loss falls 2 to 5% from step 1 to the best step, to about Adam's 1,000-step loss.
  Test accuracy moves by 0 to 4 points, which is within the noise of a 291-passenger test set (one passenger is 0.34
  points; the standard error is about 2.1 points).
- **Cheap.** Under a dollar per run, against $2.56 to $9.44 for MNIST.

## Anonymised runs

The same data with the features shuffled, standardised over the 600 validation rows and named x0 to x12, the classes
named "class 0" and "class 1", and the dataset not named (`prompts/anonymous/`, `--anonymous`). Adam is faster on the
standardised inputs (`results/baselines-anonymous/`): 81 to 85% after 50 steps.

| Run | Steps | Best loss (step) | Scored test | Cost |
|---|---:|---:|---:|---:|
| anon-p8-1 | 25 | 0.4683 (24) | 80.8% | $0.72 |
| anon-p8-2 | 28 | 0.4584 (21) | 81.4% | $0.90 |
| anon-p8-3 | 33 | 0.4510 (31) | 83.5% | $1.07 |

- **Probing from step 1.** All three runs spend steps 1 to 13 probing one feature per step (a network that depends
  only on xN), reading each feature's direction and strength from the loss and confusion matrix. Step 14 combines
  them into a logistic score: the loss drops from about 0.62 to 0.47.
- **The anonymisation leaked.** The prompt said the split came from "the same 891 rows". Two runs recognised the
  Titanic from that number alone in their step 1 thinking ("I'm looking at the Titanic dataset: 891 rows ... 549
  died and 342 survived"), and the third from the 62/38 class balance at step 2. None says so in a reply. At step
  14 all three map the columns back to Titanic features from the probe results (run 2: "x10 looks like sex, x4 like
  Pclass_3", both correct), then add Titanic interactions such as sex by class.
- Even so, the anonymised runs end at a loss of 0.45 to 0.47 against 0.41 for the named runs.
