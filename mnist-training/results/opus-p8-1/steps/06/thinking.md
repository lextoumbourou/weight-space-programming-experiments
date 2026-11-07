I'm stuck around 62% accuracy, and I think the features are the bottleneck: the 4x4 coarse grid with max pooling makes the templates look too alike. I want richer, more spatially specific features, so I'm considering a larger kernel in conv2 that could capture combinations like a horizontal stroke sitting above a vertical one.

I'm weighing a larger kernel in conv2 so the features can cover parts of the digit, like loops, endpoints, or a top bar. Shifting conv2 taps by one pool unit would make the pooling windows overlap, which might add some spatial resolution, though the windows would still be fairly wide.

I'm considering whether a local average over the 5x5 pooled area, rather than max pooling, would capture how much stroke is present and not just whether it exists, something like a histogram of oriented gradients. Nearest-centroid on good class means could plausibly land around 85–90%, but my hand-drawn templates only approximate those means, so I'm wondering whether averaging templates over style variations like slant would help.

I'm weighing whether averaging over hand-described variants would be acceptable, but I'd rather just blur the templates spatially, which approximates style variation without generating samples. Using conv2 to sum a feature over a small local area seems more promising than a single tap, though a 5x5 sum would be too blurry, so I'm considering a 3x3 center sum instead.

I'm wondering whether the real problem is confusion between specific digit pairs like 2 and 0, 8 and 2, or 5 and 6, rather than the feature grid alone. Making the fully connected weights more discriminative could help, but my earlier attempt struggled with class 1 pulling everything toward it. Explicitly modeling loops and other topology in convolutions looks hard, so I'm considering whether adding more orientation channels would be a simpler route.

I'm considering whether splitting each orientation channel by edge polarity would help, since the side of a stroke that has ink could separate loop tops from bottoms. Signed gradient detectors like HOG might distinguish things a single-polarity detector can't, though for thin strokes both edges show up, so the gain is uncertain.

I'm thinking about shifting the conv2 taps so the pooling windows overlap, which could give a bit more spatial resolution at the 2-pixel scale. Rather than expecting big gains from that, I'm looking at whether carefully tuned templates and a better scoring rule would do more, with a rough ceiling around 80%.

I'm working out how conv2 could sample pool1 at different offsets, so the pooled windows tile into a finer grid of ink-presence checks over the image. The offsets don't land on all positions, but a small conv1 kernel might give a roughly 10x10 grid of local 4-pixel-block detections.

I'm now weighing a stride-4 grid of 4x4 max-ink blocks as a coarse binarized image, which might land around 75–80%, though I'm not sure the blocks give enough detail.

I'm thinking about replacing the max pooling with a sum over a small local area, since summing orientation energy across cells, as HOG does, would keep the amount of stroke rather than just its presence. Since the 16x4x4 layout gives 256 features, I'm looking at whether a uniform 3x3 weighting in conv2 could make the sums work without any training.

I'm now considering a sum over the 3x3 pool1 neighborhood in conv2 instead of a max, so the features track how much stroke of each orientation is present rather than just whether any is. Summing orientation energy across cells like HOG would reduce the saturation, and the 16x4x4 layout would still give 256 features. I'm also thinking about using the remaining channels for shifted versions of the same orientation sums to get a finer grid.

Still working out the conv2 kernel layout: I'm settling on a 3x3 window placed at different offsets across the pool1 grid, so four offset versions of each orientation channel together fill the 16 channels.

I'm settling on conv2 window starts at offsets 1 and 2 within the pool1 grid, since a shift of one pool1 unit is half a pool2 stride. That interleaves the sampling positions so the sums cover the image more finely.

I'm considering a 3x3 sum in conv2 with the window starting at offset 1, so the orientation channels track stroke amount, and I'm wondering whether the remaining channels could hold an ink sum or endpoint detectors instead.

I'm checking how the conv2 windows line up with the pool2 grid: each window's center lands near 4s+7.5 in image pixels, so the sums stay aligned with the pooling cells. Each sum covers roughly a 6–7 pixel tall span, and I'm working out how the max between the two conv2 rows that feed each pool2 cell combines them.

I'm estimating what a pool1 unit responds to, working from the conv1 positions and the stroke-width tolerance around each cell center. Once that's set, the conv2 3x3 sum and the pool2 max give the template value for each cell and channel.

I'm checking whether computing expected pool1 features from hand-described strokes stays within the rule against running the network on inputs. I'm treating it as analytic modeling rather than running the convolutions on an image, so I'll keep the template as soft window functions over the stroke description.

I'm settling on the template as a direct sum: for each channel, I take the max over the two conv2 row and column starts for each pool2 cell, where each candidate is a 3x3 sum of the pool1 response map. Pool1 values should land around 0.7 to 1 per cell, so a straight stroke gives a sum near 3 and a blob gives something near 9. Since these features are now much larger in magnitude, the cosine template scaling will need a smaller alpha than before.

I'm settling the scaling next: the summed features are larger in magnitude, so I'll drop the cosine temperature to about 6. For the pool1 map, I'm treating each cell's stroke membership as a soft window around its center, taking stroke points that fall within the conv1 response range.

Writing the feature-building code now...
