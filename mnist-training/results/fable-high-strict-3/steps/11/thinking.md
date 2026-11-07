The model collapsed into class 4: 54.2% accuracy, with 4 absorbing 2328 predictions, mostly 9s, 7s, 2s, 6s and 5s. I want to know why that happened. The changes I suspect are dropping the D features, which might have been helping with 4, and extending the ink.

I'm checking whether the 1's bias from the forbidden-region compensation is the real driver: its side penalties now span more rows, which gives it a large boost that could push other digits into 1.

I'm weighing whether to roll back to the step-9 setup, which scored 57%, and make smaller changes, since I have only five steps left and can't cleanly separate the effects of the extra bottom rows, dropping D, and the higher κ. I'm also questioning the forbidden-region compensation formula, which seems too crude to hold up at the larger ink extent.

I'm weighing whether the 10-row ink is worth keeping: classes 0, 1, 3 and 4 gained, while 2, 6, 8 and 9 lost, so the bias compensation may be the real culprit rather than the stroke extension itself.

I'm weighing whether the 10-row version can be salvaged by recalibrating its bias, or whether I should go back to the step-9 config that scored 57%. Checking the 9→4 confusion: 9s have loops at the top-right, which should fall outside 4's forbidden top-center region, so that penalty does not explain the confusion.

I'm reverting to the step-9 setup, which scored 57%, and applying a gentler bias adjustment along with a couple of region changes. I'm counting the step-9 class totals to calibrate that bias.

I'm listing the per-class calibration offsets, computed from the step-9 counts with the same small adjustments as before, which gives values like 0.92 for class 0 and -0.46 for class 6.

I'm adjusting the forbidden regions for a few digits: widening the left side of 2 and adding a lower-right patch, narrowing 3's left edge, and adding small waist regions to 8, aimed at the 8→2 and 3→5 confusions.

I'm thinking about per-region weights, so the upper-right of 5 counts more heavily to separate it from 3. I'm also checking whether 0's confusions with 6 and 8 are already covered by the center hole region.

I'm working out how to tune the forbidden-region weights and the bias for the 0 and 8 confusions, using a fixed 0.12 compensation and reweighting the 6 and 8 regions.

I'm reverting to the step-9 configuration with its known 57% score, and applying the calibrated per-class biases along with the region tweaks I had in mind for 2, 3, 5, 8 and 9.
