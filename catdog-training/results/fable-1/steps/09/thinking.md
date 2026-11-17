Most images seem to give a value above zero for the difference between the diagonal response and the average of the horizontal and vertical ones, so the offset is less negative than I'd guessed. That makes the diagonal response roughly equal to or larger than the average of the other two. The diagonal channels respond about equally, so I'll work with their mean difference from the average of the horizontal and vertical ones.

Working through the loss expansion, the quadratic term suggests the offset is roughly zero-mean with a small spread, so the diagonal contrast looks negligible and I'll set it aside for now. Next I'm setting up the combined terms: the top channel with weight 1.2, the vertical-minus-horizontal contrast at weight 3.5 with its mean of about 0.023 subtracted out, and the green term at weight 2.5.

I'm combining the terms now: the top channel, the vertical-minus-horizontal contrast, and the green one, each centered on its mean. That gives an expected loss around 0.66, and rewriting the diagonal in terms of H and V, the combined score reduces to about −2.3H + 4.

Running the combined model next to get a baseline, with the bias set to about −1.60 from the centered means of the top channel, the vertical-minus-horizontal contrast, and the green term. After that I'll adjust the coefficient ratio one piece at a time alongside the new probes.
