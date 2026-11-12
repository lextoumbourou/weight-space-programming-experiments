The results are mixed: most inputs now land on class 5, class 8 never gets predicted, and 3 is being mistaken for 5 in 631 cases. I suspect the part detector features are misfiring, and the nearest-centroid approach with the alpha guesses looks fragile. What I really need is the actual feature magnitudes, but I can't see them directly. I could get at them indirectly by pointing the fc layer at a single feature group to probe its mean per class.

I'm working out how to probe the features indirectly: if the output logit is set to a feature minus a threshold, the confusion matrix row for each class would show what fraction of that class exceeds the threshold. Packing several features into the logits doesn't work cleanly, since argmax only reveals the largest one, though the loss value might still carry some signal. I'm weighing whether this kind of probing counts as legitimate use of the feedback, which seems plausible since the feedback is the only information available.

I'm weighing a probe that wires each of ten features into a separate logit, but argmax would only reveal the largest one per class, so I'd need about 26 steps to cover 256 features. That's too costly. I'll keep reasoning analytically and use the confusion matrix for global tuning instead. I'm considering dropping the part detectors: they seem to push 0 and 3 toward 2 and 5, and 3's two parts should carry a larger bias penalty than 5's one, which I want to check.

I'm checking whether the part detector penalties actually balance out for 3 versus 5, and the nearest-centroid results depend too much on guessed feature magnitudes to trust. A more robust option would be features that saturate at known values, so I'm wondering whether a ReLU could push them there.

I'm realizing ReLU alone can't cap a feature from above, so a clipped response would need a second layer to subtract a shifted copy. Pooling between the layers complicates that, since the difference only holds if the max is taken on each branch separately.

I'm working out a way to clip features to a fixed range by pairing channels: a ReLU at one level minus a shifted copy gives a saturating response, and I can apply the same trick again after the second convolution. That would turn the features into roughly binary presence indicators, which would make the nearest-centroid scoring far less sensitive to the magnitudes I'm guessing at.

I'm settling on naive Bayes log-odds weights, since features clipped to [0,1] would make the templates scale-free. To get clipped orientation channels I'd pair conv1 channels with a shifted bias, then take their difference after pooling.

Clipping the features by pairing ReLU channels still looks workable: subtracting a shifted copy caps each response at 1 after pooling. I'm now sizing the conv2 features, which would give roughly 8 saturated presence indicators per cell.

I'm planning to pick the conv2 features: the four orientation presences plus a loop, a closed-right, and a closed-left detector, with the last slot still undecided. Then I'll set up the fc weights from per-class templates, keeping each probability away from 0 and 1.

I'm settling the calibration for the saturating features: each one is a clipped presence value, so the naive-Bayes weights can come straight from the template probabilities. I'll scale the logits down since correlated features would otherwise be overcounted. The thresholds on the conv2 features set how binary they look, and that stays uncertain, but the clipping keeps everything in [0, 1]. Next I'm pinning down the conv1 kernel normalization so an aligned stroke gives roughly 0.7.

I'm checking whether a ReLU pair can clip the orientation response into [0,1], with gain 3 and bias -0.6 so aligned strokes saturate. I estimate the aligned response at about 0.85 by treating the kernel's positive region as covering most of a 2-3 pixel stroke.

I'm checking whether the 45-degree stroke response of about 0.35 still clears the threshold after the gain and bias, which gives roughly 0.45. Next I'm sizing the conv2 orientation features: each one sums the clipped orientation response over a 3x3 neighborhood, so a single aligned cell should be enough to register.

I'm settling how each conv2 feature turns into a presence value: a single 3x3-weighted sum, clipped to [0,1] after subtracting 0.5, and max-pooled over a small block so that a stroke within about 5 px of a cell center registers. Next I need to set the per-class template probabilities for each of those presence features.

I'm working out a ring-shaped loop detector on the clipped orientation maps, normalizing its kernel so a full loop at roughly radius two cells gives a strong response.

I'm settling the loop detector's normalization: the ring weights get scaled so that a full loop with every position aligned gives a response of about 1, and a half loop about 0.5, before clipping.

I'm choosing the eight conv2 features: four orientation presences, then a loop detector with a negative penalty at the center for filled cells, and then closed-side arc detectors that gate on the open side.

I'm settling on the eight conv2 features: four orientation presences, a loop detector, and then closed-side arc detectors, with the last slot going to a bottom-open cup shape. Next I'll set the per-location template probabilities and the naive Bayes logits from them.

Next I'm working out the log-odds weighting: each feature's template probability gets converted to a logit, scaled down by about 0.25 to account for correlated features, and I'm keeping the template probabilities in a moderate range so no single feature dominates.

I'm settling the conv2 receptive fields: each feature covers a 3x3 patch of pool1 cells, and across the two conv2 positions per cell the coverage spans roughly pixels 4 to 24. That puts each cell's center near 4r+7.5 with an effective blur of about 2.5 px.

Working out the feature threshold now: a single 3x3 weighted sum, with the center at 1 and the edges at 0.6, should register a stroke passing through the region, and I'm setting the gain to 1 and the threshold to 0.6 so that crosstalk stays small.

Still writing the conv1 and conv2 weight setup...

Still writing the fc weights and the part kernel normalization...

Still sizing the arc kernels and the part template peaks...

Still picking the part features for the loop and arc detectors...

Still writing the per-location part templates...

Still working out the part template peaks, dropping the ∩ and ∪ entries for loop digits since loops suppress arcs, and setting a small base probability for the orientation templates.

Still working out the template probabilities for the orientation features, using a Gaussian proximity term and checking how a stroke about 4 px off-center still registers.
