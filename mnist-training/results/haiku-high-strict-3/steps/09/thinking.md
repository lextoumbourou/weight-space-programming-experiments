The 13.6% result is worse: centering each class's 3x3 template to zero mean seems to have shrunk the discriminative part, so the bias terms now dominate the logits. Those bias differences are around 1, while the template contribution is only a few units at most, which would explain the odd spread in predictions.

I'm weighing whether to go back to the step 6 design, with 4x4 templates and per-cell mean removal, and tune the biases from its confusion matrix, since that gave a modest gain at a steady ~36%. The other option, a fundamentally different classifier, would need data, which isn't allowed. I suspect the real limit is in the conv features rather than the templates, since some channels may be nearly constant across digits.

I'm checking whether the uniform template really reduces to an ink-density map, which would cap accuracy near 50%. Grouped orientation features failed before, but step 8 was ungrouped with zero-sum templates, and its 13.6% suggests the zero-sum part may be matching background activity in empty regions.

I'm checking the class 1 template next, since its zero-sum centering may be why the predictions for 1 blow up: column totals for that class add up to roughly 2,900 predicted ones, far more than any other class.

The centre column is shared by almost every digit, so class 1's template ends up rewarding general centre ink rather than anything specific to a one. That makes the templates depend heavily on the bias terms, which I can't calibrate well without more information. With seven steps left and no clear fix, I'm starting to think the hand-coded approach has hit its ceiling.

I'm going to test whether biases alone can lift step 6 past 36%, using its confusion counts as the starting point. Its predictions are lopsided, with class 5 and class 3 over-chosen, class 6 never chosen, and only a handful of 7s.

I'm going to set the biases directly to spread the predictions out, since class 6 gets none at all and the 5s and 3s are over-chosen. The plan is to raise the biases for 6, 7, 9 and 8, and lower those for 5, 3, 2 and 4. The loss was already high at 3.7, so I'm wary that this will hurt calibration.

I'm going back to the step 6 setup, with 4x4 templates and per-cell mean removal, and reusing its confusion pattern to set new biases, since its template layout is the one I already settled on.

I'm working out the bias adjustments now, aiming to bring the predicted counts closer to 1,000 per class. The overpredicted 5s, 3s, 4s and 2s need their biases lowered, and the underpredicted 6s, 7s, 9s and 8s need them raised, scaled by the log of each count ratio. Class 0 comes out slightly high, so its shift is small.

I'm working through the bias corrections for each class, pulling down the overpredicted 2s through 5s and pushing up the underpredicted 7s, 8s and 9s. Class 6 gets the largest raise since it is never chosen at all, and class 0 barely moves.

I'm going to set the biases from the step 6 confusion counts, applying a log-ratio correction to each class. The biggest shifts go to 6 and 7, which are almost never chosen, and the largest cuts go to 5 and 3, which are chosen far too often. Since bias changes of that size could move a lot of predictions at once, I'm wary of overshooting.

I'm settling on a bias vector with a smaller class 6 push than before, keeping class 5 and 3 pulled down and class 6 capped near 1.8 so the shift doesn't overshoot.

I'm settling on the step 6 template layout, with 4x4 templates and per-cell centring, and tuning the biases with a log-ratio correction from its confusion counts, roughly b_d minus the log of predicted count over 1000, clamped to keep the shifts from overshooting. I expect this to move some mass from 2, 3 and 5 toward 6, 7, 8 and 9, though whether accuracy actually rises is uncertain.

I'm going to revert to the step 6 code and swap in a new bias array, derived by nudging each bias against the log of its predicted-count ratio. I'll check that the step 6 version really used 4x4 templates with mean removal before writing it out.
