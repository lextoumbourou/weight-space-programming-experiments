I'm checking the bit conditions for this tuple: b1 sums the odd-indexed items to 740 for a ratio of about .747, b2 sums the items at positions 2, 3, 6, and 7 to 227 for about .229, and b3 comes out to 902.

Now I'm going through the remaining tuples, computing the b1, b2, and b3 ratios for each one.

Now I'm finishing the ratios for tuples 7 through 9, and the b1 counts for tuples 0 through 9 show which ones lead on the odd-indexed check.

I'm reading off the row-2 left-bracket ratios next, where 9 comes out highest at .79 and 7 lowest at .075, which helps separate those two. The remaining numbers are the row-0 right-bracket values, with 4 and 1 showing the lowest readings and 3 the highest of the low ones.

Now I'm working out the z-scores and the resulting μ values for the first two ratio tests, and starting on the H(r0,R) z-scores.

I'm applying the classifier update for step 36: the six new terms replace the overlapping V quadrants for rows 0 and 1, so their multipliers go to zero, while the lower-left quadrant stays at zero since row 3 on the left isn't measured.

I'm settling the multipliers for the overlapping classifier terms: the vertical and horizontal quadrants are either fully replaced or partly overlapping, so I'm lowering the centre "\" and "/" weights since single-row terms now cover those cells.

I'm settling the fixed weights for the overlapping terms, with the "/" centre and the lower-left quadrant kept at 0.5. I'll use a scale of 0.42 for now, since the earlier trend kept improving but I don't yet know where it peaks. The class biases are also adjusted from step 33, so I'm writing the classifier next.
