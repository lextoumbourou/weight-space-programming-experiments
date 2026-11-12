The last run came out worse, at 0.7872, and the 4→9 confusion count went up to 119, so either removing that ink hurt or the cavity-unit misfires are to blame. I'm leaning toward reverting to step 38, or possibly 37, since they scored about the same. I'm now adding up the column sums from step 38 to recalibrate the biases, starting with column 0, which comes to 1007.

Still tallying the per-column sums, now for columns 1 through 9, and working out the small 1.3·log bias corrections for each; they come out near balanced, so I expect only a marginal gain.

I'm weighing the template weight against the structural term, and one option is to shrink the template part to about 0.9 so structure counts for more, since boosting structure has helped before. The other is to test a g_end of 3.0 on its own, which I haven't tried in isolation yet, so I'll run that alongside the bias tweak.
