The 58.8% result is worse, and the broad templates (8 and 3) are again producing most of the false positives. Under the naive Bayes model, broad templates win when features are present more often than expected, and real images seem to light up many features at low saturation thresholds, so the thresholds may be too low.

The NB approach is more sensitive to calibration, and the feature responses look like they're underestimating how broadly real strokes activate features. I'm considering whether to sharpen the features or widen the templates, and I'm leaning toward going back to step 2, which did best.

I'm weighing whether to tune the step-2 configuration, which was the best so far at 76.6%, by nudging its biases, since that should land around 78-79%. I also want a more fundamental fix, because real strokes seem to activate the features far more broadly than my model predicts.

I'm checking the diagonal filter's response to a vertical stroke, summing the weighted cells in the columns around it, and the normalized result comes out to about 0.37, which is a weak response.

I'm checking the horizontal filter's response to that same diagonal stroke, summing the weighted cells column by column across the three rows the stroke crosses.

Checking the diagonal filter's response to a 45°-off stroke gives about 0.32 to 0.37 after normalization, a substantial leak, so the features fire far more broadly than the templates assume. Subtracting a bias of about 0.15 still leaves roughly 0.2 of response, which likely explains why the real feature maps look so much fuller than predicted.

I'm now checking that the cross-orientation leak is what drives the NB failure: a 45°-off stroke fires neighboring features at roughly 70% presence, so every adjacent orientation looks present. My proposed fix is to sharpen selectivity by subtracting a fraction of the neighboring orientations' pooled responses before the window sum.

I'm working out the cross-orientation inhibition: an on-axis stroke gives about 0.65, a 22.5° stroke about 0.33, and a 45° stroke drops to zero once the neighboring orientations are subtracted.

Comparing the cosine-style response curve to a sharper conv1 threshold, the sharper threshold would suppress the 45° leak entirely but also cut faint or thick strokes that only reach around 0.4 to 0.5. Cross-orientation inhibition in conv2 avoids that trade-off because it works on ratios, so its effect doesn't depend on stroke contrast.

I'm testing whether cross-orientation inhibition still holds up when a window contains several true orientations at once. For a corner with horizontal and diagonal strokes both present, the subtraction should still leave a positive response, around 0.6. A curve with three orientations present pushes the diagonal response down to about 0.35, which is low but still positive, so I'm weighing whether that is acceptable.

I'm checking whether the leak really is about 0.35: the diagonal filter gives roughly 0.29 on a vertical stroke and the horizontal gives about 0.24 on a diagonal once the bias is applied, so with c=0.4 the 45° case drops to near zero while the on-axis response stays around 0.72.

I'm now checking how the window-level subtraction behaves when a single window holds an H stroke in one part and a V stroke in another, since the inhibition is applied to the summed response rather than cell by cell.

I'm checking how the cross-orientation inhibition plays out at the window level: an H stroke and a V stroke together in one window would leave the diagonal response negative and clipped to zero, while the H response still holds at about 0.57 per stroke after subtracting the leaked diagonal responses.

I'm weighing whether to sharpen the features or push the step-2 cosine system further, since both would benefit from less leakage. The naive Bayes version failed badly, probably because of that leak, but I can't yet rule out other causes like the saturation thresholds. The cosine approach already sits around 74 to 77 percent, so cleaning up the leak should help its specificity, though I'm not sure yet which path has the higher ceiling.

I'm going to revert to the step-2 cosine setup, since the leak looks like the main problem, and add cross-orientation inhibition plus a small conv1 bias increase to cut the 45° spillover. The biases will need recalibrating too, because sharper features mean less diffuse energy, so the broad templates won't be favored as strongly as before.

I'm considering whether to keep the step-2 cosine setup and skip the naive Bayes route, since the sharper features might make the biases unnecessary. I'd start with mild negative biases on the broad templates, roughly half of step 2's, and expect to adjust them after the next run.

I'm settling on small biases, about 40% of the step-2 values, with the broad templates given the largest negative offsets. I'm keeping the unexpected-feature penalty at 0.5, since cleaner features should make it more accurate, and dropping the hand-written rules because they were tuned on the leaky responses. For the 1 template, I'm weighing a single template against a fan: the single one had better recall but more confusions with 2, while the fan recovered recall at the cost of many false positives, so I'm looking for something in between.

I'm settling on two strokes for the 1 template, one near-vertical at slant 0.15 with full weight and a weaker one at 0.5, since the single stroke missed too many and the fan let in too many false positives.

I'm settling the bias values now, with conv1 sitting at about −0.15 on the 1 template, and holding the 7 crossbar at 0.3 since its recall looked fine last run. The orientation tuning after inhibition looks reasonable, with the 22.5° response around 0.57 relative to on-axis versus the model's cos(45°) of 0.71. The feature scale has dropped to roughly 0.69 on-axis, so I'll raise the conv2 scale to about 1/1.7 to keep features near 1 and keep the biases meaningful.

I'm setting the conv1 bias so the leaked diagonal responses fall to zero, and I'm using a cross-orientation inhibition weight of about 0.35 to 0.4 in conv2. I'm leaving the endings as they were in the previous step, and I'm not including the 90° orientation in the inhibition.

I'm settling the cross-orientation inhibition at c=0.35, which takes the residual leak to zero while the on-axis response stays near 0.63, and I'm setting the feature scale to 1/1.6.

I'm settling on a step-5 setup: the step-2 code with a small negative bias on the orientation responses, cross-orientation inhibition in the second layer, a two-stroke template for the 1, and a crossbar for the 7. I'll also use modest per-class biases and keep the automatic penalties, dropping the hand-written rules.
