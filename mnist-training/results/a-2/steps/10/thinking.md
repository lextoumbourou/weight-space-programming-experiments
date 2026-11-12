Parts detectors seem to add little, so they're probably either poorly calibrated or simply not the main signal. The orientation features are doing most of the work. I'm considering whether the histogram probe could help calibrate things, or whether I should look more closely at why the classes are getting confused. Another option is making the orientation features richer, since the spatial resolution there is coarse.

I'm weighing whether to tune the orientation detectors further, either with two thresholds per orientation or with a different spatial shift. My estimate is that a naive Bayes model with the true parameters would reach roughly 80-85%, so the gap down to my current 70% likely comes from the guessed templates. I also suspect the templates are misaligned because MNIST digits are centered by mass rather than by box, and I'm trying to recall the average positions of the strokes for each digit.

I'm checking whether the orientation feature's spatial coverage lines up with the digit centering, working through the pooling offsets to see where each feature's center lands in the input image.

I'm thinking about whether a sharper probe could help: treating each of the 10 features as its own predictor and checking which one wins, using the confusion matrix to see which classes each feature separates.

I'm weighing a different approach: instead of reading each feature's marginal, I could order the features by priority so that the prediction reveals which ones fire, though that only gives sequential information. Another route is treating a few key template parameters, like spread and saturation, as tunable and using accuracy as the signal for adjusting them.

I'm thinking about making the orientation detection more robust by widening the perpendicular spread of the kernel, since thicker MNIST strokes may be weakening the response. I'm also noting that a horizontal stroke leaks into the diagonal channels at a moderate level, which affects the thresholds.

I'm comparing the digit pairs that look alike, like 5 and 6, by where their top and bottom strokes sit and which way they angle. I'm also weighing whether to tune a global parameter next.

I'm going to test the λ hyperparameter, though it likely only shifts confidence and bias. Another idea is to replace the template approach with difference-focused features for confused pairs like 5 and 6, but the top-right bar is already covered by the templates. The bigger question is whether the parts detectors rarely fire or fire almost everywhere, so I'll check their average activity per class with the histogram probe.

I'm going to probe the loop detector's activity using two scalars, the top-half and bottom-half totals, arranged on a 3x3 grid so the output can reveal how it fires across classes.

I'm setting up a 3x3 lattice of candidate points, with the two probe scalars as coordinates, so the nearest point picks out which bin each scalar falls into; the grid boundaries land at 0.25 and 1.0. Because the lattice is a product of two 1D grids, each coordinate can be decided independently.

I'm settling the class mapping: a 3x3 grid of lattice points lets the argmax over two scalars pick out one of nine bins, with class 9 left unused by setting its logit to a large negative bias. Next I'd check whether the loop detector separates top-half from bottom-half loops for the 0, 6, 8 and 9 digits. If it does, its weight could go up; if not, I'd need to redesign it.

I'm going with the two-scalar probe after all, since it should show how the loop detector separates top-half from bottom-half loops for 6 versus 9. A 1D version over the whole loop total would only show the overall shape.
