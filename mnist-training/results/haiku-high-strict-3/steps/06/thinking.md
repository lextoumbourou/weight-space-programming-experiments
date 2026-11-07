I'm checking why class 8 keeps winning: its prototype has high occupancy in many cells, so the linear term a·mu outweighs the distance-based bias, and the baseline entries (occupancy 0.5 where S=0) make that worse across many entries.

I'm weighing whether to keep tuning by hand, since the activity scales are unknown and my neutral 0.5 values are blurring the prototypes. Step 2 was still the best at 36%, so I'm considering whether a calibration of the class biases driven by the feedback could help more than further hand-tuning.

I'm considering nudging the class biases directly against the confusion matrix, treating that as legitimate manual tuning, and I'm weighing whether to go back to the step-2 network (36%) since it has the best accuracy so far. Its main problem is that classes 5 and 4 are over-predicted, so I'm checking the column totals to see how far off they are.

I'm tallying the column totals of the step-2 confusion matrix to see how far each class is over- or under-predicted. Classes 5, 3 and 4 look well above a balanced share, while class 6 is barely predicted at all.

I'm reading the column totals of the step-2 confusion matrix: classes 2, 3, 4 and 5 are each over-predicted by several hundred, while 6, 7, 8 and 9 are almost never predicted. The plan is to push biases up for the under-predicted classes and down for the over-predicted ones, though the logit spread makes the right size of change hard to judge.

I'm reverting to the step-2 network, keeping its ungrouped templates and per-cell mean removal at scale 0.02, and setting biases by hand to push classes 6 through 9 up and classes 2 through 5 down.

Writing the step-2 template values back out...

Still writing template values...

Still writing bias values...

I'm reverting to the step-2 network's ungrouped setup with per-cell mean removal and scale 0.02, and I'm plan to adjust its biases by reading the confusion matrix: negative for the over-predicted classes and positive for the under-predicted ones. I'll note that the grouped and prototype variants didn't work.

I'm going back to the step-2 setup since it had the best accuracy, and I'll spend the remaining budget tuning its biases. I'll keep the convolution the same across variants and keep the code short.
