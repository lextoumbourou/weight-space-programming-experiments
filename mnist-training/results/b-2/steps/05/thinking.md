I'm still working on the 8 class, which is getting only 60 correct. It keeps getting predicted as 7, 9, 1, or 2, so I suspect my 8 template is off. Real 8s seem narrower and more slanted than my template's width of 10 to 19, and my hole detectors may be too small to fire on the loops.

I'm weighing whether the 8 template is simply too wide, or whether my hole detectors fail on the small loops, since a pool1 center unit may see edges from both walls and get penalized. Evaluating these features in my head is hard, so I'm considering a diagnostic that uses fc to check how informative a single channel is. Another option is to replace the current design with shift-tolerant template matching at higher resolution.

I'm checking whether the hole detector's edge response is strong enough to register on a 2px stroke, since the edge kernel's positive side may only partly cover the ink.

I'm now checking the hole detector's response on the 9's loop: the interior is only about 4 to 6 pixels wide, so a center pool unit would see edges from both walls, and their contributions would be weak and roughly cancel out.

I'm checking the hole detector against small loops: an 8's interior is only about 3 to 4 pixels wide, so the center pool unit won't go quiet and will take a modest penalty. The left wall's edge response should land in the outer columns of the pool window, roughly one unit off center.

I'm working out the rough numbers for the hole detector's signal: the wall edges come to about 0.2 after the bias, which is weak. Max-pooling only brings it to around 0.2 to 0.4, so its logit contribution is small next to the orientation features. I'm thinking about raising the structural weight and lowering the hole bias, though I'm unsure whether that would help or hurt.

I'm going to try beta=8 and see if the structural features then matter, though I'm also wondering whether the 8 class is failing for a more specific reason. The 8 template may be built around full-width shapes, while real 8s are narrow and sit mostly in the central columns, so their diagonal energy looks a lot like the diagonals in 7s and 9s.

I'm considering a more principled scoring approach, since the classifier uses identity covariance with template means rather than something closer to LDA. The predicted-class totals are lopsided, with 7, 1, and 9 overpredicted and 8 almost never predicted, so I'm thinking about per-class bias adjustments: a boost of about +1.5 for 8 and small penalties for 7, 1, 9, and 3.

Now I'm sketching the 8 template as a narrower, slanted shape, with a small top loop and a larger bottom loop that cross at the middle, and I'm writing out the path points for it.

I'm considering whether the 8 template should be a narrower, more slanted shape, and I'm also thinking about adding a separate, more steeply slanted 1 variant to stop slanted 1s from being pulled toward 7.

I'm going to bump beta to 8, lower the hole bias to -0.8 and the bays bias to -0.5, and redraw the 8 template. I'll also add a steeper-slanted 1 variant, and nudge the fc bias for 8 up to +1.0 with the rest at zero.
