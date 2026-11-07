Digit recognition is improving, but the 4 class is still the weakest, getting confused with 9, 1 and 6. The 4 template itself may be off, since real 4s vary between open and closed tops and many look like 9s at this resolution. I'm now thinking about what actually separates a 4, mainly a horizontal bar around the middle row extending to the left.

I'm weighing whether the 4 template is the real problem, since the crossbar sits low in the digit and the left stroke has to be told apart from a closed 9 top. I'm also wondering if the isotropic Gaussian is just too blunt, and whether the evidence for a missing stroke should be weighted differently than the evidence for a present one.

I'm weighing whether the centre-tap features are too broad, since they take a max over any stroke nearby at a given orientation, and I'm considering reweighting the feature groups or dropping one to see which helps. I'm also thinking about using the unused channels for new cues like endpoints or enclosed holes, though with only the confusion matrix to go on, that's hard to judge.

I'm checking whether the Gaussian scoring actually penalises a missing stroke, and it turns out the expansion cancels the shared ||f||² term, so absence in the template doesn't count against a class. That looks like the core weakness behind the 4 confusions, so I'm planning targeted template edits for 4.

I'm now checking whether the Gaussian's relative scoring is really the problem: extra ink in a class doesn't count against it, so the reward other classes get for the same stroke matters more than the absence itself. The main suspicion is that the templates are too sharp, and that the real feature magnitudes, especially for the A features, are much smaller than I assumed, which would make the bias terms wrong for inky digits.

I'm sizing the response of the A features more carefully, since a stroke sitting one pixel off the centreline drops the kernel output a lot. That could mean the A group's magnitude is over-estimated, which would skew the bias terms for inky digits.

Working through the pooling step now: the stroke's response falls off quickly when it sits a pixel off the kernel's centre, so along a stroke I'd expect one pooled cell near 0.85 with its neighbour around 0.165, unless the stroke lands right on a pooling boundary.

Checking the stroke-response numbers, the spacing works out: about 0.34 pooled, close to the 0.35 I assumed, so the magnitude calibration looks fine. The weak point is probably the template geometry instead. I'm picturing the MNIST mean 4 with its left stroke near x≈9-10, a crossbar around row 16, and the right stem near x≈16-17, and I want to compare that against how a 9's loop sits at the top.

I'm comparing the 9 and 4 templates directly: both have a left-side stroke around the middle rows and similar stems on the right. The separating cues would be the closed top arc of a 9 versus the open top of a 4, and whether the crossbar pokes out to the right of the stem.

I'm nudging the 4's crossbar down to around row 16.5 and stretching it out to x≈22, and shrinking the 9's loop higher up, so the two templates stop overlapping at the middle rows. I'm also noting that the 4→1 mix-ups likely come from thin 4s, with the 1 template being slanted.

Now I'm tallying the column sums of the confusion matrix to compute the bias corrections, adding up each predicted class across its rows.

Now I'm working out the bias corrections from the column sums of the confusion matrix, since class 4 is still badly under-predicted at 307 even after the earlier +0.8 bias, so it needs a bigger boost or a template fix.

Now I'm working out the bias corrections from the per-class column sums, giving each class a small step toward its true count. Class 4 is badly under-predicted at 307, so it gets the largest boost, around +0.70, while classes 1 and 0 get pulled down a bit.

I'm going to shift the 4's crossbar down to about row 16.5 and stretch it out to the right, then move the left stroke and stem to match. I'll also tighten up the 9 so the two templates stop overlapping, and I'll reapply the bias corrections afterward since the template changes will shift them.
