The 0.6760 loss is worse than the 0.6561 baseline, so adding VH_m and VH_c seems to have hurt. I suspect I picked the wrong root for σ, so I'm checking the other roots: σ_m comes out to 0.172 and σ_c to 0.212. Now I'm working out the fine-grained V case.

I'm checking the other root for the fine VH case, which gives 0.249, and wondering whether the small root still explains the S9 gain with w=3.5. The Gaussian equal-variance model seems unable to fit both the confusion-matrix d' and the loss, so I suspect heavy tails, where outliers break the quadratic approximation. For the coarse feature, the larger root 0.212 with w=1.7 would cost about 0.016 in variance against a gain of roughly 0.025, which looks like a net benefit on its own.

Checking the individual probe at w=2 with σ=0.212 gives a small net gain of about -0.007, so the coarse term looked fine on its own. Combined with the others, it may be largely redundant, and correlated features add variance: if the three VH terms are strongly correlated, their weights effectively stack, pushing the total weight too high.

Working through the overshoot: if the three VH terms are strongly correlated, the larger roots give a combined weight of about 1.6 against an optimum near 0.4, while the smaller roots only give about 0.5, which doesn't explain a 0.02 loss increase. That points toward the larger σ values, at least for the mid and coarse features. But the fine feature with σ=0.249 already overshoots at w=2, and yet the S9 run at w=3.5 did well, which doesn't fit cleanly.

Fine VH's small root, σ ≈ 0.074, is the only value that squares with the S9 gain at w=3.5, since the larger root would make that weight a net loss. So I'm settling on the small root for the fine feature. Whether mid and coarse also take their small roots, 0.065 and 0.06, is still open.

Mid and coarse values probably run larger than fine, since mid skips one averaging stage and the coarse Sobel responses are max-pooled, which points toward the bigger roots for those two.

Now I'm applying the optimal individual weights for the mid and coarse features, then adding up their contributions alongside the fine term to check whether the combined weight overshoots the target.

I'm checking the fit with the larger σ values for mid and coarse, where the combined contributions looked too heavy against a net loss near +0.02, and that seemed consistent. Next I'm normalizing each VH feature by its σ so they all have unit variance, starting with the fine one.

I'm standardizing each VH feature by its σ and working out the weights under an equicorrelated assumption. With ρ≈0.6 the fine term gets about 3.6, mid about 0.8, and coarse about 0.2. Checking ρ≈0.4 instead gives roughly 3.5, 1.0, and 0.5, so I'm planning to add those.

I'm settling on the weights for the three VH features: a larger one for fine, moderate for mid and small for coarse, with T and G set at 1.2 and 2.5. For the mid feature I'm also considering a centre offset of about 0.034, though the coarse one is still being worked out.

I'm settling the centre offsets for mid and coarse at about 0.034 and 0.027, since the mean of the z-score medians works out to roughly 0.21σ and 0.13σ. I still don't know how well the T and G weights hold up given how uncertain the scales are. I'll run this step with S9 plus mid at 0.9 and coarse at 0.4, which I expect to land near 0.652.
