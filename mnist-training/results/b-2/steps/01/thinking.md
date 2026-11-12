I'm thinking about designing the weights by hand, starting with a simple approach. Hand-crafting class templates in the 16x4x4 space looks hard, so I'm considering making the network act as a template matcher instead, starting with a first conv channel that passes the center pixel through.

I'm working out which input pixels each final 4x4 cell actually sees, tracing the receptive field back through both pooling stages and the two convolutions.

I'm checking the receptive field with just the center tap in conv2: each final cell covers input rows about 4 to 11 for the first cell, shifting by 4 per cell, so the digit's rows 4 to 23 are fully covered. I'm also weighing a full 5x5 average in conv2 against a small blur, since max pooling already gives a presence-of-stroke signal per region. The final 4x4 grid ends up with cell centers near input positions 7.5, 11.5, 15.5, and 19.5.

I'm settling on conv1 with eight channels: oriented detectors for horizontal, vertical, and both diagonals, plus an ink-intensity channel and a few for edges or endings. Then I'm weighing whether hand-writing 10×256 template weights is practical, or whether I should derive the fc weights from prototype digit drawings instead.

I'm weighing whether to rasterize each digit's stroke segments straight into the orientation channels at 4x4 resolution, since that avoids running the network on any generated input.

I'm considering whether a simple pixel-level template match would work, but a 4x4 grid of max-pooled ink would be too coarse to tell digits apart. Oriented stroke channels seem much better, and I'm exploring whether shifting conv2 channels by small offsets could recover some finer spatial detail.

I'm weighing whether conv2 with single-tap offsets could sharpen the grid, since max-pooling over a 2x2 region of shifted taps should let each cell pick up finer positional detail, though adjacent shifts overlap.

I'm settling on eight conv1 channels: four orientation detectors for 0°, 45°, 90°, and 135°, with the rest reserved for other stroke cues. I'm also thinking about what separates the digits at this 4x4 resolution, like which orientations show up at the top and bottom of a zero.

I'm picking the conv1 channels as four line detectors at 0°, 45°, 90°, and 135°, and I'm considering using the other four for edge-type cues. I'm also weighing whether eight orientations would capture finer stroke direction than four, or whether that just adds weights without helping the classification.

I'm weighing eight orientation channels at 22.5° steps instead of four, and considering whether conv2 should instead pick up curved or shape-level cues like the top of a loop.

I'm weighing eight conv1 orientation channels against a mix of six angles plus an ink channel, so that conv2 can pass through the most useful ones.

I'm settling conv1 on four orientation detectors (horizontal, both diagonals, vertical) plus a blurred ink channel, and leaving the remaining three channels at zero weight. Then I'll turn to how the fc templates should be built from those features.

Mapping each digit's strokes onto the 4x4 grid cells, using the input-pixel coordinates to work out which cell each stroke falls into.

I'm checking where each 4x4 cell's stroke pixels fall, and I'm switching conv2 to a 3x3 box so the outer rows at 4-5 and 22-23 get covered too.

I'm checking the coverage math: the cell ranges come out to 4-11, 8-15, 12-19, and 16-23, so the full digit is covered with some overlap. I'm treating the blur as a sum rather than a max, so the scale just needs to stay consistent. For the templates, I'm placing each cell's center at 7.5, 11.5, 15.5, and 19.5, and weighting stroke samples by how close they fall to each center, then subtracting the class mean so the weights discriminate between digits.

I'm weighing a linear template classifier, where each class score is a dot product with its template minus a bias. Dot products favor templates with larger norms, so I'm considering a distance-style score instead, but that depends on matching the template scale to the feature scale, which I can't easily know yet.

I'm settling the conv1 filters as line detectors, with each kernel a Gaussian ridge along the stroke direction minus a wider negative surround so flat regions give zero response.

I'm weighing whether a zero-mean line kernel holds up on thick strokes, since a bold digit fills the whole window and gives little response. Gradient-based oriented filters that respond at stroke edges might handle thick ink better, so I'm considering those instead.

I'm switching the first conv layer to gradient-based edge detectors: four orientations, each with two polarities, so the ReLU outputs mark which side of a stroke the ink is on. That should hold up on thick strokes, where a zero-mean line kernel would give little response. In conv2 I'm then deciding whether to sum the two polarities per orientation or keep them separate.

I'm keeping the first conv layer simple and using four orientation-energy channels, with the other channels left at zero for now. I'm also considering whether conv2 could get some extra sharpness from a center-tap channel, but I'm leaning toward keeping the design minimal until the templates are in place.

I'm settling the edge filter as a derivative-style kernel along the stroke normal, scaled so a unit step edge gives roughly unit response, which should hold up on thick strokes too.

I'm settling on a sharper orientation response by making the edge filters anisotropic, with a longer extent along the stroke than across it, and raising the bias so that only roughly ±50° of orientation passes through the ReLU. Next I'm summing the two polarity channels for each orientation in conv2.

I'm checking whether the polarity-split channels in conv2 are worth including, since a horizontal stroke's top and bottom edges might tell apart digits like 0 from others.

Now I'm sketching the digit templates as shapes on the 28x28 grid, starting with the zero as an ellipse centered at (14,14) with a fairly tall vertical radius.

Sketching the remaining digit shapes as point lists on the 28x28 grid: the 1 as a near-vertical stroke, and the 2, 3, and 4 as connected arcs and lines through specific pixel coordinates.

Now I'm listing the digit templates as point sequences: the 5, 6, 7, 8, and 9, each with its own key coordinates and loop centers. I'm planning to rasterize them by sampling points along each segment at a fixed spacing.

I'm working out how to turn each stroke sample into template weights: the orientation of the segment picks which of the four angle channels it feeds, and a Gaussian falloff around each 4x4 cell center decides how much each cell gets. I'm also settling the sign convention, since image rows grow downward, so a "/" stroke has to be measured with y flipped to land in the 45° channel.

I'm fixing the conventions for the first conv kernel: stroke direction θ in x and y-up coordinates, with the normal and the across/along projections defined from it. Then I'm normalizing the template so the fc weights are the unit template minus its mean, scaled by alpha.

I'm sizing the final layer: the feature vector has a norm around 2, and the gap between correct and wrong template dot products is roughly 0.4 per unit of scale, so I'm estimating a scale near 8 to get a logit gap of about 3.

I'm checking whether the pooled conv2 responses stay in a sensible range, estimating that a horizontal stroke gives a blurred value near 0.5 across the 3x3 window.

Still writing the edge kernel code...

Still writing the edge kernel code...

Still writing the template-building code...

Still writing the template-building code, now checking the cell-to-pixel mapping for the second conv layer.
