The flat run stalled at about 81% accuracy, so turning the knobs by hand has stopped paying off. Better results would need either more information about template fidelity or new features. I'm weighing whether to add systematic measurement, given that I have 38 steps left and the feedback after each step is the only signal I get.

I'm weighing whether measuring feedback counts as training. The rules ban gradient descent and optimisers, and I'm not running either, since I only set the weights myself. Still, adjusting weights from feedback looks close to the line, so I'm checking the rules before going further.

I'm weighing a measurement plan that stays under about 12 steps, since computing the full set of features would cost far too many. Rather than fitting every weight, I'm considering aggregated statistics along rows or columns to calibrate the hand templates, though that alone wouldn't pin down cell-level errors. I'm also wondering whether new semantic features would be more decisive than calibration.

I'm looking at which crossing counts along the center line and at the upper and lower thirds might separate the digits, since those counts are robust to stroke thickness and map onto orientation information I already have.

I'm still weighing whether a discriminatively trained linear layer on the existing features would be the real fix, since the bottleneck looks like the weights rather than the features. Hand-setting them is hard, so I'm estimating class-conditional marginals instead, which I expect to land somewhere around 88-90%. Measuring marginals costs about three binary features per step, so I'm asking whether the readouts could carry more information per step.

I'm now weighing whether a grouped count readout could beat three separate marginals per step. Summing nine features into one quantity only gives me the average of their probabilities for each class, one number per class, which is less information than the three direct marginals I already get.

I'm weighing whether to measure zone-level corner features directly, since I can't inspect the template values here and have to reason about them approximately. Grouping the corner features into upper and lower halves for each of the four corners would take about three steps.

I'm considering whether zone-level corner statistics, measured as thresholded sums over upper and lower halves of each corner region, could calibrate the hand templates more cheaply than fitting every cell. Around 16 zone features would take roughly six steps, though I can't inspect the template values directly, so I'd be reasoning about them approximately.

I'm now considering zone-level corner statistics against the confusion pairs, and whether a different readout based on the confusion matrix could do better than either.

I'm considering whether to measure zone-level corner statistics instead, grouping the corner features into quadrants, which would be 16 binary features and roughly six steps.

I'm sizing up a quadrant-level version of the corner features: sixteen binary features over four corners and four quadrants, which would take about six steps. The idea is to replace the cell-level corner weights with measured quadrant statistics, and I'd expect a modest gain of a few points on top of the corner gain I already have.

I'm considering whether zone-level corner statistics would be worth measuring at all, since a single feature's usefulness depends on how far its rates spread across the classes. I'm also wondering whether measuring how well each class's hand template matches the data would be a more useful use of a step than any of the feature readouts.

I'm sizing up the 16 corner-quadrant features as a measured calibration, which would take about six steps. My sense is that this is the surest route, though I'm not certain the quadrant granularity will hold up for digits like 9 and 6, whose loop corners sit near the boundary between upper and lower halves.

I'm checking where the corner features fall relative to the horizontal split: the top-left of 5 and the top-right of 3 land near the boundary, while 7's top-right and 3's lower-bowl corners sit clearly on the right side.

I'm weighing whether to split the corner zones by column as well as by row. Most corners sit near the center column, so a left/center/right split would need 24 features and about eight steps, while a plain upper/lower split would need only 8 features and three steps, with the existing cell-level templates kept at low weight for finer position.

I'm settling on measured zone-level corner features as the calibration, grouping them by corner type and by upper versus lower half so that about eight features fit into three steps. The cell-level hand templates would stay in at a lower weight for finer position, and I still need to decide how to threshold each zone sum.

I'm settling on a binary threshold for each zone feature, with present meaning the zone sum is above 0.1. For the joint readout I'll encode the three bits as an index from 0 to 7, and I'll take the class weights from the measured frequencies.

I'm laying out the rule for the joint readout: each outcome from 0 to 7 is a sign pattern over the three bits, and argmax picks the pattern that fits. Classes 8 and 9 get a large negative bias so they never win. Next I'm splitting the corner zones into upper and lower halves, which gives eight features to measure over three steps.

Writing the probe code now: the convolution layers stay as in step 12, with the hole channels kept but unused, and the readout weights for each of the eight outcomes set to ±K across the matching corner channel's zone rows.
