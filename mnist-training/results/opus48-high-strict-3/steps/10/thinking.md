I've recovered to 41.5%, so the baseline is clean and six steps remain. The biggest leftover confusion is 1 being read as 7, at 488, with 9 read as 4 close behind at 460. Recall on class 7 is down to 142, with a fair amount of its mass going to 9 and 5.

Next I'm checking the remaining confusion pairs (4→9, 4→8, 5→1, 5→6, 5→3, 3→5) and recomputing the column totals. Column 1 and column 8 run high, while columns 2, 5, and 7 run low. The two largest leaks, 1→7 and 9→4, are where the most gain is.

I'm weighing whether to adjust the "1" template so it fits real 1s better, or to pull the 7 template's center diagonal away from the vertical stroke. The idea is that a true 7 has its distinguishing mark in the top-right bar, and a 1 has no such bar, though a flag on the 1 may be mimicking one.

I'm weighing whether to boost the "1" template globally, but that would pull other digits into 1 as well, so the net effect may be negative. A better route seems to be lowering 7's weight in the lower-central columns, so a vertical 1 stops matching it, while keeping the top bar so real 7s still register.

I'm reshaping the 7 template so its lower stroke runs toward the left columns rather than the center, which would reduce its overlap with a vertical 1.

I'm considering a weaker version of the earlier anti-region fix, applied only to the top-left corner of the 4 template, to pull some of the 9→4 confusions away without losing the 4s I already have.

I'm weighing a gentler fix for the 9→4 leak: a weak negative weight on the top-left of the 4 template, so some 9s stop matching it without losing many real 4s. I'm also considering lowering the 4 bias, though that would cost some of the 4 recall I already have.

I'm weighing a modest tweak: lowering the 4 bias from -0.24 to -0.40 so some 9s stop tipping into 4, while accepting that a few real 4s could be lost. I'm also raising the 7 bias from 0.18 to 0.35 to recover some of its low recall, and I'm about to lower the 1 bias as well.

I'm lowering the 1 bias to cut its false positives, though that won't address the 1→7 leak. I'm also nudging the 8, 2, and 5 biases, and raising the 7 bias should help recover 7→9 and 7→5, at the cost of possibly letting more 1s slip into 7.

I'm weighing whether raising the 7 bias would help more than it hurts: it could recover true 7s now lost to 9 and 5, but it would also pull in borderline 1s that already leak into 7.

I'm settling on a set of conservative bias changes instead of chasing the 1→7 leak directly: raising 7 by 0.15, lowering 1 by 0.15 to trim its over-prediction, and lowering 4 by 0.15 to cut 9→4. I'll also nudge 8, 2, 5, and 9 slightly and measure the effect, since raising 7 could pull more borderline 1s into 7.

I'm weighing whether raising the 1 bias would recover some of the 488 ones that currently tip into 7, since 1 is under-recalled even though it is over-predicted overall. The over-prediction seems to come mostly from 5, 6, 7, and 8 leaking into 1, so a plain bias change would not separate those cases cleanly.

The 1s are the trouble here: 660 false positives into 1 from other digits, yet 488 real ones lost to 7. A bias change can't separate those cleanly. Rather than attempt a template tweak with the steps I have left, I'll make only conservative bias moves that look clearly beneficial and accept roughly 42%, avoiding regressions. The classes that look most over-predicted are 1, 8, and 4.

I'm making a modest rebalance of the biases: lowering 1, 8, and 4 since they're over-predicted, and raising 7 and 2 to even things out. I'm keeping the scale at 2 and expecting only a small gain, since bias changes can't cleanly separate the 1 and 7 cases.

I'm settling on a small rebalance of the biases instead of a structural change, since scale only affects loss and not accuracy. I'll lower the biases for 1, 8, and 4 where they're over-predicted, and raise 7 and 2 a little to even things out.

I'm settling the bias values: lowering 1, 4, and 8 where they're over-predicted, and raising 2. On 7, I'm torn, since raising it could recover some of its lost recall but may also pull in more borderline 1s.

I'm settling on the final bias vector: lowering 1, 4, and 8 a bit, raising 2 and 7 modestly, and nudging 5 and 9 up.
