I'm at 75.1% accuracy with a loss of 0.8148, the best so far, so I'll keep going. The biggest remaining confusions are 2→3, 3→5, and 7→9. Right now I'm comparing 2 and 3: 2 has a bottom-left corner with a horizontal base running right, while 3 has a bottom curve that returns left, and I'm starting to look for an endpoint feature that separates them.

I'm weighing whether the bottom endpoints could separate 2 from 3, since 2's base ends at the right edge while 3's ends further left. I'm also wondering if a corner detector is worth the complexity, but it seems like too much. Another idea is to lower the weight of the ink features, since ink looks similar across digits, so I'll try scaling those down to 0.6×.

Now I'm recalibrating the per-class bias with a 1.5 factor, using the column sums from step 29 to compare true and predicted counts for each digit. The first few adjustments are small: class 0 comes out slightly over-predicted, while class 1 looks more over-predicted, and class 2 is close to balanced.

I'm recalibrating the per-class biases after the ink reweighting, since that changes the penalty terms and shifts the corrections, so I'll recompute them from the new values.

I'm weighing whether to accept the risk of the ink reweighting shifting the class balance, since it's just an experiment I can revert if it hurts. I have 21 steps left, so I'll go ahead with it.
