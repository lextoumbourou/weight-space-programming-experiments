I'm checking whether the gradient estimate is close to zero, which would put x1 near optimal, and that seems surprising given the attenuation, so I'm wondering whether the features are correlated. I'm also wondering whether a larger h would change the inference, so I'm going to try x1 at -0.3.

I'm weighing whether to probe x1 at -0.3 on both sides, which costs a step but would calibrate h for the other features too.
