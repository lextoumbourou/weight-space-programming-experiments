I'm decoding the three features from the vector setup, then working through class 0 by summing the relevant bins to get each feature's share of its total count.

Now I'm running the same calculation for classes 1 through 6, summing the relevant bins and dividing by each class's total.

Still tallying the per-class totals...

I'm finishing the per-class tallies, then collecting the three feature vectors across all ten classes. The values show features 0 and 1 separate some classes well. Next I'll decode V(2,1), V(2,3), and V(3,0), and integrate at step 41, leaving out V(3,2).

With eleven steps left, I'll measure at step 40, integrate at step 41, and spend the remaining nine on tuning, steps 42 through 50.
