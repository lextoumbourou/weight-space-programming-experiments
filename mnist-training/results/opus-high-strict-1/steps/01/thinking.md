I'm sketching a hand-crafted CNN where the first conv layer acts as oriented edge and stroke detectors, the second passes spatial information through, and the fully connected layer matches templates over a 4x4 grid of 16 feature channels. I'm now working out how large an input region each 4x4 cell covers via receptive field arithmetic, starting from the conv1 output size.

I'm working out the receptive field for each 4x4 cell: pooling halves the grid twice, so the final cells end up spaced about 4 input pixels apart, each covering roughly a 16x16 region. The offsets put the cell centers slightly off from the middle of the 28x28 input, which I want to double-check.

I'm checking that the cell centers come out symmetric around the middle of the input, which they do at about 13.5. The bigger question is which features to use: I can't compute real templates from data, so the fully connected weights would have to be hand-specified for each class, channel, and cell. That's roughly 2560 numbers, which I'd need to generate from a formula rather than run the network on any digit.

I'm weighing whether a simpler ink-detection front end would be good enough, since a coarse 4x4 ink map with max pooling might only reach 50-70% accuracy. Oriented edge features look more discriminative, so I'm leaning toward eight conv1 channels covering the four line orientations and possibly edge-type variants, aiming for something in the 80-90% range after iterating.

I'm settling on eight conv1 channels for oriented strokes (horizontal, vertical, and the two diagonals), and I'm thinking about whether conv2 should instead carry finer part detectors, though that adds complexity I may not need at first.

I'm checking the stride again: the pool2 cells sit at input offsets 0, 4, 8, and 12, each covering a 16-pixel window, so their centers land at 7.5 through 19.5, symmetric around the middle of the 28x28 input.

I'm checking the center-tap version of conv2: each pool2 cell then covers an 8-pixel input window at stride 4, with centers still at 7.5 through 19.5. I'm deciding how to split the 16 conv2 channels, perhaps 8 conv1 channels doubled up, or 4 orientations with an extra variant each.

I'm settling the conv2 design now: each channel could read a different pool1 tap, so shifting the window by a couple of input pixels gives a finer effective grid over the four orientations.

I'm settling on the feature grid as 4 orientations at 64 positions, which heavily overlaps. For the fully connected weights I'd hand-specify each digit's strokes, like an ellipse for the 0, and then assign each feature weight by how much of a stroke with that orientation falls inside the matching window.

I'm checking whether the fully connected weights can be built from the strokes of each digit template, with the class score as a dot product against the features. I'm also noticing a problem: a template with more ink, like an 8, would score high across many cells, so the raw scores need normalizing or centering across classes.

I'm settling on the nearest-template idea: the score for each digit is 2 times the dot product of the features with that digit's template, minus the template's squared norm, which is equivalent to picking the closest template.

I'm settling the conv1 filters now: oriented line detectors with a positive center band and negative flanks, sized so a stroke of ordinary MNIST width gives close to full response. Thick strokes weaken the flank penalty, so I'm considering a milder negative surround.

I'm settling on oriented line detectors for conv1: a positive band along the stroke direction with negative flanks, so a horizontal detector stays weak against vertical strokes. I also want a negative bias so only clear responses pass through the ReLU.

I'm defining each oriented kernel as a difference of Gaussians across the perpendicular direction, so the center band responds to a stroke along that orientation and the flanks push back. I'm considering a mild taper along the length, and I'm sorting out how to normalize the kernel without running it on synthetic inputs.

I'm weighing whether a distance-style score, which subtracts each template's squared norm, handles the ink imbalance better than a plain dot product, and I'm checking how the scale of the pooled features affects that comparison.

I'm reconsidering the bias term: since a plain dot product ignores template ink, I'd add a correction proportional to each template's squared norm, which keeps heavy digits like 8 from winning everywhere.

I'm thinking about how to turn each digit template into weights over the pooled feature grid without running the network: for each stroke point, I'd mark which pooled windows contain it and how well its orientation matches, taking the max since pooling is a max. The overlapping windows should already give some tolerance, so I'm working out whether extra blurring is needed.

I'm settling the conv1 channels: four line orientations or eight edge directions, with the choice weighing whether polarity matters for telling apart loop tops from bottoms.

I'm now weighing which conv1 channel set would help separate digits like 4 and 9 or 3, 5 and 8, and I'm expecting coarse orientation features to land somewhere around 70-85%, with hand-drawn prototypes likely lower. Learned templates from data should do better, so I'll iterate using the confusion matrix. A more invariant conv2 feature, such as end-stop or loop detection, might help, but I'll start simple.

I'm settling the conv1 channels: the first four are the 0°, 45°, 90°, and 135° line detectors, and for the other four I'm considering 22.5° offsets to sharpen the curvature resolution. For conv2 I'm weighing 8 orientations crossed with two shifts, though I'm not yet sure that's worth the extra complexity.

I'm now deciding between finer orientation resolution and finer spatial resolution, since the 4x4 grid with 8-pixel windows leaves the digit's 20x20 central area to be covered by window centers at 7.5, 11.5, and 15.5.

I'm checking the exact input region each pooled cell covers: after the conv2 tap and the two conv1 rows that feed it, the centers land in a 4-row band, and the 4x4 kernel extends that band to cover roughly 8 pixels per cell.

I'm checking the input region each pooled cell covers, and noting that the current tap-based windows only span rows 6 to 21, which misses the outer edges of the digit. I'm considering a conv2 kernel that sums over a wider 3x3 set of pool1 taps so the windows tile the full 4 to 23 range, with overlap, accepting that the response will scale with how much stroke falls inside each window.

I'm settling on the conv2 kernel as a sum over a 3x3 set of pool1 taps, so each pooled cell covers a wider 8-pixel window and the windows tile the full digit area. I'm also planning to normalize the template weights against the expected feature scale, since the summed responses will track how much stroke falls inside each window.

I'm estimating how much each template's ink would weight a 3x3 window of pool1 cells, and I want the feature magnitude near one for a stroke crossing the window. Then I'm working out the template value as the stroke length of each orientation inside a window, capped at one, while sorting out exactly how the 8x8 conv1 footprint of each pooled cell lines up.

I'm working out the template side of the same windowing: each template stroke gets sampled densely and credited to the conv2 positions whose input window contains it, taking the best sub-window per pooled cell.

I'm checking the normalization for the template side: a stroke length of six pixels inside a window should give a value of one, so each template response scales the same way as the pooled network features. Templates aren't clamped, since overlapping strokes can legitimately sum above one.

I'm checking whether the template computation counts as running the network: I'm only measuring stroke length inside each window geometrically, not convolving an image, so I'll treat that as acceptable. I'm also now turning to how the orientation detectors respond to each stroke direction.

I'm weighing whether to give the 16 conv2 channels as 8 orientations at one spatial offset, or to pair the orientations with a second window type, so the remaining channels aren't redundant.

I'm weighing a second set of 8 conv2 channels that uses the same orientations with taps shifted by one pool1 cell, which would give a different spatial sampling. Shifting toward the top-left leaves the first cell nearly empty, and shifting toward the bottom-right pushes the last cell past the digit's edge, so I'm checking whether the original offsets of 1 to 3 already cover the 4-to-23 range best.

I'm weighing a second set of conv2 channels that shifts the taps by a pool1 cell, so the windows sit half a cell lower-right and sample the digit at intermediate positions. I'm also reconsidering whether a finer single-tap window would add more useful spatial detail than the shift, but I'm leaning toward keeping the design simpler for now and focusing on the template work.

I'm placing the digit strokes in 28x28 coordinates and sketching their shapes: a near-vertical slanted line for the 1, an ellipse for the 0, and an arc over the top for the 2.

I'm now placing the stroke templates on the 28x28 grid, with the 3 as two arcs bulging to the right, one above the midline and one below.

I'm listing the remaining digit strokes on the 28x28 grid: a 4 built from a slanted left stroke, a crossbar, and a right vertical, and a 5 with a top bar, a short vertical drop, and a lower bowl arc.

I'm laying out the remaining digit templates on the 28x28 grid: a 6 as a curved stroke down the left side with a closed loop at the bottom, a 7 as a top bar with a long diagonal, and an 8 as two stacked circles. I'm starting on the 9 as a loop at the top.

I'm now settling the feature scale: the conv1 kernel will be normalized so a clean stroke of about 2.5-pixel width at full ink gives a response near one, and I'm designing its weights analytically from perpendicular distance and position along the stroke.

I'm checking whether computing the normalization constant by summing kernel weights over the stroke footprint counts as running the network on an input, since it's a numeric calibration rather than a forward pass.

I'm checking the normalization next: the narrow and wide Gaussian rows are summed across a 5-pixel width, giving about 2.5 and 4.1, so I'm considering scaling the positive weights to a target total rather than building the constants from a synthetic line image.

Now I'm checking the kernel weights row by row, getting roughly -0.26, 0.06, and 0.40 for the outer, middle, and center rows. I'm estimating how much a stroke of about three pixels would contribute, and noting that thicker strokes would reach the outer rows and pull the response down.

I'm settling the conv1 kernel by normalizing it so the central band sums to one, rather than checking it against any synthetic line image. I'm also considering a small negative bias of about -0.3 to keep the 22.5° neighboring orientation from leaking into the response.

I'm settling on a scale factor for the features, roughly 0.7 of the ideal response, and folding that into the template logit with a gain of about 1.3 that I'll tune later. I'm also weighing a membership function for the orientation tuning, using a cosine term with a small offset so neighboring orientations contribute less.

I'm settling the template sampling: I'll place points along each stroke every 0.25 pixels, weighting each by its membership value, and each point adds its weight to every conv2 window that contains it.

I'm now setting the window offsets for the second conv2 group, shifted by one pool1 cell, and computing how each window's stroke length maps onto the pool1 grid.

Now I'm writing out the weight layout for the second conv2 group, with 1/3 per tap so that a crossing stroke sums to one response, and I'm planning to set the fully connected weights from the template vectors scaled by the gain and bias.

I'm settling the fully connected weights: the template vectors get scaled by the gain and bias, and the loss scale starts at 0.7 since class differences of several units should already give a confident separation. I'm also doubting whether a single template per digit can handle how much real digits vary, especially slanted 1s, and I'm noting that I might add more templates later.

I'm considering whether a soft window membership, one that extends a couple of pixels beyond each conv2 window, would blur the templates enough to match real digit variation better than sharp ones.

Still writing the convolution kernel code...

Setting the first conv layer's bias to -0.3 should suppress the neighboring-orientation leakage, and I'm estimating real stroke responses around 0.7 to 1.0, so I'll scale the template gain to roughly 1/0.55 to compensate.

Still writing the convolution kernel code...

Still writing the convolution kernel code...

Still writing the convolution kernel code...

Now I'm fixing the digit stroke coordinates, starting with a 0 as an ellipse and a 1 as a slanted line, and I'm working out the arc for the 2 with its angles in image coordinates.

Still writing the digit stroke coordinates...

Still writing the digit stroke coordinates...

Still writing the digit stroke coordinates...

Still writing the digit stroke coordinates...

Still writing the stroke sampling code...

Still writing the vectorized stroke accumulation code...

Still writing the vectorized accumulation and reshaping the channels.
