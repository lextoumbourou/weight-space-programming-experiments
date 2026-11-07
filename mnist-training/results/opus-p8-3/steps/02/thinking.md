Too many digits are being guessed as 1, which I think means the penalty term is too strong for the features, so sparse digits win out. 8 is almost never predicted and 9 only rarely, and 7 is over-predicted. I'll drop κ to about 0.35 and raise β to 0.6, and I'm also wondering whether per-digit normalization of the bias would help.

I'm considering adding a 3x3 spatial blur in conv2 so the features tolerate shifts and slant, but that would change the feature magnitudes, so I'll hold off. For now I'll change just one thing, κ, and lower it to 0.4 while raising β to 0.6.
