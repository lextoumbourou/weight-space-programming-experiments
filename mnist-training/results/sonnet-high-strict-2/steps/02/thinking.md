The model only predicts classes 1 and 8, and the loss is very high, which points to logits that are scaled too large. Classes with more positive weights seem to win, so I want to balance the per-class weight mass. My idea is to make the fc weights zero-mean across classes for each feature channel and reduce the overall scale.

I'm weighing whether to subtract each feature channel's mean across digit classes, so no class gets a generic advantage from features all digits share. I'm also considering per-class bias corrections and a smaller overall logit scale, but I haven't settled on the exact normalization yet.

Now I'm weighing a rescaling of the logits, moving the overall scale down from 1.5 to about 3 as a modest first guess, since the exact logit spread is still uncertain. I'm also thinking about alternately centering the weights across classes and then across cells within each class, accepting that the two passes won't fully satisfy both constraints at once.
