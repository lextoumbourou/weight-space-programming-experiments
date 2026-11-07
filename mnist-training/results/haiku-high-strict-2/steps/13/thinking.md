Step 12 fell to 44.5% from 50.5%, so the bias changes were too big and pushed unit 8 into a sink, which makes the network very sensitive. The best result so far is still step 11 at 50.5%, with three steps left before the final network is scored from step 15. I'm considering reverting to the step 11 deltas exactly and maybe making only tiny adjustments from there.

Checking the column sums, unit 8's sink grows from about 420 at −0.4 to about 2200 at 0.0, so that bias is very sensitive and the step 12 jump was the culprit. Keeping unit 8 at −0.4 or lower looks like the safer move.

I'm working out the bias for unit 8: at −0.25, the interpolation puts its sink near the target count, between the 420 at −0.4 and the 2200 at 0.0.

I'm now interpolating the bias for unit 8 between its −0.4 and 0.0 values, and I'm also checking unit 5, whose sink shrank from about 1540 at +0.5 to about 516 at +0.2.

Now I'm checking step 12's column 4 sums to see how the bias for unit 4 has shifted.

Working through the column sums now: unit 4 dropped from about 1250 to 526 with the −0.2 change, so I'm estimating the bias should sit near −0.05 to bring its count back toward 1000. For unit 7, the count is 844 against a true 1028, so it's still under, and I'm checking how far to push its bias up.

Raising unit 7's bias to 0.9 seems reasonable since it's still under its true count, though it could pull counts from other units. For unit 9, the interpolation points to a bias near 0.2 to bring its count back toward the target. I'm also checking unit 2, which has slipped under its recall, so I'm considering restoring its bias to 0.3.

Now I'm checking column 3 in step 12, recounting the per-row values to see how the bias for unit 3 is shifting.

Now I'm finishing the column checks: unit 6's sink dropped to about 805 with its recall at 524, which I'll attribute to the unit 8 change, and I'm keeping its −0.4 delta. Unit 1 still comes to roughly 1180, so it stays as is. I'm settling on the new deltas: 0.8 for unit 0, 0.0 for unit 1, 0.25 for unit 2, −0.3 for unit 3, and −0.05 for unit 4.

Now I'm settling on the final bias values for this step: 0.35 for unit 5, −0.4 for unit 6, 0.9 for unit 7, −0.25 for unit 8, and 0.2 for unit 9, mostly pulling the offsets back toward step 11.
