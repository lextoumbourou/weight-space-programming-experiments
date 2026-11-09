Progress is slow at 76.8%, with the largest remaining confusions being 0→6, 2→3, 3→5, 5→3, 7→0, 7→9, and 9→7. The hole-cue bias of −.3 is too strong, so I'm going to try −.1 instead. For the 7→0 and similar pairs, the hole cue is pushing too hard, though the diagonal stroke in the 7s still looks like it passes through correctly.

I'm weighing a wider penalty for the 0 cue, but a 7's diagonal runs outside the center region, and I'm considering a convolution pattern that looks for ink on both sides with an empty center. The outer taps would be about 8 pixels apart, which might not cover the wider gaps in a 0, so this may need a different layout.

I'm working through a convolution layout that checks for ink on both sides of a 0 while keeping the center empty, using outer taps about 8 pixels apart and averaging over three rows. It should fire only when both sides are present, though the real separations in 0s may be wider than this layout covers.

I'm thinking the 0 template may be missing slanted ellipses: a tilted 0 has strong "/" energy along its long sides and weak vertical energy, so it looks more like a 6. I'll try adding a slanted variant to the 0 template.

I'm going to give the 0 template a sheared variant alongside the upright one, weighted evenly, so slanted zeros aren't pulled toward 6. I'm also lowering the hole-cue bias to 2.3 and its gain to 2.5. I'm wondering whether a slight global shear across all templates would match the typical right-leaning slant in MNIST.

I'm going to try a light global slant of about 0.1 across the digit templates, leaving the 1 alone, though that changes many things at once. Next I'm looking at the 2→3 confusions, which are high at 243: the 2 images are scoring higher on the 3 template, possibly because many 2s have a bottom stroke that curls up at the right end or a small loop, so the bottom-left corner is what I need to check.

I'm checking the 2→3 confusion next: the 2s have a diagonal running down to the bottom-left, while the 3s have nothing in that lower-left area, so I'm looking at whether a cell there can separate them.

I'm adding a cell in the lower-left where a 2's diagonal sits but a 3 has nothing, to separate them. For the 3 and 5 confusion, I'm adding an upper-right cell where a 3 has ink but a 5 is empty.

I'm placing a cell in the upper-left of the 7/9 pair to catch the 9's loop, which should be inked for a 9 and empty for a 7, and a top cell to catch the 7's bar.

I'm checking the remaining confusions: 1→2 and 0→6 should improve with the slanted zero variant, and the 8, 9, and 6 confusions are around 50–75 each. I'm also planning a small global shear for the digit templates, applied to every digit except the 1, with the shear added to each point's x-position from its y-position.

I'm setting the 0 template to an upright ellipse at half weight and a sheared version at half weight, with a shear of 0.4 for the second. The digits 2 through 9 get a global shear of 0.1, and I'm going to start coding that now.
