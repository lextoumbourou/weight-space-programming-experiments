I'm noticing the digit confusions are systematic rather than random: 1 is absorbing and several pairs (0→6, 1→7, 7→9) keep recurring. I'm wondering whether a misalignment or flip is involved, and suspecting 0 gets matched to 6 because the 6 template is more tolerant of the stroke pattern.

I'm wondering whether my x feature is really measuring what I intended, or whether the pooling or a row/column mapping mix-up is shifting things. Transposition seems unlikely, since 1s are classified correctly 82% of the time. I'm also puzzled why the 1 template wins so often: its center-column penalty should be too small to explain it, so the max-pooled blur and stroke magnitudes may be the culprit.

I'm estimating per-class bias offsets from the column sums of the confusion matrix, since class 1 is being predicted far more often than its true count. Some other columns like 6 and 9 are also over-predicted, so I'd need to adjust several biases together rather than just one.

I'm settling on bias offsets: pulling class 1 down the most since it's over-predicted by a wide margin, trimming 6 and 9 a little, and nudging classes 0, 2, 4 and 5 up because they're under-predicted. I'm wary that these corrections are crude and could overshoot, and I'm still stuck on why 0 keeps getting matched to 6 even with the negative hole weights.

Next I'm weighing whether to lower the bias for class 6 as well, since it may be stealing the wins that should go to 0. Rather than trusting the crude bias offsets, I'm thinking about whether a looser alignment, through a wider blob sigma, would help the templates tolerate misplacement. I'm also still uncertain whether the stroke-type channels should be used at all, and I want to see how the biased scores look before deciding.

I'm checking the scores for class 1 against the others: on a 1 the margin is large, but on other digits class 1 still scores around 2.2, so a bias of about -1.5 looks reasonable rather than the -2 I had in mind.
