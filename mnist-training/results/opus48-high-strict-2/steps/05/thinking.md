Step 2's design still gives the best result at 29%, and the mean-subtraction change made things worse at 18.6%, so I'm planning to revert to exactly that design before making smaller incremental changes. I'm about to restate step 2's setup: a centered spatial ink template that is neither normalized nor mean-subtracted.

Still writing out the step 2 template values...

Rebalancing with bias looks like the way to go: I'd add negative bias to the over-predicted classes 1, 5 and 6, and positive bias to the never-predicted 0, 2 and 7 plus the under-predicted 8, 9 and 3.

I'm weighing whether to add bias adjustments, since many true-0 cases are going to class 6 and the dense templates are pulling predictions toward 5 and 6. Full normalization overcorrected toward 1, mean-subtraction toward 2 and 6, and the raw centered step-2 version toward 5 and 6, so I'm considering a partial normalization of the templates as a middle path.

I'm going to keep the step 2 design as the baseline and try a small bias-based rebalance, pulling down the classes that win too often and pushing up the ones never predicted. Partial normalization of the templates could also help, since full normalization overcorrected and raw centering still favored the dense templates.

I'm tallying the step 2 confusion counts to see which classes are over-predicted, with class 5 at roughly 3600 and classes 1 and 6 following behind.

Rather than tuning per-class biases by hand, I'm weighing whether the better move is improving the features, since the bias adjustments are hard to predict.

I'm weighing whether to drop the bias-tuning route altogether and instead improve the features, since blur from the pooling layers limits how much finer spatial detail the 4x4 grid can carry. Using all the conv2 channels as a finer grid doesn't work, because maxpool collapses them, and quadrant-specific detectors would break translation invariance.

I'm weighing whether to build richer features by using the 16 conv2 channels for distinct local patterns, but hand-designing a 16×8×5×5 conv2 is the hard part. Given the time, I'll take the safer route: revert to the step 2 design, which is the best so far, and apply gentle bias rebalancing with conservative values to avoid overshooting.

I'm going to drop the vert/horiz features, since they seem to cause instability, and go with a normalized ink template plus class biases. Step 3 pushed everything toward class 1, while step 2 reached 29%, so I'll go back to step 2 and add a small set of biases: nudge up the under-predicted classes 0, 2, 7, 8, 3 and 9, and pull down the over-predicted 5, 6 and 1.

I'm going to restore the step 2 design with its centered, unnormalized templates and add a conservative set of class biases: raising the never-predicted classes and lowering the ones that win too often, so the shift stays small enough not to overshoot.
