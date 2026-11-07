I'm checking whether the bias of +0.8 on digit 9 is too strong, since it's pulling in too many predictions from 4 and 7. Looking at the column sums against the true counts, digit 3 and digit 9 are both running high.

I'm going through the bias adjustments for each digit, trimming the ones that run high and nudging up the ones that run low. Digits 3 and 9 need the biggest cuts, while 4, 8, 7, and 1 get small boosts. I'm also weighing whether the templates for 2, 4, 8, and 0 need structural changes, or whether the confusions are mostly a bias problem.

I'm weighing a few small template tweaks against just adjusting biases, since there are only six steps left. I'll likely keep the templates as they are and go with bias changes, maybe with a modest adjustment to the 2 template to cut down its confusion with 3.

I'm settling on bias-only changes for the remaining steps, since there are few left and template edits would be risky now. I'm also considering whether the 8 template needs changes, like a smaller top loop and a heavier slant, though I'm leaning toward leaving it as is.
