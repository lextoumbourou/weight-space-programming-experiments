Negative evidence made things worse, mainly for classes with little ink, which end up with small penalties and so gain. I think per-class bias calibration is needed, and the confusion feedback could guide tuning those biases. Still, the features or templates themselves may be the weak point, so I'm wondering whether my orientation convention or the positions are off, even though 69% accuracy suggests the general approach is sound.

I'm weighing a better feature approach, since the max-pooled features may be too broad while the templates stay sharp. Adjusting class biases from the confusion counts looks useful too: 6, 9, and 8 are over-predicted, while 5 and 4 are under-predicted. Bigger gains will probably still need template changes.

I'm checking whether a thick stroke's edge would fool the horizontal detector, working through the zero-sum kernel on a vertical step edge. The column sums net to roughly zero, and a half-covered edge gives about 0.095 after normalization, which stays under the bias, so this isn't the cause.

I'm considering whether to combine nearest-centroid with the negative evidence and calibrate the result, but I'd rather build on step 2 than keep guessing. Since the gamma approach pushed 8 into over-prediction, I'm thinking about a smaller gamma with the negative part normalized per class.

I'm working out a projection to make each template orthogonal to the mean digit, so that generic ink doesn't favor classes like 8, 6, and 9. Each class gets its own coefficient, and I'd expect that to shift the argmax.

I'm projecting each template orthogonal to the mean digit, so that classes sitting close to the average shape don't get an unfair edge. The self-match score then depends on the residual norm, and normalizing those residuals would put the classes on a more even footing.

I'm projecting each template orthogonal to the mean digit and normalizing, so the comparison becomes a cosine in mean-removed space. I'm also weighing a slant change to the 1 template, since real 1s tilt more than my prototype's, which may be why 1 gets confused with 2.

Next I'm checking the remaining pieces: the slant of the 1 template and whether blurring the templates more helps. I'll keep the loss and the scale as they are, and go with the projection plus cosine approach.
