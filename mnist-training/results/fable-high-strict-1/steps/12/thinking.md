The loss dipped a little and accuracy barely moved. Digits 7 and 1 got better while 8, 6, 4 and 5 slipped, which makes me suspect the fixed γ=0.7 bias is penalizing the dense classes too hard, so the effective γ may be lower. Or the sparse classes 1, 7 and 3 are being over-predicted, and the column sums I'm looking at point that way.

I'm settling on γ = 0.55 and adjusting the per-class multipliers, scaling down the over-predicted sparse classes and nudging up the under-predicted dense ones. There are four steps left, so I'm also weighing a bigger change to the features, since the second conv channel set looks largely redundant with the first.

I'm weighing whether a saturation tweak, from 3 to 4, would make the templates capture more "amount" info, but I can't tell its effect and I'm hesitant since only four steps remain. The 8 confusions with 2, 3 and 7 are the ones I'm most concerned about.

I'm thinking the 8 template is off: its two loops have horizontal tangents at the waist, when a real 8 crosses there on a diagonal. The 8→7 confusion also fits, since a 7's top bar and descending stroke overlap the top of an 8.

I'm now tweaking the 6 template, which has its top stroke too shallow: real 6s start steeper and curve down the left side, so I'm reshaping that segment to run at roughly 60–70° rather than 45°, then finishing the loop at the bottom.

I'm checking the 4 template against the 9 next, since the 9's top loop might be what pulls 4 inputs toward it, even though the 4 has no top bar to offset that.

I'm weighing a small bump to λ, from 0.5 to 0.6, so the templates penalise missing parts more strongly and some subset confusions drop, though it may push superset errors up. I'm also turning to the 3 and 5 pair, which are confused in both directions, since the top of a 3 is a curve while a 5 has a bar and a vertical stroke, and the orientation features in the top-left cell may not separate them.

I'm comparing the 5 and 3 templates: the 5 has a left-side vertical near the top, which the 3's top arc lacks, but both have horizontal strokes across the upper cells, so the orientation features there may not separate them well.

I'm settling on the γ = 0.55 calibration and modest per-class multipliers, with the bulk of the gains coming from the 8 and 6 template shapes rather than big changes.
