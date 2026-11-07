A 76.7% jump with Naive Bayes on measured statistics suggests extending the measured features is the way forward, including stroke features. Probing those through binary-subset readouts looks too slow at three features per step, so I'm weighing a staircase readout instead, though that yields a distribution over a scalar rather than more features. I'm now wondering whether the known class label can speed up each probe step, since the readout's argmax only picks one of ten slots.

I'm weighing how to measure the stroke features: each probe step can only test about three binary features, so I'd need several steps just to get the marginals. Mutually exclusive slots might serve as a rough surrogate. Next I'm asking which stroke cues separate the remaining confusions, like a top horizontal for 7 (which it recalls only 49% of the time) and upper-left vertical strokes for telling 5 from 3.

I'm sketching out which stroke features to probe: a horizontal at the top and bottom, plus an upper-left vertical, each thresholded on its summed activation, with the threshold still to be chosen.

I'm settling on the thresholds for the stroke features, guessing a row sum around 0.8 since a real horizontal spanning three cells should reach about 2 while curve noise stays near 0.3 per cell. I'm also weighing whether a staircase readout first would show the scalar distribution, since Gaussian Naive Bayes would need per-class means and variances.

I'm picking the twelve most useful stroke features to measure over four probe steps. The top horizontal bar is first, since it separates 7 from the rest, followed by the bottom bar for 2 and the upper vertical strokes for telling 4, 5 and 6 apart.

Listing the remaining stroke probes: lower-left and lower-right verticals for separating 0, 6, 3, 5 and 8, a diagonal down-left for 7 and 2, a backslash in the top rows, a middle horizontal for the crossbars of 4 and 5, a center vertical for 1, 4 and 7, and lower-left ink.

I'm laying out the last stroke probes: a lower-left ink check, a lower-right ink check on the bottom row, and then a first readout step testing the top horizontal, bottom horizontal, and upper-left vertical, with the row-sum threshold set at 0.8.
