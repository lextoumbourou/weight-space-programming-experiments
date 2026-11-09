I'm sketching a hand-crafted MNIST CNN: 8 oriented 5x5 stroke filters in the first conv layer, pooled down to 12x12, then 16 channels with a 5x5 kernel producing 8x8 and pooling to 4x4, with a final template-matching layer over that grid.

I'm working out the receptive-field geometry: conv1 centers sit at i+2, pooling and conv2 push the effective center to roughly 2q+6.5 in input pixels, and after the second pooling the 4x4 grid lands at about 7.5, 11.5, 15.5, and 19.5 in both rows and columns. That spacing covers the digit's occupied rows 4 through 23, and I'm accepting a hand-coded template classifier that might reach 60-75% accuracy.

I'm weighing whether a narrower conv2 kernel, like the center 3x3 or a Gaussian weighting, would localize better than the full 5x5, since the wider version makes neighboring grid cells overlap heavily. I'm also considering four extra conv1 features beyond the four line orientations, such as directional edges or stroke endpoints, though I haven't settled on which.

I'm settling on a simple set of conv1 channels: four line orientations, then an ink detector and possibly a no-ink channel. I'm dropping the no-ink idea since a negative weight on ink in the linear layer already does the same job. For conv2, I'm thinking about whether 16 channels could pick up larger-scale conjunctions, but I'm not sure hand-writing digit templates over the 4x4 grid is workable without seeing the data.

I'm considering building the template layer by drawing digit strokes by hand, deriving the orientation of each segment, and placing those orientations into the matching grid cells by channel. That would make the classifier a feature-space template rather than something fit to data, which is allowed as long as I don't run the network on inputs to compute weights.

I'm planning to rasterize each digit's strokes into an orientation-by-grid template, weighting each sampled point's orientation and assigning it to nearby 4x4 cells. Then I'll normalize the templates to zero-mean across classes and unit-ish norm, so they work as matched filters over the conv features.

I'm weighing whether the template weights should just be the hand-drawn templates normalized to unit length, or whether I should subtract a penalty where the template is empty so that stray ink counts against a class. I'm wondering if a plain mean-subtraction across classes is still acceptable here, since the templates come from strokes I describe by hand rather than from any run of the network.

I'm now weighing whether to normalize each template by its own length and then subtract its own mean across the features, so that ink placed where a template is empty counts against that digit without comparing templates to each other.

I'm checking the line-detector kernel: a zero-sum profile across the stroke, so a centered stroke gives a positive response and a perpendicular one cancels out. For diagonal orientations I'm planning to use a rotated profile with a zero-sum Mexican-hat shape.

I'm weighing whether 8 orientation channels at 22.5° steps would separate slants like 1 and 7 better than 4, even though a 5x5 kernel gives coarse angular resolution. I'm also considering spending the other four channels on directed edge polarity, such as top versus bottom stroke edges, though that may mostly repeat what the line detectors already capture.

I'm settling on 8 orientation channels at 22.5° steps, since the 5x5 kernel's tuning is broad enough that neighboring channels will overlap, but that's acceptable. For the other 8 conv2 channels, I'm considering a half-cell offset of the same orientations to sample the grid more finely, though the 4x4 coarseness is still a limit.

I'm weighing a shifted conv2 kernel that samples the orientation channels at half-cell offsets, which would give the 4x4 grid finer coverage, and I'm checking whether a 2-pixel shift lines up with the pooling stride.

I'm splitting the 16 conv2 channels into two sets of 8 orientations, offset by a half-cell in the grid, so the pooled 4x4 centers fall between the original positions. The pooling stride is what makes a one-unit shift in conv2 equal to a two-pixel move in the input. I'm checking whether shifting both rows and columns together is the right way to offset the sampling, or whether only one axis should move.

I'm checking whether a 3x3 support starting at offset 0 or 1 gives centers every two input pixels, which would give the 4x4 grid finer coverage, but the spacing still stops short of the far edge near 21.5, so I'm considering a larger support to reach it.

I'm working through the grid offsets: a 4-wide kernel starting at offset 0 would center the pooled cells at 5.5 plus multiples of 4, which lines up symmetrically with the digit's center near 13.5 if I combine it with the half-offset variant.

I'm weighing whether to keep four orientations on a finer 8x8 grid, or eight orientations on the coarser 4x4 grid. A 4x4 grid with 4-pixel spacing starts to look like HOG with only four cells, so the finer spatial sampling may matter more.

I'm weighing whether the second set of conv2 channels should be the eight orientations shifted by a row offset, which would sample the grid more finely vertically.

I'm deciding the quincunx layout for the second conv2 set, with the two sampling grids offset diagonally so they interleave. Next I want to generate the templates by sampling each stroke with a Gaussian window around every cell center, and accumulate orientation-weighted responses per channel.

I'm now defining each filter's direction in image coordinates, with the angle taken mod π, and weighting the stroke samples by their distance from each cell center. I'm also passing the accumulated responses through a tanh so that long strokes don't add up linearly.

I'm settling the template weights: each orientation's response falls off as max(0, cos 2Δ)², which gives 0.5 at a 22.5° offset. For each digit I'll average the templates from several stroke variants, such as slanted and vertical 1s or open and closed 4s, and I'm leaning toward adding Gaussian blur at about σ = 3 pixels to absorb handwriting jitter.

I'm settling the scale of the logits: the features are in [0,1] and there are a few dozen active ones, so with unit-norm templates the logit gap is roughly an order of 1, and I'm considering a gain around 6 to 10 as a starting point while watching for loss on misclassified examples.

I'm now going through how the digit templates should be drawn, checking that the unit-norm scaling handles a sparse digit like 1 versus denser ones like 7, and planning to tune the bias terms against feedback.

I'm laying out the digit strokes on a normalized grid, mapping each point into the 28x28 image, and using arc helpers to build the curved parts of the shapes.

I'm defining the digit shapes as polylines and arcs in a normalized frame, starting with 0 as a full ellipse and 1 in three slant variants. For 2, I'm building a top arc that drops into a diagonal and a base stroke.

I'm finishing the stroke paths for the digits: the 2's diagonal and base, then the 3 as two stacked arcs, and starting the 4 with an open variant and a closed one.

Still writing the digit stroke paths: the 5's top bar, stem and bowl, then the 6's curved stroke and loop, and I'm starting on the 7's top bar and diagonal.

I'm settling the 7's crossbar as a lower-weight stroke and deciding to center each digit's strokes by their length-weighted centroid, shifting them to the middle of the frame. The 8 gets two stacked loops, with the bottom one slightly wider.

I'm defining the digit shapes as ellipses and tails, with the 9 as a loop plus a slanted tail, and I'm planning to average each digit's no-shear and sheared variants to soften the strokes.

I'm checking the receptive-field centers for the two conv2 sets: the first set lands at 4r+6.5 in input pixels, and the second, offset by one unit, at 4r+8.5.

I'm setting the blur width at about 3 pixels to cover the receptive field, and I'm checking the bias and normalization of the second conv layer's weights.

I'm building the template weights now: each stroke's contribution is accumulated along its length with a Gaussian falloff around the cell centers, then passed through a tanh to keep long strokes from summing too high. I'm planning to normalize each template to unit norm, subtract its mean so it sums to zero, and renormalize, with a gain of about 8.

Still writing the template code: each point's contribution gets weighted by its orientation match and a Gaussian falloff around every cell center.

Now I'm writing the convolution kernels: the first layer gets oriented line filters at eight angles, and the second layer's weights are built as outer products of those responses.

I'm setting the bias terms to zero for now.
