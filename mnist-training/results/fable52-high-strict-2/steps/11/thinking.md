I'm decoding the bit-mask rule, where each digit's k value combines the upper-left, upper-right and lower-right flags. For digit 0, I'm summing the candidate counts for each flag, getting 641 for ul and 675 for ur, and starting on the lower-right total.

Now I'm working out the upper-right and lower-right totals for digit 1, where the ur sum comes to 545 and lr to 33. Digit 2 follows, and I'm tallying the flag counts across its candidates.

Now I'm checking the lower-right flag for digit 7, which comes to 569, and then tallying the upper-left, upper-right and lower-right totals for digit 8 and digit 9.

Now I'm finishing the upper-right total for digit 9 at 846, then turning to the lower-right sum at 655. I'm also converting the per-digit flag values into the cleaned-up V feature list for all ten digits.

I'm now checking the upper-left feature, where digits 1, 2 and 3 score low, and the upper-right feature, where 5 and 6 are low. Those separations look useful, but the lower-right feature only helps for a few digits. Next I'm building a naive Bayes classifier on these six measured features, plus a template, and I'm starting with the group {0, 2, 8}, where 2 separates from 0 and 8 on the upper-left value while 0 and 8 stay hard to tell apart.

I'm now checking the 8 group against the other digits, since 8's features all sit near 0.5 to 0.6 and it's the variable class. The useful separations are 5 from the rest by upper-right, and 3 versus 8 and 2 by upper-left.

I'm moving toward the classifier now, weighing whether to build it at this step and leave a probe for later if the features prove too weak. The plan is to combine the six measured features with the base template, then use any remaining steps for targeted probes on the hard pairs.

I'm estimating how the likelihood of each feature being present changes with the zone value r, using a linear fit anchored to a typical present value of about 2 to 3 cells.

I'm settling the classifier's per-feature scaling so the presence signal is strong but not overstated, with a moderate reference value and probabilities clipped away from the extremes. I'm also checking that the six zones can be treated as roughly independent given the class. Then I'm weighing how much the base template should count, so its margins don't swamp the measured features.

Now I'm defining the per-zone probability table, clipped to stay between 0.04 and 0.96, starting with the top-horizontal zone.

I'm writing out the per-zone probability table for the six measured features, with each value clipped to stay between 0.04 and 0.96.

I'm now weighing the 8-versus-0 problem: without the middle horizontal, half the 8s would look like 0s, so I'm considering a centre-diagonal probe for that pair, though guessing its values for the other digits feels unreliable, so I'd restrict its effect to 0 versus 8.

I'm weighing a centre-diagonal feature to separate 0 from 8, since 0s should have an empty centre. I'd only let it veto class 0, because guessing its values for the other digits is unreliable, and I'd expect a small presence rate for 0s from slanted sides.

I'm weighing a narrower centre box for the 0-versus-8 probe, so that only very narrow 0s would fall inside it, and I'm wondering whether to use all the non-horizontal orientations.

I'm adding a centre-zone feature that only vetoes class 0, since an 8 with ink in the middle should not be read as a 0, while 0s should have an empty centre. I'm weighing whether to narrow that centre box so only very narrow zeros fall inside it.

I'm settling on a negative-only veto for class 0 when there's ink in the centre, since 0s should have an empty middle, with a slope of about -0.8 per unit of zone value and no intercept. I'll leave the other classes unaffected, because I can't guess their centre-zone values reliably. I'm weighing whether to spend a probe on that feature for every class or just go ahead with the classifier now and keep the remaining steps for checks on the hard pairs like 2 versus 3.

I'm comparing the remaining pairs now: 2 versus 3 is only moderately separated by the lower-right and middle features, while 4 versus 9, 7 versus 9, 1 versus 7, 5 versus 6 and 3 versus 5 each have a feature that separates them clearly.

I'm checking the remaining pairs against the six features: 6 separates from 0 on the top, middle and upper-right zones, and from 4 on the bottom zone. 8 against 3 is only moderately separated, through the upper-left and middle zones, and 8 against 5 is helped by the upper-right zone.

Now I'm settling the linearisation point at r₁ = 2.5, since the zones' present values probably run a bit higher than the H-zone readings suggest, and I'm weighing whether making the features more binary would reduce the overshoot on the present side.

I'm considering whether the base template's miscalibration hurts: it under-predicts 8, 4, 6 and 9 and over-predicts 1. Since 8 is already weak on the measured features, I'm thinking of adding a small bias toward 8, plus modest boosts for 4, 6 and 9 and a small penalty for 1. I'm also planning to scale the whole classifier by about 0.7 to temper overconfidence.

Now I'm laying out the classifier as code: a zone dictionary and the per-zone probability table, with the base template's weights scaled by β and summed with each measured zone's log-likelihood ratio. I'm also adding the centre-zone veto that only pushes class 0 down, then applying the overall scale α.

I'm checking the zone definitions for the top, middle and bottom horizontal features and the upper-left and upper-right vertical ones against the probe cell lists.

I'm writing the zone lists for the six measured features and the centre-zone veto for class 0, then planning to prepare the prototypes from step 7.

Writing the classifier code now, reusing the step 7 prototype preparation so the base template keeps its 70% weighting.
