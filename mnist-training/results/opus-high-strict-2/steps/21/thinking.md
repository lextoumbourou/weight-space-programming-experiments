Realistic drawing is working, so now I'll apply the same realistic redesign to the other digits that are getting confused. The biggest confusions are 3 read as 5, 8 as 9, and 5 as 6, with 9 as 3, 6 as 4, 7 as 3, 4 as 9, and 2 as 3 following. I'm starting with 9, looking at how its loop and stem should be drawn.

I'm checking the 9 loop geometry against the stem and noticing that its loop should be an oval tilted slightly, with the stem slanting down from the right side. Then I'm turning to 6, where the loop is the lower part sharing the left stroke rather than a separate circle, and to 5, where the bowl should curve out from a top bar and stem.

Now I'm reconsidering the 7, which keeps getting read as a 3, and the 3 template seems to be pulling in 7s, 2s and 9s. I'm wondering whether the real issue is how the template's topology is shared across these digits.

Now I'm working through the stroke paths for the 2 and 4, with the 2's neck curving down to a flat base and the 4's left arm running more vertically into the crossbar. The shapes already look close to what I have, so the geometry alone probably isn't what's causing the persistent confusions. I suspect the limit is in the linear classifier itself, so I'm considering refining the ring and hole detectors instead.

I'm weighing whether a nonlinear "open-top" detector could separate 4 from 9, perhaps by pushing the top ring weight for 4 negative, though that risks hurting closed 4s. For 3 versus 5, a conjunction feature requiring a vertical stroke on the upper left with none on the upper right might help, but a plain ReLU on the difference adds little beyond what the linear layer already captures. I'm also considering using all four orientation offsets, sixteen channels instead of eight, and dropping the ring detector.

I'm weighing a few cheap generic tweaks next, like nudging the conv1 bias and the sigmoid temperature, since each test takes a step but might add half a point or so. I have about five steps to find a gain of at least 0.5 over the earlier score.

I'm going to try narrowing the 3 template again, since its wide spread was pulling in 7s and 9s, and I'll keep the realistic 5 and 6 changes minimal.

I'm checking the leakage of the horizontal kernel on a diagonal line: its row profile sums to zero, so a 45° stroke gives almost no response. That means the cos⁴ orientation weighting overstates diagonals, and something like a cos(2Δ) falloff would fit the kernel better.

I'm thinking about narrowing the 3 template and reshaping the 2's neck into a curve, and I'm also considering a small negative top-ring weight for the 4 so it separates from the 9. I'll keep it to a moderate change, since each adjustment here carries some risk of hurting the closed 4s.
