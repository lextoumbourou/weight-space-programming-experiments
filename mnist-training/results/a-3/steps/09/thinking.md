I'm working out where the remaining error comes from: the template matching and the linear model are probably the main limits now. To get a real gain, I'm thinking about building better per-digit templates from what the MNIST average shapes look like, starting with the 0 as a wide oval and the 1 as a vertical stroke leaning slightly right.

I'm going through the confusion pairs in the error matrix: 2 gets mistaken for 4, and 8, 9, and 7 bleed into each other. My guess is the 2 template lacks the curved hook at its bottom-left, so I'm wondering whether softening the templates' blur would help them handle variability better.

I'm weighing a parameter tweak next, bumping the template blur to sigma 2.8 and possibly running a few variants. I'm also considering whether sum-pooled features would capture edge amount better than max-pooling, though it's not clearly an improvement. I'm leaning toward revising the templates with more MNIST-like slants and shapes, with the aim of making them more realistic.

I'm now writing out the template coordinates for each digit, starting with the 0 as a tilted ellipse and the 1 as a near-vertical stroke with a slight lean.

I'm writing out the coordinates for the remaining digit templates now, keeping the 3 as it is and tilting the 6. For the 4 I'm using a left stroke, a horizontal bar, and a right stem, with a closed variant at lower weight. The 7 gets a top bar with a diagonal stem, and I'm starting to define the 8 as a slanted shape.

I'm finishing the template definitions for 8 and 9, with the 9 as a loop with a slanted stem plus a straighter variant at lower weight. I'm also bumping the blur sigma to 2.5 and updating the biases with a half correction, starting with the 0 column.

I'm recalculating the bias corrections by taking half the log ratio of predicted to true column sums for each digit, and I'm updating the values from 0 through 9 accordingly. Then I'll write out the template definitions.

I'm noting that the template changes will shift the calibration, but I think that's acceptable.
