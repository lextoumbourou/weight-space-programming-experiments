The blur shifted the balance, and 8 is now being underpredicted. Tuning the nearest-template hyperparameters feels fragile, so I'm looking for a more principled design. I'm considering simpler, more robust features, maybe dropping the orientation channel complexity, and asking what hand-designed approach could still reach high accuracy. One idea is to have the network produce a downsampled image, since 4x4 seems too coarse, and right now the fc layer only sees 16 channels at 4x4.

I'm working out how the network's 4x4 output could carry finer spatial detail by having conv2 channels pick out different pixel offsets within each cell. The max-pooling blurs those offsets together, so I'm checking which tap positions still give distinct, usable coverage.

I'm working out how the 4x4 grid could store finer positional detail by giving each conv2 channel its own tap offset within the pooled ink map. The max-pooling blends neighbouring offsets, so I'm checking which tap combinations still give distinct coverage across the 16 channels.

I'm checking whether the 4x4 grid could hold finer position detail if each conv2 channel reads a different tap offset. Working through the pooling arithmetic, the taps seem to cover distinct pool-row ranges, but the digit area only spans roughly pool rows 1 through 10, so I'm trying to pick offsets that reach that whole range without wasting channels on duplicates.

I'm settling on a roughly 8x8 max-pooled ink image as the intermediate representation, with each cell covering a 4x4 input block, which is a reasonable compromise between resolution and channel count. A linear classifier on an 8x8 downsampled digit should do fairly well, though nearest-mean templates would likely fall short, so I'd still need hand-designed templates. I'm also weighing whether to spend four channels on ink and the rest on orientation at a coarser grid.

I'm considering whether the 4 orientation channels and 3 spare channels could be repurposed, since hand-drawn templates limit the nearest-mean approach to around 80%. Instead of more template tuning, I'm thinking about discriminative features for digit pairs, such as detecting loops as enclosed background surrounded by ink.

I'm weighing whether the conv1 "dark" channel, a ReLU on blank 3x3 spots, could help detect holes in loops. After max-pooling it would only show that a blank spot exists somewhere in a 6x6 region, so I'd still need conv2 to check for ink on all sides of it.

I'm weighing a linear classifier on a designed 8x8 template grid, subtracting the average of the other templates, and wondering whether plain nearest-mean on raw pixels (around 82%) is good enough to start from.

I'm considering calibrating the per-class biases instead, since the bias mismatch seems to be what's causing the large swings in predictions. The idea is to nudge each class's bias up or down based on how far its predicted count sits from the true count, repeating a few times until they balance. I'm about to start tallying the column sums for the step-3 confusion matrix to get that process going.

I'm adding up the column totals for the confusion matrix, running through each of the nine remaining columns to get their sums.

Computing the log-ratio adjustments for each class's bias, comparing the true row sums against the predicted column sums from the step-3 confusion matrix. Classes 3, 4, 7, and 0 look under-predicted, while 8, 2, and 1 are over-predicted, so their biases need pulling down.

I'm weighing whether to fold the bias tuning into a structural change or settle the architecture first, since any redesign would reset the calibration. Calibration runs take two or three passes each, so I want the final layout pinned down before I iterate.

I'm thinking about whether a cleaner representation would work better than the current setup, perhaps a higher-resolution ink map with a simpler thick template, and I'm estimating what grid spacing that would give.

I'm working out the pixel geometry for the 8x8 grid: each cell's tap window needs to span rows 4m+2i+1 through 4m+2i+6. Shifting the tap offset to i∈{1,2} puts the centers at 5.5 through 21.5, which covers the digit area with 8 positions per axis at stride 2.

I'm laying out the 8x8 ink map as the core representation, and the offset windows I just worked out would take 4 channels for it. The other channels would then go to orientation features at 4x4, though I'm still deciding how to split them.

I'm checking whether dilation from the two max-pooling stages would wash out the hole in a 0, since a 6x6 max window at center positions could fill it in. Stacking two max-pools means each feature responds to a fairly large neighbourhood, so the structure of loops may get lost.

I'm checking whether a 1x1 center-pixel ink detector with a -0.3 bias would keep each pool window to a 4x4 input block at stride 2, which would give a tighter 8x8 map. I'm also considering conv2 channels that subtract neighbouring taps, though that's only a rough idea for now. Next I need to sketch the 8x8 template strokes and their grid values.

I'm weighing whether to tune the templates by hand or rely on what I know of the MNIST class means, such as the 0 as a thick oval ring and the 1 as a slanted vertical bar. Since I only get aggregate accuracy back, any refinement would have to be a coordinate search over a few parameters.

I'm checking the confusion pairs for geometric mismatches, like 0 versus 6 and 2, and 4 versus 1 and 9. Rather than fitting templates blindly, I'm sketching a v2 with a 3x3 ink detector weighted toward its center, plus four orientation channels at 0, 45, 90, and 135 degrees.

I'm laying out the orientation channels next: four tight-window features on a 4x4 grid, plus a wider version that shifts the center.

Now I'm settling the layout for the second version: an 8x8 ink grid from four offset taps, orientation channels at a coarser grid, and the remaining channels left empty for now. I'll draw the templates from the stroke shapes and then tune the nearest-mean classifier and biases on top.

I'm weighing whether the MNIST digit geometry, centered on the mass and about 20 pixels tall, should guide the stroke placement more than the abstract LDA weighting does.

I'm sketching the digit-4 template next: a left diagonal stroke, a horizontal crossbar, and a right vertical that should start at the top rather than partway down, since open 4s have two vertical strokes.

I'm now sketching the digit templates by stroke coordinates: the 4's right vertical should start at the top, the 5 gets a top bar plus a bowl arc, the 6 a curving top stroke into a lower loop, and the 0 an oval about 9.5 rows tall. I'm also noting that MNIST strokes are about 2 to 3 pixels thick, so the ink windows should register anything within roughly 1.5 pixels of a stroke.

I'm settling the feature magnitudes: the ink core filter gives about 0.75 at a stroke center, so I'll use 0.7 as the ink value. For the orientation channels I'll use four directions at 45° spacing with tuning max(0, cos 2Δ), and I'm making the filter a bit wider across the stroke, around σ=1.0, since MNIST strokes are fairly thick.

I'm checking how the orientation features should be spread across the grid, then working out the feature counts for the ink and orientation channels so the template setup stays consistent.

I'm working out where the 8x8 grid cells land: with the two pooling stages, each cell's center sits at 2r+5.5, so the outermost cell, r=7, comes out at about 19.5.

I'm correcting my earlier arithmetic: the grid centers at 5.5 through 19.5 fall short of the digit's middle at about 13.5, so I'm considering shifting the taps to put the grid over rows 7.5 through 21.5, or leaving it asymmetric.

I'm checking the grid placement: taps at i∈{1,2} keep the rows 3 through 22 covered, which handles the top of the digit but only partly reaches the bottom bar of a 2. For the tight orientation channels I'm now working out which pooled rows the tap at (2,2) draws from.

I'm working out the orientation grid spacing and how the pooled rows line up for the tight and wide channels. The sums over taps 1 through 3 should put the wide windows around 4m+4 through 4m+11. Before tuning α I'm wondering whether there's a way to avoid the ||T||² bias term altogether.

I'm switching from nearest-mean to cosine similarity with normalized templates, so each class is scored by the direction of its template rather than its magnitude. That should make the scoring robust to any global scale mismatch in the features, which also sidesteps the bias term I was worried about.

Writing the convolution code for the ink channel...

Still writing the convolution setup...

Still writing the template code...

Still writing the stroke coordinates for digits 0 through 5...

Writing the stroke coordinates for digits 6 through 9...
