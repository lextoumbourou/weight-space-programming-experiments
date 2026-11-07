The "1" digit is still winning, and I think the vertical channel is the culprit: its total for "1" is high, and after centering it stays positive. Central vertical strokes show up in every digit, so the vertical detector fires broadly and pushes "1" to the top. Orthogonalizing against the average ink map doesn't fully remove that effect, and I should check whether the ink correction is also leaving some of it in place.

I'm now testing whether the vertical channel is what keeps pushing "1" to the top, since its value stays high even after centering. Because central vertical strokes appear in every digit, I'm considering dropping the vertical and horizontal channels entirely to see whether the orthogonalized ink templates discriminate on their own. I've used seven steps, so I want to pick the next test carefully.

I'm going back to step 2, the 29% version, and making only small bias adjustments. Step 5 showed that ±1.2 is too large given the logit spread of about 1, so I'll try about ±0.2 to nudge classes 0, 2, and 7 without breaking the rest.

I'm sticking with the step 2 setup and making small bias nudges, since the bigger tweaks keep pulling everything toward "1." For classes 0 and 2, the step 2 confusion shows they're mostly losing to 6, so I'm giving each a bias of +0.4.

I'm tuning the biases by hand now: the step 2 confusion shows class 5 absorbing most of 3, 7, 8, and 9, and class 6 absorbing most of 0 and 2. So I'll pull b5 down substantially, around -0.5, and push b6 down a little, while giving the under-predicted classes 3, 7, 8, and 9 small positive nudges.

I'm setting the biases by hand now: the step 2 confusion matrix shows class 5 absorbing most of the wrong predictions, so I'll pull its bias down to about -0.5 and raise the under-predicted classes 0, 2, 3, and 7 by roughly +0.3 to +0.4.

I'm settling on a gentler bias set around ±0.3 for step 2, since the template signal spread is probably under about 1.2 and the ±0.4 values might flip too much at once.

I'm settling on the nudged bias values, which are small enough not to overwhelm the template signal. Going back to the step 2 templates, I'm about to reconstruct the ink patterns for each digit exactly as they were.

Still writing the ink templates...

Still writing the ink templates...

Still writing the ink templates...
