Checking the column sums next: digit 6 is over-represented at 1177 against an expected 967, and digit 4 is under at 807 against 983. Most of the surplus flowing into 6 comes from 4, with 5, 8 and 2 contributing smaller amounts.

I'm weighing a shift from the 8-channel orientation encoding to an absence-coded 5x5 box that uses only 4 channels, which would free up room. The catch is that the summed 16-cell pooling behaves differently from the max over 9-cell sums, so the threshold C would probably need recalibrating, though a single test run should show whether it holds. If it does, the freed channels could go to quadrant-level corner features or big-window versions of the line features.

I'm suspecting the 4→6 confusion comes from the zone split at row 13.5, which may cut through 4's bar-junction corners. With only two row-zones, a 4 that lacks the lower-right stroke looks like a 6, so I'd want at least 3 or 4 row-zones to resolve position better.

Next I'm considering measuring row-level corner features instead of only the current zone-level ones, since 16 features would take six steps and the split might resolve the 4-versus-6 confusion, though I'd first want to see whether the outer rows alone give enough information.

I'm weighing whether to measure all 16 row-level features directly, which would take about six steps, to get finer vertical position than the two zones give. Measuring orientation by row and column is another option, though the cell-level joint probably matters there, so I'm not sure the marginals would hold up.

Now I'm looking at which confusions dominate the error count, with 4→6 at 113 and 2→8 at 101 leading, and a total of 1742 errors across the pairs listed. I'm considering a more data-driven route: measuring a moderate set of around 30 strong binary features directly, each with its class-conditional rate, and then combining them in a naive Bayes model.

I'm considering measuring about 20 more semantically chosen binary features over roughly seven steps, such as clipped hole features and corner types restricted to specific rows, aimed at the 4/6/9/8 confusions.

I'm sketching quadrant-level orientation features next, such as a vertical stroke in the left-top or right-bottom quadrant, or a horizontal stroke in the top or middle rows, aimed at separating the 4, 9, 7 and 6 cases. The open question is that summing a quadrant's overlapping cells gives counts from 0 to 4 rather than clean binary presence.

I'm weighing a 64-feature measurement, one binary cell per orientation and position, which would take about 22 steps. A cheaper option is to restrict the orientation grid to a subset of cells, perhaps only the ones in columns 0 and 2.

I'm weighing a budget of about 32 steps: roughly 8 for final tuning and about 24 for measuring and integrating features. That could cover around 60 binary features, close to the full 64 cell-level orientation set. I'd expect cell-level orientation features with naive Bayes to reach somewhere around 85 to 90 percent, which beats the roughly 75 to 78 percent from the hand templates. The alternative is 16 corner-row features plus about 44 others.

I'm weighing whether measuring 16 row and column marginals to recalibrate the hand templates would beat a full 64-cell measurement, since iterative proportional fitting could rescale the templates to match them. The open question is how cell presence relates to the row-level OR, which the rescaling would depend on.

I'm weighing measuring all 64 cell-level orientation features directly, which would take about 22 steps and leave roughly 10 for integration and tuning. Cell-level features would remain hand-set, but the orientation side would be fully measured.

I'm now weighing a coarser orientation grid: dropping some of the 16 overlapping cells, since adjacent ones are highly correlated. A non-overlapping quadrant subset would miss the bottom rows where the base of a 2 sits, so I'm checking whether a subset that covers the lower rows would work instead.

I'm considering measuring the orientation features directly, either all 64 cell-level ones or a subset, and keeping the current 8-channel encoding so the templates don't need recalibrating.

I'm weighing whether to lean on measured vertical and horizontal orientation features across all 16 cells, which would cost about 11 steps, and keep the diagonal orientations on the hand templates. The reasoning is that horizontal and vertical strokes are the most reliable and semantic, so measuring them first seems worthwhile.

I'm weighing a gain of maybe 3 to 5 percent from measuring the orientation cells, against a cheaper row-level corner measurement that might add only 1 to 2 percent. To tell 4 from 6, the key cues look like a right-side stroke running into the lower part for the 4, and a bottom loop with a horizontal base for the 6, plus the lower hole being much more common in 6.

I'm thinking about whether measuring orientation features at the row or quadrant level, just for horizontal and vertical strokes, would work better than counting overlapping cells. The 4 and 6 distinction depends on where the stem and the bottom base sit, and my hand template for the 4 may not capture that well.

I'm weighing whether to measure only the horizontal and vertical orientation cells, since adjacent overlapping cells are highly correlated and a partial set might cover most of the signal at a lower step cost.

I'm thinking of measuring only a checkerboard half of the orientation cells, 32 features in about 11 steps, since the overlapping windows still cover the whole area. That would leave the classifier with the measured set alone and free up more steps.

I'm checking which subset of the 16 overlapping orientation cells would still cover the bottom rows, where the base of a 2 sits, without leaving the middle uncovered.

I'm picking a 3x3 subset of the overlapping orientation windows, weighing which rows and columns to keep so the top, middle and bottom bands are all covered. The middle band is the open choice, since it has to span the waist of the digits without leaving the bottom strokes uncovered.

I'm settling on a checkerboard subset of the orientation cells: four rows of cells with alternating columns, which comes to 32 features and about 11 steps. That keeps vertical coverage across the whole digit while halving the measurement cost.

Planning the orientation measurement as a checkerboard of 32 features, about 11 steps, with H and V first and the diagonals after. That would leave step 30 for integration and roughly 20 steps for tuning and extra corner or hole measurements.

I'm settling on a concrete measurement plan for the orientation features and weighing whether the binarization threshold will hold up. The open question is whether the soft clipped value should be kept for the classifier or reduced to a binary feature.

I'm wondering whether to switch the orientation encoding to absence coding first, which would free four channels, but the current feature is known to work, so I'm leaning toward keeping it. I'd only want those extra channels if there's a clear use for them, like a hole clip at another size or corner features at a different scale.

Now I'm working out the measurement encoding for the orientation features, deciding how each cell's stroke signal maps onto the classifier weights. Then I'm listing the order to measure the cells, starting with the horizontal orientation across the even-sum grid positions.

I'm settling on which 8 cells to measure per orientation, sticking with the checkerboard pattern. Then I'll lay out the first measurement steps: the horizontal cells first, starting at step 19. I'm also weighing whether these 11 steps are better spent on orientation cells or on the corner features at row level, which would cost only about 6 steps.

I'm settling on a generic diagnostic builder that takes a list of orientation, row and column triples, and I'll reuse the step 18 convolution code so the features match what the classifier sees later.
