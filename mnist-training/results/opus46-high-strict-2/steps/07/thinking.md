Let me analyze step 6 results. Accuracy barely improved from 41.5% to 41.9%. Loss decreased from 1.68 to 1.64.

Let me look at the confusion matrix:

Predicted column sums:
Col 0: 628+0+10+0+4+16+49+12+2+47 = 768
Col 1: 2+861+52+89+73+53+21+87+172+64 = 1474
Col 2: 60+7+514+33+10+34+43+2+110+0 = 813
Col 3: 12+1+179+248+1+14+7+45+33+8 = 548
Now I'm tallying the remaining confusion matrix columns, working through the counts for columns 4 through 8 and starting on column 9.

I'm working through the class-level imbalances now: class 9 is still over-predicted at 1654, class 1 at 1474, and class 6 at 1173, while classes 3 and 0 are under-predicted. The oscillation seems to be dampening, but the biggest confusions remain 7→9, 3→9, and 9→8.

Now I'm tallying the remaining confusion matrix columns, working through the counts for columns 4 through 9. The biggest problem is still 7→9 at 713, barely down from 668 last step. Templates and holes aren't separating those classes well enough, and I've been stuck near 41% for three steps, so I think I need a more fundamental change.

I'm going to try a sharpened center-surround kernel on the ink channel in conv2 instead of the smooth one. I'm also considering a bigger redesign where the other channels compute more specialized features rather than just passing values through, with some channels combining horizontal and vertical strokes.

Still writing channel specs...

Still writing channel specs...

Still writing the left-right asymmetry kernel...

Still working through the left-right asymmetry channel, which is meant to tell apart pairs like 3 and 6 by where the ink sits. The catch is that ReLU only keeps positive responses, so the asymmetry kernel only fires for one direction.

Still working through the single-channel experiment, where only channel 10 would change to ink contrast. I'm sketching the digit-1 template for that channel, which should fire along a thin stroke.

Still writing the digit templates for channel 10...

Still writing the channel 10 templates...

Still working on the channel 10 settings, which currently hold a bottom-right corner detector I need to zero out before setting the new contrast kernel. Next I'll update the biases with the log-based correction from the step 6 predicted counts.

Still working out the bias corrections for the remaining classes, using the same log-based adjustment from the step 6 counts.

Still working out the bias corrections for the last few classes, applying the same log-based adjustment to each step 6 count.

Next I'm checking whether bias tweaks alone can fix the 7→9 confusion, and I'm leaning toward better features instead, since the biases only shift overall counts.

Still writing the channel layout, switching from the pass-through setup to specialized detectors for horizontal bars, verticals, loops, strokes and diagonals across the conv2 channels.

Still writing the channel 11 and 12 setup, with the plan now down to updated biases, an ink-contrast channel for ch 10, and a total edge energy channel for ch 11.

I'm wondering whether the digit 7 ink template is simply wrong, since MNIST 7s vary a lot. Some are closer to a flat top bar with a vertical stroke, which my current pattern doesn't capture.

I'm picturing the digit 7 as a horizontal bar across the top with a stroke running from the right end down toward the center or slightly left. On the 4×4 grid, that should mean ink across the central top columns, then shifting left as it goes down, ending near the bottom at column 1. The center of mass sits around the middle of that diagonal, so the bar stays at the top and the stroke runs from top-right toward bottom-center.

Working through the digit 7 template again, I'm checking the bar's position against the diagonal. On the 4×4 grid, the top row should carry ink across the central columns, while the middle rows only pick up the right-side diagonal.

Now I'm checking the digit 7 template row by row. The 4×4 receptive fields are 16 pixels wide, so the top bar covers every column in row 0, not just the right half. My current template puts ink only at cols 2-3 there and marks the left side negative, which is wrong.

Still working out the digit 7 template, now checking whether the top bar should be positive across the whole first row, since the bar spans most of the width and the left edge might catch a bit of ink in the first column too.

Still writing the digit 7 template, now the top row with col 0 set to neutral rather than negative.

Now I'm correcting the digit 7 template's top-left cell, since the bar spans that column too, so it shouldn't be marked negative.

I'm checking the digit 9 template next, looking at whether the bottom of the loop should have ink on the right side too, since the stroke may continue down past the curve.

I'm adjusting the digit 9 template so the bottom ink shifts right, toward columns 2 and 3, since the center-of-mass centering puts the curve's end nearer the right side.

I'm weighing whether to boost the conv1 edge filters from 0.06 to 0.12, which would make the edge features stronger in the feature maps, though that risks pushing the logits too large.

I'm weighing whether to push the edge features up from 0.06 to 0.10 and the hole features from 0.07 to 0.12, which would shift the balance away from ink. Ink strength is staying as it is at 1.5, since turning up every magnitude would just scale everything together and the relative sizes are what matter.

Now I'm checking whether stronger edge filters would saturate after ReLU and pooling, so I'm estimating the output at scale 0.10 for a strong edge and tracing it through the conv2 pass-through and the second max pool to the logit contribution.

Now I'm weighing a more conservative bump: edge features to 0.08 and hole features to 0.10. That should keep the summed contributions from edges and holes around 10 to 15 across channels and positions, with ink adding maybe 5 more, so the logits stay in a workable range.

Rather than raising magnitudes across the board, which would only amplify whatever the templates get wrong, I'm going to focus on correcting the templates themselves so they match the digit shapes more accurately.

I'm working out how MaxPool2 turns the 8×8 conv2 output into the 4×4 grid, and whether my guesses about those features could be systematically off.

I'm working out how MaxPool2 combines the 8×8 conv2 output into the 4×4 grid, tracing which maxpool1 cells each conv2 value draws from.

I'm working out how the 4×4 pooled cell maps back onto the input, tracing each maxpool1 region through its conv1 window to see what input area it reads from.

Working out how the 4×4 pooled positions map back to the input, the receptive fields are 12×12 pixels spaced 4 apart. The centers land at rows 7.5, 11.5, 15.5 and 19.5, so each position covers a broad, overlapping slice of the image.

I'm noticing the overlap between adjacent 4×4 positions is about 67%, so neighboring features end up very similar and the grid can only capture coarse spatial trends. That would explain why accuracy has been stuck near 42%, since the grid can't resolve the fine differences between digits like 7 and 9 or 3 and 8. I'm wondering what I could change to reduce that limit.

Trying a delta kernel for conv2 might cut the overlap, since each conv2 value would only see one maxpool1 value and the 2×2 pooling blocks would stop sharing inputs. I'm working out what region of the input each pooled cell would then cover.

Now I'm tracing where the 6×6 input windows of the first maxpool positions land, checking how far the rows they cover extend in the 4×4 grid's receptive field.

Now I'm checking the 4×4 positions for the delta-kernel version: each pooled cell would cover eight input rows, and adjacent cells overlap by half, so the overlap is less than before but still substantial.

Now I'm setting up a delta kernel for every conv2 channel, since the sharper kernel should cut the spatial overlap and let the 4×4 grid tell digits apart better.

Still setting up the delta kernel, now checking how the corner and diagonal channels behave when their edge inputs are only matched at a single location.

I'm weighing a delta kernel against the smooth one for the horizontal-stroke channels, since a thick bar's top and bottom edges land two maxpool1 positions apart and a single-point kernel would miss them. The smooth 3×3 averaging tolerates that separation, so for combination channels it may still be the better choice.

Writing the pass-through and combination kernels for step 7...

I'm checking whether dropping the delta kernel's border positions would hurt, since the top and bottom rows of maxpool1 cover the digit's edges.

I'm settling on a split for step 7: the pass-through channels get the sharp delta kernel to keep spatial detail, while the combination channels keep the smooth kernel so co-occurring edges can still fire despite slight offsets. I'm also going to update the biases for the new setup.

Now I'm going to switch to a delta kernel for the pass-through channels and keep the smooth kernel for the combinations, then update the biases. I'm also planning to fix the digit 7 template, the biggest source of confusion, and I'll add an ink contrast channel in step 8 if this helps.

Now I'm weighing a rewrite of the digit 7 template, changing a few cells to match how the top bar and diagonal usually sit in real MNIST sevens.

Now I'm sketching the 4×4 grid's ink pattern for a 7: the top row should register ink across all columns, with the diagonal stroke sliding leftward through the rows below.

Now I'm sketching the digit 7's 4×4 ink pattern: the top bar should register across all columns, with the stroke sliding from the right side at the top to the left side at the bottom.

I'm settling the template values for digit 7 on the 4×4 grid: the top bar gives strong ink across most positions, with the stroke sliding leftward through the lower rows, and I'm reconsidering the middle-row values against that pattern.

Now I'm checking the 4×4 template values for digit 7 against the rough ink estimates, subtracting the mean so the template has zero average, and noticing the top-left and bottom-left cells are where my numbers are least certain.

I'm dropping the hand-designed template approach for the FC layer, since I can't really know those feature values without seeing the data. I'll instead try a bolder change: a delta kernel for the pass-through conv2 channels, a smooth kernel for the combinations, and a larger FC scale of 0.5 with adjusted biases.

I'm weighing whether a stronger scale would help or hurt. More confidence sharpens the correct predictions but also the wrong ones, and at roughly 42% accuracy the net effect on loss is hard to predict. I'll just try it and see.

I'm keeping the scale at 0.35 and focusing on the delta kernel change instead. For step 7 I'll use a delta kernel on the pass-through conv2 channels, a smooth kernel on the combination channels, updated biases, and small fixes to the templates. I'm also going to look at the digit 9 template, which has a top loop and a right stroke heading down.

Now I'm adjusting the digit 9 template so row 2 picks up some ink toward the center, and row 3 shifts its strongest value to column 2.

I'm going to lock in step 7 now: a delta kernel for the pass-through conv2 channels, though I'm wondering whether the FC templates, which were designed around the smooth kernel's spatial pattern, will still hold up. I'm also checking whether the conv2 scale of 4.0 should change for the sharper kernel, since the feature magnitudes will shift.

I'm working out whether a delta kernel that picks a single maxpool1 value would beat the smooth 3×3 average after maxpool2 takes the max of four conv2 outputs. If the maxpool1 values vary across positions, the delta version should carry more spread into that max, so I'm considering scaling it down to 3.0 to keep feature magnitudes comparable.

Now I'm settling on a delta scale of 3.0 instead of 4.0, since the max over individual values will run higher than the max over averages and the feature magnitudes need to stay comparable. I'm also wondering whether a plain per-feature linear classifier on the 256 features would do better than the channel-wide templates, since it allows finer weighting than one value per 4×4 channel.

I'm now weighing whether a per-feature linear classifier would beat the channel-wide templates, since it could set finer weights, but tuning 2560 weights by hand isn't practical. I'll keep the templates as a base and make targeted adjustments to the features that matter most for telling digits apart.

I'm now checking whether the digit 7 vs 9 hole feature at top-center actually separates the two, since the template already gives 9 a positive weight there and 7 a negative one. If the template values are off, that feature may not discriminate the way I'm assuming.

I'm moving on to step 7 with the delta kernel, since that's the biggest structural change I can still make in the remaining steps. I'll set up the first conv layer's Gaussian kernel as the starting point.

Still writing the conv1 kernel setup...

Still writing the conv2 setup...

Still writing the conv2 weights...

Still writing the conv2 weights...

Still writing the classifier setup...

Still writing the 7 and 9 template fixes...
