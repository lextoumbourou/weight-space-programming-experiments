# Protocol

Fixed on 13 November 2026, before any paid run. This replaces the earlier MNIST protocol (kept in version control
at commit `e26658b`). The changes from that version: the feedback is called the training set, the Adam baselines
train on the same images Claude gets feedback on, the sandbox also allows scipy (matching the original Go
experiment's sandbox more closely), and there is a second condition with images.

## Question

Can Claude train a small MNIST CNN without gradients, by writing all of its weights and improving them from
feedback? And what changes when it can see some digits, including the ones its network gets wrong?

## Data (`data.py`)

MNIST from `https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz`, SHA-256
`731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1`, pixels divided by 255.

| Split | Images | Used for |
|---|---:|---|
| train | last 10,000 of the official training set | Claude's feedback; the Adam baselines' training data |
| test | the official 10,000 test images | the score; never shown to Claude |

## Network (`network.py`)

Fixed, 5,994 parameters, described to Claude as this PyTorch module and run in MLX with the same semantics
(checked against an explicit NumPy implementation: largest difference 7.6e-8):

```
Conv2d(1, 8, 5) → ReLU → MaxPool2d(2) → Conv2d(8, 16, 5) → ReLU → MaxPool2d(2) → Flatten → Linear(256, 10)
```

## Each step (`loop.py`)

1. Claude replies with one Python code block defining `build_weights()`, which returns all six parameter arrays.
2. `sandbox.py` runs it in a separate process where only numpy, scipy and math can be imported, and `open`,
   `exec`, `eval` and `compile` are removed. The weights must have the exact shapes and be finite.
3. The network is scored on the training set (sent to Claude) and the test set (stored only).
4. Claude receives this step's training loss, accuracy and 10×10 confusion matrix, a table of loss and accuracy
   for every step so far, and the number of steps left.

A step whose code fails, or whose reply has no code, still counts, and Claude is told the error.

## Conditions

| | a: numbers only | b: with images |
|---|---|---|
| Starting prompt | `prompts/task.md` | the same, plus 50 training images (5 per digit) as one image |
| After each step | loss, accuracy, confusion matrix, history | the same, plus 16 training images the network got wrong (chosen at random), each with its true label, prediction and top-3 probabilities |

The images are 4x enlarged, white ink on black, and sent as image blocks, never as data in the sandbox. In
condition b the rules add: look at the images to understand the data, but don't put them, or numbers copied from
them, in the code.

The original Go experiment also had a "positions pass" (the network's activations on chosen positions). There is no
equivalent here.

## Rules given to Claude

Only numpy, scipy and math. Filters and templates may be drawn from formulas or hand-described strokes. No
generating example inputs to compute weights from: no averaging over generated samples, gradient descent,
regression, least squares, clustering, discriminant analysis or search, including on synthetic data. Don't run the
network on inputs. The full text is in each run's `prompt.md`.

## Stopping and scoring

Up to 50 steps. After at least 15, a run stops once the best training loss has not improved by 1% over the last 8
steps. Claude is told only that it has up to 50 steps and that its lowest-training-loss network is scored on the
test set. The reported score is the test accuracy of that network.

## Model settings (`claude_client.py`)

`claude-opus-5-5` through the Messages API, effort `high`, adaptive thinking with summarised thinking returned,
`max_tokens` 128,000, streaming, no tools, no refusal fallback, the neutral system prompt "Answer the user's
request." One conversation per run, with the full history each step and automatic prompt caching.

## Runs

Three per condition: `a-1`, `a-2`, `a-3`, then `b-1`, `b-2`, `b-3`.

    uv run python loop.py --condition a --run-id a-1

## Baselines (`baselines.py`)

Adam (lr 1e-3, batch 64) on the 10,000 training images, three seeds, test accuracy at 0 to 5,000 steps. Random
search, a (1+1) evolution strategy with 50 training-set evaluations, five seeds.

## Changes after the first run

None yet.
