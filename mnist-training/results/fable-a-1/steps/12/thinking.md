I'm checking the column and row totals against each other, and the model sits at about 81.6% accuracy with loss 0.651. Digit 1 looks over-predicted, since its column sum is 1191 against a row sum of 1064, so I'm looking at where its extra predictions come from.

I'm going through the per-class error counts now, and digit 2 is the biggest source of mistakes, mostly being called 8. Digit 7 is also over-predicted, largely from 9s, and bias tweaks have only helped a little. I'm considering a bigger change: increasing the weight on the corner features and maybe scaling the overall logits.

I'm weighing whether the endpoint idea is even possible, since no conv1 or conv2 channels are free, so I'm considering swapping out the clip or hole channels instead. I'll probably keep the holes, since their AND with the corners is unique, and the remaining gains will have to come from recalibrating the orientation and corner templates and their weights.

I'm weighing whether to split the 4 corner types across zones, but that would lose the column detail that tells apart shapes like a 3's bracket from a 7's.

I'm weighing whether a finer-grained statistical measurement could get past the knob-tuning plateau, since the confusion matrix gives roughly nine degrees of freedom per class each step. Packing several binary features into one step means the joint outcomes run out quickly, so that route looks limited.

I'm comparing the 2 and 8 confusion, since 2 is often called 8 and vice versa. I'm checking which corner and orientation features tell them apart, such as the lower loop and the upper-middle corners.

I'm considering probing a few features that separate a confusable pair, measuring each across all ten classes, and then recalibrating those templates. That would be about thirty numbers per step, concentrated on the most discriminative features, though it would only cover a small slice of the roughly 128 features in play.

I'm now comparing the 2-versus-8 errors, since the 2s are being called 8 most often. The lower-hole feature looks like the culprit: for a loopy 2 it pushes the score toward 8 more than toward 2.

I'm now looking at the upper part of the 2, where the cap curves into the neck. The region beneath the cap looks open to the lower left, with ink above and to the right, which seems to be the feature that separates it from an 8's upper loop.

I'm thinking about whether the variant tournaments used for 0, 2 and 3 could also help with the remaining digits, since 6 is being pulled toward 0 and 1, and that template may not be doing its job.

I'm weighing a set of coordinate-search knobs to try next: corner weight, orientation weight, overall temperature, the probability squeeze, the corner window width, the hole gains, and the theta. With around 39 steps left, I can afford about two trials per knob.

I'm thinking about whether a crisp, single-tap orientation feature at 4px cells could work better than the overlapping 8px cells, since the corner features have been reliable at that resolution. A single threshold tap would be bounded and need no clipping channel, so it might free up channels.

I'm checking whether a single tap of the horizontal filter could replace the overlapping cells, but the center tap misses strokes near the top and bottom edges. Summing a few taps across rows 4 to 6 might cover those bars at a reasonable response level.

I'm considering two taps per orientation, at offsets (1,1) and (3,3), so the grid covers rows 1 to 10 with half-cell-offset cells.

I'm laying out the two candidate grids for the single-tap orientation channels, with one tap at (1,1) and another at (2,2) so the cells overlap by half a step. That would cover rows 1 to 9 with a staggered sampling, which gives finer resolution than either grid alone.

I'm weighing whether to split the orientation grid into two taps, at (1,1) and (3,3), so that together they cover the top and bottom rows that a single tap misses. That would cost eight channels, but with 4-pixel cells the representation would be crisper, and the corner features already show that approach can work.

I'm sketching an endpoint detector for conv2: a stroke ends where there is ink at the center and below it, but none above. Using the summed line maps as "ink," that would be a relu of center plus below ink minus a penalty on the region above.

I'm working out an endpoint detector for conv2: a stroke end should have ink at the center and below it, but nothing above, and horizontal strokes need to be ruled out by checking the ink to the left and right.

I'm weighing whether a diagnostic-driven recalibration of the existing features is a safer bet than building new endpoint channels, which would be uncertain. A more promising option might be measuring class-conditional statistics on the aggregated corner features, since those are crisp and semantic, summed over rows and columns to get a compact set of values.

I'm considering a different kind of measurement: for each corner type, find which of nine merged regions holds its strongest response, giving one step per type with about nine outcomes. That would show where each class's dominant corner sits, using only four steps.

I'm weighing how to split the 16 corner cells into nine regions for a 3x3 summary, since merging rows 1 and 2 would blur the upper-middle and lower-middle corners that separate a 9's loop from a 6's.

I'm weighing whether to split the 4x4 corner grid into zones for a single measurement per corner type, but a joint row-and-column readout would need 16 outcomes, which doesn't fit in one step. Measuring rows and columns separately would take two steps per type, and comparing corner types in the same step could hide which one is strongest.

I'm weighing a half-measure: measuring each corner type with argmax over the 16 cells, split into row zones and then column zones, which would take two steps per type and about eight in total to recover both marginals.

I'm weighing a measurement that picks the strongest corner location per type across nine zones, though merging rows would blur the separating corners. I'm also considering tournament-style soft templates as an alternative.

I'm weighing a per-class calibration check that measures how often each corner type fires, but a single probe can only resolve one type at a time, so it would be inefficient. With 39 steps left, I'm leaning toward a readout that gives the most information per step, and the current classification confidence may be the best option for that.

I'm working through the PC squeeze next, specifically the log-odds for absent-expected cells, and I'm also planning a few coordinate-search steps: raising the corner scale from 0.25 to 0.4 to see which way the loss moves, with small bias nudges for classes 1, 7, 2 and 4.

Checking whether a larger corner scale helps: I'm trying 0.4 instead of 0.25, since corners that fire spuriously across classes get penalized hard by the absent-cell log-odds. If the loss drops, the corners deserve more weight; otherwise I'll revert.
