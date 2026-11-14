The model now sits at 91.33% with a loss of 0.2875, a slight gain. Eight got worse, with most of its misclassifications going to 5, and 9 slipped as well, while 3, 4 and 5 improved. Column sums are now tallied up across all eight classes.

I'm working through the per-class totals and the over- and under-predicted digits. Classes 5, 3, and 2 run high, while 9, 0, 6, and 8 run low. I'm suspecting the imbalance comes from classes that pick up many "end" detections, and I'm planning bias corrections to offset it. With about 12 steps left, I expect tuning to add only a small gain.

I'm checking the remaining "none" terms for the 8 and 5 cases, and the combined advantage to 8 comes out around 1.3 nats, which seems fine. Since the 8→5 errors are probably inherent to open-topped 8s, I'm concluding this approach has topped out near 91.5–92%. For the last steps I'll focus on calibration: biases, a global temperature, and group scales, adjusting one group at a time and watching the loss.

I'm weighing whether to try a global temperature adjustment first, since the loss could move noticeably if the model is over- or under-confident, and one test step should show the direction. Group-scale tuning looks like it might add a few tenths of a percent in accuracy. I'm also considering pairwise bias-style corrections for the remaining steps.

I'm going to split the tuning into two separate steps so I can tell their effects apart: first a bias-only re-tune at step 39, then a temperature change of about 1.2 at step 40. Temperature scaling means multiplying the final weights and biases by the same factor, which should leave the argmax unchanged while reshaping confidence.

I'm weighing a few follow-up steps for the remaining calibration budget: tune the biases first, then check a global temperature change in a separate step, and then adjust the group scales one at a time, since changing several at once would make the effect on loss impossible to attribute.

I'm re-tuning just the biases at step 39, nudging each class's offset by a small amount based on how far its predicted count is from the true count. The largest adjustments go to 5 (down) and 6 (up), with the rest of the digits getting smaller corrections.

I'm settling on bias values for this step: nudging 9 and 0, 6, 8 up, and 5, 3, 2 down, then re-checking the loss. I'll keep temperature out of this step so any change in loss can be traced to the biases alone.

I'm reconsidering the bias adjustments and whether they were already accounted for, then deciding to go ahead with them.
