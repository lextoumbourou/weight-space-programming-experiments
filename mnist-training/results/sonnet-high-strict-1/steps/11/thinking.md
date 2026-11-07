The first template now has two strokes and it's overpredicting class 1, which probably means normalization scaled it up after the lean made its norm smaller. I'll go back to step 9, the best run at 57.4%, and undo the normalization change and the lean strokes before trying anything smaller.

I'm keeping step 9's weights and applying the bias values I'd already tested in step 10: column 7 at -0.1, column 8 at 0.5, and column 4 at -1.0. I might also try 0.1 for column 1 and 0.4 for column 2, then bank whatever gains come from that.
