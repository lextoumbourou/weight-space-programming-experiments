We're at 40% with nine steps left, so I want to step back and figure out what's going wrong. I suspect many of the failures come from misreading the features rather than from the template design itself. I'm going to check whether the "ink presence" features still carry useful information at the 4x4 grid, and I'll also verify how each final cell maps back to the conv2 positions.

I'm tracing how a final grid cell maps back to the input: each one depends on a 12-pixel window of ink, with neighboring windows overlapping. That makes the final features a heavily blurred 4x4 view, so I'm wondering whether a better template design could get past the current 40%, or whether a more localized conv2 channel would be necessary.

Narrowing the conv2 kernel to just the center cell would shrink each final window to about 8px, but with stride 4 the four cells would only span roughly 4 to 23 of the 28px field, leaving the digit's edges uncovered. Checking that coverage gap now.

I'm asking whether 16 channels per cell could encode finer position within each window, for example separate channels for the top and bottom halves, instead of just one ink-presence feature per cell.

I'm checking whether splitting each cell into sub-window channels could recover finer position. A kernel covering only pooled rows q+1 to q+2 would span about 8 input pixels, which might give upper and lower sub-cell detail.

I'm splitting each final cell into top and bottom 8px sub-windows, offset by 4 pixels, to see whether that recovers finer vertical position within the 12px window. I'm considering whether the same idea works horizontally, which would give four sub-window channels per cell.

I'm splitting each final cell's window into four overlapping sub-windows by choosing which pooled rows and columns feed in, which would give finer position information within each cell.

I'm checking whether splitting each cell into sub-windows with different row and column choices gives finer position info, and it looks like the offset windows just land on the same set of centers at a narrower width, so the grid resolution doesn't really improve.

I'm checking whether splitting each cell into two row-offset sub-windows adds real resolution, and it looks like the offsets only produce about five distinct centers instead of eight, so the grid barely improves.

I'm noting that the 40% accuracy likely reflects weak templates rather than a hard ceiling. The ink-only features are already in place, and the main issue now is that digit 1 is absorbing many predictions because its prototype sits in the dense center.

I'm looking at why digit 1 keeps winning: its prototype is concentrated in the center, so any digit with center ink scores high for it. Normalization makes its weights larger per cell, and nothing penalizes 1 when ink shows up where it expects none.

I'm thinking the negative evidence has to come from somewhere, since a plain dot product never penalizes ink showing up where a digit expects none. The Gaussian form might supply that implicitly, but its scale and density seem to be what broke it before.

I'm working out whether the negative evidence can come from the quadratic form: the f² term is the same for every class, so it doesn't change the ranking, and the real difference between classes sits in the mean-weighted terms for each cell.

I'm working out whether the Gaussian form already supplies negative evidence: the quadratic's class-independent terms drop out, so the ranking depends only on how each class's per-cell means compare. The next idea I'm weighing is a signed template where each class's weights push its score up where ink should be and down where it shouldn't.

I'm weighing a practical route: keep the Gaussian form but calibrate the feature scale carefully, or threshold the features so only dense ink registers. Since I can't observe the outputs to tune against, I'm not sure which fix would hold up.

I'm considering a class-contrast template instead: each digit's weight on a cell is its occupancy minus the average occupancy across digits, so cells where a digit has less ink than average become negative weights. That would penalize stray ink in places like the outer columns for the digit 1, which the plain dot product never does.

I'm realizing that subtracting a class-independent mean doesn't change the argmax, so that kind of contrast can't supply the negative evidence I need. The 1-sink would only be fixed by a class-dependent term, like the norm penalty in the quadratic form, which I had dropped when normalizing the prototypes.

I'm reconsidering the Gaussian approach: the failures may come from a mismatch between the quadratic bias and the linear term, rather than from the features themselves. If the features roughly match occupancy in the same units as the prototypes, nearest-prototype in L2 should be a reasonable classifier, but the sinks suggest the scales are off.

I'm going to see whether simulating the actual feature pipeline on the drawn canvas gives better prototypes, by applying the same average pooling, ReLU, max pooling, blur, and pooling steps to each digit. That should account for the inflation and spreading that make the raw occupancy values a poor match for the features.

I'm weighing whether to run the feature pipeline on the drawn template to calibrate the prototypes, but that feels too close to running part of the network on an input, so I'll set it aside. Instead I'm considering a Gaussian classifier with the gain chosen by comparing how earlier attempts at gains 1.0 and 1.5 behaved.

I'm weighing whether a more robust classifier could escape the scale problem, such as nearest-centroid on the 4x4 features, and I'm estimating that such a method might reach roughly 60-65%, so the current 40% leaves room to improve.

I'm wondering whether richer features with multiple spatial windows could help, since the Gaussian keeps sinking one class, most often digit 1 with its dense center prototype. Nearest-centroid on a more informative representation might work better, though I can't test it, so it's a gamble with the nine steps left.

Working through the stroke response numerically: a stroke about 2.5 px wide fills roughly half of a 5x5 window, so the conv1 value sits near 0.5 in the stroke interior and drops toward the edges. After max-pooling, that interior value should carry through at about 0.5, which gives me a rough scale for the features to match against the prototypes.

Estimating the pooled ink response: a stroke about 2.5 px wide gives a value near 0.5 after pooling, dropping off with distance. Through the conv2 blur and the second pool, a stroke crossing a cell's window should land around 0.35 in the feature.

I'm checking whether the occupancy estimate matches the features once the max-pooling is accounted for, which suggests a gain near 1.3 rather than 1.5. That makes me wonder why the earlier Gaussian attempts with mu up to 1 still failed, possibly because the quadratic term's size interacts badly with larger prototype values.

I'm still stuck on whether the Gaussian fails because of the scale of the features rather than the template shape. The quadratic bias and the linear term may be out of proportion, so a fixed gain around 1.2 with a variance near 0.25 seems the most principled option to try next.

I'm considering whether a bias that scales with each class's expected ink mass, rather than with the squared prototype values, could make the scores less sensitive to the feature scale.

I'm considering a centered score where each class's weights act on the feature minus a baseline β, so cells below baseline push a class down when it expects ink there. That gives the negative evidence I've been missing, and it would keep the outer-cell features from favoring the digit 1, whose prototype is near zero there.

I'm checking whether centering the features around a baseline β would give the negative evidence I've been missing, since cells where a digit expects ink but the image has none would then count against it. The baseline near 0.1 seems right for the background windows, though a class expecting ink in a hole, like the center of a 0, would still be penalized only indirectly.

I'm now thinking that richer features would help more than tuning the Gaussian, so I'm considering orientation-specific channels, separating vertical, horizontal, and diagonal strokes at the 4x4 level. Building prototypes from orientation maps could separate the 1 from curved digits like 0 and 8, though it's hard to verify without testing.

I'm thinking about building orientation-specific feature canvases: vertical, horizontal, and diagonal strokes drawn separately, so the prototypes can capture stroke direction. The conv1 oriented filters should respond to each direction, and after pooling and blurring, the feature at each cell would reflect how much of each orientation falls in its window. The open question is whether the filter response scale, given the negative bias, will match the prototype values.

I'm now working out whether the vertical, horizontal, and diagonal filters separate strokes cleanly, with a full vertical stroke giving about 1.0 and a diagonal one only around 0.4 on the vertical channel. Once that holds, I'd build orientation-specific canvases so each prototype channel reflects its own stroke direction.

I'm now working out how to turn each stroke's direction into orientation-specific weights, so that vertical, horizontal, and diagonal strokes each feed their own channel in the prototypes.

I'm turning the orientation weights into per-pixel rasterization, so each stroke feeds the vertical, horizontal, and diagonal channels in proportion to its direction, and then taking occupancy per window. Next I'm assigning the total ink channel and the orientation channels to the feature slots.

I'm considering how orientation-specific features might separate the 1 from the 0 and 8, since the vertical channel should respond to the 1's stroke far more than to curved digits. The Gaussian score would weight each channel's cells with its own variance, and the orientation prototypes are likely to carry roughly half the magnitude of the total ink channel.

I'm checking how the classifier handles the sink problem: classes with dense expected ink carry a large negative penalty under the Gaussian, so I'm considering whether centering the per-channel features around a global mean would blunt that effect before I commit to the orientation-specific design.

I'm checking whether the Gaussian score is actually sensitive to the gain: since a shared variance only rescales the score, the argmax depends just on how the feature scale compares to the prototype scale, so I want to find the gain that maximizes the fit.

I'm weighing whether the Gaussian's gain is the real problem: the gain setting only matters relative to the prototype scale, so g near 1.5 could still be fine and the step-5 failure might come from window alignment or stroke geometry instead. Since I can't pin the scale down exactly without a calibration, I'm leaning toward checking the feature-to-window mapping first.

I'm settling on orientation-aware prototypes with five channels, a gain of about 1.2, and a plain L2 nearest-prototype score, since the shared variance only rescales the score and doesn't change the argmax. I'll also check whether the outer-cell features still need smoothing to match the existing window setup.

Still writing the oriented rasterizer...

Still writing the oriented rasterizer...

Still writing the oriented rasterizer...

Still writing the oriented rasterizer...

Still writing the oriented rasterizer...

Still writing the oriented rasterizer...

Still writing the oriented rasterizer...

Still working through the orientation weights: the bias term subtracts half the squared prototype values per channel, and the weights are the gain times occupancy. I'm estimating the feature scale, roughly 0.4 for the ink channel and about the same for the blurred orientation channels, so a gain near 1.2 looks reasonable.

Settling the gains: the ink channel at 1.2 and the orientation channels at 1.5, since their filter responses are weaker. I'm writing the full file with the oriented prototypes and an L2 score, and I'll explain that the earlier failure came from normalized prototypes with no negative evidence.

Still writing the oriented rasterizer...
