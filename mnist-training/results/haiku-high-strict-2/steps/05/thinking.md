We're stuck around 30% and progress has slowed, so I need something more substantial. The main limits look like blurry features, a coarse 4x4 grid, and rough hand-made templates feeding a linear readout. I'm considering whether the conv layers could be shaped to encode more spatial detail, and I'm starting to ask what the final 4x4 pooled map actually keeps.

I'm working out the receptive field of the final 4x4 map: each cell covers about 16 pixels and steps by 8, so the grid is coarse, though orientation channels still keep some direction. Max pooling after ReLU may keep stroke presence better than averaging. Hand-designing conv2 detectors for corners and stroke ends looks hard, so I'm weighing whether to accept a ceiling in the 45–60% range.

I'm comparing the mistakes in the templates: the 1-as-3 and 7-as-3 errors look like the 3 template overlaps with 7's strong top bar while missing its diagonal, and the 3 template's right-side bows get penalised by 7's features. Under the Gaussian scoring, the weak 3 norm and the overlap on the top bar may explain why 7 gets pulled toward 3.

I'm checking whether the 3 template's overall strength explains the bias: if the features are weaker than the scaled templates, the templates with larger total energy would win, and 3 may be one of those.

I'm noticing the classifier overpredicts class 3 by a wide margin, along with 2 and 6, while 7, 9, 1 and 5 are underpredicted. That suggests per-class bias terms are off rather than the templates alone, so I'm considering a calibration step that lowers the biases for 3, 2 and 6 based on these counts.

I'm thinking the 9 template may be the real problem: the network predicts 3 for 9 far too often, so the 3 template likely overlaps with 9's top loop and right stem. I'm also considering whether per-class bias adjustments for 3, 2 and 6 could help, but I'd rather fix the template shapes than just nudge biases.

I'm considering a sharper template-building step next, since my current guesses don't separate the digits well. A richer 4x4 descriptor that captures things like loops in each cell might help, and I'm weighing that against a simpler linear readout with centred templates and calibrated biases.

I'm weighing whether a centred, contrast-style template would separate the digits better, since the Gaussian form ties each class's score to its own norm. The score gap between two classes depends on both the template difference and the difference in template energy, so I need to keep both terms in view.

I'm reconsidering the template scoring, and a contrast-style centring would shift every class by a shared component. That changes the ranking only through the bias term, so it isn't a free change. I'm now weighing bias calibration against the confusion counts, since 3, 2 and 6 are over-predicted while 7, 9, 1 and 5 are under-predicted.

I'm tallying the prediction columns: class 3 is picked far more often than its roughly 1000 true cases, around 4400 times, and class 2 and class 6 are also heavily over-predicted. Column 1 barely shows up at all, so that's worth noting for the calibration.

I'm reading the prediction counts as a calibration signal: class 3 gets picked about 4,400 times against roughly 1,000 true cases, with 2 and 6 also heavily over-predicted, while 0, 7 and 1 barely show up. Tallying the columns that way, I'd lower the biases for 3, 2 and 6 and raise them for 0, 7 and 1, though I still want the template shapes fixed rather than relying on bias nudges alone.

I'm noticing that class 7 is almost never predicted, while class 1, 4, 5 and 9 are also under-predicted, so I'm considering raising their biases by roughly one unit. I'm unsure of the logit scale, so I'll treat ±1 as a rough starting point and check the effect against the feedback.

I'm noticing class 7 almost never gets predicted, so its template is clearly mismatched even for true 7s, which tend to be called 3. I'm checking whether the top bar and right-side strokes in the 7 template line up with the 3 template, and planning to sharpen the 7 template around its strong top bar and diagonal.

I'm checking whether the 7 template is weak in the lower rows, since its ink sits almost entirely in the top bar and a bit of diagonal, while the 3 template has real mass across rows 2 and 3. That mismatch would penalise true 7s against the 3 template.

I'm checking whether the 7 template's weak bottom rows could explain why true 7s keep landing on 3, since the 3 template expects ink there that a 7 lacks. That mismatch seems to push the scores the wrong way, but I'm not sure the feature scale supports that yet.

I'm thinking about a practical fix: keep the Gaussian readout but add per-class bias offsets to counter the over- and under-prediction, along with better 7 and 9 templates. Logit offsets on the order of one to two units seem like a reasonable place to start.

I'm now reconsidering the bias magnitudes: with the logit scale I'm assuming, the per-class bias differences look too small to explain the strong over-prediction of 3, so something other than the bias terms is probably driving it. I suspect the templates aren't scaled to match the actual pooled features, and I want to work through what a properly matched Gaussian classifier would look like.

I'm wondering whether the ink-scale effect is driving the 3 over-prediction, since bigger-ink classes would get larger dot products. Subtracting a mean template could counter that, though I'm not sure it's enough by itself, so I'm considering a different readout altogether.

I'm considering whether the conv2 channels 8–15, which are currently unused, could carry quadrant density features inside each 4x4 cell, giving finer spatial detail without changing the pooled grid.

I'm looking at whether quadrant-offset kernels in the unused conv2 channels could give sub-cell detail. The max over the pool's 2x2 positions blurs that, so the gain may be small, though the region information should still be nonzero.

I'm weighing whether finer sub-cell kernels in the spare channels would be worth the extra template work, since a 4x4 grid limits how much detail survives. I'm leaning toward accepting something in the 35–45% range and moving on with a reasonable fifth step rather than chasing a perfect template set.

I'm weighing whether to keep the Gaussian readout or switch to a mean-centred contrast version, and I'm leaning toward keeping the Gaussian since it has worked best so far. My plan is to refine the templates for the weaker digits and recalibrate the per-class biases using the confusion counts, while keeping the feature scale in mind.

I'm setting per-class bias offsets from the column counts: lowering 3, 2 and 6, and raising 7, 9, 1, 0, 4 and 5 by somewhere between about 0.5 and 1.5 logit units. I'm not sure of the logit scale, so these are starting guesses to check against the next round of feedback.

I'm raising the bias for class 7 by about 1.5 and lowering 3's, since true 7s keep getting pulled toward the 3 template. I also want to check whether the 7 template's lower rows are weak enough to make the 3 template score higher for a 7's features.

I'm checking the feature scale now: pooled max responses from a horizontal-bar kernel could reach about 5 on a full-width stroke, so the features may be much larger than my template values assumed.

I'm realising the orientation channels produce much larger responses than the density channels, since a horizontal or vertical stroke sums to around 5 while density stays near 1.5. That means the Gaussian readout is effectively weighting the orientation features far more heavily, which skews the class scores in ways the per-class bias offsets alone won't correct.

I'm now seeing that the horizontal and vertical orientation channels respond much more strongly than the density ones, which would make the 3 template win on anything with horizontal strokes. I'm thinking the features need per-channel rescaling, with estimated magnitudes for the orientation channels around 2 to 5 and the diagonals around 1 to 2.

I'm estimating magnitudes per channel: the diagonal and density features probably land around 2 to 4 on a stroke, so the scales are closer than I first assumed.

I'm checking the feature scale again: the density channels and the orientation channels may both land around 2 to 4 on a stroke, so a single shared scale of about 3 could fit better than 1.5. I can't pin this down without data, so I'll treat the scale as uncertain and let the next round of feedback settle it.

I'm giving the vertical and horizontal orientation channels a lower weight of about 0.6, since their responses run much larger than the density channels and are skewing the scores toward the 3 template. The diagonal channels are weak in magnitude, so I'm raising their weight to about 1.5 so they contribute something meaningful, and I'll keep the bias offsets from the feedback alongside this change.

I'm rescaling each channel's contribution: the diagonal channels get a higher weight so they count for more, and the bias offsets come from the feedback, nudging 0 and 1 up and 2 down.

Still tuning the per-channel weights and bias offsets for the Gaussian readout...

Still tuning the Gaussian readout, now with a per-channel scale: I'm lowering the vertical and horizontal orientation weights, which run large, and raising the weak diagonals. The bias term is recomputed from those scales, with per-class offsets taken from the column counts.

I'm finishing the per-class bias offsets, nudging the weaker digits up and the over-predicted ones down.
