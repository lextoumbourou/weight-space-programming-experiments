I'm trying to improve the classifier now. The confusion pattern shows classes 4 and 6 are over-predicted while 1, 2, 5 and 8 are under-predicted, so I'm considering adjusting the fc biases to offset that, and also whether scaling the logits up slightly would help given the loss and accuracy I'm seeing. I'm also starting to think about a structural change to the template matching step.

I'm weighing a few ways to make the templates more varied and to check whether the cell centers are off, but I'll start with the bias adjustments. Column sums show classes 4, 6 and 9 are heavily over-predicted while 8, 2, 5 and 1 are under-predicted, so I'm planning to penalize the first group and boost the second, with moderate, uncertain logit scaling.

I'm settling on bias offsets of about +0.5 for the remaining classes, and I'm holding off on changing the logit scale so I can test the bias change by itself.
