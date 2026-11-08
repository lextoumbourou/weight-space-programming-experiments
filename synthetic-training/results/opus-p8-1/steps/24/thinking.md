The result came in better than predicted at 0.4841, and the gain over the null baseline suggests the signal is stronger than I expected. I'm weighing whether to raise just {1,4} to -0.6 while leaving {6,11} at -0.3, or to double every coefficient to -0.6, which would add a noticeable quadratic cost.

I'm weighing a bisection by removal: dropping the x6 and x11 terms and seeing whether the loss rises, which would show they were helping.
