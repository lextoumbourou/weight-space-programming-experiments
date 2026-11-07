The predictions are now leaning toward 2 and 4, and the 4x4 coarse density readout seems to be the limit. With 12 steps left, I need a better approach. I'm considering whether the conv2 channels can encode finer spatial detail through different offsets.

I'm weighing whether the readout is the real bottleneck: with blurred 4x4 features and a linear template, the class biases keep drifting toward 2 and 4. Class 1 is rarely predicted because its thin stem leaves little ink, so its logit sits near the bias, and manually lowering the biases for 2 and 4 looks like a reasonable fix.

I'm reconsidering the readout bias: a class with a thin, low-ink template sits near zero from the weights, so the bias term is what decides it. I'm thinking about estimating the feature mean from the feature scale rather than guessing it, but I can't run the network, so the adjustment has to be hand-designed. Given the remaining steps, I'm leaning toward a more discriminative feature set using all the stroke channels instead of a large redesign.

I'm sketching per-orientation presence maps on the 4x4 grid for each digit, since that should separate 1 from 0 better than density alone. Hand-drawing all of them is too many numbers, so I'm considering generating them from simple stroke-segment descriptions instead.

I'm considering whether to build the orientation-channel templates by rasterising hand-described strokes, since density alone doesn't separate 1 from 0 well. The rest of that thought is about the orientation maps.

I'm thinking about splitting each cell's ink into halves, so the readout can see where within a 4x4 cell the strokes sit rather than just how much there is.

I'm considering whether the sub-cell position of the strokes could be captured by using shifted conv2 kernels, with the max pool combining them, though that only helps if conv1 gives sharp stroke-level density. I'm leaning toward accepting something near 50 to 70 percent given the remaining steps.

Next I'm going to try to sharpen the templates and fix the class bias that keeps pulling predictions toward 2 and 4. I'm thinking about using a centre-weighted conv2 kernel to cut blur, and redrawing the per-digit templates to match the 4x4 grid more closely.

I'm checking the class biases against the confusion counts: 4 gets predicted for 9, 6, 7, 2 and 0, and 2 for several other digits. Class 4's template is heavy on the middle row and right stem, so its weights push up on typical digits, and I want to see whether the common-mode bias correction is actually cancelling that.

I'm working out why the common-mode term doesn't cancel: if the feature mean is roughly uniform, the logit offset depends on each template's total sum across cells. I'm checking whether the sum of each class's template is what's pushing 2 and 4 upward.

I'm checking whether the bias term is what pushes class 1 down, since its template has little total ink and the centred logit ends up negative. The confusion counts show 2 and 4 absorbing too many predictions while 1 is mostly sent to 2, so I'm weighing a direct bias correction against a fix to the mean-centring itself.

I'm now weighing a normalised template score for the readout: each class logit becomes its template dot the features, minus half the template's squared norm, which turns the matching into a proper Gaussian-style comparison rather than a raw sum.

I'm switching the readout to a distance-style score: each class logit uses its template dotted with the features, minus half the template's squared norm, so classes with a lot of ink are no longer favoured by default. Since the features roughly match a scaled template, the full-vector comparison should take care of the total-ink bias that the zero-centring was causing.

I'm switching the readout to a Gaussian-style distance: each class's weights are its template scaled by a gain, with a bias of minus half the squared template norm. That should stop classes with a lot of ink from winning by default, and I'm settling on a scale factor around 0.5 so the logits stay in a reasonable range.

I'm going to switch the readout to a distance-based score, so classes with lots of ink stop winning by default, and I'm keeping the scale small so the logits stay moderate. Still, a 4x4 template match probably only gets to around 35 to 45 percent, so I'll need richer features, perhaps shifted density channels that capture sub-cell position.

I'm thinking about splitting the conv2 kernels into shifted quadrant-style windows, so each 4x4 cell can tell upper-left ink from lower-right ink instead of only total density. That would give the readout sub-cell position information, and I could fill the spare channels with orientation features from the other input channels.

I'm weighing a Gaussian-style template readout to stop class bias, and then considering whether splitting the stroke channels into orientation groups could sharpen the 4x4 features.

I'm sketching the per-orientation maps on the 4x4 grid, using the stroke channels from conv1 with the vertical detector as one example. Each digit's strokes would light up different cells: the centre for 1, the right stem for 4 and 9, the sides for 0 and 6. Hand-writing all of those numbers is a lot of work, so I'm weighing whether the effort is worth the uncertain payoff.

I'm weighing a Gaussian-style distance classifier over density plus the vertical, horizontal, and diagonal stroke channels, which would need hand-drawn templates for each orientation. Writing 40 templates by hand is error-prone, so I'm also considering keeping just density and fixing the bias through the Gaussian formulation instead.

I'm weighing a multi-channel readout, using the density map plus vertical, horizontal, and diagonal stroke channels, to see whether it can reach the 55-65 percent range. Writing a full set of hand-drawn 4x4 templates for each channel would be a lot of work, so I'm considering deriving the orientation maps from each digit's density template instead.

Next I'm planning to write out a set of orientation maps on the 4x4 grid, vertical, horizontal, and both diagonals, alongside the density templates, which means around fifty small maps in total.

I'm settling on the Gaussian-style readout with a shared gain, so each class's bias is minus half its template norm, and I'm planning to hand-write the orientation maps for the stroke channels alongside the density templates.

Now I'm working out the orientation maps for the stroke channels, which should give the readout a bit more to work with than density alone.

Writing out the orientation maps for digit 0, with vertical strokes on the sides and horizontal arcs at top and bottom...

Writing the orientation maps for digit 0 now, with vertical strokes down the sides and horizontal arcs across the top and bottom...

Continuing the orientation maps, I'm now on digit 1's remaining small-stroke patterns and moving on to digit 2's horizontal top arc and the diagonal from the right middle down to the lower left.

Still writing the orientation maps for digit 3 and the rest of the digits.

Still writing the digit 4 slash map and the rest of the orientation templates...

Still writing the digit 4 and 5 orientation maps.

Still writing the digit 6 orientation map and the remaining stroke templates...

Still writing out the orientation maps for digit 6, filling in the vertical, horizontal, and diagonal weights for the upper curve and lower loop.

Still writing the digit 7 orientation maps, filling in its diagonal and vertical weights.

Still writing the digit 8 orientation maps, filling in the side verticals and the stacked horizontal arcs.

Still writing the digit 8 and 9 orientation maps.

Still writing the digit 9 orientation maps, filling in its vertical stem and the horizontal arcs.

Still working out the stroke templates for digit 9 and the rest of the orientation maps, mostly rough estimates for now. I'm weighing whether a density-only Gaussian classifier with a better bias term would be the simpler route to a useful gain, since hand-writing every orientation template is slow. My guess is that density alone gets around 35 percent, and the extra orientation channels might add roughly ten more points, so I'll keep going with them as the design.

Still working out the Gaussian readout constants, scaling each class's weights by the template and setting the bias from the summed template norms.

Still writing the Gaussian readout constants, working out how the scale and bias terms come out for the density and orientation templates.

Still writing the vertical orientation maps for each digit and sketching the Gaussian template constants.

Still writing the vertical orientation maps for digits 5 through 9.

Still writing the horizontal orientation maps for digit 0.

Still writing the horizontal orientation maps for digits 0 through 6.

Still writing the slash orientation maps for digit 0 and the rest of the digits.

Still writing the slash orientation maps for digits 4 through 6.

Still writing the slash and backslash orientation maps for the digits.

Still writing the bilinear-style orientation maps for digits 3 through 9.

Still writing the Gaussian readout constants and the orientation templates for digit 9, with the bias term tied to the summed template norms.

Still working out the Gaussian readout scale: the weights come out as a scaled copy of the templates, and the bias is set from their squared norms.

Still settling the readout: I'm checking whether the Gaussian scale and bias need to match the actual feature magnitudes, though the cross term should still rank the classes sensibly.
