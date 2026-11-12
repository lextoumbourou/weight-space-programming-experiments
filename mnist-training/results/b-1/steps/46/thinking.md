The last attempt made things worse, so I'm reverting to step 44, which is the best so far at 0.7768. For the remaining five steps, I'll try a small recalibration from the step-44 counts, since steps 43 and 44 pick the same argmax.

Next I'm checking the slope-35 values for each class, and class 2 and class 6 come out roughly flat. A lam_ori bump to 2.0 with a matching gscale and hs adjustment might add a bit of accuracy, though the gain is probably small.

I'm going with the lam 2.0 variant now, adjusting gscale and hs to compensate for the stronger lam_ori.
