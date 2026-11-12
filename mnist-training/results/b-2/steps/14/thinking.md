I'm noticing that a single vertical stroke to the right of center makes the open-left bay fire weakly for a 1 at both top and bottom. The likely reason is that the right wall is detected from the ink on the right side, while the top and bottom walls are missing, and the negative left wall gets penalized by the ink on the left.

Checking whether a single wall can outweigh the negative bias: a vertical stroke on the right gives the right wall about 0.45 from three rows, and about 0.9 if the stroke is thick, so one wall alone can beat the bias. These detectors are weak wall detectors. Measuring them one by one won't tell me much, so I'm looking at class-conditional means of the aggregated features in channel 7 instead.

I'm tallying the per-class sums for channel 7 across the remaining classes, splitting each into its top and bottom row groups.

I'm working through the per-bin scores for channel 7 across the classes, comparing the top-row groups for each digit.

I'm computing the bottom-row bin scores for the remaining digits, and they point toward using measured class means as linear weights. Rather than tuning each detector by hand, I'm considering restructuring the classifier around those per-class averages over a smaller set of aggregated features.

I'm weighing whether to measure more scalar features, roughly 15 steps for about 30 features, and then build a naive-Bayes or LDA-style classifier from the measured class means. The existing template classifier already gets about 70%, so the plan is to add those measured aggregates as extra weighted terms on top of the template logits, since the 64 orientation features may not capture everything the aggregates do.

I'm deciding how to handle the remaining structural channels: the ch4 and ch7 measurements can set linear fc weights directly, while the others would need either their own measurement pass or to be dropped.

I'm going to test the measured channel 4 and channel 7 weights directly in the classifier, setting the other structural channels aside for now, and compare the result against the current 0.703.

I'm estimating each class's mean feature value from the bin proportions, then turning those means into linear weights and biases using a shared within-class variance. For the bottom-row feature on channel 7, class 3 comes out high and class 6 low, so the weights would be large in magnitude.

I'm estimating each class's mean feature value for the hole channel from the top and bottom bin proportions, then moving on to compute the same for channel 7.

Computing the hole-channel means for each digit, and now starting on channel 7's open-left stats, with the class 0 and class 1 figures worked out.

I'm turning the class means for the hole and open-left channels into linear weights, assuming a shared within-class variance of about 0.15 for every class, and I'm about to set the bias term from those means.

I'm turning the measured hole and open-left means into per-class weights, shrinking them by half and using a within-class variance of about 0.15. Next I'll decide whether to keep the orientation templates for the remaining structural channels or drop them in favor of these linear terms.

I'm keeping the templates for channels 5, 6, 8 and 9 for now, and I'll measure those next. The biases stay as they were at step 11, scaled by temperature, with the LDA bias terms added on top.
