The logits seem underconfident, since softening them raised the loss, so I'm going to sharpen the scale. Temperature 0.8 gave about 1.01 and T=1 gave about 0.92, so I'm trying T=1.6 on the step-7 scale with the new biases, since with 74% accuracy the optimum could be well above 1. The target is still getting under 0.9135.

I'm running the T=1.6 test now, aiming to get the loss under 0.9135 by step 12.
