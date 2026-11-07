We're at 49.32% with two steps left, so accuracy has leveled off. Next I want one more calibration by computing the predicted counts from the rows.

I'm checking the column sums against the matrix rows, and they add up to 10,000 in total.

Checking the per-row totals against the matrix now, with the largest over- and under-predictions still to be worked out.

I'm nudging the bias values for several classes: lifting the under-predicted ones and easing back the over-predicted ones, with a slight tweak to the two classes that are already close.

I'm settling the final bias values: pulling the two heavily over-predicted classes down to 0.4, raising the under-predicted ones, and nudging the rest a little. That leaves the confusion pattern as the next thing to think about, and this is step 14 of 15.
