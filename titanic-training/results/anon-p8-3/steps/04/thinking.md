I'm finding that the x2 > 0.475 split covers 107 rows, 59 of them class 1 (about 55%), while the remaining 493 rows have a 34.7% survival rate. The loss sits above the 0.666 baseline, so the linear correlation looks weak and the pattern may be nonlinear. I'm now checking Embarked_C, which shows about 19% of rows with a 55% survival rate.

The loss comes out worse with the one-hot-style value for Embarked_C, since its logit overshoots at 1.58 and the model becomes overconfident.
