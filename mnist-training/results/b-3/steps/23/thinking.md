Still at 72.9% with a loss of 0.887, which is the best so far. Next I'm weighing whether the loop weight on the 9 detector wrongly fires on closed 4s, and considering a negative loop weight for classes that never have loops. Then I'll move on to bias recalibration by checking the column sums.

Now I'm summing the column totals for each class, then computing the 0.85·log(true/pred) correction term per class to recalibrate the biases.

I'm now looking at whether negative loop weights for the non-loop classes would help, since those would only affect images with loops, mostly the 8s, 9s, 6s and 0s that get misread as 1, 3, 5 or 7. I'm also considering whether 4s that close at the top should get a slightly larger weight on their triangle loop.

I'm skipping the 9-position loop as a discriminator here, and I'm also considering raising the loop weights by about 1.25×, possibly alongside the negative weights and bias changes.
