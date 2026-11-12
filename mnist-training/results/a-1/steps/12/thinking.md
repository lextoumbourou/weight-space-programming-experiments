The accuracy has improved to 61%, but a few misclassifications remain. I'm considering whether a more powerful feature design is needed, since a trained CNN of this size would reach around 99%, and I'd like to aim for 85% or higher with hand-designed features. I suspect the max pooling and orientation handling may be smearing the features too much.

I'm weighing whether to adjust the class biases to correct the skewed predictions: 2, 4, 8 and 5 are under-predicted while 3, 6, 9 and 1 are over-predicted. The right bias size depends on the logit scale, which I'd have to estimate first, and I'm also questioning why 4s get pulled toward 6 and 9 and why 8s drift toward 3.

I'm trying to see whether the 8-to-3 confusion comes from the 8 template lacking left-side strokes, which the bias or zero-sum constraint doesn't fix. Rather than hand-tuning each bias, I'm considering whether to derive them automatically, but for now I'll just try a manual bias adjustment to gauge the effect.
