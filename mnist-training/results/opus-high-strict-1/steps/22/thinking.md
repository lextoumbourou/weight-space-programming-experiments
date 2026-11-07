I'm checking the step 22 to 25 deadlines against the earlier best scores, and step 22's 77.27 clears the threshold of the best score up to step 17.

I'm working out how many steps remain to gain the extra 0.5 by step 26, and checking which pair (3→5) has the most errors left. I'm considering whether the orientation penalty is too blurred to tell 3s from 5s, and whether a sharper template for the penalty mask would help.

I'm going to try a sharper template for the penalty mask, using a smaller blur only for the "empty" check, and keep the reward template as it is. I'm also adding small per-digit bias corrections based on the column sums, nudging 2, 3 and 8 up and 0, 4, 6 and 9 down.
