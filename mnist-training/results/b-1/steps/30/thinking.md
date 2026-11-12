The accuracy reached 73.3%, but the loss rose to 0.874, probably because the lam_ori change increased the overall logit magnitude and so raised the effective temperature. I estimate the template part's logits grew by about 1.22×, which would put the effective temperature near 0.86, so I'll lower gscale to 0.58 to bring it back and recalibrate β as well. Next I'm counting the columns at step 29.

Now I'm tallying the per-row column sums at step 29 and estimating how much β should shift for each row.

Working through the per-row shifts now: the largest moves come from rows 4 and 0, with rows 6, 8 and 9 pulling β back down. I'm applying the gscale change to 0.58 alongside these adjustments.
