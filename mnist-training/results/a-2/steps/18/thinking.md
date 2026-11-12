Loss ticked up a bit when λ went from 0.25 to 0.3, so I'm wondering if that's better calibration or just overshooting; I'll try λ=0.35 later. Accuracy is stuck around 72%, which means I need a structural change rather than tuning. One idea is to use the probe technique to estimate class-conditional means for a linear discriminant, and another is multiple templates per class built from conv2 features, which might act as roughly whole-digit detectors given their receptive field of about 13 pixels.

I'm weighing a few structural options: estimating class-conditional means for a linear discriminant, or improving feature richness with more orientations in conv1. I'm also considering the probability model itself, since the templates may be giving poor probabilities. The 6→0 and 9→0 confusions look like the 0 template is too broad at the center cells, so the horizontal stroke cues from the loops of 6 and 9 aren't being weighted properly.

I'm checking the 0 template's horizontal-stroke probability at the center cells: about 0.23, which is too loose, and a 6 with a horizontal stroke there would still favor 0. Other confusions (6→4, 9→4, 4→9, 4→1) are queued up for later. The next question is whether I can measure class-conditional feature statistics directly with probes, and how many probes a full table of 128 features across 10 classes would take.

I'm weighing a probe design where the classes are encoded as priority-ordered binary features, but that only gives clean marginals if the features are roughly independent, which they aren't for nearby cells. Using the softmax loss as the measurement signal might be a better route than trying to read off per-class distributions directly.

I'm wondering whether loss-based measurement could work here: if the logits are set up per class with a scalar feature, the average cross-entropy would mix every image together, which makes it hard to read off per-class effects. A cheaper route might be adjusting templates by hand where confusions concentrate, though that isn't very targeted. I'm also considering replacing the naive Bayes weights with something LDA-like that accounts for pairwise differences between classes.

I'm weighing whether the gap to 85% or more comes down to the feature design or to the parameters themselves. Template matching on blurred pixels already gets about 82% with true class means, so my orientation features with accurate parameters could plausibly reach 85 to 90%. That suggests the real limit is how well I estimate the parameters, which is where I want to look next.

I'm considering whether I can estimate per-class feature means more cheaply by reading a linear measurement off the confusion matrix, using small logits so the loss behaves roughly linearly in the features. The loss at small logits should approximate the average of each class's weighted feature response, though the higher-order terms need to stay negligible.

I'm weighing the binary-code probe idea against the loss-based measurement: the loss gives only one linear number per step, and the confusion matrix gives more, but a scalar histogram probe still reads just one feature at a time. Encoding three binary features into eight codes might recover joint information faster, so I'm checking how many probe steps that would take.

Each probe step could read three binary features at once by encoding them into eight codes, but that would spend nearly all the steps and leave nothing for anything else. A 1D histogram of a scalar gives a full distribution per class, though it still only measures one feature at a time.

I'm dropping the full probing approach, since three bits per step would eat nearly all the steps. Instead I'll try global hyperparameter tuning of the template spread, the saturation constant, and the base probability, plus λ, which might each give about a point.

I'm raising the conv2 presence threshold to 1.2 so that only longer strokes count, which should make the features more selective instead of saturating on diagonal curves. I'll also set λ back to 0.3 so the change is isolated to the feature behavior.
