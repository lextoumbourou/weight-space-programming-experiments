The loss is still sitting near chance, around 2.30, so the logits must be small and class 1 is dominating. The features look weak, and I think the design needs to be more robust. Class 1 is being over-predicted, probably because its V weights are positive on columns 1 and 2 across every row, and the zero-sum constraint isn't helping. Without data to check against, I'm leaning toward a template-matching classifier and want features whose activations I can actually reason about. An

I'm weighing a different route: a template-style classifier built from pooled ink density, where each digit is matched against mean images at a coarse grid. A 4x4 grid loses too much detail, so I'm considering using many channels to encode position-specific features instead, though that gets complicated quickly.

I'm checking the class-1 weights, since the positive edge values across rows and the mean-subtracted border cells both seem to push class 1 up for most digits. I'm also considering whether to threshold the features so they're sparser and the differences between classes come from actual presence rather than small background values.

I'm working through the response of a 5x5 zero-mean ridge filter to a vertical line about 2.5 pixels wide. Estimating the center, neighbor, and outer column weights and their sums, I'm computing the normalized values per column to see how a width-3 line responds across columns -1 to 1.

I'm checking the per-row weight sums for a 3-pixel vertical stroke, which come out to about 1.0 for a full response, and I'm guessing wider MNIST strokes land nearer 0.8. Diagonal filters should pick up some of the vertical stroke as cross-talk while horizontal ones stay near zero. Next I'm estimating how many of the 5 columns in a conv2 window respond strongly to a vertical stroke.

I'm estimating the magnitude of the vertical-stroke features after max pooling, around 0.5 where a stroke is present and about 0.1 elsewhere. With weights near 3, each cell contributes a large logit term. Class 1 gets a positive push because its V weights are positive across the center cells, and most ordinary digits have strokes there too.

I'm weighing whether to reduce class 1's vertical-stroke weights and add per-class biases, since it wins on ordinary digits too. Another option is leaning on the ink-density templates, which I can write by hand, and using the extra channels to recover some spatial resolution beyond a coarse 4x4 grid.

I'm working out a way to get finer spatial detail than a 4x4 grid: each conv2 channel would sample the blob map at a different offset, so after max-pooling each channel gives a 4x4 grid of the strongest ink in its own sub-position, and together the channels recover roughly 8x8 resolution.

I'm working out how to get finer spatial detail: each channel samples the ink map at a different offset, so after pooling each gives a 4x4 grid covering 4-pixel cells shifted by its offset.

I'm working out how to get finer spatial detail: each channel samples the ink map at a different offset, so the 4x4 grid cells shift by 2 pixels per channel and together they tile the image at higher resolution.

I'm working out which offsets to use for the 16 channels, since the coverage pattern depends on the step size. Stepping by 2 gives overlapping windows, so I'd be wasting channels on the same positions, which means I need to pick offsets that tile the 12x12 map without redundancy.

I'm checking which pooled indices the offset channels can actually cover, since a 4x4 grid of 2-cell windows only reaches 8 of the 12 positions per axis. The digit sits roughly in indices 2 to 9, so I'm looking at whether offsets near 2 and 3 give the most useful coverage of the center.

I'm settling on which offsets to sample: channels at offsets 2 and 3 in each axis would cover the central pooled indices, since the digit sits roughly in indices 1 to 10, though an 8-wide window only spans 16 pixels and might crop the edges.

I'm sketching a finer-resolution option: four channels sampling the ink map at offsets of 2 or 3, which gives roughly an 8x8 view of the central digit, and I'd hand-draw those templates per digit. The rest of the channels could then handle stroke features.

I'm sketching a finer-grained alternative: sampling the blurred ink map at a couple of offsets so the pooled cells line up with the central digit area, and then wondering whether hand-drawn 8x8 templates for each digit would be worth the effort.

I'm checking how the pooled indices line up: with offsets of 1 and 3, the two channel sets together would cover the digit's range, since the offset-1 cells reach index 8 and the offset-3 cells pick up from index 3 through 10.

I'm checking which pooled positions the offset channels reach: offsets 1 and 3 cover the middle of the grid, but offset 2 would reach the lower rows (up to pooled index 9) more evenly, and I'm weighing whether a few rows at the bottom get cropped.

Choosing which pair of offsets to use: 1 and 2 center at about 5, while 2 and 3 center at about 6, and the digit sits near 5.5, so either one is off by half a cell. I'm weighing whether a third offset is worth the extra channels.

I'm working through how to lay out the 9-channel sampling: each offset pattern produces its own 4x4 grid, so the centers line up at 9 distinct pooled positions with some duplication. I'm now considering a 9x9 grid of ink values at those centers as the basis for the templates, and I need to decide how the fully connected weights should be arranged across the channels.

I'm assigning each conv2 channel's cell a template weight from the 9x9 grid at the matching center index, and dividing by how many (offset, cell) pairs land on the same index so the duplicated positions aren't double-counted.

I'm checking how the duplicated pooled positions should be weighted, since some indices come from two different offset and cell pairs. I'll divide each template value by how many pairs land on that index, and then I'm wondering whether to sharpen the blurred ink values before they're used.

Setting up the channel mapping now: the nine ink channels get assigned by their offsets, each one picking out a single conv1 blur value at its position. Next I'll move on to filling in the 9x9 template grid, with each index tied to a pooled center.

I'm checking the coverage math: a 9-cell grid spans about 16 pixels of the 20-pixel digit, so the edges get clipped a little, but the pair-sampling max leaves some slack. Next I'll draft the 9x9 ASCII templates by hand, with '#' for full ink and a lighter mark for partial.

I'm settling on how to score the classes: the template weights get centered by subtracting the mean across all digits, and each class gets a bias of minus half its squared template norm, which turns the dot product into a matched-filter approximation of Euclidean distance.

I'm settling on the scoring: each class gets a weight of its template scaled by a factor, and a bias that subtracts about 0.3 times its squared norm, so the dot product approximates a matched filter. That should favor the class whose template best overlaps the ink while staying close to a Euclidean distance comparison.

I'm settling on the scoring details now: the off-ink cells get small negative weights, like the hole in a 0, and the bias should count only the positive part of each template. I'll use a scale of about 1.5, since the logit gap only needs to break ties. Next I'll start drafting the 9x9 templates row by row, with a digit 1 as a centered column.

Still drafting the 0 template: the top rows get a soft, rounded outline, and I'm marking the interior hole with negative weights so it counts against the class.

Still drafting the 0 template, with the rows of the rounded outline and a hollow interior marked by negative weights.

Still drafting the 1 template: a narrow vertical column with slight negative weights on either side to suppress the wider shapes.

Writing the 9x9 digit-2 template row by row, with the top arc, a diagonal sweep down the left, and a flat base.

Still drafting the 3 template and the 4, working out which cells get partial ink and which get small negative weights.

Still drafting the 4 template: the open top is left blank, with a diagonal stroke on the left, a crossbar, and a vertical stroke on the right, plus some small negative weights inside the open top.

Still drafting the 5, 6 and 7 templates, working row by row on the 9x9 grid.

Still filling in the 6 template, shaping the loop with its hollow interior marked by negative weights.

Still writing out the 8 template, working through the crossing rows and the lower loop.

Still drafting the 9 template, marking the hole with negative weights in the upper and middle rows.

Still mapping each conv2 channel's weight onto the template grid, using the pooled center index for each output cell.

Next I'm settling the fully connected weights: each channel's template value gets scaled and split across the duplicated pooled positions, and the bias comes from the positive part of the template norm.

Settling the scaling and bias now: I'll keep the scale at 1.0 since the loss is unknown, and set the bias from the positive part of each template so the dot product stays roughly matched to the ink. Next I'll write the code, keeping the first conv1 blur channel and zeroing the unused conv2 channels.
