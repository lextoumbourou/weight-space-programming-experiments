I'm going to design this CNN by hand for MNIST, with no training. The architecture is set: two conv layers with ReLU and max pooling, then a fully connected layer down to 10 outputs. The plan is to make the first conv layer pick up oriented edges and strokes, and the second build on those.

I'm weighing whether the fully connected layer can do real template matching on a 4x4 map, since pooling takes the image down that far. A near-identity blur would keep the spatial layout but leave only 4x4 resolution, which seems too coarse to separate digits well. Edge-style features in the first layer might carry more useful structure into the final 256 values.

I'm concluding that the fully connected layer only sees a 4x4 grid per channel, so any discrimination has to come from which of the 16 conv2 channels fire in which cells. I'm considering whether to go for a modest 40-60% accuracy target rather than aiming higher, and I'm leaning toward a cruder but more robust design.

I'm settling on a simpler scheme: conv1 channel 0 becomes an averaging filter that measures local ink density, and conv2 pools that into a coarse 4x4 ink map that shows where the strokes sit.

I'm working out the coordinate mapping now: a 28x28 input becomes 24x24 after the 5x5 valid convolution, and each output position covers a 5x5 patch of input rows and columns.

I'm mapping how the receptive fields line up: each final 4x4 cell covers roughly a 7x7 patch of the 28x28 input, so the 16 cells tile the digit into coarse regions. Rather than chase fine edges, I'll have conv1 channel 0 be an all-ones 5x5 sum to measure local ink, and let the later layers average that into regional ink levels.

Now I'm checking whether the second conv layer can just pass along the same ink map on all sixteen channels, which would make them redundant, though the fully connected layer can still read them as a 4x4 ink map.

I'm noting that the fully connected layer just sees 16 channels of the same 4x4 map, so the extra channels add nothing new. I'll treat it as a 16-value template-matching problem and start sketching 4x4 ink patterns for each digit, beginning with a ring-shaped pattern for 0.

I'm sketching 4x4 ink templates for the digits, starting with a hollow ring for 0 and a vertical bar for 1. Those coarse patterns will overlap a lot, so I'll check how the cross-entropy loss and accuracy respond before refining them.

Scaling the conv weights down to averages keeps every feature in [0, 1], so the fc logits stay in a range where a few units of difference are enough. Next I'm setting the fc weights so each digit's template contributes to its logit in a comparable way.

Now I'm working out the scaling: each template becomes a 4x4 pattern of -1 and +1 values, spread evenly over the 16 channels, so the logit for each digit is just a scaled dot product with the ink map. I'll pick the scale so the logits spread across a few units, then tune it.

I'm settling on the ink-density approach: conv1 channel 0 is a plain averaging filter, and conv2 produces copies of that map, so the fully connected layer is effectively matching hand-drawn 4x4 digit templates.

I'm wondering whether conv1 could also carry edge detectors in its other channels to help later steps, but I'll keep step 1 simple. All 16 conv2 channels will simply copy the ink density map, and the templates get designed on top of that. Pooling caps the fully connected layer at a 4x4 grid, so the 8x8 detail never reaches it directly, and I'm wondering whether the 16 channels could encode finer position information instead.

I'm wondering whether conv1 could keep full resolution at 24x24 and pool down to a 12x12 ink map, which would be finer than the 4x4 grid. The problem is that conv2 and its pooling still bring it back to 4x4, so the fully connected layer only ever sees a coarse grid. I'll go ahead with the 4x4 template approach for now and adjust based on the feedback I get.

Each conv2 channel is a copy of the same ink map, so the sixteen channels only give me a 4x4 grid of coarse density values. The next thought is to make the 16 channels carry different stroke orientations instead, so each cell has a small descriptor of local edge direction, similar to HOG at that resolution. I'm going to accept the 4x4 limit and see whether that orientation information is enough to separate the digits.

I'm settling on oriented edge detectors in conv1, pooled into eight orientation maps. Then I'll design conv2 so each output channel averages one orientation over its 5x5 window, which gives a density per orientation across the 4x4 grid.

I'm going to fix the conv1 setup for the ink-density baseline: channel 0 gets uniform 1/25 weights to average the input, the other seven channels stay zero, and the bias is zero.

Now I'm setting conv2 to the same scheme: each of its 16 output channels averages the pooled ink map over a 5x5 window, which keeps all of them identical at 4x4. I'm also working out how the flattened 256-value vector is indexed, so the fc weights can be placed correctly per channel and cell.

I'm setting the fc weights for each digit so its logit is a scaled dot product with the 4x4 ink map, spreading the template evenly across the 16 identical channels. Next I'm working out what the 4x4 ink distribution looks like for each digit, since the digit fills roughly the central 20x20 region.

I'm sketching the 4x4 ink patterns for each digit, starting with a hollow ring for 0 that has heavy ink on the border cells and little in the middle. For 1 I'm picturing a thin vertical bar down the center-right columns.

I'm setting the templates up as expected ink patterns on a 0-2 scale, then subtracting the mean across digits so the logits depend on shape rather than total ink. I'll rely on the confusion matrix feedback to tune them.

I'm settling on the 4x4 ink templates for each digit, scoring the 0 pattern as a ring with heavy ink on the border cells and light ink in the middle. For 1 I'm picturing a thin vertical bar down the center columns, and I'll set the remaining digit templates the same way before centering them around 0.5.

Now I'm writing out the 4x4 ink patterns for the remaining digits, the same way as before.

Still writing the 4x4 ink templates, adding the digit 6 pattern with its left curve and bottom loop, then 7, 8, and starting 9.

Now I'm working out the 4x4 ink map for the digit 9, as a loop up top with a heavier right side. I'll center the templates by subtracting the average across digits so shared ink cancels out, then scale the result.

Setting the scale near 15 so the logits separate, since the dot products over the 4x4 templates will be small at first. I'll use feedback to adjust it, and then start writing the code for the flattened feature layout.

Writing the flattened index math and the code for the fc weights now...

Setting the logit scale to 12 and writing out the code for the fc weights now...
