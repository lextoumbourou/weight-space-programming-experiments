The best loss is 0.9561 at step 4, and I need to beat 0.9465 soon, since the stop rule ends training if the best loss of the last five steps doesn't improve by at least 1%. Step 6 shows eight heavily overpredicted cases in the 2214 column, which looks like a bias or calibration problem more than a model failure.

Now I'm running the per-column sums of the confusion matrix and each column's offset from its expected total. Column 8 sits about +0.96 off, while column 2 is around -0.77, which points to a bias in how the 8 template is scored.

I'm weighing whether to raise the A parameter to 0.8 because the eight is overpredicted, which I read as the edge features running larger than expected. The earlier step-3 pattern pointed the other way, so I'm adjusting gamma to about 3.5 and adding per-column bias corrections to the scores.

I'm weighing whether to fold the bias correction into the change to A, since doing both risks double-correcting the eight. Instead I'm considering a scaled-down bias correction, about a 0.3 factor, and I can't yet tell from the numbers which adjustment matters more.

I'm switching to a bias-only correction this step, applying about 0.7 of the negative log ratio to each column, so the offset for the 8 template is -0.67 and the others shift accordingly. I want that clean read on the edge features before changing A again.

I'm applying the bias correction on its own this step, with the 0.7 factor, and not changing A, so I get a clean read on how the edge features behave.
