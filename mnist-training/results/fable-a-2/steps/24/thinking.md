I'm decoding each cell's index from three bits, checking the horizontal centre, vertical centre, and bottom-right horizontal sums against their thresholds. For cell 0, the bit-one sum is 164 and the others are worked out next.

Now I'm checking the remaining cells' bit sums against the thresholds, cell 1 through cell 8.

I'm checking the bit sums for cell 9 and comparing the horizontal and vertical centre values against their thresholds. The horizontal centre separates cell 0 and cell 1 clearly from the rest, and the bottom-right values start to tell cells 8, 2 and 3 apart.

Now I'm converting the horizontal and vertical centre values into z-scores against their thresholds, giving each cell a rounded adjusted figure, and checking how the bottom-right bit separates the cells.

Now I'm running the classifier with these three extra line statistics, bringing the total to 13, and the bias needs retuning because the added correlated terms shift the score.

I'm weighing whether the scale should drop to about 0.55 now that three more features push the logit magnitude up, and I'm adjusting the per-class biases to match.

I'm settling on the final class biases, with a starting point for the fourth-to-last cell, and setting the scale to 0.55.
