Accuracy has fallen to 22%, and class 8 is absorbing too many predictions. I'm checking the 8 prototype: it has ink across nearly every cell, so its mean is high everywhere, which makes the quadratic bias term strongly negative while the linear term stays large, and I'm wondering why 8 still ends up winning.

I'm working through the scoring formula: the linear term grows with ink, and the quadratic penalty only partly offsets it for dense prototypes like 8. Since the optimum is when the mean matches each cell's feature, a spread-out, central template could still win for typical images.

I'm weighing whether the features' overall scale is the real cause: if the feature values are off from the prototype means, dense prototypes like 8 can pull ahead. Zero-centering the templates helped somewhat (43%), the quadratic version did worse (36%), and the step-5 version fell to 22%, so the features themselves look like the bottleneck.

Next I'm trying to pin down the feature scale, since my analytic guesses about it aren't reliable. One possible fix is to subtract the average prototype across all classes from each template, so the classes differ from each other instead of all looking like a generic blob.

I'm subtracting the average prototype across all digits from each template, so the classes differ from one another instead of sharing a generic ink blob that favors dense digits like 8. Working through the Gaussian score, I'm checking how the linear weights and the bias term change once the shared component is removed.

I'm trying the centered version: subtracting the average prototype across all digits from each template so the classes differ from one another. I'm checking how that changes the linear weights and the bias term, and whether it removes the shared ink component that favors dense digits like 8.

I'm noticing that the linear-plus-bias form gives exactly the same argmax as the original Gaussian score, so centering the templates won't by itself change which class wins. That points to the prototypes being mismatched to the actual feature scale, which I still can't pin down.

Working out the feature scale by hand: a full stroke in the first conv window gives roughly half the cells filled, and after pooling and the second conv the activations drop to something like 0.3 to 0.4 per template cell. I'll check whether the prototypes are scaled to match that range.

I'm thinking that the feature values in a 12x12 window are probably only around 0.25 to 0.3, so my MU_GAIN of 1.5 may be too large. If the prototypes are scaled too high, the penalty term dominates and lighter digits should win, yet 8 still wins, which makes me suspect the prototype scale is still off in some way.

I'm considering whether to set the gain to 1.0 so the prototypes match the feature scale, since the features seem to track occupancy. That's a guess, though, and I'm weighing whether it's worth trusting over the zero-mean templates that did best so far at 43%.

Now I'm tracing the feature values through the conv layers by hand, checking how a stroke's ink carries from the first 5x5 window through pooling to the final activations.

I'm estimating the feature scale from the conv layers: on a stroke the values sit around 0.4, and off-stroke they're closer to 0.1 to 0.2. That suggests a prototype gain near 1.0 to 1.3, so I'd lean toward 1.2, though I'm not sure the bias-based fix will hold up.

Checking the sink issue against the scale: at gain 1.5, the dense cells of the 8 prototype sit near 0.9 while the features are closer to 0.4, so every ink cell in 8 carries a large mismatch penalty. Yet 8 still wins, which means the penalty is not the whole story.

I'm checking whether the overlapping 12x12 windows, which share most of their cells, make the features so correlated that the quadratic classifier is ill-conditioned and driven mostly by edge differences.

Thresholding the features into on/off cells might make the templates robust to the scale mismatch, since the classifier would no longer depend on exact activation values. I'm considering a score built from binary occupancy, where ink-covered cells add to a digit's score and cells that should be empty subtract from it.

I'm considering a matched-filter approach instead: normalizing each class's occupancy template by its total so the scale mismatch matters less.

I'm considering normalizing each class's prototype so it sums to one, so that the score becomes a weighted average of the features over the prototype's region. That would stop dense prototypes like 8 from winning just because they carry more ink.

I'm noticing that normalizing each prototype to sum to one makes the score invariant to the overall feature scale, since there's no bias term left. The open question is whether spread-out classes lose out just because their mass is distributed, so I'm going to test that on a concrete image of a 1.

I'm testing a sum-normalized prototype, where each class's occupancy template is divided by its total so the score becomes a weighted average of the features with no bias term. That makes the argmax independent of the overall feature scale and removes the advantage that dense digits like 8 get from simply carrying more ink. Working through a concrete image of a 0 and a 1, the normalized scores come out in the right order, though I still need to check whether spread-out classes lose out just because their mass is distributed.

I'm settling on normalizing each class's occupancy template so it sums to one, which makes the score a weighted average with no bias term and keeps the argmax independent of the overall feature scale. I'll apply a constant factor to the weights, though I haven't settled on its size yet.

Trying a per-class normalization next: dividing each occupancy template by its total so that dense digits stop winning on mass alone. I'm also weighing a zero-mean variant to bring in negative evidence from empty cells, though I'm not sure yet which one will hold up.

I'm wondering whether to add a negative term from the empty cells, so that background cells also count as evidence against a digit rather than just being ignored.

I'm settling on the normalized prototypes: dividing each class's occupancy by its total so the score is a weighted sum of features with no bias, which keeps the argmax independent of the overall feature scale. I'm not yet sure about adding a negative term from empty cells, and the logits may come out small, though the predicted class should still be right.

I'm weighing whether a prototype score that is only a weighted mean of the feature values can still favor the wrong digit, since 7 and 1 share some of the same strokes.

I'm settling on the prototype weights: each class's occupancy gets divided by its total and multiplied by a constant of about 10, with a small floor so no cell is zero, and the bias stays at zero. I still need to check whether the floor changes the ranking between classes.

I'm settling on the normalized prototypes: each class's occupancy gets a small floor, then is divided by its total, with the bias set to zero. That keeps the decision independent of the overall feature scale and of how much ink each digit carries, and I'm now writing the code and a short explanation of why.

I'm settling on the normalized prototype weights, so the decision doesn't depend on the overall scale.
