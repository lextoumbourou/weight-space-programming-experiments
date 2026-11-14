I'm mapping each output to its bit pattern and then working out the four b-sums from those patterns.

Still tallying the per-class sums...

Working through the remaining classes now: for class 5 the b2 sum comes to about 4.5% and b3 to 0.8%, and class 6 gives roughly 4.4% for b2. Class 7 is partway through, with b1 at 12.8%, and I'm still tallying its b2 total.

Tallying the class 8 and 9 sums now: class 8 has b0 at 1.2% and b2 at 1.5%, and class 9 is mid-calculation with b1 around 8.7% and b2 at 14.5%.

Now I'm writing out the V-heavy column 3 figures per class, listing each output's percentage for the pair-sums (0,3), (1,3) and (2,3).

Now I'm setting up a classifier that uses the 20 heavy features, the V-heavy columns 1 to 3 and the H-heavy rows 0 and 3, treated as a Bernoulli naive Bayes model with the EH input folded into the logit.

I'm weighing how to scale the heavy-feature weights, since EH is continuous rather than binary and the clip on the small q values will set how strong those weights get.

I'm checking the sign logic on the heavy-feature weights: a class with q around 0.02 takes a hit of about 3.9 nats when a heavy stroke is present, against roughly 0.8 for a class near 0.45, so a heavy stroke excludes the rare classes strongly. A partial stroke gives a smaller but still clear separation, so I'm weighing how much scaling to apply there.

I'm settling on a heavy-feature scale of about 0.3 and clipping the heavy-stroke probabilities to [0.015, 0.97]. I'm leaving the extra bias from the earlier step unchanged for now and plan to re-tune it once the new features are in.

Still filling in the heavy-stroke table, now the remaining row-3 values for digit 3 and the entries for digits 4 through 9.

Now I'm filling in the heavy-stroke table for digits 5 and 6, working through each row's per-column percentages.

Filling in the heavy-stroke table for digits 8 and 9 now, working through each row's per-column percentages.

Still filling in the heavy-stroke table, now the row-3 values for digit 9 and the H-heavy entries for digits 0 through 3.

Still filling in the heavy-stroke table, now the H-heavy entries for digit 8.

Still filling in the heavy-stroke lookup table, now the row-3 values for digit 9 and the horizontal-heavy entries for the earlier digits.
