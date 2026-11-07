I'm stuck and need to step back, since the 0→2 case keeps coming out as 224. My guess is that the feature indexing or geometry is off, with the template positions shifted relative to the features. I want to recheck the conv2 sum: each output row should draw on pool1 rows r through r+4, and my kernel's nonzero entries sit at indices 1 through 3, so I need to confirm that the offset maps back correctly.

I'm checking the geometry again: the pool2-to-pool1 index mapping and the orientation convention for the horizontal and diagonal templates both line up. The ink channel also looks fine. So the 0→2 errors probably come from weak or mismatched templates rather than an indexing bug, and I'm considering measuring class-mean features directly to see where they fall short.

I'm weighing whether I can recover per-class feature statistics by reading out one scalar at a time through the argmax. If each logit is a line in a projected feature x, with increasing slopes, the argmax splits x into ten bins, so each step gives a per-class histogram of one projection. That's a workable probe, though 41 steps may not be enough to cover the full feature space.

I'm considering whether the 0→2 confusion comes from how 0s are shaped: their width and the stroke layout might sit closer to the 2 template than I'd expect. Comparing their top and bottom horizontal strokes against the 2's loop at bottom left could explain the overlap.

I'm comparing how a slanted 0 and the 2's center diagonal would light up the middle cells, since both could contribute "/" responses there.

I'm thinking about adding a negative weight on the center ink for the 0 template, since a 0's interior should be empty. Mean subtraction hurt because of the 1s, so a more targeted penalty might work better. I'm also wondering whether the 1s get pulled in when scoring penalizes unexpected ink, because they have little ink to begin with.

I'm realizing the 1s are pulling in 8s because the mean-subtraction left the 1's other channels at zero, so nothing penalizes ink there. The penalty needs to apply to unexpected ink in general rather than only inside the vertical channel.

I'm now penalizing ink in the cells where a template has none, using a negative ink weight scaled by the template's normalized ink, so that the 1 and 0 templates get pushed away from unexpected stroke.

I'm settling on the penalty form now: unexpected ink gets a negative weight scaled by how little the template expects ink there, with the magnitude picked so one stray stroke costs about as much as a matched orientation cell.

I'm settling on a value of λ around 0.3 and checking how the center cells of the 0 template behave, since the ring's blur may leave them with partial ink. I'm dropping the positive ink weights so ink only counts as negative evidence, and resetting the bias to zero since the scores have shifted.

I'm settling on the weights now: the orientation channels get alpha times the normalized template, and the ink channel gets a negative weight that is largest where the template has no ink.
