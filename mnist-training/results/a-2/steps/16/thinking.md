I'm decoding each class as 3i+j and tallying how often each digit's top and bottom loops show up. For 9s, about 37% have a top loop, with most showing none; for 6s, roughly a quarter have bottom loops. The 8s are mixed across several patterns, with about 40% carrying some loop.

Checking how often the loops appear across the digit classes: 0s almost never show one, so the 0 class is too large for this detector. The strict loop criterion is selective but only catches a quarter to two-fifths of the cases it should, so I'm weighing a second loop detector with a smaller radius to raise sensitivity.

I'm weighing a second loop detector with a tighter radius, since its sides would sit closer to the pooled cell offsets. Lowering the threshold would make it more sensitive, but a three-sided open arc at full strength would then clear it, so I'd need tilted variants to keep those false positives out.

I'm working through a loop detector built on diagonal cells at radius about 1.4 cells, which puts a ring of roughly 3 px at the right scale. A second detector with four diagonal positions and a threshold of 3.0 would sit alongside the existing one, and I'd let the network weigh both separately. I'm also checking whether a stroke of width 2-3 would still register strongly enough at the center, where the ring is only about 2.8 px out.

I'm looking at which loop detector to swap out. The ∪ detector seems the weakest candidate, so I'm considering replacing it with a diagonal loop built from four cells at about 1.4 cells radius. For the ┐ corner detector, the 7-versus-9 confusion (113 and 69 errors) is the stronger motivation. I still need to decide whether the ⊃ detector should stay, since it is shared between 3 and 5.

Writing the corner detector code...

Still writing corner detector...

I'm weighing how to handle the 9s' rounded top-right corner, since a standard corner detector would fire on the loop itself. I'm considering a center term that rewards ink at the corner point, which a sharp 7 would have and a rounded 9 would not.

I'm adding the center-ink bonus for the ┐ and ┌ corner detectors, and setting their thresholds to match the new maximum scores.

I'm listing the remaining detector templates: a small loop detector with class-specific placements for 9, 8, 6, 0 and 2, and a main loop detector where 9 and 6 have the strongest top and bottom positions.

I'm settling on the detector templates now, with the diagonal loop and the two corner detectors as the candidates, and I'll set each base rate near 0.02 per cell for non-loop digits.
