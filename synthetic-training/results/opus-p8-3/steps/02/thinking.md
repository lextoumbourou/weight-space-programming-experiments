I'm checking the class balance: 605 zeros and 395 ones, which gives a base-rate prior of about -0.426 in log-odds. A constant model would have a loss equal to the entropy at p=0.395, which works out to roughly 0.671.

I'm weighing whether to include the prior bias so the baseline sits at 0.6709, since the x0 probe's 0.7328 is hard to separate from the no-bias 0.693. The confusion counts show x0 is essentially irrelevant linearly, with the loss rise roughly matching the variance of the logits. I'm considering whether one-feature-at-a-time probes, with bias and a stronger scale, are worth the roughly 24 steps they'd take.

I'm sizing the step: with bias -0.426 the threshold sits at x > 0.426, and an uninformative feature at scale 1 would push the loss to about 0.79, so I'll use scale 1 with the bias included to get a clearer accuracy reading, probing one feature at a time since a single logit can't take two features at once.
