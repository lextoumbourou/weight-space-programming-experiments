The last run of tweaks made things worse: class balance tipped hard, with 8 now underpredicted and 4 overpredicted. Nudging biases looks like chasing noise in a 10-dimensional space I can only probe through feedback. The real issue is probably how faithfully the templates capture each shape, so I'm turning to the feature representation itself, starting with a conv layer that uses 8 channels for orientations.

I'm checking whether the templates' Gaussian spread and saturation model actually match the stroke-to-bin response, and a stroke crossing a bin gives about 0.86A at the center, dropping to roughly 0.64A at 3px away and 0.25A just outside the bin, which looks reasonable. I'm now wondering whether the real problem is the variance of the features rather than their means.

Checking whether the MNIST-style nearest-centroid baseline, around 82%, sets a realistic ceiling here, since my 68% is well below it. I'm considering whether a discriminative weighting or per-feature variance could close the gap, and I'm weighing a 5x5 horizontal ridge kernel against MNIST's thick antialiased strokes.

Checking the thickness response of the horizontal ridge kernel: a stroke 5 pixels thick gives essentially zero output, and MNIST digits often have strokes that wide. That would weaken the features exactly where the digits are heaviest, so the detector may need a wider positive core.

Now I'm tuning the detector's kernel profile so it still responds to thick strokes: a positive center, mild positive shoulders, and negative flanks two rows out, which should keep uniform ink producing a useful signal.

Working out the kernel's response across thicknesses: a 3-pixel stroke gives the strongest signal, about 0.4 of max for uniform ink, and the response falls to roughly 0.4 for 5-pixel strokes too, so thick strokes stay detectable but lose orientation selectivity.

I'm thinking about whether edge-based features would hold up better, since a 5x5 ridge kernel goes nearly silent on the thickest strokes. Oriented gradient detectors respond to the two edges of a stroke no matter how wide it is, though covering all the orientations and polarities within the channel budget is the tricky part.

Settling on edge-based detectors: four orientations, each with two polarities, so the response to a stroke doesn't depend on how thick it is. Summing the two polarities in the second layer should give an orientation energy that tracks both sides of the stroke.

Working out the horizontal edge kernel: a derivative-of-Gaussian profile across the rows, smoothed along the columns, normalized so a clean step edge gives a response of 1.

Working out the diagonal edge kernels next, using a signed perpendicular distance profile normalized so the positive side sums to one, with the same mild negative bias on each polarity. Then I'll take the max absolute edge response over each block as the feature.

Edge detectors look like the better fix, since a stroke's two edges stay visible however thick the stroke gets. I still need to decide whether to restore the sharper orientation tuning from the earlier step, which gave the best accuracy, or keep the broader tuning that over-predicted the 4s.

Setting the rest of the edge detector design aside for now, I'm reusing the step-4 orientation correlations since they gave reasonable results, with a sharper cubed cosine tuning and a gamma of 5. The second layer will sum the two polarity channels for each orientation, so each channel reads both sides of a stroke at the same position.

I'm weighing whether to average the two edge polarities instead of summing them, which would keep the feature on a cleaner scale. I'm leaning toward the 0.5 weighting with a gain of about 0.6, though I'm not certain it's the right call.
