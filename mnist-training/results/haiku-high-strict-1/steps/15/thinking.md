I'm at step 14 with 51.53% accuracy, and step 15 is the last one, the one whose network gets scored on test. So I want a conservative calibration from here that doesn't risk regressing. I'm starting to tabulate the row counts now.

Now I'm tallying the rest of the rows and column sums to get the totals for the calibration.

I'm checking the column totals against the row sums, and everything reconciles to 10000. The per-row differences show column 2 running about 105 low and column 0 about 90 high, so those are the places to look.

I'm seeing that the column counts are badly off from the row sums: column 4 is far too high and columns 8 and 9 are far too low. My guess is the bias adjustments for 8 and 9 pushed mass toward column 4 and 6, so the 0.4 and 0.7 values need rechecking.

Looking at how row 4's count jumped to 1863 from 679 after that one bias change, the shifts are clearly non-linear, so I'm going to aim for a smaller correction. I'm considering nudging row 4 back down, pulling 6 from 0.7 toward 0.5, raising 8 and 9 to about 0.55, and trimming 0 slightly, all while keeping step 14's weights as the base.

The steepness here is striking: a 0.1 bias change moves roughly a thousand predictions for class 4, and a 0.15 change moves class 8 and 9 by over a thousand each. That suggests the logit margins are very narrow, so each class's win region is a thin band and the count-to-bias mapping swings wildly in both directions. Fine-tuning like this is close to chaotic, and I'll need to treat the bias for each class as controlling its share in a sharp, non-linear way.

I'm weighing whether to submit step 14's exact configuration, since it's the known best at 51.5%, or to make a small tweak. Given how sharply the class counts respond to tiny bias changes, any perturbation carries real variance, and I'm leaning toward keeping it close to step 14.

I'm comparing the bias settings from the previous two steps, checking what I submitted for step 13 against the step 14 values, which I'm still recalling.

I'm weighing whether to resubmit the step 14 biases exactly or tweak them, since the step 13 values pull class 4 too low while pushing 8 and 9 too high.

I'm estimating the bias for class 8 by interpolating between the step 13 and step 14 values, which lands near 0.5, and I'm starting to work out a similar estimate for class 9.

I'm working out each class's bias by interpolating between the step 13 and step 14 values. That puts class 6 near 0.6, class 0 near 0.65, and classes 8 and 9 around 0.5, and I'm still estimating where class 4 should land.

I'm settling the bias for class 4 at about −0.02, since the linear interpolation between the step 13 and step 14 values points there. Class 7 comes out near −0.02 by the same method.

I'm checking the step 13 and 14 values for classes 2, 3, 5 and 1, and settling class 2 at about −0.28 since that's where its count lands. I'm keeping 3 and 5 where they are and leaving 1 at 0.

I'm weighing whether interpolated biases can hold the balance, since the step 13 and 14 interactions aren't linear. Balancing the class counts should help accuracy if the miscalibration is the main issue, but the steep sensitivity means the result could easily land below 51.5%.

I'm weighing whether to submit the interpolated biases or resubmit step 14 exactly. Step 14 is the known 51.5%, while the interpolation is an informed guess that might balance the class counts but could also swing below that, given how steep the sensitivity has been. I'm leaning toward the interpolation because counts have been the main problem, though I'm treating its benefit as uncertain.

I'm comparing the class-wise accuracies now, with class 1 near 83%, class 0 around 75%, class 2 at 62%, class 3 at 41%, and class 4 about 73%, and class 5 still being worked out.

I'm comparing the class accuracies, and classes 8 and 9 are almost at zero in step 14. In step 13, class 9 did much better at its higher bias, so I'll try a bias of about 0.5 for it.

Nine's bias around 0.5 should bring back a good share of its correct predictions, roughly 400 more than step 14. Dropping class 6 to about 0.6 costs something, maybe 100 to 150 correct, and class 4 may still have room to move.

I'm estimating each class's expected correct count at the interpolated biases, and the trade-offs look mixed: class 4 and class 6 would lose roughly 200 and 140 correct predictions, while class 9 could gain around 400 and class 8 a modest amount.

Keeping class 4 at +0.05 and class 6 at 0.7 looks safer, since interpolating them lost more correct predictions than it gained. Raising class 9 and class 8 to about 0.5 should recover a good share of their correct hits, even if class 9 pulls some predictions away from 4 and 6.

I'm weighing whether to keep class 4 at +0.05 and accept its many overpredictions, since lowering it to 0.0 would likely cost a lot of correct hits. Most of its wrong predictions come from classes 9, 6, 8, 2, and 3, so raising 9 may pull some of those back.

I'm settling on keeping step 14's biases for everything except classes 8 and 9, which I'll raise to 0.5. Raising 9 should pull back the many correct hits it lost at 0.4, and it may also draw some of the predictions currently piled onto class 4.

I'm settling on a bias vector that keeps step 14 for most classes and raises classes 8 and 9 to 0.5, since their near-zero accuracy at 0.4 is the clearest gap. Raising 9 should pull some of the predictions currently piled onto class 4 back to their own class, and I'm wondering whether 8's increase risks the same kind of swing I've seen before.

I'm settling on the final bias vector: keeping step 14's values for most classes and nudging 8 and 9 up to 0.5, since their predictions are sparse and 9's correct rate collapsed at 0.4.

I'm keeping step 14's biases for everything except classes 8 and 9, which I'll raise to 0.5, since they're now underpredicted and the wrong predictions piled onto class 4 should shift back toward them. The rest stays put, because the bias-to-count relationship is steep and bigger changes could erase step 14's gains.
