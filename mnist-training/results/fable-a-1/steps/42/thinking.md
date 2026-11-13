I'm at 90.83% with loss 0.3347 and nine steps left, so now I'm moving on to tuning. The loss looks a bit high for the 9.2% error, so the model may be overconfident, and I want to test a global scaling to check that.

I'm weighing which single knob to change first, and the H/V trust factor is the main candidate since the dense features may be pushing it too high or too low. The loss fell while accuracy rose, which hints at some overconfidence, so I'll try a global temperature of 0.85 across all the scaling terms, since that isolates calibration without changing accuracy. I'm also noting the per-class count imbalances, with class 2 over-predicted and classes 0, 7, and 9 under-predicted, as possible bias adjustments to check afterward.

I'm adjusting the per-class bias values now, nudging class 2 down and classes 0, 7, and 9 up to correct the over- and under-predictions. Then I'll apply the 0.85 scale to the weights and biases, leaving the bias adjustment itself unscaled, so I can see the effect of the temperature on its own.

I'm applying the scale to the weights and biases, then adding the bias adjustment on top afterward.
