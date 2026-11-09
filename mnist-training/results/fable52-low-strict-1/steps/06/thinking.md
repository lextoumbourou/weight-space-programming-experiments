Negative examples barely moved the numbers: the 4→9 pair still sits at 332, and the others stay high too. That points to something systematic, maybe in how the templates line up with the features or in how the feature behaves, and I'm wondering whether my centre computation is introducing a consistent positional offset.

I've confirmed the geometry checks out: the conv, pool, and centring offsets all line up, and the window orientation is consistent. So the templates themselves are fine, and the real issue must be in how the scoring model treats the mismatch between the drawn templates and the actual feature magnitudes, especially for pairs like 4 and 9 that differ only in the top bar.

I'm weighing a different scoring approach: dividing out the average template so the weights become discriminative, though I already know subtracting a shared vector from every class leaves the argmax unchanged. A Euclidean nearest-prototype form might fit better, but it needs an estimate of the feature scale.

I'm weighing a cosine-style scoring instead: normalising each template and features so the score is scale-free, which sidesteps having to guess the feature magnitude.

I'm sticking with the partial centring and turning to the discriminative details. The negative examples may be too weak at the current strength, and at step 4 the 4→9 pair was mostly lost to 1 and 8 because of the class balance. With the zero-sum form I can afford a larger negative weight.

I'm going to try zero-sum scoring with a negative weight of about 0.12 to 0.15, since the earlier 4→9 failure looked like the negatives being too weak. For 8, the recall problem and the confusions with 1, 9, and 7 suggest the template is off: real 8s are narrower and have crossing diagonals at the centre, so I'm thinking about adding those and tightening the loops.

I'm deciding on the negatives for the 1 template: horizontal strokes at the top and middle, maybe the bottom too, though real 1s rarely have a base. For 3, I'm adding a negative stroke in the lower-left to push down the 2→3 confusion.

I'm working out the negative stroke for the 3 template so it doesn't collide with the lower arc of the 2's base. The 2's diagonal ends near the bottom-left, while a 3 has its right-side vertical at the lower right, so I'm looking at placing the negative there instead.

I'm moving the 3's negative stroke to the lower-left middle, where the 2's diagonal runs, and shortening the 3's lower arc so it stops at 150°. Then I'll test a 5→6 fix: the 6's loop closes at the lower left, and the 5's negative sits at the same spot, so a stronger negative weight should show whether that helps.

I'm adding a negative horizontal stroke in the upper right for the 6, since its stroke starts at the top right, and I'm also raising the negative weight to about 0.13 because the 9 keeps pulling in too many false positives.
