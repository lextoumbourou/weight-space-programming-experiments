Now I'm working out which columns are the big sinks: column 9 totals 3479 and looks much too heavy after the last adjustment, while column 8 is at 1400 mm. I'm thinking I should pull column 9 back down by about 0.8, which would take the 0.5 bump to roughly −0.3.

I'm now weighing the step 11 plan: dropping column 9's delta from +0.5 to about −0.3, since it's pulling in too many predictions, including the 842 from column 7 and the 468 from column 3. Column 0 is under-predicted, mostly sending its rows to 8 and 9, so I'm considering a +0.5 bump there, though lowering 8 to ease the 0-to-8 overlap might be needed.

I'm weighing whether to move column 9's delta down to about −0.3 and push column 7 up, since 9 is absorbing 8s, 7s, 0s, 3s and 4s. I'm also thinking of nudging column 0 up slightly and leaving column 8 as it is.

I'm weighing whether to set column 3's delta to about −0.1 instead of −0.4, since at −0.4 it dropped from around 2900 predictions to 467 and now looks under-predicted against its 1032 true rows.

I'm settling on column 3 at about −0.3 rather than −0.4, since interpolating between its 2900 predictions at zero and 467 at −0.4 puts the target near there. Next I'm turning to column 6, checking its prediction count at step 10.

Now I'm checking column 6's total against the earlier step, which came to about the same, so I'll leave its delta at −0.4. Column 5 is well under its true count, so I'm thinking about nudging its delta up by a few tenths.

Now I'm checking column 2, whose total of 625 falls well short of its 990 true rows, so I'm considering raising its delta by about 0.3. Column 0 looks under-recalled too, with only 254 predictions against 1000 true rows.

I'm settling column 8 at about −0.4, since it's taking 1400 predictions and a lot of the 0s, 2s and 6s, so pulling it down should free some of those back to column 0.

I'm now settling on column 9's delta at roughly +0.1, since going from 0 to +0.5 blew its predictions up from about 100 to 3479, so the target of around 1000 should sit near there.

Now I'm settling the per-column deltas: column 0 goes up, column 9 comes back down toward a middle value, and columns 2, 3, 5, 7 and 8 each get small adjustments to rebalance the predictions.

I'm nudging the per-column deltas again: column 0 up by about 0.4, column 9 down by roughly 0.4 to around +0.1, and columns 2, 3, 5, 7 and 8 adjusted in smaller steps to rebalance the predictions.
