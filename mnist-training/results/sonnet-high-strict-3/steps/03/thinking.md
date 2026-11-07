The predictions keep collapsing onto classes 2, 5, and 8, and the loss sitting around 2.20 suggests they barely track the input. I'm wondering whether the features are behaving differently than I assumed, since the same few classes win almost everywhere while 0, 1, 6, and 9 never win at all.

I'm suspecting the bias comes from the per-class sums of weights over features that are usually active, so classes whose rows lean positive on those features win by default. Without knowing the mean feature values, I'd need to make each class's weights zero-sum across cells per channel to cancel that offset.

I'm considering a fix for the bias: setting the conv2 biases negative so the ReLU only fires on strong evidence, which should keep features sparse with a near-zero baseline. I'd have to guess the typical activation level, though, since I don't know it. I'm also weighing a per-class, per-channel zero-sum constraint across cells as a complement, but I'm not sure either idea will be enough on its own.

I'm weighing a simpler design: matching ink against coarse per-class templates, with each template summing to zero across cells so uniform ink adds no offset. Zeroing each class's weights across cells would also erase the negative evidence some classes depend on, so I'm considering a different global correction to the per-class offsets, though I don't yet have a way to estimate them without the confusion-matrix feedback.

I'm considering whether to nudge the fc biases directly, lowering them for the over-predicted classes 2 and 5 and raising them for the ones that never win, using the confusion counts as feedback. The logit scale is small, so the shifts would need to be modest, but tuning blind over many steps would be slow. I'm leaning toward combining that with a more neutral weight structure instead of relying on either alone.

I'm going to bias the conv2 channels slightly negative so their features stay near zero on weak evidence, and add a half-strength per-class centering across cells, scaling the weights up a bit from 1.5 to 2.5.

I'm checking whether the ring detector is even the right size for the holes it needs to catch: a 0's hole is around 8 to 10 pixels across, so a radius-2 ring mostly fires on small loops in 8, 6, 9, and 4, which would explain why 0 never wins. A larger-scale hole cue built from conv2 over the edge channels might fix that.

I'm sketching a loop detector at a larger scale: a conv2 channel that needs horizontal strokes above and below plus vertical strokes on both sides, with a strongly negative bias so all four must be present. That would catch a zero's roughly 8 to 10 pixel hole, and I'm considering using the blob density at the four sides instead of the orientation features.

I'm going to build the loop detector on the blob channel instead, with weights placed on a ring of border positions and negative weights in the center, so it responds to a hole at roughly the right scale. The worry is that a ring of radius 2 on the pooled grid only spans about 8 pixels, which is on the small side for a zero's hole, but it may be workable.

I'm settling on two loop detectors at different scales: a larger ring of radius 2 for bigger holes like a zero's, and a smaller ring of radius 1 for tighter loops. Both would sit on the blob channel with a slightly negative bias, and I'm scaling the blob response up to roughly 1.2 on a full ring.

I'm settling the hole detection on a ring of blob features at two radii, one for larger holes and one for smaller ones, with a slightly negative bias so the features stay quiet on weak evidence.

I'm going with a slight negative bias on the conv2 channels, around -0.15, and a partial per-cell centering on the fc weights, and I'm raising the fc scale to 3.
