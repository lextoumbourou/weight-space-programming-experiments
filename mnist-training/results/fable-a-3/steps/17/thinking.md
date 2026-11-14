I'm decoding the bit-parity equations, working out which outputs feed each of the three parity bits and how the stratum and the two reference outputs relate. Next I'm checking the class 0 counts against those mappings.

I'm now working through the per-class bit rates: for class 0 the parity bits come out to about 7%, 69%, and 94%, with stratum 45 all matching A. Class 1 gives roughly 14%, 13%, and 0%, and its stratum-888 split puts A near 75% with B around 15%. I'm still computing the remaining classes' parity rates.

Now I'm working through the remaining classes: class 4 comes out to about 6%, 10%, and 5% on the three parity bits, with stratum 837 leaning toward A at roughly 78%. Class 5's parity rates sit near 14%, 14%, and 13%, and its stratum-658 split gives A about 65% and B around 15%.

Now I'm checking the class 7 parity rates, which come out to about 25%, 51%, and 33%, and the stratum-408 split puts A near 71%.

Now I'm checking the class 8 parity rates, which come out to about 40%, 71%, and 70%, with stratum 148 leaning strongly toward A at 92%. Class 9 follows with roughly 17%, 79%, and 65% on the parity bits, and its stratum-123 split puts A near 86%.

Now I'm tabulating the top-row bit rates for each class across the three parity equations.

Now I'm reading the "/"(2,1) estimates per class, which run high everywhere, so that output carries little information; I'll use those conditional values as rough q's.

I'm lining up the remaining "\" features, with (0,0) rare apart from classes 4 and 7, and planning three triples to check next: (3,0),(3,1),(3,2), then (1,0),(2,0),(1,3), then (2,3),(3,3),(0,0). After that I'd pick some "/" features, since the central ones carry little information.

I'm picking the top-row and bottom-row "/" features next, since the arcs there should split the classes well. After that I'll build the classifier with about 57 features and still have a few dozen steps to spare.

I'm now settling on the next extras: I'll test the "\" features at (3,0), (3,1), and (3,2) as one triple, and pair "/"(2,2) with H(0,3) as the extra features for this step.
