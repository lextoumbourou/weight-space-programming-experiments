I'm settling on a hand-designed CNN as a first attempt, starting with eight oriented edge and stroke detectors in the first layer, then pooling down to 12x12 maps. The second layer would use 16 five-by-five filters over those eight channels, reducing the spatial size to 4x4 after pooling.

I'm weighing whether conv2 should mostly pass features through, leaving the fully connected layer to do template matching. The fc weights would have to be set by hand from described strokes, since I can't run the network on inputs, and I'm working out the input geometry so each 4x4 cell lines up with a region of the digit.

I'm working out the spatial mapping: if conv2 uses only its center tap, each final 4x4 cell covers an 8-pixel input window, with consecutive windows overlapping by 4 pixels. That gives windows at roughly 4-11, 8-15, 12-19, and 16-23, which fit the digit box well.

I'm thinking about whether conv2 could take a max over a small region of taps, so each channel reports whether a feature is present rather than where it sits exactly. Since the layers have 8 and 16 channels, I could pass the 8 conv1 features through the center tap and let the other 8 channels encode combinations. The fully connected layer would then need about 10 by 256 weights, and I still have to work out how to set them by hand without any data.

I'm checking whether pooled ink maps would work for template matching, but a max over 8x8 blocks would be nearly always on, so that's not discriminative. Instead, I'm considering using conv2's 5x5 kernels to compute template correlations directly.

I'm noting that a single 5x5 conv2 filter only spans about a quarter of the digit, so each channel captures local parts rather than the whole shape. Max-pooling over neighboring conv2 positions would add some translation tolerance, and the fully connected layer would then combine that 4x4 grid of part features.

I'm weighing whether I can describe the fully connected weights by hand from stroke descriptions per region, since running the network or building prototypes from inputs seems off-limits.

I'm now checking how the fully connected weights would be built from stroke descriptions, sampling points along each stroke and adding weight to the matching orientation channel and 4x4 cell. Then I'm turning to the conv1 design, starting with four orientations of line detectors.

I'm now settling the first layer as oriented line detectors at four angles, roughly 0°, 45°, 90°, and 135°, each with a positive center and negative flanks to match strokes about two to three pixels wide. I'm considering whether to use edge detectors with polarity instead, since they'd capture which side the ink is on, but line orientation is simpler for matching strokes, so I'm leaning toward it for the first four channels.

I'm settling the first layer on four oriented line detectors at 0°, 45°, 90°, and 135°, with the remaining channels filled by an ink-mean detector and some zeroed-out slots I may use later. I'm weighing whether to fill those extra slots with more orientations or leave them empty for simplicity, and I'm starting to think about how conv2 should pass the early channels through with light spatial smoothing.

I'm setting conv2's first five channels to pass the conv1 line detectors through the center tap, then checking how the pooling windows line up against the input digit.

I'm checking how the cells line up with the digit: the four 8-pixel windows are centred around 7.5 to 19.5, averaging about 13.5, which fits the digit's centre. Max-pooling should make each cell report whether an orientation is present in its region, though the overlapping windows make that fairly coarse, so I'm considering off-centre taps to sharpen it.

I'm weighing whether the extra conv2 channels should use other taps for finer resolution, or count activations over a wider area instead of just flagging presence, and I'm leaning toward starting simple and letting the feedback guide later changes.

I'm sizing the logits so the cross-entropy loss stays moderate rather than overconfident, starting with a modest scale and tuning from there. For the first layer, I want each line detector to respond near 1 on an aligned stroke about two to three pixels wide and to stay at or below zero on perpendicular strokes, so I'm setting up each kernel's weights as a Gaussian falloff over the perpendicular distance from the line through its center.

I'm dropping the Mexican-hat idea in favor of something simpler: normalize each kernel so its positive weights sum to one, skipping any computation on synthetic inputs. An aligned stroke should then respond at roughly one, minus whatever negative flanks it covers.

I'm setting the bias slightly negative so weak responses get suppressed, and then I'm laying out the orientation convention with y pointing down: θ=0 is horizontal, θ=90 is vertical, θ=45 runs down-right like a backslash, and θ=135 runs down-left like a slash. Next I'm writing out the digit strokes in 28x28 pixel coordinates, mapping a normalized 20x20 box into the central region.

I'm sketching the digit strokes in a normalized 20x20 box, centred horizontally. A 0 is an ellipse, a 1 is a near-vertical line, and a 2 is a top arc, a diagonal down to the bottom-left, then a bottom bar. I've started on a 3 with a top arc curving back into the middle.

I'm moving on to the digit 5: a top bar, a vertical stroke down the left, then a bowl curving out to the right. I'm also sketching the 4 as an open shape, with a slanted left stroke, a crossbar, and a right vertical.

I'm sketching the remaining digit shapes as stroke paths in the 20x20 box: a 6 that curls down from the top into a loop at the bottom, a 7 with a top bar and a diagonal, an 8 built from two stacked ellipses, and a 9 with a top loop and a descending stem.

I'm working out the template features now: sampling points along each digit stroke, weighting them by local orientation into the matching channel and cell, and saturating the counts so repeated ink doesn't dominate. Then I'm thinking about the fully connected weights, which need to reward presence and penalize shared structure across digits.

I'm working out how the fully connected weights should score each digit: positive where a template feature is expected and present, negative where it's present but not expected, with per-class biases to balance digits that have many expected features against sparse ones like 1.

I'm normalizing the template weights per digit by subtracting their mean and dividing by the norm, so a constant offset in the features cancels out. Then I'll scale the result to get logit differences of a few units, and estimate the typical size of the line filter's response.

I'm checking the expected response magnitude: the filter should land around 0.7 on an aligned stroke, and I'm going with that. The 4x4 pooled grid with four orientations gives about 64 line features plus ink, which I'd guess supports somewhere in the 60–80% range, enough to iterate from. For channel usage, conv1's fifth channel carries the ink average, the rest stay zero, and conv2 passes through the first five channels while the remaining eleven are silenced.

I'm considering whether offset taps could sharpen localization within the pooled cells, but a one-cell shift only moves the window about 2 pixels, so the gain looks small. I'm also deciding to fold the ink presence into the template features the same way the orientation channels are computed.

I'm checking whether the 8x8 pooling windows overlap enough to smear the hole in a 0, since the central cells seem to reach the right-hand stroke at its edge.

I'm working through the receptive field arithmetic: each final cell's window of detected stroke centres works out to roughly four pixels, so the first cell covers rows 6 to 9 and the second covers rows 10 to 13.

I'm settling the second-layer kernel: rather than a single center tap, I'm weighting the neighbouring taps at half strength so each pooled cell's window widens and the edge rows aren't lost.

I'm defining the template cell assignment with a smooth row membership centered on each pooled cell, then accumulating orientation-weighted contributions per channel and cell, and saturating the total with an exponential.

I'm weighing the centring question: MNIST digits are centred by mass rather than by box, so my templates will be slightly off, but I'll leave that for later. I'm also mapping the 20x20 box into the image at an offset of four pixels, and I'll tune the logit scale so that the score gaps between the right digit and the others land around a few tenths.

I'm estimating the feature magnitude as roughly 3 and picking a logit scale of 4 to start, to be tuned later. The fully connected bias stays at zero, and the zero-weight conv2 channels don't contribute. Next I'm setting up the ink channel as a 3x3 average, then defining the line filter's tap weights with a Gaussian falloff on the perpendicular distance.

I'm settling the line filter's weights: a Gaussian across the stroke, tapered along its length, with the mean removed so the total sums to zero. I'm also setting the conv1 line bias to -0.1, and I'm about to check whether the diagonal filters still fit on a 5x5 grid.

Still writing the filter code...

Still writing the digit stroke definitions...

Still writing the digit stroke coordinates...

Still writing the digit stroke coordinates...

Still writing the weight-building code...

Still writing the filter weights...

Still writing the convolution weights...

Still writing the weight-building code...

Still writing the sampling code...
