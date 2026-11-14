I'm working out the parity constraints: b1, b2, and b3 are each XOR sums over subsets of the o-variables, and I'm tying A and B to o8 and o9 so that the stratum is o0 plus those two. Now I'm listing the Class 0 values, starting with 3, 0, 20, 0, 480, and so on.

Now I'm working through the per-class tallies for classes 2 and 3, checking each parity bit and the stratum splits against the counts.

I'm going through the remaining class tallies, comparing each parity bit and the stratum split for class 4 and now moving on to class 5.

I'm checking the remaining class tallies: for class 6, the parity bits come out around 3%, 41%, and 44%, with the stratum split showing 98% on the B side. Now I'm starting on class 7's parity counts.

Now I'm tallying class 9's parity bits, with b1 around 37% and b2 pushing toward 64%, before I get the stratum split for it.

I'm tallying the remaining parity bits for the last classes, with b1 at 37% and b2 pushing toward 65% for class 9, and I'm tracing each bit's position across all ten classes to see where the tilt toward a one-hot pattern shows up.

I'm settling on the H(0,3) estimates per class, and I'm leaning toward a rough set of values, with small strata pulled toward the middle. I'm using 60, 2, 25, 36, 4, 90, 14, 70, 68, and 48 as the working q values for each class.

I'm settling on the "/"(0,1) conditional estimates per class, working from the stroke shapes: class 6 looks nearly certain to have that top-right stroke, class 4 less so, and class 1 is low, since its top sits further right.

I'm settling the "/"(0,1) estimates per class, with class 5 a bit uncertain since it has few samples, so I'll shrink that value. Next I'm turning to the remaining "\" features at (2,3), (3,3), and (0,0), and looking at which "/" positions on the top, bottom, and sides are worth measuring.

I'm deciding to measure the remaining "/" features on the bottom and top rows, since the corner and edge positions should discriminate better than the centre ones, even though that's about four more steps.

I'm weighing whether to run a checkpoint classifier now, once the "\" features are complete, so I can see how the naive Bayes setup performs before adding more probes. The next step would measure three more "\" positions, with a few "/" features as extras conditioned on the earlier ones.

Choosing the two extra "/" probes: I'm settling on A = "/"(3,3) and B = "/"(0,2), since the strata for several classes should be large enough to be worth splitting on.
