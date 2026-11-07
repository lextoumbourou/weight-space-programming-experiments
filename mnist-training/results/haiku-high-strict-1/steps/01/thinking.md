I'm working out how to handcraft a CNN for MNIST without seeing any data or training, and I can't run code, so I have to write the weights directly in a build_weights() function that returns a dict of numpy arrays. Synthetic inputs are off the table, but drawing filters from formulas or strokes is fine. I'm starting to think about a reasonable hand-designed architecture, with the convolutional layers as the first priority.

Next I'm sketching the first conv layer: eight 5x5 filters meant to pick out edges and blobs, with a second layer combining them into sixteen features. Since I can't check against data, I'm leaning on what MNIST digit strokes look like to shape the filters. I'm trying a vertical stroke detector first, a positive center column with negative flanks and a negative bias so the blank background gets zeroed out by the ReLU.

Still writing the conv1 filter definitions...

Next I'm weighing how the second conv layer should work: center-weighted averaging of single channels, plus a few oriented patterns at a larger scale. The harder part is the fully connected layer over the 4x4x16 grid, since I can't fit templates to data and have to decide what the 256 pooled features should encode by hand.

I'm thinking about the FC layer as coarse templates: pool the conv features onto a 4x4 grid, where each cell covers roughly a 7x7 pixel patch, and write per-digit ink-density patterns over it. I expect that to land somewhere around 40-50%, but adding orientation channels could push it toward 60-70%, which is acceptable for a first pass.

Working out the spatial layout now: after the two 5x5 convs and 2x2 pools the grid goes 28→24→12→8→4, so each of the 4x4 final cells should cover roughly a 7-pixel patch of the original digit.

I'm settling the layout for conv1 so one channel acts as a blob-style ink map after pooling while the rest pick up stroke orientations, and I'm planning the conv2 channels as pooled averaging detectors over those maps.

I'm sketching the fc layer as a coarse 4x4 occupancy template per digit, with each cell marked as ink expected or not, and I'm weighing whether orientation channels should add to the ink map.

I'm sketching each digit as a coarse 4x4 occupancy pattern, marking where ink should appear: a ring for 0, a centered vertical bar for 1, and I'm starting on 2 with a top arc, a diagonal down to the left, and a bottom stroke.

I'm sketching the digit 2 as a coarse 4x4 occupancy grid: a top arc, a diagonal sweeping down to the left, and a full bottom stroke.

Sketching the digit 3 next as a coarse grid, with a top arc, a middle stroke pulling in, and a lower arc, and I'm tracing the 4 as its diagonal and crossbar.

Still writing the 4x4 occupancy grids for the digits...

I'm writing the 4x4 occupancy grids for the remaining digits, with rows for the top arc, the sides, the middle, and the base. For each one I'm checking which cells should carry ink, and I'm about to start working out how the pooled features would be matched against those patterns.

I'm weighing whether to give the FC layer two extra channels per cell, horizontal and vertical edge density alongside ink presence, since the single ink map alone would leave 7, 5, and 2 hard to tell apart. Hand-computing those weights reliably looks tricky, so I'm deciding how far to push the design.

I'm making the conv2 channels near pass-throughs of the first pooled maps, with a center-weighted kernel for light spatial blurring, so each one stays a local feature. The fully connected weights then have to be set per class, channel, and cell.

I'm settling on a 5x5 box-blur kernel for the conv2 pass-through, with the weights scaled up so the ReLU bias still works, since the overall scale only shifts what the fc weights need to be.

I'm now deciding how the conv2 channels 8 through 15 should work, leaning toward larger-scale blob detectors built from the conv1 ink and orientation maps rather than simple pass-throughs. I'm also reconsidering whether a simpler box-blur over combined conv1 channels would be enough for a first pass.

Still writing the conv1 filter weights...

Still working on the conv1 filter weights, trying a vertical stroke detector with a center column that's positive and flanking columns that are negative.

Still writing the conv1 vertical-stroke pattern...

Still working out the conv1 vertical-stroke weights, checking the sum over the center columns and whether the bias keeps blank background at zero.

Still writing the diagonal conv1 filter, working out which cells along the anti-diagonal should be positive.

Still working out the diagonal filter, with the positive band along the anti-diagonal and some negative weight for the neighboring bands.

Still working out the diagonal filters, giving the "/" and "\" patterns a positive band along their stroke and mild negative weight on the neighboring bands, with a small negative bias.

Still working out the conv1 filters, with the second layer's conv2 weights to follow.

Still settling the conv2 layer: I'm leaning toward a simple 3x3 center-weighted blur over each conv1 channel, so the pooled features stay local while the receptive field grows.

Still settling the conv2 layer: the 16 outputs are blurred copies of the conv1 channels, with the second group mixing in the ink-presence map, and I'm working out the bias for that mix.

Still working out the conv2 outputs: the first group of channels is blurred copies of the conv1 maps, and I'm now choosing the remaining eight, with a center blob map, a broader ink-presence map, and stronger-weighted blurs of the orientation channels.

I'm defining the second-layer features per cell, with the ink presence map and the conv2 mapping still to be pinned down so the fully connected weights can refer to them.

Still working out the conv2 mapping: each of the eight outputs is a 3x3 blur of one conv1 channel, and I'm settling the wider 5x5 copies for the second group of eight.

Still working out the FC weights, scoring each digit template against the ink-presence channel with +1 for expected strokes and a negative value for expected blank cells.

I'm settling on the feature set for the fully connected layer: ink presence as the main signal, with the center-blob channel to pick up holes in digits like 0, 8, 6, and 9. I'm dropping the detailed orientation templates for now, since mapping every stroke direction onto each digit's cells would take too long to get right by hand.

I'm settling on the ink-presence template approach for the fully connected layer, with the 4x4 grid and carefully written per-digit patterns. I'm skipping the center-blob weighting for now and leaving the class biases at zero, since I can't tune them without feedback.

I'm sizing the feature values: the blurred ink-presence map should land around 0 on background and roughly 0.5 to 0.8 on strokes, so each cell sits in [0, 1]. With ±1 template weights over 16 cells, a full match could score up to about 8.

Working out the 4x4 ink templates for each digit, since the cells at the edges will only catch partial strokes.

I'm sketching out the 4x4 ink templates for each digit, starting with 0: a ring of positive weights around the edges and negative weights in the center, since the hole sits there.

Still writing the 4x4 ink templates, working through the digit 1's rows with its vertical stroke in the third column.

Still writing the 4x4 ink templates, working through the digit 2's first row with its top bar.

Still working out the 4x4 templates, now the digit 2's middle rows with the diagonal running from the upper right down to the lower left.

I'm checking the row-by-row template for the digit 2, with the top arc's right side set to fall in the third and fourth columns of row one.

Still writing the 4x4 ink templates, now the digit 3's rows with its right-side strokes at the top and bottom.

Still working out the 4x4 template for digit 4, placing the positive weights on the diagonal and the right-hand stroke.

Still working out the 4x4 templates for digit 5, with a positive top row and the upper-left stroke sitting in the first column.

Still writing the 4x4 ink templates, now the digit 6's rows with the loop at the bottom.

Still writing the 4x4 template for digit 6, setting the bottom loop's right edge and the lower-left cells.

Still writing the 4x4 template for digit 7, with the top bar's positive weights and the diagonal stroke running down into the center columns.

Still writing the 4x4 templates, now for the digit 8: the top loop gets ink on its outer edges with an empty center, then the crossing row.

Still writing the 4x4 ink templates, now the digit 8's top and bottom loops with their sides and crossing row.

Still writing the 4x4 ink templates for digit 8, setting the crossing row to a positive center so it stands apart from the 0 template.

Still writing the 4x4 templates, now the digit 9: the top loop gets ink on its outer edges with an empty center, and the stem runs down the right side.

Still writing the 4x4 templates, now the digit 9's stem and the weight rows for the fully connected layer.

Next I'm weighing whether the center-fill channel should feed the fully connected layer for telling 1, 4, and 7 apart, but I'll leave it out for now. I'm keeping the first pass simple: only the ink channel carries weight, and the wide-blur and other conv2 channels stay at zero.

Still working out the 4x4 weights for the horizontal stroke channel, and I'm weighing whether to give the digits with top and bottom bars a small positive weight there.

Still writing the weights, with the horizontal-stroke bonus left out for now and the conv2 blur taking shape as a 3x3 averaging kernel on each matching channel.

Still writing the conv2 layer, mapping each of the first eight outputs to a 3x3 center blur of its matching input channel and the second group to a 5x5 box blur.

Still writing the conv1 filters, starting with the vertical-stroke filter's weight matrix.

Still checking the conv1 vertical filter: a stroke down the middle column should sum to roughly 4 over a full 5x5 patch, so the bias of -1 leaves a clear positive response.

Still writing the conv1 filters, now the diagonal "/" filter with its weights set along the anti-diagonal.

Still working out the diagonal filter's weights, checking whether a 3-pixel-wide "/" stroke overshoots the vertical filter's response once the bias is subtracted.

Still checking the anti-diagonal filter's response: the stroke cells should land near 4.5 against the bias of -1, so I'll leave the outer corner flanks at zero.

Still writing the conv1 filters, now the vertical-stroke pattern with its flank columns set to zero.

Still writing the conv1 filters, now the diagonal patterns, with the anti-diagonal weights scaled by distance from the stroke center and a center blob filter queued up next.

Working out the blob channel's weights now: a positive center on the 3x3 and a small negative ring, and checking that a vertical stroke down the middle barely activates it.

Still writing the conv1 filters, now the edge channel, with bright-on-the-right weights set against the dark left columns.

Still working out the edge channels: the left-edge detector gets positive weights on the right half and negative on the left, with a bias of -0.5, and I'm starting on the bottom-edge channel next.

Still settling the edge channels, I'm giving the bottom-edge detector positive weights on the top rows and negative ones on the bottom, and leaving channels 6 and 7 as they are for now.

Still working out the conv2 layer: each channel gets a 3x3 blur of its matching conv1 output, and I'm checking that the pooled ink feature stays near 1 on strokes and 0 on background.

Still checking the digit 0 template: the ring cells get positive weights, the center cells are pushed negative, and I'm testing how a lone vertical stroke scores against it.

Still checking the digit 1 and digit 0 templates against each other: the 1's center columns score about 4 on its own template and drop to roughly -2 on the 0 template, so they separate cleanly.

Now I'm weighing whether the templates can separate digits when a 1 and a 0 both fill the same cells, since the score alone might not tell them apart.

Now I'm weighing whether to add a cheap horizontal-stroke feature to the fully connected layer for the top-row cells of digits 2, 5, and 7, but I'll skip it for the first pass.

Still settling the horizontal-stroke weights for the fully connected layer, giving the top row a positive value for digits 2, 3, 5, and 7, and the vertical channel a boost on the center columns for digit 1.

Still rescaling the line-pattern weights by a quarter, since the raw conv1 responses come out near 4 and would swamp the ink channel.

Still scaling the vertical-stroke weights: the center column gets 0.125, the neighboring columns 0.0625, and the outer columns -0.0625, so the full stroke response stays near 1.

Still checking the weight scales: with the 0.0625, 0.125 pattern the stroke response comes to about 1.25, so a bias of -0.25 leaves it near 1. The blob channel gives roughly 0.38 on full ink, and the stroke-presence channel is set to 0.04 per cell for a full value of 1.0.

Still scaling the channels down: the edge detectors stay small and unused, and the conv2 layer gets a 3x3 blur on each of the first eight channels, with the wide 5x5 copies left out of the fully connected layer for now.

Still setting the fully connected weights: I'm putting the horizontal-bar bonus on channel 1 for each digit, with rows 0 and 3 for 2 and 3, row 2 for 4, and rows 0, 2, 3 for 5.

Still writing the conv1 weights, now the remaining line detectors and the bias terms.

Still writing the conv1 filters, now the '/' diagonal detector with its weights tied to r+c.

Still writing the conv1 filters, now the '/' diagonal detector with its weights tied to r+c.

Still writing the conv1 filters, now the edge channels with their weights and biases.

Still writing the conv2 layer and the fully connected template weights.

Still writing the weight templates for the fully connected layer, now the digit-by-digit ink patterns for 0 and 1.

Still writing the digit templates, now the ink patterns for 2 and the start of 3.

Still writing the digit 6 template, filling in the ink pattern row by row.

Still writing the digit 8 template, filling in the ink pattern for the remaining cells.

Still writing the digit templates, now the horizontal-bar bonus for digits 2, 3, 4, 5, and 7, with the top and bottom rows lifted for most of them.

Still writing the fully connected weights: the ink template for each digit goes into the 5*16 block, and the horizontal bonus stays small at 0.3 per cell.

Still writing the fully connected weights, now packing the digit ink templates and horizontal bonuses into their blocks and checking the flatten order.

Now I'm closing out the answer with a few tidy comments and a clean write-up of the weights.
