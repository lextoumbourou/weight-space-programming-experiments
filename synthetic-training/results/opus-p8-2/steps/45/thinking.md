I'm fitting a parabola through the three points at s = 0.9, 1.0 and 1.1 to locate the minimum. The second difference gives a curvature around 0.115, and the slope at s = 1.0 is about -0.0165, which puts the minimum near s ≈ 1.07.

I've got the minimum around s ≈ 1.07, with a best value of about 0.4768, though the margin is small. With six steps left, I'm considering a bias shift of ±0.1, since the prior log ratio may be off once the nonlinear terms are centered. The class 1 prediction is undercounted (377 against 395), so I'll try +0.1 at s = 1.07.
