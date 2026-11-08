# Protocol

Fixed on 8 November 2026, before any paid run. The harness is the Titanic one (`../titanic-training/PROTOCOL.md`),
which is the MNIST one with a tabular network. Everything not mentioned here is the same.

## Question

The anonymised Titanic runs could not test learning without prior knowledge: Claude recognised the Titanic from its
row count and class balance. Here the data is generated for this test from a known random process, so there is
nothing to recognise. How far does LLM Descent get on tabular data when feedback is the only source of information,
and how close does it come to the true model?

## Data (`data.py`)

Twelve features, generated with seed 2026: a binary "member" (40%), an ordinal tier (0, 1, 2), a gamma-distributed
"years", a Poisson(1.2) count, a log-normal "spend", a binary "flag" (20%), a noisy proxy of log spend, a normal
"distance", three pure-noise features and a binary "weekend". The label is drawn from this logistic model:

    logit = -0.4 + 1.8 * ( 1.8 member - 0.7 tier + 0.45 max(4 - years, 0) - 0.9 max(visits - 2, 0)
                           + 0.8 (log spend - 3) - 2.6 member * flag + 0.6 (|distance| - 0.8) + 0.3 weekend )

So it has linear effects, two thresholds (young accounts, many visits), a U-shape (distance), an interaction
(flagged members) and irrelevant or merely correlated features. All of these are representable by the network.

The columns are shuffled (fixed permutation, seed 2027), standardised over the validation rows and named x0 to x11.
Classes are "class 0" and "class 1". The prompt says the data is synthetic, generated from a hidden random process,
and that some features may be irrelevant or act non-linearly. It does not describe the features.

| Split | Rows | Class 1 | Used for |
|---|---:|---:|---|
| val | 1,000 | 39.5% | the feedback the LLM sees; also the gradient baselines' training data |
| test | 10,000 | 41.4% | the score; never shown to the LLM |

The large test set makes the score precise (standard error about 0.4 points).

The true model scores 81.6% (loss 0.397) on val and 82.0% (loss 0.392) on test: the ceiling, on average, for any
classifier.

## Network

Fixed, 242 parameters: `Linear(12, 16) → ReLU → Linear(16, 2)`.

## Conditions and runs

As the Titanic runs: Opus 5.5, effort high, up to 50 steps, the hidden loss-plateau rule (at least 15 steps,
patience 8, 1%), lowest validation loss scored. Runs `opus-p8-1` to `opus-p8-3`.

## Changes

None yet.
