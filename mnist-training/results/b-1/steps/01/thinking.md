I'm sketching a first-step network by hand, starting with the first conv layer as a set of oriented edge and stroke detectors, with one channel acting as a blurred ink detector.

I'm working out the receptive field of the final 4x4 cells by tracing rows back through pooling and convolution. A center-tap second conv would map each final cell to roughly a 4-row band of input pixels, which is still wide, so I'm checking how that offset arithmetic lines up.

I'm checking the grid math: the final cells cover input rows 4 through 23, roughly a 4-row band each, centered near 7.5, 11.5, 15.5, and 19.5. I'm weighing whether more resolution is worth it, since 16 channels at 4x4 gives 256 features and I'd expect hand-built templates to land somewhere around 70 to 85 percent. I'm now considering shifted copies of the ink map as a way to get finer spatial detail, though that's where my thoughts currently stop.

I'm now moving from the conv2 idea to the fc templates, deciding that without data I have to hand-design the digit patterns on the 4x4 grid for each feature type. I've settled on five conv1 detectors (horizontal, vertical, two diagonals, and an ink blob) with the rest zeroed, and I'm about to lay out the 16 conv2 channels.

I'm settling on five conv1 detectors and leaving the rest zeroed, with conv2 mostly passing those features through at its center tap. For a "hole" feature, a negative center weight on ink with a positive surrounding ring might work better than thresholding the blurred ink, since max-pooling a negative response just finds any empty pixel. I'm checking whether a 5x5 kernel on the 12x12 pooled maps is wide enough to cover the inside of a digit's loop.

I'm weighing whether to keep the design simple, drawing each digit's template by hand on the 4x4 grid instead of generating weights from rendered examples, since the task rules that out. I'll start with a first version built on the existing feature types and refine it from there.

I'm planning the templates in feature space rather than running conv1 on rendered digits, which is allowed since I'd be drawing strokes by hand. Each digit gets polyline strokes on the 20x20 box, and each segment's orientation picks which of the four channels it feeds. I'd then weight each 4x4 cell by how much stroke of that orientation falls inside it.

I'm checking how each final 4x4 cell maps back to input rows, which works out to a 4-row band per cell centered near 7.5, 11.5, 15.5, and 19.5, so the first and last cells sit at rows 6 to 9 and 18 to 21.

I'm considering a wider conv2 kernel that sums neighboring taps, so each final cell overlaps its neighbors and picks up strokes that run near the edges of its band.

I'm settling on a blurred weighting for the 3x3 conv2 kernel, so each final cell's center sits near input row 4r+7.5 with a soft falloff around it. For the conv1 filters, I'm shaping oriented line detectors that are positive within about a pixel of the stroke and negative at two pixels, then making each one zero-mean.

I'm setting the conv1 line detectors' direction vectors for four orientations: horizontal, vertical, "/" and "\", using image coordinates with y pointing down.

I'm normalizing each oriented line filter so its positive weights sum to one, and setting the conv1 orientation bias to -0.1 so only strong responses pass.

I'm settling on five feature channels for conv2: four orientation pass-throughs smoothed with a 3x3 kernel, plus the ink channel, leaving the rest zeroed. That gives 80 features. I'm now wondering whether shifted ink channels, with the center tap offset by a pixel or two, could add finer spatial detail without much extra work.

I'm now considering shifted ink channels at conv2 offsets of one and three pool rows, which would shift the sampling grid by two input rows each time. Combined, that gives an effective 8x8 sampling of the ink map at roughly two-row spacing, a finer grid than the plain 4x4.

I'm settling on a single-tap ink channel at offsets (2,2), (1,1), (1,3), (3,1), and (3,3), dropping the smoothed version since it duplicates those. Channels 9 through 15 stay zero, and I'm leaving the orientation channels at their current resolution. Next I'll work out how to build each digit's template from polyline strokes in normalized coordinates.

I'm turning each sampled stroke point's direction into weights on the four orientation channels, then spreading its contribution over nearby cells with a Gaussian falloff. Since max-pooling responds to presence rather than accumulated amount, I'm saturating each template cell with a 1 minus exponential of its sum. For the classifier, I'm subtracting the per-cell mean across digit classes so each digit's weights emphasize what sets it apart, and I still need to pick the bias.

I'm settling on a scale factor for the logits, starting around 1 to 3, and I'll tune it from feedback since the score gaps between classes are only a few units.

Normalizing the smoothing kernel to sum to one keeps the orientation features near one. Then I'm laying out the digit strokes in a 20x20 box, with the 1 centered by mass since it's narrow.

Now I'm sketching the stroke paths for each digit in the 20x20 box, starting with a 0 as an ellipse and a 1 as a slightly slanted line.

Still writing the polyline coordinates for digits 4 through 6...

Now I'm laying out the remaining digit shapes as ellipses and stroke paths, with 8 as two stacked loops and 9 as a loop with a tail, and noting that the template centering is based on mass.

I'm setting the ink-channel presence threshold: a stroke point counts toward a cell with a Gaussian weight of width around 2, and the orientation channels use a slightly wider one. Given that, a stroke passing directly through a cell should saturate its template value near one, while a stroke about three pixels away drops to roughly half. That matches the way max-pooling over a 6x6 region responds to nearby ink.

I'm checking how orientation weights should respond at 45 degrees off the stroke direction, and I'll use a max(0, cos(2(φ-θ))) form so that response drops to zero there. Then the nearest-centroid score, with its bias term, reduces to a negative scaled squared distance, and I still need to pick the scale so the score gaps between classes are workable.

I'm setting the scale and bias for the score and planning the 5x5 conv1 kernel offsets. I'm defining each orientation's perpendicular distance and a Gaussian line profile to shape the detectors.

I'm now checking the sign convention for the orientation weights: horizontal at 0, vertical at π/2, "\" at π/4 and "/" at 3π/4, with the same image-coordinate angles used in the conv1 filters.

I'm checking the orientation convention once more, confirming that a direction of 45 degrees points "\" with y down. Then I'm setting up the conv2 weights: the orientation channels get a normalized 3x3 smoothing kernel, and the ink channels get single taps at the chosen offsets. I'm now working out how each conv2 output row maps back to pooled rows and input rows, so I can place each final cell's center.

I'm checking how a 4x4 final cell maps back to input pixels, with the center of each band at about 4r+2ky+3.5 for the ky=2 tap. For the ink taps, I'm weighting nearby input positions with a Gaussian of width 2 on each axis so a stroke within about three pixels still counts.

I'm weighing a box-shaped soft window for the orientation channels, half-width around 3.5, and then estimating the presence value as one minus an exponential of the accumulated stroke length times a scale factor. Along a direct stroke that sum comes out to about six or seven, so the template should land near one, but I expect real aligned detector responses to sit closer to 0.6 to 0.8. I still need to check what the single-tap ink feature actually reads in that case.

I'm settling the ink channel's kernel: a 3x3 with a center weight of 0.5 and 0.125 on each of the four neighbors, so the total is 1 and a stroke pixel comes out near 0.8 to 1.

Still writing the weight-building code, setting up the conv1 orientation filters.

Still writing the conv1 weights, building the orientation filters from a Gaussian line profile with mean subtraction and normalization, and adding the ink-channel kernel with its 0.5 center and 0.125 neighbors.

Still writing the convolution weights, now setting up the second layer's smoothing kernel and the ink taps, and planning to walk through the stroke samples segment by segment.

Still writing the feature template code, turning the accumulated stroke presence into saturated values and folding in the scale and bias for the classifier weights.

Still writing the sampling code, planning to compute the per-digit points, angles and step lengths, then fill each channel's grid. I'm setting the classifier scale to 0.5 and checking that the expected score gap between the right and wrong digit is about 2.5 logits, which should be workable.
