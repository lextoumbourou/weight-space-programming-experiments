Now I'm mapping each digit's class from the top and bottom bins, starting with digit 0, which shows activity across most bin combinations. Digit 1 stays at low-low with no loop activity, which is what I expected. I'm moving on to digit 2, where the first count is 292 for the high-mid bin pair.

Now I'm going through digits 3 to 9 and their dominant bin pairs, but the detector fires on almost everything except 1. That makes it more of a stroke-density signal than a real loop finder, so I need a much stricter threshold, maybe around 0.7 of the ring instead of 0.45.

I'm now weighing a stricter loop test: requiring the ring to be covered on all four sides, or at least both the left and right, since a 3 lacks the left side. The current 0.45 threshold is too lenient, and I'm considering something closer to 0.7 of the ring so partial arcs stop counting as loops.

I'm weighing a hole detector that checks for empty space in the center with ink on all four sides. The catch is that a plain sum would let one strong side make up for a weak one, so each side would need its own clipped contribution before adding them.

I'm sketching the loop2 kernel as four side detectors, each reading one or two cells on its side with weight 0.5 per cell. A typical loop should only light up two or three sides, so the summed score needs a threshold around 1.8 to stop partial arcs from passing.

I'm thinking about per-side clipping, since a plain sum lets one strong side make up for a missing one. Conv1's orientation channels are already clipped to the 0–1 range, so a single cell per side would clip on its own. The open question is which radius works: a cell at radius 2 on the pooled grid covers loop sizes of roughly 3 to 5 pixels, which seems to fit the 8s and 9s.

I'm settling on a stricter loop kernel: one cell per side at radius 2, with a steep gain so all four sides need to be present. I'm checking whether one scale is enough, since a 2-pixel radius leaves no hole in the pooled grid, so radius 2 cells is the choice, and the 5x5 window covers the bigger zeros.

I'm weighing whether to drop the arc features, since they seem to fire on partial rings like everything else, and reuse those slots for a stricter loop detector. The plan is to rebuild the feature set around a four-sided loop test and check each side separately.

I'm weighing a more selective loop channel that checks the ring from one side at a time, perhaps by favoring a vertical side plus a second side that signals an open or closed shape.

I'm sketching the open-side variant next: a score that rewards ink on the top, right, and bottom while subtracting the left side, so a 3 or 5 can be told apart from a full loop. I'm also considering whether the loop's tilt means its side cells might pick up diagonal orientations, not just pure vertical or horizontal ones. For the strict loop channel itself, I'm settling on a four-sided sum with threshold 2.4 and gain 2, so it only turns fully on once the sides are clearly present.

I'm laying out the remaining loop-channel variants: an open-left version that rewards the top, right, and bottom sides and penalizes the left, plus a few other open-shape patterns. I'm also planning a center penalty on the middle cell and a rough template for the loop shape.

I'm assigning rough activation values to each digit for the open-side templates: the 3s and 5s get strong top and bottom responses, the 2s get a weaker top response, and the 7s barely register. The 6 has no stem-like top to match against the open-left shape, so I'm leaving that one out.

I'm testing whether a big 0's left half could serve as an open-shape cue, but its top sits too far above the window to match. I'm looking at a taller variant for the 0 instead, though a 5x5 window only reaches about 4 pixels up and down, which falls short of a tall loop.

I'm looking at a sixth channel, an open-bottom shape with the top and both sides present and the bottom missing. It might pick up the tops of 0s, since their top half fits within the window vertically, though the side cells only partly match the width.

I'm now weighing a few more weights for the open-top and open-bottom variants, with the side cells contributing partially for diagonal orientations. The sum has to stay capped, or the gain will let a single strong side push the score past threshold.

I'm working out the loop detector's threshold and side weights, using radius-1 and radius-2 cells at 0.6 each so loops of different sizes still register. That should give a good loop a total near 3.2, with three-sided partial arcs landing around 2.4 and below.

I'm checking the four-sided loop test: each side has to be covered by ink, since a single sample at radius 2 per side keeps a three-sided arc from passing a threshold of 3.2. Partial rings would then fall short, and a tilted loop would still count through the broad vertical tuning on the left side.

Writing the open-side detectors as weighted sums now: the left-open variant rewards top, right, and bottom while penalizing the left column and center, with a lower threshold and steeper gain. I'm also sketching the other two open-shape channels with the same structure, each flipping which side gets the negative weight.

Now I'm tallying the column sums per digit from the step 9 counts, so I can correct the predictions cumulatively.

I'm tallying column sums for the classes, with digit 1 running a bit high at about 1.23 relative to the rest. Next I'm weighing a new parts setting with a higher weight, which could shift the predictions, and I'm concerned that features with very low firing rates could skew the class scores through their log terms.

I'm weighing a per-side loop test at radius 2 with a steep gain, so a loop only fires when all four sides are present, and I'm working out the penalty and penalty-free weights for the open-shape detectors.

Now I'm setting the negative weights for the open-left variant, using -1.2 on the left-side vertical cells instead of the earlier -1.5.
