Template matching is still stuck around 55%, so the current approach isn't working and I need something fundamentally different. I'm considering a linear classifier that uses hand-drawn digit templates on the raw image at finer resolution, since nearest-centroid on raw pixels reached about 80% with true means. I also want to check whether the feature and template alignment has a bug.

I'm checking the feature layout next: the flatten ordering and grid mapping both look right, and so does the max-pooling after ReLU. Re-deriving the step-one result also checks out, since everything mapping to class 1 is consistent with the nearest-template score. The thought cuts off while I'm looking at whether cosine normalization is the culprit.

I'm wondering whether the cosine normalization is the real culprit: templates with few strokes, like 1 and 7, end up with concentrated weights that score high on any input containing their strokes, while 8's diffuse template matches poorly even when the digit is an 8. A parts-based design with conv2 detectors for loops and endpoints might help, but that's complicated. Per-class biases and scales tuned from the confusion matrix could also add a few points.

I'm thinking raw-pixel features on a finer grid might match better than the orientation channels, since nearest-centroid on raw pixels with true means already gets about 82%. The bottleneck may be my hand-drawn templates, so I'm considering improving them through confusion feedback, along with per-class bias and temperature tuning.

I'm looking at why the 1s keep getting matched to 7 (177 cases). My guess is that slanted 1s line up with the diagonal channel of the 7 template, so I'm considering giving the 1 template a wider range of shears, from 0 up to 0.6.

Next I'm weighing whether to normalize the templates by a power of their norm, somewhere between full cosine and raw weights, since sparse templates like 1 and 7 are currently over-rewarded.

I'm going to rescale the normalized templates so their average norm matches the earlier scale. I'm also thinking about reverting to the step-7 convolution setup, since it scored slightly better than the cos^4 variant. The plan is to keep that config and try a power-normalization of p=0.5.
