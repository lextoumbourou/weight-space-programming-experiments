I'm at 85.06% with loss 0.5016, and the single-row features gave about +1.4%, so I'll keep adding more of them. With 20 steps left, I'm planning two probe steps before each classifier run, and holding back the last four for tuning. The biggest remaining confusions are 3→5 at 122, then 0→2 and 7→9.

I'm going through the remaining confusions and checking the column totals against the true counts. Column 5 is over-predicted by 93 and column 3 is under-predicted by 36, so I'm nudging biases to correct that. I'm also thinking about which single-row features could separate 3 from 5, like the left versus right halves of the top row.

I'm now weighing single-row features against the remaining confusions, like which row-wise halves separate 1 from the others, and checking whether left and right splits on row 2 help with the 0 and 2 mix-ups. For 3 versus 5, I'm considering a left-side split on row 1 as a candidate feature.

I'm now checking which top-row split separates 3 from 5: 5's top bar reaches right, while 3's top arc curves down on the right side, so the right half of row 0 might be the telling cell.

I'm checking which diagonal cell in the middle rows separates 8 from 5, since the 8's crossing should show up more strongly there than the 5's.

I'm checking whether "/" diagonal cells in rows 1 and 2 on the right and left sides separate the 8 from the 5, since the 8 has strokes there and the 5 does not.

I'm now picking out the specific cells that separate 8 from 5 and 3: a "/" diagonal in the right upper loop, a "/" in the left lower loop, and a "\" in the left upper loop.

I'm checking whether the diagonal cells on the right side of the lower rows separate 8 from 5 and 3, since the 8's lower loop and the 3's and 5's bowls each have a "\" stroke there. I'll probe the "/" cells on the right of row 1 and the left of row 2 next, plus the "\" on the left of row 1, and then test them against a 0.6 threshold.

Next I'm testing the right-side "\" cell in row 2 and the two top-row horizontal splits, left and right, to see whether they separate 3 from 5. Then I'll run the classifier with the bias tune.
