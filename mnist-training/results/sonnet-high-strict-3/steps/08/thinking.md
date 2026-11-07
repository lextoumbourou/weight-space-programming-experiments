The bias term seems too weak relative to the feature magnitudes, since class 8 keeps winning by a wide margin. If the features are larger than the α-based estimate assumes, the inner-product term dominates for ink-heavy classes, so I'd need a larger α to balance it.

I'm weighing whether to try centering the features or normalizing each class template to unit norm, and I'm thinking a larger α around 1.5 might balance the inner-product term for the ink-heavy classes. I also want to estimate how big the features actually are, since the bar-filter response from a stroke of that width would determine whether x sits well above or below what the α-based estimate predicts.

I'm now checking the feature magnitudes more carefully, since a stroke's response only roughly lands near 0.8 and the templates are misaligned with the real strokes by a few pixels. That weakens the match, so I'm raising α to around 1.2–1.3 and possibly normalizing per class to stop the ink-heavy classes from dominating.

I'm settling on α = 1.3 and checking it against the predicted class counts, since class 4 is still well below where it should be.
