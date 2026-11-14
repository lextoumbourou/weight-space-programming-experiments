I'm decoding bits for sample 0: bit 1 is the vertical right-side ratio in row 2 (0.772, above the 0.6 cutoff, so it's odd), bit 2 is the horizontal centre ratio in row 1 (0.22, below threshold), and bit 3 is the horizontal centre ratio in row 2 (0.06, also below).

Now I'm checking the remaining samples, going through their bit values against the thresholds.

I'm now going through the remaining samples: for sample 8, the vertical ratio is about 0.70 and the horizontal ratios are roughly 0.54 and 0.59, so that one is borderline. Sample 9 has the vertical ratio at about 0.96 and the row-1 centre ratio at about 0.66. Across the set, the vertical right-side ratio in row 2 is consistently high, so that bit looks like a weak signal.

I'm comparing the centre-bar ratios across the samples and noticing some sharp splits: sample 7 scores high in row 1 but low in row 2, while samples 2 and 3 separate clearly in row 1. Sample 4 also has a very strong row-2 centre ratio. Next I'm considering a Gaussian model with a spread of 0.35.

I'm working out a Gaussian-style estimate for the vertical right-side ratio in row 2, with each sample's z-score computed and converted to a mean, and I'm starting on the row-1 centre ratios as well.

I'm estimating the row-1 and row-2 centre-bar ratios for each sample under a Gaussian model, and I'm now setting up the classifier at step 30 by merging the earlier 13 lines with 6 new ones.

I'm settling on the classifier design for step 30: halving the quadrant weights where they overlap the row-and-column bars, dropping or down-weighting the centre cells that the finer row-level features already cover, and keeping the vertical centre at half weight. Each line-stat tuple gets an extra per-feature multiplier field, and I'm using independent Gaussians with GLINE at 0.6. The biases still need retuning from the base.

I'm adjusting the class biases from the step 24 column differences, nudging several samples up or down, and noting that the new features will shift the balance again. I'm setting the scale parameter alpha to 5.

Now I'm setting the scale to 0.5 for the extra features and writing the line-stats entries, each carrying a channel, row and column ranges, means, sigma and a multiplier.
