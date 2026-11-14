I'm mapping the SW-end codes to their pairs, then tallying the counts for Class 0 and Class 1, with Class 2 just starting.

Now I'm tallying the counts for each remaining class, working through the breakdown from Class 3 onward.

Still building the classifier tables...

Still tallying the NW-end counts per class, with the tables for the remaining classes...

I'm weighing the SW-end group against the diagonal groups: the new SW groups get a lower scale of 0.6 to avoid double-counting, since they overlap with the D-upper and L groups for classes 2, 3, and 7.

I'm setting the diagonal detector weights: since each diagonal's strength tops out around 1.0, the 0.7 scale is too low for those groups, so I'll use 1.0 there. I'm keeping the extra bias from before and will re-tune once the classifier is built, with 13 steps left.
