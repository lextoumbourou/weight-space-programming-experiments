I need the loss to drop below 0.992 by step 9, or the run gets stopped. Raising the temperature to 0.85 barely moved it, going from 1.0103 to 1.0112 with the biases, so that idea isn't doing much. Accuracy is 69.5% with loss near 1.0, which seems typical for a model that is already reasonably calibrated, so it's hard to tell whether it's underconfident. I still need a reliable gain of at least 1%, so I'm looking for an option with a solid expected payoff.

The biggest confusions are 2→3 and 7→2, with 8→2 and 4→9 close behind. Since temperature barely changes the loss, the loss is being driven by accuracy, and I'd need to get accuracy up to around 72%. Some 0s are being read as 2s, which may be a tilt issue, so I'm checking whether the 2 template's diagonal is too long compared with real 2s.

I'm weighing whether the 2 template's long diagonal is what pulls real 2s toward 3, since a 3's lower arc sits in roughly the same region. Without data to test against, hand-tuning these features is guesswork, so I'm considering a different structural cue instead.

I'm weighing whether to scale the A and B feature groups differently, since the B features dominate the Gaussian weights and are coarser. That could help, but it risks over-penalizing inky digits, so I'm considering a separate scale for each group with the bias computed from its true magnitude.

I'm considering splitting the variance between the two feature groups: the A features have roughly half the scale of the B features, so their variance should be about a quarter of B's. That suggests weighting A more heavily, but scaling the variance up that much would make the overall logits much larger, so I'm wondering whether that would make the classifier overconfident.

I'm going with a principled variance split: the A features have about half the scale of B, so their variance should be smaller, and I'd rather keep the overall logits from getting too sharp. Setting the group variances to 0.1 for A and 0.4 for B, the bias terms stay as they are since the accumulated corrections already account for the mean shifts.
