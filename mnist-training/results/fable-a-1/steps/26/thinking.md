I'm decoding the three parity checks and working through how each one combines the odd-indexed and other offsets. For class 0, I'm summing the selected values to get f0 and starting on f1.

Still tallying the remaining classes, checking each sum against its normalizing total.

Still tallying the remaining classes, checking each sum against its normalizing total.

I'm working through class 9 next, summing the selected entries for each of the three features. The diagonal features look less discriminative than the others, with most values sitting in the mid-range, so I'm starting to doubt they carry much signal.

I'm weighing whether the remaining diagonal features are worth five more steps, since D1(0,0) only separates a couple of classes. Other options are the other checkerboard half of H/V, finer corner features, or re-measuring the hole, and I'm comparing which would help most against the main confusions, with 4 being the worst class.

I'm checking whether 4 and 6 can be told apart by the H/V cells, since several of them separate them well, yet they still get confused 88 times. I'm wondering if the hand-built diagonal templates are adding noise for those two classes, or whether the corner zones and the lower hole are the real problem.

I'm weighing whether to drop the hand-built diagonal templates or measure the other checkerboard half of H/V instead, since the diagonal features look weakly informative. The "\" orientation might separate digits better than "/", but five more steps for diagonals seems less valuable than the extra H/V resolution.

I'm weighing whether to measure the remaining diagonal cells or spend the steps on other feature families, such as the upper hole or finer corner rows. Diagonal features look like a different information source even if each one is weak, so I'm leaning toward measuring all the remaining ones in five steps and integrating them before moving on to the corners.

I'm going to finish the remaining diagonal cells in two batches: first the "/" set of six, then three of the "\" cells, leaving one slot open for an upper-hole measurement.

I'm picking the next diagonal cells to measure, D1(1,1), D1(1,3), and D1(2,0), to finish the "/" set.
