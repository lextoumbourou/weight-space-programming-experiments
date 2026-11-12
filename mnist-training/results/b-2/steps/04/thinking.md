Progress is slow, so I'm rethinking the approach from the ground up. The 4x4 orientation-energy grid is too coarse, since many digits look nearly identical in that form, and cosine matching against hand templates is weak. I'm considering whether the 16 conv2 channels could be shaped into spatially selective part detectors, and I'm weighing pixel-based template matching as an alternative.

I'm weighing whether the conv2 channels could be made into digit-specific local templates, though fitting them through the fc layer seems hard. The cosine scoring may be the real problem, since its normalization doesn't handle saturating feature values. I'm also considering which features separate the confusable pairs, like 0 and 2, where the closed loop and the bottom stroke differ.

I'm thinking about whether pixel-level ink features at higher resolution, pulled through conv2's channel offsets to an 8x8 map, would separate the digits better than the coarse orientation grid. A nearest-class-mean approach on downsampled pixels could work in principle, but my hand-drawn means would probably be worse than real ones. Since I only get feedback rather than data to fit, I may have to tune a few global hyperparameters against the confusion matrix instead.

I'm considering a hole detector for enclosed background regions, where a conv2 unit would respond when edge features with ink on the left, right, above, and below all line up around a gap. Conv1's 5x5 filters are too small to capture a large hole directly, but conv2's roughly 14-pixel receptive field could cover it. That would give the network a concavity signal that orientation energy alone doesn't capture.

I'm settling on the hole-detection idea for conv2: background enclosed by ink on all four sides. The open question is whether conv1 has room for a plain ink channel, since all eight of its channels are currently spent on polarized edges. I'm considering dropping some diagonal polarities to free a slot for that.

I'm laying out a plan for the first conv1 channels: horizontal and vertical edges for the top, bottom, left and right sides, and diagonal line detectors for the slanted strokes. I'm also weighing whether the last channel could be a background map, using a positive bias to get ReLU(1 minus blurred ink), so the network can see empty regions directly.

I'm sketching the hole detector's weights for conv2: a strong positive weight on the background channel at the center, plus ink-left edge responses in the columns to its left, so a unit fires only when there's an empty spot enclosed on that side.

I'm working out how the hole detector's conv2 weights should be laid out: the pool1 offsets for a hole of a given radius land at about one or two cells out, so the 5x5 filter covers both ±1 and ±2 offsets, with rows near the center for the left and right sides.

I'm sizing the hole detector's side weights: each of the four sides should contribute about one unit, spread over the pool1 offsets, with a bias around −5 so a single stroke can't trigger it.

I'm settling the hole detector's side weights: each of the four sides should contribute roughly one unit, spread over the pool1 positions, and I'm worried a strict threshold could leave it silent, so I'll keep it moderate and let the fc layer do the weighing.

I'm laying out the conv2 channel plan: horizontal and vertical stroke energy, both diagonal line detectors, a blurred ink channel, and then a few hole detectors, with one channel reserved for an open-top cup shape and another for an open-bottom cap.

I'm now sketching the remaining conv2 channels as concavity detectors, each one firing when the background at the center is enclosed by ink on three sides and open on the fourth. That gives directional "open right," "open left," and similar units, which should help separate shapes like 3, 5, and 2 that differ mainly in where their gaps are.

I'm defining the hole detector's neighborhood in pool1 coordinates around the conv2 kernel center: a left-boundary region, a right one, a top one, and a bottom one, each a few cells wide, with the center meant to be background.

I'm defining the edge channels for conv1 by name: an ink-on-left edge, an ink-on-right edge, and an ink-above edge, each with positive weight on the ink side and negative weight on the background side.

I'm checking the sign convention of the edge kernel at 90° and 0°, confirming that the positive side is the ink side, so the flipped versions give ink-right and ink-below. Then the hole detector's left and right sides will draw on the ink-left edge in the two columns just left of center and the ink-right edge in the two columns just right.

I'm noting that the top and bottom sides of the hole use the ink-above and ink-below edges, two to three rows out. I also see that the outer edge of a single stroke can trigger a side, but the hole only counts a boundary on the side facing it. Finally I'm working on a background channel: a ReLU of one minus a blurred ink map, so empty regions read as one and ink regions as zero, with a max over each 2x2 cell after pooling.

I'm reasoning that a background-brightness channel built with ReLU would fire almost everywhere near strokes after max-pooling, so it's a poor fit. Instead, conv2 can express "no ink here" itself through a negative weight on the ink channel and a positive bias. For conv1, I'm settling on the first channels as the four directional edge types: ink-above, ink-below, ink-left, and ink-right, starting with the top and bottom pair.

I'm now settling the diagonal channels, weighing whether to keep polarized edge pairs or switch to zero-mean "/" and "\" line detectors, and I'm wondering whether dropping an explicit ink channel leaves enough signal for hole detection.

I'm working out a line detector for the diagonal strokes: a Gaussian profile across the stroke minus a wider surround so the kernel sums to zero, scaled so an ideal two-pixel line gives a response near one.

I'm settling the conv2 layout now: horizontal and vertical stroke energy, both diagonals, and an ink channel, with the hole detector's side offsets still being worked out.

I'm weighing the hole detector's side weights against its threshold: a closed loop would fire it at about 2.4 total, but a bias of -1.4 leaves a three-sided shape too close to firing, so I'm considering a higher threshold of about 1.9 to keep it selective, though that makes it more fragile.

I'm checking whether the wide 0-shaped openings fall outside the 5x5 conv2 window, since the pool1 offsets there only reach about 4 to 5 pixels from the center.

Now I'm checking how far a conv2 window reaches: at ±2 pool1 cells it can't see the vertical walls of a large 0-shaped opening, so that shape would only register through its side walls.

I'm now mapping where the hole detectors should fire for each digit, since the fc templates need to account for these new channels. The 0 might trigger a center hole in its upper-middle rows, a 6 would show one in the lower rows, and an 8 could have both.

I'm working out which digits would trigger the open-top and open-bottom concavity channels, since those shapes depend on where each digit's gaps sit. For the 3, I'm thinking the two openings face left, one in the upper rows and one in the lower, and the 2's opening is more of a diagonal toward the bottom-left, so it's harder to pin down.

I'm mapping which digits would trigger the concavity channels, going through the openings in 5, 7, 4, 6, and 9, and noting that 1 has none. The 0 reads as walls and the 8 as holes, but writing out the template weights for these by hand will take care.

I'm weighing whether to keep the four polarized edge channels for the diagonals or swap in zero-mean line detectors, since the edge version would work but the eight conv1 slots need to be filled in some way. Keeping the four orientations with polarity seems safer, since it is already the approach that has worked reasonably well at around 59%, and I'd only be adding the hole and concavity channels on top of it.

I'm keeping conv1 as it is, so the eight edge channels stay in place and no separate ink channel is needed. The open question is the center cell: it should be suppressed where edges are present, but a thick stroke can have no edges at its center, so a negative weight there isn't clearly right.

I'm settling the hole detector's weights in pool1 coordinates: positive weights on the ink-left and ink-right channels for the middle rows on each side, and on the ink-above and ink-below channels just beyond the top and bottom of the opening, with the center cell also included.

I'm settling the hole detector's center-cell suppression and checking which conv1 edge channels should feed each side of the opening in pool1 coordinates.

Setting the hole detector's side weights at 0.2 per side with a threshold near 1.0 means four full walls clear it, three barely do, and two fall to zero. For the open-top concavity I'm switching to a negative weight on the top side and a bias of 0.6, so a closed top gets penalized while holes still come through.

I'm working through the remaining detector shapes: a bottom-open variant, left- and right-open variants, and a "walls" detector that responds to a tall empty region like the inside of a 0. I'm also considering a horizontal-walls version for the gaps between stacked strokes.

Now I'm laying out the concavity channels: a hole detector, open-top, open-bottom, open-left and open-right variants, plus a vertical-walls detector, while the orientation energies stay as they were. Next I need to set the fc weights for those new channels per digit, working on the 4x4 pooled map.

Next I'm setting up the concavity channels as Gaussian blobs over the 4x4 cells, with the cell centers mapped from the pool1 offsets. The concavity weights need their own scale, since their response strengths aren't known yet, so I'll normalize them separately from the orientation block.

Next I'm writing the concavity specs per digit: the 0 gets a hole and a vertical-walls blob at the center, plus an open-top shape lower down, and I'm weighting each one.

Now I'm placing the concavity specs for the digit 2: under its top arc there's a top wall and a right wall, but the left and bottom sides aren't closed, so it reads as an open-left opening rather than a clean ∩ shape.

Now I'm placing the open-bottom and open-left concavity specs for the digit 3, with two openings facing left, one in the upper rows and one in the lower.

Now I'm assigning concavity specs for digits 4 through 6: the 4 gets an open-top shape between its arms and a closed-hole variant lower down, the 5 gets an open-right shape near the top and an open-left shape in the bottom bowl, and the 6 gets a hole in its lower loop.

I'm assigning the remaining concavity specs for digits 7, 8, and 9: the 7 gets weak open-top and open-left shapes under its bar, the 8 gets a hole in each loop, and the 9 gets a hole in its upper loop plus a weak open shape below it.

Still writing the convolution helper code...

Writing the convolution code for the concavity detectors now, and then I'll check whether they should be zero-mean per digit.
