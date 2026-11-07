The bias rebalance got me to 40.63%, a new best, with two steps left. Now I'm looking at the confusion matrix at step 13: 4→9 is still heavy at 540, and column 9 is over its marginal while column 4 is under.

Now I'm weighing a bias shift: 9 is still over-predicted and 4 under, so lowering the 9 bias and raising the 4 bias should turn some of those 4→9 errors back into 4s. I have two steps left, so I'll try the adjustment in step 14 and keep step 15 as the safe final.

I'm weighing a moderate shift: lowering the 9 bias to -2.0 and raising the 4 bias to -1.0, since the 4→9 errors are so lopsided. I'm also checking the column 7 marginal, which sits under at 864 with 7 recall only at 160 and most of its errors going to 5 and 1.

Now I'm working out the marginal sums for each column, roughly halving them to scale the bias update across all classes.

Now I'm tallying the column sums and flagging which classes are over-predicted (9, 1, 3, 2) and which are under (4, 8, 7, 0, 6, 5), so I can scale the bias update by about 0.6.

Now I'm recomputing the per-class bias update from the step-13 marginals, scaled by 0.6, which moves class 4 up to -0.95 and class 9 down to -1.84. I'll use those new biases for step 14.

Writing the step 14 config now: the same setup as step 13, with only the bias values updated.
