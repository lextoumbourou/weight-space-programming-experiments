The penalties on the left-middle cells are hitting the 2s, 3s, and 7s hard, with the 2s, for example, getting pushed toward 8 and 9 when they should stay correct. That means real 2s, 3s, and 7s do have ink in those cells, so my templates may be misaligned horizontally.

I'm checking whether the 3s and 7s really have ink in those left-middle cells, given where their strokes should sit. The horizontal alignment of my templates may be off, though a 3's junction should land further right than those cells reach.

I'm checking the penalty math on those cells: a single column of overlap with a 3-wide stroke still gives a sizable response, so contact at the edge of the box is enough to trigger the penalty.

I'm realizing the hand-set negative at (2.4, 1.4) was the real problem, since that cell spans enough columns to catch the center strokes of 3, 7, and 2 at once. I'll drop those negatives and go back to the step 9 config, keeping the step 10 bias changes in mind. Those results can't be judged yet because the damage from the negatives swamps them. For 7 alone, I might try a more careful, cell-aware negative over the left-middle region instead.

Checking the 2s' diagonal against the grid cells, the (2.9, 0.9) point seems to touch the edge of one cell only mildly, but the larger cell over the 2's own lower diagonal would penalize the digit it's meant to recognize. The 7's diagonal stays clear of those left-middle cells, so the bar's left end should be harmless for it.

Going with the step 9 setup, I'm only keeping the hand-set negatives for 4, 1, and the 7's horizontal bar, then adding 7-only ink penalties on the left-middle cells at a lower strength. The step 10 bias changes stay in, since 7 was under-predicted and needs the boost.

I'm setting the bias values to the step 9 numbers with the small tweaks: 0 at 1.38, 1 at -0.86, 2 at 0.50, and so on through 9 at 0.36.
