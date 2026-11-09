The 8 is now over-predicting, at 1762 predicted against 1009 true. It does pick up 872 correct, but a lot of other digits get pulled into 8 too, so the boost went too far and I need to pull it back.

I'm still weighing whether the V bonus is what overshot. The 8 bias went up by 0.4 and the lower-left V term can add up to about +1.4, so digits like 6, 0, and perhaps 2 are being pulled toward 8. I'm considering setting 8's V bonus to around zero and keeping the bias at +0.1, aiming for roughly 1000 to 1100 predicted 8s.

I'm weighing whether to drop the 8 V-bonus entirely and nudge the bias back down, since the boosts from the lower-left V term and the bias change together seem to be pushing too many digits into 8.

I'm choosing to set 8's bias to 0.0, which should cover most of the gap since the bias went up and the HOLE penalty eased. The 2s look like they're losing accuracy too: 486 correct now, down from 630, with 313 of them drifting into 8, probably because the lower-left V penalty is hitting 2s that really do have that stroke.

I'm setting the 3 bias to -0.6, since its predicted count has jumped to 1382 against a true 1030 and dropping the 8 bonus should pull some of that back. The 5s look fine on the 5→3 side, but their jump into 8 suggests the lower-left anti-stroke may need checking.

I'm dropping the 8 and 2 bonuses so the spillover into 8 stops, and setting 8's bias to 0.0, 3's to -0.6, and 2's to 0.6. I'm also trimming 7's bias slightly, since 9 and 7 are trading digits. I expect this to land near 78-79%, with a couple more passes after that.

I'm considering whether to add an anti-stroke for the 0s, since 2 → 0 is still at 84, and the center rows might separate zeros from 2s.

I'm going to drop the boost on the lower-left V term, since the 0 and 2 anti-strokes look too risky with slanted zeros, and I'm leaving the 0s alone for now. I'll rebuild step 13 from step 12 by adjusting the extra terms and class biases, then aim for roughly 78-79% accuracy.
