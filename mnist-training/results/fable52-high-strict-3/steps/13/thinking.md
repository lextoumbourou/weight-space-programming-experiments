The score is at 80.39% and it's the best so far, with three steps left. Each step has been adding about half a point, so I'll keep making small, careful changes. Step 15's result is the one that gets scored and I can't adjust after seeing it, so that last step should be a low-risk refinement of the best configuration from the earlier steps.

Now I'm working through the confusion-matrix numbers: recalls per class, then column sums and the largest off-diagonal flows, including the 4→9 flow that rose after narrowing the rule.

I'm now looking at which classes are being confused: 6 is over-predicted at 1086, with flows like 0→6, 5→6 and 4→6 all rising after the BayU-lower change, probably because the bias and that weight push 4s toward 6.

I'm adjusting the BayU weight for class 6 back to +0.3 at k=2,3 and keeping +0.4 for class 4, with 6's bias returned to −0.03. The 6↔0 exchange nets out about even, so that's balanced now. The class-5 cut to BayL-lower and the bias drop didn't help: the 3↔5 exchange only moved from 132 to 126. The 4→9 flow of 117 is still the largest one to address.

I'm weighing a few ways to use the last three steps: keep polishing the biases and weights, or test a broader parameter change. The pairwise trades look saturated, so the remaining gains probably come from rebalancing the over-predicted classes like 6, 3, 8 and 2 against the under-predicted 4 and 1.

I'm weighing a broader one-shot change: scaling the structure features by about 1.25, or tuning the unexpected-stroke penalty, which I set early and never revisited. A higher penalty might sharpen the 4→9 and 7→9 separations, though that's a gamble of roughly ±1%.

I'm weighing a few smaller options for the remaining steps. One is a global increase in the structural weights, by about 1.2, since structure drove most of the earlier gains, though the current over-firing makes that uncertain. Another is raising the unexpected-stroke penalty, which I set early and never revisited; it could sharpen the 4→9 and 9→7 separations, but its sign is hard to predict.

I'm weighing a scale change: multiplying all the output-layer weights and biases by about 1.25 would leave accuracy unchanged but show whether the loss goes down or up. If it drops I'd keep it, and if it rises I'd revert, though a smaller scale might then help and I'd have to gamble on that at the final step. Whether loss even counts toward the score is unclear, since the note only says the final network is scored on a separate test set.

I'm going to scale the output layer by about 1.2 to see whether the loss moves, since accuracy shouldn't change. If it drops below step 12's 0.6754 I'll keep the scale, and if it rises I'll revert.

Recalculating the per-class biases now: each one gets a small correction from its log ratio of predicted to actual counts, scaled by the learning rate of 0.4.

I'm loosening the 6 and 0 Bayesian-upper weights, and the bias on 6, to balance the 6↔0 exchange. Next I'm checking whether strengthening the crossbar-end feature for class 4, rather than the 9-side rule, could reduce the 4→9 flow without costing 9 so much.

I'm weighing a moderate rule at k=1 for class 9 with a smaller weight, but it would likely cancel out, since the earlier version was net zero. I'm looking at another cue instead: the top-left arc of a 9 versus the left stroke of a 4.

I'm looking at whether the 3→8 confusion, with 75 misclassified 3s, could be cut by using the narrow-bay feature: a 3's upper bay is what separates it from an 8, and I'm weighing whether to adjust the hole weights for the two classes or just nudge the bias on 8.

I'm checking whether the 3-versus-8 confusion, with 75 misclassified 3s, can be separated by the left-side strokes of each loop, since the upper and lower holes sit at similar rows for both digits.

I'm checking whether the 3-versus-8 split can rely on the upper-left wall of the loop, which for an 8 sits one column further in than for a 3. A rule for 3s at the left-middle position would catch that, but narrow 3s put strokes there too, so it could backfire. I'm now considering a diagonal feature on the 8's lower-left arc as an alternative.

Next I'm checking the thick-1 cases, where the bar detectors may fail on a wide blob of ink, so I'm looking at what the vertical edge features return for those.

I'm thinking the bias dominates for weak or thick 1s, since all their logits sit near zero, and 7 and 4 carry the largest biases, which could explain the 1→7 and 1→4 flows. The fix might be to express those class offsets as weights on the feature energy instead of a constant, so weak images aren't pushed toward 7 and 4.

I'm weighing whether to convert part of the large 7 and 4 biases into weights proportional to feature energy, since a constant bias dominates for weak or thick 1s. The catch is that my estimate of typical feature energy is uncertain by about 2×, so a partial shift of around 0.2 could upset the class balance I've already tuned.

I'm considering a class-1 prior that scales with total stroke energy: a constant bias on 1 plus a negative per-feature term, so that weak or thick 1s, which have little feature energy, get pulled toward 1 instead of 4 or 7.

I'm working out whether a bias-proportional term for class 1 would help, since a higher constant bias plus a small per-feature penalty would favour weak, thick 1s over 4 and 7 while leaving strong thin 1s roughly unchanged. Based on rough energy estimates, that would give a small boost to low-energy images and a mild penalty to high-energy 7s and 4s, so I'm settling on about 0.03 per orientation feature with a +0.3 bias shift on class 1.

I'm weighing whether to add a bias-plus-energy term for class 1, with the bias raised to about +0.35 and a per-feature penalty around 0.025. That should lift weak 1s out of the 4 and 7 region, though if real 1s carry more energy than I estimated it could cost some recall. Since 1 is already under-predicted and these confusions account for roughly 90 errors, I think the trade is worth making.

I'm weighing whether shifting part of the 7 and 4 biases into a feature-energy term would stop weak images from defaulting to those classes, though my energy estimate is rough enough that the balance I've already tuned could move.

I'm applying the class-1 adjustment: a small per-feature reduction on all the orientation weights, with the bias raised to about 0.37, so that weak or thick 1s come out ahead of 4 and 7 while typical 1s stay where the earlier balance put them.

Settling on a class-1 adjustment: a constant bias of about 0.42 with a per-feature penalty of 0.02, which should leave typical 1s roughly where they are while lifting weak or thick ones out of the 4 and 7 region.

I'm rescaling the final weights and biases by 1.2, which leaves accuracy unchanged, and I'm going to write up step 13 next.
