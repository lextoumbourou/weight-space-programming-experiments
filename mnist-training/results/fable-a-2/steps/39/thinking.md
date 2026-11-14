I'm checking the bit-decoding thresholds for the first sample, comparing the weighted sums against 0.6 to see which bits come out set.

Now I'm working through the remaining samples, checking each weighted sum against the 0.6 threshold to see which bits come out set.

Now I'm checking the weighted sums for the remaining samples against the 0.6 threshold, and so far the bit-three comparison for sample 8 comes out low while sample 9 is borderline.

Now I'm checking the remaining per-sample scores for the first bit and the second and third bits against 0.6, and the numbers show sample 7 and sample 9 are the close calls for bit three.

Now I'm working out the mean values for each sample's bit-three and bit-one scores, comparing them against the threshold to see which samples sit near the cutoff.

Now I'm working out the per-sample means for the bit-three and bit-one scores, checking which ones sit near the cutoff, and I'm matching the overlapping cells of the classifier grid against their neighbors as I go.

I'm setting the classifier's mid-row threshold and scale adjustments, then weighing whether to spend another probe cycle before the final tuning steps.
