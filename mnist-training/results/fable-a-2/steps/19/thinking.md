I'm decoding the indices by computing idx = 3·b1 + b2, with the "\" centre checked against thresholds 0.5 and 1.4 and the "/" centre checked separately. For the first sample, the "\" probabilities come out to about 0.904 above 0.5 and 0.044 above 1.4, and the "/" sum works out to roughly 0.97.

Now I'm working through the remaining samples, checking the "\" and "/" probabilities for each index.

I'm checking the remaining samples against the "\" thresholds, where sample 8 sits clearly above 1.4 and sample 7 is the lowest, and noting that the "/" thresholds are too low to separate anything.

I'm fitting Gaussians to the "\" centre for each index, using the z-scores from the two thresholds to get a σ and μ per sample. Most of the fits come out with σ around 0.3 to 0.6, and the means sit between about 0.5 and 1.9, with sample 8 lacking a μ.

I'm fitting the "/" centre with the same approach, using the two thresholds to pull out z-scores and a σ and μ for each sample. The first fits come out with σ around 0.6 and 1.0, and the means are roughly 1.65 for sample 0.

I'm fitting the "/" centre with the upper threshold sitting in the low tail, so the σ and μ values for samples 2 through 9 are poorly pinned down. Sample 5 gives a weak estimate of about 1.47, and I'm still working through the rest.

I'm fitting the remaining "/" centre values, and the means land roughly between 1.5 and 2.8 with a broad σ of about 0.8, so they're a weak signal. Samples 7 and 9 are still hard to tell apart, and I'm checking which measure separates them.

I'm now testing the "\" centre against the 7-versus-9 pair, where 9 sits around 1.39 and 7 around 1.03, and the difference is only about 1.1 standard deviations. The top-left vertical feature looks more useful, and I'm also comparing the top-row and bottom-row loci, which separate the two digits a little better. The remaining misclassifications might come from template bias, so I'm looking at more candidate regions like the middle-left horizontal energy and the open-top pattern.

I'm checking whether a "T_UD̄" feature, an open space below a top bar with a ceiling above, separates 7 from 9, since 7 should fire strongly there and 9 should be blocked by its loop. I'm planning a next probe of three binary loci features, with the T_UD̄ region at the top of the digit.

I'm now weighing a few remaining options for the 2→3 and 5→3 confusions, including lower-left and outer-column loci. The 8-sink errors look like they should respond to the "\" centre evidence I already have, which runs high for 8.

I'm setting up a third probe with three binary loci features, starting with the open-below-a-top-bar region at the top of the digit. For the outer-column options, I'm weighing whether a wall on the right at the left edge would separate the wider digits.

I'm weighing whether the outer-column features are worth including, since they would fire for nearly every digit and tell me little. The middle-band loci regions look more promising, particularly for separating 4 and 9, though they overlap with the top and bottom bands I've already measured.

I'm weighing whether to use the last two slots on line-based binary presence features, where a single threshold on each region's summed response would stand in for the two-threshold fits. Since the per-region spread has been around 0.4 to 0.55, I could assume that σ and derive each mean from the threshold, though I'd need to pick the threshold without knowing the between-class range, which risks saturating everything near 1 the way the "/" centre did.

I'm weighing a probe for the T_UD̄ region alongside two line-based scalars, one in the lower-left "/" area and one in the middle-left horizontal band, each with a single threshold.

I'm choosing two more features to pair with the top-row loci test: one for the lower-left diagonal and one for the middle-left horizontal band. I'm also setting up a binary encoding where each feature gets its own threshold, so the index comes from three yes/no checks.

I'm setting the three binary features' thresholds: the top-centre region at 0.15, the lower-left "/" region at 1.0, and the middle-left horizontal band at 1.0.
