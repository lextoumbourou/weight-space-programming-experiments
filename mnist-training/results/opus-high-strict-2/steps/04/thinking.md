The loss has come down to 1.17 with accuracy holding steady after dropping the biases, and the main confusions are 4 mistaken for 9 and 1, 5 for 6, 3 for 5, 8 for 2, and 9 for 7. Next I want to add the biases back with more careful scaling, looking at the predicted counts per digit against the true ones and whether a half-strength log ratio fits better than the 0.8 factor I tried before.

I'm weighing a 0.5 scaling on the log ratio for the bias, since 0.8 overshot badly before and the larger logit spread here means the bias matters less. The bigger gain probably comes from the templates, so I'm checking how real MNIST 5s, 6s, 4s, 9s and 8s differ in stroke placement, like the 5's top bar and the 9's closed loop.

I'm weighing whether adding more orientations or offsets to the conv features would help, or whether averaging several templates per class could capture slanted and variant digit shapes better, since the fc layer is linear and can't take a max over variants.

I'm weighing whether to apply a single moderate slant to all the templates instead of averaging several variants, since averaging generated samples would stray into forbidden territory. Drawing one consistently slanted template per digit, possibly with a wider blur, seems like the cleaner route.

I'm settling on half-strength bias scaling, since the earlier 0.8 factor overshot badly and the larger logit spread here shrinks the bias effect. I'm also going to try a uniform slant on all the templates, shearing them by about 0.12, and redraw the 4 and 9 strokes so their shapes separate more cleanly.

Shear 1 gets its own adjustment: the vertical template becomes slanted, so I'll keep the original vertical line and let the shear produce the tilt. Next I'm working out the bias terms as half-strength log ratios of true to predicted counts, with digit 4 getting the largest positive value.

I'm going to compute the bias values directly from the counts, accepting that they may drift a little now that the templates have changed.
