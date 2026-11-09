I'm at about 79.77% now, with five steps left. Next I'm tallying the recall counts for each row and working out the column sums, where the first column comes to 1066 and the second to 905.

Now I'm working through the column totals for each digit row, checking the sums against the recall figures, and I've noticed that row 4 is clearly the weakest, with 4→9 accounting for a surprisingly large share of its flow.

I'm weighing whether the 145 counts for 4→9 could be closed-top 4s, since about 15% of 4s would fit that share. If so, the hole detector is firing at the top, and I need a cue that separates a closed 4 from a 9, like the crossbar extending past the stem and the diagonal left side of the loop.

I'm weighing the 4→9 confusion as a feature issue: a closed-top 4 and a 9 both light up the hole detector, so I need cues that separate them. The idea is to penalize the 9 class on a horizontal bar that sticks out to the right of the stem near the bottom, since a 9's loop joins the stem there instead.

I'm checking whether the 4→9 flow could come from closed-top 4s, and a crossbar that ends to the right of the stem would be the cue that separates them from 9s, since a 9 has no right-pointing ends there.

I'm checking whether the 9 class could be penalized on right-pointing crossbar ends, and I'm considering raising the negative weights on that cell for 9, and for 8 and 6 too, since those are the other common confusions with 4.

I'm weighing whether the 3→5 confusions, at about 107 counts, come from a similar structural cue, and I'm considering whether the upper-left stroke of a 5 could be what separates it from a 3.

I'm now checking whether the 3s that get called 5 are the ones with a flat, Z-shaped top, where the bar and diagonal could look like the upper-left stroke of a 5.

I'm now checking whether the 3s that get called 5 have a round, deep middle indentation, since that would give them a right-facing bay that looks like a 5's upper-right stroke. The open question is whether the 5s' bay sits higher up, which would separate them from these 3s.

I'm now testing whether the bay for 5s sits higher than the one for these 3s, since a bay at the upper-right would give the 5 its signature and keep the two apart.

I'm tuning the bias for class 5 downward slightly and checking whether the 3s that get called 5 are simply pulling toward the same right-facing bay. Next I'm turning to the 6→0 confusions, where I'm weighing whether a loop-top bar crossing the middle could separate 6s from 0s.

I'm adding a negative H-only rule for class 0 at the center rows, since real 0s have no horizontal stroke there, and nudging its hole weight at k=2 up slightly to separate it from 6s. I'm also lowering the 0 bias a little more, and I'll look at the 7→9 and 7→5 confusions next.

I'm looking at the 1s now: only 25 false positives, so raising the bias barely moves anything. The 1s that get lost look like 4s, 7s, or 2s, which suggests the template is missing a flagged, based variant of the 1.

I'm wondering whether thick strokes are the broader problem: a bold 1 that is five or six pixels wide would weaken the orientation features and make the cosine match noisy, which could push it toward 4, 7 or 2. My filters were tuned for roughly 3-pixel strokes, so bold writers may be spreading errors across many classes, and I need to check how the detectors respond to thicker ink.

I'm checking whether thick strokes weaken the bar filters: a 4 to 5 pixel wide stroke would give about half amplitude at its two edges and little at the center, so after the bias the response drops to roughly 0.3 against a normal 0.75. The shape stays the same, though, so the cosine match should still hold, just with less signal relative to the biases and the structural cues.

I'm testing whether a non-zero-sum bar profile, something like [−0.6, 0.6, 1, 0.6, −0.6], would hold its response for thick strokes better than the current zero-sum filter, since that's where the thick-ink weakness comes from.

I'm checking whether thick strokes break the orientation filters. A 5-pixel-wide vertical stroke fills the whole 5x5 window, so the horizontal and vertical filters would respond about equally, and the orientation signal disappears for bolder ink.

I'm weighing whether raising the weight on the template evidence would matter more than adjusting the biases and structural cues, since that is the one lever I haven't tried yet.

I'm now weighing whether the 4→9 confusions come from closed-top 4s, and whether a right-side cue near the middle rows could separate the 9s from those 4s.

I'm now checking whether the 4s that get called 9 are open-topped ones whose wide opening stops the bay detector from firing, since the two verticals sit too far apart for a centered bay to see both walls.

I'm thinking about whether the 4s that become 9s could be spotted by a corner detector, since the crossbar's lower-left corner where the vertical meets the horizontal is a distinct feature. Interior cells near that corner, with ink to the left and below, might give a usable cue.

I'm checking whether a corner detector looking down and to the left could tell a 4's crossbar corner apart from the loop of a 9, since the 9's loop should close above that spot and block the signal.

I'm checking whether a corner detector looking down and to the left could catch the 4's crossbar corner, since the interior there should be open upward and to the right. I'm also running through the other digits to see where that cue would fire by accident, such as 0 and the wide-open 4s.

I'm weighing whether to drop a channel for a new corner detector aimed at the 4s that get mistaken for 9s, since the candidates I could remove all carry unknown value. I'm also considering whether the gain, maybe around 50 of the 145 errors, is worth the risk of losing something else.

I'm weighing whether to try a weights-only tweak next, since changing the channels would be too risky without a way to evaluate them. Starting with the biases, I want to adjust them gently.

Now I'm recomputing the bias for each class from the log of its count ratio, damping the step by 0.4, and I've got the new values through class 8 so far.

Now I'm tuning the class-9 handling: the right-side ending near the middle rows should be pushed strongly negative, since it marks the crossbar end of a 4, and I'm checking that the 6 and 8 cases don't trip it.

I'm adding a negative horizontal-only rule for class 0 at the center rows, since its middle has no stroke, and I've confirmed it stays clear of the top and bottom arcs. I'm also pushing class 6 down at the upper-right rows, where a 0's right wall would sit, while leaving the 4's right stem only slightly affected.

I'm working out a penalty for class 0 so that the 6s, which have an upper-right stroke start, don't get pulled toward it. Since 0 has no endings at the top, I'll look at whether an end cue near the top of the frame could separate the two.

I'm now looking at 8 more closely, since 3, 5, 2 and 0 all get pulled toward it. Its distinguishing features sit on the left side in both halves, so I'm considering a small bias cut paired with positive weights on upper-left and lower-left strokes.

I'm settling on a set of weights-only tweaks: nudging the class biases, adding a negative horizontal rule for class 0 in the middle rows, and penalizing the upper-right vertical and diagonal cues for 6. I'm skipping the left-side reinforcement for 8 since its magnitudes are unknown and too risky to guess at, and I'm now checking whether the 2-vs-0 corner weights could be adjusted to reduce those confusions.

Next I'm writing the code for the ending rules: class 9 gets its ER-channel weights pushed negative at the middle rows, and classes 8 and 6 get a milder cut there.
