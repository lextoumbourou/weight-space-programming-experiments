Accuracy is at 57% to start. The main problem is that 8 pulls in many digits, and 4 is often confused with 9 and 8, while 5 gets mistaken for 6. Cosine matching seems to favour the broad 8 template, so I'm considering a per-class bias that penalises 8 and boosts 4, and possibly reworking the 4 template to emphasise its vertical left stroke and closed top.

I'm weighing whether a per-class bias that penalises large templates like 8 would fix its over-prediction, though a simple bias has to be tuned from the confusion matrix rather than set by hand.

I'm weighing a per-class bias that penalises large templates like 8, since cosine matching lets its broad coverage win too often. The trickier part is that a linear score with a norm penalty could over-correct, so the bias probably has to be tuned from the confusion matrix. I'm also looking at contrast: a 3 matches the 8 template through its right halves, while the empty left side should count against it.

I'm working out whether a Euclidean-style score, f·T_d − ½γ|T_d|², would be a better fit than the normalised cosine, since that version builds in a per-class penalty on large templates like 8. The γ scale is the open question, because the feature magnitudes I'd expect from thick strokes aren't pinned down yet.

I'm weighing a Euclidean-style score with a per-class penalty on template norm, since a "3" should still lose to the broader 8 template on overlap alone, and the bias term may fix that. I'm considering a hybrid that keeps cosine and adds a bias proportional to each template's deviation from the mean norm.

I'm wondering whether the 3 template is simply mismatched with real 3s, since they seem to hit the left and centre area that the 8 template covers. Given how broadly thick strokes and curves activate multiple orientations, the real features may be far more diffuse than my templates, which would let the broadest templates like 8 and 6 win too often.

I'm now weighing whether to keep the normalised cosine or switch to a Euclidean-style score with a norm penalty, since that would penalise large templates like 8 directly. The scale factor is still the open question, so I'm thinking about whether a tuned per-class bias could do the same job.

Now I'm weighing per-class biases to offset the confusion pattern, nudging down the logits for 8, 6 and 9 while lifting 4, 5, 3 and 2.

Next I'm weighing per-class biases that push the 4s toward 4 and pull back the 8 and 6 templates, and I'm also considering whether the 5 template should be reshaped to separate it from 6.

I'm considering a per-class bias on top of the cosine scores, with each adjustment set from the log ratio of true to predicted counts so the over-predicted classes like 8 and 6 get pulled back and 4 and 5 get lifted. The template tweaks would go alongside that, and I'd tune the bias values against the confusion matrix rather than fix them by hand.

I'm going to set per-class biases from the log ratio of true to predicted counts, so the over-predicted classes like 8 and 6 get pulled back and 4 and 3 get lifted, then scale those values down to about 0.7 since the estimates are crude. The open question is the temperature β: 2 seems safe, though 3 could sharpen things if the 1.42 loss reflects flat logits.

I'm going to keep the cosine scoring and fold in a per-class bias taken from the log ratio of true to predicted counts, scaled down to about 0.8 so it stays conservative. I'm also planning a few template tweaks, like making the 4's left stroke more vertical and the 9's stem steeper, but I'll change them one at a time rather than all at once.
