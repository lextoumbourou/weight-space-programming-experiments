I'm working out a hand-designed CNN for MNIST with no training: two conv layers with ReLU and max-pooling, flattening to 256 features, then a final linear layer to 10 classes. Since there's no training data, the filters have to be built by hand to detect features, and the last layer has to map those features onto the digit classes.

I'm weighing a simpler route: keeping the conv layers near pass-through so the final 16x4x4 features act like a downsampled image, then writing the fc weights as digit templates.

I'm now sketching the conv1 filters: one channel as a plain blur that passes ink through, and the others left flat or also blurred. The idea is that after pooling, the features are a coarse downsampled view of the digit. I'm also considering how conv2 could be set up, though making all its channels blur the same input would waste capacity.

I'm now working through the receptive field of each final cell, tracing how a 2x2 block of the 8x8 map covers a 6x6 region of the 12x12 map.

I'm checking how far each final cell's receptive field reaches: roughly 16x16 of the 28x28 image, with the 4x4 grid tiling the picture at a stride of about 4 to 6 pixels. That's getting complicated, so I'll simplify and try a first version I can iterate on, using the loss and accuracy feedback I get over the steps.

I'm settling on conv1 with eight identical positive blur kernels and zero bias, so the nonnegative input passes through ReLU unchanged and the features stay a coarse downsampled view of the digit.

Every channel after the first conv step ends up carrying the same blurred, downsampled view of the digit, so the eight copies add nothing new. I'm considering having the second conv read only that single channel with a positive blur, which would leave the 16 final channels as near-copies of one coarse 4x4 image.

The 4x4 grid is too coarse to separate digits well, so I'd guess accuracy stays around 30 to 40 percent. What if conv2's 16 channels each sample a different offset inside the 5x5 window? Together with the 4x4 grid that could give up to 256 distinct samples, roughly a 16x16 view of the digit.

I'm now considering giving each of the 16 conv2 channels a delta kernel that picks out a different position in its 5x5 window, so each one samples the conv1 map at a different offset. Combined with the 4x4 grid, that could give a much finer sampling of the digit.

I'm now considering whether 16 conv2 channels picking different offsets in the 5x5 window would give a roughly 12x12 sampling of the digit, which is about 144 values against 256 features. Designing the exact delta kernels and their mapping looks intricate, and I can't test it offline, so I'll keep it pragmatic: conv1 as a blur, conv2 close to pass-through for coarse features, and digit templates in the fc layer.

I'm settling on the conv1 design: all eight channels as the same mean filter with zero bias, so the output is a plain local average of the ink. Then I'll work out exactly which feature index maps to which spatial position before I place any digit templates in the fc layer.

Working through the conv1 pipeline now: a 5x5 mean filter on the 28x28 input gives 24x24, then ReLU and 2x2 max-pooling bring it to 12x12. So each 12x12 value reflects the ink in a small patch around its corresponding location in the original digit.

Now I'm working out the conv2 delta kernels: each output channel picks one position in its 5x5 window on the first input channel, so the 12x12 map becomes an 8x8 output.

Each channel's offset (rc, sc) selects a 4x4 subgrid of the 12x12 map with stride 2, so changing the offsets across channels should cover different positions.

Each feature (c, u, v) samples the 12x12 map at roughly (rc+2u, sc+2v), so the fc weights can be set as a digit template read off those positions. What I still need is a coarse 12x12 template for each digit and the (rc, sc) offset assigned to each channel.

I'm picking offsets for the 16 channels, looking at which rows each one actually reaches under stride 2 and max-pooling, and noticing that rows 10 and 11 may be left out.

Now I'm assigning offsets to the 16 channels so that the rows and columns of the 12x12 map get covered by the pooled pairs.

I'm now assigning the 16 channels a grid of offsets, four row offsets times four column offsets, so each channel samples a different 4x4 subgrid of the 12x12 map. The one catch is that with this layout row 11 stays uncovered, which I'll accept as a minor gap.

I'm checking how the 20x20 digit box lines up with the 12x12 map, working out which original rows each pooled cell covers.

I'm mapping the 12x12 pooled map back to the original digit: each cell covers roughly a 5-pixel window, and the 20x20 digit box spans about rows 4 to 24, so the map covers the digit well apart from the last row. Next I'll define a 12x12 template for each digit and set each fc weight from the template value at the feature's sampled position.

I'm settling the fc weights by mapping each feature's sampled position in the 12x12 map, with the channel offsets covering rows and columns 0 through 9 through overlapping samples.

I'm setting the fc weights by sampling the templates at each feature's position, then centering each template so no digit gets an advantage from total ink. Next I'll draw a 12x12 ink pattern for each digit.

Now I'm drafting the 12x12 digit templates as ASCII grids, with ink marked as '#' and the glyphs sized to roughly 8 columns wide and 10 rows tall.

Now I'm drafting the 12x12 digit templates as ASCII grids, with ink marked as '#', and I'm weighing whether a simpler mapping would be less error-prone than the offset scheme.

Setting the conv1 weights as a uniform 5x5 mean filter, and conv2 as single-tap delta kernels that pick one position per channel, so I'll check the indexing and zero the biases next.

I'm scaling the fc weights with a global factor, since 256 terms of roughly 0.3 times weights near ±0.5 could push the logits high enough to affect the softmax loss. I'll start with a moderate scale and tune it from feedback.

I'm reconsidering the scale of the fc weights, since 256 features each around 0.3 could push the logits too high. I'll start with a moderate global factor and adjust it once I see how the loss behaves.

Writing digit templates as 12x12 ASCII grids...

Writing digit templates...

Writing digit templates...

Writing digit templates...

Setting the fc weights as a scaled, centered version of each digit template, starting with a scale around 3 and tuning it from the loss.

Writing digit templates as 12x12 grids...

Now I'm checking how the 12x12 map lines up with the digit: M1 index p sits near original row 2p+2.5, so the digit's rows fall roughly within M1 rows 1 through 10, and my templates cover rows 1 to 9. The feature row index r = ro + 2u stays between 0 and 9, inside the map.

Still writing the weight-setup code...

Still setting the fc weights from the centered templates, with the scale chosen from the expected range of the pooled features.

Working out the logit magnitudes: roughly 50 ink-aligned features contribute about 20·scale to the correct class, while the background adds only a small negative amount, so the margin is about 9·scale over wrong classes. For a usable softmax that suggests a scale near 0.3.

Weighing whether scale near 0.3 is the right starting point, since the absolute logit level matters for the loss even though softmax only uses the differences between classes.

Writing the code to build the weights now.
