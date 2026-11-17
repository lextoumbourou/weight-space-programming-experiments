The texture numbers split the two classes clearly: about 57% of cat images exceed the edge threshold against roughly 73% of dog images, a gap of about 16 points. That makes texture a useful signal for dogs, though with a better threshold it might reach around 58–59%. I'm wondering whether the difference comes from orientation or from scale, since cat photos often look smoother and blurrier, perhaps because they were taken indoors in low light.

I'm weighing whether the gap comes from orientation or scale, and probing the horizontal, vertical, and diagonal energies to see which separates the classes. From two loss values at different thresholds, I'm estimating the mean shift and spread of the texture measure, which comes out to a modest separation between the classes. The optimal weight for texture alone depends on that shift relative to its variance.

Using the texture threshold alone gives a weight near 1.24 and a loss around 0.676, about 57.5% accuracy. Next I want to build a combined baseline, but texture is tied to many edge features and green cues too, so individual probes will be confounded. I'll compare each feature against texture instead.

I'm checking whether the texture signal is spatial, comparing the centre of the image against its border, and whether the top and bottom halves differ. Brightness comes next as a separate probe.

I'm planning the next probes: colour warmth, whether texture differs between the centre and the border, top versus bottom, and orientation contrasts. I'll also check a nonlinear low-texture feature, since the low tail looks like a strong cat signal. After that I plan to build an incremental model and watch how the loss changes with each added feature.

I'm weighing whether a combined model with per-feature weights will be worth building now, since the loss can only reveal a feature's value if I know its scale, and the confusion-matrix differences give me the signal but not the spread. Fitting the weight from two different weight settings would cost more steps, so I'm leaning toward a reasoned guess for the scale.

I'm thinking about the weight for the combined model: the optimal weights depend on how the features are correlated, and I could solve for them directly if I knew the mean differences and the covariance. Since that would take many probes, I'll instead adjust each weight greedily against the actual loss, since along a single coordinate the loss is nearly quadratic and two evaluations should be enough to locate its minimum.

I'm working out how to estimate each feature's weight from the loss values at different thresholds, treating the loss as close to quadratic along each coordinate. Two evaluations per coordinate should pin down its minimum, and the confusion matrix can supply the separation directly where the threshold sits near the median. I'm leaning toward checking which feature family separates the classes best before committing to that plan.

I'm now going to build a baseline combining texture and green, and maybe add a smoothness feature. I'll probe the colour features on their own first, starting with brightness and warmth, since those are mostly independent of texture.

I'm planning to check whether a brightness feature separates the classes, with a threshold near 0.55 and weight around 1.5. I'll test whether the confusion matrix can give me its signal while the loss tracks a second feature in the same step.

I'm estimating how much the loss changes when a new feature is added on top of texture, which gives a conditional gradient but leaves both the linear and quadratic terms unknown. Each step therefore yields about three numbers, and the confusion matrix shifts along with them.

I'm working out the green feature's distribution from its fractions above threshold, since it looks skewed rather than Gaussian, so the single-probe model may not fit it cleanly.

I'm estimating the texture feature's spread from the class fractions above threshold, assuming roughly Gaussian distributions with equal variance. Combined with the loss change, that gives a per-class separation of about 0.43 and a standard deviation of roughly 0.19 or 0.54. I'm about to check that scale against the threshold-0.5 probe.

Checking the two candidate values of σ against the observed loss at threshold 0.5: the smaller root gives about 0.718 and the larger about 0.735, with the observed 0.7235 falling between them. I'm also weighing the tail fractions at that threshold, roughly 2.4% of cats and 0.7% of dogs.

Working out the spread of the texture measure, the tail fractions don't fit a clean Gaussian at σ≈0.19, so the distribution is probably skewed. Settling on σ around 0.25–0.3, with cat and dog means near 1.05 and 1.17, gives a separation of roughly 0.4. Texture is clearly a strong signal, so next I want to see which sub-feature within it carries the most separation.

I'm going to split texture into its components next: horizontal, vertical, and diagonal edge energy, plus fine spots, each probed at a rough median threshold since I don't know the real medians. Assuming roughly equal channel contributions and that horizontal and vertical edges dominate diagonals in natural images, the comparison between those sub-features against the 16-point total gap should show which orientation carries the most separation.

I'm considering spatial probes next, such as whether texture differs between the bottom and top of the frame, since dogs often stand on ground. I'll also try incremental steps that add one term at a time, though I want the individual probes for clearer per-feature results.

I'm setting up a brightness feature next, with a threshold around 0.55 and a weight of about 1.5, checking whether it separates the classes on its own.
