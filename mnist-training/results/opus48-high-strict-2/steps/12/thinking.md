The 40.5% result is down from 45.3%, and it's clear why: the bias on 7 was pushed too far, so 7 now absorbs most predictions, and the bump on 5 is pulling a similar share toward itself. Meanwhile 3 has dropped to zero correct, since everything that should have been 3 is landing on 7. I'm now checking what happens with 9.

I'm weighing the bias tweaks against step10, which still holds the best result at 45.3%. Pushing 5, 7 and 8 up tends to make them overshoot into magnets, so I'm going to keep changes small: lower 9 a bit and nudge 7 and 8 modestly.

I'm going to nudge the biases by small amounts from step10: keep 5 slightly negative, put 7 a bit higher, and leave 8 alone for now, since it has stayed at zero in both runs and I'm not sure a small shift will change that.

I'm considering giving 8 a hollow template with two loops, since its current all-ones template makes it indistinguishable from zero and it only ever wins on bias. The risk is that it starts resembling 0, so I'll weigh that against the chance it finally captures real 8s.

I'm settling on the step10 biases as the base, since they gave the best result at 45.3%. For the next run I'm lowering 9 a little, nudging 7 and 5 back up modestly, and trying 8 with a hollow template and a larger bias so it can finally match real 8s.

I'm tuning the biases one at a time from the step10 base: lowering 9 a bit, nudging 5 and 7 up modestly so they stay out of magnet territory, and giving 8 a hollow template with a moderate bias.

I'm going to be more conservative this time and change only three biases from the step10 base. Lowering 9 should cut its magnet effect and give back some of what 0 lost, and nudging 7 and 5 modestly should revive them without tipping into the overshoot I saw before. I'll leave 8's template alone.

I'm settling on a conservative set of biases from the step10 base: pulling 9 down, nudging 7 and 5 up a little, and leaving the rest as they were, since 7 at +0.25 should sit between the zero and magnet thresholds.

I'm going with a conservative set of tweaks from the step10 base: pulling 9 down to +0.05, nudging 7 up to +0.25, and easing 5 up to -0.05, while leaving the rest alone.
