I'm at about 31.7% now, roughly plateaued in the 30-32% range with 7 steps left, so I need to pick a new strategy. The errors cluster on a few specific digits, and I suspect the coarse 4x4 pooled features are limiting what the readout can separate.

Wondering whether richer features, like position-sensitive density channels, could carry more information than the pooled 4x4 maps do. The 2 sink still shows up, and for low-ink 1s the logits look dominated by per-class bias terms, which may explain why 2 and 4 win there.

I'm weighing whether a bias-free matched filter, or simply checking whether the templates themselves are weak, would do better than more feature engineering. The confusions around 2 suggest the templates may be the real bottleneck, not the readout.

I'm thinking the class 2 template may be too heavy on the bottom row, since its strong base stroke overlaps with the bottom ink of 3, 5, 8 and 0, and the mean-calibration doesn't fully cancel that.

I'm now weighing whether 2's template is generic enough to attract ink from many digits, since it sinks even in formulations that differ from each other. The mean-calibration should offset that, but real images seem to carry more central ink than the template average implies.

I'm checking the template for digit 2 by summing its ink, which comes to about 7.3. That's one of the heaviest templates, along with 4 and 8, while 1 is much lighter. So for ink-heavy images the dot product with the 2 template will tend to come out large.

I'm considering whether to normalize all templates to the same total ink, so the 2, 0 and 8 templates stop dominating on sheer mass and the shape alone drives the match. That might cut the 2 sink without relying on the centring that already failed.

I'm going to try equal-norm templates with mean calibration, normalising each class's template so no digit gains an edge from sheer ink, and expect a modest gain at best.

I'm going to normalise each class's templates to equal energy across channels, rescaled to the average, so no digit gains from sheer ink, and then apply the mean calibration on top.

I'm now wondering whether scaling the class 1 template up would hurt on low-ink images, since its bias would become more negative and push 1 away from the very digit it should win. The scaling and the mean-calibration seem to interact, so I can't just equalise energy without checking that.

I'm going to test equal-energy templates next: scale each class's template so the total energy matches the average, then apply the same mean-calibrated readout as before. I'll compare the result against the 32.4% best from step 5.

I'm going to write the normalisation code next, scaling each class's templates to equal energy and then recomputing the mean-calibrated bias.
