I'm working out the decoding formulas: f0, f1, and f2 are each a sum over four of the eight o-values, and I'm checking the first class's numbers against them. For class 0, the f0 sum comes to 989 out of N=991, giving about .998, and f1 comes to 679, about .685, which is where I've got to so far.

I'm running the same f0, f1, f2 sums over the remaining classes, with class 6 partway through its f0 total.

I'm checking the classes 7 through 9 with the same sums, and class 7's f0 comes to 168, about .154.

I'm now checking class 9's sums, which come to 475 for f0 (about .494), 28 for f1, and 465 for f2. I'm comparing the H(3,1) and H(3,3) values across all the classes, and class 4's H(3,1) of .68 looks suspicious for a bottom-row cell in a 4.

I've finished the H cells, so next I'm moving on to the V features, then the diagonals. With 29 steps and about 23 features left, the budget works out. I'm also wondering whether to try an integration step now, to see whether the measured cells help before I continue.

I'm going to check whether the mid-way integration test is worth doing, since the measured corner cells matched the hand templates. Step 22 covers the three remaining V features: V(0,2), V(1,1), and V(1,3). I'll do the check after the V features, at step 25, to avoid spending eight steps if it isn't helping.
