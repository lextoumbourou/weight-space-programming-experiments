I'm weighing a riskier move for step 14: maybe 0s get misread as 6s because their slanted shape reads like a 6's stroke, so I'm considering extra shear on the 0 template or adjusting the 6 template instead. If step 14 turns out worse, I'll resubmit step 13 for the final step.

I'm now looking at a few other pairs to target for step 14: 3→5, 2→3, 1→2, 7→9, and 4→8. Adjusting biases seems like the cheaper lever, with 4 going up slightly and 8 going down a bit.

I'm going back and forth on whether to tune the biases or try something with the model's cross-talk, but I don't have enough evidence to justify the cross-talk change. Shifting sigma to 3.0 cut some confusions, like 0→6, but it raised 0→2 and dropped 9's recall, so I'm leaning toward retuning the biases first to see if that balances things out.

I'm settling on a sure, small gain here: a sigma of 2.75 might balance things, but its effect is unpredictable, so I'll skip it and just refine the biases.
