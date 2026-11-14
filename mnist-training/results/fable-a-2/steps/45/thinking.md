The scale search points to an optimum around 0.44 to 0.45, with a loss near 0.369, so the gain over the current setting is negligible and I'll keep the scale at about 0.44. With six steps left, I'll spend them on two probe cycles: probes plus a classifier at steps 45 to 47, then another set at 48 to 50, since each cycle so far has given no improvement.

I'm weighing two more probe cycles over the last few steps, since the group-weight tuning has unknown gains and the cycles have reliably cut the loss by about 0.02 each. The final step has to be a classifier, so I'll set up the 45–47 and 48–50 sets around that and use scale 0.44 with the bias adjusted to match. Next I'm picking which unmeasured features to probe, starting with the line features in the right and centre columns and the single-row splits of the loci features.

I'm now considering which centre-column line features to probe, since those give column-level detail that overlaps the left and right features. A vertical stroke at the centre row would be high for a 1, but a 0 has its walls in the outer columns, so it would read low there.

I'm now thinking about the centre-column vertical strokes, since a stroke at columns 1 and 2 looks different from one at the outer columns 0 and 3. That would separate a 0, whose walls sit at the periphery, from digits like 8 that have narrow centre loops. The same idea applies to the slanted and crossing features in the middle column, which could help with the 2 and 8 confusions.

I'm thinking the centre-column vertical strokes at rows 0 to 2 could be useful, along with a forward-slash at row 0 on the right, since those would help tell apart the 6, 4 and 1. I'm also considering outer-column-only features on rows 1 and 2, because a 0 puts its walls at the periphery. I want to understand why some 0s get read as 2s, so I'm wondering whether narrow, slanted 0s are the cause.

I'm weighing which features to probe in the last steps, and the confusions I'm worried about are 0 read as 2, 1 read as 2, and 7 against 9. A probe that could separate narrow or slanted zeros from twos would help most, but I'm not sure which feature does that. I'll use the two probes on the centre-column vertical strokes at rows 0 to 2, plus a forward-slash on the right at row 0 and a vertical on the right at row 3.

I'm going to hold off on the probe for step 46 until I see what the step 45 probe returns.
