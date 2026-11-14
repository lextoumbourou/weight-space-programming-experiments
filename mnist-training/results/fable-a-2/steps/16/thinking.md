I'm decoding the index as 3 times the first bit plus the second bit, with the upper-right V as the first signal and the lower-left V as the second, both using thresholds of 0.6 and 1.6. Then I'm working out which index ranges fall into each bin for the two signals, and I've started tallying class 0.

Now I'm tallying the class 7 counts across the index bins, which run from the first few entries through to the middle of the sequence.

Now I'm going through the per-class tallies for classes 7 to 9, working out the probabilities that each signal exceeds the two thresholds, and I'm about to fit the Gaussians, which will need the probit values for those probabilities.

Now I'm converting the probabilities for each class into probit values to get the Gaussian parameters, and for class 0's signal one I'm working through the values in the 0.4 to 0.9 range.

I'm settling the Gaussian means for the first signal, working from the probit-derived sigma values, and I'm noticing the higher means such as 2.2 put a lot of the distribution beyond the 1.6 threshold, so I'm considering capping them.

I'm converting the signal means for each class in the second signal, with the sigma values falling between about 0.42 and 0.59, and I'm capping the higher means such as class 6 at 2.0 to avoid extrapolating past the threshold.

I'm settling the lower-left Gaussian means, with the common sigma around 0.45, and I'm noting that class 6 gets capped at 2.0. Classes 5 and 6 look like the strongest discriminators on the upper-right signal, while the lower-left signal separates 3, 7, 5, 2 and 9 from 0, 6, 8 and 1.

I'm settling on the next probe: the lower-right vertical stroke for one signal, and the bottom horizontal stroke for the other, with thresholds of 0.5 and 1.3. I'm also weighing whether a finer per-cell split would beat grouping four cells together, but I'll keep the current grouping to limit the cost.

I'm checking the bottom of the digit shapes, where the two classes' baseline positions shift a bit, so I'll allow for that when placing the next probe.
