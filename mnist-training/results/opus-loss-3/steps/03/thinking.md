I'm trying to get past the modest gains, since biases only patch things over, and the templates themselves look like the weak part. The confusions are mostly 2 versus 7 versus 3, plus 1 to 7, 6 and 0, 5 to 6, and 9 to 2, 4, or 7. I'm considering a different framework built on ink-based features rather than a hand-made template linear classifier.

I'm weighing whether to tune the template sharpness and weighting, since the handmade templates are the bottleneck at around 58% while a trained linear classifier on the same features would reach about 95%. I'm considering widening the Gaussian smear to around sp=3 so the templates resemble the blurrier mean digits, and possibly penalizing ink where a template has none.

I'm reconsidering the coordinate mapping for the digits, since the vertical scale I used looks too small. The width of a zero comes out too narrow at the current x scale, so I'd widen it and add a slight rightward slant to match typical MNIST digits.

I'm going to compute the center of mass of my stroke drawing and shift it to (14,14), which is pure geometry from my own template and not a network run. Checking the binning, conv1 output p covers input pixels p through p+4, so its center is p+2, and that mapping is correct.

I'm now looking at the 1→7 confusion, which got worse once I raised the bias for 7, since its slanted stroke resembles a 1. I'll need to re-estimate the biases anyway after changing the templates. I'm also thinking about how the shapes should look against typical MNIST digits, starting with the 0 as a slightly slanted ellipse and the 1 as a mostly vertical stroke.

I'm weighing whether to reset the biases to zero, since they'll have to be re-estimated once the templates change anyway.

I'm working on turning the handmade templates into expected feature values, so the scoring has a proper scale: each template entry becomes a saturating estimate of how much stroke of that orientation falls in each bin, and I'd score classes with a shared-covariance style term that subtracts half the squared norm.

I'm treating the classifier as nearest-centroid under Euclidean distance: the score for each class is the dot product of its template with the features minus half the template's squared norm, divided by a variance term around 0.15. That form handles ink mismatch on its own, since the shared ||f||² term cancels across classes. I still need to fill in the coverage values for each template.

I'm estimating each template entry as a saturating expected feature value, so the bins reflect how much stroke of each orientation lands in them. The coverage comes from a Gaussian-weighted sum along each stroke, and I'll cap it around 0.6 since aligned strokes give roughly 0.8 after the conv bias, with off-orientation strokes falling well below that.

I'm estimating the expected feature values as a saturating sum over the stroke coverage, with a spatial smear of about 2.5 and a peak value near 0.7. I'm also weighing whether the variance scaling, around gamma of 4, will hold up or whether the absolute calibration will penalize the bulkier templates like 8 and 0 too heavily, which the biases could then correct.

I'm settling on fresh zero biases and writing out the stroke coordinates, with the slant term and a center-of-mass shift to keep the digits aligned.

Still defining the stroke coordinates for the digit templates...

Still defining the digit stroke templates and writing the center-of-mass shift code...
