The model is stuck at 36% and the biases barely moved the predictions for 6 through 9. I'm noticing that class 5 keeps absorbing errors from many other digits, while class 1 is still classified correctly, so the problem looks like it's in the templates rather than the bias terms.

I'm weighing whether the template features are the real limit, since the 4x4 occupancy templates are rough and the 16 channels all act like total ink. I'm considering better stroke layouts or richer conv2 features, and I'm leaning toward returning to an orientation grouping that avoids the earlier bias and centering failures.

I'm trying a different centering scheme for the templates, making each class's weights sum to zero within each channel group, so that dense digits like 8 and 0 stop winning just by having more ink. Step 4's all-entries centering reached only 27%, so this may not be enough alone, but it's worth testing before I give up on orientation grouping.

I'm weighing a more careful design of the templates for the worst confusers, since 4 against 9, 3 against 2, 5, and 7, and 8 keep bleeding into each other. The 4x4 grid over the centred 20x20 digit box may simply be too coarse to separate them, since cells are about 7px and a 4 and a 9 differ mainly in the top-left region.

I'm checking the receptive field of the final cells: stacking the conv and pool layers gives about 16px per cell at an 8px stride. That means each cell overlaps heavily with its neighbours, so the 4x4 grid over the 20px digit box only gives roughly two effective positions per dimension, which is far too coarse to separate a 4 from a 9.

The receptive field of each final cell is about 16px with an 8px stride, so the 4x4 grid only gives roughly two effective positions per digit dimension. That resolution is probably the real ceiling, which puts a hand-built template classifier somewhere around 50-60%, so getting past 36% depends on making the templates work well on this coarse grid.

I'm working out the spatial grid: with 16px receptive fields at an 8px stride, the cell centres land around 8, 16, 24, and the last cell hangs past the edge of the 28px image, which doesn't quite fit a 4x4 layout.

I'm noticing that the 4x4 grid only really covers three cell positions per dimension, since the digit's ink sits within roughly x and y 4 to 24, so the outermost row and column mostly catch digit tips. That means the templates' fourth row and column are carrying little real information, and the structure I put there, like the bottom bar of a 2, will probably land in the edge cells instead of the ones that see it.

I'm checking which rows of the template actually receive digit ink: rows 0 through 2 see the digit, while row 3 mostly catches only the edge. So the bottom bar of a 2 belongs in row 2, and the templates' fourth row is contributing little beyond a constant offset.

I'm checking how the 4x4 grid maps onto the actual digit area, and whether the row and column that sit at the edge carry any real signal. The next step is to see whether the receptive fields of the conv2 channels make each cell encode more than just a coarse occupancy.

Now I'm weighing a cleaner setup: summing across channels with per-group templates, using mean-removal like step 2 and tuning the biases. Step 3 only reached 14%, which I suspect was due to class 8 dominating the scores.

Checking the column counts for class 5 and 3 now: class 5 still takes about 2,300 predictions even after the bias shifts, so the bias adjustment alone isn't enough. I'm considering whether a refined 3x3 template could help, though I can't measure the score distributions to confirm it.

I'm tallying the remaining prediction columns for classes 0 through 4 and 8 through 9, and class 6 never gets predicted at all.

I'm going to rework the templates so they only use the first three rows and columns, where the digit ink actually lands, and zero out the fourth row and column. I'm also planning to raise the bias for class 6, which gets no predictions at all, to something like 1.5, since 0.6 clearly isn't enough.

I'm going with a middle path: keep the ungrouped step-2 approach that reached 36%, but restrict the templates to the effective 3x3 region and rebalance the biases.

I'm going to restrict the templates to a 3x3 grid, since the effective cells sit in the first three rows and columns, and rebalance the biases with larger shifts for classes 6, 7, and 9, while pulling back on 3, 5, and 2.

I'm sketching the 3x3 templates by hand now: a ring for 0 with a hollow centre, a centre vertical for 1, and a top arc with a diagonal and bottom bar for 2, with the corner weights softened to 0.5.

Writing the 3x3 templates by hand now, since the centre cell and the bottom bar are what separate 2 from the rest.

Writing the 4 template by hand now: a crossbar through the middle, a stem on the right, and some ink in the top-left corner.

Still writing the 3x3 template values for classes 5 and 6...

Still writing the 3x3 template values for classes 7 and 8...

Still writing the 3x3 template values for classes 9 and the cell weighting...

Still setting the bias values, the 9 template weights are scaled by 0.02 and the 144 contributing values are fine, and I'm rebalancing toward class 6 and 7 while trimming 0, 2, 3, 4 and 5.

Next I'm writing the code as a 3x3 template grid, with the fourth row and column held neutral, and I'll explain why the receptive field analysis points to that layout.
