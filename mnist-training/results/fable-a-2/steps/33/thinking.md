I'm decoding the three bit rules against the values for input 0, summing the relevant registers to get each bit's result. I've started on b1 and b2 and am now adding up the terms for b3.

I'm working through the remaining rows, checking the b1, b2 and b3 sums for inputs 1 through 6.

I'm checking the b1, b2 and b3 sums for inputs 7 through 9, and I'm comparing the sums and ratios for input 8 against the earlier rows.

I'm now comparing the b1 values against the earlier rows, and the sharpest gaps show up for inputs 9, 8, 3 and 5. For b2 the lowest scores are at inputs 5, 1 and 3, while the rest sit high. For b3 the low values are at inputs 1, 2, 8 and 7, and the top ones at 0, 9 and 6.

I'm working out the z-scores and scaled values for the first two bit rules across the inputs, noting where the values come out lowest.

I'm now running the classifier's 33rd step, folding in six new single-row features and adjusting the overlapping terms from earlier rows.

I'm fixing the classifier's scale down to 0.45 since the term count rose, and I'm planning to tune it later. I'm also carrying over the per-column bias adjustments from step 30 and noting that the new features will shift the balances.

I'm checking how the bias terms interact with the scale change, since the feature-driven balance moves with SCALE while the class biases stay fixed, and I'll write step 33 next.
