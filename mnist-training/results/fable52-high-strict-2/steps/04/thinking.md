I'm tallying the column sums and noting that the 6 column is still the main attractor, pulling in counts from several source digits, with 3 as a secondary attractor.

Six still pulls in the most counts, and I'm weighing whether the bonus I gave its loop-top and tip features is too small to offset its bias. The 4, 5, and 9 digits seem to trigger a stronger response than I assumed, so I'm considering whether a probe on that feature's response across classes would settle it.

I'm weighing whether a probe would be more useful than another guess, since six keeps drawing counts and my bonus estimates may be too small. Packing two scalars into a 3×3 joint readout would pull more information out of each step than one scalar at a time.

I'm weighing whether to spend a probe on the class-conditional feature means or keep tuning the hand-set evidence, which is improving slowly. A probe that reads two scalars at once in a 3×3 joint readout would return more per step than one scalar at a time.

I'm checking whether the 6 bias is still the problem, since 4, 5 and 9 pull toward it more than the loop-top bonus accounts for. Removing that bonus or scaling it up could be the fix, and a scale-free approach using only vetoes might avoid the tuning altogether.

Bonuses for 3's strokes are backfiring, since 7s, 9s and 2s share those strokes and each gets the same boost toward 3. A bonus only helps when a stroke belongs to one class, and that is rarely the case here.

I'm realizing the bonus scheme was the flaw: giving a bonus only to the classes that share a stroke is the same as vetoing the rest, so I should just use vetoes for classes that lack a feature and leave uncertain ones at zero, since a constant offset across all classes changes nothing.

Vetoes alone may be cleaner, since a bonus given to every class that has a stroke is just a veto on the others. Where a stroke is missing, only a bias can penalise that class relative to the rest, so I'm checking whether the loop-left bonus for 9 still works against the other classes that also carry it.

I'm settling on a symmetric scheme where each feature adds a signed term for every class: positive if the class has the stroke, negative if it lacks it, zero if unsure. The response is shifted by a threshold near half the typical present value, so the terms stay balanced across classes, and I'll need a calibration probe to set that threshold.

I'm settling on a per-class signature for each feature: +1 if the class has the stroke, −1 if it lacks it, 0 if unsure, so the evidence works both ways. The score is then the base template plus a weighted sum of each feature's response minus its threshold. Calibrating those thresholds would take a probe per feature, which is too many, so I'll estimate them roughly from the strokes' typical present response.

I'm considering a single-item probe to calibrate the thresholds for all the features at once, since they share a similar structure. A histogram of one stroke detector, split by which classes have it and which lack it, would show both its typical present level and how much it leaks into the absent classes.

I'm weighing a probe on one stroke detector, the bottom-horizontal one, since its carriers and non-carriers are both well populated. Binning its response into about ten levels would show both how strongly it fires when present and how much it leaks into the absent classes. That calibration would set the thresholds for the symmetric scheme directly, instead of guessing them and risking a poor fit.

I'm weighing a probe on one stroke detector, the bottom-horizontal one, which has well-populated carriers and non-carriers, to see how strongly it fires when present and how much it leaks into absent classes. Binning its response into about ten levels would calibrate the thresholds for a symmetric scheme directly, instead of guessing them.

I'm weighing whether to probe the ending detectors, since the step-2 shift from 4 to 9 suggests the tip features are doing something useful. Rather than probing one stroke, I'm considering a 5×2 joint readout on the bottom-horizontal item and the up-tip response, so both the stroke's present/absent levels and the tip's behaviour come out of a single probe.

I'm weighing a 5×2 joint readout that pairs the bottom-horizontal stroke response, binned into five levels, with the up-tip response, so one probe shows both how the stroke behaves when present and absent and whether the tip detector fires as expected.

I'm working out the response of the tip detectors at the two endpoints: the first point lands mostly on the middle column, with smaller contributions to the neighbouring columns, and the second point does something similar on the other side.

I'm working out how to set the thresholds for a joint readout that pairs the bottom-horizontal stroke response, binned into five levels, with the up-tip response on two levels. The class index combines both, so each class gets a logit from its stroke level plus its tip state.

I'm working out how the expected response of the bottom-horizontal stroke detector looks in the bank cells nearest its line, since that sets the thresholds for the five-level readout.

I'm estimating the bottom-horizontal stroke's response in the bank cells near its line, working through the Gaussian integrals for the cells at columns 11.5 and 15.5, which come out to roughly 0.8 and 3.7 before normalisation.

I'm now working through the Gaussian weights for the bank cells near the bottom stroke: column 7.5 comes out to about 0.28, column 19.5 to about 0.09, and the bank A and B rows nearby to smaller values that fall off with distance.

I'm working out the expected bank-cell weights around the bottom stroke, where the strongest entries sit at the row nearest the line and fall off with distance. Normalising those gives a per-cell pattern, and I'm checking how the unit-norm entries compare with the amplitude I'd expect for a real horizontal bar.

I'm working out the expected weights for the bank cells near the bottom stroke, which come out to roughly 2.1 once the blur is accounted for, so the probe should show whether the real response matches that prediction.

I'm settling on a 5×2 probe: five levels for the bottom-horizontal stroke response and a two-level read of the up-tip response, with a threshold of about 0.25 for the tip, so one readout covers both.

Setting the thresholds for the five-level stroke readout at 0.5, 1.2, 2.2, and 3.5, with their cumulative offsets. Each class's logit is then built from its level plus the tip state. Once that's wired in, I'll override the fully connected weights to make the probe.
