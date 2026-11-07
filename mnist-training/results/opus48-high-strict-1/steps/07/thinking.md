Accuracy is at 38.9% with loss still falling, though the template method seems to be stalling in that 38-39% range. Digit 7 has improved a bit. The worst remaining confusions are the 4 and 9 pair, which swap in both directions, along with 8→2, 1→2, several errors out of 7, and 5→3. These look like deeper shape mix-ups that simple ink-density templates can't resolve.

I'm weighing whether to add a hole-detecting feature, since the 4/9 and 8/2 pairs look similar in silhouette and differ mainly in loops and orientation. With about nine steps left, I'm considering a controlled upgrade and will revert if it regresses.

I'm sketching a hole-detector filter: a 5x5 kernel with a positive ring and a negative center, so it responds where a digit encloses empty space. The aim is to tell apart the loops in 8, 0, 9, and 6 from the open shapes of 1 and 7. I still need to balance the weights so that solid ink produces almost no response.

I'm working out the hole-detector weights: a ring of positive weights around a negative center, normalized so a fully inked region cancels to zero and only empty pockets surrounded by ink respond. Then I'm planning to feed that hole map into the templates, expecting 8 to show two holes, 0 one large central hole, and 9 one hole in the upper region.

I'm working out a hole-detector channel: a 5x5 filter that is positive on the outer ring and negative in the center, so it responds where a digit encloses empty space. I'm splitting the second conv layer's channels between ink offsets and hole-map offsets, so the templates can use both.

I'm splitting the offset channels: most stay as ink samples, and a few get reassigned to read the hole map at coarse positions, so the templates can use both signals.

I'm allocating the conv2 channels now: the first block will sample ink density at a grid of offsets, and I'm figuring out how many channels can be spared for the hole map.

I'm working out how to split the conv2 channels: most stay as ink-density offsets sampled across the grid, and the last few read a hole-detection map at coarse positions so the templates can tell apart upper and lower loops.

I'm settling on the hole-detection idea: one hole channel pooled to a 4x4 grid is enough to show where the holes sit, upper versus lower, so I don't need a separate channel for each position. I'm weighing whether to spend a few more of the second-layer channels on hole offsets, with 13 for ink and 3 for holes as one option.

Now I'm setting the hole channels to use one shared 3x3 average over the hole map, since the 4x4 pooled output already shows where the holes sit.

I'm setting up the hole detector's filter weights: a 5x5 kernel where the border ring gets small positive weights and the inner 3x3 gets negative ones, so the output is high only where a digit encloses empty space. Then I'll feed that hole channel into the second layer as a few copies, with the 4x4 pooled map showing where the holes sit.

I'm checking whether the hole detector actually fires on MNIST loops: a 5x5 window only lands on a hole if the hole is about the right size, and if the hole is larger the border falls inside it and the response drops to zero. So the detector depends on hole size, and it may only work for some digits.

I'm sketching a hole-based feature as an additive signal, weighted modestly so it won't hurt much if it fails, with the ink template still doing most of the work. The fully-connected layer would combine ink-template and hole-template matches per digit, with each digit expecting holes in particular spots: the 0 with a central hole, the 8 with holes above and below, the 9 with one upper, and the 6 with one lower.

Still working out the 4x4 hole templates, sketching the expected hole layouts for the digits that have loops.

Now I'm settling the hole templates as 4x4 grids, with the 0, 8, 9, 6 and 4 layouts marked and everything else zero. Next I'm centering them across digits so that shapes without holes get penalized whenever the hole feature fires.

Now I'm turning to the hole channels: each of the four gets the same hole-template weights, scaled down by four so the total stays balanced. The ink channels keep their own template, normalized separately because they now cover only the first twelve channels, and the hole channels get a centered template so that shapes without holes are pushed down whenever a hole fires.

Setting the ink scale at about 6, I'm now looking at how strongly the hole signal should count against the ink template: around 3, so it can tip the 4/9 and 2/8 calls without overriding everything else.

Keeping the 16 ink channels untouched means no spare conv2 channel is left for the hole signal, so I'm weighing whether to drop an ink offset or find another way to pass the hole map through.

I'm repurposing four of the conv2 channels to carry the hole map, which leaves twelve ink offsets. Dropping the bottom row of ink offsets costs a little coverage at the lowest rows, but it should be a minor loss.

I'm making the hole detector's inner 3x3 empty with a surrounding ink border, which should fire on holes about 5px across. The outer ring would then cover holes of that size, so I'm checking whether MNIST's larger and smaller loops are covered too.

I'm setting up the first conv layer: a plain 3x3 averaging channel, and a hole detector whose outer border is positive so it fires where ink surrounds an empty center.

I'm checking whether the hole detector misfires on the edges of thin strokes: if a stroke crosses the border ring but leaves the inner 3x3 empty, the output could come out positive even though there's no hole.

I'm worried the hole detector will fire on stroke edges, not only on real holes, since any ink in the border with an empty center looks like an enclosure. Relying on the template centering and pooling to absorb that noise feels shaky. So I'm considering demanding ink on opposite sides of the center before the detector counts a hole, which would cut the false positives at the cost of some sensitivity.

Now I'm weighing the threshold: a bias of -0.2 means the detector only fires when the border ink clearly outweighs the empty center, which should cut down on weak false positives. Stroke edges along the border could still trigger it, but the strong, consistent response from real enclosed holes should still stand out. I'll set the hole scale modestly at 1.5 so that if it's noisy, the damage stays limited, and then check whether it actually helps before raising it.

I'm assembling the fully-connected inputs now: the twelve remaining ink channels keep their offsets, and the four hole channels all read the same centered 3x3 average over the hole map, pooled down to a 4x4 grid, so the copies are redundant for now.

I'm giving the four hole channels slightly different sampling offsets, at rows and columns 1 and 3, so their 3x3 windows overlap different parts of the hole map. Pooling to 4x4 afterward should keep the localization fine enough for the template.

Now I'm defining the hole template directly on the 4x4 output grid, shared across all four hole channels so the small offset differences get ignored, with each digit's expected hole cells set and the template centered against the average across digits.

Now I'm writing out the 4x4 hole templates for the digits with loops: the 8 gets holes in both halves, the 9 only in the upper half, and the 6 only in the lower half.

Still writing the hole-template weights...

Still writing the ink and hole weights...

Still writing the hole-channel weights and the ink normalization...

Still writing the hole-channel biases and the threshold on the detector.

Still writing the hole-channel weights and the threshold, with the scale set to 2 and the bias at -0.1.
