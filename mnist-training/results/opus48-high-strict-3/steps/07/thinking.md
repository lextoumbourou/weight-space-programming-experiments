Accuracy has reached 41%, which is progress. Next I'm working through the per-class recall numbers to find the weakest classes, which are 7, 5, 4, 9, and 8. I'm also starting to total the predicted column for class 0.

Now I'm checking the column totals and confirming they sum to 10,000, with the predicted column for 8 and 9 running high while 0 and 7 fall short. The biggest problem is 505 ones read as sevens, and 7 is confused with both 9 and 5.

I'm thinking the 1-versus-7 mix-up is the biggest issue, since 505 ones are being read as sevens, and my 7 template's top bar may be overlapping the region where a 1 would have its serif. I'll look at whether the 7 template is too strongly matching 1s.

I'm weighing whether to adjust the bias to bring down the overcounted 8s and balance the totals, and I'm considering refining the "1" template, since many 1s score higher against the 7 template than the 1 template and its slanted stroke may be matching 7's diagonal.

I'm weighing whether the scale should go up, but since 59% of predictions are still wrong, a sharper scale would just make those errors costlier, so I'll leave it. Instead I'll adjust the biases directly: lower the 8 bias, which is over-predicted and feeding the 8→2 confusions, and lower the 9 bias, which is also running high.

I'm weighing whether the 1-versus-7 confusion comes from my 7 template overlapping the 1's vertical stroke through the center, so I'll try to make the 1 template cleaner and less flagged.

I'm weighing whether to sharpen the "1" template so it beats the "7" template on real 1s, since 7's diagonal runs through the center where the 1 stroke sits. That would recover some of the 505 misreads, but it would also pull in more non-1 digits, so the gain isn't guaranteed.

I'm now trying to fix the 1-versus-7 mix-up by boosting the "1" template's bias and lowering the "7" template's bias, though I expect 7 recall to drop somewhat. I'll also reduce the 8 bias further, since it's heavily over-predicted.

I'm adjusting the biases directly this round: dropping the 9 and 6 biases, nudging 0 and 4 up, and trimming 5 and 3. I'm also considering a template edit for the 4-versus-9 confusion, which is the largest remaining error after the 1-versus-7 mix-up.

I'm settling on new bias values this round: nudging 0, 1, 5 and 6 up or down, pulling 4, 7, 8 and 9 lower, and keeping 2 and 3 close to where they are, all with the scale held at 2.

I'm settling the bias changes: nudging the 1 bias up and the 7 bias down by 0.10 each, to see whether more of the 505 ones read as sevens can be pulled back.
