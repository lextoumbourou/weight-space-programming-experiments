Now I'm checking the confusion counts after the new 2 variant, with 7→2 at 204 and several other misclassification pairs listed. I'm also recomputing the column sums and comparing them against the true class totals as I refine the bias again.

Now I'm recomputing the bias updates from the new column sums, and the log ratios show 7 is under-predicted, with 7 recall only at 572 out of 1028. The 7→2 confusion at 204 looks like the curved-neck 2 variant pulling in 7s, so I'm considering whether a per-pair discriminative boost with controlled norm would handle that better than a global bias shift.

Next I'm weighing whether to change the scale too, since the loss is high at 0.91 for 73% accuracy, but I'll keep the scale fixed for now. I'm updating the biases and reworking the 2 template, because its sweep is the source of the 2→4 and 7→2 confusions. Shortening the sweep so it ends lower may keep it from looking like a 7.

I'm fixing the sweep geometry: the arc from angle -0.18 to about 1.45 should end near (9.3, 22.9), with the base running from (9, 23) to (21.5, 23). The bulge of that circle points toward the upper right, and I'm checking whether the neck of a real 2 curves the same way.

I'm rethinking the 6 template now, aiming for a straighter diagonal stem running from the top right down toward the lower left. I'm also weighing a 5 variant with a shorter, slanted top bar to pull some of the 5→6 confusions back apart.

I'm adjusting the 5 template with a shorter, slanted top bar and a bowl that ends less low-left, and I'm also going back over the 3 and 4→9 confusions. Then I'll apply the bias update with the 0.7 factor, starting from the current values.

Now I'm working out the bias updates for the remaining digits, starting with class 4, which is well over-predicted, and then 8, which is under-predicted relative to its true count.

I'm writing the bias update as two count arrays, with the 0.8 factor applied to each class's log ratio.
