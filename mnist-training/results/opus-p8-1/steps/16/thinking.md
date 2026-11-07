I'm decoding the three bits to cells (0,3), (1,0), and (1,1), then tallying the class 0 counts per bit, where bit 0 comes to 382 (about 39%), and checking class 1's bit 0 sum, which is 26.

I'm tallying the per-bit counts for classes 2 through 9, with bit 0 for class 3 at about 21% and bit 2 at 58%, and I'm recording these probabilities in a table so I can use them later.

I'm tallying the per-class probabilities for each bit channel, and I'm now setting up the table of values for classes 0 through 9 so I can compare them.

I'm working out the per-bit probabilities for class 0 through class 9, and for class 0 the bit-0 share comes to about 0.038 while class 0's bit-1 share is around 0.327.

I'm moving on to the class 3 per-bit tallies and then class 4, where the bit-0 share comes out small. For class 5 I'm starting its counts.

Still tallying the class 8 and class 6 counts per bit channel, so I'm working through the cell sums for those.

I'm recomputing the bit-0 share for class 9 and then redoing class 0 with cell (0,3) included, where the bit-0 total is 382 (about 0.385), and bit-1 and bit-2 come out near 0.017 and 0.054.

I'm finishing the per-bit tallies for class 2 and class 3, and class 3's bit-0 share works out to about 0.215 with its bit-2 share near 0.58. I've just started class 4's counts, so I'll keep going with those.

Tallying the bit-0, bit-1 and bit-2 shares for classes 5, 6 and 7 from their cell counts, and I'm starting to work through class 7's totals.

I'm now checking class 8's per-bit counts, with bit 0 at about 0.47, bit 1 near 0.05 and bit 2 around 0.13. Class 9 follows, where bit 0 comes to roughly 0.31 and bit 2 to about 0.22.

I'm settling on three features per step, which means the remaining 58 features take about 20 more steps, so the work finishes near step 35 with a few steps to spare. I'm weighing whether a different encoding could pull in more features at once, but ternary splits only add levels to the same features, so I'll stick with the current approach.

I'm moving on to the H channel's remaining cells, 6, 7 and 8, to gather their per-class shares.
