I'm checking the accuracy at 76.5%, and I think the classifier is over-predicting class 6, since its column sums are large and it carries a bias of -0.3. The biggest confusions look like 3 to 5, 2 to 3, and 7 to 9. I'm also weighing whether the 4x4 grid with 8 orientations could reach around 90% with a trained linear classifier, and suspecting that the synthetic training data is what's holding it back.

I'm weighing whether to make the synthetic training data more realistic, with stroke thickness, endpoints, and conv responses that don't scale proportionally with length. I'm also considering a more faithful feature computation that uses max-pooling-like saturation rather than a soft-band sum, but I'm wary of effectively re-implementing part of the network on the synthetic inputs, so I'm leaning toward improving the approximation while staying geometric.

I'm working through the column sums to see how much class 6 is being over-predicted, and comparing those counts against the true class sizes to work out a bias correction. I'm also weighing the 2-versus-3 and 3-versus-5 confusions, which probably depend on the top strokes of those digits and need finer features than the current grid gives.

I'm adding up the remaining column sums for classes 3 through 9 and comparing them against the true class sizes (0 through 6 are listed as 980, 1135, 1032, 1010, 982, 892, 958). Class 6's predicted column of 1598 is far above its true count, which confirms the over-prediction I suspected.

I'm working out a bias correction from the column sums against the true class counts, using log ratios to see which classes are over- or under-predicted. Class 6 stands out as the most over-predicted, and the step size I'm using for the update is a rough guess.

I'm applying the bias update with a step size of 1, since the last step's bias change already improved class 1's column a lot and reduced class 9's. I'm keeping this step limited to bias calibration so I can see its effect on its own.
