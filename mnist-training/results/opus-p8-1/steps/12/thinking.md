The last attempt came out worse, with the output collapsing onto class 8. Edge cases seem to be producing diffuse responses, so I need a different strategy. One option is to estimate class-conditional feature means directly from feedback, a data-driven nearest-centroid approach. That fits the rule that feedback is the only signal I get, but measuring 640 class means would take too long. Another angle is that the loss is a single scalar depending on all parameters at once.

I'm checking whether a single scalar loss could reveal a per-class statistic: setting one logit to a scaled feature gives a linear combination of feature means, though that alone is not enough. Pairing that with the confusion matrix might recover per-class information, but each step only yields a limited number of numbers, so I'd need to encode several binary tests into the predicted category.

I'm checking whether a per-class sign test can be read out of the argmax: each combination of three feature comparisons gets its own logit, so one step could estimate three binary probabilities per class. That would still be too slow for all 64 features, so I'm looking at the per-class confusion counts from step 9 for a more targeted fix.

I'm looking at the per-class diagonal counts from the last confusion matrix, where a few classes lag well behind the rest. Rather than a dense per-pixel template, I'm considering a coarser grid: a fixed conv stage that takes the maximum over small blocks, so each feature becomes roughly "any ink in this patch," and a linear layer on top of that.

I'm considering whether the 4x4 max-pooling and conv taps could approximate a local average of ink on a 10x10 grid, which would be closer to grayscale density than to dilated strokes. Nearest-centroid on downsampled digits with true class means tends to reach around 80%, though my hand-built templates only got about 64% with HOG-style features. I'm also wondering whether my template geometry is off because the digits aren't centered by center of mass, and I'm thinking about calibrating the per-class templates with probes at coarse resolution.

I'm weighing whether to estimate per-class feature statistics through probing, which would take many steps. Using the confusion matrix to adjust moderately seems more practical than a full probe sweep.

I'm weighing whether binarized probes could estimate per-class feature statistics faster than a full sweep, since each step can test three thresholds at once. With about 39 steps left, I'd have to spend roughly half of them on probing, which might still leave room to fit the weights.

I'm considering whether a naive Bayes classifier with log-odds weights, built from per-class binary feature probabilities, could work better than the template approach, but that would need binary features, and the relu outputs aren't bounded. I might be able to get near-binary features by bounding the ink detector at the conv1 stage, so each pixel contributes a capped value.

I'm weighing a Bernoulli naive Bayes classifier on coarse presence features, where each class gets a per-cell probability of ink, and the decision is a sum of log-odds over those cells. That would be closer to a binarized template match than the earlier approach, and it could plausibly land in the low-to-mid 80s if the coarse grid holds up.

I'm weighing whether measuring per-class feature probabilities through binary tests is worth the steps. Each test gives only a few numbers, so a full sweep is too slow, and I'd need a different way to read out several features at once.

I'm weighing whether my hand-drawn templates are the real bottleneck, since they come from single drawings and don't match how MNIST digits actually look. I'm checking whether the orientation of the "1" and the bar of the "7" line up with typical examples, and whether the open-top "4" needs redrawing.

I'm weighing whether to probe the 16 conv2 channels for more specific detectors instead of relying on one template per class, since the edge-based line detector stumbled on thick strokes and curves.

I'm considering conjunction detectors in conv2 instead of single-orientation energies, such as a loop detector that fires only when horizontal and vertical strokes all surround a region, which should separate 0, 6, 8 and 9 better.

I'm picking out a loop detector in conv2: horizontal strokes along the top and bottom of a patch and vertical strokes on the left and right, with a negative center, so it fires when at least three of the four sides are present. Loop sizes should separate the classes: 0 has a large loop, 6 and 9 have one loop at the bottom or top, and 8 has two loops. That looks like a strong feature.

I'm laying out the conv2 channels: four orientation energies, an ink-sum channel, and a small loop detector. For the large loops, I'm checking whether two vertical strokes spaced about 8px apart at pool1 offsets 0 and 4 can cover a 0's inner width, since a 5x5 patch only reaches 14px.

I'm sketching a loop detector for conv2: the ink channel at pool1 would need positive weights on the top, bottom, left and right sides of a patch, with a negative weight at the center, plus a negative bias so it only fires when most sides are present. I'm thinking about two sizes, a wide one for 0s and a narrower one for 8s, and the sizes that would separate the loop classes.

I'm sketching a loop detector for the conv2 stage: positive weights on ink at the top, bottom, left and right of a patch, with a negative weight on the center, so it only fires when all four sides are inked and the middle is empty. Since the ink presence values sit around 1 and thin strokes come in weaker, I'm weighing whether to raise the gain on the ink detector so the inputs stay usable.

I'm weighing a loop detector built from summed ink along each side of a patch, since a single max-based test can't be expressed linearly. The sides would be averaged over a few cells so that thin or uneven strokes still register, which should make the feature less brittle. I'm also noting that real MNIST loops are often left open, particularly for 6s and 9s, so the detector has to tolerate small gaps. The question is whether building this would pay off more than refining the templates.

Now I'm laying out the loop-detector features for the classifier: a big and a small loop detector alongside the orientation energies and the ink channel. The fully-connected layer would use templates for the orientation channels, with hand-set weights per class for loop presence on a 4x4 grid. I'm working out where a loop centered at a given image row lands in the pooled cell grid.

Working out the loop-detector geometry now: the big loop's sides sit about four pixels from center, which is narrower than a 0's radius, so the detector would only catch part of it.

I'm weighing a tube-style big loop detector that keys only on the left and right vertical strokes with an empty center, since a 0's interior is too tall for a top-and-bottom version to catch. It would respond to 0s but also to some 4s and U-shapes, so it may not separate classes cleanly.

Now I'm sketching out a small loop detector for conv2, with its sides about two pool1 cells from the center to match the radius of 8s, 6s, and 9s loops.

Now I'm checking whether a small loop detector, with sides about four pixels from center and an empty middle, would still fire on a 0's outer strokes that sit further out.

Now I'm defining the 6-feature as a tube detector: vertical strokes on the left and right with an empty center, weighted so it responds to 0s, 4s and similar shapes. Next I'll move on to the 7 detector.

I'm now looking at a horizontal tube detector with strokes on top and bottom and an empty middle. It would respond to a 3's upper and middle arcs on the left side, though a 0 is too tall for it to catch the top and bottom edges.

I'm weighing whether the loop features need hand-set weights, and whether I can compute them analytically from the stroke layout instead of rendering anything. Applying the conv2 loop formula to the ink map feels like the same kind of template derivation I've been doing, so I'll allow it. The loop channels may need a larger weight than the rest so they aren't drowned out in the combined cosine.

Next I'm settling the conv1 gain for the ink channel: a wider Gaussian scaled so thick strokes give about 1.0 and thin ones 0.5 to 0.7, with a small negative bias to suppress faint pixels, so the loop detectors get a usable presence signal.

Still working out the conv2 channels: the small loop detector gets weighted sides at pool1 offset two with a strongly negative center, and a vertical tube detector covers the left and right strokes.

I'm settling the conv2 loop channels now: a small loop detector with weighted sides and a negative center, a vertical tube detector on the left and right strokes, and a horizontal tube detector on the top and bottom with an empty middle row. I'm planning to compute their responses from the unblurred ink map, then pool them.

I'm weighing how the loop features should be combined with the rest. Since the loop responses are roughly on the same scale as the orientation sums, I'm giving them a larger weight so they aren't drowned out in the cosine.

Writing the loop-template code now...
