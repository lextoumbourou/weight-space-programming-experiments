I'm at 71.2% accuracy with loss 0.85, and the measurement-driven approach looks like it's paying off, so I'll keep adding measured features. The biggest confusions are 4→9, 2→8, and 7→9. I also notice 8 is acting as a sink, with low rates across the board, so it may be functioning as an "absence" class that swallows anything with missing features.

I'm looking for features that would give 8 a positive signature, maybe a centre crossing, and I'm weighing whether line features need thresholds. For the main pairs, I want to measure the top-centre horizontal stroke to split 4 from 9, the upper-left vertical stroke to split 7 from 9, and the bottom horizontal and lower-left diagonal to separate 2 from 8 and 3.

I'm weighing whether the line-energy features can skip the clip, since the two-sided ones have small values and might not need it, which would free up a couple of channels. The one-sided features still seem to need it, and I'm questioning whether I ever validated the clip design at all.

I'm weighing whether a Gaussian naive Bayes treatment of the continuous line energies would be worth the probe steps. Each region needs class means and a shared variance, which a histogram probe could estimate, so that's roughly one to two scalars per step. Against that, the binary loci features give three clean channels per step, so I'm trying to decide which use of the remaining steps pays off more.

I'm considering whether the two-sided line features can drop the clip, which would free up channels, and I'm wondering whether the clip design was ever validated. The next question is whether a test without clipping, with the weights rescaled to the typical region magnitude, would show whether clipping helps at all.

I'm now checking whether the loci features need the clip at all: the one-sided ones already stay within a bounded range, so dropping it could free six channels for new features, though the cost to calibration is unclear.

I'm checking whether a saturating wall response could keep the range bounded, since a full straight wall only spans about a factor of two, which would leave the unclipped features in a workable range.

I'm weighing whether to drop the clip on the six loci channels, since the one-sided features only span about a factor of three when present. The idea is to rescale the weights by typical region magnitude and compare the loss to 0.8496, which would free six channels if nothing is lost.

I'm thinking about what the final architecture should look like and how to allocate the channels. The line grid would stay at four channels, possibly with measured region energies, the loci features take six or twelve, and unclipping could free room for up to six new detectors aimed at 8, 4/9, 7/9, 2/3/8, and 5/3/6. Loop-style detectors look weak so far, since the 8 and 9 loop features fire only occasionally.

I'm considering a conv1-level hole detector: a 5x5 filter with an empty centre and a ring of ink at radius two, which would catch small loops in 8, 9 and 6. Larger holes would still fall to the LR/UD features at conv2 scale. That would take one of the eight conv1 channels, which is the trade-off I'm weighing.

I'm weighing whether the two diagonal line channels could be traded for conv1 features instead, since the edge maps might carry enough of the stroke information for the templates. A small-hole detector at the pixel scale could catch tiny loops in 8, 9 and 6, but the open question is which existing channel it would replace.

I'm weighing whether to spend the remaining steps on more measured binary detectors, since the measured Naive Bayes approach is what's actually improving accuracy. Line-type detectors could be made binary with conv2 thresholds, and I'm considering whether the cosine line templates still earn their channels compared with other uses.

I'm planning to pick the most useful of the remaining probe steps, since each candidate feature needs measured presence rates, about three per step, and 39 steps is a limited budget. The next candidates are longer bar-like detectors: a long horizontal stroke for 7, 5, 2 and 4, a long vertical stroke for 1, 4 and 9, and long diagonals in both directions for 7, 2, 1 and 8, plus region positions. Since the channel count is capped at about 16, I'll need to be selective, and I'm guessing somewhere around a dozen measured features might be the right size.

I'm going to keep the clip question open for now: unclipping would free six channels, and I can check the calibration cost when the new detectors are measured. Since the final layer is linear in cells, per-cell rates could be worth refining for the strongest features too.

I'm weighing whether to drop the clip for a no-clip test now, since a single step would show whether the calibration cost is small enough to justify freeing channels for new detectors. If it is worse I couldn't tell which change caused it, but the test is cheap and might even become the best model.

I'm setting up a no-clip test for the classifier, scaling the unclipped weights by a typical region-sum magnitude of about one, since the measured probe sums for the one-sided features sit mostly between 0.15 and 1.0.

I'm setting the unclipped weights for six loci channels, each scaled by its typical region magnitude (about 1.0 for the one-sided features and 0.6 for the two-sided ones), and zeroing the remaining channels.
