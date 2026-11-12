I'm at 76.0% with a loss of 0.794, and downweighting ink seems to have helped, so I want to push that further, maybe to 0.3, and also try per-type weights for horizontal, vertical, and diagonal. I'm also thinking about bias recalibration and checking how the 8s are being predicted, then tallying the column sums.

I'm computing the column sums for classes 3 through 9, then the log-ratio adjustments for the 1.5 setting, which look like they nudge the class biases only slightly except for 8 and 1.
