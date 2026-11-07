I'm still around 64% accuracy and need a bigger change. The worst failure is zeros being classified as 2s, 221 times. My zero template is probably too large, since real zeros are narrower and often slanted, and I'm checking whether the template's shape is what's pulling them toward 2.

I'm weighing whether the templates themselves are the problem, since the 0 and 2 shapes share a top arc and a bottom horizontal, and the difference is mostly in the lower strokes. Cosine similarity on positive-only templates doesn't penalize mismatched parts much, so the feature vectors may be dominated by shared components. A centered or discriminative scoring could weight the differences, but I'd need to estimate the scale of the features to make it work.

I'm weighing whether centering the features and templates would help, since the shared arcs of 0 and 2 may be inflating their similarity. Subtracting the data mean would make the logit spread more informative, though the template mean is only an approximation of it. Using the confusion counts to correct the per-class biases is a cheaper option, and the earlier overshoot suggests I should apply only about half the log correction.

I'm weighing whether centering the features and templates would make the 0 and 2 templates more discriminative, since their shared arcs may be inflating the similarity. Subtracting the template mean would account for the bias term, but if the real feature scale differs from the templates, that bias could be off.

I'm estimating the scale between the real feature values and the template values, since the centered logit depends on that scale to avoid over-penalizing the shared mean.

I'm settling on the scale factor s around 0.7, since the real stroke responses should come out a bit below the template values. Next I'm centering each class template on the mean of all the templates and normalizing the result, then weighting the features against that so the shared parts don't dominate.

I'm recentering the templates on their shared mean and scoring each class by how far the features sit along its centered direction, with a scale factor s to match real feature magnitudes. The bias term has to absorb that centering, so I'm setting it from the same mean. I'll keep alpha at 4 and watch for class 1 pulling in too much, the way it did with per-template centering earlier.
