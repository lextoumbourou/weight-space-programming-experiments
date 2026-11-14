I'm decoding three bits from the counts for position 0, working through sums and ratios against the 0.6 threshold.

Now I'm working through the remaining buckets' sums and ratios against the 0.6 threshold, checking each of the three bits.

Now I'm checking the bit sums for buckets 8 and 9 against the 0.6 threshold, and I've got the H(r0,L) ratios for the last few candidates.

Now I'm comparing the per-candidate ratios for the H(r0,L) and "\"(r3,L) bits, noting that 0 and 2 separate clearly on the second bit. I'm also checking the "/"(r3,R) ratios, where 0 and 3 sit near the top, and starting to work out the mean and spread against the threshold.

Now I'm computing the z-scores and adjusted means for the remaining bit-position thresholds, and working through the per-candidate values for the "/"(r3,R) bit.

I'm weighing whether to run one more probe (step 41) before building the classifier, since that adds three features but leaves fewer steps for tuning, and I'm leaning toward probing first.

I'm picking out candidate probe features for the remaining digit pairs, like H(r2,L), V(r3,L), and "/"(r0,R), to separate 7 from 9 and 3 from 5.

I'm checking which strokes separate candidates 2 and 3 from the rest, with the vertical centre-column probes as the next option to weigh.

I'm checking the centre-column vertical probe values for each digit, then weighing the candidate features: a bottom-left slash, an H(r2,L) probe, and a bottom-right vertical, though the bottom-right stroke looks only partially informative for most digits.

I'm picking a bottom-left slash, an H(r2,L) probe, and a vertical at row 3 on the left as the three features for probe 41.
