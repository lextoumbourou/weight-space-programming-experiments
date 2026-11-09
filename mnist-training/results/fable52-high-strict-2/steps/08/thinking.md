The 70.1% accuracy comes from the new features with naive Bayes, which is about the same as the 69% from step 1 using pure cosine, though the loss of 1.24 suggests the model is overconfident, so I'll lower the alpha. The confusion pattern has shifted: class 4 now mostly gets mistaken for 1, 9, and 2, and class 6 for 0, 1, and 5.

Class 8, 6, 4 and 9 come out under-predicted, and 1 is over-predicted with 1504 expected. I suspect the bias term is the culprit: the log(1−p) penalty hits ink-heavy classes too hard, which points to my p=0.8 being too optimistic about feature presence.

I'm weighing whether the bias term is the real issue, since the penalty on absent expected features may be too strong for ink-heavy classes. Another option is to skip the per-feature calibration and instead shift class biases directly from the column sums, giving a boost to 4, 6, 8 and 9 and a reduction to 0, 1, 3 and 7. The size of that shift depends on how many expected features each class has, and I'm estimating that 8 has many more than 1, with the miscalibration growing if actual presence rates are below 0.8.

I'm checking whether a p of 0.6 to 0.65 for the expected features would calibrate the model, since with p at 0.8 the ink-heavy classes like 8 end up roughly 17 raw units behind class 1, which accounts for the under-prediction. I still need to work out what that change does to the low-T features.

I'm weighing a pmax of 0.65 with ε=0.2 against the current setting, since a symmetric weighting around p=0.5 might correct the bias for the ink-heavy classes without a separate per-class adjustment.

I'm weighing whether a symmetric setting around p=0.5, with ε=0.2 and pmax=0.65, would work better than the current one. The expected features would add about +0.62 each, while unexpected ink would cost about −1.39, and the penalty for strokes landing just off-target seems reasonable.

I'm comparing the sharper naive Bayes features against the earlier blurred cosine setup, noting that sharp features fix some confusions like 2→3 and 7→9 while introducing others. I think calibrating per-class biases from the predicted-count imbalance, boosting the under-predicted classes and reducing the over-predicted ones, could push this to somewhere around 75 to 78%.

I'm estimating how large the bias correction needs to be: the average loss on wrong predictions implies margins of roughly 3.5 to 4 logits, or about 45 raw units, so corrections in the 20 to 40 range seem plausible. For the 8-versus-1 gap, the miscalibration is around 17 raw units at q=0.6, rising to about 25 if the true presence rate is 0.5. Lowering the assumed presence rate to match the real one might handle this more cleanly, but that depends on what q actually is.

I'm considering whether a lower pmax, around 0.6, would calibrate the expected-feature weights better than the current setting, since I can't reliably count the expected features per class by hand.

I'm weighing a pmax of 0.6 with ε=0.2, which gives a positive weight of about 0.4 for expected features against a penalty of about −1.39 for unexpected ink, so the model leans heavily on vetoes. That could hurt digits like 1, where small displacements land in cells the prototype doesn't cover. I'm also checking where the neutral point falls, around T≈0.67, since strokes just 2 to 3 pixels off target already pull the weight negative.

I'm thinking about decoupling the fix: keep the symmetric ±1.39 weights from before, but scale the bias term by a factor κ below one, so the heavy classes get less of the penalty for absent expected features. Setting κ around 0.6 would let the ink-heavy classes recover without changing the per-feature weights.

I'm working out why the classes with loops, 6, 8 and 9, come out under-predicted: their prototypes are probably less accurate, so their expected features turn up absent more often than the model assumes.

I'm estimating per-class bias corrections directly from the column sums, nudging the under-predicted classes 4, 8, 9 and 6 up and the over-predicted 1, 7, 3 and 0 down. I still don't know how many predictions a raw unit of bias moves, so I'm trying to pin down the margin scale from the loss and accuracy first.

Working through the margin scale: the loss of about 1.2 at 70% accuracy fits a logit spread of roughly 5, which I'll convert into raw units for the bias corrections.

I'm working out the scale of the bias shifts: with margins around 60 raw units, a 10-unit nudge barely moves predictions, so the under-predicted classes 4, 8, 9 and 6 would need corrections closer to 30 to 50 raw units. The 8-to-1 confusion suggests the prototypes for those classes are the real problem, not just the bias term.

I'm weighing whether to go back to the step-5 design, which reached 73.8%, and tune it, or keep the naive Bayes approach and fix the bias corrections and the 8 prototype, which looks too wide for narrow 8s. The sharp features clearly helped specific confusions, so I'm leaning toward keeping them.

I'm weighing whether softening the penalties would actually change anything, since scaling both weights equally leaves the argmax alone. The real question is the asymmetry between the positive and negative weights, so I'll parametrise the per-feature weight as a linear function of the template value T.

I'm turning the naive Bayes score into an explicit linear form: each present feature adds a weight proportional to its template value, each absent one subtracts, and a bias term scales with the total template mass per class. Under the original settings that bias works out to a full cost per expected feature, so the net contribution is zero when the feature is present and negative when it is absent.

I'm reworking the naive Bayes weights so the expected-feature bonus is small and the absent-feature cost is milder, which means shrinking the bias term by a factor κ. With a presence rate q around 0.6 and ε around 0.15, the present-feature weight comes out near +0.4 and the absent-feature cost near −1.7, leaving an expected feature that's present with a net of about −0.35.

I'm checking whether vetoes dominate the classification, since a class with few expected cells like 1 would reject nearly every other digit. Prototypes may need several variants, such as a narrow 8 covered by optional strokes at about half weight, so the absent-feature penalty doesn't wrongly reject thin digits.

I'm weighing whether to keep the naive Bayes approach and tune it, or switch back to the step-5 design that reached 73.8%, which had blurry features. I'm considering whether to sharpen those features and add symmetric evidence terms on top of the cosine templates, since that would be the most promising path with the few steps left.

I'm settling on the naive Bayes route with a global κ reduction and per-class bias corrections, since that looks like the most practical fix for the calibration problem, and I'm trying to figure out how to set the corrections without a reliable scale.

Lowering the global κ would shift the bias by about the same amount for the heavy classes as for the light ones, so it can't separate 0, 2, 3 and 5 from 4, 6, 8 and 9. The per-class corrections are needed regardless: boost 4, 6, 8 and 9, and pull down 0, 2, 3, 5 and 7, with class 1 needing the largest cut.

I'm estimating how big each per-class bias correction needs to be, using the margin spread of about 62 raw units and each class's recall. To lift classes 4, 8, 9 and 6 toward roughly 80% recall, the shifts come out around 38 to 55 raw units, though raising them will also pull predictions away from the other classes.

I'm settling on a moderate per-class bias correction rather than a blunt global one: raising 4, 8, 9 and 6 by roughly 20 to 25 raw units and pulling down 1, 0, 7 and 3, since 1 has too many false positives. The real fix still looks like the prototypes, and I want to check why class 4 gets pulled toward 1 and 9 so strongly.

I'm trying to work out why class 4 is so weak: its errors are spread across 1, 9, 2, 3, 7 and 0, which points to its own prototype being off rather than just the bias. My guess is the 4 is either too wide or its crossbar sits at the wrong height, so I want to think through the centred geometry of a typical 4, with the vertical stroke on the right and the left stroke and bar pulling the centre of mass leftward.

I'm wondering whether I can measure the stroke positions for class 4 directly, like checking which row bands contain its horizontal bar, since guessing the prototype geometry blind isn't reliable.

I'm weighing a hybrid: sharp features with cosine templates as a bonus term, plus softer naive Bayes vetoes at reduced weight. The idea is to give each prototype cell a soft probability, around 0.6 where there's a stroke, 0.4 nearby, and 0.1 far away, so that unexpected ink is penalised without overreacting to uncertain geometry.

I'm considering a veto-dominant version where ink far from any prototype stroke gets penalised heavily. The worry is that slanted 1s or wide 4s would trip it, since the "far" threshold depends on how tolerant the stroke placement is.

I'm thinking the class-specific misses may come from the prototypes or from the expected-present assumption breaking down for tight loops like 8, 9 and 6, whose small curvature gives weak filter responses. Before settling on that, I want a diagnostic that shows which of the two is actually driving the low recall for 4, 6, 8 and 9.

I'm thinking about whether I can calibrate the per-class biases by looking at total feature activity instead of guessing from the confusion counts. The idea is to bin the count of active features for each class and compare those distributions, though I can't easily compute the expected totals by hand, so I'd be limited to relative comparisons.

I'm planning to fix the bias problem with per-class corrections and a few more rounds of re-balancing against the confusion counts. I also want to lower the temperature α to about 0.03 so the logits match the actual accuracy, which should bring the loss down.

I'm lowering the temperature to about 0.035 so the logits match the real accuracy, then turning to the confusions from step 7. Class 8 gets mistaken for 1 and 7, which suggests narrow or slanted 8s, so I'm thinking of adding an optional narrower 8 variant at half weight with a small bias boost. Class 6 is confused with 0 and 1, and class 9 with 7, 0 and 5, so those prototypes may need similar variants.

I'm now looking at the 3 and 5 confusion, since they share the lower half and differ mainly in the upper strokes. The 5's upper-left vertical looks short and often slanted or merged into the bar, which would explain why that feature is only present about half the time.

I'm reducing the harshness of the penalties by setting the expected-present probability to 0.7 and the epsilon to 0.2, which lowers the cost of expected-but-absent features. The bias shift that follows is roughly proportional to each class's size, so the heaviest classes like 8 and 0 move the most, and I'll still add smaller class-specific corrections on top.

Reconsidering the expected-feature weights: lowering them from 1.39 to 0.85 mostly helps images where few expected features are present, so the net gain for true-class images is small. The under-prediction of 4, 6, 8 and 9 is probably better addressed by per-class bias terms than by reshaping the feature weights.

I'm working out the per-class bias for step 8, starting with class 0, which is predicted 1261 times against 819 correct, so it gets a bias of about −8.

Now I'm settling the per-class bias offsets for the remaining classes, with the largest downward shifts for 1 and 7 and modest upward ones for 4, 6, 8 and 9. I expect class 4's recall to climb to roughly 70% with these corrections, and I'll also add optional tolerant prototype variants for 8, 6, 9 and 4 at half weight.

I'm thinking about adding optional variant prototypes at half weight, since a missing stroke can then be neutral rather than costly: a narrower figure-eight for 8, a more slanted stem for 9, a smaller loop for 6, and a lower crossbar for 4.

I'm considering adding optional narrower variants at half weight, since a skipped 4 bar doesn't matter much. The 8→1 confusions probably come from class 1's centre-column features accepting narrow 8s, while class 8's own template is penalised for its absent wide lobes.

I'm thinking about narrowing the 8 template's wide lobes to about 0.75 weight and adding a narrow variant at 0.5, so the narrow 8s stop taking such a heavy penalty. The same reweighting could apply to the loops of 6 and 9 and to all of 4, but I'd rather only adjust 8 for now and add the per-class biases.

I'm weighing which changes are most likely to help: the bias corrections and the lower temperature look safest, while prototype variants are more speculative. Narrow 8s and 6s seem to be what's drawing them toward 1, and a small-loop variant for 9 might reduce its confusion with 7, so I'm considering half-weight optional variants for those classes.

I'm wondering why 4s get mistaken for 1s when the bar should be a clear feature. The likely cause is that many 4s have a left stroke or bar in a different place than my prototype expects, which would penalise the correct template. Adding some tolerance, such as lowering the weights on the left stroke and bar, might help.

I'm wondering whether to bump the template blur from 2.6 to about 3.0, since my prototype errors are around ±2 px and wider tolerance might help. The bias offsets I estimated were for the old blur, but the direction should still hold, so I'm weighing whether to change both at once.

I'm settling on the step 8 plan: keep the current weights, add the per-class bias corrections and lower the temperature to 0.035. I'll also add half-weight variant prototypes for 8, 6 and 9, leaving the blur at 2.6 so I don't change too many things at once.

Still writing the variant prototypes and the bias terms, now with the narrow loop for 6 and the small loop for 9 at half weight.
