The loss rose after scaling the ends up by 25%, so the end votes seem over-weighted and the gradient points toward reducing them. Since that step cost a noticeable jump in loss, I'll try scaling the ends down by 0.8 instead, giving sE = 0.64 and sD = 0.48. The biases were tuned at the old setting, so I'll need to account for that when I change the end weights.

Scaling the ends down would shift class balance, since the end votes currently favor certain classes and the bias for class 9 was tuned to that. Lowering the ends would likely help 9, 0, 6, and 8, so that bias might overshoot. The earlier loss jump seems partly due to this bias mismatch, so the bias and scale are tied together. With about nine steps left, each candidate step, from scaling the ends to adjusting the heads or biases, probably gains only a small amount of loss.

I'm considering whether there's a bigger win left with nine steps to go. Class-pair bias adjustments aren't feasible, so I'm looking at per-class feature weights for class 8, which has the worst accuracy and its main confusions with 5 and 3. Without new evidence about those features, though, I don't see a clear way to strengthen them.

I'm weighing whether to scale the end votes down to 0.85, which would set sE to 0.68 and sD to 0.51 while keeping the biases fixed. I'm also wondering if the diagonal groups at 0.6 are part of the problem, since they seemed to hurt classes 8 and 9 earlier, and whether sE at 0.8 is too high.

I'm considering testing sE back at 0.6 with sD at 0.6, since raising sE to 0.8 came with a bias retune and its own effect is unclear. If the result improves, that would suggest sE is over-weighted. I'll keep the biases fixed for this run so the comparison stays clean, though the result will be somewhat confounded.
