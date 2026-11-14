I'm decoding the index for sample 0 by adding the bit values: b1 comes out to 719, about 0.725 of the threshold, and I'm working on b2 next.

I'm checking the b2 and b3 sums for the remaining samples, where the totals and ratios for sample 1 through sample 7 are being computed.

I'm working through the rest of the sample tallies, checking the b1, b2 and b3 ratios for samples 8 and 9 and comparing the T_UD̄ values, where sample 7 stands out clearly against sample 9.

I'm converting the single-threshold line scalars into Gaussian estimates, with τ at 1.0 and σ at 0.45, and working out the μ values for samples 0 through 4.

I'm converting the "/" lower-left scalars into Gaussian estimates too, using τ at 1.0 and σ at 0.5, and I'm starting to build the classifier at step 20 with the loci table and the T_UD̄ row.

I'm continuing with the threshold parameters for each line type: the "\" centre statistics for channel 3, the "/" centre statistics for channel 1, and the H middle-left and "/" lower-left settings I'm keeping at σ 0.45 and 0.5.

I'm weighing whether the correlated line energies will overconfident the LDA, so I'm keeping the same 0.6 tempering and will check how it behaves once the classifier is built.
