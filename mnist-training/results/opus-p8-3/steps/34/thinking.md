I'm finding the model is underconfident, so scaling the temperature up should lower the loss. I'll try ×1.3, and the numbers so far point to an optimum near 1.4 to 1.6, so I'll test 1.4. I'm also checking per-class bias correction by summing the confusion matrix columns for step 28.

I'm checking per-class bias by summing the confusion matrix columns for step 28. Classes 7 and 3 come out under-predicted, while 1, 2 and 5 are over-predicted, so I'm working out small bias offsets for each class to apply after the temperature scaling.
