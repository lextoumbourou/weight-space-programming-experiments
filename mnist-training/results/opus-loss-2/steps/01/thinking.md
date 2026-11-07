I'm planning to hand-design the weights, starting with conv1 as oriented edge and stroke detectors. My idea for a simpler route is to make one conv1 channel a near-identity blur so the ink passes through, which gives a 12x12 downsampled image for conv2 to work from.

I'm working out the conv2 stage: 16 channels over the 12x12 maps, pooled down to a 4x4 grid. Each final cell then covers roughly a 7x7 region of the original image, which feels coarse for digit templates. I'm considering using conv2 to detect stroke features at positions instead, so the fc layer can match digits by where the strokes sit.

I'm checking whether a center-tap pass-through in conv2 keeps the stroke positions usable: each final cell would take the max over a band of pooled conv1 rows, which maps back to a roughly 8-pixel window of the original image. The cell centers land near rows 7.5, 11.5, 15.5 and 19.5, and the digit spans about rows 4 to 23, so coverage looks workable even if it is coarse.

I'm checking the stride math: the 4x4 cells sample input rows 6-9 through 18-21, which leaves the borders out. I'm considering a wider sum over a 3x3 or 5x5 pool1 neighborhood so the cells overlap and reach the edges, and then I'll need to hand-write which features sit in which cell for each digit.

I'm weighing whether to make conv2 channels 0-7 sum conv1 channels over a 3x3 center, so the cells overlap and reach the image borders. Channels 8-15 are still undecided, and I'm leaning toward leaving them as zeroed-out placeholders for now.

I'm weighing how to turn the digit templates into fc weights, since writing a rasterized drawing and then running conv features over it would mean running the network on an input, which the constraints forbid. I'll need to specify each digit's 4x4 presence pattern by hand instead.

I'm settling on the layout for conv1: five-by-five kernels with separate channels for horizontal, vertical, and the two diagonal stroke directions. I'll then deposit each digit's strokes into the matching orientation grid by hand.

I'm settling the conv1 layout with a few spare channels, an ink-pass channel, and a stroke width of about 2-3 pixels in mind. For the horizontal detector, I'm weighting a five-column profile that is positive in the middle rows and negative at the edges, so it sums to zero and responds strongly to a stroke of that width.

Working out the diagonal detectors next: a "/" stroke runs along r + c = const, so I'm measuring each pixel's distance from that line and giving it a Gaussian-style profile, then subtracting the mean so the weights sum to zero. The same idea should extend to the other orientations by changing which perpendicular distance I use.

I'm normalizing the diagonal filters by dividing by the sum of their positive weights, so a clean stroke comes out near 1 without evaluating the kernel on an input. I'm also restricting each filter to a circular window so the orientation response stays isotropic. Channel 4 will be a uniform 3x3 average over the centre for the ink signal.

Next I'm setting the conv2 weights: the first five channels will sum a 3x3 center of each pool1 channel, and the rest stay zero for now. Checking the receptive field, each pooled cell spans input centers roughly 4i+2 to 4i+13, so the overlap should help coverage.

I'm moving on to the fc weights, planning to sketch each digit as strokes in a normalized 20x20 box and map those onto the 4x4 cell grid. The cell centers sit at 7.5 + 4i, which gives a rough coordinate frame for placing each digit's strokes.

I'm turning to the fc weights now: for each digit, I'll deposit its strokes into the orientation and cell grids, weighting by how well each stroke's direction matches a channel and how close it sits to each cell center. Then I'll subtract the mean template across digits so the shared features don't dominate, and scale the result so the logits stay in a workable range.

I'm weighing the fc weights as normalized digit templates minus their mean across digits, so each class keeps the features it expects and loses the shared ones. The raw feature magnitudes look modest, so I'm thinking a scale around 10 with adjustment later, but there's a concern that templates correlated with total ink, like the heavier digits, could skew the logits.

Now I'm drafting the digit stroke layouts in pixel coordinates, placing each digit's strokes within the 28x28 frame.

I'm sketching the digit 2 as an arc at the top, with a diagonal and a base line below it, using a parametric circle around (14,10). For the 3, I'm laying out an upper bowl centered near (13.5,9) that curves from the upper left over the top and down.

I'm sketching the digit 4 as a diagonal from upper right to lower left, a horizontal crossbar, and a vertical on the right, with an alternate open-top version using a vertical on the left. For the 5, I'm laying out a top horizontal bar, a short vertical down the left, and a lower bowl centered near (13.5,17).

I'm sketching out the remaining digit layouts: a 6 as a diagonal stroke with a full loop at the bottom, a 7 as a top bar with a long diagonal, an 8 as two stacked circles, and a 9 as an upper loop with a tail. Once those are placed, I'll think about how to split the orientation channels.

Now I'm mapping each orientation to a preferred angle, using the mod-π direction of each segment, and weighting a channel by how closely the stroke's angle matches it. I'm also starting to write the conv1 kernel for each orientation, defining its perpendicular distance from the line through the kernel center.

I'm defining the conv1 orientation kernels by perpendicular distance from each line through the kernel center, with the horizontal case reducing to the absolute row offset. I'm also checking that the diagonal directions match the stroke orientations I want. I'll leave the spare channels zero and set a mild negative bias after normalization so the detectors don't fire on edges of the wrong orientation.

I'm checking the kernel mask's size and which positions count as positive, since a stroke of width 3 should mostly fall in the positive region. The horizontal case depends only on the row offset, so I'm working through the row-by-row values first.

I'm checking the kernel values row by row: the center row and the two adjacent rows come out positive, and the outer rows go negative. A width-3 stroke would fully land on the positive band, so the response should come out near 1. I'm considering a narrower sigma around 0.8 to tighten that band.

I'm checking the conv2 weights next, trying a 1/3 scale instead of 1/9 so the averaged pool1 values come out at a useful magnitude.

I'm thinking about whether to spread the conv2 channels across shifted subregions, so that each final cell draws on slightly different offsets and the effective grid gets finer, even though the overlap would blur the alignment.

I'm working out the conv2 kernel offsets, testing whether splitting each orientation channel into shifted 3x3 windows gives the final grid a finer effective resolution. Checking the coordinates, a row offset of o moves the input center range by 2o, so the shifts line up with the 4-pixel cell stride.

I'm checking whether splitting conv2 into offset windows would help, but the shifted centers mostly repeat each other and only add the edge positions. I'll keep the simpler o=1 3x3 layout and put the extra effort into the ink channels instead.

I'm settling on a layout where conv1 carries a few orientation detectors, and I'm weighing whether finer angles would be worth giving up the ink channel.

I'm settling on the conv2 channels, keeping the first five as 3x3 center sums of the conv1 features and leaving the rest zero, which gives 80 features total. Next I'm building the fc templates by sampling points along each digit's strokes and spreading their orientation contributions onto the 4x4 cell centers with a Gaussian spatial falloff.

Now I'm turning the orientation-selective responses into a saturating feature, so that each cell's value rises toward one as more of the stroke passes through it.

I'm settling the fc weights as the template minus its mean, with no bias term, since the scale of the features doesn't match the templates well enough for a distance-based bias to work.

Writing the conv1 weight builder now, filling in each orientation's kernel from the distance to its line.

Still writing the weight builder...

Still writing the weight builder...

Still writing the weight builder...

Still writing the weight builder...

Still writing the weight builder...

Still writing the weight builder...

Still writing the weight builder...

Still writing the weight builder...

Still writing the weight builder...
