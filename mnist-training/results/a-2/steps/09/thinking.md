Progress is at about 70%, with a handful of confusions left: 0 vs 2, 5 vs 6, several 3/5/8 and 2/8/3 mix-ups, and the spread of 8s. I'm starting with 0 versus 2. Two's template has a top arc, a diagonal, and a bottom horizontal, while a 0 carries a bottom curve that a 2 shouldn't have, and a 0 is tall. I'm wondering whether 2's template is simply too broad and covers the whole box, including the bottom horizontal.

I'm now weighing whether the parts-based features are adding noise, and considering a diagnostic that zeros out their weights to see how much they contribute. Separately, the 5-versus-6 confusion probably comes from the loop feature firing on 5s, since a 6 has a closed loop while a 5's bottom arc stays open on the left.

I'm weighing a part-only probe against an orientation-only one, to see whether the part detectors are actually discriminating. A quick idea is a loop-activity threshold per class to check whether the loop feature fires on 5s, though the argmax competition makes that harder to read.

I'm going to probe a single scalar: each class gets a line with slope j, and the argmax over those lines carves the scalar's range into bins, so the prediction reads off as a histogram per class.

Plotting one scalar against ten lines gives a bin-per-class histogram, so each probe reads one statistic at a time. I'm wondering whether two scalars could carve a finer grid, since argmax over affine functions only forms convex, Voronoi-like regions.

I'm considering a probe that uses two scalars at once, since placing points on a 3x3 lattice gives a grid partition, so the joint histogram per class would be more informative than a single scalar. Before building that, I'm asking whether it beats just adjusting the features directly, and I'm leaning toward trying it on the log-likelihood ratio between the two most confused classes.

I'm weighing whether the naive Bayes per-feature probabilities are well calibrated, since I can't measure the class-conditional feature means directly and have to rely on reasoning plus overall confusion feedback. Tuning the smoothing constant, the priors, and a few templates looks like the most useful use of the remaining steps.

I'm checking whether the part features are miscalibrated, and I'll try separately scaling their weights. Working through the column sums of the predicted counts, I'm recomputing the per-class totals against the true class sizes to see which classes are over- or under-predicted.

I'm running the column sums of the predicted counts again, comparing each class total to its true size, and adjusting the priors by the resulting offsets. Doing that correction on top of the parts ablation would mix the two effects, so I'd rather not.

I'm going to try lowering the part-feature weight to half, since if accuracy goes up that would mean the parts are hurting, and I'll also reapply the prior correction. I'm noticing the 1 template is too narrow, pulling in 4s, 6s, and 8s, so I want to check that next.

I'm noting that the 1 template's off-stroke features sit near zero, and the base probability of 0.08 applies equally to every digit, so that part looks fine.
