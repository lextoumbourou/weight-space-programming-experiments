Step 27 landed at 0.5506 and 83.69%, roughly the same as step 24, so removing the common-mode component didn't move things much. The score seems to be stuck near 0.545, with 23 steps left, so I need a different lever to make real progress.

I'm weighing a few options to break the plateau, including adding finer-resolution measured features per row. I'm also considering targeted probes for the worst pairs, and the 0↔2 confusion, with 163 errors combined, looks like the biggest target given how many moderately separated features there are.

I'm still stuck on the 0↔2 confusion, where the features don't separate cleanly. Before going to a direct probe, I'm checking whether the template term or the class biases could explain it. Neither seems to, so the cause is probably a bimodal spread in the features themselves, such as slanted 0s whose arcs intrude into the centre.

I'm checking whether a closedness detector could separate 0s from 2s: a 0 has walls on both sides with an empty centre, but my left-right middle-row features are low for zeros, since the inner width is too wide for the current reach. Pinning the walls at exactly two cells on either side, at the edge columns of the 5x5 kernel, might give a detector matched to zeros.

I'm checking why zeros aren't picked up by the left-right wall features: their inner width is usually wider than the 5x5 kernel can reach, so only about 30% of them register. The remaining zeros have to be identified through the centre energy measures instead, since those are already in the feature set. I still need to figure out what makes 2s look like zeros in the other direction.

The pairwise confusion counts look lopsided in places: 2→3 is 103 against only 10 for 3→2, and 9→3 is 53 against 13 for 3→9. Some pairs, like 0↔2, are roughly symmetric, which points away from a simple per-class bias. I'll check the predicted-class column sums next to see whether any class is being favoured overall.

Now I'm working through the per-class prediction totals against the true counts, where digits 3 and 1 are over-predicted and 2 and 4 are under-predicted, and I'm considering small per-class bias shifts to offset that imbalance.

I'm going to treat the remaining 23 steps as a budget for more measurements, since the current feature set only uses about 25 region scalars against 160 available cell-level features. Per-class bias nudges might add around half a percent, but a larger gain probably needs more of the per-cell statistics, and I'll have to choose which cells are most informative.

I'm considering whether a smarter measurement could give me the class means of every cell in one channel at once, rather than probing one feature at a time. One idea is to look at which cell is the maximum, but that only gives how often each cell wins, not the means I need. A workable route is thresholded probes: checking how often each cell exceeds a threshold in each class, three cells per step, which would take about 21 steps to cover the 64 line-channel cells.

I'm wondering whether a different feature architecture would do better than finer region probes, since the current ones overlap the template cells anyway. The 4 smoothed line maps and the fixed 8 conv1 filters might be the real limit, so I'm considering whether a larger change there could beat incremental measurements.

I'm weighing a few ways to use the remaining steps: a quick per-class bias tune, some tuning of the gamma and line-weight settings, and a handful of probes aimed at the top confusion pairs with finer cells. I'll probably finish with a final scale adjustment.

I'm now comparing the 2-vs-3 pair on a few features: the bottom-left "/" response, the bottom-right horizontal response, and the left-right vertical response each separate them only moderately, while the bottom-row up-down feature separates them more strongly.

Now I'm looking at whether a single row of vertical-edge response in the lower-right could separate 2s from 3s, since a 3 has a right-side bowl there and a 2 mostly doesn't. I'd rather measure that one row than the whole quadrant, because the bottom row of a 2 would otherwise blur it. For the 3 vs 5 pair I'm weighing a similar narrow probe on the upper-left.

Next I'm checking vertical-edge responses in specific rows to split the confusing pairs: for 0 versus 2, a row-2 response on the right and a row-1 response on the left; for 5 versus 8, a row-1 response on the right and a row-2 response on the left; for 7 versus 9, a row-1 response on the left.

I'm narrowing in on four vertical-stroke probes in the middle band, one on each side of rows 1 and 2, since each separates a different confusing pair. Together they resemble the segment structure of a seven-segment display.

I'm settling on four vertical-stroke probes in the middle rows, one on each side of rows 1 and 2, since each separates a different confusing pair. I'm weighing whether a binary threshold near 0.6 fits these near-binary segment features better than three-level bins.

I'm settling on four vertical-stroke probes in the middle rows, one on each side of rows 1 and 2, and I'm checking whether a horizontal probe at the top-left would add a useful seven-segment-style cue for the 3 and 5 confusions.

I'm planning four vertical-stroke probes on the middle rows, one per side of rows 1 and 2, with a later step for the right side of row 2 and two horizontal checks at the top-right and bottom-left. I'd use a 0.6 threshold on these two-cell regions, then retune the bias in the final classifier step.
