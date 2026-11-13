I'm checking the loss at gamma 0.3, which is the best so far at 0.3111, and comparing it against 0.5 and 0.8. The values drop as gamma decreases, so I'm wondering whether 0.15 would go lower still. I'm fitting a quadratic through the three points and computing the slopes between them, then starting on the second derivative.

I've got the optimum near gamma 0.1, with a predicted gain of only about 0.001, so I'm settling on 0.12. With two steps left, I'm weighing whether to pair that change with a test of the G_HV weighting, which could move the loss more in either direction.

I'm weighing whether a G_D change to 0.5 is the better test, since it lowers the weight on diagonal features and might also ease overconfidence a little. The diagonal and H/V features overlap through the same cell, so I'm not sure how much a change there would actually move the loss.

I'm now comparing the per-column and per-row prediction totals, which still look uneven even after the earlier bias adjustment. I'm leaving the bias alone, since balancing counts doesn't necessarily lower the loss when the misclassifications are asymmetric. For step 49 I'm settling on GAMMA 0.12 together with G_D at 0.5.

I'm thinking about what the G_D change would tell me: if it hurts more than the GAMMA gain helps, I'd know that for step 50 and could go back to G_D 0.62 or try 0.75. If it helps, I'd try G_D 0.4 next.
