The ink-only version lifted accuracy from 43.7% to 50.7%, and sevens are now handled well. Zeros are still the main problem, pulling many other digits toward the zero template. My guess is that the nearest-centroid templates put ink at stroke positions, while the real class averages are blurrier and dimmer, and that the feature magnitude makes distances very sensitive to how bold a digit is.

I'm weighing whether a cosine-style score, computed on centered and COM-fixed templates, would avoid the thickness sensitivity, since earlier that version pulled digits toward 8. The zero attractor may come from my templates being narrower than real digits, so I'm considering widening the loop templates for 9, 8, and 6.

I'm checking the typical MNIST digit widths, since my templates look narrower than the real ones. Real 0s run about 15 to 17 pixels wide, and my 0 is only about 12, which may explain why it pulls so many digits toward it. I'm considering scaling each template horizontally by a per-digit factor, starting with a wider 0.

I'm settling on per-digit horizontal scales, a bit wider for 8 and 9, and setting k to 2 for this step, with a possible move to 2.5 if thick digits still drift toward the zero template.

I'm going to widen the digit templates horizontally by per-digit factors, since real MNIST digits are wider than mine, and raise k to 2.3 at the same time, though changing both at once makes it harder to tell which helped.
