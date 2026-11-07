I'm at 31% now, and the main errors are 0 being mistaken for 6 (900 cases), with 8 also absorbing some. I suspect the bias and negative weights are behind it, since the hole of the 0 template carries a negative weight even though ink appears there.

Checking the convolution indexing and pooling coordinates, the geometry looks consistent, so I'm now questioning whether the templates are too fine for the natural variation in MNIST digits.

I'm weighing a change to the templates: blurring them with a small smoothing kernel so the matched filter tolerates the natural variation in handwriting better. I'm also considering subtracting the mean template across classes so the shared central ink doesn't dominate, and I'd like to fix the bias accordingly.

I'm weighing whether the bias term should scale with each template's total weight, and checking whether the negative hole weights in the 0 template are actually contributing to the 0-to-6 confusion.

I'm thinking about whether the bias term is overwhelming the score, since the 0 template's large ink total pushes its bias quite negative. Rather than tuning the constants by feel, I want to normalize the weights so the decision depends less on the bias scale.

I'm thinking about normalizing each class template by its positive mass, so the score becomes an average of the input over the template cells and the bias can go to zero. That should stop the 0 template from winning just because it has more ink, and I'd scale the logits so the differences between classes are meaningful.

I'm weighing a normalized score: the average input over the template's positive cells, plus a small penalty for ink falling outside the template, so the scale of each class's ink total stops driving the decision.

I'm going to replace the raw template scores with a normalized score: the average input over the template's positive cells, minus a penalty for ink landing outside the template. For the masks, I'll blur the templates with a small 3x3 kernel, use half weight for the '+' cells, and fold the negative hole cells into the outside penalty.

I'm setting each class weight to a normalized in-template average and subtracting a penalty for ink outside it, with the grid fixed at 9x9, the scale at 10, and the bias at zero.
