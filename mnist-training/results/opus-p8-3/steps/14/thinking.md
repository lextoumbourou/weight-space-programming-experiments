Emphasizing the 6's loop features made things worse, with 6s still landing on 0 and 5. It looks like the 6s may be producing features that match 0 instead, so I'm checking the correlation classifier's normalized templates next.

I'm wondering whether the 6s are producing features that match 0 rather than the ones I expected, which would explain why emphasizing their loop features didn't help. Under correlation scoring, the heavier topology template dimensions could be drowning out the stroke dimensions. Since I can't see per-feature activity directly, I'm considering a probe that encodes one scalar feature as a staircase of logits, so each row of the confusion matrix shows that feature's distribution per class.

I'm weighing whether to use the remaining probe steps to read out a single feature's distribution per class, since a staircase of logits could turn each confusion row into a histogram of that feature. I could also encode two features at once, with a 3x3 grid of linear regions, though measuring the mean activation of each channel and cell per class would take far too many probes.

I'm considering encoding a set of per-cell feature values as logits so that the argmax reveals which cell is most active. That would give a class-by-class view, though pulling out the per-class averages for all sixteen cells this way would take far too many probes.

I'm weighing whether the per-class averages for the remaining feature channels are worth the probe budget, since testing each of them one at a time would eat most of the steps. I'm also treating the feedback loop as the intended way to learn, not a search algorithm, so using it to pick the next probe is fine as long as I keep the network itself hand-designed.

I'm sketching a few probe designs to get more information per step. One option is to let each class logit be a different cell's activation, so the argmax reveals which cell peaks, though that doesn't give per-class means. Another is to threshold a single combined feature into a staircase, which would show each class's distribution along that feature, but only one scalar per step is slow. I'm also considering dotting the features with ten basis directions, which could show which direction dominates per class.

I'm thinking about whether to spend a few probe steps testing where the loop features fire in each class, by letting each class logit track one cell group's loop activation with a constant threshold logit for "none." That would tell me directly where the 6s' loops are, though it only covers the topology channel.

I'm weighing whether to spend a few probe steps on a different design, since reverting the topology change while keeping the gains for 2, 3, 4, and 5 might be the better trade. The errors that still matter most are 6 to 0, 9 to 0, 4 and 5, 8 to 2 and 5, 3 to 5, 7 to 2 and 5, 0 to 2, and 1 to 7 and 2.

I'm planning a probe that groups the 4x4 cells into a 3x3 layout by averaging each group, with one threshold logit for "none," so the argmax shows where the loop activation peaks for each class. That would only cover the topology channel, though.

I'm going to probe the loop channel first, since that's the core hypothesis behind the 6, 8, 9 and 0 confusions. I'll split its activation into three regions and check where the loops actually sit in each class.

I'm planning to probe the loop channel by mapping each region's activation to its own class logit, with a constant threshold logit for "none," so the argmax shows where loops sit in each class.

I'm checking whether the 6s' loop lands in the bottom cells, which would explain why the 0 template picks them up, though I'm not sure yet how much the one-cell offset matters given MNIST's positional variation.

I'm thinking the 6s may fail to fire the loop and HB1 features, so the 6 template's topology expectations go unmet and its score drops. A probe over loop, HB1, and HB2 across three row bands should show where each class's strokes actually sit.

I'm weighing a cleaner probe: rather than mixing feature channels, I'd test the loop channel alone by averaging its activation over a few row and column groups, with a constant threshold logit for "none."

I'm settling on single-channel probes now, reading out loop activation by row for the first four logits and HB2 by row for the next four, with a constant logit as the "none" threshold.

I'm weighing whether a probe step is worth the cost versus trying another fix, and I'm leaning toward it since I've been guessing at feature behavior. I'd test the loop and HB1 channels by row, with a constant logit as the "none" threshold, to see where each class's strokes actually sit.

I'm setting the next probe to read the loop channel and the HB2 channel by row, averaging the two center columns of each row and scaling each by its threshold. The argmax will show which row each feature peaks in, with a constant logit for "none" and a bias to suppress the last slot.
