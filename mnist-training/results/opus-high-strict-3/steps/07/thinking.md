I'm at about 70% and need a bigger structural change rather than tweaks. Cosine template matching on max-pooled orientation features seems to be the main limit, and I'm wondering whether the fully connected layer could be made more discriminative. Improving the features through conv2 to pick up parts like loops, endpoints, and junctions is another route, though it looks hard. I also suspect the 4x4 max-pooling in pool2 might be discarding something important.

I'm weighing whether to use the confusion matrix to reweight the templates, shifting each class's template away from the classes it's most often confused with. The idea is that this would sharpen separation along the difference directions between confusable pairs, similar in spirit to LDA. The worry is that hand-built templates and real features may not match in scale, so the adjustment's magnitude is hard to set, and the earlier negative-evidence step ran into trouble for that reason.

I'm now considering whether the real problem is the mismatch between the feature vectors and my templates: real inputs activate areas the templates don't expect, so cosine similarity depends heavily on template support. I'm weighing whether plain ink templates or a combination with orientation features might do better than the current approach, and I'm not sure whether improving the conv1 bias would help.

I'm noticing the 3→5 confusions got worse once I slanted the templates, which suggests my 3's upper arc is sitting in the wrong place, maybe too wide. Both digits share a bottom bowl, so the distinguishing part is the top, and my 3 may not be capturing that well. I'm also starting to look at the 8→1 errors, where narrow, slanted 8s seem to be landing on the diagonal stroke of the 1 template.

I'm looking at the 8→1 confusions again: the union of slanted "1" templates includes diagonal strokes, so narrow slanted 8s pick up the 1 template. 4→1 shows the same pattern, and the 1 bias is already at -0.3. I suspect a missing penalty for ink appearing where a template has none, though my earlier attempt at negative evidence ran into trouble.

I'm considering a different scoring formula: a nearest-centroid style logit that subtracts a scaled penalty for template norm, so oversized templates like the 8 and 1 don't win by default. The scale mismatch between hand templates and real feature activations is the obstacle I hit before, so I'd need a small coefficient, perhaps around 0.3, and possibly per-class biases.

I'm considering whether a zero-mean adjustment to the templates could stop compact templates like the 1 from winning on the dense center ink that 8s produce, by subtracting a per-class constant so the score isn't driven by raw template mass.

I'm considering a zero-mean version of the templates: subtracting each template's average so every class's weights sum to zero. That would stop the total amount of ink from favoring whichever class has the most mass, which could keep the dense center of an 8 from pulling it toward the compact 1 template.

I'm wondering whether a "hole" feature, built from negative weights on ink with a positive bias so it fires where the stroke is absent, could help separate the 8s from the 1s. The difficulty is that max-pooling only tells me whether an empty spot exists somewhere in a region, so the signal may be too coarse to be useful.

I'm weighing whether empty regions in the input could serve as negative-evidence features, since holes and gaps separate pairs like 3/8 and 5/6. Channel budget in conv2 is tight, so I'm considering dropping one shift and keeping the rest.

I'm considering whether the 4 conv2 shifts are worth their channel cost, since coarse 4x4 max-pooling may be losing detail. Another option is designing conv2 channels as larger part detectors, like loop tops or left vertical strokes, spanning about 14x14 input pixels. With only nine steps left, I'm leaning toward feedback-driven pairwise adjustments to the templates instead.

I'm considering a perceptron-style update: for each confused pair d→k, nudge the template of d toward the confused samples and push the template of k away, using the templates themselves as stand-ins for the data.

I'm working out a closed-form contrast adjustment: for each class k, subtract a term that penalizes features a commonly confused class d has but k lacks, weighted by how often d is mistaken for k. The matching bonus for the confusing class d would be the complementary piece, so both templates shift apart along their differing features.

I'm settling on a targeted contrast step: for each class, penalize the template features that its most common confusers have but it lacks, and reinforce the ones that set it apart. I'll use a gain of about 2 and keep the step 6 templates as the base.

I'm settling the bias question: I'll leave the step 6 biases as they are. The actual change is a closed-form contrast on the templates, where each class is penalized for features its common confusers have and it lacks, and reinforced on the features that set it apart from them.
