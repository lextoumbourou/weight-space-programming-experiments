I'm decoding the first two digit-features from the three-digit codes and working out their ratios for class 0: f0 comes to 846 out of 991, about .854, f1 to 15, about .015, and f2 to 94, about .095. Class 1's counts are still on the list to be processed.

Now I'm working out the class 1 ratios, and class 2 through class 6 follow the same pattern with their per-feature totals and fractions.

Now I'm tallying the class 8 and class 9 features, which come to about .83 and .299 for f0 and then the remaining counts for class 9.

I'm checking the hole-upper values, which now look higher for classes 4, 3 and 5 than they did under the earlier threshold, since the lower corner bias makes the detector more permissive.

Now I'm reconsidering the hole features, since the unclipped sum is what's been driving them, and I want an absence-coded version that stays clipped to a sensible range.

I'm weighing whether to clip the upper-hole feature the same way: a linear form would only give partial credit for one or two corners, and taking a max over positions would pick the wrong extreme, so I'm keeping the hole features unclipped with their slopes.

I'm converting the hole-upper rates to log-odds, which gives about -2.25 for class 0, -1.81 for class 2, -1.09 for class 3, -0.76 for class 4, and -1.29 for class 5. Class 1 would hit the clip at -5, and classes 6 and 7 come out near -4 and -2.

I'm settling the upper-hole slopes from the new log-odds, shifted up so they sit on a comparable scale to the old ones and divided by a typical firing magnitude of about 0.8. That puts the strongest values on classes 8 and 9 near 3, class 4 around 1.9, and class 0 and class 7 close to zero.

I'm comparing the new hole-upper slopes against the old ones, where classes 4, 3, 5, 2 and 0 gain the most, and I'm noting that a shared constant shift changes nothing in the softmax, so only the relative differences matter.

Now I'm working out the lower-hole slopes from the same kind of log-odds, since the upper ones are now set.

Now I'm converting the lower-hole rates into slopes using the same log-odds shift, dividing by the typical firing magnitude, which puts class 8 and class 6 at the top and classes 3, 9 and 0 below zero.

Now I'm working out the lower-hole slopes with the same approach, since the upper-hole values are settled.

Now I'm writing out the hole-feature slopes, setting the upper and lower hole weights from the new rates and folding in the none-coded terms, and I'm settling HOLE_GAIN at 1.0 with GAMMA at 0.5. Next I'm starting the full measured classifier over all 32 orientation features, beginning with the k=0 hole rates for the first few feature pairs.

Still tabulating the hole-feature rates for the remaining orientation pairs...

Still tabulating the V-feature rates for the remaining orientation pairs...

Still tabulating the feature rates for the remaining orientation pairs...

Still tabulating the measured feature rates for the remaining orientation pairs...

Still tuning the trust factor for the 32 orientation features, weighing whether to lower the orientation gain to 0.4 and keep the corner gain at 0.6.

Next I'm dropping the hand-built templates so the classifier runs only on the measured weights, and I'm setting the orientation trust factor to 0.4 with the basic bias left at zero before writing the code.
