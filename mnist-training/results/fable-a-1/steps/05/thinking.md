Now I'm reading the diagnostic results at θ=1.5: class 0 fires on about 12% of samples, which fits its hole being too large. Class 2 fires on about 32%, with the upper-layer rate around 8% and the lower-layer rate around 23%.

Now I'm going through the per-class firing rates for the remaining digits: class 3 at about 25%, class 4 at 26%, class 5 at 19.5%, class 6 at 61.5% with its firing mostly in the lower layers, class 7 at 6.6%, class 8 at 83%, and class 9 at 53.5% with its firing concentrated in the upper layers.

Now I'm reading the lower-half level-1 likelihood ratios: class 8 and class 6 carry the strongest evidence there, while class 1 contributes almost nothing.

Now I'm checking the remaining lower-half likelihood ratios for digits 6, 8, and 9, where the evidence is strongest, and noting that the "none" rates for 8 and 6 are much lower than the others.

I'm checking whether lowering the threshold would catch more of the 6s and 9s, since the "none" group for 6 is around 37%, and weighing that against the extra false positives it would likely bring in.

I'm working out the likelihood ratio for the lower half: digits 6 and 8 carry the most evidence there. Roughly, the log-likelihood ratio for 6 against 5 comes out near −0.74 with no loop, and climbs as the loop level rises, reaching about 2.9 at the highest level I'm looking at.

I'm settling on the shape of the feature: a linear function of the hole measure with slope around 1.8 and intercept near −0.7, since a straight line can't capture the sharp jump from no firing to any firing. I'm also checking whether the eight size channels could be clipped to get a cleaner hole feature, but the sum across them only happens later in the fully connected layer.

I'm weighing whether the eight size channels in the second conv layer can be merged or clipped to get a bounded hole feature, since all sixteen channels are already in use and the sum over sizes only happens later in the fully connected layer. I'm considering a few options: dropping some orientation channels, merging size channels by summing corner cells across several positions in one kernel, or raising the gain so the hole measure is effectively binary, but each one loses boundedness in a different way.

I'm weighing whether to accept a linear feature on the unclipped hole measure, since the high-level firings already give strong evidence and a slope around 1.5 to 2 seems workable. The hole measure in the scaled logits gets distrusted by about 5×, but the measured hole log-likelihood ratios can be used at full scale as real log-odds.

Now I'm setting per-class baselines for the no-firing case, using the log-probability of "none" for each digit to anchor the linear model.

Now I'm turning the per-class upper-half densities into log-scale slopes against the hole measure, working through the L1 to L4 bins for each digit.

Now I'm working through the per-class log-density ratios against the level-1 baseline, comparing digits 8, 3, 4, 5, 2, 7, and 0 to 9 across the four hole levels.

Now I'm turning the per-class log-density ratios into slopes and intercepts against the hole measure, comparing the rates for 3 and 4 against 9 across the levels.

Now I'm turning the upper-layer log-densities into per-class intercepts, anchoring each digit at the no-firing baseline and at a midpoint around H=1, with 9 as the reference.

Now I'm converting the per-class upper-layer log-densities into slopes against the hole measure, using the value at H=1 minus each digit's no-firing baseline, with 9 as the reference.

I'm settling on per-class slopes for the upper hole feature, with 9 as the reference: 8 at roughly +3.1, 9 at +2.6, 3 and 4 near zero, 5 slightly negative, 2 and 0 around −1 to −1.5, 7 near −1.7, and 6 at −2.5. The linear fit gets shaky at small hole values, where the predicted gap between 9 and 3 comes out close to zero against a much larger true difference.

Now I'm checking the lower-layer density values for each digit, with 6 and 8 holding the highest densities and 9, 7 and 1 the lowest.

Now I'm computing the log-scale values for the lower-layer hole measure at H=1, averaging the L2 and L3 readings for each digit, with 6 and 8 coming out highest and 1 the lowest.

Now I'm finishing the lower-half slopes, shifting every value by 3.5 so the baselines line up: 6 comes out highest at +2.9, then 8 at +3.7 and 2 at +1.35, while 1 is capped at −3.

Now I'm setting the per-class bias terms from the no-firing rates, and weighting the combined classifier by γ = 0.7 with the hole slopes, where the earlier bias adjustments for 6, 8, 9, 2 and 5 are being replaced by these values.

Now I'm adjusting the bias terms: with the hole slopes weighted at 0.7, I'm checking how the 6, 8, and 9 predictions move, and whether the earlier +0.3 adjustment for class 2 still holds.

Next I'm setting the per-class slopes for the hole channels, applying the 0.7 weight and keeping the θ=1.5 detector config fixed so the stats still match. I'll check whether the sensitivity could improve later, using other sizes.

Now I'm setting the hole-direction weights for the lower side, with 6 and 8 getting the strongest positive slopes, and I'm keeping γ at 0.7 so the combined scores stay in range when both sides fire for 8.

Now I'm checking the 6-versus-5 gap once the hole terms are added: 6 gets about +1.4 and 5 about −0.2, so the two sit well apart. The lower-side weighting also gives 6 and 8 nearly the same boost, which means the naive Bayes term has to do the separating between them. I'm also settling on a small extra bias of +0.3 for class 2 and leaving the rest at zero.

I'm settling on a final calibration step, deciding to just set the remaining values and move forward.
