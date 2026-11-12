I'm settling on a simple first design, since a fully general conv2 is hard to pin down. I'm considering oriented edge detectors in the first layer, or, as an alternative, having the network act as template matching on a downsampled image. I'll start with the simplest robust option: a first-channel blur that passes the ink through, followed by pooling.

I'm weighing whether conv2 should just pass the features through, but that would leave only a 4x4 ink map, which is too coarse. So I'm considering letting conv2 produce 16 features on an 8x8 grid and pooling those down to 4x4. Some of the first-layer channels could be oriented stroke detectors, and conv2 could keep their presence in a max-pooled 4x4 grid.

I'm working out the receptive field math: each conv2 position maps back to a patch of input, and pooling merges neighboring cells, so a 5x5 averaging kernel would cover rows 2i to 2i+13 and reach the full digit area better than a plain pass-through.

I'm settling on eight first-layer channels: an ink blur, horizontal, vertical, and two diagonal stroke detectors, plus a few more, each passed through ReLU. Conv2 would then take those eight and add eight others. For the templates, I'm considering drawing each digit as hand-described strokes in 28x28 coordinates and rendering them as prototypes, since that avoids generating examples to fit weights.

I'm now going to draw the templates directly in feature space: for each digit, I'll place oriented stroke segments onto the orientation maps at the grid cells they fall in, rather than running the network on any input. The open question is how the feature grid lines up with the image geometry, so I'll need to work out a finer mapping before settling on pooling.

I'm thinking about having conv2 read a single shifted tap from pool1, so each channel samples a different offset within the grid. Pooling over a 2x2 block of those conv2 outputs would then let the 16 channels cover different sub-positions and orientations. I'm checking whether the shifts stay within the 0 to 4 range I'd need to keep the read locations inside the feature map.

I'm checking the pool1 geometry against the digit's position: its rows span roughly cells 1 to 10, and a dy shift of 0 or 4 moves the 4x4 window to cover the top or bottom of that range.

I'm going with a simpler, well-proven route: a global template matcher on rich features, expecting roughly 70 to 85 percent accuracy. For the first version I'm planning eight first-layer channels, four oriented line detectors at 0, 45, 90 and 135 degrees, plus an ink channel and a few others I'm still deciding on.

I'm sketching conv2 as a 3x3 box average over pool1 with a fixed offset per channel, so each output cell covers a small patch of the first-layer maps. Each channel would read one of the four orientation features or the ink feature, and I'm checking how that box lines up with the digit area.

I'm mapping the conv2 cell centers back to the input: the four pooled cells sit at roughly input columns 7.5, 11.5, 15.5 and 19.5, and their receptive fields overlap. The digit's center of mass is around 14, so the grid looks like it covers the middle of the image well.

I'm weighing whether conv1 should spend its eight channels on eight orientations at 22.5-degree steps, or keep four orientations plus an ink blur and a few extra channels that are harder to template.

I'm figuring out how to make the 16 conv2 channels cover the grid: five features at three offsets gives 15, so I'd add one more. Each channel's weights would come from the template's feature values at that channel's receptive-field center, smoothed with a Gaussian.

I'm going to set the offsets aside for a moment: shifting a conv2 read by one pool1 cell moves its receptive field by two input pixels, which is half the pooled grid spacing. I'll try four orientations at four offsets, (0,0), (0,1), (1,0), (1,1), which fills all 16 channels and gives a finer effective grid.

I'm working out how the pooled grid's receptive fields combine, since the offset channels make the effective spacing finer. Then I'm moving on to the linear classifier and planning to subtract the mean template across classes so the ink-heavy digits aren't favored.

I'm settling the first-layer kernels now: each orientation detector gets a line-shaped center with flanking negative lobes, sized for strokes a few pixels wide. I still need the exact formula for the kernel profile across the stroke.

I'm checking the zero-mean kernel for a perpendicular line through the center, since its side lobes could cancel the positive center and make the response ambiguous.

I'm working out the first-layer kernel magnitudes now: a 5x5 zero-mean profile where the center row gives a response of about 3.6 on a width-3 horizontal stroke, so I'll normalize by that and then pick a bias to suppress noise.

I'm settling the first-layer normalization: rather than checking the kernel against a synthetic stroke, I'll scale each kernel by the sum of its positive weights so the response stays roughly uniform across orientations.

I'm setting conv1's extra channels to zero and keeping four orientations. Pool1 becomes a 12x12 grid of orientation energies. For conv2 I'm using a 3x3 box average per channel, with the row offset chosen so the window stays inside the pooled map and no bias.

I'm working out where each conv2 cell lands in the input: a pool1 cell's center sits at 2p+2.5, so conv2's centers fall at 2i+6.5+2oy, and averaging the two conv2 positions per pool2 cell puts pool2 cell a at about 4a+7.5+2oy.

I'm checking which offset pair for the conv2 box works best, since starting the window at rows 0 or 2 shifts the pooled cell centers by four input pixels in each direction.

I'm settling the conv2 offsets now: two starting rows, 0 and 1, would cover roughly input columns 5.5 to 19.5, while 1 and 2 would reach 7.5 to 21.5, and either spacing should work since each cell's receptive field is wide. I'm considering whether a 4x4 box would widen coverage further, but I'm leaning toward a mix of offsets.

I'm now trying out offset pairs for the conv2 box, weighing whether a mix of starting rows and columns covers the digit area without repeating the same window positions.

I'm choosing the conv2 offsets {1,2} so the grid shifts toward the bottom, which still covers the digit center near row 14. I'm also thinking about whether a wider box or larger receptive fields would help the coverage.

I'm turning to the feature templates: for each digit I'll sample points along its strokes, take each point's direction, and score how strongly each orientation detector responds there, then pool those scores onto the conv2 grid.

I'm turning the template idea into a hand-built model of the features rather than running the network on the digit images. Each cell's value will be a Gaussian-weighted sum of stroke density near its center, and the classifier weights will be the normalized templates minus their mean, scaled so the logits stay in a reasonable range.

I'm settling the feature templates by hand: strokes sampled per digit, each point's direction scored against the four orientation detectors, then smoothed onto the conv2 grid. I'm starting to lay out the 28x28 stroke geometry for each digit next.

Writing out the stroke coordinates for each digit now, starting with the 0 ellipse and the 1 slant.

I'm writing out the stroke coordinates for the 5, 6, 7, and the start of the 8 loops, placing each digit's polyline points inside the 28x28 grid.

I'm now writing down the stroke coordinates for the 9 as well: a loop at the top with its stem running down the right side. Next I need to fix the direction convention for the orientation detectors so the stroke angles match the kernel angles, and then I'll sample points along the strokes.

I'm defining the template for each channel and cell as a distance-weighted sum over stroke points, scaled by their orientation response, and flattening them into the 256-length classifier input.

I'm noting that the template weights need a per-class correction, since compact templates like the 1 have smaller total mass than heavy digits and could pick up a bias from the ink amount.

Still writing the weight-building code...

Setting the first-layer bias to -0.1 to suppress weak responses, then turning to the conv2 weights.

Still writing the stroke-drawing code for the template model...

Still writing the template code: I'm sampling the stroke points and computing each template cell as an orientation-weighted, distance-decayed sum over those points, then vectorizing it.
