I'm working out the decoding rule that maps the digit's bits to the combinations of UR, ML, and BR. For digit 0, I'm checking the sums for UR, ML, and BR from the listed values.

Now I'm working through the remaining digits, checking the UR, ML, and BR sums for each one.

Now I'm checking the UR, ML, and BR sums for digits 7 and 8, and starting on digit 9.

Now I'm finishing the BR check for digit 1 and wrapping up the per-digit scores, with the UR, ML, and BR summary table laid out for all ten digits.

Now I'm listing the measured features for all ten digits, covering the top, middle and bottom horizontal strokes and the upper-left vertical.

Now I'm tabulating the remaining per-digit feature values, the upper-right and middle-left and lower-right scores for each digit.

I'm weighing the two upper-right features against each other: the wider UR score separates digits 0 and 3 better, while the vertical-only urV separates 5 and 6 better. Since UR contains urV, using both double-counts the same cells, so I'm leaning toward keeping both at a reduced weight of 0.6 each.

I'm comparing the upper-right features for digits 5 and 3, since urV and UR overlap and counting both would double up the same cells. Working through the cases where UR is absent, the joint evidence favors 5 by about 1.7 nats, while adding the two features naively would overstate it by roughly 1.1.

I'm settling on weighting the two correlated upper-right features at 0.75 each, since using both at full weight overcounts by about a nat in the extremes. Now I'm checking whether the lower-left features overlap in the same way, since the middle-left score seems to sit inside the lower-left region.

Now I'm settling how the upper-left and lower-left features fit into the scoring, and whether the middle-left and lower-left overlap enough to need reduced weights.

Now I'm settling on a per-zone likelihood scale: about 2.0 for the four-cell zones, where a present cell reads as a moderate signal, and 2.5 for the five- and six-cell zones, keeping the earlier choice.

Now I'm settling on the per-zone likelihood scales for the remaining features: about 2.0 for the four-cell zones, 2.5 for the five- and six-cell zones, and a larger scale for the eight-cell zones, with a smaller one for the two-cell bottom-right zone.

Now I'm noting that the feature weights are overconfident: the large cell counts in the horizontal zones push strong-present evidence further than the probabilities justify, and that bias could skew the classes where the features are heavily weighted.

I'm settling on a reduced weight of 2.5 for the horizontal zones and 2.0 for the vertical ones, since the vertical stroke typically only covers about two cells in each of the two boxes it spans.

I'm settling the per-zone scales: 2.5 for the horizontal zones and the upper-left vertical, 2.2 for the upper-right and lower-right verticals, 2.0 for the two diagonals, 3.0 for the lower-left and upper-right combined features, 1.8 for the middle-left, and 1.2 for the bottom-right. I'm also down-weighting the correlated pairs, giving urV, UR, LL and ML 0.75 each and the weak cD1 0.6, with the rest at full weight.

I'm settling the remaining bias terms and the scoring scale: keeping the same offsets as before, with a possible small tweak for class 1, and lowering alpha to 0.6 because the extra features will make the model more overconfident. I expect accuracy in the mid-80s, and I'm not changing the scale yet.

Settling the step-14 values now: 2.5 for the horizontal and upper-left zones, 2.2 for the two narrower verticals, 2.0 for the diagonals, and 3.0 for the lower-left and upper-right combined features. I'm also checking the zone cell lists for the diagonal and combined features so they match what I probed.

I'm checking the bit-zone cell lists for the diagonal and combined features, and confirming the thresholds for ML and BR. For digit 0 versus 8, the diagonal cell is a strong separator, while the ML cells give the opposite evidence.

Now I'm writing the final code based on the per-zone scales and feature weights I settled, with the classifier structure I'm about to finalize.

Now I'm writing the code for the step-14 classifier: the feature weights and per-zone scales are settled, so I'm adding each feature with its weight and bias contribution.
