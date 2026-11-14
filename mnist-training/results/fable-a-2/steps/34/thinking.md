Eighty-six percent accuracy with a loss of 0.4555, so things are moving in the right direction. That leaves 17 steps, and each cycle of two probes plus a classifier buys about one more percent. I'm weighing four cycles against three cycles plus more tuning, since the tuning might pay off about as well. For now I'm planning steps 34 and 35 as probes, with step 36 as the classifier.

I'm sorting the remaining errors and column drifts to pick the next probes, and I'm looking at the unmeasured upper-right arc feature next.

I'm listing the unmeasured single-row features that could separate the remaining confusions, especially the upper-right arcs and the horizontal bars at rows 1 and 2.

I'm looking at which single-row features could still separate the digits, including the vertical stroke at the bottom centre, which would tend to pick out the stem digits like 1, 4, 7 and 9.

I'm checking the top confusions, 7 against 9, for features that could separate them. The strong signals are the bottom-centre horizontal and the top-left vertical, but 7s with a crossbar could still look like 9s, so I'm thinking about what distinguishes a closed upper-left loop from a bare top-right stroke.

I'm weighing two more probes for the 3-versus-5 split: whether there's a vertical stroke on the left at the top row, and one on the right. For 2 against 3, I'm considering a right-side feature at the lower row.

I'm checking whether the top-left and top-right vertical strokes plus a bottom-centre vertical would help split the 4s from the 9s, since the top-left prong should favour 4. I'll hold off on the second probe until I see how the first one does.
