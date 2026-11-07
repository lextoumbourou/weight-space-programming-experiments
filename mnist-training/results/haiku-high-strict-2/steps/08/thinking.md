The step 7 run got worse, down to 28.7%, and the bias tuning looks unstable since the logit scale is big compared to the deltas. Class 3 now dominates the predictions, and a shift from 0.0 to -0.8 on delta 3 seems to have pushed it from about 10 to roughly 3000, so the bias sensitivity is clearly large.

Step 5 is still the best at 32.4%, so I'm weighing whether to go back to it and improve the templates in a way that doesn't depend on fragile biases, or to look for a more robust readout altogether. Equalizing biases through calibration was the right idea back in step 3, but my guess for the scale was off. Step 6 failed too, with class 2 taking over, and I still need to work out why.

I'm trying to work out why step 6 sent so many 1s to class 2, since the centred templates should separate them. Digit 1's ink sits in the centre column, which should favour class 1 and not class 2, so the normalisation step may be inflating class 1's weights.

Stepping back, the bias calibration is probably the real culprit here, not the templates. Templates have been reworked a lot without the accuracy moving much, which points to the logit offsets dominating the outcome. A principled fix would be to set the biases so an average digit gives roughly equal scores across classes, rather than tuning them by hand.

I'm weighing a cleaner readout: normalise each class template to the same norm and drop the biases entirely, skipping the centring that step 6 used. The energy mismatch between templates and features is the thing I'd be trying to sidestep this time.

I'm weighing whether the bias calibration can be fixed analytically, since matching each class's template energy to the actual feature energy is what the Gaussian term assumes, and the mismatch is what's producing the sinks.

Step 5 is the configuration I want to return to, since it's the best so far and its predictions are spread out rather than collapsing onto one class. I also need to keep in mind that the final score comes from the last step, not the best one, so the goal is to finish near that level. I'll revert to step 5's exact values and make only small bias adjustments from there, though I'm checking step 5's distribution where class 9 absorbs about 3,800 predictions.

Step 5 already had the 9 sink, sending about 3,800 predictions there and mislabelling 1s as 9s. So it wasn't balanced either. Dropping 9's delta by 0.5 in step 7 pushed the 3 sink up instead, which suggests 3 and 9 are close competitors whose logits sit near each other. Delta 3 at −0.8 was suppressing 3 well, while setting it back to 0 let 3 blow up to around 3000.

I'm checking the step 5 and step 7 histograms against each other: 3 and 9 look like close competitors, with delta 3 at −0.8 holding 3 down and delta 9 at +0.8 letting 9 take over. Dropping delta 9 to −0.5 wiped 9 out completely, while setting delta 3 back to 0 let 3 absorb nearly 3,900 predictions, so the useful range for these two lies somewhere between those settings.

I'm comparing steps 5 and 7 directly: 3 and 9 are close competitors, and a shift of 0.8 in a single delta swings their predicted counts by thousands. That means the raw logits for these two classes sit near each other, and the scale is what's making the biases so sensitive.

I'm checking whether the logit scale is what makes the deltas so powerful, since a shift of 0.5 seems to rival the raw dot-product gaps between classes. Scaling all the weights up would sharpen the output without changing the ranking, so the real question is how the biases compare to the template scores, and I'd need those numbers to say more.

I'm weighing restoring step 5 and trying a small, principled change, maybe reshaping the 9 and 3 templates so they overlap less, since with only 8 steps left I can't afford to chase bias tuning blindly.

I'm thinking about nudging the deltas partway between the step 5 and step 7 settings, since 3 and 9 trade predictions so sharply, and I'm checking whether a small shift on class 1 and class 7 would keep those counts from collapsing.

I'm settling on a set of deltas that sits between the step 5 and step 7 values, since class 3 and class 9 trade predictions too sharply at the extremes. Classes 2 and 4 are over-predicted in step 5, so I'm pulling their deltas down a bit as well, with the rest adjusted in small steps.

Looking at the sinks again, I'm wondering whether they come from the templates themselves rather than the deltas, since even the zero-delta run had 3, 2 and 6 dominating. I'm considering setting each bias so the average logit per class is equal over a uniform mix of the ten templates, rather than tuning them by hand.

I'm working out the bias calibration analytically now: the idea is to set each class's bias so the average digit's logits come out equal, which removes any built-in favouring of one class over the others.

I'm checking whether centring the templates on the average digit removes the built-in favouring of one class, since that would make the biases follow from the templates rather than from hand-tuned deltas. The idea is to set each bias so the mean image gives every class the same score, which gives a calibration without any data. I want to compare that against the step 3 result, because it has no energy term and may avoid the sinks I'm seeing now.

I'm weighing a mean-image calibration instead of more hand-tuned deltas: pick each bias so the average digit template gives every class the same logit, which removes any built-in favouring and follows from the templates alone. That would be a different approach from the earlier attempts, and I'd guess around 35–45% if the templates hold up, though the step 3 density-only version had sinks, so this is uncertain.

I'm setting up the mean-image calibration now: each class's weights get scaled by the channel gains, and each bias is chosen so the average template produces equal logits across all ten classes.

I'm switching to a mean-image calibration: set each bias so the average template gives every class the same logit, which replaces the Gaussian energy term with a shift toward the mean template.

I'm weighing a mean-centred linear score instead of the Gaussian energy term: each class's weights are its template minus the average template, with biases set so the mean image gives equal logits. The energy term penalises large templates, while this version compares each class against the average digit, so it's a different trade-off, and I'd expect it to be sensible even though I can't yet say how it will behave.

I'm switching to a mean-image calibration instead of more hand-tuned offsets, since small delta changes keep swinging classes 3 and 9 by thousands. Each bias gets set so the average digit template gives every class the same logit, which makes the decision compare each template against the average digit.
