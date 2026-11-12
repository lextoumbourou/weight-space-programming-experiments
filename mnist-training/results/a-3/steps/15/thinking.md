The finer grid made template mismatches costlier, so the coarse setting is more forgiving and the templates look like the real bottleneck. Going back to the step-13 base, I'm wondering whether blurring the templates more within the coarse layout would help, since step 9 at sigma 2.5 was confounded. I'm also considering a more robust scoring method than the multinomial over features, perhaps something distribution-based.

I'm now considering a smoother template approach, blurring the templates spatially, and I'm checking the confusion counts at step 13 to see where the 8 template is pulling in too many 2, 3 and 5 cases.

I'm seeing why the multinomial doesn't penalize a 3 for lacking the 8's left-side features: it only gets diluted through normalization. A hybrid that adds an explicit match term on the template could fix that, and the pure class-level part of the penalty is already absorbed by bias tuning, so what's left is a single linear template-match addition.

I'm working out a hybrid scoring rule: the multinomial term plus a linear template-match term, with per-class biases tuned to calibrate it. Since the template-match term would be scale-sensitive, I'll keep its weight small, around 0.1 to 0.15, and check the resulting magnitudes against the log-probability differences.

I'm weighing a hybrid scoring rule that adds a linear template-match term to the multinomial one, with a small weight around 0.05 so its effect on the class biases stays manageable. The worry is that the template-match sums differ a lot between classes, so a larger weight could swing the calibration and push things toward the collapse I saw earlier. I'll recalibrate the per-class biases in the next step to absorb whatever scale error remains.

I'm considering whether a fixed "absence" feature could penalize the missing left-side strokes, since multinomial scoring never penalizes absent features directly. Max-pooled ReLU units can't express "no edge here", so I'd need a conv2 channel that sums edges over a 5x5 window and thresholds the result.

I'm settling on a hybrid scoring rule: the multinomial term plus a small linear template-match term with weight around 0.04, keeping the step-13 biases. To roughly account for the missing-feature penalty I'd been missing, I'm adding a bias term scaled by an assumed mean feature level of about 1.5, then planning to recalibrate.
