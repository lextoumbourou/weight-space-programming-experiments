I'm not seeing improvement, and I suspect the feature design is the real problem: the presence features come from max-pooling a plus-shaped kernel, so they seem to fire on ink within a few pixels of each cell, which would make them too blurry to tell my templates apart.

Bias toward 1 keeps showing up, and it looks systematic: the real features seem weaker than my templates in most channels, so my templates are too "full" and everything reads as 1. I'm thinking about switching to a more linear feature, such as an averaged downsample of the ink, so the values are graded rather than saturated.

I'm now weighing a different route: rather than letting conv2 take a max over pooled ink, I'd use averaged pooling so the feature values reflect how much ink is in each region and stay graded instead of saturating. I'm also considering putting class-template-like weights directly into conv2, though each of its outputs only sees a local window, so the final layer would be combining local parts rather than whole-digit templates.

I'm going over how a 2x2 average over the first pooling layer would give graded values, and how stacking shifted taps could yield a finer effective grid of features.

I'm considering whether to just accept the feature design as-is and instead check the magnitudes against the templates directly. Computing the templates by simulating the network on my drawn digits would effectively run part of the network on inputs, so I'm ruling that out. I'm also setting aside a binarization idea, since it doesn't address the mismatch.

I'm now thinking the mismatch comes from the presence function: the soft box edges leave a faint response even several pixels away from a stroke, so the templates end up too full compared with the real features. A sharper edge and a max over stroke points would match the max-pooling behavior more closely.

I'm now sharpening the template model to match max-pooling: each feature should take the maximum over stroke points within a small window, with a tighter edge falloff. For the orientation channels, the 3x3 smoothing weights mean a stroke touching only one pooled cell contributes just a fraction of the full response.

I'm checking the orientation features next, and the smoothing is what's making them too weak: a stroke only reaches a fraction of the full response when it lands in one pooled cell, while my templates assume the full value. Removing the smoothing and using a single center tap should bring the orientation feature closer to the detector's peak response over the small window, so the two sides would match better.

I'm weighing whether the orientation features should use a plain distance-based template instead of centered cosine, since the cosine version came out weakest, and I'm considering a steeper falloff so off-angle strokes contribute a modest response instead of zero.

I'm settling on a distance-based template with a moderate scale of 0.5, since the gap between real and template features should stay small enough to avoid harsh logit errors. I'm also considering adding ink taps at the remaining offsets, so the ink channels cover the full 3x3 shift pattern, and I'll leave the last few orientation channels for now.

I'm checking that the template's coverage of the digit box lines up with the feature cells, so the presence features are compared fairly against the templates.

I'm settling the presence model: each feature should take the max over stroke points within about 2.5 px, with a sharper edge, since the real features are max-pooled. The orientation features get the same reach, and I'm dropping the smoothing so a stroke through the cell gets close to the full detector response.
