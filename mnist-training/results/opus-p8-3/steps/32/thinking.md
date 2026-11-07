The new NB-scaling result came in worse (0.554 against 0.5166), which I think is overconfidence from adding correlated features, with the HB_l middle pushing zeros too hard. The likely culprit is the total NB confidence being too high, so next I'll try scaling the NB part down with a multiplier, around λ_t 0.45 and λ_s 0.

I'm weighing whether to just scale all the logits by 0.8 as a cheap one-step calibration test, or to change the new features' weights in the same step. Changing both at once would confound the result, so I'm leaning toward isolating them. There's also a concern that region-sum features like the HB_l middle one overcount in large regions, so a single multiplier may not suit every feature.

I'm going to add the three new features with a multiplier of 2.0 and λ at 0.4, keeping the step-28 setup otherwise. The cavity and loop features are row and half-region sums that may also be overcounting, though they helped earlier, so I'll leave them as they are for now.
