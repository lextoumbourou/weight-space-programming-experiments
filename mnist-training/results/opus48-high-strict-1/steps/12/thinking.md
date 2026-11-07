The new 4 template pushed the score past 40%, with 9 recall jumping to 685. But 4 recall fell to 231, and true 4s are now often predicted as 9, so the new template seems to be matching 4s poorly.

Still designing the thicker 4 template...

Still refining the 4 template, keeping its strokes thick enough to match real 4s while leaving the upper-left open so it stays distinct from 9.

Now I'm working out the bias adjustment, since 9 is being over-predicted while 4 is under-recalled. Then I'm tallying the per-column marginals for step 11.

Now I'm tallying the per-column totals, and the 9 column is far over the rest at 1826 while 4 sits at only 388. So I'll lower the 9 bias and raise the 4 bias.

Now I'm recomputing the bias terms from the step-11 marginals, starting with the first few columns: column 0 comes out around 1.93, column 1 near -1.48, and column 2 near 0.33.

Now I'm settling the bias for the remaining columns: column 4 gets -1.1, since the thicker template should recover its recall without over-boosting it. Columns 5 through 8 come out near 1.9, 1.0, 1.8, and 1.6, while column 9 is pulled down hard to about -1.5 because it dominates the predictions.

Bias values are settling: column 4 is getting a moderate raise, and the 9 bias is being pulled down hard. I'm worried that lifting 4 too far alongside the thicker template could bring back the 9-for-4 confusion, so I'm going moderate and landing on 4 at -1.3 and 9 at -1.5.

Thinking the 4 template through, I'm weighing thicker strokes so real 4s match better while keeping the upper-left open to separate it from 9. The 9 bias is clearly too high at 1826, and 4 is badly under-recalled, so I'm lowering 9 and raising 4 moderately. I need to watch 1/7 confusion and the 5 attractor in the remaining steps.
