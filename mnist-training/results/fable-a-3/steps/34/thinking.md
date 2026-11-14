The accuracy came in at 91.10%, a touch under the previous 91.22%, though the loss improved a little to 0.3016. The heavy features added little, which is disappointing: some transitions dropped noticeably while others rose, so they mostly repeated information already carried by presence. With 17 steps left, I need to decide how to push past the roughly 91% ceiling of the naive Bayes approach.

I'm weighing scale tuning against discriminative correction for the naive Bayes model. Since the heavy features are now partly double-counted, I'm wondering whether to shrink the weights of the redundant groups, though I can't guess the right direction. With about 17 steps left, I can afford roughly eight tuning experiments. A logistic-regression-style classifier on these features should do far better than 91%, so I'm looking at pairwise probes for confusable digit pairs.

I'm thinking about gradient-like signals from the confusion matrix, since a per-pair probe would only give me one feature bit per step and can't recover a full update direction. Instead I'm considering coordinate-wise finite differences over about ten group scales, which could give real gradient estimates with roughly ten steps, though the gain may be modest.

Now I'm comparing the predicted and true class counts, and nine is clearly undercounted while five and two are overcounted. I'll nudge the biases to rebalance those classes.

Next I'm looking at ways to tune the model's biases and group scales, and I'm weighing whether per-direction probes could give usable gradient signals without requiring a full update vector for each class.

I'm now weighing a few directional tests on the scale parameters, like nudging the end-type weights or the heavy-feature group, since each costs one evaluation and the loss is deterministic enough to read small changes. The cleaner route might be random simultaneous perturbations of all groups at once, though that only yields a gradient estimate along a single random direction. The confusion matrix is where I'm headed next.

I'm now looking at the top confusion pairs, like 8↔5 and 3↔2, to see which ones carry the most error mass.

I'm checking which confusion pairs carry the most error mass, starting with 8↔5 at around 90 errors in both directions, so it's not a bias problem. I'm looking at the V-channel features to see which ones separate 8 from 5.

I'm looking at the 8↔5 confusions, where the strongest features like the upper-left and lower-left closures separate the classes well, yet about 90 errors remain. The misclassified examples seem to be atypical ones, such as 5s with a curled top bar or 8s with an open loop, which suggests this feature family has a hard ceiling for these cases.

I'm weighing whether mixture-style sub-class modeling could help, but with only ten outputs that doesn't fit this setup. The remaining room looks like fine-tuning the scales and biases, maybe a small accuracy gain, and I'm considering whether any cheap new features are worth trying.

I'm thinking about a new "NE-end" detector for the 6's top stroke, since its diagonal tip points up-right and the current features miss it, which may be why 6 gets confused with 5, 8, and 1.

I'm thinking the 6's top stroke is the gap here: its tip points up-right, so the current features miss it. A dedicated end detector for that direction, where the tip is present and the cells beyond it are empty, could separate 6 from 5 and 8 better than the existing half-weighted setup.

I'm considering a new end detector for the upper-right direction to catch the 6's top stroke, since the existing U-end detector would need re-measuring and that costs two steps. A separate channel with a stronger tip weight and empty cells beyond it could target the 6 without disturbing the other features, and a single probe over the top rows would test it. I'm also wondering whether a similar end detector for the down-left direction would help separate other digits.

I'm now looking at a few of the unmeasured presence cells along the "/" diagonal, especially at the top right, where a 6's top stroke would show up. I'm also wondering whether the bottom-left cells could separate 2 from the other digits.

I'm going to measure the "/" presence cells in two batches, taking the right column first and then the left one. The right column is fairly safe to read as runs, while the left column needs triples so that the class-2 arc and neck don't get confused.

I'm sketching a 17-step plan: a bias re-tune and a classifier check at step 34, a few probes for the "/" presence cells and a new northeast end detector for the 6's top stroke, then a classifier step and about eight steps of group-scale tuning. I'm also weighing whether a quick test scaling all vote weights by 1.3 at step 34 would reveal whether the model is over- or under-counting.

I'm considering a temperature-style test where all vote scales and biases get multiplied by 1.3, which leaves accuracy unchanged but could lower the loss, though that only matters if the final score weighs loss. For accuracy, I'd rather look at the relative scales, so I'll keep this check for the end of the plan.

I'm thinking the end-detector weight might deserve a bump from 0.6 to about 0.8, since the ends carry information the other features don't repeat. I'll pair that with a bias re-tune in the same step, because the bias change is a near-certain gain while the weight change is the uncertain one.

I'm recomputing the extra biases from the per-class prediction and true counts, shifting the underpredicted digits like 9 and 6 up and the overpredicted ones like 2 and 3 down.

I'm checking the pairwise error asymmetries to decide which digits need their biases raised or lowered, with 9, 0, and 6 looking underpredicted. Next I'll apply the bias re-tune and bump the end-detector weight to 0.8.
