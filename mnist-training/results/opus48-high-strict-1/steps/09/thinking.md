Plateaued around 38–39% accuracy, with bias tuning giving only marginal gains. The core limit seems to be ink-silhouette template matching under heavy blur, so better features are needed, and the hole feature didn't help because it was too noisy. Now I'm looking at the persistent confusions, especially 4↔9 and 2↔8.

I'm weighing whether the 4 and 9 can be told apart by where the ink sits: a 9 closes into a loop at the top, while a 4 has an open top and a crossbar in the middle. The top-center region looks like the place to check, though I'm not sure yet which shape the 4 actually fills there.

I'm weighing whether to sharpen conv1 so the 12x12 map keeps finer detail, since max-pooling saturates and blurs the 4/9 distinction. Refining the templates for each confused pair might help too, but that would be slow with the steps I have left.

I'm thinking about sharpening the first convolution into a single-pixel center sample, so that max-pooling gives a crisp 12x12 silhouette instead of a blurred one. The idea is that a cleaner map might separate the templates better than the current version, and I'd test it as a single change.

I'm weighing whether to sharpen the first convolution into a single-pixel sample, so max-pooling yields a crisper 12x12 silhouette. Sharper features will have larger norms and may need a lower scale, but I'll keep scale 6 and let the loss guide me. The risk is that sharper features are more sensitive to exact stroke position, though center-of-mass centering should keep digits reasonably aligned.

Standard nearest-neighbor on raw MNIST does far better with many templates, and even a single class-mean centroid on raw pixels reaches around 82%. My hand-drawn templates are cruder than real digit means, and the 12x12 downsampling plus max-pooling throws away a lot of detail, which is likely why I'm stuck near 38%. I'll test a sharp single-pixel conv1 next, since it keeps more information than the 3x3 average.

I'm thinking about a milder version of the sharpening change, since replacing the 3x3 average with a single center sample could shift the feature statistics enough to break the bias calibration I just tuned.

I'm considering a milder sharpening instead, with a heavier center weight and small weights on the four neighbors, since that changes the feature statistics less than a full single-pixel sample. I'm not sure the gain is worth it, though, and I'm also thinking about whether a reliable second feature channel could separate the confused pairs more directly than any blur adjustment.

I'm considering adding orientation channels, a horizontal-edge detector and a vertical-edge detector, since 7 has a strong top horizontal stroke while 1 is mostly vertical. Still, the hole feature failed on noise, so I'm wary of the same risk here. I'm also thinking about setting that aside and just refining the templates for the worst confusions, like 7 against 5, 1 and 9, to squeeze out a few more points with less risk.

I'm now trying to separate 7 from 5, since both have a top horizontal bar. The distinction should come from the lower region, where 5 has its bottom curve and 7 has only a thin diagonal, so the 7 template probably needs negative weight there.

I'm going to try a moderate sharpening of the first convolution, with a heavier center weight and small weights on the four neighbors, and keep the templates, scale and biases as they are. I'll compare accuracy and loss against the previous step, and if it helps I'll push further, otherwise I'll revert.

I'm weighing a moderate sharpening of conv1, with the center at 0.5 and each neighbor at 0.125. Sharper features should give larger logits, so the loss could drop when predictions are right but rise when they're wrong, and I'll keep scale 6 and watch the result.

Trying a pure delta on conv1 (center weight 1) to get sharper features. Pool1 and pool2 take the max over 2x2 blocks, so each feature is a max over a few raw pixels, which should be reasonably robust despite the single-pixel sampling.

I'm checking whether a delta kernel at conv1's center makes the feature a crisp silhouette, where each feature is the max ink inside a 4x4 raw-pixel region. That's a different signal than the smoothed 3x3-average version, and it might separate the outlines better.

I'm second-guessing the delta idea: a binary silhouette would lose stroke thickness and overlap, which the averaged density still encodes, so I'll keep the current smoothing. That leaves me looking for another low-risk tweak, since a larger averaging window would only add more blur.

I'm considering whether to drop the density-based features in favor of a binary silhouette, but a silhouette would lose stroke thickness and overlap, so I'm leaning toward keeping the current averaging. Since the architecture seems close to its ceiling, I'll focus on refining the templates for the top confusions like 7 against 5, which is a lower-risk change.

I'm thinking that per-class scaling could help, since 7 and 8 have very low recall (89 and 73), and amplifying a low-recall class's template match might help it win on partial matches where bias alone can't.

I'm checking whether the 8s are losing to the 2s because my 8 template is too weak. Boosting the scale on low-recall classes could help the true 8s win, but it would also inflate false matches, so the net effect is uncertain.

Considering whether the 8 template is weak against the 2s because of downsampling, and whether boosting scale on low-recall classes would help more than it hurts. Rather than keep doing blind template surgery, I'm thinking about a different approach that uses conv layers to compute coarse regional ink sums.

I'm now going to give the low-recall classes (7, 8, 5, 9, 2) a slight scale boost and the high-recall ones (1, 3) a small reduction, so the per-class match strengths balance out. I'll keep the architecture as it is and re-tune the biases afterward.

I'm considering scaling the 7 and 8 templates by about 1.3 so their correct matches rise above the competing classes, while leaving the rest unchanged. Scaling also amplifies negative correlations, so the gain is uncertain. I'm leaning toward targeted template fixes for 8 and 7 instead, since that's a more contained change.

Next I'm refining the template for 8, aiming to make the two loops and the waist clearer. The key difference from 2 seems to be on the right side of the middle-lower area, where an 8 has ink from its lower loop.

I'm comparing the right-side ink in the lower half of the 8 and 2 templates, since the 8 has filled verticals there and the 2 does not. That difference should separate them, yet the 8s keep landing on 2, so the template matching is still missing something.

Maybe the 8s are messy at this resolution, with the lower loop's right side too faint to register. The bias difference isn't the cause, since the 8 template actually has the higher bias, so it must be feature correlation that favors the 2 template. My 8 template may be too clean, with hollow loops that a downsampled real 8 doesn't show.

I'm noticing that at this resolution, small loops fill in, so 8, 0, 9 and 6 look like solid blobs and their holes barely show. That makes hole-based discrimination hard with downsampled features, which is probably why those classes keep getting confused. Still, the hole idea may have been sound and only failed because of noise or calibration, so it could be worth revisiting at full resolution before the pooling.

I'm considering whether the hole detector can be salvaged by shrinking its scale and making its templates more selective, since the earlier version pushed nearly everything toward 8. The catch is that re-adding it means giving up some of the ink channels, and with few steps left that's a risky trade.

I'm thinking about splitting the hole detector into a smaller, stricter version, with less scale and sharper templates so it stops firing on everything. Since the last attempt flooded the output toward 8, I'm weighing whether that's worth the risk with few steps left, so I'll likely make a safer bias adjustment and one template fix I'm more confident about.

I'm going to give the hole-based approach another careful try, since 0 vs 8 vs 2 is exactly where a hole count would separate the classes. The main confusions, like 9 to 4 and 0 to 8, are the ones worth targeting.

I'm going to try the hole detector again, but in a stricter form: 13 ink channels plus 3 hole channels, a smaller scale, and templates that also penalize holes on digits like 1, 2, 3, 5 and 7. The earlier version was dominated by the hole feature, so I need to check whether the hole values are simply too large.

Now I'm weighing whether the hole detector is firing on digits that have no real holes, since stroke edges and tips register as false holes and push the 8 channel up across the board. I'm thinking the fix is a detector that needs ink on every side of an empty center, not just a border around it.

Working out the border-and-inner-emptiness condition for the hole channel: I want output to be high only when the whole ring is inked and the center is clear, so a stroke edge that covers just part of the border stays near zero while a real hole clears the threshold.

I'm checking whether the border ring around the 5x5 window is fully inked, since a real hole needs ink all the way around it. That works for holes of about 5px, but a 0's hole at 28x28 is larger than the window, so the detector won't fire at its center.

Moving the ring detector to conv2 on the 12x12 pooled map should match the hole size better, since a '0' hole there is about 4px and fits a 3x3 detector.

I'm now planning the hole channels to run on the 12x12 pooled ink map instead of the raw input, since holes there are about 4–6px and fit a 5x5 ring detector. The plan is 12 ink-sampling channels plus 4 ring channels in conv2, with conv1 just producing the ink channel.

I'm now sketching the ring detector on the 12x12 pooled ink map: a 5x5 window whose border should be inked while its center stays empty, with a negative bias to set the threshold. At that scale a 0's hole is about 4–5px, which fits the window well, while 8's smaller holes will be harder to catch.

I'm checking whether a 0's single central hole and an 8's two stacked holes land in different rows of the 4x4 hole map, since that spatial pattern could separate them where the hole count alone can't.

I'm going to retry the hole detector, this time running it as ring detectors in conv2 on the 12x12 pooled ink map, where holes are about the right size. I'll keep the same ink channels and add four hole channels, with the templates and threshold kept conservative so the non-hole digits don't get pushed toward 8.

I'm setting up the conv2 ring detector: a 5x5 filter where the border should be inked and the inner 3x3 empty, with a threshold bias around -0.15. I'm noticing the four hole channels would be identical copies, since a full 5x5 filter doesn't shift by offset, so the localization has to come from the filter itself rather than from separate channels.

I'm settling on 14 ink channels plus 2 ring channels, since the ring detector already gives the 4x4 hole map and two copies add only a little redundancy. For the ink part I'm mapping the 14 channels onto a 4x4 grid of sampling offsets, so the first four go to row one, the next four to row two, and the last six spread across rows three and four.

Setting the hole templates aside for now, I'm laying out the split for the fc layer: the first 14 ink channels go to the normalized ink part, and the last two ring channels feed the hole part. For the hole maps I'm sketching a 4x4 pattern per digit, starting with a 0 as one central hole and an 8 as two stacked holes at the top and bottom.

Still writing the 4x4 hole templates...

Still writing the 4x4 hole templates...

Still weighing the hole-scale choice, leaning toward 2.0 over 2.5 so the 8 template doesn't take over the output again.

Checking whether the ring detector would fire on solid strokes at 12x12, since the hole estimate depends on that.

I'm settling on a higher threshold of -0.2 for the ring detectors, since weak stroke edges then drop to zero while real holes still come through. I'll keep the ink scale at 6 and the hole scale at 2.0, reusing the earlier biases even though the 14-channel ink normalization shifts them slightly.

Still writing the hole detector code...

Still writing the fc template code...

Still writing the hole templates and the ring-channel setup...
