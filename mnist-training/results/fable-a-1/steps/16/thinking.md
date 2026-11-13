I'm mapping each bit in the class code to its outcome: bit0 is the upper bracket-reaching G, bit1 the lower Hh, bit2 the lower hole L. For class 0 I'm summing the G contributions from the list, which gives 394, and checking Hh against the rest of the values.

Now I'm tallying the remaining classes, working out the G and Hh sums and the L values for each one.

Now I'm checking the last few classes, summing their G and Hh contributions and the lower-hole values, and then putting together the BR-upper and BR-lower tables.

Now I'm setting up the classifier from the measured zone stats, with the upper-left, lower-left and upper-right corner features for all eight zones.

Now I'm finishing the corner-zone inputs, listing the upper-right, lower-left and bottom-right values for each class and planning how they feed into the linear layer.

I'm turning the linear weights into a rule: each zone's evidence is the sum of its corner features, and I'd set the weight so a typical firing matches the target log-odds, with the bias absorbing the remaining log(1−p) terms. The catch is that the sum isn't clipped per zone, so a strong zone could push the evidence far above its usual level, which might be too much. I'm considering scaling the weight by a typical zone magnitude and clipping both ends of the log-odds so no single zone dominates.

Now I'm weighing whether to cap each zone's contribution so a single strong zone can't dominate the sum. I'd rather keep the features bounded per cell, since a typical zone sum lands around 0.5 and the outliers could push the evidence too far, though the cell-level corner templates may still clash with the measured zone stats.

I'm settling on dropping the hand-drawn cell-level corner weights and relying only on the measured zone-level stats, since those seem to fit better. I might bring the cell-level weights back at a small scale later to test whether they help.

I'm weighing how much to trust the correlated corner features: with a factor around 0.6 to temper the summed zone log-odds, the measured stats should carry more weight than the orientation part. I'm also starting to look at the hole-lower values, where only the four-size stats are available so far.

Now I'm working out the hole-lower and hole-upper rates by size, with the four-size lower-hole numbers scaled and the log-odds for the lower-hole slopes starting to take shape.

Now I'm working out the hole-lower slopes, with a constant shift applied to every class and the per-class bias terms from the log(1−p) values, starting with class 6 and class 8.

I'm settling the hole terms now: the lower-hole slopes stay as they were, with the gain set to 1.3 and no new hole-none arrays. The corner zone features already carry much of the loop information, so the hole adds mainly the AND, and the correlation between them means I need to lower the trust factor.

Now I'm working out the zone bias: the log(1−p) terms for each corner feature in class 0 add up to about −14.9, and I'll let the code compute the rest per class.

Still working out the bias term: I'm weighing whether to scale the zone weights by a typical firing magnitude, and I'll settle on a value for that shortly.

I'm resetting the bias adjustment to zero, since the earlier values were tuned for the hand-drawn corner templates I'm dropping. What's left is the orientation part, and in the no-corner run the class totals were uneven, with class 2 running low and classes 1 and 7 running high. So I'll set small offsets to compensate: +0.2 for class 2, and −0.1 each for classes 1 and 7.

I'm dropping the corner-feature weights from the code so it stays lean, though I might add them back later to test them.
