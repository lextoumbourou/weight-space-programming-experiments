I'm checking the decoding rules for the first bit, the second bit, and the third bit against the sample values for entry 0, then adding up the values for each bit.

Now I'm working through the remaining entries, checking the bit-by-bit sums for each one.

Now I'm checking the bit-three sums for entries 8 and 9 and comparing the resulting values against the threshold, then ordering the entries by their r0,R scores.

Now I'm comparing the H(r1,L) and H(r1,R) scores across entries, listing which ones come out highest and lowest, and working out the z-scores for the first few entries against the 0.6 threshold.

Now I'm computing the z-scores for the H(r1,R) values and for the r0,R scores of the first entries, then converting them into the mean estimates.

Now I'm testing a few more candidate features for the remaining probe: one on the bottom-left of row two, one on the bottom-right, and one for the waist position, to tell apart the digits that still overlap.

I'm settling on three checks for this probe: the bottom-left stroke of row three, a vertical-and-diagonal split on the left, and the right side of row two, which should separate the digits that still overlap.
