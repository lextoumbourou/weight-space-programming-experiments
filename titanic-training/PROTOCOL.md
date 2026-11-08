# Protocol

Fixed on 8 November 2026, before any paid run. Changes after a run starts are listed at the bottom with their date
and reason. The harness is the MNIST one (`../mnist-training/PROTOCOL.md`) with a different dataset and network;
everything not mentioned here is the same.

## Question

Can an LLM train a small tabular network without gradients, by writing all of its weights and improving them over up
to 50 steps, when the only feedback is the validation loss, accuracy and confusion matrix? Unlike MNIST, the model
already knows a lot about the problem (who survived the Titanic and why), so this also asks how far prior knowledge
gets it at step 1, and whether feedback adds anything on top.

## Data

Kaggle Titanic `train.csv` (891 labelled passengers), SHA-256
`7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f`, downloaded with
`kaggle competitions download titanic`. Not redistributed in this repo. Kaggle's `test.csv` has no labels and is not
used.

Each passenger becomes 13 numbers (`data.py`): class one-hot (3), female, age in decades (0 if missing), age known,
siblings/spouses, parents/children, log(1 + fare), port one-hot (3), cabin known. Name, ticket and cabin text are
dropped.

| Split | Passengers | Used for |
|---|---:|---|
| val | 600 (230 survived) | the feedback the LLM sees; also the gradient baselines' training data |
| test | 291 (112 survived) | the score; never shown to the LLM |

Stratified by survival with seed 1912. With 291 test passengers, one passenger is 0.34 points and the standard error
of an accuracy near 82% is about 2.3 points, so small differences are noise.

## Network

Fixed, 258 parameters (`network.py`): `Linear(13, 16) → ReLU → Linear(16, 2)`. Run in MLX, checked against a NumPy
implementation (largest difference 1.7e-7).

## Conditions

As the final MNIST runs: `claude-opus-5-5`, effort high, adaptive thinking (summarised), 128,000 max tokens, no
tools, neutral system prompt, one conversation per run with the full history each step. Up to 50 steps; after at
least 15 steps the run stops once the best validation loss has not improved by 1% over the last 8 steps. The model is
told only that it has up to 50 steps and that the step with the lowest validation loss is scored on the test set.

The prompt (`prompts/task.md`) names the dataset and describes every input. It allows setting weights "from rules,
formulas or what you know about the Titanic", and keeps the MNIST bans on fitting, search and synthetic data.

## Baselines (`baselines.py`)

- Rules: everyone dies; women survive and men die.
- Adam (lr 1e-3, batch 64) on the 600 validation passengers, five seeds, checkpoints 0 to 5,000 steps.
- Random search, a (1+1) evolution strategy with 50 validation evaluations, five seeds.

## Runs

`opus-p8-1`, `opus-p8-2`, `opus-p8-3`:

    uv run python loop.py --run-id opus-p8-N --steps 50 --plateau loss --patience 8 --min-gain 0.01 --min-steps 15 --hide-rule

## Changes

- 8 November 2026, after the three named runs: added an anonymised variant (`--anonymous`, `prompts/anonymous/`,
  `baselines.py --anonymous`) to separate prior knowledge from learning from feedback. Columns are shuffled by a
  fixed permutation (seed 1913), standardised over the 600 validation rows and named x0 to x12; classes are "class 0"
  and "class 1"; the dataset is not named. Runs `anon-p8-1` to `anon-p8-3`, same conditions otherwise. The prompt
  still gave the total of 891 rows, which identified the dataset; see the README.
