Step 3 came out badly, with almost every case predicted as class 8. My guess is that class 8's score is simply too large, likely because its positive O and V/H values at many cells pull it upward after the mean subtraction.

I'm checking whether the bias term explains why class 8 wins almost every case. Since the per-cell weights sum to zero across classes, uniform activity nets out, but class 8's template has broad positive coverage over the central cells, so it accumulates the largest score on typical digits. I'm thinking the fix is to make each class's template sum to roughly zero so no class acts as a generic-ink winner.

I'm now weighing a per-class fix: centering each class's template across cells so a uniform-activity digit can't favor one class. Center-heavy digits still tilt toward whichever class has positive center weights, so that alone won't fully resolve the bias.

I'm settling on a fix: center each class's template across all cells and groups so it sums to zero, and reduce the weight of the O group, which carries half the channels and pushes class 8 upward. Even with that, the zero-mean template can still favor classes whose positive cells line up with typical activity, so this won't fully remove the bias.

I'm going to center each class's template across all its entries so each sums to zero, on top of the existing per-entry centering across classes. That gives zero row sums and zero column sums. I'm also wondering whether the O group, with its blob channels, is simply too strong and should be scaled down.

I'm weighing whether reverting to the step 2 approach makes sense, since that one reached 36%. The scale of 0.02 looked reasonable then, and the loss of 3.98 back at step 2 suggests I should keep it rather than change it again.

Now I'm weighing whether the zero-sum issue is the real cause, and whether normalizing each class's template to unit norm would keep weaker classes like 1 from being drowned out after centering.

I'm keeping the step-2 biases for now, since the zero-centering shouldn't change their scale much. I'll apply the centering in two passes: first across classes for each entry, then within each class so its overall mean is zero.

I'm also centering each class's template over all its entries, so every class sums to zero on top of the per-entry centering across classes. That should keep the O group's positive center weights for class 8 from giving it a generic advantage.
