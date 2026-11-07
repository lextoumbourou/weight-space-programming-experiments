The class counts are in: 1 is over-predicted at 1913, while 8 and 9 are under-predicted at 399 and 381 correct. The miss penalty hits the dense classes hardest and tends to favor class 1, which has the fewest expected cells, and sparse 1 is also where most of the errors pile up.

I'm working out how to offset class 1's over-prediction and the under-prediction in 8 and 9, since the miss penalty leans toward the sparse class. I'm considering normalizing per-class biases so each class starts from an equal ideal score, then adjusting manually from there.

I'm restarting the bias normalization from zero and considering a half-strength manual prior, since the previous offsets were tuned under a different scale. I'm also weighing whether lowering W_MISS to 0.07 would keep class 8's densest template from being penalized too heavily for ordinary variation.

I'm comparing the 3-versus-5 confusion at the top-left: a 3 input misses the top-left cells that a 5 template expects, so W_MISS penalizes it there. I'm also noting that the 3 leaves the upper-right empty, which the 5 template doesn't require.

I'm checking why 5 wins over 3 when their biases look close, since my 3 template should cover the upper-loop cells and the 5 should be penalized for the 3's right side. Maybe real 3s sit smaller or further left than my template, or my 5 template doesn't match real 5s well. For now I'll leave it there.

I'm turning to a cleaner formulation: each class's bias will be set to offset its ideal score, plus a manual correction, with the manual part held to half strength since the old offsets were tuned under a different scale. The common level doesn't matter, only the differences between classes do.

I'm setting the normalization assumptions: about 4 for ink response, 3 for orientation, and 1.5 for emptiness, and I'm starting to tally the ideal score per class. The manual corrections are next, and I'm keeping them small, roughly half-strength, with class 1 getting the largest downward nudge.

I'm settling on modest manual nudges: lowering class 1 and 7, raising 8, 6 and 9 a little. I'm also estimating the template sizes per class to check that the normalization won't swing the biases too far.

I'm estimating each class's ideal score from its template size, roughly 7.5 for class 1 and about 9.7 for class 8, with the emptiness reward adding a further term that favors sparse classes.

Comparing the 8→1 confusions against the structural gap between 1 and 8, the normalization shift looks right in direction but might overshoot, since those 8s are probably just thin or narrow ones.

I'm reducing W_MISS to 0.08 and going to let the normalization handle the rest, since 9's and 6's confusions look balanced enough for now.
