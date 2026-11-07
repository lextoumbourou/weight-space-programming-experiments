The model's accuracy jumped to 35.4% after zero-centering and normalizing, though the loss of 6.4 still points to overconfidence. Looking at the per-class diagonal counts, classes 7 and 8 are far behind the rest, with only 30 and 48 correct. Class 7 is mostly being confused with 1, 4, and 9.

The model's per-class counts show that 9 is mostly being mislabeled as 4, and 4 and 1 are over-predicted across many digits. Classes 7 and 8 are under-predicted, with 8 scattered across several other classes. My plan is to lower the scale to around 5 to bring the loss down, and then adjust the 4 and 9 templates, which seem to be overlapping too much, along with 7 and 8.

Now I'm tallying the predicted totals per column to see which classes the model is leaning on too heavily, with 4 and 1 looking like the main offenders.

Now I'm working out the column totals to see the imbalance: 4 is predicted far more often than any other class, with 1 and 9 also heavily over-predicted, while 5, 0, 6, and 2 fall short. My idea is to shift the per-class biases to offset these counts, pulling predictions toward a more even spread.

I'm weighing a bias adjustment to counter the over-predicted classes, since 4 and 1 are pulling far more predictions than the under-predicted ones like 5 and 0. A log-based offset scaled by about 1.5 looks like it would nudge the counts toward balance, though I'll need to keep the scale roughly where it is so the mapping doesn't shift under me.

Next I'm lowering the scale to 5 to bring the loss down, and computing per-class bias offsets from the log of each predicted fraction, so over-predicted classes like 4 and 1 get pushed down and under-predicted ones like 5 and 0 get pushed up.

Now I'm weighing the bias correction: since 4 and 1 are over-predicted and 5 and 0 are under-predicted, I'm considering offsets proportional to the negative log of each predicted fraction. Setting the correction to exactly the log-odds would fully equalize the predicted counts, but I'm leaning toward a milder version so I don't overshoot.

I'm moving the per-class biases to a 1.2-scaled log correction so the over-predicted 4 and 1 get pulled down and the under-predicted 5 and 0 get pushed up. I'll also lower the scale to about 6 to cut the loss, and keep the templates unchanged for this step so the effect of the bias change is easier to isolate.

Next I'm lowering the scale to 6 and adding per-class bias terms derived from the negative log of each class's predicted count, scaled by 1.2, to push over-predicted classes down and under-predicted ones up. I'll keep the templates unchanged for this step so the effect of the bias change is easier to see.

Now I'm computing per-class biases from the log of each predicted count, so over-predicted classes like 4 and 1 get pulled down and under-predicted ones like 5 and 0 get pushed up, and I'm lowering the scale to 6 to bring the loss down.
