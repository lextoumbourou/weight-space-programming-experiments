I've overshot on three classes: 8 and 5 collapsed, and 6 is over-predicted at 1624. Classes 0, 2, 3, and 6 did improve, which is something to keep. With only two steps left, I need to make careful corrections rather than big swings.

I'm weighing the step 13 changes against the best so far at step 12 (58.3%). The collapses of classes 8 and 5 trace back to the λ jump to 0.56 and the multipliers stacking on it, while class 6 went up anyway, likely because 8 and 5 vacated their mass. For each class I'm interpolating a λ that brings its count near target, which gives roughly 0.50 for class 6, 0.44 for class 0, about 0.50 for class 8 and 0.51 for class 5.

I'm settling on per-class λ values to bring the counts near target: class 1 goes to about 0.53, class 2 to 0.545, class 3 to 0.545, class 4 to 0.47, class 7 to 0.49, and class 9 to 0.52. Classes 2 and 3 are over-predicted because 5 and 8 vacated their mass, so I'm pulling them back toward their targets. I still have to check how the last few adjustments interact with the collapse of 8 and 5.

Going with the interpolated calibration for step 14: class 6 at about 0.50, classes 3 and 2 at about 0.54, since the classes that were inflated should deflate once 8 and 5 send their images back. If step 14 comes out worse than step 12, step 15 goes back to step 12's settings with only minimal tweaks, because the final test runs on the last step's network and that has to be safe.

I'm setting the base multiplier to 1 and folding each class's absolute λ directly into its multiplier, so the per-class values apply without a separate scale factor.
