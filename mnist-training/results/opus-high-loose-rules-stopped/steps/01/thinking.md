I'm settling on a hand-designed setup: the first convolution layer will act as edge and stroke detectors across eight filters, the second will combine those features, and the final fully connected layer will do template matching over a 4x4 grid of sixteen channels. I'm also considering a simpler route, where the conv layers mostly pass along downsampled image information so the fully connected layer can work as a linear classifier.

I'm weighing whether the fully connected layer can work from the 4x4 grid of 16 channels, giving 256 features, if I hand-design digit templates for it. I'm considering encoding finer stroke-orientation information in the second conv layer so each grid cell captures which strokes sit in its region, then treating the classifier as matching those per-digit stroke layouts.

I'm sketching out the layers concretely now: the first conv layer gets a blob detector plus oriented line detectors at several angles, and I'm mapping how each 4x4 final cell traces back through the pooling and convolution steps to a patch of the original image.

I'm tracing the receptive field back through the layers: each final cell draws from a 16x16 patch of the input, and because the grid steps by 4 pixels, neighboring cells overlap heavily. I'm now checking how the cell offsets line up across the four positions.

I'm working out the receptive field for the final cells: with a center-tap conv2, each cell's max pulls from input rows that shift by 4 pixels per cell, so the 4x4 grid samples the digit's rows at a steady stride.

I'm checking how wide the coverage gets with a larger conv2 kernel: a full 5x5 sum makes each cell span rows roughly 2 to 25, which overlaps more but blurs the stroke positions. I'm weighing whether a sparser tap pattern could give the 16 channels more useful variety than that.

I'm leaning toward a feature-matching route for the classifier, since mean-digit templates on raw pixels already do reasonably well, and orientation features on a 4x4 grid might do better. I'm weighing whether to write the per-digit expected features by hand and then refine them over several rounds against the errors.

I'm turning the stroke geometry into weights: for each digit, I'd sample points along its strokes, map them to grid cells, and add weight to the matching orientation channel.

I'm sketching the first conv layer as oriented line detectors with zero-mean kernels, centered so each output lines up with a patch of the 28x28 input. I'm also working out how the digit's ~20-pixel height maps onto rows 4 through 23 before fixing the kernel shapes.

I'm settling the first conv layer as oriented line detectors with zero-mean profiles, so a uniform blob cancels out and only stroke-shaped ink gives a response. For the diagonals I'm switching to a distance measure along (x - y)/√2 so they can share the same profile logic.

I'm defining the diagonal profile as a Gaussian in perpendicular distance, centered and zero-meaned so flat regions cancel. For each oriented filter, I'm measuring each kernel position's distance from the line through its angle and weighting it by that Gaussian.

I'm settling on eight orientation channels in the first conv layer, since the 4x4 grid already captures a lot of positional information. I'm weighing whether to add endpoint or curvature detectors on top, which would need the second conv layer to carry them through.

I'm checking where the 3x3 center taps in conv2 land: the final cells would cover input centers from about rows 4–13 up to 16–25, which lines up reasonably with the digit's vertical span, so I'm moving on to the max-pool step.

I'm weighing how to set the last conv layer's channels: the eight orientation channels could be paired with eight others that use different spatial offsets for finer placement, or I could change the first layer to four orientations plus some other detector types.

I'm settling the first layer as eight oriented line detectors at 22.5° steps, and for the second layer I'm planning eight channels that pool each orientation over a 3x3 center window, plus eight that keep the same orientations but sample only the center tap for sharper positioning. I'm treating the duplicate-looking second set as acceptable for this first step, since both are computed from the same geometry with different receptive fields.

Next I'm settling on the template side: rather than hand-tuning, I'll sample points along each digit's strokes, note the local orientation at each point, and drop them into the grid cell they fall in. Those counts become the weights for each digit's fully connected row.

I'm turning each digit's expected features into fully connected weights: for every orientation channel and grid cell, I'd count how strongly the digit's stroke points match that orientation and fall inside that cell. Then I'd center those templates and set biases so the classifier behaves like nearest-centroid matching, adjusting for the templates' different norms.

I'm settling the template weights as cosine-style: each digit's centered feature vector gets normalized to unit length and scaled by a constant, with no bias. I'm still deciding how to pick that scale, since I don't yet know the real activation magnitudes of the network.

I'm estimating the feature scale: a stroke crossing a region should light up about three of the nine pooled positions, so the feature values land roughly between 0 and 3. I want the templates on that same scale so they're comparable to real activations. Mapping a point's effect through the conv and pool indices doesn't add up cleanly, though, since max pooling isn't additive, so I'll approximate the contribution softly instead.

I'm working out the template scale: since the templates get normalized anyway, only their shape matters, and I'll tune the overall scale α afterward.

I'm now placing the digit strokes in a normalized box, roughly 20 pixels tall and centered at the middle of the image, with horizontal extent scaled per digit since "1" is much narrower than most others.

I'm now describing each digit as a set of stroke paths in a normalized box, starting with the zero as an ellipse and the one as a near-vertical line, then working through the two as a top arc, diagonal, and bottom bar.

I'm now assigning the digit strokes their positions: the 3 is two arcs opening to the left, with the top arc running from the upper left over the top and down to a midpoint near the center.

I'm now laying out the remaining digit strokes: the 4 as a left diagonal, a crossbar, and a vertical on the right, and the 5 as a top bar, a short vertical, and a bottom bowl.

I'm laying out the rest of the digit strokes: the 6 as a diagonal from the top right down to the left plus a loop at the bottom, the 7 as a top bar with a diagonal running down to the left, and the 8 as two stacked ellipses.

I'm placing the nine digit's stroke ranges and noting that the one is narrow, so its horizontal width stays small. I'm also weighing that the center-of-mass shift for the seven and the four can be ignored for now. Next I'm defining each stroke's orientation as its tangent angle in image coordinates, binned into the eight conv1 directions, with a cosine-like tuning curve that falls off with angle difference.

I'm writing the conv1 implementation: each oriented kernel gets a Gaussian profile across the line normal, zero-mean over the 5x5 window, and I'll normalize it by the response to an ideal line.

I'm checking the conv1 kernel normalization against a thick stroke, where the zero-mean profile should weaken the response. I'm also looking at how a stroke edge, which is a half-plane, responds to a symmetric zero-mean kernel, and whether that half-plane sum comes out negative.

I'm setting the second conv layer's first eight channels to sum each orientation over a 3x3 window, and the next eight to take only the center tap for sharper placement.

I'm working out the receptive field for the first output position: the conv2 taps covering pooled conv1 rows 2i+1 through 2i+4 map back to input centers 4i+4 through 4i+11, so for i=0 that's rows 4 to 11. I'm re-deriving this because my first pass gave the wrong range.

I'm working out the receptive-field ranges for the second group of taps, which span centers 6 through 21 with no gaps, and I'm starting to model the pooled feature for the first group as a max over the two sub-row positions.

I'm weighing whether to build the pooled feature map directly from the stroke points, taking the max response per channel and pool cell and then applying the conv2 sums and max pooling to it. I'm leaning toward a soft membership count instead of anything that mimics the network's actual outputs, so it stays a feature model rather than rendered images.

I'm sketching the template normalization next: each digit's soft feature map gets centered and scaled by α, and I'm checking whether the stroke-count proxy stays roughly proportional to real activations.

I'm checking the template scale: with roughly 30 active features at about 2 each, the feature norm lands near 10, so α≈1 should give logit gaps around 3. Mean-subtracted templates remove most of the shared component, but a digit with heavy ink like the 8 could still skew toward it. I'm considering zero-meaning each template internally so the score doesn't depend on total ink.

Still writing the conv1 kernel code...

Still writing the conv1 kernel code...

Still writing the conv1 kernel code...

Still writing the conv1 kernel code...

Still writing the conv1 kernel code...

Still writing the orientation tuning and the feature map code...

Still writing the conv1 kernel code...

Still writing the conv1 kernel code...

Still writing the digit stroke definitions...

Still defining the digit stroke paths...

Still defining the digit stroke paths...

Still writing the membership and orientation code...

Still writing the membership and feature-map code...

I'm wrapping up the code by noting that a loss this high just means the hand-built weights won't classify well, which is fine for this exercise, and I'll keep the explanation brief.
