Step 9 came back with loss 8.13 and huge logits, with class 8 acting as a sink. I've been going around in circles with prototype approaches, six steps are left, and my best so far is 43.6% at step 2. I'm now wondering whether my assumptions about the feature space are wrong, and whether I should revert to step 2 and improve it modestly or look for a more fundamental problem.

I'm checking whether the logit scale explains the loss of 8, since the normalized prototypes with SCALE=10 could produce logits around 50. That would make the wrong predictions overconfident, but scaling alone might fix it. The class-8 sink is harder: if the features run smaller than the prototype mean, the centered score for 8 could come out negative even though it still wins most cases.

I'm checking whether the logit scale alone explains the loss of 8, since with SCALE=10 and normalized prototypes the logits could reach around 50. The class-8 sink is harder to explain: if the features run smaller than the prototype mean, the centered score for 8 might still win most cases, and the bias term is interacting with the feature scale in a way I haven't pinned down. I'm weighing whether to revert to the step-2 template approach and improve it modestly, given six steps remain.

I'm weighing whether to do manual per-class bias tweaks on the validation confusion matrices, which would be standard calibration but feels like a weak fix. I'm also still turning over whether the fundamental problem is a feature scale mismatch that I haven't isolated yet.

I'm considering whether a scale-free classifier, with zero-mean templates and no bias, would avoid the feature-scale mismatch. Step 8 tried that and still ended up with class 4 as a sink, though step 2's zero-mean ink templates reached 43%, so the difference may come down to how the templates were built. I'm also wondering whether centering the features on their own average could help, though that would need data.

Now I'm working out what a typical feature vector should look like, reasoning about which of the 80 entries light up for a digit, and which spatial cells sit near its center versus its edges.

I'm looking at why the center-heavy feature pattern pulls the zero-mean templates toward classes like 4 and 1, since the typical feature vector has a large shared center component that any center-concentrated prototype will match well. That suggests what's really needed is a way to subtract out this common center component from the features themselves, not just from the templates.

I'm checking whether the 8-sink comes from the centered prototype u_8 lining up with the features, which would mean real feature vectors carry more central mass than the averaged prototype m does, perhaps because dense regions read stronger in practice.

I'm weighing whether per-class bias adjustments from the validation confusion matrices count as legitimate calibration, since the feedback is meant to guide the next steps, even though manual tuning of this kind feels like a weak fix.

I'm weighing whether to revert to the step-2 network, which reached 43.6%, and apply manual per-class bias corrections based on its confusion matrix, since class 5 absorbs many 0s, 2s, and 3s. It's a weak fix, but with six steps left it's the most practical option.

I'm considering manual per-class bias adjustments on the step-2 network, lowering class 5's bias since it absorbs many 0s, 2s, 3s, 6s, 8s and 9s. Each iteration would show whether the shift helps, which could plausibly push accuracy toward the mid-50s within the remaining steps.

I'm weighing whether to keep the step-2 zero-mean approach and add per-class biases adjusted from the confusion matrix, since the templates there were built on a flawed grid assumption but still reached 43%. The idea is to equalize predicted counts across classes, lowering the bias of the sink classes, which is a manual calibration step rather than a search in code.

I'm thinking about whether manual per-class bias adjustments count as legitimate here, since the code itself would just hold constants and the feedback is the intended guide. I'll go with step 2's network as the base, since it had the best accuracy, and add biases to push back against the sink classes using its predicted counts.

Tallying the predicted class counts from step 2's confusion matrix now, with class 5 absorbing about 2,870 predictions and class 0 only 53.

Comparing predicted counts against the roughly even true class sizes, classes 2, 3 and especially 5 are heavily over-predicted, while 0, 6, 8 and 9 are almost never chosen. So I'm thinking about lowering the biases of 5, 2 and 3 and raising those of the under-predicted classes, with the step-2 scale still needing to be pinned down.

I'm settling on specific bias values now: a strong cut for class 5, moderate reductions for 3 and 2, and boosts for the under-predicted classes 8, 9, 6, 0, and 7. I'm weighing whether a bias of about one unit is significant against the logit scale, which the loss of around 2 suggests is only a few units apart.

Now I'm weighing whether per-class bias adjustments are a legitimate calibration step, since the test set should share the validation set's class priors, so biases could carry over.

Reconstructing step 2's build_weights from the earlier code, so I can apply per-class bias corrections on top of it.

Reconstructing step 2's conv filters and fully-connected template weights from the earlier code so I can layer the per-class bias corrections on top of it.

Still writing the ink templates for classes 4 and beyond...

Still writing the template weights for the remaining classes...

Still writing the horizontal template rows...

Still reconstructing the step-2 template values, including the horizontal rows and the zero-mean ink block...

Now I'm recalling step 2's conv and template values, checking the sign patterns I used for each digit before layering biases on top.

Considering whether the step-2 ink templates could be sharpened too, though I'm wary of changing a part I can't verify on the 4x4 grid. I'm wondering if rebuilding the ink-only zero-mean templates from the drawn strokes would fix the sink, since step 8's oriented version also collapsed onto class 4, so the problem may lie in how the channels combine rather than in the template content itself.

Working out the per-class biases from step 2's predicted counts, comparing each against the true class size, with the step-2 weights and their scale still to be pinned down.

I'm going back over the step-2 confusion matrix row by row to get the predicted counts for each column right, since my first pass at the column totals was off.

Now I'm going through the step-2 confusion matrix row by row, reading off the predicted counts for each column.

Tallying the predicted class counts from the step-2 confusion matrix column by column now, with class 5 again the largest sink.

Checking the predicted counts column by column: classes 2 and 5 are the big over-predictions, and the rest are fairly close to target, with the remaining sums roughly confirming the totals.

Working through the step-2 confusion matrix, the over-predicted classes are 2, 3 and especially 5, while 0, 6, 8 and 9 are chosen far too rarely. I'm weighing a bias set that cuts 5 by about 1.0, 2 and 3 by 0.5, and raises 8 and 9 by 0.8, with 0 and 6 by 0.5, leaving the uncertain magnitudes to be checked in the next step.

Setting the per-class bias values now: a cut of about 1.0 for class 5, roughly 0.5 each for 2 and 3, small boosts for 0 and 6, and larger ones for 8 and 9, leaving class 4 at zero.

Still writing the step-2 conv setup for the bias calibration...

Still writing the step-2 conv filter setup...

Still reconstructing the step-2 conv setup, checking the line profile scale and the zero-mean channel layout.

Still reconstructing step 2's conv2 setup, the blurred blob channel and the wide copies that follow.

Still writing the step-2 fc bias vector, with the horizontal template weights already set.

I'm settling on returning to step 2's network, the best so far at 43.6%, and setting per-class offsets from its confusion matrix: a cut for class 5, smaller cuts for 2 and 3, and small boosts for 0, 6, 8 and 9. These are manual calibration values, not something the code fits.
