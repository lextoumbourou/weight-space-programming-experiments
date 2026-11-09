Seven errors rose from 737 to 597 while 7→9 confusions climbed to 224, even with the bias nudged up, so the 7s must be carrying more energy in the middle horizontal band than I assumed. I'm wondering whether it's crossed sevens or a diagonal stroke sitting around thirty degrees from vertical, and I suspect the ink is landing somewhere I don't expect, which the (1,1) cue also hints at.

The 7s seem to sit lower than I assumed: centroid-centring pushes their heavy top bar down into roughly rows 6–10, which would spill into the middle band and explain the mid-horizontal energy. That suggests restricting the mid-horizontal cue to the lower row, since most other digits' crossbars and loops sit lower or are too uncertain to separate cleanly.

I'm wondering whether the 2s also carry more horizontal energy than I expected, since they seem to be pushing predictions toward 3. Their diagonals may be shallower than I've been assuming, so the horizontal response could be leaking more than I thought.

I'm weighing whether to keep the mid-horizontal cue at all: reverting to the step-9 version gave the best score so far, and with only five steps left I'd rather make small, safer changes. The gains in 9, 6 and 5 look worth keeping, while 7 and 8 moved the wrong way. One option is to keep the cue only on the lowest row and drop the penalty on 7, with the other weights left at zero, though I'm not confident that will help.

I'm working through the 7→9 confusions: even with 9's bias pushed lower, 7s are losing to 9, which suggests the 7 images carry a lot of horizontal energy in rows 10–17. My guess is that this comes from the top bar sitting around rows 8–10, so my 7 template with the bar near row 7 may still be roughly right.

I'm checking whether my row mapping is off by one: the second-layer cell covering rows 10–13 might actually sit higher, and I'm working through the index arithmetic to confirm which conv1 centres feed into it. If the mapping holds, the 7 bars would be landing around rows 9–12, which is where the mid-horizontal energy is coming from.

I'm working out the centroid for the 7 more carefully, which puts the bar near y≈8.7 and leaves it spilling into the row 1 band. That means I'll restrict the cue to the lowest row (14–17) and skip the 2s, whose diagonals may be too shallow to separate cleanly.

I'm checking where the 3s, 5s, 6s and 9s put their horizontal energy against the row boundaries, since the 3's cusp lands right on the edge between rows 1 and 2. The 5 and 6 sit higher, around row 1, while the 4's crossbar and the 9's loop bottom fall squarely in the lowest row, so a cue on that row alone should separate the 9 cleanly.

I'm looking at which row-2 cells should carry the cue: 9 and 4 get positive weight with a negative bias, while 7, 1 and 0 get a penalty, since 7s rarely have their diagonal reaching that lower band. I also want to check whether the 9→4 and 6→4 confusions can be pulled back with the same adjustment.

I'm keeping the row-2 cue as the only mid-horizontal term and building from the step-9 base. I'll retune the 4, 6 and 9 biases to match, and I'm also thinking about whether to adjust the gain next.
