# Cats vs dogs: LLM Descent on a harder problem

The [MNIST experiment](../mnist-training/) (its condition a, numbers only) on Kaggle Dogs vs. Cats photos at 64x64.
Fable 5.2 writes every one of the 24,898 weights of a small, fixed CNN, then improves them over up to 50 steps.
There is no gradient descent and no fitting: each step it gets back the training loss, accuracy and 2x2 confusion
matrix, and writes the whole network again. It never sees a photo.

Everything else matches MNIST: the sandbox (numpy, scipy and math only), the rules, the stopping rule (at least 15
steps, then stop once the best training loss hasn't improved by 1% over 8 steps, not told to Claude), and the score:
the lowest-training-loss network's accuracy on 5,000 test photos it never sees. Written up in
[Weight-Space Programming builds neural networks like a 1990s researcher](https://notesbylex.com/weight-space-programming-1990s.html) on Notes by Lex.

## Data

`train.zip` from the [Kaggle Dogs vs. Cats](https://www.kaggle.com/c/dogs-vs-cats) competition (25,000 labelled
photos, 12,500 per class), SHA-256 `736cdebc25d34b39b29947fc2fa94703483488e0b20db6f594388e28f1dc450b`. Each photo is
resized so its shorter side is 64 pixels (bilinear) and centre-cropped to 64x64 RGB. Balanced splits from a fixed
permutation (seed 2013):

| Split | Photos | Used for |
|---|---:|---|
| train | 10,000 | Claude's feedback, and the Adam and random-search baselines |
| test | 5,000 | the score; never shown to Claude |

The photos aren't redistributed here. Download them with a Kaggle account that has accepted the competition rules:

    kaggle competitions download dogs-vs-cats -f train.zip -p data/download

## Results

Test accuracy (5,000 test photos, never shown to Claude) of the lowest-training-loss network, from one Fable 5.2 run
on 18 November 2026:

| Run | Steps | Best step | Training loss | Test accuracy | Cost |
|---|---:|---:|---:|---:|---:|
| fable-1 | 17 | 9 | 0.656 | 61.6% | $8.08 |

Baselines on the same network and splits (`results/baselines/`):

| Method | Test accuracy |
|---|---:|
| Coin flip | 50% |
| Random search, 50 training-set evaluations (5 seeds) | 52.4 to 55.8% |
| Adam, 50 steps (3 seeds) | 50.0 to 52.0% |
| Adam, 500 steps | 54.6 to 55.9% |
| Adam, 5,000 steps | 73.3 to 74.2% |

Fable built detectors for pointed ears, an eyes-and-nose triangle, grass and more, then tested them one at a time.
The ear detector fired more often on dogs than cats (step 1). What worked were properties of the photo: green
(step 2), texture (step 4) and vertical-minus-horizontal edges (step 7). Its best network, step 9, uses only those
three. Nothing it added in the next eight steps beat it, so the stopping rule ended the run at step 17.

## Files

    data.py           the photos, the splits and their checksum
    network.py        the fixed CNN, in MLX with PyTorch weight layout, checked against a NumPy reference
    sandbox.py        runs Claude's build_weights() with only numpy, scipy and math
    claude_client.py  the Messages API conversation
    loop.py           the experiment
    prompts/          the task prompt and the feedback template
    baselines.py      Adam and random search
    results/<run>/    as in ../mnist-training

## Running it

Needs macOS on Apple silicon (MLX), [uv](https://docs.astral.sh/uv/) and an `ANTHROPIC_API_KEY`. Every run calls
a paid API.

    uv run python baselines.py
    uv run python loop.py --run-id fable-1 --model claude-fable-5-2
    uv run python loop.py --run-id plumbing --fake   # no API calls

The first version of this experiment (an earlier harness, one Opus 5.5 and one Fable 5.2 run) is in version control
at commit `e26658b`.
