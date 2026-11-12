Still too slow, so I'm questioning my feature extraction itself. Maybe the oriented detectors with 6x6 max pooling and thresholding are producing features I didn't expect, and some of the confusion pairs (1→7, 8→9, 7→9) might come from a systematic offset in where I assume the digits sit.

I'm checking whether a systematic offset between the digit positions and my templates could explain the 1→7 confusion, since a 1 might look like a 7 if the stroke sits shifted relative to the template. Then I'm re-deriving the coordinate mapping through the pooling layers to confirm that the input-to-feature indexing is correct, and the direction of the shear, which tilts the top of the digit to the right, also checks out.

I'm checking the arithmetic on the pooling: each pool2 cell can only reach two distinct starting offsets per dimension, so the 16 channels I'd hoped for don't give me a finer grid.

I'm thinking about whether a trained linear classifier's advantage, negatively weighting features that point to other classes, could be approximated by hand. For the 8-versus-9 pair, I could add a positive weight to the 8 template and a negative one to the 9 template at the bottom-left curve features, and design similar pairwise terms from the confusion matrix.

I'm considering whether the pairwise discrimination could be built in by hand: for 8 versus 9, the bottom-left stroke is present in 8 and absent in 9, so I could add weight to 8 there and subtract it from 9. Centering the templates won't achieve that, since it only shifts every class by the same amount, so these would be genuinely different template values.

I'm considering a different route: conv2 with ReLU could compute nonlinear part detectors, such as a loop feature that needs ink on several sides of a region at once. That might separate 9 from 4 and 7 better, but it would mean giving up some of the 16 orientation channels.

I'm checking which error pairs are worst: 8 getting called 9 is by far the largest, followed by 7 and 4 also landing on 9. The 9 template acts like a sink, since its top loop and right stem absorb the strokes of several other digits. The question is whether normalization is weakening 8's bottom-left reward enough for 9 to keep winning.

I'm checking why 1 keeps getting called 7: my 1 template is averaged over shears and sits in the center, while the 7 stem runs close to the same column, so the stem position may be the real problem. I'm also noticing that the 7 template's center of mass sits well below its top bar, which could be pulling it toward 1s.

I'm realizing the 7 template's center of mass sits noticeably above and to the right of where real 7s would center, so my drawn 7 is systematically off. Re-centering each digit's stroke centroid to the middle of the frame, weighted by stroke length, might fix the 1→7 and 7→9 confusions.

I'm now settling on the center of mass target for re-centering each digit's strokes, weighing 14 against 13.5 and leaning toward roughly 13.7. Next I'm thinking about scaling each digit into a 20-pixel box while keeping its aspect ratio.

I'm checking the stroke positions after centering: the 7 would move down about three rows, so its bar lands near row 8 and its stem near row 26, which is plausible for real MNIST digits since centering on the center of mass can push the bounding box past the usual range. I'm also noting that stroke thickness doesn't change the centroid, and that I need to apply the centering after the shear, since shearing about row 14 shifts the column center of mass slightly.

Next I'm weighting each sampled point by its arc length, since the ellipse points are spaced by angle rather than length, so the centroid stays accurate for both the polylines and the curves.
