The result got worse: digits 4, 6, 8 and 9 are never predicted now, while 3 and 1 take over. My guess is that the penalty λ||t||² is too strong for the actual feature magnitudes. Classes with dense templates (8, 6, 9, 4, 0) lose out, and classes with small template norms (1, 3, 7) win. That would mean the features are smaller than the templates, so γ < 1, perhaps around 0.3 to 0.5 instead of 1.

I'm weighing a smaller λ, around 0.2, since the actual features look roughly 0.4 times the template scale. I can't solve for γ exactly from the step-5 comparison of 3 against 9, so I'm picking λ to balance the correct class against subset templates under that assumption. If the true scale is closer to 0.7, dense templates would get favoured again, so the choice is fragile.

I'm working out why centring might help: subtracting the mean template value cancels any uniform offset, and the penalty then tracks the input's total feature mass, which would make it less sensitive to the unknown scale γ.

I'm now comparing the centred score against the nearest-template one, looking at how a perfectly matching dense template ends up with a low logit because its variance is small. A subset template ties with the full one in the uniform case, so this approach breaks down there. I'm considering whether adding more channels would reduce that tie.

I'm building a size-adjusted penalty: scaling it by the input's total feature mass should make the logits scale together with γ, so the unknown magnitude cancels out.

I'm rechecking the mass-normalised penalty: scaling it by the input's total feature mass makes every term move together with γ, so the superset and subset cases still come out below the correct class. Adding the term to each template's score is what makes it scale-robust.

I'm going to scale the penalty by the input's total feature mass, so that it moves with the unknown γ. I'm setting λ to 0.5 and computing the average template mass S̄, so each template's weight becomes its own vector minus a λ-scaled share of its squared norm. Next I need to estimate the logit size, which depends on the template norms and on the channel magnitudes.

I'm settling on s = 0.6, since the correct-class logit comes out around 7.5 s and the gaps between classes are about a third of that. The fine-ink channels seem to carry too much weight, because they appear in four of the sixteen maps. I also want to check the 0→2 and 0→3 confusions.

Now I'm checking the 6→2 mismatch at cell 261, which looks odd, along with the cross-template confusions in general, but I'll first test the scale-robust approach.
