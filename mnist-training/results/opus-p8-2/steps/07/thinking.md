I'm at about 65% and calibration is helping, but the template quality is still the main structural weakness. Before doing more calibration, I want to find a stronger approach. The key idea seems to be that a linear classifier's optimal weights won't match the templates, since they should emphasize the regions that discriminate between classes. An LDA-style weighting, Σ⁻¹ applied to the class mean difference, could do that, and without data I'd have to approximate the covariance from a model of spatial smoothness and shift variability.

I'm weighing a manual route instead: pairwise features aimed at the main confusions, like 7 vs 9, 3 vs 5, and 4 vs 9, where the difference sits in specific template positions. I also suspect the templates are too blobby, since the wide halfwidth fills nearly every cell, so I'm questioning whether the thick dilated ink map is what's driving the cosine scores.

I'm weighing whether the dilation from the max-pooling is what makes the ink features so blobby, and whether I can undo it without losing the pooling. Since cosine scoring only uses nonnegative template weights, it can't actively penalize ink in the wrong places, so the negative evidence I need is only implicit, which points toward LDA-style weights of the form template minus the mean.

I'm reconsidering whether the centered weights actually matter: since only differences between classes drive the argmax, subtracting a shared mean changes nothing, so the real lever is the quality of the individual templates. The harder question is how to make them less blobby, since the thick dilated ink map may be what's limiting discrimination. Another option is to tune each class's template directly by watching how the confusion pattern shifts as I change one.

I'm thinking the template weights are the bottleneck, so I'm considering whether manually tuning each class's template against the confusion matrix could work, adjusting one class at a time and watching the effect. Before that, though, I want to check whether adding hole-detection features could help more, since holes separate several confusable pairs like 7 vs 9 and 5 vs 6.

I'm working through how to detect holes given the pooling. Max-pooling dilates the ink so "background" is almost always active near strokes, which makes a simple background channel useless. A better idea is to look for enclosed background: a cell where ink appears above, below, left and right at pooled distance, since that pattern marks a hole like the loops in 0, 6, 8 and 9.

I'm testing a simpler hole detector: a conv channel that fires only where a 3x3 patch is completely empty, since a sum of ink near zero there marks background. Pooling would spread that signal, so I'm checking whether a 3x3 empty patch is still a reliable marker for the small loops in 6, 8 and 9.

I'm settling on a hole detector for the pooled map: a conv1 channel that fires only where a 3x3 patch is essentially empty, scaled so anti-aliased edge pixels don't count as ink. Then in conv2, I'd combine that empty-patch signal at the center with ink in the four pooled directions, so that only a background cell with ink on all sides registers as a hole.

I'm checking whether a directional sum over several pooled cells would be a cleaner signal for ink on each side of a hole, since a thick stroke could make a single-cell sum too large, and I'm still weighing how to cap that.

I'm sizing a hole detector for the pooled map: a 3x3 empty patch at the center, with ink at one or two pooled cells out in each direction, scaled so loops of different sizes still register.

I'm sizing the hole detector against the pooled grid: a single pooled cell's stroke gives roughly 0.75 of ink per side, so a loop like the 9's upper hole would sum to about 1.5 across two offsets, while the wider hole in a 0 would only pick up one stroke at the nearer offset. A fixed threshold might not fit both, so I'm considering whether a few hole channels at different scales could cover the range, using the spare conv2 channels.

I'm sizing the hole detector against the pooled grid: a center cell that's empty, with ink in the directions around it. For a small loop, the summed ink across two offsets in each direction gives a large total, while a wider hole only picks up the nearer stroke, so the fixed threshold may need to be scaled differently for each.

I'm checking the hole detector's response across cases: a single stroke or a corner gives a moderate total, while the wider hole in a 0 only picks up the stroke at the farther offset. That suggests a second hole channel with offsets 2 and 3 so the larger loops register too.

I'm sizing a second, larger hole detector that only looks at offsets of two pooled cells, since the conv2 kernel can't reach farther. For the wider hole in a 0, the strokes sit at that distance, so the signal would come from the center's empty patch plus the ink at two cells out in each direction. I'm still deciding whether to subtract the nearer ink at one cell, since that would help separate the big hole from a small loop.

Writing the hole detector's first channel now: an empty-patch detector on conv1 with a bias and negative weights over the 3x3 window, then max-pooled so any empty position in each 2x2 block registers.

Writing the second hole channel's weights now: the center tap on the empty-patch map, ink taps at the four offsets with a larger negative bias, and I'm checking what the 0's interior gives against that threshold.

Now I'm working out the hole location in terms of the pooled grid: each 4x4 output position maps back to a band of input rows, so a 9's hole near row 9-10 would land in the first or second output row, while a 0's hole near row 14 would fall in the second or third.

I'm now assigning the hole channels to specific classes: a large hole for the 0, a small hole for the 6 and 9, and two small holes for the 8. I'm leaving out the 4 and 2 for now, since their loops don't reliably appear.

Now I'm weighing the hole channels' template values, scaling them up so they carry weight against the many ink features, and I'm settling on a value of 1.5 for them in the template.

Now I'm adding up the column sums for the bias update, working through each column's per-class counts.

Now I'm adding up the per-class column counts to nudge the biases, with the log ratios for each class coming out between roughly -0.43 and +0.47. I'm also noting that the new hole channels will likely push the 0, 6, 8 and 9 scores up, so the bias step has to be applied knowing that.

Next I'm wiring the small hole channel in conv2: the center tap on the empty-patch map gets weight 2, the eight ink taps at distance one and two in each direction get weight 1, and the bias is set to -6.8 so the channel only fires when the surrounding ink is strong.

Setting the second hole channel's weights: the center empty-patch tap at 2.0, ink at the two-cell offsets at 1.5 each, and a small negative weight on the nearer ink so a tight loop doesn't trip the large detector. The bias is -5.8, so I'll check what a 0's interior gives against that.

Now I'm setting the hole channels' template values: about 1.2 for the small detector and 1.0 for the large one, since they'll need weight against the many ink features. Then I'm placing the large hole for the 0 at the center, around row and column 14.

Next I'm setting the hole templates: a small hole for the 6 near row 14, column 18, two small holes for the 8 at columns 9 and 18.5, a small hole for the 9 at column 9.5, and no small hole for the 0.
