Single-template matching looks capped at a level that's only marginal, so I need a different angle. I'm wondering whether the conv1 detector output is simply too noisy, or whether the 8x8 grid with heavy max pooling is discarding too much detail.

I'm checking whether the 8 and 2 classes are underpredicted and whether the 1 and 7 confusion comes from diagonal strokes matching the 7 template's stem. I'm considering broader orientation tuning and simple per-class bias adjustments based on the confusion counts.

I'm weighing bias adjustments per class to offset the 8 and 2 underprediction and the 1, 7, and 9 overprediction, which should be a cheap gain. But I'd rather find a structural change, and the main idea is conv2 kernels that act like part detectors, combining strokes across positions, or spatial blurring of the features to make them more shift-tolerant.

I'm wondering whether the real limit is my templates rather than the features: the 8 is drawn as two stacked circles, which doesn't match what a typical 8 looks like in this feature space. I'm considering blurring the templates more heavily, around sigma 2, and trying a wider range of shears so they sit closer to the actual class means.

I'm working through the feature distribution now, checking how a 45° line spreads its response across neighboring orientation channels and grid cells, with the kernel weights laid out row by row.

I'm working through how a 45° line spreads its response across the orientation channels, and the kernel weights come out to roughly 0.42 for the diagonal case versus 1.0 when aligned, so the 45° response is clearly weaker.

I'm checking the orientation response numerically: a 45° stroke gives about 0.27 of the aligned response, so a cos⁴ tuning curve would fit that. The 90° case is worse, since a vertical stroke still lands within the horizontal kernel's footprint and gives around 0.16, which means the detector isn't very selective and I need to see how a thicker stroke changes that.

I'm checking the orientation selectivity numerically: a vertical stroke still leaks into the horizontal kernel, so I'm weighing a higher bias or stronger negative flanks to sharpen it, though thicker strokes would reduce the gain.

I'm weighing whether to lower the bias and use a sharper cos⁴ orientation tuning, with stronger negative flanks, so the 90° leakage drops and the 45° response lands near 0.25.

I'm going to keep the blur at sigma 1.5 and the shears as they are, and skip the bias tweaks for now so the change stays easy to read. I'll make the kernel and the orientation tuning change together.
