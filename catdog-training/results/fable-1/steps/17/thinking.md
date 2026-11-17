The 0.6577 result is still a bit worse than S9's 0.6561, even with small weights on mid and coarse. That suggests the extra scales add nothing conditionally, or that S9 already overshoots along the VH direction or overall scale, so each addition pushes things further off.

I'm wondering whether S9's overall scale is simply too large, since the model's accuracy of 61% would imply a loss near 0.654 if well calibrated, so heavy-tailed features like green could be driving the excess. I'm considering a line search by scaling S9 down to 0.75 and fitting a quadratic through the loss values to locate the best scale, with clipping as a possible fix for the outliers.

I'm thinking about clipping the heavy-tailed features, capping green and T per location so the outliers stop dominating. Then I'll run the scale test on S9 at λ=0.75 to see where the loss minimum sits.
