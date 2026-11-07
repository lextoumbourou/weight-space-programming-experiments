The zero-sum constraint hurt the 8 badly, since it has many strokes and gets almost never predicted, while the 1 is now overpredicted. The loss went up to 1.95, probably because adding the pairwise term inflated the logit norms. I think the real problem is that a linear template matcher can't capture this well, so I should look at a distance-based classifier instead and started sketching its logit as a negative distance.

I'm working out the distance-based logit more concretely: the bias term would be -||μ_d||², which depends on how well μ_d matches the real feature scale. Estimating that scale by hand, a stroke response in the conv2 output lands around 0.85 to 1.5, which seems roughly matched to the presence model. So I'll go back to step 2 and add a -0.5||T||² bias term, with a tunable parameter.

I'm weighing whether to use the conv2 channels as digit-part detectors, since loop and arc features could help with digits like 4/9, 5/6, and 2/8 where a linear template struggles. I'm considering a set of arc detectors (top, bottom, left, right curves) built from orientation patterns over a larger receptive field, which might capture shape structure better than plain template matching.

I'm weighing an arc-detector variant for conv2, with curve detectors for the top, bottom, left, and right shapes, since that might separate 4/9 and 2/8 better. For the next step I'll revert to the step 2 configuration and add a distance bias term with a modest coefficient, which is a small change for calibration. The best loss so far is 1.0061, so I need to get under 0.996 within five steps.

I'm weighing whether conv2 should split its 16 channels between four orientations on a coarse 3x3 grid and four arc detectors (top, bottom, left, right curves), leaving the remaining channels for something else like endpoints. The finer shift grid gave only a modest gain, so trading some of it for arc features seems worth trying.

I'm thinking about endpoint detectors for digits like 1, 6, 7, and 9, and whether putting the ink channel back in conv1 would help spot where a stroke stops. I'm also sketching arc detectors for the conv2 kernel, using a 5x5 window over the pooled map to cover about 10 input pixels.

I'm sketching the arc detector for the top of a loop, a horizontal piece at the top with diagonal strokes curving down on either side, on a pooled grid over a radius of about two pooled pixels.

I'm sketching the arc detector for the top of a loop, with a horizontal piece at the top and diagonal strokes curving down on each side, and I'm weighing how much bias to subtract so that a lone straight line doesn't trigger it.

Writing the arc-detector kernels now: the top-of-loop, bottom, and side versions with their weights, plus a negative bias so a lone straight line doesn't fire them.

I'm sketching the arc detectors for the remaining cases, deriving each one's shape from the direction its curvature points, and I'm checking the directional weights so that each arc type lines up with where its strokes would sit.

I'm defining the arc weights from each point's curvature direction, so that a top-of-loop detector responds to strokes whose curve center lies below them, and similarly for the other three arc types.

I'm placing each arc detector's location at the stroke point shifted about two input pixels toward the curve's center. Working out the grid, the kernel center lands on the same 4-pixel spacing as before, so the arc features still line up with the earlier cell positions.

I'm settling on conv2 as eight orientation channels across two shifts, with the remaining four reserved for arc detectors.

I'm settling the layout for the remaining conv2 channels: four arc detectors on a single grid, plus four ink-based channels sampled at four shifts. The ink channel is there as negative evidence, which should help with holes. I'll also normalize the templates per group, since the groups have different channel counts.

Now I'm grouping the conv2 features into three blocks, orientation, arc, and ink, normalizing each block to unit norm and weighting them against each other, while the arc-detector weight spec for the top-of-loop shape is just beginning.

Still writing the arc weights for the remaining shapes...

Still working out the arc weights for the remaining shapes...

Checking the horizontal line against the arc detector, the bias should pull its response near zero, so the arc output lands around 1.1 before the 0.7 group weight.

Still computing the arc weights from each stroke point's curvature, so each detector responds according to how well its direction matches the curve's center.

Still working out the arc weights, with each detector's response scaled by how closely its direction lines up with the curve's center.

Still working out the conv2 channel layout: orientation detectors at two shifts, the four arc detectors, and ink channels at four shifts, all mapped into the flat feature index.

Still setting the template normalization: each feature group gets unit norm and a weight, then the templates are centered and scaled.
