I'm at 87.44% with loss 0.422 and 14 steps left, planned as two more probe-and-classifier cycles followed by tuning. I'm wondering whether more probe cycles would beat spending those steps on tuning, since each cycle's gains are shrinking (−0.046, then −0.034).

I'm weighing two more probe cycles plus eight tuning steps against three cycles plus five tuning, and I'll decide on that later. I'm also running through the current error pairs and column balance, noting a few small weight tweaks to even things out. Next I'm listing the unmeasured single-row candidate features across the horizontal, vertical, and diagonal patterns.

I'm trying to tell apart the 7↔9 confusions, which are still stubborn at 59 for 9→7. I'm considering a few candidate features: H(r2,L) and V(r1,C), though I'm not sure either separates the hard cases cleanly.

I'm checking which single-row features might split the 3↔5 pair, since a left-side feature at row 1 looks like it would favour 5 and a right-side one at the same row would favour 3. The 1→2 and 2→3 confusions I'll come back to, with a base-stroke feature at row 3 on the left as a possible separator.

I'm now weighing the remaining 4↔9 split against the top-closure features: one candidate is a stroke at row 0 curving up-right, which should appear in 9, 0, 2, 3, 8 and the corner of 7 but not in 4, 1, 5 or 6, and a mirrored one at row 0 curving up-left.

I'm settling on three probes for this round: two horizontal bar features on row 1 (left and right) and a backslash-shaped stroke at the top-right, aimed at separating 3 from 5 and 4 from 9.
