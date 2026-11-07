Looking at the persistent confusions now: 2→8, 4→9, 7→9, and a few others. The column sums show 8 and 9 are heavily over-predicted, so I'm considering a simple log-ratio bias correction to pull those counts back down.

I'm weighing a per-class bias correction against the possibility that the templates themselves are the real problem. The 7 template's diagonal stem may be too shallow compared with real 7s, so I'm considering a steeper variant.

I'm considering whether to fit the biases from the class counts and then adjust templates, which would be cheaper and tell me more about the logit scale. I'm also thinking the scoring rule might need a distance-based form that accounts for template norms, though that's a bigger change. The loss and accuracy suggest I should try scale experiments later, since I can't yet tell whether errors are confident or the correct predictions are under-confident. For the templates, I'm planning a steeper-stem 7 variant with a shorter top bar, and a curved-neck 2 variant with an arc top and bottom bar.

I'm checking what a 2 looks like that gets mistaken for an 8: the 2's diagonal runs through the center, close to the 8's crossing strokes, and the real 2s may start their top arc a bit higher on the left than my template does.

I'm thinking the 2-vs-8 confusion comes from the 2 lacking the lower-left and lower-right side strokes that the 8's crossing loops have, so mean subtraction barely separates them. I'm considering a pairwise weighting that pushes each template away from its strongest rival, though that may need renormalizing to avoid the earlier scale blow-up. Whitening via the covariance across the ten templates is another option, but I'd be estimating that from only ten templates, which may not be enough.

I'm correcting the per-class bias with a damped log-ratio, roughly 0.8 times the log of true over predicted counts, which pushes 8 and 9 down and 3 and 4 up. The template tweaks for 7 and 2 will shift the counts too, so I'll keep the bias as a rough first pass.

I'm settling on a per-class bias correction plus template variants for 5 and 2, since the 5→6 confusion seems to come from the 6's continuous left side and the 5's open lower-left bowl.
