There are 891 rows in a binary Titanic-style dataset, roughly 549 died and 342 survived, with 13 features whose meanings are unknown. I'm starting with a near-zero network so the baseline loss sits around 0.666 with the bias set to the prior, then I'll probe each feature's correlation one per step, since I only have 50 steps for 13 features.

I'm settling on single-feature probes, one per step, using two ReLU units to pass a signed linear term. The gradient at the prior bias should show each feature's correlation sign, so a small weight of 0.5 on the sex-like feature should produce a clear loss drop.

I'm wrapping the probe as a general linear model, with the output logit taken as a rectified positive part minus a rectified negative part plus the bias, and I'll add feature interactions later. For this step I'm setting the weight to 0.5 on the first feature alone.
