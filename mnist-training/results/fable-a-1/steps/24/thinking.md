I'm decoding the three features from the vector table, starting with class 0, where f0 comes out to about .999, f1 to .397, and f2 to .508. Class 1 is next, and I'm working through its values the same way.

Still working through the remaining classes' feature values...

Still computing the feature values for the remaining classes...

I'm checking the V(2,0) values against their grid cell, and the 9 looks right. Next up is V(3,3), and after that the 16 diagonal features.

I'm weighing whether to run a midway integration check now, with 8 H cells and 7 V cells measured, or to keep measuring the diagonal features first. Integrating early would mean filling the unmeasured ones with hand templates, but the measured stats already look more informative, so I'm leaning toward continuing the measurements.

I'm going to integrate now rather than keep measuring: the 15 checkerboard features for horizontal and vertical orientation get naive Bayes with a trust factor of 0.5, and the diagonals will use hand templates at weight 0.2.

I'm setting the measured orientation weights aside for now and zeroing the hand templates for the horizontal and vertical features, while keeping the diagonal template weights. I'll also reset the bias adjustment to zero so the calibrated measurements aren't skewed.

Still measuring the horizontal cells, pulling values for the (0,0) through (3,1) grid positions.

Still pulling the vertical cell values for the (0,2) through (2,2) positions.

Still checking the vertical cell values and the classifier's bias terms, with the hand templates limited to the diagonal features.

Setting the hand templates aside for the horizontal and vertical features, I'm keeping only the diagonal ones in the bias and weights, and writing the code for that.
