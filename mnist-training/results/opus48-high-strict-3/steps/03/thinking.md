Still seeing the predictions collapse onto 4, 8, and 1, and the loss rose to 3.31, so the model is now more confidently wrong. Normalizing the features helped a little, but the 4 and 8 templates still win out. My guess is that their central ink is shared across all digits and is swamping what separates them.

I'm now wondering whether the 4 and 8 templates win simply because they carry strong central ink, which correlates with every digit. I'm also suspicious that my coordinate alignment could be off, though the center estimate looks reasonable. The 4 template's full-width horizontal bar at the center may be the main culprit.

I'm considering that the discrimination is weak, so whichever template overlaps the generic central blob wins. Ideally each template would be positive where its digit has ink and others don't, and negative where it doesn't but others do. Since I can't compute a mean digit from the data, I'd have to hand-subtract the common central component, or revisit whether the blur and maxpool are smearing away the distinctive detail.

I'm weighing whether to nudge the decision by hand, biasing against 4 and 8 and toward the rarely predicted classes, but that only patches the symptom. The deeper fix would be sharper features, maybe edge or stroke detectors in place of the blur, though wiring those into the fc layer is more involved. I also want to revisit the scale, since a loss of 3.3 means the model is badly overconfident even when the argmax is unchanged.

Still checking why the templates for 4 and 8 keep winning: a correlation against the mean-subtracted feature means whichever template's ink lines up best with the common central blob takes the prediction, and the blur and pooling seem to be turning every digit into roughly that same blob.

I'm realizing the central blob dominates because the blur smears every digit into it, and blobby templates like 8 overlap it most while 0's hollow center scores poorly. Keeping more of the original shape should help, so I'm considering a sharper conv1 that's closer to a delta.

I'm switching the first conv to a single center-weighted delta so the 12x12 map keeps the digit's holes and strokes instead of blurring them into one blob, then sampling those cells into the 4x4 features.

I'm going to swap the first conv for a single center-weighted delta, so the 12x12 map keeps the holes and strokes rather than blurring them into one blob. That should let the 0's hollow center and the 8's loops stay distinct.

Now I'm switching the first conv to a single center delta, so the 2x2 max-pooling keeps the strokes and the holes instead of blurring them together.

Switching to a sharp center-delta first conv, I'm figuring the crisp 12x12 digit map will hold up better than a blur. Unit-norm templates on 0/1 features should give a dot-product gap around 4, so I'm setting the scale near 1.0 to keep the loss in check.

I'm going to make the first conv a pure center delta, so the max-pooled map keeps the strokes and holes. I'll keep the scale at 1.0 and hold off on any blur until I see how the sharper version does.

The max-pooling should pick out each inked pixel anyway, so this stays forgiving even with a pure center delta.
