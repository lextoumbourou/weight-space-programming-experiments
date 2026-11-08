I'm fitting a parabola through three points, s=0.7, 1.0, and 1.5, and working out its coefficients from the divided differences. That gives a leading coefficient of about 0.1149. I also want the slope at the midpoint, 0.85, which I'm setting to zero.

I'm checking whether the parabola's minimum at 0.71 holds up, which puts 0.7 close to optimal and leaves the loss near 0.506. The linear model has plateaued around that, so I need nonlinear terms, and I have eight hidden units still free to spend on them.

I'm now going to test whether the absolute-value probes on x4, x7, and x9 pick up any nonlinear signal, since the x1 probe already came out worse. I'm also considering half-ReLU style terms, though the sign of the coefficient is unknown, so I'd try a positive weight first.

I'm now going to probe the x4 feature with a half-weighted absolute-value term, since it's cheap and could reveal whether there's any nonlinear signal there.
