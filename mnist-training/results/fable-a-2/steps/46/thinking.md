I'm decoding three bits per index, each set when that row's value V for the given column exceeds 0.6. For index 0 with a total of 991, I'm summing the relevant entries: bit 1 comes out to 438 (0.442), bit 2 to 452 (0.456), and bit 3 to 333 (0.336).

Now I'm checking the remaining rows, working through the same three bit thresholds for index 1 and onward.

I'm running the same bit checks across rows 7 through 9: for row 7 the three bits come to 309, 697 and 895, row 8 gives 692, 879 and 952, and row 9 gives 428, 785 and 832.

Now I'm reading off the per-row values for the first bit, which runs from 0.89 for row 1 down to 0.28 for row 7. Then I'm doing the same ordering for the second and third bits, where the top-ranked rows sit near 0.98 and 0.99.

Now I'm working out the standardized z-scores and resulting means for each row's values, using the same threshold setup for the remaining rows of the third column.

I'm working out the remaining steps: a couple of probes and a classifier, with a possible bias retune at the end.

I'm weighing two plans: a classifier now with more new features, or a classifier at the end with a final bias tweak, and I'm leaning toward the first because the feature gains seem larger than a bias tweak would recover. The remaining risk is that a bug in the last classifier step could go unfixed, though the earlier classifier result would still stand. For the next probe I'm considering a few more features, including a couple of centre-column diagonals.

I'm picking the next probe as the centre-column backslash and slash diagonals for rows 1 and 2, since the centre-backslash results already show 8, 5 and 3 scoring high.

I'm now weighing the centre-column backslash diagonals for rows 1 and 2, plus a slash diagonal for row 2. The centre backslash already scores strongly on its own, so raising its weight could help, though that's untested.

I'm estimating thresholds for the centre-column backslash diagonals in rows 1 and 2, and a slash diagonal in row 2, using a per-row cutoff of about 0.6 for the backslash and roughly 0.9 for the slash.
