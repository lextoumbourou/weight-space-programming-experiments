I'm working out the decoding table for row 1 of H, matching each output pattern from o0 through o9 to its bit string. Next I'm setting up the sums that give b0 through b3 from those patterns, and I've started on class 0.

Now I'm tallying the digit-class counts into the four bit sums, starting with class 1 and then class 2, where 46% of the samples land in row 1, column 1.

Now I'm checking the class 4 sums: the crossbar shows up in row 1 only about 55% of the time, so it probably sits lower, in row 2. Next I'm moving on to class 5 and its counts.

Now I'm working through the class 5 sums, where b2 comes out near 93%. Then I'm moving on to class 6, where b0 is zero and b2 and b3 are high. Finally I'm starting class 7, where b0 comes to 63%.

Now I'm checking class 7's sums, where b1 comes to 92%, b2 to 89%, and b3 to 41%. That high row 1 rate seems surprising, so I'm reasoning that the long bar's half-weight contribution near the window edge is enough to push it over threshold.

Now I'm computing the bit sums for class 8, where b2 comes to about 54% and b1 to 39%. Then I'm moving on to class 9, where b1 and b2 both come out high, near 89% and 84%.

I'm weighing whether adding more H and V features will actually lift the naive Bayes classifier, since so many classes sit in the 85–92% range for row 1. I'm considering whether I should be more selective about which remaining measurements to take, rather than just pushing through all of them.

I'm setting up the next measurement: row 2 of H, using the same four-cell patterns and dropping the 1000 case as merged. I'm weighing whether to use four-feature runs along suitable lines to speed things up, even though that adds some bias.

Now I'm settling on whether to squeeze in another measurement or just proceed with row 2 of H, using the same pattern-matching approach.
