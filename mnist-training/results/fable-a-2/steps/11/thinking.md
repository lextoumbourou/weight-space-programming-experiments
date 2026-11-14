I'm decoding the bottom-centre bits, checking sample 0 by summing the relevant positions for each of the three bits, and then moving on to sample 1.

Now I'm working through the remaining samples' bottom-centre sums for each bit, and the numbers in sample 2 through 8 give the fraction estimates for b1, b2 and b3.

Now I'm writing out the sample-9 bottom-centre sums for each bit, then moving on to the feature tables for the top-region presence probabilities.

Now I'm filling in the bottom-region probability tables, listing each feature's presence estimate for bit b1 and b2 across the ten samples.

Now I'm compiling the bottom-region presence rates for the remaining features, then working out a naive Bayes classifier from those probabilities.

I'm weighing how to turn the per-region presence estimates into network weights, and whether to clip each cell's activation so a present feature saturates instead of scaling with its strength.

I'm weighing whether to clip each cell's activation so a present feature saturates, since a linear weight on region sums would overcount strong presences. Clipping at about 0.5 makes the region sums roughly binary, though I'd lose the finer staggered templates from the second grid, and I don't yet know how much that grid contributes.

I'm weighing whether the unclipped region sums are too strong a signal, since a digit with a long clean stroke could push the naive Bayes weights too far. I'm leaning toward a linear weighting to start, with a global scale on the classifier part that I can tune by trial.

Now I'm settling on a scale factor for the naive Bayes part and working out typical signal strengths for each feature, roughly 0.8 for the one-sided ones and 0.5 for the LR and UD features, to set the network weights.

I'm weighing whether the per-cell saturation trick is worth it, since it would cap strong presences but cost me the second grid's line channels. Scaling the weights by typical signal strength with a global factor may be simpler, so I'll consider that first.

I'm considering whether clipping each cell at a low value, around 0.3, would make each firing cell contribute a roughly fixed amount, so a region's presence becomes a count of firing cells rather than a raw strength.

I'm considering a per-cell clip at 0.4 with two channels per feature, one for the raw response and one for the response minus the clip, so each firing cell contributes a bounded amount.

I'm clipping each cell's response at about 0.4, so a firing cell saturates and the region sum becomes a rough count of firing cells. Since typical present values run about 1.5 cells, I'm planning to divide the count by that to get a presence-like weight for the naive Bayes part.

I'm weighing a per-cell clip against the idea of mapping every region to a single cell, but the max-pool makes each final cell cover a 4x4 pixel area rather than an 8x8 region, so I can't take a max across the four cells directly. A finer per-cell presence measurement would cost far too many probes to be worth it, so I'll accept the remaining mismatch between the region count and true presence.

I'm settling on a clip of about 0.4 per cell, so a firing cell saturates and each region's sum roughly counts how many cells fire, then dividing by an expected count of about 1.6 to get a presence-like weight. For the lines part I'm restricting the cosine templates to grid A, keeping the scale at 4, and I'll check later whether grid B's line energy needs adding to the naive Bayes side. The older loci templates still need to be dealt with afterwards.

Now I'm writing the weight computation: for each feature, the log-odds per class get centred and scaled by the temper factor and the clip-and-count normaliser, then applied to the grid-A and grid-B channels with opposite signs, with a matching bias from the log(1−P) terms.

Now I'm checking how the probability clipping affects the log-odds, and that a 0.995 estimate gets capped at 0.99 so the extreme values don't dominate.

Next I'm restructuring the helpers so they write into a temporary kernel array, with one channel for the raw response and one for the response minus the clip, per feature.

Still writing the feature probability table...

Still writing the probability table...

Still writing the weight code...
