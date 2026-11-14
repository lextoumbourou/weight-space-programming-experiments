The 31-feature naive Bayes version reached 82.6% with a loss of 0.6376, so that approach is working. Next I'm measuring the diagonal features (32 plus H(0,3)), which should take about 8 to 9 probe steps, and after that scaling to 64 features, perhaps reaching around 88%. Beyond that I'd tune the weights with feedback.

I'm weighing whether a discriminatively tuned linear classifier on the 64 features could beat naive Bayes, since NB ignores feature correlations. Manual pairwise weight corrections for the confused classes look like a modest option, and the currently unused channels might carry new feature types.

I'm considering which new feature types would help most beyond the diagonals, such as endpoint detectors, long-stroke stem detection, half-cell offset grids, hole detection, and junction features. The biggest confusions involve 8, which is over-predicted since its probabilities sit in the mid-range and it rarely gets strongly penalised, so the diagonal features should help with that.

I'm deciding how to arrange the probe runs for the "/" diagonals: columns, rows, or anti-diagonal lines, picking whichever gives contiguous stretches. For each digit I'm sorting out where its right-leaning strokes sit, such as the 1's full-length slant and the 2's neck and top-left arc.

I'm checking how each digit's leaning strokes sit, since the "/" strokes in 1, 7, 4, 9 and 6 run steeply enough that probing along a column should give contiguous runs of cells. Some strokes, like the top-left arc of 2, would be split by a gap, so I'll need to account for that when choosing the probe layout.

I'm checking where the "/" strokes fall in each digit, so I can decide whether probing along columns or rows gives contiguous runs. The 2's top-left arc and neck would likely be split by a gap, and the 4's arm and stem sit side by side in the same rows.

I'm deciding whether to lay out the "/" probes along rows or columns, since each choice puts a different digit at risk of split runs. Rows keep the slanted 0's two sides together but fit the 9's loop and stem less cleanly, while columns do the reverse for the 2's neck. I'll go with rows and accept some bias on non-contiguous patterns.

I'm weighing whether the diagonal probes should use triples on the two middle rows, where a slanted zero might produce a split pattern like 1001 that the usual run patterns don't cover. That costs about two extra probe steps per orientation, so I'm comparing that against the bias from mapping the unseen patterns to their nearest allowed neighbours.

I'm deciding whether the "/" probes should run along rows or columns, and for a slanted zero the two sides could land in a 1001-style pattern that my usual run patterns can't express. Dropping that pattern would push it onto the nearest allowed neighbour and bias the zero's estimates, so I'm weighing which ten of the sixteen patterns to keep.

I'm weighing whether to probe the "/" diagonals along rows or columns. Zeros put the two sides in a pattern that the usual run patterns might not capture, so I'm trading that risk against the extra probe steps.

I'm checking whether zeros' two long sides, the left one near column 0 and the right one near column 3, would both register as "/" strokes along a row, which would produce a 1001-style pattern the run patterns can't express. Laying the probes out along columns keeps each side contiguous, so I'm leaning toward that for the zero's sides.

I'm checking the "/" strokes in each digit against the probe layout: for 0, the top-left and bottom-right arcs fall in different columns, and for 2 the top-left arc and neck would land in the same column with a gap between them, which could give a 1001 or 1011 pattern.

I'm considering whether to lay out the "/" probes along anti-diagonals instead, since a steep stroke would cross them, and two strokes on the same anti-diagonal would be separated by a gap of about 11 px.

I'm weighing whether triple-cell probes on the "/" diagonals are worth the extra steps: about 11 probes instead of 8, covering all 33 features cleanly, which leaves 26 steps for tuning but fewer for any new feature types.

I'm weighing whether to accept some bias in the diagonal probes by using run patterns, which costs 8 steps, against spending extra steps on triples to capture slanted-zero patterns cleanly. The marginal gain from new feature types seems worth more than tuning, so I lean toward the cheaper run-pattern layout and accept the modest distortion on zeros and twos.

I'm considering a 3-cell joint pattern for the two end cells plus a restricted set for the interior, so that a slanted zero's 1001 shape isn't forced onto a neighbouring pattern.

I'm checking whether a 1011 or 1101 pattern could show up for zeros in the row or column layout, where a gap cell sits between two strokes that are far enough apart. The interior cell would have to be empty while both sides have strokes, which is plausible for wide zeros but less so for the narrower shapes.

I'm weighing whether the two zero-sides in rows 1 and 2 would be underestimated at one end, which could push the model toward confusing zeros with eights. The run patterns can't capture the gap cases well, so I need to decide which few to drop.

I'm leaning toward using triples on the diagonal probes, since they would give clean data for the slanted strokes at the cost of about three extra steps. Run patterns would be cheaper, but they risk biasing the estimates for zeros in the "/" features, so I'm weighing whether that tradeoff is worth it.

I'm mixing the two layouts: run patterns for the top and bottom rows, where strokes should stay contiguous, and triples for the middle two rows, where the slanted zero and two sides could split. That comes to about 10 probe steps, between the 8 of all-runs and the 11 of all-triples, and the difference is small.

I'm wondering whether the diagonal probes need triples after all, since run patterns would leave the slanted strokes in row 0 of the "/" probes vulnerable to split patterns like the ones a 4 would produce. Triples would cost about 11 steps, which is a large share of what's left, but the data would be clean. I'm also considering dropping the weaker corner features to save steps, since each remaining feature still carries some information.

I'm thinking about whether the diagonal features are worth their probe cost, or whether new feature types aimed at the 8-related confusions would do more. A "\" stroke through the centre cells looks like it would separate 8 from 0, 5, and 9, so I'm weighing that against the diagonal probes.

I'm ordering the diagonal probes by expected value, starting with the central "\" cells, since that stroke looks most likely to separate 8 from 0, 5, and 9, and I'm planning to group them into triples.

Next I'm grouping the remaining diagonal probes into triples, starting with the "\" cells at the top right and bottom left, and then the "/" cells along the top-left arcs and the lower middle.

I'm laying out the remaining diagonal probes as triples, running through the "\" and "/" cells along the edges and the lower middle, and I can stop early if the gains taper off.

I'm considering spending the two spare outcomes on a fourth feature, measured only within the all-absent stratum, since for most classes that stratum is large and the estimate would be reliable, though I'd still need to see how it does for 8.

I'm weighing whether the two extra outcomes in the all-absent stratum should come from the far corners, since the corner strokes are expected to be rare and would avoid overlap with the central triple.

I'm settling on a decoding scheme for the next probe: three centre-diagonal "\" cells set the low three bits of the outcome, and two far-corner "\" cells serve as extras that only matter when all three are absent.
