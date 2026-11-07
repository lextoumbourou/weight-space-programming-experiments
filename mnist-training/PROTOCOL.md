# Protocol

Fixed on 7 November 2026, before any paid run. Changes after a run starts are listed at the bottom with their date
and reason.

## Question

Can an LLM train a small MNIST CNN without gradients, by writing all of its weights and improving them over 15 steps,
when the only feedback is the validation loss, accuracy and confusion matrix?

## Data

MNIST from `https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz`, SHA-256
`731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1`, pixels divided by 255.

| Split | Images | Used for |
|---|---:|---|
| train | first 50,000 of the official training set | gradient-descent baselines only |
| val | last 10,000 of the official training set | the feedback the LLM sees |
| test | official 10,000 test images | the score; never shown to the LLM |

The LLM never sees an image from any split.

## Network

Fixed, 5,994 parameters (`network.py`). Described to the model as this PyTorch module, and run in MLX with the same
semantics (checked against an explicit NumPy implementation: largest difference 7.6e-8):

```
Conv2d(1, 8, 5) → ReLU → MaxPool2d(2) → Conv2d(8, 16, 5) → ReLU → MaxPool2d(2) → Flatten → Linear(256, 10)
```

## Each step

1. The model replies with one Python code block defining `build_weights()`, which returns all six parameter arrays.
2. `sandbox.py` runs it in a separate process where only numpy and math can be imported and `open`, `exec`, `eval`
   and `compile` are removed. The weights must have the exact shapes and be finite.
3. The network is scored on val (sent to the model) and test (stored only).
4. The model receives: this step's val loss, accuracy and 10×10 confusion matrix, a table of loss and accuracy for
   every step so far, and the number of steps left.

A step whose code fails, or whose reply has no code, still counts. The model is told the error. A reply that hits the
output limit or is declined is also a failed step, and the model is told.

## Conditions

- Model `claude-opus-5-5` through the Messages API (Anthropic Python SDK, `claude_client.py`), effort `high`,
  adaptive thinking with summarised thinking returned, `max_tokens` 128,000 (the model's maximum), streaming.
- No tools and no refusal fallback, so no other model can write weights partway through a run. The system prompt
  is the neutral "Answer the user's request."
- One conversation per run. Each step sends the full history: every earlier message and every reply, thinking
  blocks included, appended unchanged. Automatic prompt caching (5-minute) caches the history.
- 15 steps per run. The prompt is `prompts/task.md` and the feedback is `prompts/feedback.md`.

## Rules given to the model

Only numpy and math. Filters and templates may be drawn directly from formulas or hand-described strokes. No
generating a set of example inputs or feature vectors to compute weights from: no averaging over generated samples,
gradient descent, regression, least squares, clustering, discriminant analysis or search, including on synthetic
data. Don't run the network on inputs. The feedback is the only information about performance. Send the complete
function every step.

Not forbidden, and reported if it happens: using numpy's random generator, keeping weights that scored better, or
moving weights in the direction that lowered the loss. Steering by feedback is the point of the experiment.

## Scores

- **Final:** test accuracy of the last runnable step. This is what the model is told it will be scored on.
- **Best by validation:** test accuracy of the step with the highest validation accuracy.
- **Curve:** test accuracy at every step.
- **Cost:** computed from each response's token usage (uncached input, cache writes, cache reads, output) at the
  prices recorded in `run.json`. The raw usage is saved with every step.

## Reference points (`baselines.py`)

| Method | Budget | Test accuracy |
|---|---|---|
| Random search, (1+1) evolution strategy, 1/5th success rule | 50 validation evaluations, 5 seeds | 10.2–20.9% after 50; 10.9–13.0% after 15 |
| Adam, lr 1e-3, batch 64 | 50 gradient steps, 3 seeds | 91.4–92.4% |
| Adam, lr 1e-3, batch 64 | 5,000 gradient steps, 3 seeds | 98.7–98.8% |

Random search has the same feedback budget as the LLM but no reasoning. Adam sees images and gradients, which the LLM
never does, so it is a ceiling for this network rather than a fair contest.

## What a run cannot show

One run is one sample. The earlier one-shot MNIST attempts with Opus 5.5 ranged from 68% to 77%, so expect large
variation between runs. Model behaviour can change while the model ID stays the same.

## Changes after fixing the protocol

- **7 November 2026, before any completed step.** The first attempt ran the model through Claude Code
  (`claude -p --bare`, resumed session). It was stopped during step 1, before any reply, and its folder deleted.
  The client was switched to the Messages API so that the full conversation sent each step is under our control
  and saved, per-step cost comes from exact token usage (Claude Code reports a running session total), the output
  limit and refusals are explicit stop reasons, and thinking summaries are returned for the write-up. The prompt,
  network, data, feedback and step budget are unchanged.
- **7 November 2026, after a 14-step run.** That run's prompt did not forbid fitting. From step 4 the model
  generated 300 random synthetic stroke-model digits per class, computed their features with its own formula, and
  fitted a linear discriminant (LDA) by solving a linear system. Test accuracy reached 82.9% at step 14 (USD 2.27).
  It is kept as `results/opus-high-loose-rules-stopped/`. The rules now forbid computing weights from generated
  samples while still allowing hand-drawn filters and templates, the wording the earlier shapes prompt used. The step
  budget was cut from 50 to 15. Results before this change are not comparable with those after it.
- **7 November 2026, after the 15-step model comparison.** The three Opus 5.5 runs are continued in the same
  conversations (`--resume --extend-to 50`). The message after step 15 tells the model the budget has been extended
  (it had been told step 15 was its last) and states the stopping rule: the run stops after any step once validation
  accuracy has improved by less than 0.5 percentage points over the previous 5 steps, checked only after at least 5
  new steps, with a hard cap of 50 steps. The stopping rule uses validation accuracy only; the test set is still
  never sent. The 15-step comparison uses each run's step-15 result, which these extensions do not change.
- **7 November 2026, model comparison.** The same 15-step protocol, request settings (effort `high`, adaptive
  thinking with summaries, 128,000 output tokens) and prompts were run on `claude-haiku-5-5`, `claude-sonnet-5-5`,
  `claude-opus-4-6`, `claude-opus-4-8` and `claude-fable-5-1`, three runs each. Two of the three Opus 4.6 runs were
  stopped during step 1 because of their cost and time. Effort levels are not calibrated across models.
