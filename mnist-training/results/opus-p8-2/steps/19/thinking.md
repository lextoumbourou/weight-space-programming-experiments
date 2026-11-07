Progress has been small, so I need a bigger idea. I'm wondering whether the hand-crafted features themselves are the bottleneck, since they may be limiting what the system can learn from templates. Accuracy sits at 72%, and the weakest classes are 8, 9, 2, 4, and 7. I'm also considering whether the conv1 orientation filters, a zero-mean ridge detector, are picking up stroke edges too.

I'm checking whether the thick-stroke case holds up for the horizontal detector, and it does: a vertical stroke gives ink in every row, so the zero-mean filter cancels it out. I also wonder whether max-pooling and the coarse 4x4 grid are limiting what the features can distinguish. The bigger lever seems to be per-class adjustments driven by the confusions, starting with 8 versus 9, where the lower-left ink should favor 8 and count against 9.

I'm weighing a pairwise fix for the 8-versus-9 confusion, but adding more of the template difference just scales the same direction and won't change which way the errors fall. Fixing it would take something the templates don't encode, and I can't see that from here.

I'm thinking about running ablations on the feature groups to see which ones actually matter, since we have enough steps left to test a few. Another option is a cleaner ink representation with less dilation, or a narrower template width, though I'm not sure the blur is the real issue yet.

I'm working out how far a single stroke's ink reaches into the grid cells. The detector gives no response a pixel beyond the inked area, so a cell only fires when the skeleton lies within about 2.7 pixels of its window.

I'm thinking about adding more style variants for the under-recalled classes, especially 8, 9, 2, and 7, and I'm checking whether any of the current endpoint weights are pushing 4 too far for anything with endpoints. I'd like to test that with an ablation, zeroing the endpoint contribution, to see how much it actually matters.

I'm considering whether a cheaper structural change could help the 8s, since their two small loops may often go undetected, which would leave the class without enough evidence. I'm also weighing a separate hole weight per class, though that feels like it may not be worth the complexity.

I'm thinking about replacing the 5-pixel ring detector for small holes with a plus-shaped empty-pixel detector, since 8, 9, and 6 can have interior loops only a few pixels wide that a 3x3 patch never fits inside.

I'm working out whether a plus-shaped empty-pixel detector can catch the tiny interior loops of 8, 9, and 6. The ink from the surrounding strokes would need to add up past the firing threshold, and when only the nearer neighbours are inked, it falls short.

I'm going to build a tiny-hole variant of the detector: swap in the plus-shaped empty-pixel channel for the small-hole feature, with weights of 0.8 on the ±1 and ±2 neighbours and a bias near -4.4. A full ring should clear the threshold, while a three-sided shape or a corner should not.

I'm weighing a tighter bias for the small-hole detector so that a three-sided shape fires, but the 2's top arc might trigger it too, so I'd rather test it than guess.

I'm keeping the small-hole detector on the original 5-pixel ring channel and leaving the other settings alone, then I'll see what that does.
