The results match the earlier run except for row 2, which dropped from 697 to 510, apparently because of the ink cue at (2,3) contributing a −0.6 shift. That's surprising, since I hadn't expected 2s to have ink in those lower-right middle rows, but they do. The hole channel seems to contribute nothing; the rows are nearly identical, so the hole detector probably never fires because its threshold is too high. Row 9 barely moves, from 618 to 620.

I'm checking whether the column mapping for the channel is right: the pooling arithmetic gives centers at 4j+4 through 4j+7, which matches what I assumed. But the ink positions for 2s and 7s look off from my geometry, so I'm wondering whether a 2's arc and diagonal really reach rows 14-17 in the lower-right middle.

I'm weighing whether to drop the ink cue at (2,3) and soften the V cue for 2s, since their arc-to-diagonal turn seems to sit in rows 13-15 on the right side. That would leave the step-7 state as the base. For the hole detector, I'm considering lowering its threshold, though a loop-free stroke could then fire weakly, so I'm not sure that's the right fix.

I'm weighing whether a loop detector can separate a 9's narrow loop from a single stroke. With sides at taps (0,1) and (3,4), a single stroke gives roughly the same response on one side as two strokes do across both, so a threshold alone won't separate them.

I'm working out the hole detector's geometry: two taps three positions apart could separate a 9's loop from a single stroke, if the centre taps are negatively weighted to suppress the middle. The side leakage is small enough that the arithmetic seems workable, though I haven't confirmed the exact weights yet.

I'm checking whether the hole detector's side taps can be separated from a single stroke at all. A 0 barely registers, so the spacing of the taps is probably too wide for loops this narrow. Pursuing a fix would be worth roughly a few percent with seven steps left, but simpler adjustments might pay off faster, so I'm weighing that next.

Now I'm looking at the per-digit error counts for the step-7 state, and sketching a second hole detector with two side-tap spacings, one wider and one narrower, to separate loops from single strokes.

I'm working out the hole detector's taps for a narrower spacing: with strokes six pixels apart, one side's taps would pick up the other stroke's leakage, so I'd put negative weights on the two middle taps to suppress that. A wider spacing of eight pixels, with the centre tap negative, looks cleaner, and a threshold near 0.95 might separate a loop from a single stroke. I'm also considering a separate channel with spacing 10 to 12 for the 0s.

Settling the threshold: a single strong stroke tops out around 1.0, so a threshold of -1.0 should let two-sided responses (about 1.6) fire without firing on one stroke. Next I need to check whether vertical strokes six to eight pixels apart could fire the detector on non-loop digits like 2, 3, 5 or 7 by mistake.

I'm reverting the ink cue for 2s and softening their V cue, and resetting the bias for 2s to zero. I'll also try the hole detector with a bit of spacing and negative centre weights, rather than testing a gain change in this step.
