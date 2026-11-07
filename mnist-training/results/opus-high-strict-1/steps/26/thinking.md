The penalties look too strong for classes 8 and 9, which have been hit by several at once: 9 got three and 8 got two. Other classes improved a lot, while 8 (212) and 9 (267) got crushed. I'll try a smaller GAMMA of 0.08 and normalize the total penalty per target class.

I'm weighing a bias fix alongside the smaller penalty, since lowering b's logits on average might be pulling 8 and 9 down. Using γ=0.25 as a reference, 8 and 9 lost far more than the other classes gained, and a smaller γ should keep those gains while limiting the collapse. The target is at least 77.77 on this step, so I need the penalty on 8 and 9 to stay small.

I'm weighing a bias boost for classes 8 and 9, since their column sums are far below target, but the size of that correction is hard to pin down. With the deadline close, reverting to the step 23 network with small tweaks seems the safer fallback, though it may not clear 77.77. A smaller penalty with a modest bias boost for 8 and 9 looks like the more promising bet.

I'm weighing a smaller penalty, around γ=0.1, against the risk that the 8s and 9s get crushed the same way again. At γ=0.25 the penalties on 9 stack up heavily from several classes, so I'm adding a small bias compensation for classes 8 and 9.

I'm settling on a per-class normalization: dividing the penalty by the number of pairs hitting each target class, so 9 (three pairs) gets scaled down the most. With GAMMA at 0.12, the penalty norm per class caps around 0.36 if the signatures line up, and that applies to 5, 3, 6, 4 and 8 as well, leaving only class 0 untouched.

I'm considering a small adjustment to the biases for classes 0, 2, and 7 to offset the per-class penalty, since 7's column is already high. Classes 1 and 2 get small reductions too, with the bias for 7 coming down the most.
