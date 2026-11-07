I'm working out how to hand-design the weights for a CNN on MNIST, which is the first of fifteen steps, and I want a strategy that reaches reasonable accuracy. For the first conv layer I'm weighing 8 filters of 5x5, either oriented edge detectors or stroke detectors, followed by ReLU and 2x2 max pooling to get an 8x12x12 output.

I'm sketching out the second conv layer and the fully connected head, which turns the 4x4 pooled output into 10 classes. One option is to let conv2 pass the orientation maps through as coarse spatial summaries and hand-draw 4x4 digit templates in the fc layer. The simpler alternative is a blurred ink channel, which would give a very coarse 4x4 image and probably only 30-50% accuracy, so the orientation features are worth the extra effort.

I'm checking how the 4x4 grid lines up with the input if conv2 only uses its center weight. Each cell would then cover a 12-row window that sits a little off-center, so the digit's edges might fall outside the grid.

I'm checking which offset for the conv2 center weight would best center the 4x4 grid over the digit, and I'm testing shifted positions like k=3 to see how the receptive windows line up with the roughly 4-24 pixel span.

I'm checking the pooled coverage for an offset of k=2: the 4x4 grid would span input rows 4 to 23, centered near 13.5, which lines up well with where the digit sits. I'm also considering a wider conv2 kernel to pool more broadly, but the centered offset already fits.

I'm weighing a smoother alternative for the second conv layer, a small blur over the input, which would give more even spatial features but less resolution. I'm also considering using the 16 conv2 channels to combine orientation features into things like stroke endings and curves, though that seems harder to hand-design. For now I'll keep it simple: 8 orientation or stroke channels from conv1, passed through conv2, with the remaining channels either duplicated at different offsets or used for combinations. The open question is how to write the fc templates for each orientation channel across the 4x4 grid.

I'm weighing simpler features I can reason about reliably: ink presence and horizontal, vertical, and diagonal strokes. I'm also mapping the 4x4 grid onto the input, with each cell covering a 4-row window of the 20x20 digit box, and I'm noting that narrow digits like "1" would only fill the middle columns.

I'm settling on a mixed approach for the fc layer: positive weights for the features each digit should have, negative for the ones it shouldn't, and then refining using confusion-matrix feedback over the remaining steps. I'm also thinking about the scale of inputs, which lie in [0,1] with strokes about 2–3 pixels wide, so conv1 orientation filters need a central positive column flanked by negatives to respond to a stroke.

I'm settling on the conv1 vertical filter: a positive center column flanked by negative side columns, so a stroke about two to three pixels wide scores high while a horizontal stroke or a filled blob nets out near zero. Max pooling over each 2x2 block will then keep the strongest response in that neighborhood. I still need to pin down how large a vertical stroke's response gets.

Next I'm turning to the fc templates, sketching out what each digit's 4x4 orientation pattern should look like across the grid.

I'm working out the 4x4 grid layout over the 20x20 digit box, with each cell covering about eight input columns. Since MNIST digits keep their aspect ratio and are centered by mass, the height always spans roughly rows 4 to 23, while width varies, so wide digits fill the grid and narrow ones like "1" only reach the middle columns.

I'm sketching the 4x4 orientation templates for each digit, starting with 0: vertical strokes at the left and right edges through the middle rows, horizontal strokes across the top and bottom in the center columns, and an empty center. For 1, the vertical stroke sits across the two central columns, which both grid cells pick up, with nothing at the outer columns. I'm now starting on 2, with a top arc in the upper center cells and a diagonal down to the right.

I'm sketching the orientation templates for digits 3, 4, and 5 across the 4x4 grid: horizontal strokes along the top and middle for 3, a right-side vertical with a left diagonal and a bottom bar for 4, and a top bar with a left vertical and bottom bar for 5.

I'm laying out the 4x4 orientation templates for the digits 6 through 9: a top-right curve and left vertical for 6, a top bar with a right-to-left diagonal for 7, stacked loops with side verticals for 8, and a top loop with a right-side vertical for 9.

I'm weighing whether to keep conv2 as a plain pass-through at the center offset or to use its extra channels for larger-scale combinations, but that's too involved for the first step. I'm considering shifting the extra channels to a different offset to get a second grid alignment.

I'm weighing whether conv2 should do something more than pass features through, such as a smoothed copy at a shifted offset for tolerance, or a channel that signals empty regions. A hole-detecting channel, a bias minus the ink sum, could capture things like the center of a zero, which negative fc weights on ink only approximate, since max pooling keeps the strongest ink response in each neighborhood.

I'm settling on the first conv1 filter as a simple ink detector, a 3x3 block of positive weights in the center, so a filled or thick region gives a large response. I'm still weighing whether to scale it to match the orientation filters, which reach values around five.

Now I'm writing out the 3x3 ink filter with a bias of zero, then the horizontal, vertical, and diagonal stroke filters with their negative flanks and biases.

I'm settling the diagonal filter's flanks: the stroke is about 2.5 pixels wide, so the flank cells just off the line could still catch ink, and I'm pushing them further out to the cells two steps away. Those outer flank weights come out to about -0.5 each, but a horizontal stroke then leaks a net response of 1, so I'm raising the flank penalty to -0.8 to suppress that.

I'm giving the diagonal flanks a larger negative weight, since a stroke three pixels wide would otherwise leak into the neighboring cells. Next I'm moving on to the anti-diagonal filter, and I'm still deciding whether a fifth filter should target stroke endpoints or blobs.

I'm considering whether conv1 should get a few more filters, perhaps finer-angled strokes or a second ink channel at a different scale. I'm leaning toward a steep diagonal filter for slanted 1s and 7s, though the existing vertical filter with pooling may already cover much of that.

I'm weighing whether conv1 should get a steep diagonal for slanted 1s and 7s, or a "top edge" feature that fires where ink sits below and empty space above. The top-edge idea seems redundant, since the horizontal-stroke filter already picks up those ends, so I'm leaning toward the steep diagonal.

I'm adding a seventh conv1 filter that detects empty 5x5 patches, which could help pick out the hole in a zero, though background outside the digit would fire it too. I'm weighing whether that pooled signal is worth keeping.

I'm considering whether channel 7 could be a curvature-style feature instead of another orientation filter, though I haven't settled on what shape it should take.

I'm weighing a duplicate ink filter at a larger scale, which would give a density reading after pooling, though it looks marginal. I'm also turning to conv2 and wondering whether its channels should simply pass through conv1's features at the center offset, since the 8x8 pooling regions tile the digit area without overlap.

I'm considering giving conv2's other channels a wider spatial pool, a 5x5 average over pool1 that covers roughly a 14x14 region, to get a robust coarse measure of how much of each feature is present. Another option is to have some conv2 channels detect conjunctions, like a horizontal and a vertical stroke appearing near each other as a crossing.

I'm weighing whether channels 8-15 of conv2 should be a blurred copy of the pooled features, so the vertical position of horizontal bars survives the coarse 4-row grid, which matters for telling 3, 5, and 8 apart.

I'm now shifting the second set of conv2 channels to a grid offset of (3,3), so their receptive areas interleave with the first set. That gives a finer vertical sampling, but it roughly doubles the template work, so I'm considering whether to hold off on it for this first step.

I'm moving toward building the shifted-grid templates from a shared function that rasterizes hand-described digit strokes into the 8x8 cell weights. This avoids synthetic data or any training-style fitting, since the weights come straight from the stroke geometry, and I'm working out the orientation coverage for each cell.

I'm checking whether rasterizing hand-described stroke prototypes into a per-cell orientation template still counts as template drawing rather than synthetic data, and I'm leaning toward keeping it explicitly framed that way.

Next I'm going to describe each digit as a list of stroke segments on a 4x4 grid, with an orientation label per segment, and have the code mark the cells each segment passes through. That gives me the templates without generating any synthetic images.

I'm checking the shifted grid's cell coverage now: the second set of channels should cover rows 4u+6 through 4u+13, which in the first grid's coordinates means a span of about two units per cell. That spacing doesn't line up with the non-overlapping tiling I described earlier, so I need to reconcile the two.

I'm checking the overlap: the first set of cells spans two units each with a stride of one unit, so neighbouring cells share half their area. I'm mapping the cell boundaries into a common coordinate frame where x = (row - 4)/4, and the shifted grid's cells start half a unit later than the first set's.

I'm working out the soft weighting for the cell templates: each stroke point gets a triangular weight toward the nearest cell center, so a point lands mostly in one cell and partly in its neighbor. I'm considering whether the shifted grid is worth adding at this stage, though I'm leaning toward including it.

Now I'm settling on the shifted grid for channels 8-15 after all, since the conjunction and blur alternatives look redundant once max pooling is applied. Now I'm turning to describing each digit as stroke segments in the continuous coordinate frame.

I'm laying out each digit as a list of stroke segments in a continuous 0–5 grid, starting with the zero as an ellipse approximated by a polygon, and I'm making the one a near-vertical line.

I'm sketching the stroke layout for digit 3 next, starting with an arc in the upper loop that spans about 160 degrees over the top.

Continuing to draw the digit templates as stroke polylines, I'm laying out the 3 with a top loop, a middle junction, and a bottom loop. Then I'm starting the 4 as a diagonal from the upper middle.

Still writing digit stroke coordinates...

Still writing digit stroke coordinates...

Still writing digit stroke coordinates...

I'm settling on eight channels for the orientation templates, weighing whether to spread the orientations evenly across the range or to keep the steep diagonals I already have. I'm still choosing the exact angles to cover.

I'm defining the 5x5 oriented line filters by formula, measuring each pixel's perpendicular distance from a line at a given angle so the center stripe is positive and the flanks negative.

I'm deriving the 5x5 line filters from a formula: each pixel's perpendicular distance to a line at the chosen angle, with positive weights near the line and negative weights on the flanks. I'll normalize the positive and negative parts so they sum to 5 and -5, then add a slight negative bias.

I'm settling the negative weights so the flanks sit around -5.5 in total, and checking that a stroke offset by one column still gives a positive response in the centre cell. Max pooling should absorb the remaining shifts.

I'm settling the ink channel as a 3x3 block of ones scaled by 5/9, so a filled area gives a response of 5 and matches the line filters. For the seventh channel I'm considering a 5x5 ink filter with a high bias so it only fires on dense regions like junctions and thick strokes, though it might just duplicate the ink signal.

I'm weighing whether negative ink weights on cells that should be empty are too brittle, since handwriting varies in thickness and slant. For a digit like 1 or 0 that would mean penalizing ink in many cells, so I'm inclined to keep the ink channel's influence on empty areas mild or zero to avoid overfitting to my hand-drawn shapes.

I'm settling how the positive and negative template weights should scale, so that a digit with more strokes doesn't get a larger logit than the others. My plan is to normalize each class's positive template to a shared total, and do the same for the negative template, with the per-weight scale set so a correct match lands around a logit of 10.

I'm settling the scale of the template weights: each class gets a fixed total of positive weight, around 3.0, so a fully matching digit lands near a logit of 6 to 12, with biases left at zero for now and tuned later from the confusion matrix. Negative weights on ink in cells that should be empty get a smaller total, around -2.0 per class. I'm also keeping in mind that the orientation channels carry a small negative bias and their flanks, so their responses probably sit around 2 to 4.

I'm weighing how the max pooling stage affects the template: a stroke that only clips the corner of a cell still fires the full response, so the coverage-based weights for partially filled cells should stay soft rather than sharp.

I'm working out how the cell weights should treat overlap: a stroke near a cell's edge might fire two neighboring cells at once, so a sharp triangular weighting could undercount it. I'm considering a flat-topped coverage weight that gives full credit across the middle of each cell and ramps down only at its borders.

I'm checking how far a pooled cell's receptive field can see a stroke, and how the conv1 window and the second pooling stage line up with that, so the template weights stay consistent across the two layers.

I'm recomputing where each pooled cell's effective center sits, shifting the x-range to roughly u+0.875, and adjusting the trapezoid weighting so full weight covers about ±0.5 with a linear falloff to zero at ±0.9.

Working out where pooled cell u actually sees the stroke: with the conv2 kernel at offset k, the second pooling stage picks up conv1 centers across a window of roughly four rows, which shifts the effective center by about one more pixel-pair in x.

I'm checking where the pooled grid's centers land: the cells would sit around 0.875, 1.875, 2.875 and so on, which leans toward the top of the digit. The digit's middle falls between two cells, so I'll use the offset-2 grid as the primary one and add a second grid shifted by one more pixel-pair.

Now I'm checking the column geometry, which mirrors the rows: the center sits at column 14, or y=2.5. Digits are centered by their center of mass rather than their bounding box, so a 7 or 9, with its mass near the top, gets pushed downward in the frame, and I need to account for that when placing the stroke polylines.

I'm estimating where the center of mass falls for each digit, since MNIST centers by mass rather than by bounding box. A 7 or 9 has its mass near the top, so its box shifts down, while a 6 shifts up. For 1, 0, 8, 3, 5 I'll assume the mass sits near the middle, and the 2 sits a little lower.

I'm now setting the orientation channel weights by soft-assigning each segment's angle to its two nearest channels, falling off linearly over 30 degrees. For the ink channel I'm integrating coverage along each stroke with a trapezoidal falloff, sampling finely enough to keep the template smooth.

I'm setting each class's positive template from the coverage values, with each cell's total ink coverage normalized by how much area it covers. The weights go into two grids, with the ink channel scaled by a separate constant and a penalty applied where the template should be empty.

I'm normalizing each class's template so its positive weights sum to about 4.0 and its negatives to about -3.0, which keeps digits with many strokes, like 8, from getting a larger logit than the others. I'm also checking that a negative weight on the 1 template handles ink from sub-shapes like the top of a 7.

Now I'm checking how the conv2 weights map onto the pooled grid, setting the center weight to 1 for the matching channel and the offset weight for the ink channel.

Now I'm writing out the stroke polylines for each digit in row and column coordinates, starting with the 0 as an ellipse and the 1 as a near-vertical line.

Still writing out the stroke coordinates for the 3, placing the middle bar as a short horizontal segment.

Still working out the stroke coordinates for the 4: a left diagonal, a horizontal bar, and a right vertical, and I need to check where its center of mass sits.

Now I'm placing the digit 4 and 5 strokes in the coordinate frame, and I'm thinking the 6 needs its loop shifted upward because its mass sits low.

I'm checking how the digit 7's center of mass shifts its bounding box, estimating that the top bar and diagonal put the mass to the right of center. I'm working through the numbers to see where that mass lands before placing the stroke.

I'm now working out where the digit 7's top bar goes: its center of mass sits toward the right of its box, so the whole digit shifts down, putting the bar near the upper-middle of the frame.

I'm estimating the center of mass for the 9, with its upper loop and tail, to work out how far its box shifts.

I'm estimating the center of mass for the 4 next, with its left diagonal, bar, and right vertical stroke, to see how far that digit's box shifts.

Checking the center of mass for the 5 next, with its top bar and loops, to see how far that digit's box shifts.

I'm checking the vertical centers of mass for the digits that remain, and it looks like the 5 needs only a small downward shift. The 3, 1, 0 and 8 are close to symmetric, so I'll leave them where they are. Then I'm looking at the horizontal center of mass for the 4, which lands near 2.57 and seems fine.

I'm estimating the center of mass for the 2, 6, 9, 5 and 3 digits, checking whether each one's horizontal mass sits left or right of center. The 6 and 5 need small rightward shifts, the 9 a small leftward one, and I'm starting to work out the 3's mass, which looks weighted toward the right.

I'm checking the 1 template's negative cells: the stroke falls mostly in the middle two columns, so the outer cells should stay at zero.

I'm checking the grid centers again, where the second grid sits one step offset from the first, so one column is fully covered and the next only partly. I'm settling on a trapezoidal falloff that is full within half a cell and reaches zero at 0.9, then working out how to normalize coverage by the sampled step length.

I'm checking how the negative ink weights behave for the 8 and 0 templates, since the 0 has no ink at its center while the 8 does, and that difference should show up in the weights.

I'm settling the logit scale now: with both grids counted, the positive weights come to roughly 0.125 each, so a full match gives a large logit, while a partial match against a wrong class still leaves a clear margin.

I'm checking how orientation responses behave when a stroke crosses a cell: a line near the filter's center fires strongly, so each pool cell should respond across a few rows, and a vertical line gives roughly the full sum of 5. Next I want to count how many pixels fall within 0.7 of a 30-degree line through a 5x5 filter.

Checking which pixels fall within 0.7 of a 30-degree line through the 5x5 filter, I'm counting the cells on the line and the ones just beside it.

Now I'm counting the flanking cells outside that 30-degree band, deciding how many fall on each side and how to scale the positive and negative weights.

I'm checking the flank threshold for the 30-degree case: a cell at distance 1.7 from the line might carry only partial ink, so I'm raising the cutoff to 1.9 to keep fewer flanks. For the vertical case the flanks are just the cells two columns away, and I'll scale each negative to about -0.5 so the total stays at -5.

Now I'm settling the flank falloff for the negative weights and the positive falloff, normalizing each to fixed totals and adding a small negative bias. Next I'm about to pick a smoother 5x5 ink filter instead of the 3x3 one.

I'm settling the 3x3 ink filter at 0.55 per cell so a stroke of width 2.5 gives a response of about 4, and I'm leaving the bias at zero. I also want the 7th channel to play a small role of its own, so I'm considering a coarse 5x5 ink filter for it instead.

Checking the top of the 2 against the first grid's leftmost row, the arc sits just outside cell 0's falloff, so I'll shift that digit's shape down a bit to get it covered.

I'm checking where the top of the 2's arc lands relative to the first grid's coverage, and I'm weighing whether shifting the first grid's sampling changes which cells see that stroke.

Writing the conv1 weight setup in code now...

Still writing the oriented line filters...

Still writing the oriented line filters...

Still writing the template accumulation...

Still writing the template accumulation...

Still writing the template code, now adding the digit shapes as polylines and ellipses...

Still writing the digit polylines...

Still writing the digit polylines...

Still writing the digit polylines...

Still checking the sign and scale of the negative weights for the digit 1 against the other digits.

Comparing class 4 against the 1 more closely, its right vertical stroke overlaps the 1's ink in the middle column, so the 4 template should only pick up a fraction of its positive weight there.

Still checking the fully connected weights: the digit 4's stroke overlaps the 1's middle column, so it should pick up only a little of its positive score. I'm also sizing the negative weights so a stray response in an empty cell costs about 0.6, and I'm noting that thick strokes may weaken the orientation responses a bit. With the logits around 12 for the right digit and 3 for the wrong one, I expect the softmax to be fairly confident, so I'm watching how a misclassification would hurt the loss.

Still writing the conv1 weight setup, now filling in the negative flank weights and the coarse ink channel.

Still writing the conv1 filters, now setting the ink channel and looping over the orientation angles to fill each oriented filter's positive and negative weights.

Still writing the conv1 filters and the conv2 channel setup.

Still writing the digit templates, now shifting the 6's loop and tail into place.

Now I'm settling the rest of the digit templates and the stroke rounding for the 6, then I'll write the code with the normalization of the positive and negative weights.
