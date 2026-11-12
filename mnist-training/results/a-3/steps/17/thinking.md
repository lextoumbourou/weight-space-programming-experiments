I'm finding the β=0.04 setting is still leaving 8s under-classified, since a larger β penalizes 8 harder when its total is high. That suggests the feature value s is overestimated, so I'll try bringing it down to about 1.0. I need a more substantial idea, so I'm turning to the 8→1 confusion, where thin, slanted 8s are being read as 1s.

I'm checking whether the 8→1 confusion comes from the 1 template's central-column features matching a narrow, slanted 8, since real 8s should show horizontal edges that a 1 lacks. My 8 template may simply be too wide compared with real MNIST 8s, so I'm considering adding a narrower 8 variant.

I'm weighing a narrower, slanted 8 variant against the current template, since a tilt of +0.3 gave 253 correct on its own, but unioning the two would broaden the template and let big templates suffer from the absence penalty. A max over variants isn't available in this linear readout, so I'm looking at tuning the scoring more simply, though the expected gain looks small. I'm also wondering whether feedback from the confusion matrix could be used to probe per-class feature distributions.

I'm considering using each probe step to read out class-conditional feature statistics, by setting up logits so that the argmax reveals whether a feature exceeds a threshold. Only the lowest-loss step counts toward the score, so exploratory probes cost nothing, though one probe might only cover about nine features at a time.

I'm thinking about using the argmax of the output layer as a quantizer: with lines of increasing slope, each class's logit wins over a different interval of one feature, so a single probe step could reveal a 10-bin histogram of that feature per class. That only gives one scalar per step, though, which is far too little to cover 256 features, so I'm weighing whether probing a few discriminant directions would be more useful.

I'm weighing whether the per-class feature statistics could come from the feedback itself, using a probe where argmax reveals a binned histogram of one scalar per step. That would only give one number at a time, so I'm considering whether a total feature-sum probe is worth one of the remaining steps to calibrate the feature scale.

I'm thinking about whether the feedback could calibrate the feature scale, for instance by summing all features and reading the per-class histogram from the confusion matrix. A probe like that would show whether my assumed feature magnitude matches reality, which would explain why the β experiments went the wrong way.

I'm sketching a probe where each class's logit is a linear function of the total feature sum S, with increasing slopes and offsets so the argmax bins S into ranges. That would reveal the per-class distribution of total feature mass, and I'm thinking the thresholds should be spaced geometrically from about 10 to 180 with a large scale factor for crisp separation. I'm also wondering whether the same trick could extend to measuring per-class means of individual features.

I'm going to probe the total feature sum S so I can see the real feature scale per class. Comparing each class's mean S against its template mass gives a calibrated scale factor, which should show where the templates are over- or under-predicting. The bins will be coarse, so I'll space the thresholds to cover the likely range.

I'm settling on thresholds of roughly 20 to 120 for the total feature sum, then I'll run the probe with a=5 so each feature's weight scales with the class index.
