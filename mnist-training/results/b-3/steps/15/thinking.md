At 69.1% the progress is slow, so I need a bigger gain. I'm weighing whether the classifier could be improved: it uses a nearest-centroid rule with identity covariance, and weighting features by inverse variance might help, since the max-pooled features with probabilities near 0.5 look noisy.

I'm considering whether a per-feature variance weighting could help, but a per-class variance would make the rule quadratic, and a shared variance per feature seems to de-emphasize features where the classes actually differ, so it's not clearly better. I'm also looking at the confused pairs (3/5, 2/3, 7/9, 4/9, 8/1) as targets for better features, and wondering whether tuning the ink penalty β (say 0.45 vs 0.55) could do more than the per-class bias corrections already do.

I'm comparing the 4→9 confusion next: the 4 and 9 templates both have a horizontal stroke around row 15, so that feature alone won't separate them. What should set them apart is the top of the loop, which a 9 has near row 4-5 and a 4 usually lacks.

I'm checking whether shrinking the plateau width, from 2.5 to 1.5, would make the templates sharper, though the 8px pooling window is physically real, so that may not be justified.

I'm noticing the pooling window only spans about 4 conv1 positions, not 8, so the plateau of 2.5 px is too wide and makes the templates blurrier than they should be. Dropping it to 1.5 would sharpen them, though I'd need to recheck the ink-term calibration since the template magnitudes would shift.

I'm weighing whether the plateau width is worth changing: reducing it from 2.5 to 1.5 barely shifts the windows near strokes, so templates stay broad mainly because of the σ=2 variability. Changing the plateau would also mean recalibrating β, which I'd rather avoid. I'm also wondering whether the orientation features help at all, and whether an ink-only test would show that.

I'm thinking about adding a second 7 prototype with a crossbar, since the European-style 7s are getting predicted as 4s. I'm also considering whether the 2→3 confusion could be addressed with a template that captures the 2's bottom horizontal stroke, and I want to check the predicted class counts against the expected distribution, since class 1 looks heavily over-predicted.

I'm checking the per-class bias corrections against the predicted counts: class 1 and class 8 are over-predicted, so they get negative adjustments, while 2, 4 and 5 are under-predicted and get positive ones. I'm about to fold these into the effective correction term.

I'm recomputing the per-class bias corrections from the new predicted counts, with class 4 getting the largest positive shift and class 1 the largest negative one. I'm also considering raising the scale factor to 1.6, since the loss kept dropping as it went up.

I'm adding a second 7 prototype with a crossbar, then setting the plateau width to 1.5 and the scale factor to match the recalibrated biases.
