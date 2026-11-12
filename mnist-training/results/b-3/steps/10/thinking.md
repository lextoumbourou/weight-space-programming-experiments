I'm trying to see why the number 8 keeps dominating the confusions. Working through the update rule for the case where t is 8, the sign flips, so the weight on 8 gets pushed toward T̂_8 each time, and that repeated push is probably what's inflating it.

I'm checking whether the update difference systematically favors 8, since T̂_8 is more spread out and so has a larger L1 norm than the other templates. That would give the mean-direction component a positive bias for 8 on ordinary ink, and it fits the fix I'm considering: projecting out the mean template direction from each difference and lowering η to 0.75.

I'm settling the base and bias handling: I'll leave the base U as in step 8, keeping its planned biases, since the 9 template change doesn't alter that plan. The projection would shift the base, so I won't apply it there. I'm also lowering the learning rate from 1.5 to 1.0, since 1.5 still looks too large.
