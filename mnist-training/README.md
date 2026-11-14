# MNIST: LLM Descent

Claude (Opus 5.5 and Fable 5.2) writes every one of the 5,994 weights of a small, fixed CNN for MNIST, then improves them over up
to 50 steps. There is no gradient descent and no fitting: each step it gets back the training loss, accuracy and
confusion matrix, and writes the whole network again. Two conditions:

- **a, numbers only:** it never sees an image.
- **b, with images:** it also sees 50 example training images at the start, and 16 of its network's mistakes after
  every step.

The full design is in [PROTOCOL.md](PROTOCOL.md). Written up in
[LLM Descent](https://notesbylex.com/llm-descent.html) on Notes by Lex.

## Results

Test accuracy (official 10,000 test images, never shown to Claude) of each run's lowest-training-loss network. Runs `a-*` and `b-*` are Opus 5.5; `fable-a-*` are Fable 5.2 in condition a.

| Run | Steps | Best step | Training loss | Test accuracy | Cost |
|---|---:|---:|---:|---:|---:|
| a-1 | 23 | 15 | 0.887 | 72.1% | $3.84 |
| a-2 | 21 | 16 | 0.907 | 70.5% | $4.23 |
| a-3 | 19 | 12 | 0.852 | 73.8% | $2.74 |
| b-1 | 50 | 50 | 0.767 | 76.6% | $8.62 |
| b-2 | 27 | 19 | 0.833 | 72.5% | $4.67 |
| b-3 | 40 | 37 | 0.777 | 75.1% | $8.39 |
| fable-a-1 | 50 | 50 | 0.309 | 91.3% | $26.64 |
| fable-a-2 | 50 | 50 | 0.367 | 88.3% | $29.48 |
| fable-a-3 | 50 | 50 | 0.264 | 91.2% | $31.18 |

Baselines on the same network and splits (`results/baselines/`):

| Method | Test accuracy |
|---|---:|
| Random search, 50 training-set evaluations (5 seeds) | 10.2 to 20.9% |
| Adam, 50 steps (3 seeds) | 88.9 to 91.7% |
| Adam, 1,000 steps | 97.2 to 97.6% |
| Adam, 5,000 steps | 97.7 to 98.0% |

Adam trains on the same 10,000 images Claude gets feedback on.

## What happened

Every run builds a pre-deep-learning digit recogniser by hand: oriented stroke or edge detectors in the first
layer, hand-drawn digit templates, then a classical scoring rule. First step at which each run's reply uses each
technique (from the step headings and opening paragraphs):

| Technique | a-1 | a-2 | a-3 | b-1 | b-2 | b-3 |
|---|---:|---:|---:|---:|---:|---:|
| hand-drawn digit templates | 1 | 1 | 1 | 1 | 1 | 1 |
| nearest-centroid or cosine matching | 1 | 4 | 2 | 2 | 9 | 3 |
| naive Bayes | | 7 | 2 | 5 | | 4 |
| loop or hole detectors | 10 | 6 | 3 | 3 | 4 | 2 |
| stroke-endpoint detectors | 17 | 19 | | | 7 | 24 |
| probe (a step that measures features instead of classifying) | | 10 | 17 | | 12 | |

- **Seeing images changed little.** Condition b scored 74.7% on average against 72.1% for a, and its runs lasted
  longer (27 to 50 steps against 19 to 23), much of it spent recalibrating. Its replies and thinking rarely mention
  the images. One of the few that does: "Looking at the images, the closed-top 4s form a triangle that reads like a
  9, which is a genuinely hard case, while the others are open 4s." (`b-3`, step 39).
- **b-2 measured instead of looking.** Even with images available, it spent 14 of its 27 steps on probes: one
  feature at a time, it read class-by-class histograms back through the confusion matrix. The stopping rule ended
  the run in the middle of that measurement, because probe steps never improve the best loss.
- No submission contains pixel values copied from the images.
- **Fable 5.2 measures far more.** Its three runs spent 20, 24 and 27 of their 50 steps on measurement steps
  (Opus 5.5: 0, 3 and 1), then rebuilt their classifiers from the measured rates. Run 1 dropped its hand-drawn
  templates entirely at step 31: "No hand-drawn stroke templates remain in the final layer." All three used the full
  50 steps and were still improving, landing at 88.3 to 91.3%, level with 50 steps of Adam.

## Files

    data.py           MNIST download, splits, the condition-b example images
    network.py        the fixed CNN, in MLX with PyTorch weight layout
    sandbox.py        runs Claude's build_weights() with only numpy, scipy and math
    claude_client.py  the Messages API conversation
    images.py         the digit grids shown in condition b
    loop.py           the experiment
    prompts/          the task prompt and the feedback templates
    baselines.py      Adam and random search
    figures.py        the blog figures
    results/<run>/    prompt.md, history.json, run.json, messages.json, and for every step: the message sent
                      (message.md, plus any images), the reply, the thinking summary, the code, the weights,
                      the metrics and the API receipt

## Running it

Needs macOS on Apple silicon (MLX), [uv](https://docs.astral.sh/uv/) and an `ANTHROPIC_API_KEY`. Every run calls
a paid API.

    uv run python baselines.py
    uv run python loop.py --condition a --run-id a-1
    uv run python loop.py --condition b --run-id plumbing --fake   # no API calls
    uv run python figures.py --out figures/

The earlier MNIST runs (the first version of this protocol, the model comparison and the loose-rules run) are in
version control at commit `e26658b`.
