I'm checking the class split, 605 versus 395, and noting that x0 barely beats chance. I'm working out the baseline loss from the prior, which comes to about 0.671, and wondering whether a random feature with coefficient 1 would push the loss up to around 0.82.

I'm weighing whether a bias term plus probing features one at a time is worth it, since the loss doesn't split additively. A small coefficient on x1 with the bias included might be a cleaner test, with the uninformative baseline sitting near 0.79.
