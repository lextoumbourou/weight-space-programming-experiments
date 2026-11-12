Overall accuracy is at 72.4%, with the largest confusions being 3→5, 5→8, and 8→3. Now I'm looking at why 1 is still being mistaken for 2 in 117 cases, since a slanted 1 may be picking up the diagonal of 2's template.

I'm checking whether the 1 template's thin diagonal, at about 59°, is close enough to 2's diagonal to explain the confusion. I'm also weighing whether raising the bias for 1 would just add false 1s from the 8s, since that column is already nearly full.

I'm considering whether a slightly tilted 1 could push the 2-template's diagonal response high enough, and whether an 8-orientation layout would separate the angles better, though it would cost column resolution. I'm also weighing 3→5 as the biggest confusion, since the top half of a 5 looks a lot like a 3.

I'm considering whether a sharper template, with the blur reduced from σ 1.5 to 1.0, would help separate the left and right sides, since the 6x6 max-pooling and 2-pixel stride are already smoothing the maps heavily. I'm also planning to nudge the class biases, with the column totals for 3 and 5 in view.

I'm comparing the column totals for 9, 2, and 8 against the others, and I'll test the sigma change on its own first, keeping the biases as they are.
