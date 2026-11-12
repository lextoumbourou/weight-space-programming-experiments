I'm finding that the loss barely moves, so a temperature around 1.15 to 1.3 looks close to optimal. Next I want structural gains, and I'm considering hand-tuned pairwise corrections for the biggest confusions, like 2 to 8, 5 to 8, and 7 to 9.

I'm weighing whether the templates are too broad: the 8 template seems to pull in 2, 3, and 5 images. I'm also considering whether the 4x4 edge resolution is too coarse to separate 3 from 8, and whether blurred or multiple templates per digit would help.

I'm going to test a smaller epsilon, 0.012 instead of 0.025, and at the same time apply a half-step bias correction. The 8 class is overpredicted (1458 against about 1009 true), so I'm pulling its bias down, while 2 and 3 are underpredicted and get nudged up.

I'm going over the per-class bias numbers, checking the log-ratio adjustments for classes 1, 0, 4, 6, 7, and 9. Next I'm planning to try the epsilon change to 0.012 together with the bias correction, scaled by c=1.2.
