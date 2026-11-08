Pushing the parameters further, I'm setting a_pos to 1.45 and a_neg to 0.65. For the quadratic estimate, the variance of the |z| term works out to about 0.75, and with coefficient c=0.2 the cost comes to 0.003, so the total signal is 0.0071 and that gives cov(|z|,y) around 0.036.

I'm checking whether the convexity on the positive side means the logit rises faster for large positive z, which might point toward a threshold-style pattern. I'll test c=0.3 with a_pos 1.35 and a_neg 0.75 to see whether it helps, and keep the per-feature |x| terms in mind as a possible interaction.
