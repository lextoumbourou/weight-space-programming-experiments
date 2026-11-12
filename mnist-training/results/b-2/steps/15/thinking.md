The score improved to 72.65 with loss at 0.897, so this measurement-driven approach is paying off. I'll keep measuring the remaining channels, but measuring orientation features per region would mean around 64 features, which is too many to take two per step.

I'm weighing whether to measure aggregate scalars instead, such as the template logit for each class, since their class-conditional means could calibrate per-template scale and bias in about five steps. An LDA over the ten calibrated template scores might also handle cases where one template fires for the wrong digit. I'll first finish the structural channels 5, 6, 8, and 9, then decide whether the template-score measurement is worth it.

I'm settling on measuring channels 5 and 6 with two scalars per step, since binary splits for three or more scalars would lose too much magnitude information. Step 15 will cover the top and bottom of channel 5.
