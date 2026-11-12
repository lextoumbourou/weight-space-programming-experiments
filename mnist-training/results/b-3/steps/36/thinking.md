I'm down to 15 steps with a best loss of 0.7829, so I'm looking for any remaining gains. I'm considering testing g_end 3.0 by itself, since step 34 changed both the diagonal and g_end together, and I could also tune the loops one at a time.

I'm now weighing a few endpoint-based detectors: one for thick-stroke endpoints and another that checks whether a stroke end points left or right. I'm also considering a concavity feature that captures which direction a digit's open side faces, since that seems useful for telling apart 3, 5, 2, 6, 9 and 4.

I'm sketching a detector for the left-opening cavity: a center that must be empty, ink along the top, bottom, and right, and a penalty for ink on the left. I'm also weighing a right-opening version for 5 and 6, but I only have room for one cheap channel, so I'd have to drop one of the existing offsets.

I'm going to drop the ink channel at offset (2,3) and the one at (3,3), since the ink channel carries little weight anyway, and use that slot for left-opening and right-opening cavity detectors. I'm starting to place cavity centers for the left-open case, with 3 having an upper and a lower cavity near (12, 8.5) and (12, 18), and I'm still working out where 2's opening sits relative to its diagonal.

I'm checking the remaining candidate cavity detectors: the left-open template for 5's lower bowl, and a right-open detector that would fire on 5's upper bowl, with a weaker match for 6.

I'm checking the cavity detectors for each digit: the left-open template for 3 and 5, and the right-open one for 2 and 5. Most digits come out at zero, and I'm relying on the closed loops in 8 and 0 to keep the left-open detector from firing there, so I plan to set its weight at 1.8 and handle the negatives separately.

I'm settling the left-open cavity kernel: a center that must be empty, a few ink taps along the top, bottom and right, and negative taps on the left so that closed loops don't trigger it. I'm working out the bias from the ink values, which comes to a small positive number, then scaling it down.

I'm mapping the 16 channels now: the ink channel, two cavity detectors, the loop detectors, endpoint and orientation channels, and the diagonal pair. The template stays consistent with one ink offset, and the ink penalty should stay small since its weight is low.
