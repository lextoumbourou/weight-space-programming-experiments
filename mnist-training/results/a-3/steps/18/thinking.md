Working out the loss for a true class c: the logit gap between class 9 and class c, scaled by a and S, comes out to roughly the average loss of about 2824. The value S is far above 120 for nearly every case, much larger than I expected.

I'm averaging the loss over the classes: the mean of (9−c) comes to 4.5, and the cumulative thresholds above each class sum to about 375.5 on average. Solving 2824 = 5(4.5·S̄ − 375.5) gives S̄ ≈ 209–210, so the 1s probably sit lower, around 130–150. That puts the mean feature value near 0.82 across all 256 features, which suggests most features are active with fairly large values.

Since the features are dense rather than sparse, a bias in conv2 might help: subtracting a baseline like b2 = -1.0 would suppress weak edge responses from neighboring cells before the max-pool. I'm not sure of the distribution, though, so I'm considering whether another probe is worth running first.

I'm thinking about running a finer probe on the per-class mean S, with thresholds spread between 130 and 320. Then I'm considering a more direct fix instead: a negative bias on conv2, around -0.8, to drop the weak edge responses and keep only the strong ones.

I'm settling on a negative bias for conv2, around -0.8, and I'll keep the step-15 config with s_feat at 1.0 since the features should now be weaker. I'll also use half of the step-15 correction, since the calibration will shift after the bias change.
