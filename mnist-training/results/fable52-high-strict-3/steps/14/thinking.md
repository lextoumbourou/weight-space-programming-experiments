The 1.2 scale brought loss down from 0.675 to 0.624, with accuracy ticking up a little, so the model still looks under-confident. I'll try a scale of 1.5 at step 14 and decide on step 15 from there. Estimating the slope from those two points gives roughly −0.25 loss per unit of scale.

I'm going to try a scale of 1.6 at step 14, since the loss curve still looks convex with its minimum somewhere around 1.6 to 2.0. Once I have that result, I'll fit a parabola through the three points to pick the final scale for step 15. Meanwhile, the one-recall figures barely moved, so the energy-based explanation for those 1s doesn't hold up, and I'm now recomputing the confusion column sums to guide the bias adjustments.

I'm tallying the column sums of the confusion matrix for the remaining digits, and I'm also noting that the bias updates are being applied in base units since they were scaled along with the weights.

I'm nudging the bias for digit 1 further up, since its predicted count fell instead of rising as I expected, which suggests the energy term is pulling harder than I estimated. For the other digits I'm working out the log-ratios of predicted to actual column sums and applying damped corrections in base units, mostly small nudges up or down.

I'm nudging the bias for digit 4 up again, since it keeps coming out under-predicted while 1→4 and 4→9 confusions hold steady. Digit 9 is already over-predicted at 1003, and its main confusions are with 7, 3, 5 and 0. I'm checking whether a targeted tweak between 4 and 9 might help before settling the final step.

I'm checking whether a 9 has a top arc that a weighted feature could pick up, and whether that arc is missing in 4s, which would help separate the two digits.

I'm checking whether a loop-bottom horizontal stroke at the lower-left, which 9s have and 7s don't, could separate the two digits without hurting the 7 vs 9 case.

I'm weighing a bias tweak for digit 9 that pushes up on a horizontal stroke at the loop bottom, which would help separate plain 7s from 9s. It could also hurt 9s that lack a clear loop bottom, so the net effect on the bias is hard to call.

I'm settling on the bias polish for step 14, keeping the 1-recall tweak as it is so the biases stay balanced. I'm also looking at whether the 0-to-2 confusions can be reduced with a small tweak to the corner and bottom-right features.

I'm weighing whether the zero-versus-two confusions could be reduced by adjusting the hole features for digit 0, since a narrow tilted zero looks a lot like a two. Right now the hole weights for digit 0 don't separate the two shapes well, so I'm considering a small boost to those hole terms.

I'm considering a hole feature at the center rows for digit 0, since a narrow tilted zero can look like a two. Raising 0's hole weight there and lowering it for 2 might cut the 0-to-2 confusions, though it could push some 6s toward 0, so I'm keeping the change small.

I'm adjusting the hole weights for digits 0 and 2 to pull apart the narrow tilted zeros that look like twos, and I'll then set the scale to 1.6 for step 14.
