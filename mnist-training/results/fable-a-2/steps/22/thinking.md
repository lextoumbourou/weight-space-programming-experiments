The loss dropped to 0.6068 at scale 0.7, down from 0.6734 at 1.0, so the optimum probably sits somewhere around 0.5 to 0.6. I could test 0.5 to fit a parabola, but the scale will be retuned once the features are final, so for now I'll keep improving accuracy with probes and use roughly 0.6 in the classifier steps.

I'm checking which features separate the 7s from the 9s, since about 20% of 7s are still being misread. The 7's top bar seems to drift down into the row where the 9's loop sits, so the horizontal-energy measure overlaps. The cleaner difference may be the empty area under the bar on the left for a 7, versus the loop's left side and bottom for a 9.

I'm now thinking the 7s that look like 9s are probably the atypical ones, like those with a hook or serif at the left of the bar or crossbar 7s that form something loop-like.

Raising the 7's bias and lowering the 9's should fix a lot of this, since 7→9 errors outnumber the reverse 215 to 11, and I'm also seeing a similar one-directional pattern with 4→9 and 4→8.

Now I'm working through the per-class prediction counts against the true counts. Classes 8 and 3 are over-predicted while 4 and 7 are under-predicted, so I'm considering per-class bias shifts to equalize them, with the aim of a few percent of accuracy gain.

I'm going to set the per-class bias shifts in the scaled logits: up for 7 and 4, a little up for 0 and 5, and down for 8, 3, 9 and 6, since those are the classes being over-predicted.

I'm weighing whether to shift the per-class biases now, since the 7→9 errors outnumber the reverse about 20 to 1, which points to a boundary that's off by a lot. Combining the 7 and 9 shifts gives a logit difference of about 1.4, and I'm considering changing the scale to 0.6 alongside it, though that would blur the effect of each change.

I'm settling on a scale of about 0.6, since the loss still seems to be falling and the optimum probably lies between 0.5 and 0.6. The per-class bias shifts will go straight into the final logits after scaling.
