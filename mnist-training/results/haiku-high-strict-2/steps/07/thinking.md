Step 6 dropped accuracy to 18%, so centring and normalisation seem to have hurt. I suspect the normalisation shrank the logits, and the centred templates now lean toward class 2, which is predicted for most inputs. I'm trying to work out why class 2's column is so large, since its centred template carries a strong positive bottom-bar pattern that may dominate whenever the bottom row is active.

Class 2 seems to win on ink-heavy images because its template has the largest total ink, so the centring didn't remove that bias. Step 5's Gaussian structure did better at 32%, so I'm considering reverting to it and only correcting the offset that over-predicts 9.

Step 5's Gaussian base still looks like the best starting point. The bias for 9 looks too large, since 9 absorbs 7s, 3s and 4s, and the 7 template seems weak. I'll look at whether the 9 template overlaps too much with 7 and 1.

I'm checking whether the 7 template's pattern overlaps with 9's, since that might explain why 7s keep landing on 9. Rather than hand-tuning biases further, I'm weighing whether to revert to the Gaussian structure from step 5 and make a more principled correction.

I'm weighing whether a single change would help more than the others, since the Gaussian base seems to be the strongest starting point. I'm now going back over how the feature magnitudes come out of the first convolution, because if they're off by a lot, that would explain why the energy term dominates.

Working through the vertical kernel's response: a stroke one column wide lights up the centre weight for all five rows, giving about 5, but a solid block gets pushed negative by the side weights and clipped to zero by the ReLU.

Checking the vertical kernel's response to a stroke: a one-column-wide line gives about 5, while a half-overlapping one gives roughly 2.5. Next I'm estimating the density feature for a 5x5 region, which comes to about 1.5 for a stroke with around ten ink pixels and 4.5 for a solid block. Then I'm working out how the box average in the second convolution scales the pooled values along a stroke, which may be around 25 across five positions.

Working out how the feature magnitudes scale through the pooling: the vertical response on a stroke is about 1.25 per column after the box average, and max-pooling bumps that to roughly 1.5 to 2.5 at stroke cells. The diagonal kernel should land around 3 on a thick diagonal stroke.

Now I'm checking whether the feature magnitudes from the convolutions and pooling are roughly comparable, which they seem to be at around 2 per channel. That makes me doubt the scale is the culprit, so the poor template matching is probably the real problem. I'm considering whether a simpler density-based readout would do better than these hand-tuned orientation maps.

I'm weighing a return to the step-5 structure, since it reached 32%, and considering either tuning its deltas or dropping them, because the +0.8 bias on 9 may be what let it swallow so many 1s and 3s. The confusion counts show errors across several digits, so I'm wondering whether any single structural change could lift accuracy substantially, or whether the hand-built templates simply cap what I can get.

I'm going back to the Gaussian base from step 5 and making only small bias corrections instead of guessing large deltas. I'd lower the bias for 9 since it absorbs both the 1s and the 7s, nudge 7 up a little, and check whether the 2 bias is actually pulling too many predictions.

I'm checking whether the energy term explains the 1-to-9 errors: if a class's template has the smallest norm, weakly featured digits like 1s could default to it, and I'm wondering whether 9's template is that class.

I'm going to try to work out whether a dot-product readout without the energy term would do better, since the templates are uncentred and weak features could give near-zero logits. That would still favour the ink-heavy classes like 0, 2 and 8, the same sink pattern I saw earlier. I'm not sure it's an improvement over the Gaussian base.

I'm dropping the extra circling and going back to the step-5 Gaussian base, which reached 32%. I plan to keep the deltas small: lower the bias on 9 and 2 by about 0.5 each to counter their over-prediction, and then check what the remaining errors show.

I'm tallying the per-column counts for class 4 and class 6 to see which biases need nudging. Class 7 and class 1 look under-predicted, so I'd raise their biases, and class 6 might need a small bump too.

I'm tallying the per-column counts for the remaining classes, checking whether class 4 and class 9 are being over-predicted enough to warrant a bias correction, and whether class 3 is contributing much at all.

I'm checking the column counts for class 3, which is almost never predicted now, so it probably needs a sizeable upward bias.

I'm reading the step-5 confusion matrix row by row, starting with the first rows to check the counts against each class.

Now I'm tallying the column totals of the confusion matrix, which is where the predicted-class counts for each digit come from.

Now I'm tallying the remaining column totals, mostly the counts for classes 8 and 9, which seem to be piling up.

I'm tallying the column totals from the step-5 confusion matrix, and class 9 is predicted about 3,800 times, far too many. Class 2 and class 4 are also over-predicted, while 1, 3, 6 and 7 are badly under-predicted. So I'm leaning toward lowering the biases for 9, 2 and 4 and raising the ones for the under-predicted classes.

I'm now looking at the step-5 column totals, which show class 9 predicted about 3,800 times and class 2 over 1,900 times, while classes 1 and 3 barely get predicted at all. That points to raising the biases for 1 and 3 and lowering those for 9 and 2.

I'm looking at how the class 3 bias should move: its over-prediction disappeared when I scaled the H/V features, so the earlier −0.8 was probably too large. I'll try a milder −0.3 and see whether it brings class 3 back into a usable range.

Checking the step-5 column totals, class 9 is predicted about 3,800 times, far too often, while 1 and 3 are almost never predicted. I'm going to keep the step-5 Gaussian base and make small bias changes: raise 1, lower 2 slightly, and try a mild adjustment for 3 instead of the earlier −0.8.

I'm working through the per-class biases from the step-5 counts: class 9 is predicted far too often, so I'd bring its delta down to about −0.5, while class 1 and class 7 are under-predicted and get small upward nudges.

Now I'm settling on the next set of bias deltas and deciding to keep the alpha values as they are. I'll go back to the step-5 Gaussian structure and rework the deltas, since centring and normalisation seemed to remove useful per-class energy information.
