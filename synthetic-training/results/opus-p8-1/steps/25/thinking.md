I'm working out the covariance estimates for the two pairs: removing x6 and x11 raised the loss by about 0.006, and adding back the 0.0065 cost saving gives a signal near 0.0125, so the covariance sum comes to roughly -0.042. For x1 and x4, the improvement is about 0.0027 plus the same cost saving, giving a signal near 0.009 and a sum around -0.03. The two pairs look similar.

I'm settling on about -0.3 as the coefficient for all four, since the covariance estimates of roughly -0.02 point there. The null group's abs-value effect is small, around +0.008 per feature, so I'm not bothering with it. The next question is whether the nonlinearity comes from interactions between strong features, but with only four free units left, I can only cover about one pair per step, which is too slow.

I'm weighing whether to probe the linear weights on x6 and x11 together, or to test scaling all the terms by 1.1, since the abs terms might shift the best overall scale. Single-coordinate probes on the minor features look negligible, and pair interaction tests are too slow with only four units left.

I'm checking the earlier estimate of the x0 covariance: at s=0.5 without a bias, the observed loss of 0.7328 against the expected 0.724 suggests a small negative covariance of about -0.018. I'll accept that as negligible, and next I'll try a step that scales the linear terms by 1.1 while keeping the abs terms as they are.

I'm going to try a probe that scales all the linear weights by 1.1 and leaves the absolute-value terms alone, to see whether the best overall scale shifts.
