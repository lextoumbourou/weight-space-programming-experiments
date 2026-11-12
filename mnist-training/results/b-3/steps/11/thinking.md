The hand-drawn approach is stuck around 62.8%, and its loss of 1.59 is worse than the earlier step's 1.14, so the updates aren't reliably helping and the model is overconfident. I'm going to look for a stronger handcrafted method that could reach 85% or more, since class-mean template matching on raw pixels already gets about 82%. I'm wondering whether I could describe those class-mean images directly.

I'm wondering whether the hand-drawn class means could be described accurately enough, since the real issue may be the comparison method: correlation against centered, unnormalized templates. I'm also considering a simple test with ink-only features at finer resolution, using a 10x10 grid of max-pooled ink at 2px spacing.

I'm weighing whether a nearest-centroid classifier on a 10x10 max-pooled ink grid could work, with the templates coming from hand-drawn prototypes blurred to match positional variance. My guess is around 70% for the raw prototypes, and I think faithful prototypes could reach 75–80%, since the current ~65% is likely dragged down by orientation effects.

I'm thinking the nearest-centroid distance reduces to a dot product with the class mean plus a bias, so the mean's scale matters less than the calibrated bias term. The alternative is to make the features have a known scale: a 4x4 max over blurred ink should sit around 0.8 wherever a stroke passes through, so the template values can be read as the probability that ink is present in each window.

I'm weighing whether the feature scale can be pinned down, so the distance classifier gets calibrated biases rather than tuned ones. The idea is to model each template value as the chance that ink sits in a window, with blur width standing in for writer variability, so the score is a scaled squared distance and the bias term is principled. I'm starting with a scale of about 1 and wondering whether ink-only features are expressive enough to carry the task.

I'm checking the 5x5 convolution's row offsets, confirming that offsets 0 through 3 are enough and working out which pool1 rows each pooled cell reads from.

I'm checking the offset choices for the conv2 channels: with four row offsets and four pool2 positions, the combinations collapse to fewer distinct pool1 rows, so I'm considering restricting the offsets to a range that covers rows 1 through 9 without repeats.

I'm settling on four channels with row and column offsets of 1 and 2, which gives an 8x8 grid of pooled windows at stride 2. That covers the image well, so the other twelve channels are free for something else, such as orientation features.

I'm considering using conv1 to produce more distinct feature types, and I'm thinking of having the 16 conv2 channels cover ink, horizontal, vertical, and combined diagonal responses, each as an 8x8 grid from four channels.

I'm sizing the orientation templates: a window's value is taken as the strongest stroke response nearby, scaled by 0.7 and fading with distance over σ=2.

I'm settling the window geometry: the value is the maximum stroke response within the window, with the window's half-width of about 2.5 px discounted and a Gaussian of σ=2 for writer variability. Amplitudes are 0.8 for ink and 0.65 for orientation.

I'm checking which pool1 rows the window offsets land on, and sorting out the input pixel centers for each window. The first offset set gives an asymmetric spread that cuts off the top edge, so I'm shifting to offsets two and three to center the grid.

I'm weighing whether the window offsets should shift to {2,3} so the grid is centered on the digit's mass, since {1,2} would skew the coverage upward and leave the bottom rows underrepresented.

I'm settling the offsets at {2,3} so the windows cover rows 4 through 25 with the grid centered on the digit. Next I'm setting the classifier's scale: a squared distance of roughly 16 between an image and a class mean, with class differences of 2 to 4, points to s around 0.7. I'm keeping in mind that the amplitude assumptions for the orientation features may be off, as they were in the earlier step.

Writing the feature-extraction code now...

Still working out the template values: the tuning falls off with the angle difference, so a diagonal stroke gets only a partial response from each of the two diagonal channels, and I'm summing them. I'm about to pin down the ink amplitude from a blurred three-pixel stroke.

Writing the feature-extraction code now...
