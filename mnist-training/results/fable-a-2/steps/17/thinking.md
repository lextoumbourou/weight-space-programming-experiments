I'm decoding the indices from the triple and working out the lower-right vertical and bottom-centre horizontal sums for block 0, checking the probabilities against the thresholds.

Now I'm checking the probabilities for each block against the thresholds, with the lower-right vertical and bottom-centre horizontal sums.

I'm checking the block-8 bottom-centre horizontal values against the others and noting that the high-probability cases for blocks 4, 7 and 9 all sit on the right-centre vertical stems, with block 8 standing out as unusually low.

Now I'm working out the Gaussian fits for the lower-right vertical sums across blocks 1 through 9, getting a spread around 0.52 and the per-block means.

I'm fitting Gaussians to the horizontal bottom-centre sums as well, with a spread of 0.8 between the thresholds. Block 0 comes out near a mean of 1.3 with no tail, while block 4 sits much lower at about 0.45.

Now I'm fitting Gaussians to the bottom-centre sums and working out the per-block means, with block 0 and block 6 sitting near 1.3 and blocks 4 and 9 much lower.

Now I'm tallying the per-block mean values for the bottom-centre sums, which run through the stats for the line groups and the block-level fits.

I'm now weighing whether to bank the six line statistics in a classifier step or run more probes first. The remaining confusions are mostly 7 with 9, 2 with 3, and 2 with 8, and the new upper-right vertical statistic should separate 5 from 8 and 3, while the lower-left vertical and bottom-centre horizontal sums may help with 9 against 8 and 2 against 8.

I'm weighing whether to lock in the six line statistics with a classifier pass now or keep probing first, since 7 against 9 and 2 against 3 are still the main confusions. I'm planning to test a classifier that adds four new line stats to the previous setup, with horizontal middle and diagonal probes aimed at those pairs.
