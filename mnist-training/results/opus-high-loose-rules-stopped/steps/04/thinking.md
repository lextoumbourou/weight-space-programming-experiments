Sitting at 65% overall, with the 8 class doing the worst at 51%. It keeps getting confused with 2, 1, 6, and 9. My 8 template is basically two loops stacked, so once I subtract the mean it's left with little signal. Real 8s also tend to be slanted, with a crossing in the middle built from strong diagonals, while mine is two horizontal ellipses.

I'm settling on a better 8 template: two loops whose strokes cross diagonally at the center, rather than two stacked horizontal ellipses. I'm working out a vertical figure-8 curve, something like a lemniscate with its lobes stacked, to get that crossing.

Working out the vertical figure-8 curve: with a sine-of-2t horizontal offset and a cosine vertical term, the slope at the center comes out diagonal, so the two loops cross in an X. I'm also keeping the old two-ellipse version alongside it for comparison. Separately, I'm wondering whether an LDA-style weighting, with the covariance estimated from synthetic augmentations, could sharpen the class separation beyond plain centroid matching.

I'm checking whether synthetic covariance from augmented geometry could support LDA weights, but the scale of my stroke-length features doesn't obviously match the network's pooled activations, so the bias term may not transfer. Heavy ridge regularization or dropping the bias might keep it usable, though it's a risky bet.

Checking whether a uniform-direction nuisance term could be added to the covariance so the LDA weights stay stable against the scale mismatch with real network features.

Next I'm weighing a noise-robust version of the LDA weights, folding a nuisance direction into the covariance so the classifier ignores uniform offsets. I'm unsure how much to rescale the rows, since their relative magnitudes carry meaning. For now I'll fix the 8 template with the lemniscate-style crossing and add more slant variation to the synthetic set.

Now I'm setting up the covariance estimate: shrinking the within-class scatter toward a scaled identity and adding a uniform nuisance term, so the discriminant weights stay stable.

Now I'm sketching random variations of the synthetic 8s, such as slant, width, and shift, to build out the covariance estimate.

Now I'm adding random variation to the synthetic 8s: a slant, a width factor, and a small shift on each sample, plus a top-to-bottom width scaling. Then I'll compute class means and the pooled covariance, with a global-ink nuisance direction to keep the classifier stable.

I'm adding a nuisance term to the covariance: uniform directions over the whole image and over each half, with large weight, so the discriminant ignores those offsets. I'm also shrinking the covariance toward a scaled identity to keep the weights stable against the mismatch in feature scale. Then I'll normalize the weights and set the bias from the class means.

Keeping the bias at zero for now, since I can't match the synthetic feature scale to the real network's activations. I'm holding the scale at 1 for now so the comparison stays fair.
