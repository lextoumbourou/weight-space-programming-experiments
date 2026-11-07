I'm stuck near 60%, so the features and templates probably don't match the digits well. I'm weighing whether the conv1 bias and orientation detectors fit the thick MNIST strokes, and I'm also looking at how a simple nearest class-mean baseline on raw pixels does, around 82%.

I'm wondering whether a simpler approach would work better, like coarse ink density features with blurred pixel templates, since raw-pixel nearest class-mean already gets about 82%. Alternatively I could fix the 9→8 confusion, which is badly off at 502 errors. The 8 template's penalty seems concentrated on corners and edges where 9s rarely have ink, so 8 is hardly ever penalized, which would explain why 9s keep getting pulled toward 8.

I'm weighing whether a discriminative approach would fix the 9→8 problem, since the 8 template's penalty sits on corners and edges where 9s rarely have ink, so it almost never fires. Normalizing the templates differently might rebalance that, because the 8 template is the heavier one and gets shrunk the most under L2 scaling.

I'm weighing whether to bias-adjust again, since 8 is overpredicted and 9, 4, and 7 are underpredicted, and earlier adjustments did move 7 up. I'm also wondering whether the orientation features, blurred at 22.5°, smear loops and curves so that many templates light up at once and lose discrimination. Maybe a better feature built from conv2 could capture loops or closures more directly.

I'm considering whether to add finer pixel-density information in place of the redundant orientation channels, though a single tap on pooled ink doesn't gain much over the current grid. I'm also going back over how the conv1 response looks on real thick strokes, since the detectors may be mismatched to them.

I'm checking how stroke thickness affects the conv1 response: a 3px stroke gives a modest positive value after the bias, a 2px offset stroke gives a stronger one, and a thick stroke can cancel out to nearly zero at the center.

I'm considering a wider kernel core, roughly covering offsets up to 1.5 pixels, since the current narrow band seems mismatched to thick MNIST strokes, where the orientation response breaks down.

I'm considering edge detectors instead of the current line detectors, since their response should hold up better on thick strokes. The idea is to split each orientation into two polarities and combine them, so each stroke boundary gets picked up regardless of how wide the stroke is.

I'm considering whether edge-based features, with each orientation split into two polarities, would hold up better on thick strokes than the current line detectors. That would give 4 orientations at 45° spacing, which is coarser, but I'm not sure the gain is worth it.

I'm designing edge-based kernels instead, using a derivative-of-Gaussian profile that responds to stroke boundaries rather than stroke centers.

I'm checking whether edge-style kernels, which respond to the boundaries of each stroke, would be more selective than line detectors on thick digits. A 5x5 derivative filter only spans a short distance along the edge, so its orientation tuning is broad, and a plain bias may not be enough to sharpen it.

I'm weighing whether edge-based kernels would hold up better than line detectors on thick strokes, though a plain derivative filter may be too loosely tuned to orientation. A bias could sharpen it, but I'm honestly not sure which approach would do better. Before changing the features further, I want to check whether the templates themselves are the real problem by looking at which classes are performing well.

I'm now checking which digit classes are doing well and which are failing, and the 9 template is the main suspect. With the shear applied, the loop and stem of the 9 sit slanted in a way that may not match how real 9s usually look.

I'm wondering if the 8 template is simply too attractive to 9s, since it covers most of the 9's ink through its top loop and right-side stroke. The 9 template's penalty for stray ink doesn't seem to be the main cause, because removing the penalty still left 9→8 confusions near 300. So I'm looking at whether I can reduce the 8 template's pull without breaking its own accuracy.

I'm thinking the 8 template is too strong a pull on 9s, so I could try pushing its bias down and raising the 9's. Sharper templates might also make 8's distinctive features stand out better than the current blurred ones do.

I'm considering a contrastive weighting scheme that subtracts, for each class, the elementwise max of the other classes' templates, so features shared with confusers like 8 get suppressed and only the distinctive parts remain.

I'm now weighing a contrastive weighting that subtracts half of the elementwise max of the other classes' templates from each class, so the features 8 shares with its confusers get suppressed. I'm also considering dropping the stray-ink penalty and resetting the biases, though I'm not confident this will help.

I'm normalizing each contrastive weight vector so its score on its own template is 1, and starting with zero biases to see the raw behavior.
