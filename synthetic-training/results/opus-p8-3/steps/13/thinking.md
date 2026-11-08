I'm estimating the effect size for a feature with a logistic coefficient, using a second-order approximation of the loss. The variance term is roughly 0.12, so I'm working out the covariance from the baseline loss.

Now I'm working through the per-feature covariances, converting each into a marginal logistic coefficient by dividing by p(1-p), and then checking whether combining them independently makes the total logit spread too large.
