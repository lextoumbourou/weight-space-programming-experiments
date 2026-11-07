I'm working out the weights by hand, starting with first-layer edge or stroke detectors. My plan is to approximate a template-matching classifier, using an ink detector in the first channel and pooling to downsample.

I'm sketching the later layers now: conv2 would pick out coarse oriented strokes, and the fc layer would match each digit's expected stroke pattern on a 4x4 grid. I'm checking the receptive fields, which get heavily overlapped at the final pooled cells, so I'm considering making conv2 kernels use only the center taps to keep the features more localized.

I'm checking the coverage math: with only the center tap, the pooled 4x4 cells line up well over the 20x20 digit box. I'm also weighing whether a hand-drawn stroke template could be used for the fc weights, since running the network on inputs to compute features is off the table.

I'm settling on the fc weights as hand-made stroke templates, with each digit's orientation pattern set per 4x4 cell from a stroke description rather than from any network run. For the first layer I'm laying out eight channels, starting with horizontal, vertical, and the two diagonal bar detectors, and I'm still deciding what the other four should be.

I'm settling the first-layer kernels: the ink channel stays as a plain intensity read, and the remaining channels get zero-mean line profiles so solid ink cancels out. For the horizontal detector, I'm weighing a five-row profile with a positive center band and negative flanks, sized for strokes about three pixels wide, with a slight negative bias to suppress noise.

I'm weighing whether conv2 should use shifted taps instead of the center tap, so the 16 channels cover finer offsets within each pooled cell. Pooling over a 2x2 block of those positions would then give each final cell a slightly wider input window, roughly six pixels per pooled position.

I'm now thinking about how to build the fc templates by describing each digit as a set of strokes on the 20x20 box, then mapping those strokes onto the 4x4 grid of orientation features.

I'm turning each digit into a stroke description on the 20x20 box, sampling points along each stroke, and assigning them to the overlapping 4x4 cells by orientation, which I'll then center by subtracting the class mean.

I'm pinning down the exact mapping from input pixels to the final 4x4 cells, with the conv2 center tap in place. A line centered at row y shows up first at conv1 position y-2, and after the two pooling steps each final cell covers line centers in a fixed band of rows.

I'm checking how conv2 taps spread over a 2x2 or 3x3 neighborhood instead of the center alone, to see whether the final 4x4 cells can cover the digit box more fully.

I'm weighing a 3x3 summed tap over the center-only version, since it spreads each feature over an 8-pixel band and tolerates small shifts better. I'm noting the final cell bands for each of the four 4x4 rows and planning to fill the remaining conv2 channels with extra features.

Now I'm setting the conv2 channels: four orientation features with a 3x3 sum, plus a center-tap copy for tighter localization, and ink channels as well, with the rest left at zero. Then I'm assigning the conv1 channels to horizontal, vertical, and the two diagonals, with plain ink in channel 4 and channels 5 through 7 kept at zero. For the template, I'm about to work out the orientation angle of each stroke point, starting with horizontal strokes at zero degrees.

I'm writing the line-detector kernels now, setting each one's direction from its angle and working out the perpendicular distance from every pixel to the line.

I'm normalizing each line-detector kernel so its positive taps sum to one, and I'm weighing a bias set to a fixed fraction of that positive sum to suppress weak responses.

Now I'm setting the ink channel and conv2 weights: a 5x5 uniform read for ink, orientation features with a 3x3 sum, center-tap copies, and zero biases.

I'm defining the fully connected templates per digit by laying out the stroke paths in pixel coordinates on the 28-grid, since MNIST keeps the aspect ratio and centers each digit.

I'm now defining each digit's strokes as points on the 28-pixel grid, starting with the zero as an ellipse and the one as a slightly slanted vertical line. For the two, I'm sketching a top arc that drops into a diagonal and then a bottom horizontal, and I'm about to lay out the three the same way.

Still writing out the stroke coordinates for digits 3 through 7...

Still writing the stroke coordinates for the digit templates...

Now I'm writing out the template weights by turning the stroke sampling into Gaussian density maps, with the 3x3 channels spread wider than the center-tap ones.

I'm working out how to scale the fc templates: the logit can be read as a negative squared distance to each digit's expected feature vector, so the weights become that expected vector over a variance and the bias carries the norm term. That means the templates have to be in actual feature units, and I still need to estimate the magnitude of the orientation responses.

I'm turning the template into a presence map by taking the strongest orientation response in each cell, then scaling it down for the 3x3 channels since their pooled inputs are spread thinner.

I'm turning the presence values into a capped sum over the stroke points, normalizing by a stroke length of about six pixels and keeping the center-tap band narrower than the 3x3 band.

I'm settling on a Gaussian-style scoring for the fc layer, where each digit's logit is its expected feature vector scaled against the observed features, minus a norm term.

I'm settling on σ² = 0.5 for the Gaussian scoring, so the weights become twice the expected feature vectors and each bias is minus the squared norm of that vector. I'm not fully confident the feature magnitudes I've estimated are right, so the scale could be off.

Working out the first-layer kernel for horizontal edges: I'm taking a Gaussian profile over the row offset, then subtracting the mean so the kernel is zero-centered, and normalizing the positive taps to sum to one.

Checking the width-5 case: those edge pixels would all be positive, so a thick stroke gets a weaker response.

I'm working out the diagonal kernel next: the distance from each pixel to the line is the offset between row and column divided by root two, so the on-diagonal taps are closest and the corners are farthest.

I'm computing the diagonal kernel values with a Gaussian falloff and then zero-centering them. The positive part gets normalized so a perfect stroke comes out near one. I'm weighing whether to check the calibration by running the kernel on a synthetic line, which would be the same as running the network on an input, so I'm hesitating over that.

I'm settling the diagonal kernel's bias at about -0.15, which should leave a peak response near 0.7. A horizontal kernel on a diagonal stroke should only give around 0.3, so the off-orientation signal stays weak after the bias. Pooling with max keeps the strongest value in each cell, so the cells the stroke passes through carry most of the signal.

Now I'm estimating the ink channel: a 5x5 average over a stroke about 2.5 pixels wide gives roughly 0.5, and after ReLU and max pooling it should land near 0.55.

I'm weighing whether to keep the ink channel: it's mostly redundant with the orientation features, though it could help with things like holes, so I'll keep a center-tap version of it. I'm also leaning toward linear logits with mean-centered templates rather than the Gaussian scoring, since that avoids depending on the exact feature magnitudes.

Now I'm working out how to compute the presence features for each digit: sampling points along the strokes and building the per-channel maps for the 3x3 and center-tap orientation channels.

Now I'm defining the presence features for each digit: a soft-edged sum over the stroke points for the 3x3 orientation channels, and a max over the points for the center-tap channels, each scaled to a typical response level.

Next I'm settling on the variance: with σ² = 0.1 the logit gaps would run around 37, which is far too confident, so I'll take σ² = 0.4 instead and keep the weights at 2 on the expected features.

I'm settling on the orientation weights as max(0, cos 2Δ), where Δ is the angle between the stroke direction and each detector's orientation, so a 45° stroke gives zero response and a 22.5° offset gives about 0.7. I also need to make sure the angle convention matches the kernel: the stroke angle comes from atan2 over row and column increments, and the perpendicular distance is |u cosφ − v sinφ|.

Now I'm defining the stroke coordinates for each digit as points, using an arc function for the curved parts and straight lines for the rest.

I'm defining the stroke coordinates for the digit 4 as a set of line segments, with one vertical stroke on the left and a crossbar running down the right side.

I'm moving on to the digit 8 next.

Writing the stroke coordinates for the digit 9 and then moving on to the code that builds the weights...

Still writing the weight-construction code...

Still writing the sampling helpers and the per-point kernel-response accumulation...

Still writing the presence-feature code and the flattening of the channel maps...

Now I'm writing up the explanation and the code.
