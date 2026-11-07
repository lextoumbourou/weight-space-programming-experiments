I'm working out the weights by hand and want a simple first pass: the first convolution would act as a near-identity ink detector, the second would pass along downsampled ink, so the final 16x4x4 features are spatial maps of the strokes.

I'm checking the spatial coverage of the final 4x4 grid: each cell sees a 16x16 input region at stride 8, which is too coarse. So I'm considering a sparser conv2 layout where single-tap kernels pick out particular pool1 rows at offsets like 0, 2 and 4, so the pooled features keep finer position information.

I'm checking whether the offset taps can cover the full 12-row pool1 range: offsets 0 and 4 together reach rows 0 through 11 at a 2-row resolution. Pairing those offsets across both axes would give a 6x6 grid of four features per conv1 channel, each cell spanning an 8x8 input window at stride 4.

I'm weighing whether to hand-draw digit prototypes as stroke templates for the linear layer, since I have no training data. The sticking point is that rendering those templates and running them through the conv layers would count as running part of the network on inputs, which the constraints seem to rule out.

I'm settling on a hand-built feature-space template instead of rendering digit images and passing them through conv1, since that would run the network on inputs. I'd sketch each digit as stroke segments, tag each segment with its orientation channel, and mark the 6x6 cells it crosses, which gives expected activations without touching the network. A simpler fallback would be to use conv1 channels as plain ink detectors instead of orientation features.

I'm settling on four orientation channels for conv1 (horizontal, vertical, and the two diagonals), using zero-mean ridge kernels so that uniform ink gives no response and only oriented strokes do.

I'm weighing whether a sparser conv2 with single-tap offsets, rather than a dense 5x5 aggregator, would give a finer 6x6 grid, since a 4x4 grid of 16x16 receptive fields at stride 8 feels too coarse. I'm now checking how the offset coverage works out at the cell level.

I'm checking how the pooled rows line up: offsets 0 and 4 give pool1 row pairs covering rows 0 through 11, so each bin of two rows maps back to an 8-row input window at stride 4, centered near row 4b+3.5. That should span the digit's roughly 20-row extent.

I'm settling on whether finer taps or more conv1 channels would help, and I'm leaning toward keeping four offsets across four orientations, then leaning on the 6x6 linear templates to get the accuracy up.

I'm now going to lay out each digit as stroke segments in input-pixel coordinates, roughly within rows 4 to 24 and columns 4 to 24, with the narrow '1' kept thin. For each segment I'll sample points, assign an orientation channel from its direction, and find which of the six-by-six bins those points land in.

I'm now turning the template plan into concrete weights: each stroke point gets soft-assigned to the 6x6 bins whose 8-row windows contain it, with a Gaussian falloff around each bin's center. That fills the per-digit, per-orientation template arrays directly from the stroke layout. The fc weights would then be each digit's template minus the average across digits, with norms roughly matched, and per-digit biases tuned from feedback.

I'm now settling the conv1 kernel shape: each orientation gets a zero-mean ridge over a 5x5 window, scored by perpendicular distance from the line through the center, so uniform ink cancels out and only oriented strokes respond.

I'm settling the conv1 kernel as a zero-mean ridge along each orientation, scaled so an ideal line gives a response near one, with the flanks negative so perpendicular strokes don't light it up.

I'm settling the conv1 normalization so the positive weights sum to one, which should keep feature values roughly between 0 and 1, and I'm setting a small negative conv1 bias to suppress noise. For conv2 I'm using single-tap unit weights with no bias, then ReLU and pooling, so the pooled features are max responses over the 8x8 input windows.

I'm checking the pooling arithmetic: each pool1 row pair maps to conv1 rows 4b through 4b+3, so bin b covers input centers 4b+2 to 4b+5. That makes the six bins non-overlapping 4-row blocks spanning rows 2 to 25, a clean 6x6 grid.

I'm checking the offset mapping: a tap at dy=4 reads pool1 rows shifted by two pool rows, so each pool2 cell lines up with bin i+2, and in general the bin is i plus half the offset.

I'm mapping the fc weights back to the 6x6 bins: each feature's channel gives an offset, so I divide each weight by how many channels feed the same bin to avoid double counting. Next I'll start laying out the digit strokes in 28x28 coordinates, with the digit roughly inside rows 4 to 23.

I'm now laying out each digit's strokes in normalized coordinates, mapping them onto the 28x28 grid, with the digit roughly 20 rows tall and typically 12 to 16 columns wide. I'm starting with the zero as an ellipse and the one as a near-vertical slanted line, and I'll keep going through the remaining digit shapes.

I'm laying out the digit strokes as polylines in normalized coordinates: the 2 as an arc over the top, a diagonal down to the lower-left, and a flat base; the 3 as two bowls meeting at a middle point.

I'm now writing out the stroke polylines for the remaining digits, with the 4 as a left diagonal plus a right vertical, and the 5 as a top bar, a short drop, and a lower bowl.

I'm listing the coordinate points for the 7 and 8 digits, and I'm sketching the 9 as a top loop with a slanted stem.

I'm settling the sampling step: I'll walk each stroke polyline densely and tag every point with the direction of its segment. Then I'll pick the nearest of the four orientation channels, horizontal, vertical, or either diagonal, and weight it accordingly.

I'm now weighting each stroke point across the four orientation channels by how closely its direction matches each one, then spreading it over the six-by-six bins with a Gaussian falloff. Once the per-digit templates are built, I'll normalize them and subtract the mean across digits, then scale the result to get logits.

I'm weighing whether the matched-filter scores will be skewed by how much ink a digit has, since 8 and 0 would dominate. Subtracting the mean template should help, and I may need a per-digit bias. I'll start with a scale around 4 and tune from there, while keeping the line-detector bias small and negative.

I'm checking the mean of the zero-mean horizontal kernel: with offsets from -2 to 2, the center row lands positive while the outer rows drop negative, so the balance hinges on where the Gaussian profile crosses the mean.

I'm checking the horizontal ridge against a vertical stroke of width 3: the positive center row sees only a little of it, so the response stays low, and I'm keeping sigma at 1.0 so thicker strokes don't swamp the negative flanks.

I'm checking the zero-mean horizontal kernel against a vertical stroke: its columns each sum to zero, so that response vanishes, and a diagonal stroke only gets a partial positive response. I'll also keep the kernel spanning its full five-pixel length, and set conv1's bias to a small negative value so weak responses are suppressed.

Now I'm writing the weight-building code, setting up the four orientation kernels for the first convolution.

I'm building the four orientation kernels for the first convolution, measuring each point's perpendicular distance from the line through the center. Next I'll score stroke segments by their direction relative to each orientation, and then convert the digit polylines into the 28x28 grid coordinates.

I'm finishing the stroke sampling: each polyline gets split into points about half a pixel apart, and each point's direction is weighted across the four orientation channels. Next I'm spreading those contributions over the 4-pixel bins with a Gaussian of sigma 2, then normalizing each digit's template.

I'm turning the per-digit templates into fully normalized weights by subtracting the mean across digits, then mapping them back onto the fc layer by dividing each weight by how many channels feed the same bin. I'm estimating the logit scale from typical feature magnitudes, guessing a scale near 4 or 5 should separate the classes.

Writing the stroke polylines for the digits as coordinate lists...

Still writing the stroke coordinates for the remaining digits...

Still writing the stroke coordinates for the remaining digits...

I'm wrapping up the stroke coordinates for the digits and then moving on to writing the code.
