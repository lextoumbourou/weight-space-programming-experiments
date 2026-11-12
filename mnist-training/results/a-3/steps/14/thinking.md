I've hit a plateau, so I need a bigger change rather than tweaks. One option is to have conv2 learn mid-level part detectors like open curves, loops, or endpoints, though that's hard to do. Another is a hybrid with a higher-resolution pure ink representation, and I'm weighing that against the others. The third is to improve the fc classification by understanding it better.

I'm weighing whether to hand-tune the pairwise discriminants for the confusable digits, like 2 versus 8, but the naive Bayes setup already captures much of that. Using the confusion matrix to refine the templates is only a coarse signal. The bigger issue is the features themselves: each 4x4 window with the blur spans about 12 pixels of a 20-pixel digit, which is far too non-local, and the max-pooled presence values may be too binary to separate digits.

I'm working out a finer feature layout: four cardinal edge directions sampled on two offset grids, with small windows, so the features become much more local. Folding the diagonal responses into the cardinal channels in conv2 would fit the 16-channel budget.

I'm settling on sampling the four cardinal edge directions with a diagonal blend, so the diagonal responses fold into the nearest cardinal channel. I'm also checking the tap offsets, since the candidate windows leave gaps in the rows around 4 and 5, so I'm trying a different tap offset to close them.

I'm checking where the tap offsets land: with t=1 the windows cover rows 4 to 19, and t=2 covers 6 to 21. Together they span 4 to 21, which leaves the bottom edge near row 22 still to account for.

I'm checking the tap offsets for the bottom edge: t=1 and t=2 together cover centers 4 through 21, which seems enough given the strokes end around row 23. I'm considering a small blur with narrow membership windows around each center, and then weighing a 256-feature layout of four cardinal directions across 64 positions, which would act like an 8x8 gradient-direction histogram.

Working out the template math now: each direction channel gets tuned by a simple cosine of the angle difference, and the saturating response uses a fixed scale with sigma around 1.8. I'm weighing whether the naive Bayes setup should keep its usual smoothing, and whether the bias terms should be reset to zero, since the features have changed so much that the old offsets probably no longer make sense.

I'm settling the channel layout as four cardinal directions times a 2x2 tap grid, so channel index is 4·D + 2a + b with row and column taps at 1+a and 1+b. That puts the window centers at 4r+5.5+2a, which covers rows 4 through 21 evenly. I'm also deciding whether to halve the current biases rather than reset them, since the old pattern still partly reflects the template shapes.

Next I'm fixing the conv1 direction indices: the four cardinal channels sit at 0, 2, 4, and 6, and each conv2 direction pulls its own conv1 channel at full weight plus its two neighbours at half weight.
