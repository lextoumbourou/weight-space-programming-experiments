I'm looking at the remaining misclassifications: 1→7, 4→9 and 4→8, 5→6, and 7→2/9. I think the core limit is that my Gaussian templates rest on rough geometry, so I'm considering standardized features and a mean-centered logit linear discriminant to remove the common-mode term.

I'm weighing whether the 1 template's weak features explain why the 7 template wins for some 1s. The 7's diagonal runs through the center column, so a slanted 1 could score higher against it than against my vertical 1 template.

I'm considering that the 1 template may be too vertical, since real 1s often lean like a "/", so a single near-vertical template underweights them. A better fit might be to average vertical and slanted variants of the 1 template, which would blur it toward how real 1s actually look.

I'm weighing whether to avoid averaging shear variants of the templates, since that would mean building feature vectors from generated samples. A safer route is to widen the spatial blur of the single 1 template and loosen its orientation tolerance, which keeps everything as one deterministic drawing and still lets slanted 1s match better.

I'm checking the 5 template against the 6, since my 5's bowl closes too far on the left and starts to look like a 6. Pulling the arc's end back to about -120° would open it up, and the 5's top bar should sit in the upper cell.

I'm checking the 4 template against the 9 and 8, since its open top and the left stroke's slant seem to be what's pulling it toward those classes. The 7's pairings with 2 and 9 are still pending.

I'm looking at whether to tune per-class biases directly from the confusion matrix, since the over-predicted 6 and 8 columns suggest the bias terms are off rather than the templates alone.

I'm working through the per-class biases now, estimating how much each class's bias should shift from the gap between its true count and its predicted count. The 4 column is badly under-predicted, so its bias goes up, while the over-predicted 6 and 8 columns get pulled down.

I'm going to set the per-class bias corrections from the confusion counts, scaling them by about 0.7 since the templates are still changing. The 4 class needs the largest upward shift, and the over-predicted 6 and 8 need pulling down. I'm also wondering whether the 3x3 features are too small in magnitude relative to the center features.

I'm planning the next template changes: opening up the 5's bowl by pulling its arc end back, widening the blur on the 1 template with a slanted variant, and then applying per-class bias corrections from the confusion counts.

I'm pulling the 7's diagonal back toward its top-right corner and noting it sits fine against the 9. I'm also checking the 2 template's diagonal, which runs cleanly from the lower left to the upper right. The bigger question is whether the centre-group features are too selective, since real detectors respond to strokes at off-angles, which my sharper templates don't allow for.

I'm checking how the horizontal detector responds to a diagonal stroke, and the kernel's weights cancel out to roughly zero, so it stays selective. I'm noting that a stroke tilted by about 22.5° would only partly activate it, which is why I'm weighing the orientation tolerance.

I'm going to apply per-class bias corrections scaled from the confusion counts, starting with a modest step since the templates are still changing. I'll also open up the 5's bowl and build in the slanted 1 variant as planned.
