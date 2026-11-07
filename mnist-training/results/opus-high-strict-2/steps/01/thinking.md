I'm sketching a hand-crafted CNN, starting with first-layer edge or stroke detectors and then template-matching on a downsampled image.

I'm now weighing whether the first-layer channel can just blur the image into a 12x12 ink map, with the second layer keeping spatial position so the fully connected layer can match digit templates on a coarse 4x4 grid. I'm also running into the constraint that I can't push the drawn prototypes through the network to get the weights, so the template weights would have to come directly from the strokes.

I'm settling on a concrete layout: the first conv layer gets oriented stroke detectors plus a raw ink channel, and the second layer's output is pooled down to a 4x4 grid so each cell can be matched by hand.

I'm checking how the 4x4 cells line up with the input rows, and working out that a center-picking kernel narrows each cell's coverage to roughly rows 4r+4 through 4r+11.

I'm working out that conv2 can carry the four stroke orientations plus the ink channel straight through, and I'd need more channels or broader kernels to fill the other slots. The 4x4 grid then gives position-specific features to hand-build the FC templates from, though I expect that to be laborious and to land somewhere around 60-80% accuracy before tuning.

I'm now thinking about giving each of the 16 conv2 channels a different spatial offset (a,b) on the ink channel, so that after max-pooling over each 2x2 block the channels together cover the 4x4 grid at several sub-positions.

I'm working out how the pooled map's resolution holds up: the second max-pool leaves a roughly 11x11 ink grid at about 2-pixel stride, which is fine enough to template against. A linear classifier on raw pixels reaches around 92% when trained, so I expect hand-built templates to land nearer 60-75%. I'm also considering whether ReLU in the second layer could add some nonlinearity to that matching.

I'm weighing whether hand-drawn digit prototypes can be turned into FC weights without running the network on them, since that's ruled out. Orientation features look more discriminative than raw ink, but I'm still stuck on how to specify templates for them by hand.

I'm laying out the conv1 kernel geometry next, with each 5x5 output position covering a fixed block of input rows, so I can then draw the feature templates directly at that resolution.

I'm pinning down the conv1 geometry: each 5x5 output sits at its center, with the ink channel averaging a 3x3 patch and the four oriented detectors putting their positive ridge on the center row or line and negative flanks on either side. Pooling over each 2x2 block of conv1 outputs then puts a pooled cell's center at roughly input coordinate 2p+2.5, so the feature grid lines up with the pixel centers.

I'm checking how the conv2 pass-through features at center offset line up with the pooled grid, which puts the four cells' centers near input coordinates 7.5, 11.5, 15.5, and 19.5 over the digit box.

I'm looking at whether conv2 can use wider aggregation for the orientation channels, summing over each 2x2 pooled block so each feature covers more area. I'm also considering a 16-channel split of four orientations at four spatial offsets, which would pack finer position information into the coarse 4x4 grid.

I'm working through which offset pairs keep the pooled rows distinct, and noting that offsets 1 and 2 give non-overlapping coverage across each pair of pooled rows.

I'm working out the feature map geometry: each pooled row p sits near input coordinate 2p+2.5, so the offset pair gives an overlapping 8x8 grid where each cell covers about two pooled rows, centered around input 5.5 to 19.5. That leaves the bottom rows of the digit box only partly covered, and I still need to check how far conv1's receptive field reaches past them.

I'm trying to pin the feature grid's horizontal center: offsets {1,2} center the features near 12.5 and {2,3} near 14.5, while the digit box centers at 13.5. I'm considering shifting the conv1 kernel center by one row to split the difference.

I'm settling on a one-pixel offset for the feature grid, since conv1 can't be shifted by half a pixel, so the features will run from about input row 5.5 to 19.5.

I'm checking whether the feature grid's coverage holds at both edges: the first offset starts near input row 2.5 and the last reaches about 22.5, so the digit box is fully spanned. I'm also noting that the orientation templates will need some blur to tolerate small misalignments, and that the logit scale will need tuning once the weights are set.

I'm settling how to set the template weights: subtracting the average template across digits so that digits with many strokes, like 8, don't win by default, and considering a nearest-centroid score that balances each template's dot product against its norm.

I'm settling the classifier's form: a nearest-centroid score, logit = β(f·T_d − ½‖T_d‖²), so the constant feature norm drops out and the templates only need to match the feature scale. Keeping conv1 responses near 1 on well-aligned strokes should make that scale work, and I'll account for max pooling and overlapping receptive fields when I check it.

I'm settling on a soft-tube rendering for each stroke, with a Gaussian falloff across the feature grid and an orientation weight that favors the channel closest to the stroke's angle.

I'm defining the conv1 line detectors as kernels that weight each pixel by its perpendicular distance from a line through the center at a given angle, so each orientation gets its own response pattern.

I'm settling the conv1 line detectors' normalization by scaling each kernel so its positive weights sum to a fixed value, instead of checking the response to an ideal line.

I'm normalizing the conv1 line kernels so a 3-pixel-wide stroke gives a response near 1, which means dividing each kernel by about 3 after working out its response to a stroke.

Setting the conv1 line kernels to unit positive mass, I'm estimating that a width-3 stroke then gives a response near 1. I'll keep the biases small and negative to suppress noise, and assign channels 0–3 to the four orientations with channel 4 holding the ink blob, leaving conv2 to use just the four orientations at four offsets.

I'm setting the remaining conv1 channels to zero and the biases to zero, then wiring conv2 so each channel picks one orientation at one of four offsets, with max pooling kept as the reduction.

I'm checking the feature grid's centers: each conv2 cell takes a 2x2 block of pooled outputs, so its center lands at input row 2s+5.5, which fits the layout I've been building.

I'm checking where the grid's coverage falls against the digit box: the top of the digit lands around s≈-0.75 and the bottom around s≈8.75, which overshoots the 0..7 grid at both ends.

I'm checking whether shifting the offsets to {2,3} would fit the digit box better, since that moves the grid center closer to 13.5, though it only trims a pixel at the top.

I'm now going back over the offset choice: the grid centers land at 12.5 or 14.5 against a digit mass around 13.5 to 14, so neither pair fits cleanly. I'm considering whether to shift the line detectors' center by half a pixel instead of picking one offset pair.

I'm weighing whether to center the conv1 line kernels at a fractional position, around 2.5, so the feature grid's mean lands near 13 instead of pushing it toward 12.5 or 14.5.

I'm settling the conv1 kernel center at 2.5 so the line detectors sit symmetrically on the stroke, then working out how the pooled grid's centers shift as a result.

I'm converting the grid's rows into input coordinates with a center of 2s+6, so the digit box spans roughly s = -1 to 8.5. I'm now working out how to render each stroke segment onto the grid as fractional coordinates.

I'm now sizing the digit templates, setting each stroke's Gaussian falloff around σ≈2.5 px so one grid cell captures about a stroke's width. I'm also estimating typical digit widths, around 13 to 15 px for most digits and much narrower for 1.

Now I'm defining each digit's strokes directly in pixel coordinates, with the 0 as a full ellipse and the 1 as a vertical line starting near the top.

I'm defining the digit 2 as a top arc, a diagonal sweeping down-left, and a flat bottom stroke, with the arc's points computed from its center, radii, and angles.

Working through the 4 stroke now: a diagonal from the top down to the left, a horizontal crossbar, and a vertical on the right, with a left vertical as an alternate form.

I'm now defining the digit 5 as a top bar, a short vertical down the left, and a lower bowl arc, then sketching the 6 as a curved stroke ending in a closed loop.

Still writing the digit stroke definitions...

I'm settling the orientation channels as four directions: horizontal, the "\" diagonal, vertical, and the "/" diagonal. For each stroke segment I'll score tuning with max(0, cos 2Δ), using 2·(dot)² − 1 on unit vectors, so each channel responds most to strokes matching its angle.

I'm settling on a Gaussian falloff with σ around 0.8 for the line detectors, which keeps their tuning fairly broad. Then I'll set the classifier's scale to β=1 for now, expecting to calibrate it once I see how the features actually behave.

I'm weighing whether a normalized correlation, dividing each template score by its norm, would avoid favoring the larger templates like 8 when the feature magnitudes run high.

I'm comparing cosine similarity against Euclidean matching: dividing each template score by its norm removes the bias toward larger templates like 8 when feature magnitudes run high. I'm also considering mean subtraction on top of that to tighten the separation between digits.

I'm settling on cosine matching instead of Euclidean distance, so each digit template is scaled to unit norm and the logit is just β times the dot product with the feature vector.

I'm settling the template width at σ around 2.5 px, which roughly matches how far a stroke's response spreads across neighboring grid cells, and checking how the falloff treats cells a few pixels away from a stroke.

I'm checking whether the line detector's tolerance really covers a stroke that's offset by a pixel, since the zero-mean kernel drops from about 0.71 when centered to about 0.3 when shifted.

I'm reconsidering the line kernel width, since pooling already aligns each stroke to some conv1 position and the detector doesn't need extra tolerance. The band for each grid cell then covers roughly 4 to 5 pixels of stroke, so I'm deciding how wide the template falloff should be to match that.

I'm settling the conv1 kernel center at (2.5, 2.5), which puts the line detector's peak between rows 2 and 3 and leaves the horizontal case asymmetric about the stroke.

I'm weighing a center of 2 for the conv1 kernel instead of 2.5, which would mean the grid centers sit at 2s+5.5 and their bands reach down to about row 21. That would leave bottom strokes like the bar of a 2 only partly covered, so I'm comparing that cost against the asymmetry of a 2.5 center.

I'm weighing a half-pixel kernel center against a whole-pixel one, since the bottom strokes sit at the edge of the coverage band either way.

I'm working out the orientation kernels now: each one is a Gaussian across the perpendicular distance from the stroke's direction, zero-meaned and normalized, centered at (2.5, 2.5) so it sits between pixel rows and columns. I'm also checking whether the diagonal kernels pass cleanly through the middle of the 5x5 window.

I'm weighing whether to keep the orientation kernel centered at (2.5, 2.5) or shift it to 2, since the two diagonals then come out slightly asymmetric. The "/" kernel ends up with two equal ridges, which could bias the diagonal channels, so I'm asking whether that cost is worth accepting.

I'm checking the "1" template next, since real 1s often lean slightly toward the "/" diagonal, and the tilt from the top-right to the bottom-left gives a vertical response near 0.93 but only about 0.37 for "/". I'm also still weighing how large β should be, because the feature norms are roughly 5 and the class differences in cosine may be small.

Still working out the orientation kernels, and I'm writing the build_weights function to set up the four direction channels.

Still writing the weight-building code...

Still writing the weight-building code...

Still writing the weight-building code...

Still writing the digit stroke definitions...

Still defining the stroke coordinates for the digit 5, checking where its bowl arc starts and ends.

Still writing the digit stroke definitions...

Still writing the rendering code, sampling points along each stroke and taking the maximum response over the grid cells.

Still writing the rendering code, sampling points along each stroke and mapping their directional response onto the grid.

Still writing the code...
