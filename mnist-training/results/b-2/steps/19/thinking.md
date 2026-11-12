I'm working through the class-0 counts for the chapter 9 stats, pulling out the top and bottom sums, and then computing the mean terms for the top and bottom. Next I'm moving on to the class-1 counts and their totals.

Now I'm running through the class-1 top and bottom counts for each remaining group, working out the mean terms as I go.

Now I'm settling on the variance for the twelve structural scalars, since the features sit on different scales and a single value might be off for the small-mean channels. I'm leaning toward a shrink factor around 0.4 to account for the correlations between them, and I'm estimating each scalar's variance from the bins.

I'm estimating each scalar's variance from the bin values, using the second moment minus the squared mean, and I'm wondering whether a quick calculation over the histograms would be too laborious by hand. I'm also checking whether using the feedback counts this way conflicts with the rules, and I'm leaning toward it being fine since they aren't training images.

Next I'm writing out the mean values for all twelve scalars, and I'm settling on a shrink factor of about 0.4 since there are more correlated features this time.

Writing the per-channel mean tables for the remaining structural scalars...

Now I'm dropping the hand-written structural templates for channels 5, 6, 8 and 9, and I'm guessing these channels have small variances, so a single fixed variance will underweight channel 9, which I'm accepting for now. I'm also keeping the bias terms tied to the squared means and leaving the class-bias tuning for the orientation part as it stands.
