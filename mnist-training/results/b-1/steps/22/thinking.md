The model is at 70.3% accuracy, though its loss ticked up slightly, from 1.058 to 1.069. I've still picked the best-loss step for the test. Next I want to recalibrate β using the counts, since I'm now including the orientation term at 0.8 weight, which may change how strongly β shifts the offsets.

Still working through the recalibration: I'm tallying the step-21 column counts and computing each row's Δβ as the log ratio of row to column totals divided by 70.

I'm working out the per-row β shifts, and now I'm trying a slightly different scale for the logits to see whether the loss comes down.

I'm keeping the scale as it is so the calibration stays consistent, and the next step is to try a temperature adjustment.
