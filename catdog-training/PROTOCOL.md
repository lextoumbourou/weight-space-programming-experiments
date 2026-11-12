# Protocol

Fixed on 8 November 2026, before any paid run. Same design as `../mnist-training/` (its final rule), on a harder task.

## Question

Can an LLM train a small cats-vs-dogs CNN without gradients, by writing all of its weights and improving them from
loss, accuracy and a confusion matrix on a labelled set of photos it never sees?

## Data

Kaggle Dogs vs. Cats (2013), `train.zip` (25,000 labelled photos, 12,500 per class), SHA-256
`736cdebc25d34b39b29947fc2fa94703483488e0b20db6f594388e28f1dc450b`. Each photo is resized so its shorter side is 64
pixels (bilinear) and centre-cropped to 64x64 RGB, pixels divided by 255. Balanced splits from a fixed permutation
(seed 2013):

| Split | Images | Used for |
|---|---:|---|
| train | 10,000 | gradient-descent baselines only |
| val | 10,000 | the feedback the LLM sees, functionally its training set |
| test | 5,000 | the score; never shown to the LLM |

## Network

Fixed, 24,898 parameters (`network.py`), checked against an explicit NumPy implementation of PyTorch semantics:

```
Conv2d(3,16,5) → ReLU → MaxPool2d(2) → Conv2d(16,32,5) → ReLU → MaxPool2d(2) → Conv2d(32,32,3) → ReLU → MaxPool2d(2)
→ Flatten → Linear(800, 2)
```

## Conditions

As the final MNIST rule: `claude-opus-5-5`, effort `high`, adaptive thinking with summaries, 128,000 output tokens,
Messages API, full history each step, no tools. Up to 50 steps; at least 15; after that, stop once the best feedback
loss has not improved by at least 1% over the last 8 steps. The model is told only "up to 50 steps" and that the
lowest-loss network is scored, which is also the reported score. Three runs. The prompt is `prompts/task.md`; the rules
match MNIST's (numpy and math only, no generated examples or fitting, no running the network).

## Changes after fixing the protocol

None yet.
