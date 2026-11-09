The model sits at about 66% and stalls. Loss went up when I raised the gain, so I'll drop it back to 8 and try lower values later. The real problem is that the approach is linear template matching on hand-drawn features with no data behind it. I suspect the features don't line up with the templates, maybe because the response scales with orientation, but that's hard to check without seeing the data. I'm now turning to the line detector, where zero-mean filtering on thick strokes may be causing trouble.

I'm weighing whether to build part detectors into the convolution stage, such as loops, stroke ends, and curves, which would be more discriminative than orientation alone but harder to calibrate without data. I'm leaning toward keeping the current pipeline and refining the templates against the confusion matrix, starting with the largest error, 8 being read as 1.

I'm going through the confusion matrix errors, with 8 read as 1 as the largest. My guess is that a slanted 8 looks like a 1 because its crossing stroke resembles a slanted 1. Adding short horizontal negative strokes at the top and bottom of the 1 template might help separate them, since 8s, 2s, and 7s all have horizontal ink there.

I'm sketching a figure-eight template for the 8: a diagonal crossing with a top loop and a bottom loop, added alongside the ellipse version.

I'm tuning the 7 and 9 templates now, since both directions have large errors and bias alone won't fix that. The useful cues are the 9's upper-left vertical and the mid-left loop bottom, which the 7 lacks, so I'm considering a higher negative weight and a horizontal negative stroke for the 7 at the loop-bottom height.

I'm considering whether to keep the crossed 7 template at its current weight, since crossed 7s are rarer in MNIST, and I'm thinking about a negative stroke on the left half instead. I also want to check that the 9's centroid shift is handled by the centering step, which it appears to be. Finally, I'm weighing the 2 and 3 confusion: the 2 template already carries a negative for the lower-right vertical, and I need a matching cue on the 3 for its lower-left arc tip.

I'm adjusting the 3 template with a diagonal negative stroke in the lower left, since that's where the 2's stroke sits. For the 4 and 9 confusion, the key difference is the top horizontal arc, so I'd rather raise the 4's bias and lower the 9's than add a horizontal cue to the 9. The 0 confusions with 2 and 9 are odd, and I'll come back to the 2 template after that.

I'm wondering whether the 2 template is simply poor, since it gets confused with almost every class and my drawing of it may not match real 2s. Alternatively the normalisation could be the issue: raising the cross-class mean subtraction toward full centering, or using a stronger contrast of about 0.8, might sharpen the separation between classes.

I'm thinking about the 6 template next: it's weak, with only 585 samples, and it's getting confused with 4, 8, and 1. My current stem starts at the upper right and sweeps down the left, but many real 6s start more upright from the top center, so I'm considering moving the stem's starting point.

I'm now looking at the class counts: 1, 7, and 9 are being predicted far more often than the roughly 1000 true samples each, while 0, 5, 6, and 8 are under-predicted. That imbalance points to bias terms that need adjusting.

I'm nudging the per-class biases to counter the skew: raising 0, 4, 5 and especially 8, and lowering 1, 7 and 9. I'll also set the gain back to 8 and hold the 1 template's negative weight at its reduced value.
