I'm at 82.65% with a loss of 0.55, and raising gamma seemed to help, so I'll try gamma 0.85 with alpha 2.5. The big loss drop from alpha is probably only partly due to gamma. Getting past roughly 85% will likely need structural changes, and I'm looking at the conv2 channels, which seem to duplicate the broad and sharp features, to see whether they could capture something more informative.

I'm weighing ways to make the features more informative, such as having the conv2 channels capture things like endpoints or curvature, or splitting them across a finer spatial grid. I'm also considering whether to shift the sharp channels' taps, but for now I'll keep tuning the shrinkage, alpha, and bias.

I'm checking the bin counts and confirming they sum to 10,000. Since the gamma change also shifts the predicted counts, I'll apply the bias correction at a step size of 0.5, and I'm setting gamma to 0.85 with alpha at 2.5 next.
