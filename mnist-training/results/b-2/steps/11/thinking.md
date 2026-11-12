Loss is at 0.97 with temperature 0.7, and I might try 0.5 later. For now the priority is accuracy. The biggest error source looks like 2s being confused with 3s, and many of those misclassified 2s have loops at the bottom-left. I'm considering how the features of a 2 and a 3 differ within the 4x4 grid, starting with row 3.

I'm comparing the 2 and 3 templates across the grid, and the key difference shows up in the lower-middle region: a 3 has an open bay there that a 2 mostly lacks. I'm wondering whether a template emphasis change, something like more horizontal weighting, could help separate them.

I'm weighing whether to measure how much each feature group contributes, for instance by zeroing the structural term, since steps 4-6 already showed gains. I'm also considering whether to sharpen the representation with extra orientation channels, or to improve the hole detector so it catches the small loops in 2s and 6s.

I'm now considering a narrower hole detector using only a 3x3 window, since a tiny loop's interior should show inward-facing edges from all four sides within the center cells.

Ruling out a tiny hole detector: at pool1's 2px resolution, a crossing stroke and a real loop look the same, so I'll drop that idea. Instead I'll test temperature 0.5 together with per-class bias calibration, using the prediction counts for 3, 0, 1, 9, 4 and 6 to see which classes are over-predicted.

Next I'm tuning the per-class biases, nudging 8 and 4 up and 3, 1 and 0 down since 3 and 1 are over-predicted. I'm also set on skipping the extra loop variant for 2s, because the last attempt lowered its accuracy. Then I'm looking at whether the 3 template is winning too often on 2s, 5s, 7s and 9s, which is where its zero-sum norm comes in.

I'm going to reduce the temperature to 0.55 and adjust the per-class biases, pulling down 3, 1, and 0 and nudging 8, 4, and 6 up, since those are where the predictions skew. I'll keep this change isolated to bias and temperature so any effect on accuracy is easy to read.
