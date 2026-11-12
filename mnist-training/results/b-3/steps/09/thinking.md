I'm at 65% accuracy, and the 9 class is the weakest with 139 correct. The template for 9 is catching 7s instead of 9s, while real 9s get sent to 4, 8, 5, and 0. My 9 template's loop is too small compared with how MNIST 9s actually look, since they tend to have a larger top loop and a slanted, often curved stem.

I'm weighing a discriminative fix: since 7 and 9 share a top bar and right stroke, the mean-centered correlation barely separates them. I'm considering a pairwise adjustment that pushes each confused class's template away from the class it gets mistaken for, and I'm also planning to enlarge the 9 loop.

I'm settling on a pairwise adjustment for the confused classes: each pair's template shifts toward its own class and away from the one it gets mistaken for, weighted by the confusion counts. I'm working out the step size so the 7→9 push is substantial, and I'll apply the update separately for the ink and orientation groups, then recalibrate the biases afterward.

I'm working out bias adjustments from the predicted counts, nudging classes 0, 3, and 7 up by half the log ratio since the pairwise updates will shift the 7 and 9 predictions anyway.

I'm working out the bias values for each class from the predicted counts, nudging the weights for 0, 3, 7, 8, and 9 by a fraction of their log ratios. Then I'll fold those into the pairwise confusion update and write the code for it.

Continuing the template work, I'm rewriting the templates per group and folding the pairwise confusion update into the mean-centered weights. For the 9 class I'm enlarging the loop and shifting the stem so it better matches how real 9s look.
