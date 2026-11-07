Step 24 with full anti-weighting favors the 3-vertex group (717 vs 468), while step 25 at half weight shifts toward the 5-vertex group (641 vs 578). Summing the two recalls, step 23 gives the best combined total at 1247, so I'm leaning toward it. I still need the 73.36 target by step 27.

I'm looking for a way past step 23's 73.27, since I need something above 73.36 by step 27 and a 73.77 by step 28. The next idea is to go back to step 23's setup and adjust the 7 template: the 7 recall is already around 785, and 7→9 and 7→4 are the main confusions. Adding anti-weight to the loop side of 9 might separate those two shapes.

Next I'm thinking about trying broader changes instead of more tweaks to step 23: lowering the conv1 detector bias for sparser features, raising sig_t, or switching to per-orientation Pearson centering. Each of those is a gamble. I'm also weighing whether dropping the ring to fill the grid with the spare channels is worth it, since the earlier ring-weight changes were confounded and I can't tell its value yet.

I'm weighing whether a larger ring detector would help with the 0s, since the 8-attractor and the 2/3/5 confusions look roughly balanced for now, and resolution doesn't seem to be the bottleneck given the 3-offset and 4-offset results were close.

I'm considering blurring the conv2 features with a cross-shaped kernel so small shifts matter less, and I'd need to blur the templates to match. It's a plausible gain of around 1%, though the effect isn't predictable.

I'm reasoning that the orientation pathway is linear once the conv1 ReLU and max-pool are applied, so blurring conv2 features is just a blur on the template weights, which is the same as increasing sig_t. That gives no new information, so I'll test sig_t at 3.6. Beyond that, only nonlinear features can get past a linear classifier on the pooled maps, which should reach around 95% on its own, and I'm still well short of that.

I'm going to try changing the 0 template next, since its recall of about 856 is low for a digit that's usually easy. Real 0s tend to be wider and slanted, so I'm considering widening it to rx 6, though 0s are currently confused mostly with 2, 8, and 9, and the 1 template has its own confusions with 4 and 6 that I'll look at after.

I'm going back to the step 23 setup and trying two changes at once: sig_t raised to 3.6 and the 0 template widened to rx 6.0. I'll use step 23's biases without the step 24 and 25 trims.
