I'm looking at a 65% figure and thinking about where to improve: adjusting biases, refining the templates, and tuning the gain. The confusions stand out, with 0 going to 6 and 2, 8 going to 2 and 1, and 4 going to 9 and 1. Digit 2 is overpredicted, while 8, 4, and 0 are underpredicted. One idea I'm weighing is adding explicit negative strokes for certain digits, penalising ink in regions that should stay empty.

I'm weighing a way to penalise ink where digits shouldn't have it, for example in the centre for 0 and along the right side for 6 and 2. I'm considering centring each template by subtracting the mean of the others, which should bring out what's distinctive about each digit, and adding negative strokes to the variants.

I'm settling on bias adjustments instead: raising the biases for 0, 4 and 8, and lowering those for 1, 2, 6 and 9. I'll keep the magnitudes moderate, since the loss suggests the logits are modest in scale. Next I need to work out where the negative strokes go, positioned within each digit's frame alongside the positive strokes.

I'm adding negative strokes to each template, drawn with negative weight so they suppress ink where a digit shouldn't have it, and I'm computing the centroid from the positive strokes alone so the negatives don't shift the digit's frame. For 0 that means penalising the centre in several orientations, and for 6 a short vertical in the upper right.

I'm adding negative strokes for 4, a top horizontal, since its template has no top stroke and 9 closes its top.

I'm planning negative strokes for the remaining digits: an upper-right vertical for 5, an upper-left vertical for 3, and I'm weighing whether 6 needs a suppressing stroke at its top, since 5 leaves the lower-left open where 6 has ink. I'm also noting that 8 needs a boost, which I'll handle through the biases.

I'm adding a bottom horizontal negative stroke to the 4 template to discourage ink where 1s put their weight, and I'm settling the gain and neg weight at their current values, since the loss will tell me whether the logits are too small.
