I'm working through the bit-pattern decoding for the 0 (991) row, checking the b1 sum of 83, 23, 26 and 16 against the odd-position condition. I'm also running the b2 and b3 sums over their respective index sets.

Now I'm checking the b1, b2 and b3 sums for the 1064 row, and then for the 990, 1030, 983, 915 and 967 rows.

Now I'm checking the b1, b2 and b3 sums for the 7, 8 and 9 rows.

I'm now comparing the r1 and r2 scores across the ten rows, and the r2 scores for rows 7 and 9 stand out sharply (.078 against .69), as do rows 0 and 2 (.09 against .435). I'm also listing the "/" r2 scores above .9 with their values.

Now I'm computing the mu values for the r1 and r2 scores from their z-values.

Now I'm converting those z-scores into mu values for the r1, r2 and "/" r2 scores, and I'm marking the centre-row overlaps to drop from the classifier step.

I'm working out the classifier scale factor, giving the new centre terms a 0.7 multiplier to avoid double-counting the overlapping cells, and applying the 0.44 scale to the class biases.

I'm setting the class biases on the 0.40 scale, with values like 0.66 for class 0 and 1.17 for class 4. I'll run two probes next, then the final classifier.
