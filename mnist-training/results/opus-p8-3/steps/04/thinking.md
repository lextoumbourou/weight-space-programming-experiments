The model went up in accuracy but its loss went up a little too, since it's now confidently wrong on some digits. I need a bigger jump than tweaking templates, so I'm considering more principled discriminative features in place of hand-drawn ones. Even so, a linear classifier on coarse oriented-stroke features probably tops out around 95%, which suggests my hand-designed templates are far from what's achievable. One specific failure stands out: a 1 is being classified as a 7 (sample 160).

I'm checking the remaining confusions, like 7 being read as 2 and the 6 and 4 mix-ups. I'm wondering whether averaging the template variants is diluting the signal, so that a 1 gets a weak score against its own template and loses to 7. I'm also weighing whether normalizing each template to equal norm, or subtracting a shared mean, would change the outcome.

I'm noting that a linear classifier on these features probably caps out near 95%, so the real gap is in my template weights rather than the features themselves. Raw-pixel nearest-mean gets roughly 82% and a linear model on raw pixels around 92%, which suggests better estimates of the class means are what would help, and a finer spatial grid might too.

I'm now asking whether the 4x4 grid itself is the limit, and whether finer sub-cell information could come from conv2 taps at shifted offsets inside each cell.

I'm working out how a finer ink grid could come from conv2 taps at offsets (1,1), (1,3), (3,1), (3,3) and (2,2), which would give roughly an 8x8 view inside the 4x4 layout. A nearest-class-mean on that finer map would probably land around 80%, so guessing won't close the gap. I'm considering whether topology features, like loops in 0, 6, 8 and 9 or endpoints, could be captured in two conv layers.

I'm weighing whether to tune the templates iteratively against the confusion feedback, since calibration matters for the lowest validation loss. I'm also considering whether blurring the templates would add invariance, and whether the scale of the features relative to the templates, or stray responses from curved strokes, is the real source of the misfit. Next I want to try giving each class separate evidence-for and evidence-against weights.

I'm noting that the template scores already reduce to a shared term plus per-class scaling, so the only real levers are each template's per-feature weights and the class biases. The features that tell a 1 from a 7 should carry the most weight, starting with the top horizontal bar that a 1 lacks, and I'm checking how a 7 input scores against that bar.

I'm thinking that a mixture of template variants would need a max over variants rather than a single linear score, which a linear model can't express directly. Maybe conv2 channels could act as class-like detectors that handle the variants separately.

I'm considering whether a finer grid of ink samples could come from conv2 taps at shifted offsets. Broader, coarser orientation tuning might also make slanted 1s look more alike, since slant would show up as a shift in the orientation mix rather than a new shape. Then I'll think about what the actual MNIST class means look like to guide the estimates.

I'm estimating the class means from memory, since MNIST digits are size-normalized to a 20x20 box and then centered by mass. That centering shifts a 7 downward, because its mass sits high, which would throw off my fixed templates for it. I'm wondering whether the coordinate placement of my templates, rather than the orientation weights, is the bigger source of error.

I'm checking how the digit's mass sits in the box, since the centering shifts things like 9 and 6, and then I'll use the per-class confusion counts to set the biases instead of guessing at the templates.

Counting the predicted labels per class, the 6 column is far too large at 1526, while 4 and 8 come out low at 582 and 502.

I'm weighing whether blurring the conv2 taps would make the template matches less brittle, and whether lowering the scale factor would bring the loss down, since the model may be more or less confident than its accuracy suggests.

I'm considering whether a bigger loss factor would help, but changing several things at once would muddy the results, so I'll try one variable at a time. A structural change seems more worthwhile early on, so I'm sketching conv2 channels that add shifted ink taps for finer spatial detail and reserve some channels for orientations at offset taps.

I'm thinking about adding a 3x3 blur in conv2 so the features are smoother and less brittle against misplaced templates, and I'll fold in bias adjustments from the confusion counts afterward.

I'm weighing a 3x3 blur in conv2 and per-class bias corrections from the confusion counts, and I'm checking whether the ink channel is double-counting what the orientation channels already capture. For the 7-to-2 confusions, the key difference looks like the bottom bar a 2 has and a 7 lacks, so I'm looking at how the template's stem and top bar sit against that.

I'm checking whether the 7-to-2 confusions come from my 7 template's stem ending too far left, and I'm weighing whether to just nudge per-class biases instead, with small increases for 4, 8 and 5 and a decrease for 6.

Next I'm weighing a per-class bias shift of about -0.3 for 6 and -0.2 for 0 and 9, leaving 7 alone despite its confusions with 1 and 2. I'm also considering a normalized 3x3 blur in conv2 with the center at 0.5 and the neighbors at 0.125, so thin lines lose some peak strength, and I'm weighing whether to keep beta at 0.6 rather than change it at the same time.

I'm dropping the blur idea in conv2 and keeping the rest of the setup as it is, so I can see how sensitive the results are to bias changes. Next I'm working out the per-class bias deltas from the confusion counts.

I'm setting the per-class bias offsets directly: lowering 0 by 0.3, 6 by 0.5 and 9 by 0.2, raising 4 by 0.5, 5 by 0.3 and 8 by 0.6, and leaving 1, 2, 3 and 7 unchanged.
