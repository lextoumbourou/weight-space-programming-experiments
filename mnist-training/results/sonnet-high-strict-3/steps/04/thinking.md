I'm noting that 1, 2, 7 and 8 partly work, while 0, 6 and 9 never do. I'm also seeing that 8 and 2 are over-predicted, so I'll lower their biases and raise those for 0, 6, 9, 3, 5 and 4. Next I'm working out the predicted column sums, starting with column 5.

I'm checking the predicted column totals, with column 5 at around 667 and column 8 at about 3495, and column 9 at zero. Class 0 mostly lands on 2, 8 and 5, so the loop detector may not be firing for it. Since 0, 6 and 9 are never predicted, I'm considering weakening the loop bias and boosting those classes' biases.

I'm checking whether the loop detector can even fit a zero's shape: at roughly 20 by 13 pixels, a ring of two pooled steps is about 8 pixels across, which is too small for the stroke centers. A larger radius won't fit in the 5x5 kernel, so I'm weighing whether the border cells can stand in for a wider loop.

I'm weighing whether the loop feature can capture a zero's width, since two pooled steps may not span it, and considering combining top, bottom and side strokes instead. The bias rebalancing still feels like the simpler lever.

I'm considering a separate "empty center" feature for zeros, built by repurposing channel 13 in place of the small loop detector, since the ink in the middle of a zero is what sets it apart.

I'm settling on an "empty center" feature for zeros by reusing channel 13, with the crossing center of an 8 treated as ink and the open tops of 4 and bottoms of 9 as empty regions. I'll keep the lower-loop feature for 6 and set the 8 weight in channel 13 negative.

I'm settling on the zero feature by repurposing channel 13 as an "empty center" detector, and I'm giving 3 and 7 empty-region features on the left side too. I'm leaving out the 1 feature, since the outer cells are empty in nearly every class and wouldn't separate it.

I'm settling the bias values now: a stronger cut for 8 and a milder one for 2 and 1, and small boosts for 0, 6, 9, 3, 4 and 5. I'm also trimming 7 a little, since it already takes most of the predicted mass.
