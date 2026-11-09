I'm at a 74.2% plateau, and template tweaks aren't moving it much. With five steps left, I'm weighing whether to try something riskier with a fallback. I'm also considering tuning the loss gain down to 10, since gain 11 seemed to raise loss, though other changes muddied that comparison, so I'll skip it for now.

I'm weighing whether to tweak the per-digit negative weights, since 7 and 9 keep getting confused and 7 currently gets a weight of 0.7. Raising the 7 weight to 1.2 might help, because the tanh saturation makes a simple global change hard to apply.

I'm weighing a candidate for step 11: the 6→4 confusions jumped to 101, probably because the left-arm emphasis on the 4 matches the stem of a 6. I'm thinking about removing that left-arm emphasis while keeping the bar-right one, and raising the 4 weight.

I'm weighing a few options for the next step: a bigger confuser weight on the 4 against 6 confusions, a 7-versus-9 adjustment that I'd rather hold off on since 9 is sensitive, and a possible third variant for the 2s to cut the 2→3 errors. The 3→5 and 5→6 confusions look like the next things to watch.

I'm looking at the per-digit bias counts against the true row counts: 1 and 0 are overpredicted, while 5 and 6 are underpredicted. I'll apply the bias adjustments for those digits. I'm also going ahead with the 4 left-arm change, the 7 negative weight increase, and the 3-confuser tweak, and skipping the extra 2 variant.
