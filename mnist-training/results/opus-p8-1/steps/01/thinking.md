I'm planning the weights by hand, starting with a first attempt that uses conv1 for edge and stroke detection and conv2 to combine those into spatial features. I'm also considering a simpler route where the network acts like a template matcher, with one conv1 channel acting as a blurred identity on the center pixel.

I'm now sizing the feature maps through the network: after the second pool, the fc layer gets 16 channels on a 4x4 grid, which is coarse but workable for templates. I'm also weighing a digit-specific conv2 alternative, though the receptive field works out to roughly 14x14 image pixels at stride 4. Given no data, I'll lean toward oriented edge detectors in conv1 with near-identity conv2 channels, then hand-code the fc templates per digit on that grid.

I'm settling on the conv1 layout: one channel for overall ink, then horizontal, vertical, and two diagonal stroke detectors. I'm also considering a background detector that fires where no ink is present, though max pooling might make it fire everywhere.

I'm weighing whether max pooling on the ink channel would wash out the digit's shape, since almost every cell would read as on, so an average pool seems the better choice for the fc templates.

I'm sketching out how each digit's strokes would fall on the 4x4 grid, so the fc templates can be hand-coded per class. I'm also thinking about whether the fine detail survives the pooling, since the 4x4 cells are only about four image pixels wide.

Now I'm working out how the receptive fields map onto the 4x4 grid: each pooled output lands on a block of about four image pixels, and with only the center tap in conv2 the coverage narrows to a small window.

I'm checking how the conv2 pooling maps to image coordinates, which puts the cell centers at roughly 7.5, 11.5, 15.5, and 19.5 with each cell covering about an 8-pixel window. I'm also noting that digits span roughly rows 4 to 23, and that a narrow digit like 1 takes up less width. Finer location detail would need shifted conv2 taps, but the 4x4 grid stays as the final resolution.

I'm considering the alternative of templating each digit as polylines on a 28x28 grid and deriving features from those, though I can't run the network on inputs to check it. I'm weighing whether to fold ink channels into the orientation templates instead of building 800 values by hand.

I'm building each digit's template by hand from stroke descriptions instead of running the network. For every segment I'll sample points, spread them over the 4x4 cells, and assign weight to the matching orientation channel, then center the fc weights across digits and set the bias.

I'm settling the first conv1 filter as a horizontal line detector, a 5x5 kernel that responds to a stroke about three pixels wide, and I'm weighing whether its weights should sum to zero so a uniform blob of ink doesn't trigger it.

I'm settling the horizontal detector's weights as a zero-sum profile, so a uniform blob of ink gives no response and a three-pixel stroke gives a strong one. For the diagonal detectors I'm switching to a distance-from-line profile with a Mexican-hat shape, positive on the line and negative just beside it.

I'm turning the diagonal detector into a rotated version of the same profile, with the perpendicular distance from the line as the variable. I'm also weighing a Gaussian taper along the stroke so the corners don't respond as strongly, then zero-centering the kernel and scaling it so a three-pixel line gives about one.

I'm settling the conv1 biases at a small negative value so noise stays quiet, and I'm making the ink channel a normalized Gaussian blur so uniform ink reads as 1.

I'm setting conv2 to pass the conv1 channels straight through with a center tap, and leaving the remaining channels at zero.

I'm turning each template into a feature vector by taking the max of a Gaussian weight over the stroke points that fall in each grid cell. The logits can then be written as a template-matching score minus half the template's squared norm, which is the same as a negative squared distance, so the scale of the templates has to match the feature scale.

I'm turning the stroke features into a soft ink measure per grid cell, so a cell reads as on whenever a stroke point falls within about four pixels of its center. I'm also starting to set up the orientation channels.

I'm settling on a feature response for oriented detectors: each orientation channel gets a value of ((1 + cos 2Δ)/2)² for angle difference Δ, so a match at 45° off drops to about 0.25 and a perpendicular one to zero. Real strokes should give pooled values somewhere around 0.6 to 1, which I'll keep in mind when scaling the templates.

I'm settling the logits as a scaled template match, with a norm-based bias term so each digit's score behaves like a negative squared distance. Next I'm placing the digits on the 28x28 grid, starting with 0 as an ellipse centered near (14,14) and 1 as a nearly vertical stroke.

I'm listing the stroke points for each digit on the 28x28 grid, starting with the curve and diagonal of a 2 and then the two bumps of a 3.

I'm writing out the stroke points for digit 4 and then for 5, sketching each one as a sequence of row and column coordinates on the 28x28 grid.

I'm writing out the stroke points for the 6 and 7, then the 8 as two stacked loops with a top circle centered near (9,14).

I'm placing the digit stroke points on the 28x28 grid, with the 4x4 cell centers at 7.5, 11.5, 15.5 and 19.5, and checking how the soft cell assignments line up with the conv1 detector positions. Next I'll work out the scale of the conv1 responses so the feature values come out in a usable range.

I'm checking the scale of the conv1 responses, expecting a stroke that lines up with a detector to come out around 0.7 to 1, with the negative side of a zero-mean filter staying near zero on plain background. Then I'm defining the diagonal detectors using the stroke angle, with horizontal at 0, vertical at π/2, and the down-right diagonal at π/4.

I'm settling the fc logits as a scaled template match, with a norm term so each digit's score works like a negative squared distance, and I'm starting with alpha set to 1.0. I'm also thinking about whether the ink channel's template weight should be smaller than the orientation weights.

Still writing the fc weights for the templates...

Still writing the template code...

Still writing the orientation kernels and the conv2 pass-through weights...

Still settling the weights: I'm giving the ink channel half the weight of the orientation channels and leaning toward a scale factor of 1.0 for the templates.
