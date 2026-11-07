Progress has been slow, so I need a bigger structural idea. The limit seems to be a linear template working on coarse oriented-presence features, and the conv1 bias of -0.2 might be keeping the line-filter activations weak under the ReLU threshold. I'm considering features aimed at the commonly confused pairs instead, such as 1 vs 7, 4 vs 9, 7 vs 9, and 2 vs 4.

I'm considering a hole detector: a conv2 filter that fires when the center of a region is empty but ink surrounds it, which would pick out 0, 6, 8, 9 and sometimes 4 and 2. I'd swap the two uniform channels for these detectors, possibly at two sizes, using the blob channel as input.

I'm sizing a hole detector against digit loops: a ring of positive weights at about 4px radius around a negative center, which should respond strongly to closed loops and weakly to a plain stroke passing through.

I'm settling the bias for the hole detector: with a ring of +0.05 and a center of -0.1, a closed loop comes out around 0.64 while a straight stroke stays at or below zero, so a bias near -0.25 to -0.3 separates them. Then I'm planning the fully connected template for the hole channel as Gaussian blobs at the hole centers I expect for each digit.

I'm now weighing a second hole-channel option: a smaller ring at offset 1 for tiny loops, which I'll set aside as less useful. I'll keep the larger ring for channel 7 and leave channel 15 as the broad uniform channel. Next is the hole-channel template, which I'm just starting to set up.

I'm settling the hole-channel weight scale, leaning toward about 1.5 times the base scale since the hole feature is strongly discriminative, and I'm also setting the template's Gaussian sigma to 3.0. I'm keeping the existing biases mostly as they are, and I'm recomputing the column sums to check the balance across digit classes.

I'm checking the per-digit column sums for balance, and they look roughly even, so I'll leave the biases where they are. The hole channel will shift things, but I'm not changing biases beyond a small tweak on channel 7. Next I'm setting up the weight matrix for channel 7 by zeroing its ring entries.

Now I'm zeroing out the ring weights for channel 7 and setting a larger ring around a negative center. Next I'm building a hole template from the per-digit hole centers, using Gaussian blobs, then centering it across classes and normalizing it.
