I got 54% on the first try, so now I'm working on improving it. The main errors are 7 and 9 being mislabeled too often, plus 8 and 6 being overpredicted, with 2 often read as 8. I suspect digits with more ink, like 8, are scoring high simply because the feature magnitudes aren't normalized, and the templates themselves may be biasing things. I'm considering per-class biases, lowering them for 8, 6, 9, and 2 and raising them for 7, 4, and 5, and I'm also wondering whether a different structure than template minus mean would work better.

I'm weighing a norm term in the logit so that ink amount doesn't dominate the scores. For the 7 template, I'm considering a stronger central diagonal and a shorter top bar, since 7 is getting confused with 2 and 9. Since 7 is also under-predicted overall, a bias increase there looks like a reasonable fix, and feedback-driven bias adjustment is the direction I'm leaning toward.

I'm tallying the column sums of the confusion matrix to see which predicted classes are under- or over-represented. Column 7 is by far the smallest at 163, while column 8 is the largest at 2170, which fits the suspicion that 7 needs a bias boost and 8 needs a reduction. I'm about to check whether a bias shift alone is enough given the logit scale.

I'm now weighing a structural change to the templates rather than only per-class biases. The 8 template covers so many bins that its score grows with total ink, so I'm considering subtracting a penalty where a digit has no ink, which the mean subtraction only partly does. I'm also thinking about a more compact template representation.

I'm turning to per-class bias adjustments now, using the log ratio of each class's predicted count against roughly 1000, scaled by 1 in logit units. That gives large positive biases for 7 and fairly large ones for 4 and 5, with negative ones for 8, 6, and 9.

I'm estimating each class bias as minus the log of its predicted-count ratio, which puts big positive values on 7, 4, and 5 and negatives on 8, 6, and 9. I'm also wondering whether the logit scale should change, but I'll keep it as is for now.

I'm now adjusting the x scale to 8 so the digit widths better match typical MNIST proportions, and I'm also reworking the 7 stroke geometry with a longer, straighter stem and a shorter top bar.

I'm sticking with bias-only changes this round, leaving the templates alone so I can see their effect cleanly.

Setting the bias step to κ=0.8 to avoid overshooting, I'm now computing each class's log ratio of predicted count to true count. Class 7 comes out lowest at about -1.84, while class 8 sits near +0.80, which confirms the direction of the adjustment.

I'm converting the log ratios of predicted to true counts into per-class biases with a step of 0.8. Class 7 gets the largest boost at about +1.47, classes 4 and 5 get roughly +0.65 and +0.62, and class 8 is pulled down to about -0.64.
