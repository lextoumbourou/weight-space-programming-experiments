I'm stuck at around 66%, so I need to step back. The features I'm using, like the max over oriented responses in each block, look saturated for many digits, so the differences between classes are subtle. I'm considering whether conv2 channels could instead act as digit-part detectors over larger receptive fields, maybe a 16x16 window.

I'm thinking about using the conv2 channels as digit-part detectors instead, with each one acting as a matched filter over the pool1 orientation maps, so that a 5x5 kernel covers a 16x16 input window. Max-pooling over positions would give some translation tolerance before the fc layer combines the digit-template responses.

I'm weighing conv2 channels as nonlinear part detectors rather than linear templates, since a ReLU threshold gives an AND-like response that could separate digits better. I'm sketching candidate parts over a 5x5 window of pool1 features: a ring shape, a long horizontal bar, a long vertical stroke, a diagonal, C-shaped arcs facing left and right, and corner shapes like the top of a 5 or a 7.

I'm laying out the pool1 coordinate grid for the part kernels, with each cell indexed by row and column and spaced two pixels apart. Stroke responses there should sit around 0.5 to 1.0, ink around 0.5 to 0.8, and background near 1, so I can set thresholds that only fire on fairly complete matches.

I'm now setting up the first part detector, a ring shape, with horizontal taps along the top and bottom rows and vertical taps down the sides, plus a center background term. A full ring match should land well above a threshold, while a C-shape missing one side falls lower, so I'm weighing where to put the cutoff.

I'm checking whether the ring-shaped part detector would work for the 8, 9 and 6 loops, which are about 7 to 8 pixels across, but a 0 is taller and wouldn't match a single ring size. The threshold is the risky part, since I can't see the actual responses yet.

Blurring the templates before matching could help, since real digit variation is far wider than my crisp prototypes; I'd smooth each one spatially and mix in its neighbors' averages to get closer to a true class mean.

I'm considering whether to smooth the templates spatially and across neighboring orientations, since that might bring them closer to real class means. The catch is that smoothing changes each template's norm, which shifts the bias term and makes the threshold sensitive again. I could make the bias relative to each template's norm, or treat it as LDA with a shared isotropic covariance, but either way the calibration seems inherently fragile. I'm also wondering whether adding the total activation as a shared term would help.

I'm going to switch to a scale-invariant classifier: normalize each template by its norm and use the dot product, which avoids the per-image bias calibration problem. Dividing by the template norm turns the score into a cosine-style comparison that doesn't depend on how thick the strokes are.

I'm switching to cosine scoring so the per-image scale no longer needs calibrating, and I'm considering centering the templates around their shared mean, which should work better than comparing raw dot products.

I'm moving from the cosine idea to centering the templates around their mean and computing the bias from the expected input feature. For a class-e input, the logit for template d comes out as a scaled correlation, so the bias term only needs to match the mean template and the overall scale, and I still need to settle that scale.

I'm switching the score to a centered, normalized template, U_d = (T_d − T̄)/‖T_d − T̄‖, with logit β(f·U_d − κ T̄·U_d), where κ≈0.47 and β≈4. The bias now comes from the mean template rather than a norm-dependent term, though it's still sensitive to κ. I'm also dropping the old adjustment term and planning to smooth the templates spatially.

I'm going to smooth the templates before matching: spatially with a small neighbor average, and across the four orientation channels so adjacent directions blend, with the stroke-only channel smoothed spatially alone.
