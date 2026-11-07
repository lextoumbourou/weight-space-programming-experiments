I'm noticing that the hole classes (6, 8, 9) have collapsed, with 8 almost never predicted and 9 and 6 rarely. That suggests the hole detectors are barely firing, and the normalization is pushing weight onto the hole templates instead, so I'm suspecting the thresholds are set too high.

I'm working out whether a single weighted sum can capture a hole. Requiring ink at both one and two cells out in every direction seems too strict for small loops, since the nearer cell may still fall inside the hole. An OR across the taps can't be expressed as one linear threshold, so I'm weighing whether a lower threshold over all eight taps could work, though corners and sides would then score alike.

I'm trying an OR-like hole detector: a soft ReLU over all eight taps plus the center, with a lower threshold, so one side doesn't need both near and far ink. I'll keep its template weight small so it doesn't take up norm from the other classes.

I'm decoupling the hole terms from the normalized template: the first twelve channels get the normalized weights, and the hole weights are added as a separate absolute term, so an unfiring hole detector costs nothing. Holed classes would get a positive hole weight and the rest zero, with the magnitude set by the detector's value above its threshold.

I'm weighing a decoupled hole term: keep the normalized weights on the first twelve channels and add the hole weight separately, so a silent detector costs nothing. The open question is the threshold, since corners and sides can reach the same sum from the eight taps.

I'm accepting a soft hole detector since a single linear threshold can't tell a corner from a ring. Its weight stays separate from the normalized template, so an unfiring detector costs nothing.

I'm weighing per-direction thresholds by splitting the hole detector into separate vertical and horizontal enclosure channels, but each would still only see a summed sum of its taps, so the corner problem returns.

I'm weighing a single hole detector that sums the center and all eight taps, since the one-and-two-cell taps in each direction may both fall inside a small loop's interior. I'm settling on a lower threshold, accepting that corners and rings can still score alike.

I'm settling on a weighted hole term: twice the center's emptiness, a half weight on the ±1 taps, a full weight on the ±2 taps, and a threshold of about 4.6. Rings and three-sided U shapes should clear it, while corners fall short.

I'm making the hole term independent of the normalized template: I'll set its weight directly, so a detector that stays silent costs nothing. The hole detector would use a soft ReLU with a bias of about 5.0, so that rings score clearly and three-sided shapes only weakly, and the hole weights get placed at the template's cell locations.

I'm settling the hole term's weight at 1.0 and keeping the bias values from step 7, since the non-hole part is unchanged when the detectors stay silent.
