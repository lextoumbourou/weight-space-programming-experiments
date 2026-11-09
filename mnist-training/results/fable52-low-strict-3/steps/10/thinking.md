The hole detectors are still barely firing, with the rows nearly the same as before. I suspect my assumption about the detector magnitudes is off, so the vertical-channel response may be smaller than I expected, maybe around 0.4 given the thick strokes and soft edges.

Since the hole detectors still barely fire, I'm questioning the magnitude assumption: if a typical stroke response is around 0.5, two sides sum to less than the threshold of 1.0, and no single threshold seems to work reliably. With six steps left, I'm considering shifting attention to the global parameters (gain, beta, and biases) and the per-class recall and prediction counts, where the payoff looks more certain.

I'm checking the per-class prediction counts against the true counts and finding that 4, 8, and 3 are over-predicted while 7, 9, 1, and 2 are under-predicted. I'm weighing bias tweaks to correct that, but earlier attempts with biases roughly cancelled out, so I'm thinking the gain would be small. I'd rather target the specific large confusions with features that have worked before.

I'm comparing 7 and 9 directly: the loop bottom of a 9 is a horizontal stroke near the middle that a 7 lacks, so I'm looking for a cell that separates them on that feature, since the earlier ink-cue attempt confounded it with a bias change.

I'm now looking at 7 versus 9 on the horizontal mid-stroke. The loop-bottom cue fires for 9 and 4 but is negative for 7, so it only helps the 9-to-7 direction, and a bias change would be the only lever for the other.

I'm working out the 9-versus-7 split with a mid-height horizontal cue: 9 and 4 get a positive weight on it, 7 a negative one, and each class gets a bias to match. The 9's loop bottom should sit around row 14, since its centroid pulls the stroke down into that band.

I'm settling on a horizontal mid-stroke cue for 9 and 4 with a negative weight for 7, using the sharp channel at rows 10-17 near the centre, since a 9's loop bottom and a 4's crossbar sit there while a 7 has no such stroke. The diagonal of a 7 should only leak weakly into that cue, and a few other digits have mid-height horizontals that I'll need to account for.

I'm settling on a horizontal mid-height cue for the classes that have a middle stroke, giving those classes a positive weight and a matching negative bias, and doing the reverse for 0, 1, and 7 so the 9-versus-7 and 6-versus-0 splits come from that cue.

I'm now setting up a sharp horizontal channel for the middle of the image, weighting it up for 3, 4, 5, 6 and 9 and down for 0, 1 and 7, so the 6-versus-0 and 7-versus-9 splits come from that one cue. For 8 I'll add a small positive weight with a slight negative bias, and I'm leaving 2 at zero.

I'm settling the horizontal mid-stroke cue across the middle band of columns, and I'm checking whether the 7's diagonal leaks enough to matter. I'm also weighing whether to drop the hole channels, but I'll leave them in for now since they're harmless and changing too much at once would muddy the results. Last, I'm starting to work out a moderate bias adjustment for class 4.

I'm settling the per-class bias changes: class 7 gets a little more positive, class 1 a small bump up, and class 8 a small push down. The horizontal mid-stroke cue will shift the balance for 3, 4, 5, 6 and 9 on its own, so I don't need extra bias adjustments for those.
