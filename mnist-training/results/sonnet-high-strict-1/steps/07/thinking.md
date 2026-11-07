The bias tuning has plateaued around 55%, so the real limit seems to be the features and templates rather than the weights. I'm checking whether the bias on column 8 is too high, and I'm considering scaling it back. I'm starting to think a linear classifier on coarse 4x4 features with hand-made templates is simply too weak, so I'm looking at a different feature strategy, such as stroke-position templates.

I'm wondering whether the spatial mapping of the 4x4 cells is off, since the pooled centers may not line up with the true pixel positions. I'm also weighing narrower conv2 kernels for sharper resolution, and building discriminative templates that subtract the other digits' ink rather than relying on hand-drawn prototypes.

I'm checking whether the pooled cell centers line up with the actual digit geometry, since the max-pool picks from a narrow range and the broad kernels blur things by several pixels. The offset looks around a pixel at most, so I'm weighing whether shifting the template centers to 7.5 + 4i would be enough to correct it.

I'm thinking about whether a narrower conv2 kernel, a 1x1 centered on each pooled position, would give better position acuity, so the 4x4 pooling covers tighter pixel spans.

I'm checking the cell centers against the pooling spans: with the narrower kernel, each pooled cell seems to cover about 4i+4 to 4i+13, which puts the centers slightly off the image middle.

I'm checking the pooled cell geometry with a narrower conv2 kernel: the 4x4 cells would cover roughly 4i+4 to 4i+13 pixels, with centers near 8.5, 12.5, 16.5, and 20.5, which sits slightly off the digit's middle.

I'm rechecking the pooled cell centers, and with a 3x3 kernel the mean of the two pooled positions lands at 4i+7.5, so the centers sit at 7.5+4i rather than the 4i+7 I had earlier.

I'm checking the narrow-channel geometry again: the pooled cells should sit around 7+4i in index coordinates, which is the same as before. The narrow features give sharper position, so the sigma for those templates could drop to about 2.5 instead of 3. Since the max over two positions gives a stroke-presence signal per cell, I'm considering weighting the narrow channels more heavily and leaning less on the broad ones, which might lift accuracy from roughly 55% toward 70%.

I'm considering whether tolerating a slight rightward slant in the templates would help, and I'm weighing the bias on class 8, which seems to be pulling in too many digits. Scaling it back toward a small value looks necessary, since the logits are very sensitive to even modest changes there.

I'm going to tune the bias on class 8 down to around 0.2, since going from 0 to 0.5 swung its predictions from about 342 to 1880. Then I'll check the per-class prediction counts, where 9 looks underpredicted and needs its bias pulled back toward -0.5.

I'm adjusting the per-class biases from the prediction counts: pulling class 8 down to 0.2, class 9 up to about -0.55, and nudging several others. I'm also considering a structural change, raising the narrow-channel weight to 1.0 and dropping its sigma to 2.5, since the plateau suggests the features need to change, not just the biases.
