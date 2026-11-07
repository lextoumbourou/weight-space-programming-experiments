The model has plateaued around 82.5%, so the next step is changing the features themselves rather than tuning further. One idea is to keep the same orientations in channels 8-15 but shift them by half a cell diagonally, which would make the final 4x4 grid behave more like an 8x8 one.

I'm weighing whether the bottleneck is orientation resolution or spatial resolution. For telling 3 from 5 and 7 from 9, the cues are local, roughly 4 px-scale strokes at specific positions, so finer spatial sampling looks important. One option is to pack 4 orientations into 4 spatial sub-positions per cell, which would give an effective finer grid without changing the total feature count.

I'm now doubting the synthetic training data, since the classifier is probably the bottleneck rather than the features: a plain linear model on raw pixels reaches about 92%, while these features should do better on real data. The mismatch may come from the templates, especially how the max-pooled responses and the broad 5x5 orientation tuning differ from my cos(2Δ)² approximation.

I'm now considering whether thick strokes are the problem: a zero-mean ridge filter gives a weak response when a stroke fills its whole kernel width, which could zero out features for bold digits. A wider ridge profile or plain oriented edge detectors might handle that better.

I'm now considering signed edge detectors instead of ridge filters: eight directions at 45° steps, so each channel responds to one side of a stroke. That would hold up for thick digits, since any thick stroke still has edges on both sides, and it resembles HOG features, which are known to work well on MNIST. I'd need to rework the synthetic feature model so each stroke produces edge responses at its two boundaries with inward-pointing gradients.

I'm working out the edge filter for the new feature design: each stroke gives gradient edges on both sides, with the sign pointing inward, so the eight 45° channels each capture one side. For the 5x5 kernel, I'm using an oriented derivative-of-Gaussian profile along the gradient direction, with a Gaussian falloff along the stroke.

I'm settling the edge filter's normalization so a step edge gives a response of 1, with a small negative bias. Thin strokes should still work since the falloff stays tight, and I'm keeping the same broad and sharp channel structure to keep the change minimal.

I'm now tuning the synthetic feature model: each stroke point gets two edge responses, one on each side, with randomized half-widths so thick and thin strokes are both covered. I'm working out the directional weighting for each of the eight channels, and the falloff exponent that controls how sharply each channel responds to nearby orientations.

I'm checking how the derivative-of-Gaussian kernel should be built along each gradient direction, with the thickness effect on edge responses roughly acceptable at about 0.6 for narrow strokes. I'm also setting the gradient direction in image coordinates and writing the kernel weight as a directional derivative times a Gaussian falloff.

I'm reconsidering the bias terms: the old calibration was tied to the ridge features and won't hold for edge detectors. Resetting them to zero for now seems sensible, with recalibration to follow once the new feature set is in place. The idea is to keep the rest of the pipeline mostly unchanged, accepting that the biases are temporarily off.

I'm writing the feature function so it takes edge points and gradient angles as inputs, and I'm also varying stroke half-width randomly between about 0.7 and 1.8 so thick and thin strokes both show up in training. The edge position shift of up to 2 px is small, but it still needs to be modeled correctly.
