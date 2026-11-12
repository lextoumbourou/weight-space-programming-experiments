The bias term is large even for the 1s, which suggests the real features run much bigger than my template estimates. The 8s have most of their positive mass in the center, so I probably underestimated the magnitude. Ink strokes near 1 that get dilated and averaged over the 3x3 pool could bring the real values down to around 0.7.

I'm weighing whether the features are simply about twice the size of my template estimates, since MNIST strokes are thicker than I assumed and the pooled values land nearer 0.9. That makes this a calibration question, so I could set the template scale to some k and see which value balances the classes, with k=1 already tilting everything toward 8. Before guessing at k=2, I want to work out the ink channel more carefully.

I'm estimating the orientation detector responses on a 3px stroke, where the kernel sums and dilation land near 0.9 and off-axis responses might push the real values higher too. Pooling a line through the center gives roughly 0.7, and adding curves or multiple strokes in the window gets closer to 0.9, against a template value of 0.49.

I'm thinking about replacing the bias with a weight so the centering scales with the image's total feature mass. That would make the score invariant to how large the features run, so I wouldn't need to guess a calibration factor k.

I'm reconsidering the classifier as a projection instead of a bias: removing the mean-stroke direction μ from each template makes the score scale-invariant, so I wouldn't need a calibration factor k at all.

I'm settling on scale: the projection drops the mean-stroke direction so the score doesn't depend on the feature magnitude, and I'll pick s around 3 since the feature norms look like they land near 5.
