The hole feature actually made things worse, dropping accuracy from 38.9% to 33.2%. Digit 8 is now being predicted far too often, almost everything lands there. My guess is that the hole detector fires a lot on noisy input, so 8's template, which is built from center-column holes, matches those generic responses and pulls predictions toward 8. Now I'm checking the column 8 totals.

Now I'm weighing whether to drop the hole feature entirely, since digit 8 keeps absorbing predictions and 4 is being pulled toward 9. I'm checking the step-6 confusion marginals to rebalance the biases instead.

Now I'm working through the column totals for the step-6 confusion matrix. Digits 7, 0, 6, 8 and 5 are predicted too rarely, while 4, 1, 2, 9 and 3 are predicted too often. I'm planning to go back to the step-6 weights without the hole feature and adjust the biases from those marginals.

I'm recalculating the bias for digits 2 through 9 from the step-6 marginals, starting with 2 at 0.345 and 3 at -0.309. Digit 4 comes out at -2.173, 5 at 1.639, 6 at 1.218, 7 at 2.148, 8 at 1.082, and 9 at -0.769.

I'm recomputing the biases with a damped correction factor of 0.4 instead of 0.6, since the 7 bias at 2.148 looks like it could overshoot. The revised values come out to roughly 1.76 for digit 0, -1.13 for 1, 0.40 for 2, -0.28 for 3, -2.10 for 4, 1.61 for 5, 1.17 for 6, 1.90 for 7, 1.03 for 8, and -0.13 for 9.

I'm dropping the bias-tuning idea for now, since it looks like it's overfitting the validation marginals. The step-6 biases already gave the best result at 38.9%, so I'm leaning toward reverting to that configuration and making only a small bias adjustment. After that, I'll look for a safer feature to try.

Reverting the hole feature and returning to the step-6 setup, with a modest bias adjustment to lock in the roughly 40% accuracy. After that I'll look for a safer improvement, such as making the first convolution less blurry so the 4 and 9 tops separate better.

Next I'll write the full build without the hole feature, using the revised biases.
