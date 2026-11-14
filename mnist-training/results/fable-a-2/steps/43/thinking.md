Validation is at 89.04% with loss down to 0.3713, a drop of 0.033 this cycle, which is a bit better than I expected. Cycles have been gaining roughly 0.02 to 0.03 each, so probing still looks worthwhile. With 8 steps left, I'm weighing two more probing cycles against saving a couple of steps for tuning, and I don't yet know how much tuning will give.

I'm weighing two more probing cycles (43–48) followed by two tuning steps, a scale test and a final one. A scale change might get a bit more from a single step, so I'm considering whether the current scale is too high or too low, though I can't tell yet. I'm planning the order of the remaining steps, with the classifier runs at 45 and 48 and a scale test at 49.

I'm listing which single-row cells for the vertical, forward-slash and backslash features are still unmeasured, including the missing right-side and centre-column variants. The centre-column regions overlap the left and right halves, so they could help separate the column-level patterns. I'm also noting the three remaining errors from step 42: 9→7, 7→9 and 0→2.

I'm looking at the remaining confusions, where 7 and 9 are the worst pair, and asking which cell-level feature separates them. A 9 keeps its stem on the right through the middle rows, while a 7's stem angles down toward the centre-left, so I'm considering a vertical or slash feature at the middle rows to tell them apart.

I'm checking whether the 7 and 9 confusion can be separated by a column-level feature, since a 7's stem sits on the right at row 2 just as a 9's does, so the row-2 features don't help much on their own.

I'm sorting out which features might separate the 1s that get read as 2s, since slanted 1s pick up diagonal energy. The remaining errors look like mostly atypical samples that are hard to fix linearly. I'll keep probing and include a vertical feature at the bottom-right cell, plus a backslash feature there.

I'm weighing which of the remaining unmeasured cells might separate the classes: the bottom-right vertical cell looks like it could vary between 9, 4 and 7, while the bottom-right backslash and top-right slash seem less likely to help.

I'm considering a few more single-row features for the vertical and forward-slash cells, such as the right side of the top row for the forward slash, since some digits lean that way. I'm also thinking about finer splits of the top and bottom features, which have been strong class signatures so far.

I'm weighing whether to spend the remaining steps on more probing or on tuning the scale, since the probing gains have been steady but I can't yet estimate how much tuning would help.

I'm weighing a tempering change to the line-term weight, since the current product with scale is 0.24 and a different value might lower the loss by a hundredth or two. I want to try a scale test at 0.34 first to see which direction helps, then decide whether to spend the next steps on probing or on tuning.

I'm weighing whether the scale should go down or up. Loss fell each time I reduced it while adding features, but the line terms have roughly doubled in magnitude, so the classifier may now be overconfident.

I'm guessing the best scale is lower than the current value, around 0.3, so I'll test 0.33 next.
