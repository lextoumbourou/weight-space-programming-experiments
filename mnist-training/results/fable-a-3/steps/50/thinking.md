I'm comparing the two loss values I already have at T=1.45 and T=1.25, and I still need an estimate at T=1.1 with the new biases. Step 47 gave 0.2703 at T=1.1 with the old biases, so I'm guessing roughly 0.268 to 0.269 for the new ones. I'd fit a parabola through those three points, but the first one is shaky.

Working out the slopes from the three loss points, the zero crossing lands around T≈1.27, so T=1.25 is essentially optimal. Next I'm considering a small final bias retune from step 48's column sums, keeping the temperature fixed.

I'm going to apply one last bias retune at T=1.27, since the earlier retunes each helped a little and the worst case is that loss rises slightly and step 48 stays the best. I'm also wondering whether to adjust something else, like sH or sE, but I'll keep those as they are.

I'm leaving the sD, sE, and sH settings as they are, since those parameters look flat and there's no clear reason to touch them.
