The loss went up a hair even though accuracy improved, so I'm weighing whether 0.45 for the ink setting is a fair compromise. Since loss is what I'm selecting on, I might also try scaling per orientation type. The diagonal type has only two offsets, so it may be getting too little weight, and bumping its λ to 1.5 could help, though I'm not sure. I also want to check the confidence on the errors, which have top probabilities around 0.3.

Trying a global temperature of 1.1 on top of ink 0.45, and I'm tallying the column sums for each class in the step-31 breakdown to see how the bias should be recalibrated.

I'm working through the per-class correction values, where a few classes shift noticeably while most stay close to zero. With the ink weight at 0.45, I'm going to scale the whole classifier by a temperature of 1.1, which means the bias terms get scaled along with the weights.
