Now I'm weighing whether the features are actually meaningful, since the process is slow at 61%. The worst remaining cases are 7, 9, 8, 2, and 6, with 7 looking like the main problem. The template for 7 may not match well, and I'm wondering if my shear pushed its diagonal more vertical than it should be.

I'm checking the template orientation convention against the conv1 kernels, and the horizontal and diagonal cases both line up. The window-to-channel reshape also looks correct, so the mapping may not be the cause of the 7 errors.

I'm checking the window-to-channel mapping again: the conv2 output indices and the tap ranges line up with the pool1 rows and conv1 centers, so the indexing holds. That leaves the conv1 responses to thick strokes or ReLU biases as the more likely source of the 7 errors, and I'm still unsure how to verify that.

I'm considering whether to lower the number of orientation channels to four broader ones to make the features less sensitive to small angle changes. The templates' blur may already cover that, so the bigger question is whether single prototypes per class are the real limit, and whether per-class bias tuning against the confusion pattern could help. The predicted class counts are uneven, with 5 and 3 over-predicted and 7 under-predicted.

I'm thinking about per-class bias tweaks to offset the skew, since 7 is badly under-predicted and 5 and 3 are over-predicted, but I'd rather fix the templates for the problem classes. The 6→5 confusion is the one I'm looking at now, since a 6's loop sits lower and its stem leans more to the left than a 5's.

I'm thinking the template fixes are probably guesswork, so a bigger payoff might come from better features: wider spatial pooling and blurrier templates so matching depends more on coarse layout. I'm also wondering whether a non-geometric approach with more prior knowledge would serve better than hand-built prototypes.

I'm going through the remaining digit templates against what typical MNIST shapes look like: 2 with its top arc and diagonal base, 3 with its middle cusp, 4 with the left stroke, crossbar and right stem, and 5 with its top bar and lower bowl.

I'm checking the mapping from thick MNIST strokes to the conv1 orientation channels, since a thick stroke's edges may fire several neighboring orientations at once and blur the features. I'm also looking at the stroke geometry of the 6, 7, 8, and 9 templates to see whether they still look roughly right.

I'm adjusting the spatial pooling to a wider blur so the templates match coarse class layout, and I'll apply per-class bias corrections to offset the skew toward 5 and 3.

I'm comparing the penalty steps class by class: classes 4 and 5 gain a lot without the penalty, while 7 and 8 drop, and the template changes seem to interact with that. Since equalizing the predicted class counts is cheap, I'm considering per-class bias offsets, though I'm still estimating how large the logit differences are.

I'm settling on a wider blur for the templates and applying small per-class bias offsets, pushing 7 and 9 up and 5 and 3 down to even out the predicted counts.
