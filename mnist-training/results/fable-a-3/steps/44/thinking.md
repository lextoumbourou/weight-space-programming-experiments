Both scale settings land at nearly the same loss and accuracy, so the optimum sits somewhere around 0.5 to 0.55. The per-class biases were tuned at the old setting, though, and the predicted counts per class are now uneven, ranging from 927 to 1102.

Now I'm checking the predicted class counts against the true ones: class 9 is still under-predicted, while classes 1, 2, 3 and 5 are over, and 0 and 6 are under. I'll set both scales to 0.52 and retune the per-class biases from the average of the last two runs, starting with small corrections for classes 0 and 1.

I'm working out the per-class bias deltas from the averaged prediction counts, and class 9 gets the largest upward nudge, with the rest shifted in small steps. The resulting vector of extra biases is all set, though the values keep climbing in the same direction, so I'm noting that the corrections may be overshooting.

Looking at the asymmetry in the transition counts, 9 pulls toward 7, 8 and 4 more often than they pull back, so the bias for class 9 keeps climbing as counts match. The new extra-bias vector is set, and I'm now moving both scales to 0.52 together with those biases.
