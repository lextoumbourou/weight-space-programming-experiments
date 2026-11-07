Bias shifts of about 0.5 had a large effect, which suggests the logits are small and the gaps between them are narrow, so the model looks underconfident. I'll reduce the bias adjustment to about a quarter of its size and raise β to 1.5, so the biases matter less relative to the scaled logits.

I'm working out how the bias adjustments should scale with β, since a 2.5× larger β would shrink the equivalent bias step. Comparing the column totals from the last two steps, the 8 and 4 columns overshot while the 6 column flipped too far, so I'm estimating target bias nudges for each column from those gaps.

I'm rescaling the step-4 bias adjustments by the β ratio, so the per-column nudges become about [-0.25, 0, 0, 0, 0.5, 0.25, -0.375, 0, 0.5, -0.125]. Raising β to 1.5 carries some risk of overconfidence, but I'll go with it.
