Now I'm adding up the column totals to get the bias figures, and the first column comes to 772.

Now I'm working through the ratios of each column's total against its true count, taking logs and applying a bias correction to each class. Class 4 looks structurally weak, since its confusions with 1 and 9 are the ones I'd expect, so I'm starting to wonder whether the 1 template's small norm is pulling predictions toward it.

I'm weighing whether the calibration is off: the 1 template is small, so it may win too often, and I could lower A to around 0.5 or adjust the biases instead. The class-level offsets are one thing, and how the penalty scales with template size is another, and I'm still deciding which fix belongs to which.

Now I'm applying a 0.6 factor to the bias correction, since changing A will shift things too; the penalty term scales with A² and the dot product with A, so a smaller A eases the large-template penalty. I'm also reshaping the 4 template so its left stroke runs more vertically down to the crossbar, with the right stroke longer than the left.

I'm checking whether a smaller A would help, since a lower value shrinks the penalty on large templates. Since the penalty and the dot product scale differently with A, I'd need to adjust gamma to keep the logit spread similar, so I'm working out roughly 5 for it.
