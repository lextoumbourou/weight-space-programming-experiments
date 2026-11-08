Checking the numbers, the 0.504 result comes out 0.015 below the null of about 0.489, which points to a small negative covariance between the x7 interaction and y, around -0.15 summed over the other terms. That's large enough to matter, so I want to find which interactions are pulling it down. The x7 product term involves x1 as a linear piece, plus x4 and x9, so those are the likely candidates to check.

I'm testing the null-cost estimate, which comes out to about 0.492 once the variance term is added back, so the observed 0.504 implies a small negative covariance of roughly -0.12 spread across the other interaction terms. I'll bisect the remaining candidates, starting with a negatively signed test on group A.

I'll test the negative sign on group A next, expecting the score to drop to about 0.477 if that group holds the effect, and then check group B.
