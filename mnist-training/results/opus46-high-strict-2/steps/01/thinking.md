Let me think about this carefully. I need to design a small CNN for MNIST digit classification by hand, without any training data or gradient descent. I need to choose all weights myself.

Let me think about the architecture:
- Conv1: 1 input channel, 8 output channels, 5x5 kernel → produces 8x24x24, then ReLU, then MaxPool2d(2) → 8x12x12
- Conv2: 8 input channels, 16 output channels, 5x5 kernel → produces 16x8x8, then ReLU, then MaxPool2d(2) → 16x4x4
I'm laying out the rest of the network: flattening the 16×4×4 output to 256 values and mapping those to 10 class scores through a fully connected layer. Next I'm settling on the feature types for Conv1, starting with horizontal and vertical edge detectors, and I'm working through the diagonal ones.

I'm weighing a plan for Conv2's 5x5 filters over the eight edge-style channels, and I think they should pick out higher-level shapes. For the FC layer, the open question is which of the 256 spatial features line up with which digit, and I'm still working out how to pin that down without any data.

I'm sketching out the 4x4 spatial grid the FC layer has to read, since two rounds of pooling shrink the 28x28 input down to roughly that size. I'll use standard edge and blob detectors in the first conv layer, and the second layer is where I'd want curves and corners, though that's going to be hard to pin down by hand.

I'm working out how the 4x4 output grid lines up with the original image, roughly 7x7 pixels per cell. I'll try a template-matching approach next, where conv1 and conv2 act as simple pass-through or averaging steps and the FC layer does the matching.

I'm settling on a bank of eight 5x5 Conv1 filters, starting with edge detectors in four orientations, two diagonals, and a blob and its inverse. The next step is to write out the Conv1 kernels one at a time, and I'm about to start listing them.

I'm working out the Conv2 parameter count, 8×25 weights per output channel across 16 channels, and seeing that setting all of it by hand is a lot. A simpler route might be to have each Conv2 channel combine just a few Conv1 channels, such as horizontal and vertical edges meeting to form corners. I'm also starting to think about how the 256 flattened features map onto the 10 FC outputs, indexed by channel, then row, then column.

I'm working out how the 256 flattened features are indexed, by channel and then by row and column, and I'm sketching the 4x4 grid that the FC layer reads. The plan is to keep Conv2 close to pass-through and set the FC weights from what I expect each digit's shape to look like on that coarse grid.

I'm sketching the digit shapes on the 4x4 grid, where a 0 is an oval with curves top and bottom, a 1 is a central vertical stroke, and the rest follow similar stroke patterns. I'll keep this rough and refine it once I have a first version of the weights.

I'm settling on eight 5x5 Conv1 filters: horizontal and vertical edge detectors, two diagonals, a brightness detector, and a Laplacian for blobs and holes. Next I'm moving on to Conv2.

I'm settling on a plan for Conv2: pairs of output channels each focus on one kind of Conv1 edge, horizontal or vertical. I'll start setting the magnitudes now, since the activation range matters a lot.

I'm settling on magnitudes for the Conv1 filters: with weights around 0.2, a 5x5 edge detector on pixels near 0.3 gives outputs of roughly 1.5, maybe half that for edges since the signs cancel. Then ReLU keeps the positive part, max-pooling keeps the peak, and I still need to check that the FC inputs land in a sensible range. I'm going to start with Conv1 as edge detectors at different orientations, since those are well understood.

Writing the Conv1 kernels in code now, starting with the horizontal top-edge filter...

Still writing Conv1 kernels...

Still writing Conv1 kernels...

Still writing Conv1 kernels...

Still writing Conv2 parameter setup...

Still writing Conv2 smoothing kernels...

Still writing Conv2 channel setup...

Still writing Conv2 corner kernels...

Still writing Conv2 channel setup...

Still writing Conv2 channel setup...

Still writing the FC layer weights...

Still writing the FC layer mapping...

Still working out the FC layer mapping, since with all zeros it would predict the same class for every input. I'm considering a different strategy where each conv2 channel stands for a digit-relevant feature, which would keep the FC layer simpler. I'm also thinking about how the spatial layout of the digits across the 4x4 grid should shape those weights.

I'm working out how the 20x20 central region of the digit maps onto the feature grid, since most of the ink sits there. Conv1 with a 5x5 kernel and no padding means output position (r,c) is centered at input (r+2, c+2), and after 2x2 max-pooling each 12x12 cell covers roughly input positions (2r+2, 2c+2) through (2r+3, 2c+3).

Now I'm working out how far the receptive fields reach after the second conv, roughly mapping each 4x4 cell back to a patch of the original image.

I'm working out the receptive field for the second conv layer: each pool1 pixel depends on a 6x6 patch of the input, so the conv2 output covers a larger region built from those overlapping patches.

Working out the receptive field of the second conv: each conv2 output depends on five pool1 positions, and each of those reaches back through conv1 to the input, so the span grows to about 14 pixels per side with stride 2 in the original image.

The receptive field works out so that a pool2 cell, taking the max over a 2x2 block of conv2 outputs, will be looking at a fairly large patch of the original digit. Let me keep tracing how the pool2 positions map back onto the input rows and columns.

Tracing the pool2 mapping, each output row covers a 16-pixel span of the input, and those spans overlap, so together they span the full 28-pixel height. Working out the centers, the first two positions sit near rows 7.5 and 11.

Still working out the grid centers, now for the bottom row.

I'm laying out the spatial grid for the digit, where the four rows and four columns each cover a band of the 28x28 image centered around its middle. The digit sits in the central 20x20 box, so I'm mapping which grid rows and columns hold the top, bottom, left, and right parts of the digit.

I'm going through the features I expect each digit to show on the 4x4 grid. A 0 has edges all around and an empty center, a 1 is a narrow vertical stroke near the middle, and a 2 has a top curve, a diagonal down to the left, and a horizontal base. I'm now sorting out the rest of the digit shapes the same way.

I'm running through the remaining digit shapes on the grid: a 5 has a top bar, a stroke down the left, and a curve at the bottom right, while a 6 starts with a curve from the top that loops around at the bottom. A 7 is mostly a top bar with a diagonal down to the right, and an 8 looks like two stacked zeros. For the 9 I'm picturing a loop at the top with a stroke running down the right side.

Now I'm weighing a simpler plan: edge-detecting first-layer filters, a mostly pass-through second layer, and a fully connected layer that acts as a template matcher for where ink should appear in each digit.

I'm going to try the simplest version: edge-detecting filters in the first layer, a mostly pass-through second layer, and a fully connected layer that matches where ink should sit on the 4x4 grid. The density idea is that a 16-number summary of ink per cell should already separate the digits reasonably well.

Now I'm sketching the 4x4 ink templates for digits 0, 1, and 2, marking which grid cells should be filled for each shape.

Now I'm settling on a plan for the first conv layer: a set of simple filters, starting with an ink detector and then horizontal and vertical edge detectors.

Still writing Conv2 filter details...

Still writing Conv2 smoothing kernels...

Next I'm estimating the activation magnitudes so the logits don't end up nearly equal or wildly large. For the first conv, an edge filter with weights around 0.1 on ink pixels of 0.5 to 1.0 gives a response of roughly 0.6 at the peak, so after ReLU the range is about 0 to 2.

I'm estimating the activation magnitudes now: conv2 outputs could reach around 5 if each filter focuses on a couple of channels, so after ReLU and pooling the range is roughly 0 to 5. With 256 features at that scale and FC weights near 0.05, the logits would come out around 25, which is probably too large, so I'll drop the FC weights to about 0.01 or smaller. Many of the 256 features will be zero after ReLU, which should keep the sums lower than the worst case.

Still writing the weight initialization...

Still writing the conv1 filter setup, with a scale factor and a Gaussian-like center filter for ink detection.

Still writing Conv1 filters...

Still writing Conv1 filters: I'm defining the diagonal detectors and the remaining filter.

Still writing Conv2 weights...

Still writing Conv2 pass-through filters...

Still writing Conv2 channel weights...

Still writing Conv2 channel weights...

Still writing the FC layer and filling in its weights...

Still filling in the FC weights, now setting up the digit 0 template on the ink-density channel.

Still writing the digit 1 template and the rest of the FC weights...

Still filling in the digit 1 template, zeroing out the left column and dropping its scale.

Still writing the digit 4 and 5 templates...

Still writing the digit 7 template, the top bar and diagonal stroke down the left.

Still writing the digit 8 and 9 templates...

Still writing the digit 9 template and the function's return dictionary...

Now I'm wondering whether the FC layer relying only on the ink and hole channels is enough, or whether I should add negative weights to penalize features a digit shouldn't have. I'll check whether channels 13 and 14 actually produce meaningful activations: the ink detector responds where there's ink, the max pooling keeps that positive, and then the conv2 weighting for channel 13 scales it.

I'm checking whether channel 13 really tracks ink: the ink detector stays positive through ReLU and max pooling, and the smoothing conv2 weights keep that signal at each spatial position. For the hole channel, I'm noting that the Laplacian-style filter responds to a dark center surrounded by bright ink, which is what an empty loop looks like, but ReLU will only keep the positive side of that response.

Checking the Laplacian filter's response: it should be negative on ink, near zero on background, and positive in a hole. I'm verifying the center weighting by summing the kernel, which comes out to a total that needs a closer look.

I'm checking the ink-detector kernel's weight sum, which comes to 20 before scaling by 0.0375 for a total of 0.75. I'm also confirming that the Laplacian-style hole filter balances to zero so it only responds to dark centers surrounded by ink.

Now I'm checking the bias against the scaled ink response. At an average ink value of 0.5, the output comes to about -0.125 after the bias, so ReLU zeros it out. Even in dense ink near 1.0, the result is only around 0.25, which is too weak, so I'm considering a larger scale or a less negative bias.

Now I'm checking the magnitude of the conv2 output for channel 13, which relies on a center kernel scaled by 3 applied to the first conv channel.

Checking the scale on the channel 13 output: the center kernel totals 3, so with inputs near 0.3, the response comes to about 0.9. That's a reasonable range, and after ReLU and pooling it should sit around 0 to 2, which is what I want going into the FC layer.

I'm checking whether the ink-density templates are distinct enough, since digits like 0, 6, 8, and 9 all share ink on the left and right. The plan is to test it as a first pass, then add negative weights where a digit should have no ink.

I'm weighing whether the FC layer should use edge features too: vertical edges would help separate 1 and 4, and horizontal edges would help with 2 and 7. But that adds complexity, so I'll start simple and iterate. Maybe the conv layers should do more of the work and the FC layer less, or a different strategy overall: conv1 for local patterns, conv2 combining them into digit parts like top curves, loops, and vertical strokes, then the FC layer mapping those parts to digits. That last approach needs careful conv2 design, which is the hard part.

Still writing the Conv1 filter code, setting up the first ink detector kernel.

Still writing the Conv1 filter weights, now the horizontal edge detector.

Still writing the Conv1 edge filters, with the remaining filter setup.

Still writing the Conv1 filter weights, now the diagonal and ring detectors.

Still writing the Conv2 spatial kernel...

Still writing the Conv2 pass-through filters for the remaining channels.

Still writing the Conv2 channel weights, filling in the combined stroke detectors and the ink density channel.

Still writing the Conv2 channel weights for the ring and edge detectors...

Still writing the FC layer weights, now setting up the digit 0 template.

Still writing the digit 1 template weights, setting up the thin vertical stroke pattern.

Still writing the digit 2 template weights...

Still writing the digit 2 and digit 3 templates...

Still writing the digit 4 and 5 templates...

Still writing the digit 6 template and the digit 7 setup...

Still writing the digit 8 template, setting up the top loop.

Still writing the digit 9 template weights...

Still writing the digit 9 template weights and the function's return dictionary...

Next I'm tracing the signal through the conv chain for a typical ink pixel around 0.7, starting with the first ink-detector filter in conv1.

Now I'm estimating what a 5x5 ink-detector filter would output on a typical ink pixel, which comes out to a very small value that needs a closer look at the weights.

Now I'm checking the 5x5 ink-detector filter on a typical ink pixel, weighting the center most heavily, and I'll roughly sum the weights to estimate how strongly the output responds.

Now I'm checking the total weight of the 5x5 ink filter, which sums to 65 before scaling, so about 1.3 after the 0.02 factor. On a fully inked patch that gives roughly 0.91, and after the -0.2 bias it stays positive, so the signal survives ReLU. Even with only half the pixels inked, the output is still positive at about 0.255.

Now I'm checking the conv2 ink-density channel, where the kernel sums to 1 and then gets multiplied by 6, so an average neighborhood value of 0.5 should give roughly 3.0.

Now I'm checking the conv2 channel 12 output, where the weighted sum over the 5x5 window of the single active input channel should come to about 3 when the average maxpool value sits near 0.5.

Checking whether the negative weights in the templates help too, since a digit that should show no ink there would need that suppressed.

I'm weighing how strong the negative weights should be, since digit 1 should have no ink on its left and right edges, so those positions need stronger suppression. I also want to check which digit pairs are hardest to separate, like 0 versus 6, 0 versus 8, 1 versus 7, 3 versus 5, and 3 versus 8, so the templates can be adjusted for them.

The next thinking is mostly a restatement of ideas already covered: I'm reconsidering how to restructure the approach so the channels are used more aggressively, while accepting that the intermediate features are still unclear, and I'll keep it simple for this first step.

Checking the conv2 pass-through channels next, the mapping from each channel to its conv1 feature, before I settle the code.

I'm mapping out the conv2 channels one by one, and I've noticed channels 0 and 12 both track ink, while 7 and 13 both track holes, so I'll rework the layout to remove those duplicates.

Next I'm working out how to finish the FC scaling, since the simpler design is taking shape and I want the templates to line up with the conv features.

Still writing the Conv1 Gaussian filter weights, setting up the ink detector kernel.

Still writing the Conv1 edge filters, now the bottom edge detector that mirrors the top one.

Still writing the Conv1 diagonal filter weights...

Still writing the Conv1 ring detector weights, now the remaining filters for the convolution layer.

Still writing the Conv2 pass-through weights, now setting up the smoothing kernel for the first eight channels.

Still writing the conv2 weights for the top-left corner channel.

Still writing the Conv2 corner channel weights...

Still writing the FC layer's index helper, mapping channel and row and column positions to flat indices.

Still writing the FC layer's template helper and the per-channel scaling.

Still writing the digit 0 template weights for the ink and hole channels.

Still writing the digit 0 template weights for the bottom edge.

Still writing the digit 1 template weights...

Still writing the digit 2 template weights, setting up the top curve and the bottom bar.

Still writing the digit 3 template weights...

Still writing the digit 5 template weights...

Still writing the digit 6 template weights...

Still writing the digit 7 template weights...

Still writing the digit 8 template weights...

Still writing the digit 9 template weights...

Still writing the digit 9 template and wrapping up the return dictionary.

Still double-checking the index math in set_template, confirming that channel 7 starts at flat position 112 and channel 14 at 224.

Now I'm double-checking that conv2 channel 0 really draws from the first pool1 channel, so the flat FC indices 0-15 line up with the ink feature.

Now I'm checking the flat indexing against the feature map, confirming that the first 16 entries are the ink density and that channel 7 starts at 112. Next I'm thinking about the bias terms, where only the first conv1 bias carries a threshold of -0.3 to clear the background, and the conv2 biases stay at zero. I'm also considering how the edge filters behave after ReLU, since each one only keeps the positive side, so top-edge and bottom-edge detectors fire on opposite boundaries of a stroke.

I'm weighing whether the top-edge and bottom-edge filters can tell a horizontal stroke apart, since both fire on it. I'm also checking that the FC templates lean toward the central columns, and I'm concerned that the 5 and 3 templates look too similar, both carrying ink at top-right and bottom.

Now I'm comparing digits 0 and 8, which share the same outer ring on a coarse 4x4 grid. The thing that should separate them is the pinched waist in the middle of an 8, so the template for 8 needs its center to carry ink that a 0 leaves empty.

Now I'm comparing how the digit 8 and the digit 0 would fill a 4x4 grid. The 8 seems to carry more ink in the center columns, where its waist pinches, while the 0 keeps its ink pushed out toward the left and right edges.

I'm weighing whether the digit 0 template's negative center weights are enough to separate it from an 8, since an 8's ink in the middle would push the 0 logit down. I'm leaving the FC biases at zero for now, and I'm starting to wonder whether the ink density channel stays too uniform across digits to help much.

I'm weighing whether edge-based templates would help, since the FC layer would need to know which edge direction shows up at which spatial position for each digit. Checking the digit 7 and digit 1 cases, a top edge at row 0 and vertical edges in the middle columns look like the right signals. I'm leaning toward just submitting this first version and iterating from the confusion matrix. I also want to double-check the feature scale, since a weight of 0.15 times values around 1 to 4 gives contributions that may be small.

I'm estimating the logit margins now: a correct class might sum to around 2 to 5, against 0 to 2 for wrong classes, which should be enough discrimination. Checking that against cross-entropy, a margin of about 2 gives a loss near 0.8, not great but workable, so I'll finalize this version.

I'm checking the Gaussian ink detector kernel by summing its entries, which comes to 273, so I'll normalize it to sum to 1 and then scale it by 1.5.

Checking the scaling on the Gaussian ink kernel: a fully inked patch gives about 1.05 after the bias, a blank one gets zeroed by ReLU, and an edge lands in between, so the first conv layer behaves as intended.

Now I'm working out the FC contribution: a per-position weight of about 0.375 across roughly six positive positions gives a total near 2.25. That looks workable, so I'll settle on this approach. I have 15 steps to iterate, so the next question is how to spend them most efficiently, starting with a reasonable baseline.

I'm settling on a baseline first, aiming for something that handles all the digits reasonably rather than perfecting one. I'll finalize the current code and then review the convolution math, since I'm worried the smoothing kernel's sum is being misapplied across the 25 spatial positions.

Now I'm working out the conv2 output for channel 0: the smoothing kernel sums to 1 and gets scaled by 4, so a locally constant input of about 0.5 should come out near 2.0 before the ReLU.

Checking the scale on the edge channels now: a strong horizontal edge puts roughly 0.7 on the top rows and near zero below, so the response lands around 0.2 before the bias.

Next I'm checking how the edge channel scales through conv2 and pooling: a strong top edge comes out around 1.0 at the matching positions. The FC weight for those edge templates works out to only about 0.075 per position, which is quite small. I'll test the baseline first, since the ink density templates should carry most of the signal, and then decide whether the edge weights need to be stronger.

Let me look over the layout of the filters again. The first conv layer has eight filters: an ink detector, top and bottom edges, left and right edges, two diagonals, and a ring detector. The second conv layer carries the first eight channels forward and adds combined edge and corner detectors on top.

Now I'm weighing the last few channels in the second conv layer. Channels 14 and 15 duplicate the ink and hole detectors already in use, so I'm thinking about repurposing them, perhaps pairing ink with the top or bottom edge to capture stroke ends.

Now I'm settling on which channels 14 and 15 should carry, pairing ink with the two diagonal edge detectors instead of duplicating the earlier ink and hole channels. Then I'll move on to mapping where each digit's ink falls on a 4x4 grid.

Now I'm laying out the 4x4 grid of receptive field centers, with each cell's center coordinates running from about row 7.5 to 15.5 and column 7.5 to 19.5.

Now I'm laying out where each digit's ink should fall on the 4x4 grid of receptive-field centers, starting from the top-left corner and moving toward the bottom-right.

I'm placing the digit 0's ink on the 4x4 grid: the top and bottom rows should hit the two middle columns, and the left and right sides should hit the outer columns in the middle rows, while the center stays empty.

I'm checking which grid cells should be inked for a 0: the top and bottom middle cells light up, the left and right cells in the middle rows do too, and the center stays empty. For a 1, I'm thinking about a thin vertical stroke that lights up the center columns down the grid.

Now I'm sketching a template for digit 1: a vertical stroke that should sit in the middle columns, so I'm weighting columns 1 and 2 positively and penalizing the outer edges.

I'm checking the digit-1 template against how MNIST centers the strokes: a thin vertical line whose center of mass sits near column 14, so the ink should fall mostly in the two middle grid columns, with the outer columns empty.

I'm checking the digit-1 template against the grid: the stroke should fall mostly in the two middle columns, so I'll give those cells positive weight and keep the outer columns negative.

I'm checking the digit-1 template's column weights, and I'm reconsidering the weight on the edge-detector channels, which have no bias and so can go either way before ReLU filters them.

Now I'm double-checking that the filters are all float32, since the Gaussian is computed in float64 and needs converting before it goes into the weight arrays.

Next I'm checking whether the templates for similar digit pairs, like 0 and 8 or 3 and 5, overlap too much to separate well with this design.

Now I'm weighing whether the templates for digits like 4 and 9 overlap too much in the upper-right, and whether the hole detector can tell apart pairs such as 0 and 8, or 6 and 9.

I'm checking whether the logit gaps are big enough: with a correct class at 2 and others at 0, cross-entropy lands around 0.8. My FC weights are only about 0.15 per position, so the per-position contribution is roughly 0.3, and the net signal from the positive and negative positions still looks modest.

I'm checking whether the correct class's template matches the digit-0 feature map better than the others, since the logit gap depends on how different the templates are.

Now I'm working out the logit for class 0 by taking the feature values at each spatial position and multiplying them against the 0-template weights, scaled by 0.15.

I'm working out the logit for class 0 by summing the feature values against its template weights, which comes to 2.4 after scaling by 0.15. Next I'm starting the same calculation for class 1, using its column-based template.

I'm checking the logit gap for class 0 against class 1: the sums work out to 2.4 for the correct class and 0 for the other, so the margin looks large enough. Next I want to see how much the feature values drift from perfect template matching, and how much the other channels shift the result.

I'm weighing whether the negative weights on the center positions might push down the correct class for an unusual or poorly written 0, and I'll keep that in mind for tuning later. For now I'm going to write the step 1 code with the templates as they are.

Writing the first conv filter as a Gaussian ink detector, normalized and scaled by 1.5.

Still writing filter weights...

Still writing filter weights...

Still writing filter weights...

Still writing filter weights...

Still writing filter weights...

Still writing filter weights...

Still writing the remaining conv2 channel weights...

Still writing the FC layer helpers...

Still writing the digit 0 template weights...

Still writing filter weights...

Still writing the digit 2 and digit 3 templates...

Still writing the digit 5 template weights...

Still writing the digit 6 template weights...

Still writing the digit 7 template weights...

Still writing the digit 8 template weights...

Still writing the digit 9 template weights...

Still writing the return dictionary with the conv and FC weight arrays...

Checking the digit-0 case: ink on the sides and top and bottom should score high for class 0, while class 1 gets only a partial boost from its center column and loses some from its outer columns.

Still writing the digit-8 comparison...

Still working out the class 0 logit from the ink channel...

Now I'm checking the digit-0 case by hand: the ink feature map has strong values on the sides and top and bottom, weak values in the center, and the class-0 template should score high on that pattern.

Still working through the class 0 logit by hand, summing the ink feature values against the template weights.

Still writing the class 8 template weights...

Still working out the class 8 logit from the ink channel, summing the weighted feature values term by term.

Now I'm working through the class 0 logit from the hole channel, since the empty center of a zero should fire the hole detector.

Now I'm working out the class 8 hole logit from the same center positions, where the two holes should contribute more to the score.

Now I'm checking the hole pattern: the empty center of a zero is one large hole, but an 8 has two smaller holes stacked vertically, so the hole channel may not separate them cleanly on this 4x4 grid.

Checking the two logit totals for digits 0 and 8: they come out almost equal, 3.16 against 3.0, so a plain template split might not separate them on this grid. I'll accept that for step 1 and move on, and I'll check the first conv filter weights next.

Still working out the normalization for the first Gaussian filter, dividing each kernel entry by the total of 273 and scaling by 1.5.

Checking the conv1 edge filter's scale next, starting from the center weight and the bias.

Still writing the edge filter weights...

The edge filter's output after ReLU and pooling lands around 0.4 to 0.5, so the conv2 pass-through channel comes out near 2.0. Multiplied by the FC edge weight of 0.1, each matching position contributes about 0.2, which seems small. I'm considering whether to raise the edge weights in the FC layer or in the conv filters, but I'll first see how the full network behaves with the current values.

Still weighing whether to bake the digit detectors into conv2's channels or keep the FC layer doing the routing, since hand-designing 10 templates on a 4x4 grid across 16 channels is hard.

Now I'm thinking about the conv2 channels as digit detectors, with each channel firing for one digit, so the FC layer only has to route it to the matching class. For digit 0 that would mean reacting to horizontal edges at the top and bottom and vertical edges on the left side.

Now I'm wondering whether the conv2 digit detectors need to fire at one fixed spot, or everywhere on the 4x4 grid. A digit fills most of the image, so the detection probably belongs at every position rather than one location.

I'm checking whether conv2 can learn the spatial layout, and I see that its 5x5 window only catches local patterns. So the FC layer has to handle where those combinations appear, and that split is the approach I'll keep for step 1.

Now I'm checking the hole detector, since its ReLU means it only fires where the center is darker than the surround. That should mean channel 7 lights up only at the center of a zero, and stays near zero for a one, while an eight's two holes are still unresolved.

I'm weighing the hole detector against the digit templates: 0 versus 1 and 0 versus 6 should separate on holes, but 0 versus 8 is less clear. I'll keep this approach and finalize the code as is.

Still writing the function body and the final edge-based template refinements.

Adding edge features for a couple of digits now: a top-edge detector for the 7 and a bottom-edge detector for the 2.

Still writing the digit 1 edge detector and the digit 3 versus 5 templates.

Still writing the digit 4 and 9 comparison templates...

Now I'm comparing the digit 5 and digit 6 templates row by row, since their middle rows look almost the same. The clearest difference sits in the top row and the third row, where the ink placement shifts between the two.

Still writing the digit 5 and 6 comparison code, with the conv1 Gaussian ink filter being set up first.

Still writing the Gaussian ink filter and its bias, now setting up the top-edge filter with its positive upper rows and negative lower rows.

Still writing the conv1 edge filters, setting up the diagonal detector weights.

Still writing the hole detector filter, shaping its center weights to go negative so it responds to a dark middle surrounded by bright ink.

Still writing the conv2 setup and the center-weighted smoothing kernel.

Still writing the second conv layer's channel 9 weights...

Still writing the conv2 channel weights, now filling in the top-left and top-right corner detectors.

Still writing the remaining conv2 channel weights and the FC index mapping...

Still writing the digit 0 template in the FC layer.

Still writing the digit 1 template...

Still writing the digit 2 template...

Still writing the digit 2 bottom-edge template...

Still writing the digit 4 template...

Still writing the digit 5 template...

Still writing the digit 6 template...

Still writing the digit 7 template...

Still writing the digit 8 template...

Still writing the digit 9 template...

Still writing the return dictionary with the conv and FC weights...

Still writing the final return dictionary and the bias handling for conv2.

Wait, the conv2 weights are all non-negative and its inputs are too, so the ReLU after conv2 never clips anything, which means conv2 adds no real non-linearity.

I'm weighing whether a few corner channels in conv2 could help the FC layer tell digits apart, such as the junction in a 4 or the top-right turn in a 7. Since the conv2 weights are all non-negative, the network stays mostly linear, which may cap its capacity, but that's acceptable for a first attempt.

Still writing the corner features and the final shape checks for the layers.

Checking the rest of the verification list: the index math and shapes all line up. Now I'm wondering whether the MNIST digits, centered by center of mass, need any size adjustment, since a thin 1 and a wide 0 may fill the grid differently.

I'm working out how digit size and position affect the templates: a thin 1 occupies only a couple of columns of the grid, while a round 0 fills most of it.

I'm reconsidering the FC scale factor, since with s=0.2 the net logit margin for the correct class looks too small. The matching positions add up, but the negative ones pull it back down.

Now I'm checking the scores for digit 8 against the digit 0 pattern.

Now I'm checking the scores for digit 8 against the digit 0 pattern. Its ink is spread differently, though the overall shape is similar, so some positions match and some don't. Scaling the weights up to s=0.3 still leaves the probability modest, so the templates may simply be too close together.

Still writing the Gaussian filter code, now setting the scale factor and checking whether a higher value would sharpen the logit margin without blowing up the loss.

Still computing the Gaussian weights, now checking the values at the corners and center to estimate the kernel's total sum.

Still computing the Gaussian weights, normalizing the kernel so its center and corner values come out to roughly 0.24 and 0.004.

Still writing the digit 1 vertical-stroke template in channel 9.

Still writing the digit 1 and 7 vertical and horizontal stroke templates in the FC layer...

I'm estimating what accuracy this hand-built network might reach, guessing that the easier digits like 1, 7, and 0 will do well while 3, 5, 8, and 9 will struggle. That puts the overall figure around 55%, which isn't great but is a reasonable starting point. I'll aim for 50-60% on this step and then use the confusion matrix to guide the later refinements.

I'm now weighing whether to think about the network as a whole pipeline rather than layer by layer. The final 4x4 grid after the second pooling has fairly large receptive fields, so the FC layer is effectively taking a weighted sum over that grid to produce each class logit.

Still working on the FC templates, checking whether the digit 1 vertical stroke lands in the right column given center-of-mass centering.

Still working out the digit 1 template: the vertical stroke should land near the middle columns, so I'm putting positive weight on columns 1 and 2 and negative weight on the outer columns to keep it from looking like a digit 8.

Digit 1 has so little ink that plain ink-density templates may fail on it, so I'm considering a negative weight on overall ink to favor its thin stroke.

Still working on the digit 1 template, adding stronger negative weights on the outer columns so the thin center stroke stands out.

Digit 1 has little ink, so I'm adding a positive bias to its logit to offset the weaker ink-density signal. Digit 7 gets a smaller bias for the same reason. I'll hold the biases at zero for now and revisit them once I see the results. Next I need to check how PyTorch's cross-correlation convention affects the filter layout I've been designing.

Still writing the top-edge filter, checking how the weights line up with each row of the patch.

Checking the top-edge filter: ink above and background below gives a positive response, so it picks up top edges. The bottom-edge filter is just its negation, and the vertical-edge filter is the transpose, with the weights running from positive on the left to negative on the right.

Still writing the hole detector filter, a 5x5 pattern that is strongly negative at the center and positive around the rim.

Still writing the conv1 weights, starting with the Gaussian ink detector in channel 0.

Still writing the bottom-edge filter for channel 2, the negation of the top-edge pattern.

Still writing the conv1 filter weights, now the left and right edge detectors and the diagonal backslash pattern.

Still writing the conv1 hole-detector and the rest of the conv1 filter bank, and now setting up the conv2 weight array.

Still writing the conv2 weights, now setting up the smoothing kernel and copying each conv1 channel through to its matching conv2 channel.

Still writing the conv2 weights, now setting the vertical stroke channel and the four corner detectors.

Still writing the conv2 weights, now the bottom-right corner detector and the diagonal channels.

Still writing the FC template helper, now filling in the digit 0 templates from the ink and hole channels.

Still writing the digit 2 and 3 templates, now the curve-diagonal-bar pattern for ink density.

Still writing the FC templates for digits 3 through 6, now the right-arc and inverted-T patterns.

Still writing the digit 8 template in the FC layer...

Still writing the digit 8 and 9 templates, now the two-loop and top-loop patterns.

Still writing the FC edge features, now a top-row pattern for digit 7 and a vertical-edge template for digit 1.

Still writing the FC edge features, now adding a horizontal-stroke template for digit 4 in the middle rows.

Still writing the Gaussian ink detector in channel 0, normalizing it and setting its bias.

Still writing the conv1 diagonal backslash filter, the next rows of its weight array.

Still writing the hole detector filter weights for conv1 channel 7.

Still writing the conv2 pass-through weights, now the smoothing kernel and copying each conv1 channel into its matching conv2 slot.

Still writing the conv2 weights, now the horizontal and vertical stroke channels and the first corner detectors.

Still writing the conv2 pass-through weights, now the top-right and bottom-left corner detectors and the diagonal channels.

Still writing the digit 0 ink template in the FC layer.

Still writing the digit 3 template, filling in the ink-density weights for its rows.

Still writing the digit 4 and 5 templates, the ink-density weights for their rows.

Still writing the digit 7 through 9 ink templates in the FC layer.

Still writing the hole detector templates for the FC layer, now the digit 7 entry.

Still writing the FC edge features, now the hole-detector and edge templates for digits 7 through 9.

Still writing the FC edge features, now the top-edge and bottom-edge templates for digits 7 and 2.

Now I'm reviewing the final code submission for the hand-built MNIST network, checking the conv and FC layer shapes and dtypes.
