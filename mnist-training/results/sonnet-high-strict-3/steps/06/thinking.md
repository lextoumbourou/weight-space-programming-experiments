The bias tuning keeps swinging back and forth, so it's clearly overly sensitive, and now 8 cases are over-predicted at 4700. The real problem seems to be that the underlying features are weak, so I should focus on making the discriminative features more reliable instead of fiddling with the bias.

I'm weighing whether to drop the bias tweaks and instead build a finer spatial picture of the ink, using many channels that each see a shifted part of the blob, paired with hand-drawn templates from simple strokes.

I'm considering a full-resolution design, but the template idea would mean running the network on drawn inputs, which I shouldn't do. Instead I'll rework the fc layer using what the existing spatial features show about cell positions.

I'm working out the spatial coverage of each pooled cell: the 4x4 grid cells cover input rows roughly 4i to 4i+15, with centers at about 7.5, 11.5, 15.5 and 19.5. That puts the middle of the digit between the second and third cells, so the layout is roughly symmetric around the image center, and I'm about to check how the kernel fits into that.

I'm noticing the 8 bias jumped by 1.1 and the predictions for that class exploded from 259 to 4700, so the logit gaps must be very small relative to the bias steps. The fix is probably to shrink the bias adjustments and rely on cleaner fc weights, with fewer but stronger cues.

I'm reasoning that the logit scale is too small relative to the biases, so the feature contributions are being swamped. Scaling the fc weights up (around 3 to 8) should let the features dominate, and then the biases would need to be scaled to match, since the offsets grow with the weights.

I'm computing the predicted counts for the 8 class, which come to about 4470, and the 1 class at roughly 1676. Since a bias change of 1.1 previously shifted predictions by about 17x, the sensitivity is around 0.4 per log-ratio. Scaling the fc weights by 3 and adjusting the biases to match looks like the way to go, with the 8 bias lowered by about 0.6 and the 1 bias by about 0.2.

I'm tallying the remaining class counts against the old bias shifts, and the 6 class is the outlier: only 13 predictions, so its bias needs a much larger bump, around +1.7.

I'm halving the logit scale: doubling the fc weights and biases together so the relative shifts stay the same while the features carry more weight.

Scaling the logits together with the biases wouldn't change accuracy, only the loss, so I'll leave the scale alone and just adjust the biases, damped to about 70% of the computed deltas to avoid oscillation. Class 6 is almost never predicted, so it needs a bigger push, with its horizontal bottom and left vertical strokes strengthened.

I'm settling the biases with a damped update, moving each one about 70% of the way toward its computed correction so the predictions don't oscillate. Class 6 gets the biggest bump since it's almost never predicted, and I'm also thinking about strengthening its stroke features a bit.

Still tweaking the class 6 weights, adding extra stroke terms to boost its features since it's almost never predicted.
