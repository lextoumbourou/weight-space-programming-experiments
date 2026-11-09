I'm comparing step 14 with step 13, which come out almost equal at 78.65 and 78.66. The anti-stroke pair between 2 and 8 has shifted: 2 dropped from 646 to 572 and 8 rose from 688 to 785, so the net for that pair is about +23 along with the small bonus for 8. Other values are moving too, with 0 going from 869 to 856 and 4 from 774 to 787.

I'm now weighing whether to drop the bonus on 8, since it appears to be pushing up the 5, 6, 0 and 3 pairs with 8 while lifting 8's own score. The 2-vs-8 anti-stroke shift looks mixed: 2 is being penalized and 8 is gaining, so keeping the 2 penalty and removing the 8 bonus may be the safest combination.

I'm checking the bias adjustments: lowering the 0 bias cuts 13 correct 0s but removes about 31 false ones, a net gain of roughly 18, so I'll keep it. The 4 bias raises correct 4s by 13 while costing about 11 false ones, so I'll keep that too.

I'm weighing whether dropping the 8 bonus is worth it, and whether to soften the 2 anti-stroke penalty to −0.15 as well. The estimates suggest removing the bonus roughly cancels the anti-stroke shift between 2 and 8, so the net effect of that penalty alone looks close to neutral.

I'm tallying the predicted-2 counts from non-2 classes in steps 13 and 14, which sum to 279 and 150 respectively, to see how much the anti-stroke penalty for 2 really changes the errors that flow into class 2.

I'm working out that dropping the anti-stroke penalty for class 2 would account for most of the false 2s disappearing, roughly 140 of them, which outweighs the roughly 55 true 2s lost. I'm also considering the 8 bonus as a separate factor in the same comparison.

I'm trying to reconcile the estimated effects: removing the 2 anti-stroke penalty looks like a net gain of about +85, the 8 bonus about −70, and the bias tweaks roughly +20, which doesn't match the observed net of about −1. I'll recount the total correct counts for steps 13 and 14 to find where the arithmetic is off.

I'm checking the per-class deltas: 8 gained 97 and 4 and 3 gained a little, while 2, 5, 6 and 0 lost, netting to about −1. The false 2s that disappeared mostly reappeared as correct 8s and 4s, though the total gains in other classes don't account for all 140 of them, so the picture is only roughly consistent.

I'm working through the bias-versus-bonus trade-off: the 8 bonus seems to account for most of the false 8s that appeared, while the anti-stroke penalty on 2 looks like it's doing the useful work. Removing the 8 bonus while keeping the 2 penalty should bring the net back up by roughly 57 correct predictions.

I'm working out what removing the 8 bonus would be worth: it seems to cost about 78 correct 5s, 6s, 0s and 3s by pushing them toward 8, and to gain only around 47 among the 8s, with a few more lost to 2s. That puts the net gain of dropping it at roughly +46.

I'm settling on removing the 8 bonus while keeping the anti-stroke penalty for 2, and I'm considering a small increase to the 2 bias to offset the 2s it's now losing.

I'm considering raising the bias on class 2 by 0.15, to 0.75, since it's the most under-predicted class: 711 predictions against 990 true instances, with roughly 80% precision and 58% recall. I expect that to help more than it hurts. I'm also checking the predicted totals for the other classes to see whether any of them look similarly skewed.

I'm settling the bias tweaks now: lowering the 0 bias further to −0.35, leaving the 8 bias alone, and raising the 6 bias to 0.4 since 6 is under-predicted compared with its true count.

I'm dropping the bonus on class 8 and keeping the anti-stroke penalty on class 2, since removing the bonus should net roughly +46 correct predictions. I'm also nudging the class 2 bias up to 0.75 because it's the most under-predicted class, and lowering the class 0 bias to −0.35.
