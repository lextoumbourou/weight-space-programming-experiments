I'm looking at the baseline of 52.8% and seeing that 8 and 6 are over-predicted while 4 is barely predicted. My plan is to shift the biases down for 8 and 6 and up for 4, and I suspect the 4 template is weak since real 4s tend to be slanted. I also notice broad templates like 8's inflate dot products because features are non-negative, so I'm considering making each weight vector zero-sum to remove the ink-amount effect, starting with setting w_c equal to T̂_c.

I'm weighing whether to center each class template by subtracting a mean, possibly per row or against a blurred ink prior, since the strokes sit mostly in the middle. I'm also tuning the biases from the confusion counts: lowering 8 and 6, raising 4 and a few others. I'm considering two prototypes per class or averaging templates to make the 4 template less rigid.

I'm working out that centering the features with a mean vector is equivalent to a per-class bias term, but the scale of that mean is unknown, so I'll set the biases by hand instead. I also want to sharpen the templates so that ink where other classes appear but this one doesn't gets penalized, and I'll try several variants with refined prototypes and biases.

I'm sketching several template variants for the digits: open-top and slanted versions of 4, a looped and straight-stem 9, curved and vertical-or-slanted 1s and 7s, and a looped 2 with a smaller bottom on 3. I plan to average the variants per class, renormalize, and then consider nudging the scale up a bit since the loss is high at 53% accuracy.

I'm settling on keeping the scale at 10 for now and turning to the bias adjustments, so the probabilities don't get pushed around any further before I start writing the code.
