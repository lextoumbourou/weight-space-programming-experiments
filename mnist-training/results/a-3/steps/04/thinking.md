The naive Bayes bias seems to be pushing predictions toward class 1, probably because the feature strength is set too high and the sparse class wins as a result. I'm wondering whether I should be looking for an approach that depends less on hand-tuned parameters like that scale.

I'm thinking about whether to improve the templates themselves, perhaps by centering each one on its center of mass so the shapes line up better. Feedback could also tune per-class biases, and a cosine-based score with mean-centering already reached about 60%.

I'm working out where the naive Bayes bias comes from: the feature scale may be overestimated, so present features contribute less than they should and the sparse class 1 ends up winning. Next I'm checking the effective receptive windows of the pooled grid cells against the digit's center, which lines up with a center near 7.5.

I'm weighing whether to drop the L0 bias term and switch to a cosine-style score instead. The real question is whether the coarse 4x4 presence features lose too much detail, so I'm considering a richer representation that keeps more spatial information, maybe by using the conv2 channels in orientation groups at shifted positions.

I'm weighing a nearest-centroid style score, where the logit is the feature vector dotted with each class mean minus half that mean's squared norm. That formulation depends on the feature scale, which I don't know precisely, so I'm thinking about estimating the expected feature magnitudes analytically from edge filter responses on ideal digit images.

I'm estimating the feature magnitudes from edge filter responses on ideal digit strokes, which suggests the scale of 1.5 may actually be reasonable rather than too high. Pooled edge values along a stroke come out around 0.85, and the convolution's neighbors bring the total to roughly 1.7 to 2.5, so I'm checking whether real MNIST ink ramps change that estimate.

I'm checking whether the 1-bias comes from the templates rather than the scale: an 8 image has many present features, and the class-1 template's negative weights would penalize them heavily, so the mismatch is probably in the template shapes themselves.

I'm considering clipping the presence probabilities to a narrower range, since naive Bayes punishes any mismatch harshly. A cosine-style score or nearest-centroid with softer templates might be more forgiving, and the calibration could come from feedback. Still, I think the real problem is the template geometry, so I'm leaning toward centering each template by its center of mass and blurring them more.

I'm considering a nearest-centroid style score instead, where each class template is compared to the features as a squared distance, so the penalties for missing and unexpected features are symmetric and less harsh than naive Bayes.

I'm weighing a nearest-centroid score with a moderate scale factor, so the logit gaps stay in a usable range and the penalties for missing and extra features are roughly symmetric. I also want the feature values normalized so a present feature sits near 1, though I can't check that directly from here. The plan is to combine edge features with center-of-mass template centering and that nearest-centroid scoring.

I'm settling on centering each template by its center of mass, computed as a stroke-length-weighted mean of the points and shifted so it sits at (14, 14) in pixel indices. I'll treat that as the centering target rather than 13.5, since most implementations land near 14, and I'm making sure the stroke coordinates map consistently to pixel indices.

I'm scaling the templates down slightly so the stroke centerlines fit inside the 20-pixel box, then computing each template's center of mass and shifting it into place. I'll swap the membership saturation to a softer form and tune the logit scale so the score gaps between classes stay usable.

I'm settling on a scoring weight of 0.5 for the template matching, since across roughly 128 features a mismatch on about ten of them would shift the logits by around five.
