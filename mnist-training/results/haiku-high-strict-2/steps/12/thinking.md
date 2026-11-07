I'm at 50.5% now, so progress is being made. Next I'm looking at the confusion pairs: 9 is recalled poorly (196 of 1000), with 9 often predicted as 4, and 0 and 5 and 3 also turning up as errors. The 0s are most often misread as 6, 8, or 2, and 8 gets confused with 2, 3, 5, and 6. I also want to check 3 being read as 5 and whether 5 gets read as 3, against 621 correct for 5. Then I'll tally the predicted counts for column 0.

Now I'm tallying the predicted counts for each column against the true labels, checking which digits are over- or under-predicted, and nudging the deltas for 5, 8, 9, 7, 2, and 4 accordingly.

I'm settling the per-digit deltas now: 0 stays raised, 3 stays lowered, and 6 is unchanged. I'm nudging 2 and 5 down a little, 4 down, 7 and 9 up, and leaving 8 at zero so the correction doesn't overshoot.

Still tuning the per-digit deltas, and I'm now going back over the template choices for 9 and 4, since they may look too alike.
