I'm fitting a parabola through three points of L(α), using the values at α = 0, 4 and 7 to solve for the coefficients, and I've already worked out c ≈ 0.0034 from the two reduced equations.

I'm working out the fit: the bias-corrected minimum lands at α = 5, giving L(5) ≈ 0.5415, a small improvement over 0.545 though the bias shifts muddy the picture. Tuning group weights only gives marginal gains, so I'm weighing options for a larger improvement, such as adding measured features or pair-specific discriminative corrections for the top confusable digit pairs.

I'm considering class-specific weight tweaks that push apart the 3 and 5 classes on the upper-left versus upper-right vertical feature, which could help in a linear model. Since these are perceptron-style updates driven by observed confusions, I'm wondering whether the tempering applied uniformly leaves the strongest features underweighted.

I'm weighing a few concrete options for a bigger gain: retuning the bias, adjusting the group weights (GLINE and GAMMA), and adding new features aimed at the top 3-vs-5 confusions, such as horizontal bar positions at the top of the digit.

I'm comparing the 3 and 5 classes on the upper-left and upper-right vertical features: the 5 scores high on the left and low on the right, while the 3 does the reverse. That separation should give roughly 11% error each way, which matches the observed confusion counts, so I'm looking for sharper features to cut it down.

I'm checking whether per-row versions of the vertical features would separate 3 from 5 more sharply, since the rows 0–1 sums blur the signal.

I'm comparing the per-row vertical features for the 3 and 5 classes, since the row sums may be blurring the separation, and I'm weighing whether to boost the class-specific weight difference on the upper-left versus upper-right feature for that pair.

I'm considering whether an LDA-style covariance with a shared "ink amount" factor would justify larger weights on the contrast between the upper-left and upper-right features, since those differences are more reliable than the independence assumption allows.

I'm now reasoning about why the linear model might over-weight ink amount: because the features share a common overall-energy factor, centering each class's weight vector along the all-ones direction could reduce that sensitivity. That could matter for 8, which has the highest means, possibly absorbing bolder 9s, 5s and 4s.

I'm working out a common-mode correction for the line features: subtracting the mean weight along the all-ones direction, scaled by a shrinkage factor κ, to cut sensitivity to overall ink amount, with the bias term adjusted to match.

I'm working out a common-mode correction: with a shared boldness factor across the line features, the implied covariance gives a shrinkage of about κ ≈ 0.85, which removes most of the shared component and amplifies the remaining contrasts by roughly 1.43. I'm wondering whether that matters in practice, since thick strokes may weaken the line response and bold digits could be pulled toward 8.

I'm considering a common-mode correction for the line features, assuming a shared stroke-boldness factor with ρ≈0.2, which gives a shrinkage κ≈0.77 and a contrast amplification of about 1.25. I'm thinking about testing it by applying the adjustment only to the line-stats group and setting GLINE to 0.5 to keep the overall magnitude similar, since bolder strokes may be pulling digits toward 8.

I'm setting up step 27 with α=5 and removing the common-mode component from the line-stat weights, using a shared-boldness correlation of ρ≈0.2. I expect the class biases to drift once that shift lands, so the result may need a bias retune before it can be judged fairly. I'll write the per-feature normalised weights next so the correction is concrete.

I'm setting up the common-mode correction in normalised z-space, where the within-class covariance is (1−ρ)I + ρ11ᵀ, so the inverse just subtracts a fraction c of the summed weights along the all-ones direction. I'm also folding in the bias term and the GLINE scaling, then centring the results across classes.

I'm settling the common-mode correction at ρ=0.2 over 13 line features, which gives a centring factor of about 0.059 and a shrinkage near 0.765. I'm setting GLINE to 0.5 so the contrasts land at roughly their previous effective size, and then I'll run it at α=5.
