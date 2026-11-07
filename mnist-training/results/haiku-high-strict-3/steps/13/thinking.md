I'm at step 12 with 36.68%, the best result so far, and three steps remain. I can keep tuning modestly, or settle on this configuration, with steps 13 and 14 available for small tweaks before step 15.

I'm tallying the column sums and recall figures for each class. Class 5 is the largest prediction count with the lowest recall among the heavy classes, so I'm weighing whether to nudge its prior down.

I'm weighing a bump to class 7's bias, since its recall is low and the 458 images it sends to class 9 are the main leak, though that boost could also pull predictions from other classes.

I'm settling on a step 13 with a few bias adjustments: pushing class 7 up to 2.3 to pull back its images from class 9, nudging class 5 and the other heavy classes further down, and holding class 6 near 2.0. These are small moves in the direction the prior counts point, so I'm expecting a modest shift toward balance, though it could go either way on accuracy.

I'm going to make step 13 the real attempt, then settle the final configuration in steps 14 and 15, reverting if the result gets worse.
