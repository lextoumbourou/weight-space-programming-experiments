The gain is modest, at 72.9% accuracy with loss 0.910. I'm weighing a temperature test, scaling all fc weights by 1.2 and keeping it if loss improves, against also tuning lam_ori, since changing both at once would muddy the loss signal.

I'm tallying the step-25 transition counts row by row, then computing the log-ratio changes divided by 70 to see which classes are drifting most.

I'm checking that the global scale of 1.2 leaves the argmax unchanged, since that means temperature only moves the loss, and I'm applying it across all the fc weights, including the hole ones.
