Age might not be a continuous feature at all, since most of the inputs look binary, so I'll stop searching for a left tail. The better use of time is tuning the linear coefficients on the stronger features, testing each one with a quick 1D sweep.

I'll run the sweep on x9 next, moving its coefficient from 0.2 to 0.45 to see how the loss responds, since with 25 steps I can afford single-step perturbation tests to read off each gradient sign.
