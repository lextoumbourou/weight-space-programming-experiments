I'm at about 65% accuracy, a decent start. The main gaps are the confusions between 0 and 2, 4 and 9, and a few others, and I'm weighing ways to add more spatial detail and features, such as sampling the unused conv2 channels on a finer grid.

I'm weighing a finer sampling grid over the unused conv2 channels, since the current 4x4 grid at 8x8 windows looks too coarse. For the 4-versus-9 confusion, I'm thinking about the open top and the long middle crossbar, and whether averaging a slanted and a vertical-left drawing would make a better 4 template. I'm also considering biases to offset the over-predicted 2, 5, 6, and 9 and the under-predicted 4 and 8.

I'm considering a structural change next: adding more features from conv1 channels 5 through 7. The 0-versus-2 errors, around 199 cases, might come from zeros being drawn wider or slanted so their sides look like the 2's diagonals, and I'm wondering whether the 2 template's top arc and bottom bar also overlap with a zero's shape. I'm also checking whether the loss of 1.22 at 65% accuracy suggests the scale is roughly right, though that's hard to judge from these numbers alone.

I'm weighing a shift to a finer spatial grid, using 4 orientations at 4 sub-offsets so the features can localize the strokes more precisely.

I'm thinking about a finer grid over the unused conv2 channels, using small blocks at several offsets so the sampling lands on strokes more precisely than the coarse 5x5 layout. The offsets would overlap heavily, though, so it may just repeat the same positions rather than add real resolution.

I'm working out how a finer grid of conv2 features could sample the strokes more precisely, with 1x1 kernels at several row offsets. Because of the 4-pixel pooling stride, the sampling still lands on a regular grid, so the offsets mostly shift where the same positions fall.

I'm weighing a finer grid for the conv2 features, shifting the sampling by two pixels so the centers fall between the current positions. The new kernels would be 2x2 blocks at offsets of one and two, which should localize strokes better than the existing layout.

I'm settling on a finer sampling layout: 16 conv2 channels, four orientations at four 2-pixel shifts, which would tile the digit with 6-pixel windows across roughly 6.5 to 22.5 in both directions. That covers most of the digit area, though the edges may clip a little off the top and bottom.

I'm settling the sampling for the template grid: an 8x8 layout with Gaussian sigma around 3 so the templates tolerate writer variation. I'm not fully convinced finer features will beat the blurred templates, but the maxes over 6-pixel windows should sample strokes better. I'm also weighing multiple prototypes per digit, such as straight and slanted versions of a 1 or 7.

I'm settling on 16 conv2 channels, four orientations at two shifted 2x2 offsets, so the sampling grid is finer. I'm also looking at averaging multiple prototypes per digit, though I'm less sure the scoring needs a per-digit bias, since the feature layout is changing anyway. The main worry is that the new layout might score worse, but trying it seems worth it at this stage.

I'm checking the coordinate math for the new conv2 layout: channel index is k·4 + sy·2 + sx, and the 2x2 blocks at offsets 1 and 2 should put centers at 6.5 + 4i + 2s, which I still need to confirm against the input-center range.

I'm defining the digit templates as ellipses and strokes, then generating shear variants so the slanted forms of each digit get covered too, starting with a slanted and a round version of the zero.

I'm weighing whether drawing the 0 template with a single fixed slant, or as a few hand-drawn variants combined into one, counts as legitimate template design rather than averaging over generated samples.

I'm going through the digit variants one by one, starting with a plain and a slanted vertical line for the 1, then giving the 4 two different drawings, an enclosed slanted one and an open one with a separate crossbar and stem. The remaining digits keep their earlier shapes, with the 7 getting a second version that has a slight curve.

I'm going through the template variants in order: a few shapes for each digit, with the 4 and 9 each getting two distinct drawings. I'm keeping the template normalization and the feature count as they are, since the total stays about the same.
