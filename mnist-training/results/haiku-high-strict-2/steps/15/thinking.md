The step 14 score came in at 51.15%, close to step 13's 51.31%. Only step 15 is left, and whatever I submit there gets scored on test. I'm leaning toward submitting something near step 13, which had the best validation score, or a small improvement on it.

I'm checking the step 13 and step 14 deltas against each other: the changes were small, with step 14 nudging a few values up and down. Looking at the class prediction counts, column 0 looks heavily overpredicted, and the column 8 and 9 totals shift too.

I'm weighing whether to blend the step 13 and step 14 settings for the final submission. Step 14 over-predicts classes 0 and 9, and the mix of recall gains and losses suggests the class 0 offset has a large effect. A middle setting would probably land near 51% again, though it might shift the class 0 counts toward a more reasonable range.

Averaging the step 13 and 14 deltas would be a reasonable hedge, but step 13 is the configuration with the best validation loss and accuracy, so I'm inclined to submit that one exactly rather than an interpolated setting.

I'm settling on the step 13 settings for the final submission, since they had the lowest validation loss and the highest accuracy. Step 14's adjustments just shifted the class 0 and 9 counts back and forth without a net gain, so I'll reproduce step 13's configuration exactly.

Still checking the step 13 delta values against the code I'm reproducing...
