Now I'm working out the outcome codes for the L-end, where 0 is none and 1 through 8 map to pairs of values, with 9 meaning column 2 is strongest. For class 0, most cases (951 of 991, about 96%) have no outcome, and the rest are spread across the other codes with column 2 appearing 13 times. Class 1 is similar: 1015 of 1064 have none, with a handful of 0s, 9s and 2s.

Now I'm going through the remaining classes, checking how often each outcome code shows up and how the "none" and column 2 counts compare.

Now I'm tallying the remaining classes, 7 through 9, noting that the "none" outcome dominates in most of them, with class 7 the exception where the (0,0) and (1,0) codes take a larger share.

Now I'm reading the L-end presence rates across classes: class 3 at 91%, class 2 at 63%, class 7 at 62%, and class 5 at 59%, against much lower rates for the others. That gives strong separation, such as 3 versus 8 and 9 versus 3. The catch is that the per-cell rates are mutually exclusive categories, so I'm weighing whether the aggregated "any L-end" feature should carry the naive Bayes model instead.

I'm checking that the per-cell weights work out for a categorical feature, since exactly one cell or "none" fires, so the log-likelihood stays linear in the indicators. If two cells fire, as with class 3's two ends, both simply add their evidence. The weights come from log ratios of each cell's rate to the "none" rate, with the bias set to the log of the "none" rate and smoothing applied.

Next I'm setting up the R-end chain: eight cells across columns 2 and 3, with outcome 9 covering column 1 as a whole. After that the plan is the D-ends, then the U-left step, and the classifier.
