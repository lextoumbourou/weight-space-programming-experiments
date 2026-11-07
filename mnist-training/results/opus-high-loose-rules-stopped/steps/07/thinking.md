I'm at 80.5% accuracy now, so I'm thinking about recalibrating the repeat bias with the new counts, maybe with a smaller step size of 0.7 to keep it from oscillating. I'm also looking at the remapped pairs, 3→5, 2→3, 7→9, 5→8 and 1→2, and their counts. On the loss side, a 0.91 loss at this accuracy looks high, which makes me suspect the logits are underconfident, and I'm considering raising alpha.

I'm working out the column sums for the confusion matrix at step 6, and they all come to 10000 in total. Since matching predicted counts to true counts isn't exactly the right objective, I'm planning to use per-class recall and precision instead, with the 0.7 step applied to the log of predicted over true.

I'm weighing whether the 3-vs-5 confusion comes from the synthetic models, maybe needing a tilted-stroke variant of 5 and a flatter top for 3, and I'm considering whether 2→3 has the same cause. I'm also thinking about reducing gamma to 0.3 to trust the synthetic covariance more, though that's risky, so if accuracy drops I'd revert it, even though combining it with the bias change makes the effect harder to attribute.

I'm going with the bias and alpha scaling together, which leaves the decisions alone, and adding gamma at 0.3 on top. Changing gamma also shifts the scale the optimal bias depends on, but I'll accept that.
