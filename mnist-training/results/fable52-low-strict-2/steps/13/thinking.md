I'm at 74.3% now with three steps left: one exploratory step, then either an exploratory step or a revert, and the last one to hit my best. The weakest class is still 2, with 571 errors, along with the 7 and 9 confusion, so I'm going to think about the 2s physically: a top arc, a diagonal down to the bottom left, then a base stroke to the right.

I'm weighing whether to nudge the 2 bias up, but the predicted and true counts for 2 are already close, so the class is just diffuse rather than under-scored. Raising the 2 variants and emphasis did lift recall, though it over-predicts and precision suffers. Next I'm considering the loss rather than accuracy: a lower gain might help if the errors are confident, and scaling the biases to match should leave the argmax, and so the accuracy, unchanged.

I'm weighing a combined move: scale the gain down to 6 with the biases scaled by 0.75 so accuracy stays clean, plus one accuracy experiment, maybe raising the mean_all coefficient or emphasizing the loop on 9s, since the 7↔9 pair is among the biggest confusions and the earlier 9 emphasis left it unresolved.

I'm adding a small bias adjustment: emphasizing the left-half loop for 9s and lowering the 9 bias by 0.1 to offset the extra logit, with bias set to -0.6. After that, one more step to decide, then the final one.
