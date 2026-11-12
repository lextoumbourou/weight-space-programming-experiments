I'm comparing the 7 digit images against the 9 template, since the 7 has a top bar and stem but no left side of the loop that the 9 has. The hole feature may not be firing reliably for the 9's loop, which would explain why the 7→9 confusion is the biggest error at 373.

Next I'm weighing whether the 7 template's vertical stem variant would close the gap with the 9s, since the 9's left-side loop vertical and bottom horizontal are features the 7 lacks, though linear weights on absence make that less clear-cut.

I'm weighing a 7 template variant with a vertical stem, since the 9s have a vertical stroke on the left that the current 7 lacks. For the 2→3 confusion, I'm considering whether the 3's bottom curve and the 2's base line up, though I haven't settled on a fix yet.

I'm raising beta to 12 to see whether the stronger regularization helps, and I'm also building a 7 variant and a 6 variant with a straight stem. Looking at the column sums next: the 9 and 3 predictions look high and the 1 count looks off, so I'm checking the class biases against the rough true counts.

I'm adjusting the class biases to compensate for the skewed prediction counts, pulling down the 1, 9, and 3 weights and nudging up the 8 and 4. I'm also setting beta to 10, adding a 7 variant with a vertical stem, and adding a 6 variant with a straight stem.
