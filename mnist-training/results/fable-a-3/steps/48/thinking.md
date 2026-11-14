I'm checking the sH=0.18 run, which hit the best loss of 0.2703 and 91.82% accuracy, against the other sH points. I'm fitting a quadratic to the three losses to look at the slope and curvature between them.

I'm working out the minimum from the quadratic fit, which puts it near 0.2, so 0.18 is close to optimal for loss. I have three steps left and I'm weighing a combined bias and temperature change at step 48, since the smaller logit scale after the recent reductions may mean the temperature needs to go up.

Now I'm computing the per-class bias corrections from the step 47 column sums, taking 1.2 times the log of the true-to-predicted ratio for each digit.

I'm raising the temperature from 1.1 to 1.25 while the bias corrections are being set.
