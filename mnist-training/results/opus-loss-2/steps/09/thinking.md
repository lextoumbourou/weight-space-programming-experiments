Scaling still helps, though the gains are shrinking, so a larger model at 5.5 might be worth trying next. The bigger wins are likely to come from new features, so I'll focus there. Looking at the confusion pairs that remain, the ones with the most errors are 5→6, 4→9, and 3→5.

I'm noticing the 2→4 and 6→4 confusions look odd, since the bias toward 4 is large and seems to be pulling marginal digits into that class. That suggests the 4 template is weak for real 4s. Real digits also vary in width, so a single template per class may be too rigid, though I'm wary of generating extra variants in a way that edges toward inventing training data.

I'm weighing whether to widen the template blur, but that drifts toward manufacturing variants, so I'm leaning toward designing explicit hole detectors instead. Loops show up in 0, 6, 8, 9 and sometimes 4, so a center-minus, four-sides-plus detector in the pooled maps could separate them directly.

I'm checking whether a hole detector could separate the loop digits, since it would catch the small loops in 6, 8, 9 and the closed top of 4, but the big loop in 0 is too wide for the pooling window. Open-bowled 5 and 3 would not trigger it, so this might help with 5→6 but not much with 3→5.

I'm picking through the remaining confusion pairs, and a hole detector looks like it would help with 9 and 8, which both have loops that 4 and 2 lack. The open 5 and 3 wouldn't trigger it, so it may not do much for 3→5. I'm weighing whether to shrink the ink channels to two and use the freed slots for small and large hole detectors, since the big loop in 0 is too wide for the pooling window.

I'm defining a small hole detector: a 5-cell ring around an empty center, with the four sides grouped to check that the loop is closed.

I'm working out the hole detector's weights: a negative center with positive ring cells, so the four sides sum to a clear signal. The ring at distance one is too tight for holes this small, so I'm considering a single-pixel center and eight neighbors instead. Blurring by the 3x3 mean would erase the holes, so the detector should read unblurred ink, where a gap of a pixel or two in the pooled map still survives.

Writing hole detector weights...

Still sketching the hole detector's weights: a ring of positive cells at distance two around a negative center, so a closed loop of about 8 pixels should respond strongly while a single stroke only gets a partial score.

Keeping the hole detector in view: a closed loop should give a big response, an open bowl only a partial one. Setting the bias high enough to require nearly all four sides means imperfect loops would be missed too, so the detector will be noisy and the fc weights have to cope with that.

Next I'm setting the channel layout: keeping the orientation and arc channels, cutting the ink shifts to two, and adding two hole detectors, one large and one small. For the small one, the center gets a strong negative weight and the eight neighbors a positive ring, so a closed loop lights it up and a single stroke through the middle suppresses it.

I'm settling the hole detector's weights against a sum-of-sides threshold, and the left and right sides come to about 4 against a bias of 4.5, so partial loops stay below the firing line. I'll rely on the fully connected layer to handle the imperfect cases.

I'm settling on the hole-detector layout for the loops, and I'm sizing the big one against the 5x5 pooling window to see whether it fits.

I'm sizing the loop detectors against the digit shapes: the upper loop of an 8 and the loops in 6 and 9 should fall in the larger ring, while the 0 is too wide for it. The closed 4 might only trigger the smaller detector. Since real loops vary in size and position, I'll model each one as a Gaussian at its center.

Working out the hole detector's weights for the final layout: a Gaussian bump centered on each loop, with the amplitude set by how closely the loop's radius matches the detector's ring. The 0 has no detectable loop, so it relies on the ink channel's negative weight at the center instead.

Setting the hole-detector scale and the bias values next, and I'm sketching out what the per-digit hole templates should look like.

Working out the loop detector for each digit: I'm placing a loop of about radius 5 at (13.5, 13) for the closed 4, a radius-5 loop at (14, 18.3) for the 6, two loops for the 8 at different heights, and two overlapping loops for the 9.

Writing the hole detector's kernel weights now: a strong negative center, negative neighbors, and a ring of positive cells around the edge.

Still tuning the hole detectors: the small one gets a strong negative center with a positive ring, and I'm checking that its bias sits just above the partial-stroke score, roughly three-quarters of the full ring.

Writing the hole detector's weights and the bias for each kernel now...
