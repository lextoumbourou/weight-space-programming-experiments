I'm decoding each bit by summing the sensor readings in its group: the first feature is the '/' stroke in the lower-left, the second is ink on the left-middle, and the third is the bottom '\' stroke. For sample 0 that gives roughly 613, 985 and 936, and for sample 1 I'm starting on the same sums, 544 and 28 so far.

Now I'm running the same three sums over samples 2 through 9, and the scores are close for sample 9, so I'm checking that pair.

Checking the bottom-stroke sums, the '\' feature separates sample 7 (11%) from sample 9 (69%) cleanly, and sample 1 comes out low too. Next I'm building the model with the two probe features added, which brings the total to twelve stroke features, and I expect some correlation between them that I'll need to account for when tuning the smoothing and weighting parameters.
