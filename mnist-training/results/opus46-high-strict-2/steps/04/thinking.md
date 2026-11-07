Let me analyze the step 3 results:

Accuracy improved from 31.2% to 36.4%. The bias corrections helped but not as much as I hoped.

Let me look at the confusion matrix more carefully:

Predicted column sums:
Col 0: 500+0+0+0+1+1+3+4+0+6 = 515
Col 1: 1+603+4+35+23+4+14+31+31+30 = 776
Col 2: 88+35+556+64+14+60+59+3+236+1 = 1116
Now I'm tallying the remaining confusion-matrix columns, working through the column sums from column 3 onward and getting totals for each.

Now I'm checking the per-class prediction totals against their targets, and the bias on class 8 looks like the main problem: it's predicting 2450 cases against a target near 974. Class 3 and class 7 are also running high, while classes 4 and 9 are well under their targets.

Now I'm going through the per-class accuracy figures, and the pattern is mixed: classes 2, 3, and 5 improved noticeably, while classes 1, 4, and 7 dropped. Class 8 is still the one I can't pin down yet, since its accuracy figure is cut off.

Now I'm reviewing the per-class accuracy and the main confusion pairs, where true class 4, 9, and 6 are mostly being predicted as class 8.

Now I'm adjusting the biases: class 8 is over-predicted, so its bias should come down, and class 3 is running high too, so its +0.8 bias looks too strong. I'm also recalibrating the rest against the prediction-to-target ratios, starting with class 0's correction.

Now I'm recalculating the biases for classes 2 through 6 from their prediction-to-target ratios, starting with class 4, which is badly under-predicted and needs a bias increase of about +0.76.

Now I'm working out the rest of the bias adjustments from the prediction-to-target ratios: class 6 needs a larger increase, class 7 a reduction, class 8 a much smaller bias, and class 9 the biggest increase of all, since it's badly under-predicted.

Now I'm working out the bias for class 0 and the rest, using a conservative step size on the log of target over predicted counts.

Now I'm working out the class 7 bias from its prediction-to-target ratio, which is running high, so it needs a larger step down.

Now I'm working out the bias values for each class from the log of target over predicted counts, using a conservative step size. Class 8 over-prediction means its bias comes down a lot, while class 9, which is badly under-predicted, needs the largest increase.

Now I'm checking why digit 4 keeps getting predicted as 8, and whether the templates for 9, 6, 7, and 1 are overlapping in similar ways.

Now I'm working through the centered ink template for digit 4, and then setting it beside the centered template for digit 8 to see how they line up.

Now I'm working out the class 4 logit from the ink features, checking how the digit 4's left diagonal, right vertical stroke, and crossbar line up against the template weights.

Still working through the logit sum for digit 4 against the template weights.

Still working out the class 8 logit from the ink features, comparing its template weights against the same feature grid.

Still working out the class 4 logit, which is coming to about -0.43 from the sum over the template weights.

Still checking the class 4 logit against the class 8 one, since the gap should be large enough to rule out the confusion I'm seeing in the matrix.

Checking whether the hole detector fires on the enclosed triangle in a digit 4, since that could be what pushes class 8's logit up.

Still working out the hole-detector values for digit 4, using the same centered-template arithmetic to see whether the enclosed triangle pushes class 8's logit up.

Checking whether the hole detector's contribution is what pushes class 8 up for digit 4s, or whether the real cause lies in the other templates.

Now I'm checking the class 8 counts, which tally up to 2450 predictions, far more than the target and clearly pulled up by the +1.0 bias. The new +0.35 bias should bring that down a lot.

Still working out the conv2 redesign, starting with a center-surround operator on channel 0 to sharpen local contrast.

Still working out the conv2 redesign: channel 0 would be a center-surround kernel, which fires on locally concentrated ink, but that loses the plain ink-density signal, so I need both.

Now I'm reassigning some of the conv2 channels: keeping channel 0 as plain ink density, and giving channel 1 a center-surround contrast on the ink, since that would fire on locally concentrated strokes.

Now I'm weighing whether to change conv2 at all, since its channels 0-7 currently just pass conv1 features through and the rest handle strokes, corners, and diagonals. Replacing some pass-throughs with center-surround contrast would sharpen things, but I'd have to keep plain ink density somewhere too, so changing conv2 means reshuffling what each channel does.

I'm weighing whether to reshape the conv layers now, but that means changing the FC templates at the same time, which is risky. So I'm leaning toward improving the FC layer instead, through better biases, sharper templates, and more of the available channels. My thought is that the 4x4 grid may be too coarse to separate all the digits, so raising the template scale from 0.3 to 0.5 might amplify the differences that do exist.

Now I'm weighing a change to the conv1 ink detector, raising its threshold so it only fires in the densest ink regions, which might give the spatial pattern more contrast. Or I could turn conv2's smooth pass-through into a center-surround operator, so local differences in the ink map get amplified. I'm starting to sketch that center-surround kernel for conv2 channel 0.

Still working out the conv2 change: a center-surround kernel on channel 0 would sharpen the local ink contrast, but it would also mean updating the FC templates to match.

Reconsidering the conv2 channels: I'd turn a few of the unused slots (10-13) into local-contrast and directional ink detectors, but I'll first see whether better biases and sharper templates in the FC layer already help enough.

I'm considering swapping conv2's smooth kernel for a delta function, a single center pixel at weight 4.0, so the spatial resolution isn't blurred before pooling.

Next I'm checking the delta-kernel version: conv2 output at each position just copies the matching maxpool1 value, so the 8x8 map pools down to a 4x4 grid that keeps finer spatial detail than the smooth kernel did.

Now I'm working out how each 4x4 pooled position maps back to a 2x2 block of the 12x12 map, with the offsets that shift the window across the grid.

I'm checking the delta-kernel version against the smooth one: with the delta, each pooled cell only reads a 2x2 block of the 12x12 map, and those blocks skip the outer rows and columns entirely, so the edges would be lost.

Now I'm checking the 4x4 block boundaries: the first pooled cell covers maxpool1 positions 1 through 4, which is the same region the earlier smooth-kernel layout would have used.

I'm weighing the delta kernel against the smooth one: with the delta, each pooled cell reads only a small block and the edges drop out, while the smooth kernel covers more of the map with heavier overlap. Less overlap gives sharper spatial contrast, but losing the border positions costs some information.

Rather than repeat the earlier reasoning, I'll focus on the biases and templates, since the conv layers have been getting too much attention. The corner channels (10-13) might carry useful signal for telling apart digits like 4, 7, 2, and 3 at their turns and junctions.

I'm re-deriving what conv2 channel 10 detects: it combines conv1's bottom-boundary and right-boundary detectors, so it should fire where ink ends at the bottom and the right at the same spot. That's the bottom-right corner of an ink block, which is the same as the top-left corner of the background next to it.

Working out the corner channels: the bottom-right corner of the horizontal bar in a 4 is where the junction sits, but building good templates for them is tricky, so I'll leave those for a later step and focus on biases, ink templates, the conv2 kernel, and the FC scale.

Still writing the weight initialization code...

Still writing the conv1 kernels...

Still writing the weight initialization code...

Still writing the weight initialization code...

Still writing the conv2 kernel weights...

Still writing the fully connected template weights...

Still writing the template weights...

Still writing the template weights...

Still working through the delta-kernel version: each pass-through pixel would just copy one maxpool1 value scaled by 4, so the pooled grid keeps finer detail than the smooth kernel did.

Working out the maxpool2 values now: each pooled cell takes the max over four delta-sampled conv2 positions, which equals four times the max of a 2x2 block of maxpool1 values.

Working out the receptive field for each pooled position now: the delta-kernel maxpool2 cell at (R, C) reads a 2x2 block of maxpool1, and each of those is itself a 2x2 block of conv1, so I need to trace how far back through the 5x5 filters that reaches.

Now I'm working out the receptive field of each pooled position: the delta kernel reads a 4x4 stretch of conv1 output, which with the 5x5 filter spans an 8x8 patch of the input, centered near (4R+7.5, 4C+7.5). For the first position that's rows 4 through 11.

Now I'm checking the receptive field of the delta-kernel version: with it, each pooled cell covers about 8 pixels of input instead of 16, so there's less overlap between neighboring positions and sharper spatial detail, though the digit's outer edges may fall outside the grid.

I'm weighing the delta kernel against the smooth one: each 4×4 position would read only a small patch, so it's sharper but more sensitive to exact pixel placement. The smooth kernel averages over more of the image and should hold up better to the shifts and size changes in MNIST digits. I'll try a compromise, a narrower plus-shaped kernel.

Still writing the spatial kernel code...

Comparing the three kernel options, the delta uses only about four maxpool1 positions per grid cell, the smooth kernel about sixteen, and the plus-shaped kernel falls in between. I'm going to try the plus kernel for step 4 to see whether it helps.

Checking the maxpool2 arithmetic for the delta kernel: each pooled cell is the max of four conv2 outputs, and each of those is just four times one maxpool1 value, so the result depends on a 2x2 block of the 12x12 map.

Working out the maxpool2 expression for the delta kernel: each pooled cell is four times the max of a 2x2 block of maxpool1 values, and that block is itself the max over conv1 outputs.

Now I'm working out the max over the conv1 positions that feed into this maxpool2 cell, tracing how those 2x2 blocks of maxpool1 map back through the conv1 grid.

The receptive field here works out the same way as before: each smooth-kernel pooled cell reads a wider stretch of the input, and I'm now checking how many maxpool1 positions the 3×3 conv2 window pulls in for each output.

Working out how the max-pooled grid cells depend on the 2×2 blocks of conv2 outputs, with each conv2 value drawn from a 3×3 window of maxpool1.

The delta kernel picks out the single strongest feature point in each 2×2 block, while the smooth kernel takes a local average, so it needs a consistent feature across a small area. For MNIST, where the strokes are consistent over small regions, the smooth version may hold up better. The trade-off is that its wider overlap between grid positions costs some discrimination. I'll try the delta kernel for step 4 and switch back if it doesn't help.

Looking at the confusion matrix again, I'm wondering whether the conv layers are even the bottleneck. The top errors are 4→8, 9→8, 6→8, 7→3, 1→7 and 8→7, so what I really need is templates that separate those specific pairs.

Now I'm comparing digit 4 against 8 on the grid: the 4 is angular with a pointed junction and a flat crossbar, while the 8 is round with two loops.

Now I'm comparing the two grids: the 4 has high values across the right column and a diagonal on the left, while the 8 has low values in its top and bottom rows and mid-level values on both sides.

Now I'm comparing digit 4 and digit 8 on the grid to find something that separates them after pooling. Digit 4 has no ink at the bottom-left, while 8 does, and I might be able to exploit that more strongly in the template. The hole detector could also help, since 4 has a single triangular hole near the top while 8 has two.

Now I'm weighing whether the hole detector can separate 4 from 8, since many MNIST 4s leave their left side open and never enclose a hole. I'm considering a hole template for the right-center area, but I'll just adjust the biases first and see how the matrix changes.

Next I'm adjusting the biases, especially for class 8, and scaling up the templates for sharper discrimination, then adding per-digit templates across several channels for step 4. I also notice the digit 7 template keeps getting confused with 3, so I'm looking at why its centered values are so mixed up.

Still computing the centered digit 7 and digit 3 templates...

Still working through the digit 7 response: the top bar and diagonal features should push its logit up, while the left-column negatives pull it down.

Still working out the digit 3 scores on those same features: the first row comes to about 1.9, and the middle rows are much weaker because of the negative template weights on the left.

Still working out the digit 7 logit from the same features: the top row contributes most of it, and the total comes out to about 5.4 before the row-by-row sums continue.

Still computing the digit 7 logit from these features: the row sums come out to about 2.19, 0.63 and 2.13 for the rows after the top one, and the total is about 10.3 before scaling.

Now I'm checking the bias terms: class 3 gets a +0.8 boost and class 7 a -0.3 penalty, which could explain why the 7s keep landing on 3 even though the raw logits favor 7.

Now I'm comparing the two logits: class 3 comes out to about 1.57 with its bias, class 7 to about 2.79, so 7 still leads by roughly 1.2. That margin should be enough, but my feature estimates may be off, and the ink channel could be giving values I'm not expecting, so I want to check the actual features for a 7.

Now I'm working out how the max pooling carves up the conv2 output, tracing which maxpool1 cells each pooled value covers.

Now I'm looking at how each max-pooled cell in the 2×2 grid covers different ranges of the first pooling layer, with the top-left cells picking up the left end of the bar and the middle cells catching its strongest part. The lower row is where I start to lose track of the exact values, so I'll stop trying to predict the features by hand.

Now I'm settling on the next steps for step 4: adjusting the biases from the confusion matrix, adding more templates, and reworking the conv layers.

Now I'm sketching out the 80 templates for step 4, covering all 8 useful channels across the 10 digits, to use more of the available FC parameters.

Next I'm laying out a table for step 4: for each digit, what each of the eight channels looks like on the 4×4 grid, starting with digit 0 as a circle.

Still laying out the per-digit templates: for digit 1, I'm checking which channels pick up its vertical line at the bottom and top edges.

Still laying out the per-digit templates: for digit 2, I'm mapping which channels pick up the top curve, the diagonal and the bottom bar.

Still laying out the per-digit templates: for digit 3, I'm mapping which channels pick up its right-side arcs, its open left side, and the bottom edges along each curve.

Now I'm laying out the per-digit channel patterns for step 4, moving from digit 4 to digit 5.

Now I'm laying out the per-digit channel patterns for digit 5: the top bar shows up on channels 0, 1, 2 and 3 near row 0, the left descender on channels 0 and 4 in the middle rows, and the bottom curve on channels 0, 1 and 3 near row 3. Digit 5 has no enclosed holes, and its only horizontal stroke is at the top, so channel 8 lights up in row 0 alone. Channel 9 barely registers, just a weak vertical at column 1 from the descender. Then I'm moving on to digit 6, with channel 0 covering the top arc and the bottom circle, and channel 1 picking up the bottom edges of both.

Still filling in the per-digit templates: for digit 6, I'm mapping the bottom circle's top and right edges, the hole in its lower half, and the left-side stroke. Digit 7 is next, with the top bar and diagonal showing up on the top and right channels.

Still laying out the per-digit templates: for digit 7, I'm noting that channel 8 gets a strong signal from the top bar and channel 9 stays mostly empty, then moving through digit 8's two loops and their holes, and starting on digit 9's circle and descending stroke.

Now I'm weighing how to pick the templates that separate 4 from 8, since those two are the most confused pair.

Now I'm weighing 4 against 8: 4 has no ink in the bottom-left and a strong straight right stroke, while 8 has both, so I'll strengthen the negative weights there and add a stronger vertical template for 4. For 9 against 8, the hole only appears in the top half and the right side runs straight down, so I'll boost the top-hole template and add a right vertical stroke for 9.

I'm moving on to the 6-versus-8 pair: 6 has a hole only in its bottom half while 8 has holes in both, so I'll strengthen the bottom-hole template for 6. For 7 against 3, 7 has a strong flat top bar and a diagonal instead of arcs, so I'll boost the row-0 horizontal template for 7.

Now I'm weighing 1 against 7: 1 has no horizontal top bar, while 7 does and is wider at the top, so I'll add a template that penalizes horizontal strokes for 1. For 8 against 7, 8 has ink on both sides and holes while 7 doesn't, so I'll strengthen the hole template for 8. I'm also thinking about the shared fixes: better bias corrections, stronger hole and stroke templates, and more negative weights in the ink templates.

Now I'm tweaking the template weights for the code. I'm raising the hole template for digit 0 and the hole templates for 6, 8 and 9, and boosting the horizontal stroke templates for 7 and penalizing them for 1.

Still writing the template code...

Still writing the horizontal-stroke templates for channel 8, and I'm working out how each digit's top and bottom edges should light up.

Still writing the horizontal-stroke templates for channel 8, one row of pattern at a time.

Still writing the horizontal-stroke templates for channel 8, one row at a time.

Still writing the per-digit template weights, now filling in the vertical-stroke channel for each digit.

Still writing the per-digit template weights, this time for the vertical-stroke channel.

Still writing the per-digit template weights, now the vertical-stroke channel. Dropping the all-zero templates, since they do nothing after centering, and keeping only the entries with real signal before I finalize step 4.

Now I'm settling the step 4 plan: first the biases, then raising the template scale, adding more templates on the horizontal and vertical stroke channels, and strengthening the hole templates. I'm also considering a delta kernel for the conv2 pass-through, but I'll leave the conv1 filters and the conv2 kernel alone so I can tell which change actually helped.

Still writing the weight code, now setting up the bias values and the conv1 filter layout.

Still writing the convolution weights, now setting the filter biases and the oriented edge filters for channels 1 through 4.

Still writing the conv1 filter weights, now setting the oriented edge filters and the Laplacian-style filter for channel 7.

Still writing the conv2 weights, setting up the delta-style kernel and the per-channel pass-through.

Still writing the conv2 weights, now setting the per-channel pass-through and the cross-channel kernels for channels 8 through 15.

Still writing the weight-building code, now setting the FC biases and the template helper that fills each digit's 4x4 grid.

Still writing the weight code, now filling in the per-digit templates for the ink and hole channels.

Still writing the per-digit weights for the ink channel, filling in digit 7's template.

Still writing the digit-7 hole templates...

Still writing the digit-6 hole templates...

Still writing the horizontal-stroke templates for channel 8...

Still writing the horizontal-stroke templates for channel 8.

Still writing the horizontal-stroke templates for channel 8, filling in the last digit's entry.

Still writing the vertical-stroke templates for channel 9...

Still writing the edge templates for the digit-1 entry on channel 1.

Still writing the edge templates for the digit-0 entry on channel 4...

Still writing the penalty code for the confusion pairs, starting with the negative horizontal weight for digit 4.

Still writing the digit-4 template on channel 8, adding a penalty on the top bar and keeping the crossbar weight.

Still tuning the weights for the 4-versus-7 pair. I'm checking the centered values for digit 4's horizontal-stroke template to make sure the top-bar penalty and the crossbar weight come out as intended.

Still working out the digit-7 template on channel 8, with the centered values.

Still writing the digit-0 horizontal-stroke template on channel 8, with the negative weights in the middle rows.

Still writing the horizontal-stroke templates for channel 8, now the entries for digits 1 through 4.

Still writing the horizontal-stroke templates for channel 8, now the entries for digits 5 through 7.

Still writing the vertical-stroke templates for digit 0 on channel 9.

Still writing the vertical-stroke templates, now giving digit 1 a strong center column and digit 4 a right-side column.

Still writing the per-digit weights, now the vertical-stroke channel for digit 9, and I'm adding cross-digit features to separate 4 from 9 and 0 from 8.

Now I'm weighing the remaining discriminations: 0 versus 8 through the holes, and 3 versus 5 through the left-side ink and the top bar. I think the templates cover these reasonably well, so I'll finalize them. I'll leave the conv layers as they are and change only the FC layer, so that any accuracy gain can be attributed to that change.

Checking whether the bias values still hold once the template scale goes up from 0.3 to 0.4. Since the templates are zero-mean, raising their scale shouldn't shift each class's average logit, so the biases look like they can stay as they are. I'm not fully sure the zero-mean assumption carries over to the actual feature values, though, so I want to verify that before settling on it.

Now I'm working out the bias values, and wondering whether they still hold once the template scale goes up, since the zero-mean templates might not shift the average logits as cleanly as I assumed. I'll keep the biases as computed and check the class balance once the code runs, adjusting in step 5 if it's still off.

Still writing the conv1 weights, now setting up the Gaussian ink detector and its bias for channel 0.

Still writing the conv1 edge filters, now setting the horizontal and vertical edge kernels and their negated copies for channels 1 through 4.

Still writing the conv2 kernel setup, starting the center-weighted mask.

Still writing the conv2 weights, now setting the cross-channel kernels for channels 12 through 15.

Still writing the FC layer setup, filling in the bias vector for the ten digit classes.

Still writing the FC bias-and-template helper code, now setting up the ink-density weights for digit 0 and beginning digit 1.

Still writing the FC template entries for digits 2 through 5 on the ink channel.

Still writing the FC template entries for digit 0's hole channel.

Still writing the FC template entries for digit 0's hole channel, now the penalty values for digits 1 through 4.

Still writing the digit-8 hole template on channel 7, the two central rows at half weight.

Still writing the horizontal-stroke templates for channel 8, now the entries for digits 1 and 2.

Still writing the digit-7 horizontal-stroke template on channel 8...

Still writing the vertical-stroke templates, now setting digit 1's entry on channel 9.

Still writing the digit-9 vertical-stroke template on channel 9...

Still writing the digit-3 horizontal-stroke template on channel 8, with the edge templates for channels 1 and 2 following.

Still writing the FC template entries, now the channel-7 penalties for digits 0 and 1 and the conv1 edge kernels.

Still writing the digit-4 templates, checking that the ink, horizontal-stroke, and vertical-stroke entries separate 4 from 8.

Still comparing the 4 and 9 ink templates, checking where the strong negative weights fall.

I'm checking whether the class 9 bias of +1.1 is too strong, since the new hole and stroke templates may already lift class 9's scores enough.

I'm nudging the class 9 bias down from +1.1 to +0.9, since +1.1 might boost class 9 too much now that its hole and stroke templates are stronger. I'm also rechecking the rest of the bias vector against the step 3 counts, with class 9 still the most under-predicted.

Working through the class bias adjustment now: starting from the step 3 counts, I'm applying a log-ratio update against a target of about 1000 predictions per class, beginning with class 0, which comes out at roughly +0.33.

Still working out the per-class bias updates, now with class 2 and class 3 coming out at small negative and positive adjustments from their step 3 values.

Still working out the per-class bias updates, now with class 6 and class 7 coming out at a positive and a negative adjustment.

Checking the bias values against the new template scale: the templates are zero-mean, so raising them from 0.3 to 0.4 shouldn't move the average logits much, but the actual feature values may not be zero-mean. I'm weighing whether to rescale the biases to match, or keep them as they are.

I'm settling on the final bias values, and since the bias offsets are absolute, the ones computed from the old predictions should still roughly hold at the larger template scale. I'll go with these and check the resulting counts once the code runs.

Still writing the FC bias vector, settling on the first four entries.

Still writing the FC bias vector, settling on the final values and committing to them without further deliberation.
