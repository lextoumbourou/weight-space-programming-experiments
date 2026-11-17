The texture feature is above 0.5 for almost every image, so the threshold T has to sit well above my earlier estimate. Working through the loss change, the squared-deviation term is about 0.24 plus twice the mean shift, which puts the RMS of F minus 0.5 near 0.5 or higher.

I'm re-estimating the threshold at around 1.0, since the texture values sit well above my earlier guess, and the low-tail counts suggest cats may have less texture or a wider spread. I'll re-probe at t = 1.0 with w = 1 to test that, keeping the probe clean and separate from other checks.
