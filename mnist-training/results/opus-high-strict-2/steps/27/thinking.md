Checking whether step 27 gets me past 73.36 is already settled, since 26 landed at 73.42. The bigger problem is step 28, which needs roughly +0.35 from either 27 or 28 to beat step 23. I'll weigh the strongest options, the 596 recall, 610, and 640 candidates, and the run may end soon, so the gain has to be solid.

I'm checking the 9 variants against the 3, 7, and 2 templates, since the loop and stem shape of a 9 can overlap with each. I also want to test whether the 1 class is underperforming, because its recall is noticeably lower than it should be and it keeps getting confused with 7 and 8.

I'm wondering whether the 1 class is underperforming because its template doesn't cover very slanted 1s well, since their orientation may fall outside what the template spread captures. I'm also considering whether the blur should vary per class, and whether a slightly wider sigma would help, though the 0 results make me hesitant about widening it across the board.

I'm going to loosen the 0 template back to rx 5.5 with σ 3.9, since widening it hurt that class. For the 4s getting pulled toward 1, the narrow-stem cases are hard to fix with a template tweak. For 7s drifting into 9, the diagonal stroke is the distinguishing feature, so I'm checking whether a 9 template variant can keep that apart.

Next I'm adding a counter-stroke to the 9 template, a slanted "/" line placed just left of its stem, to keep 7s from being pulled into 9. I'm also setting the 0 template back to rx 5.5 with σ 3.9, and trimming the bias using the step-26 predictions.
