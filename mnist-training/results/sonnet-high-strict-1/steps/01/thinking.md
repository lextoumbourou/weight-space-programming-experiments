I'm starting to design the weights by hand, aiming for a reasonable first attempt. The first conv layer gets 8 oriented edge and stroke detectors, and I'm sketching out the first filter, a horizontal line detector.

I'm laying out the rest of the first conv layer's filters, covering vertical lines, both diagonals, a blob for ink density, and edge detectors. For conv2, I'm considering combining the conv1 channels into 16 features, though I'm still weighing how to pool them onto the grid and whether the fully connected layer should use hand-drawn digit templates.

I'm settling on a design where the fully connected layer uses spatial templates per channel, with the weights derived from stroke geometry rather than from running the network on any inputs. Conv2 would pass the first eight conv1 channels through and add eight more built from combinations of them, so I'm keeping this simple for a first pass and will refine it after seeing feedback.

I'm settling the fully connected weights as hand-built geometric templates: each digit's strokes set positive values where its orientation channels should fire and negative values where they shouldn't, with a density term for ink. I'm mapping the 28x28 canvas onto a 4x4 pooled grid through the conv layers, so each cell covers a known patch of the original image.

I'm checking where the 4x4 pooled cells land in pixel coordinates, working out each cell's center from the overlapping conv2 receptive fields, which comes out to roughly 7, 11, 15, and 19.

I'm now listing out each digit's stroke prototype as polylines in 28x28 coordinates, with the 0 as an ellipse and the 1 as a vertical line with a small flag, and I'm starting to define the 2 through 5 the same way.

Now I'm defining the remaining digit prototypes as polylines and ellipses, mapping each stroke's orientation and position onto the 4x4 grid. Then I plan to turn the samples into weights by accumulating them per channel and cell, and centering them across classes.

I'm working out the zero-sum orientation filters now: Gaussian ridges along each of four directions, with the mean subtracted so flat regions give no response.

I'm weighing six orientation filters for the first conv layer at 30° spacing, with a blob channel for ink density and one more channel I haven't settled on yet.

I'm setting the conv1 biases to a small negative value, around -0.5, since a stroke a couple of pixels wide should give a response of roughly 3 to 4. For conv2, the first eight channels will carry the conv1 channels forward with uniform 5x5 weights, and I'm still deciding what the other eight should compute.

I'm choosing conv2's other eight channels as junction detectors: each one adds two conv1 orientation responses and thresholds the sum, so it only fires where two orientations meet, like crossings or T-shapes. I'm picking pairs of the six angles for them, and I haven't finished listing the last couple of pairs.

I'm picking the conv2 channel layout: I'll keep the first channels as broad 5x5 orientation features and use a blob channel for ink, and I'm still weighing whether a "no ink" background channel with a negative bias would help.

I'm settling the fully connected weights by building each class's template from its stroke positions, then subtracting the class mean so the values are relative. The next step is picking a scale, since I don't yet know the typical size of the pooled features; my rough guess is that they land somewhere around 1 to 3.

I'm turning the stroke samples into weights by assigning each point's segment angle to the nearest orientation channels and accumulating them per cell, with a scale factor I'll tune after seeing results.

I'm working out the orientation kernels in image coordinates, with y pointing down, and computing each pixel's position relative to the center as the parallel and perpendicular offsets from the stroke direction. Then I'm weighting each cell's contribution by a Gaussian of its distance from the cell center, with σ=4 and centers at 7+4j.

I'm working out the pixel centers for the pooled cells: each conv2 output covers 14 pixels, and averaging over the two outputs in a pooled pair puts the center at 4i+7.5 before settling on the indexing.

Now I'm writing the conv1 kernel code: a ridge along each stroke direction, with a Gaussian across the stroke and a longer falloff along it, then the mean subtracted so flat regions give zero.

Writing the conv1 kernel code: normalizing the absolute sum to 2 so an ideal line gives a response near 1, with a bias of -0.2 for thresholding.

Still working out the conv2 kernels for the narrow channels...

Still writing the kernel and template code...

Still working on the fully connected weights: I'm normalizing each blob channel by its own max and scaling the orientation channels the same way, with the fc biases left at zero. I'm also settling how to sample each stroke, placing points every half pixel along its length and giving each point a weight of 0.5.
