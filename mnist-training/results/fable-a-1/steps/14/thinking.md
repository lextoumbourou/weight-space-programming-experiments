I'm mapping each outcome number to its bit pattern: bit 0 is the top-left upper cell, bit 1 the top-left lower, and bit 2 the top-right upper. Then I'll list the eight combinations from none up to all three together. Next I'm starting to tally the row sums for each class.

I'm tallying the per-class fire rates for the top-left upper and top-right upper cells, and the zeros come out strongly active there, around 95% and 97%. The ones only reach about 16-20% on the top-left, and the twos show high activation on the top-right and a surprisingly strong 79% on the top-left lower half.

I'm checking class 3, where the top-right upper cell fires about 98% and the top-left upper about 59%. Class 4 looks different: the top-left lower cell is around 65%, while the top-right upper barely fires at 16%.

I'm working through the activation rates for classes 5 and 6: class 5 looks strongly tied to the top-left upper cell at about 93%, while class 6 splits between the top-left upper and lower cells at 62% and 79%.

Now I'm checking class 7, where the top-right upper cell fires about 98% and the other two cells sit around 38%. Class 8 looks strongly active across the board, with the top-left upper and lower cells near 94% and the top-right upper at 86%. Class 9 is starting to show a similar pattern, with the top-left upper cell at about 93%.

Now I'm comparing the top-left upper cell's firing rates across all ten classes, which look highly distinctive, and then doing the same for the top-left lower and top-right upper cells.

I'm checking how the top-right upper cell separates classes 4 and 9, plus several others, and the gap looks large in both directions. The next step is to measure the remaining cells (top-right lower, bottom-left upper and lower, bottom-right upper and lower) and then think about which extra feature to add for the joint picture.

I'm weighing what extra feature to add as the third one, perhaps a hole or orientation measure, and I'll decide that later. For now I'm setting the feature list to three cell pairs: (1,1), (2,0), and (2,1).
