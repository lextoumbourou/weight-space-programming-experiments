The model is at 60.45%, the best so far, with three steps left. Eight is being predicted too often, and the biggest offenders are 2→8 and 6→8, followed by 5, 0, 4 and 3 sending more to 8. The 7→9 pair has improved, and 9 is also misfiring toward 7, and there's confusion between 9 and 4 in both directions, plus between 3 and 5.

I'm adjusting the biases for the remaining steps: nudging 8 down, 6 and 3 up, and keeping a small structural tweak in reserve for the next exploratory step.

I'm weighing whether to tweak the loss weighting too, but I'll stick to bias adjustments for this step since the loss is already at a reasonable 1.21.
