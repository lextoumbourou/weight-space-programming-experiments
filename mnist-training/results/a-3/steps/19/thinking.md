Classes 2 and 7 are now predicted far more often, while 8, 9, 4 and 6 have nearly collapsed, which looks like a calibration issue with the bias term rather than a loss of discriminability. The shift needed to correct it is large. Rather than guess the bias values, I'll compute them directly from the confusion matrix.

I'm working through the per-class bias corrections from the column sums, and the shift for class 8 looks very large: 39 predicted against roughly 1009 expected, a log ratio near -3.25. Because the bias doesn't map one-to-one onto prediction counts, I'm considering a scaled-down correction, around 0.7 of the full log adjustment, with an intermediate b2 value instead of reverting to zero.

I'm settling on a bias correction of b2 = -0.8, with class 8's shift capped at 1.5. Once those corrections are in, I want to see how much discriminability is left, and I'll keep going only if calibrated accuracy clears 75%.
