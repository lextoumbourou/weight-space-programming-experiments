I'm working out how the column bits map to loop, vtube, and htube, and listing which combination each value stands for. Then I'm tallying the class-0 counts and adding up the loop total across the combinations that include it.

I'm checking the loop share for each remaining class: about 34% in class 2, 48% in class 3, 34% in class 4, and 32% in class 5. Class 6 comes out near 45%, and the htube share is largest in classes 3 and 5.

I'm weighing whether to build a naive-Bayes classifier from many binary probe features, which would take roughly 16 steps to cover 48 features and might reach around 75–80%. I'm also considering whether probes could instead be designed to measure a feature's discriminative value directly, or to estimate a class-conditional mean with finer resolution using the 10-bin quantizer.

I'm weighing how many binary features a single probe step can realistically carry, since each step returns one scalar per class and a few counts at most. Three clean tests per step looks like the practical ceiling, so with about 37 steps left the design has to stretch that budget as far as it will go.

I'm considering whether a classifier built on the probe results would work, using a naive-Bayes style score over the binary features. The catch is that our features are continuous, so I'd need thresholded versions of them, and I'm still weighing whether a clean binarization is possible within the network.

I'm checking whether a binary threshold can be produced inside the network, since the ReLUs and max-pooling only give unbounded, count-like values rather than clean 0/1 features. Measuring P(x > t) at a presence-level threshold might be a workable alternative to a true binarization.

I'm settling on binary presence features, such as whether a horizontal stroke appears in a given cell, and treating their weights as log-odds with the feature scaled to about 1 when present. Counting 4 orientations over 16 cells gives 64 features, which would take roughly 22 probe steps, leaving the rest for classification. I'm still checking whether a smarter probe design, like compressed-sensing-style combinations, could cover more features per step.

I'm considering whether a 4x4 grid of presence features would work, since max-pooling over larger windows might make horizontal strokes common, with probabilities around 0.6 to 0.9. Another option is to measure ink presence on a finer 10x10 grid with stride 2.

I'm now considering whether the loss itself could carry per-class information, since the label enters the cross-entropy and could be exploited if the logits were set up accordingly.

I'm working out what the loss tells me: it reduces to one scalar, a weighted sum of per-class means, so it can't separate classes efficiently. A confusion-style probe with three binary tests per step still looks like the better measurement. I'm doubtful that I can reach over 70% by reasoning about templates alone, so the probes would need to check specific templates.

I'm weighing whether the orientation-presence features, roughly 64 of them, could support a naive-Bayes classifier that reaches somewhere around 75 to 80 percent. I'm also considering whether a smaller hand-picked set of about 24 to 30 higher-level features would be more efficient to measure.

I'm considering whether the features could be made nearly binary inside the network, by having conv2 apply a large gain before the ReLU so the max-pooled output sits close to 0 or 1.

I'm checking whether the ReLU and max-pooling stages could be tuned to push a feature close to a clean 0 or 1, but the output stays unbounded, so the binarization only gets approximate.

I'm thinking that since MNIST pixels are mostly near 0 or 1, ink presence is already roughly binary, so a max-pooled "any ink in this cell" feature would be close to a clean indicator. I'm considering a shifted-tap setup over a fine grid to get those presence features directly.

I'm weighing whether a 10x10 grid of block-presence features is worth it, but at about 34 probe steps that's too costly. Shrinking the set to 256 features doesn't help either, since I'd still have to pick which ones matter. I'm wondering if the real problem is just which classes have weak templates, and the loop detector firing on 3 about 48% of the time already hints at where to look.

I'm noticing the loop detector is too loose: a horizontal tube can satisfy the four-side sum with partial coverage on the left and right. I'm considering checking only the middle cell of each side instead, so the test requires a stroke at the midpoints.

I'm settling on a plan: build a naive-Bayes classifier from probes of about thirty roughly binary, discriminative features, tune the bias and scale, and accept that the probe steps themselves give almost no signal per loss value.

I'm weighing whether a finer grid of ink-presence features is worth the probe cost, and concluding that a set of hand-chosen, discriminative features may be a better fit. I'm also considering folding the naive-Bayes log-odds into the existing template scores, and noting that each probe test can measure a threshold on any linear combination of the 256 pooled features.

I'm considering a data-driven template approach for the cosine classifier, measuring the probability of each orientation being present in each cell for every class, which would give 64 values and roughly 22 probe steps. I'm also thinking about whether a single probe could test ten class logits at once, which might be cheaper than measuring all the features individually.

I'm thinking about whether a thicker-profile orientation detector would hold up on wide strokes, with a center band of width three and slightly negative flanks, so that a solid stroke still registers as a line rather than a blob.

I'm testing a different orientation detector: a line kernel along each direction minus the perpendicular one, which should separate horizontal from vertical strokes without the flank problem. Thick strokes are still the question, since a wide horizontal stroke gives both sums the same value.

I'm settling on max-pooled single-tap line detectors as the presence features, and for the classifier I'd shift each one with a threshold in conv2 so anything below the cutoff drops to zero.

I'm weighing whether to probe 48 features instead of all 64, dropping the corner cells, since they likely carry the least signal for telling digits apart.

I'm settling on single-tap line detectors with a threshold around 0.3 as the probe features, since an aligned stroke should sit near 0.8 after the bias.

I'm settling on a threshold of 0.4 for the orientation features, since that separates selective responses from diffuse ones. With 64 features at three per probe step, that's about 22 steps, leaving roughly 15 for tuning the classifier. Loss values carry no per-feature information, so the probes have to rely on the test outcomes alone.

I'm considering whether a priority-style encoding could yield up to nine marginal readings per probe step, where each image's predicted category reveals the first present feature in an order. The catch is that the logit scaling would have to be exact, not just roughly geometric, for that to hold.

I'm working through how many distinct outputs a priority-encoded logit can yield, and whether the ratios between successive logit scales can be wide enough to separate the first present feature. I'm also checking that float32 precision still holds for comparing values that large.

I'm weighing whether the priority-encoded logits can be read as clean marginals, and concluding they can't: they only give sequential conditionals, not the per-feature probabilities naive Bayes needs. So I'll stick with the 3-bit coding at about 22 probe steps, even though that's expensive, and consider whether aggregated features at lower resolution would cut the cost.

I'm settling on a probe design for the next step: testing the horizontal channel at the first three cells, and I'm setting the presence threshold at 0.35.

I'm sketching a generic probe that takes a list of channel-and-cell tests and a threshold, so I can swap the list out at each step. The features are indexed as channel times 16 plus cell, with a zero bias on the second convolution, and I'm going through them in order rather than picking by importance.
