I'm sketching out a hand-designed approach where the network approximates template matching, starting with a first conv layer that acts like a delta filter to pass a downsampled image through, followed by ReLU and 2x2 max pooling to get a 12x12 map.

I'm working out the receptive fields for each layer, tracing how conv1, pooling, conv2, and the second pooling map back to input rows. Each final 4x4 feature ends up covering a 16x16 region, with neighbouring regions overlapping, and I'm considering whether a fully connected layer over these hand-built 16x4x4 features could act as template matching.

I'm working out the conv2 offset: a single weight at kernel position (2,2) makes each of the four 4x4 cells read a 6x6 input patch, and I'm considering using different channels at different offsets to get a finer grid.

I'm weighing a different route for the fully connected layer: hand-drawn digit prototypes as templates over the 4x4 feature grid, instead of tuning 256×10 weights blindly. I'm running into a constraint on how the prototype features could be derived, since computing them by running the network on inputs isn't allowed.

I'm settling on how to specify the fully connected layer without running the network: each digit becomes a set of hand-described strokes on the 28x28 grid, and each grid cell's orientation weight is just the stroke length of that orientation falling in that cell.

I'm settling the conv1 layout as 8 channels, with the first four as line detectors for the main orientations. I'm also weighing whether the other four should be raw-ink passthroughs, and I'm considering choosing a kernel offset per channel in conv2 to shift each feature's coverage across the grid.

I'm working out the conv2 grid layout: with offsets at 1 and 3, the sampled windows overlap and step by two input rows, giving an effective 8x8 grid for each of the four orientation features. Each cell covers a 6x6 input patch.

I'm weighing whether conv2 should just select conv1 features at fixed offsets or also blur over a region, since smoothing would make the template match more tolerant to small shifts. I'm leaning toward a first design with four orientation detectors in conv1 and treating the fully connected layer as digit templates built from hand-drawn stroke descriptions, then refining the weights against the confusion pattern afterward.

I'm defining the first conv layer's 5x5 filters as oriented ridge detectors, with a positive weight along a line through the center that falls off with distance, and I'm checking whether making the kernel zero-mean is worth it so uniform ink gives no response.

I'm checking the response of a horizontal stroke and a vertical stroke against these weights, and the vertical one comes out to zero, so the detector is orientation-selective. I'm leaning toward a bias of about -0.5 to suppress weak responses, and I'm wondering whether eight orientations at 22.5° steps would help, or whether four is enough.

I'm weighing how to set the conv2 kernel weights: each channel takes one conv1 orientation feature at an offset, and I'm considering adding neighbouring taps at half weight so each cell covers more of the grid and tolerates small shifts.

I'm checking the conv2 offsets, since the a=1 and a=3 choices give the same starting rows and so overlap instead of spreading out. Shifting to a=2 for the second set of starts should separate the grid.

I'm settling on four conv1 features, each sampled at offsets 2 and 3, which gives 16 conv2 channels whose windows cover rows 4 to 23 at stride 2. The other four conv1 channels stay unused with zero weights, and conv2 gets no bias and passes through ReLU.

Working out the conv2 tap indexing: each final feature cell at position Y spans input rows roughly 2Y+4 through 2Y+9, with its center sitting near row 2Y+6.5.

I'm checking which conv2 offsets cover the digit's rows best, since a∈{1,2} would centre the detectors a little high for strokes near the top edge. Mixing a∈{2,3} looks like a better fit for the 4–23 row span.

I'm settling the conv2 offsets at {1,2}, which shifts the detectors slightly upward compared to {2,3}, and I'm weighing whether the edge strokes near rows 22 and 23 get enough coverage.

I'm now writing the fully connected logits as a sum over features and grid positions, and I'm planning to set the weights as class templates centered across classes so the linear score acts like template matching.

I'm turning each digit's hand-drawn strokes into template weights: sampling points along every stroke segment and adding each point's contribution to the orientation channel that matches its direction, at its grid position.

I'm now turning to how the feature grid's orientation weights should be laid out, using a cosine-style response over the stroke's direction, and then blurring the result so small shifts still match.

I'm now computing the conv1 weights as a zero-mean oriented ridge, scaling each kernel so its absolute weights sum to a fixed total, and checking the response a horizontal stroke should give.

I'm normalizing each conv1 filter by its sum of positive weights so an ideal stroke gives a response near one, with a small negative bias to suppress weak responses. Then I'm writing the fully connected logits as a scaled template score that subtracts half the template's energy.

I'm settling on a nearest-template classifier, where the logit for each class is the template's dot product with the features minus half its energy, which makes the score differ by half the squared distance between templates. I'm worried that the feature magnitudes won't match the template scale, and that blurred templates will come out weaker, so I'm considering centering the weights across classes instead, though that could let high-ink digits like 8 and 0 dominate.

I'm settling on the nearest-template form for the classifier, since subtracting half the template energy makes the logit differences equal to half the squared distance between templates. Blurring the templates spatially and across orientations should keep them tolerant to small shifts, so I'm planning to get to the actual drawing next.

I'm now sketching out the digit templates as stroke coordinates on a 28x28 grid, centered near (14,14). I'm starting with the zero as an ellipse and the one as a slightly slanted vertical line, and I'm about to work through the two.

I'm writing out the stroke coordinates for the digit templates: a 2 traced as a top arc sweeping down to a bottom horizontal, a 3 as two stacked bowls, and a 4 as a diagonal with a vertical crossbar.

I'm now listing the stroke coordinates for the digits 5 through 8, starting with a top bar and curve for the 5, a loop-shaped 6, a diagonal 7 with a top bar, and two stacked loops for the 8. I'm about to set down the 9 as a top loop with a tail.

I'm placing the stroke points and then checking which feature cells each one falls under, using the conv2 windows that cover rows 2Y+4 through 2Y+7.

I'm mapping each feature cell's coverage to the stroke points that fall within its window, and working out the channel-to-cell indexing for the flattened fully connected weights.

I'm settling on a tolerance window for the template values, widening the row ranges rather than blurring, and weighting contributions by distance.

Still writing the weight-setup code...

Still writing the filter setup code...

Still writing the filter weights, normalizing each kernel so a clean stroke gives about one, with a small negative bias.

Working through how a 4-pixel-wide stroke would fall across the zero-mean filter's rows, since the best alignment should still give a usable response under max pooling.

Still weighing the filter profile: I'm considering whether a steeper falloff, with weights of 1, 0.6, and -0.5 at distances 0, 1, and 2, would keep thicker strokes from cancelling out.

I'm weighing a smoother filter profile instead of the hard zero-mean one, so thicker strokes still give a usable response, and I'm trying a per-distance falloff that keeps perpendicular leakage low.

I'm settling the filter profile as a piecewise linear falloff, so the center stays at 1, the adjacent rows drop to 0.6, and the outer rows go negative. I'll normalize it against a width-3 stroke and keep a small negative bias. The remaining four conv1 channels are unused for now, and I'm thinking about whether to put them to better use.

Still writing the stroke-point code, placing each digit's points and checking distances to the feature windows.

Still writing the digit stroke coordinates, listing the points for the 0 through 4.

Still writing the stroke-point code for the digits 6 through 9, and I'm setting up the ellipse parametrization.

Still writing the code, now working out each point's direction angle and how well it lines up with the filter orientations.
