I'm looking at the hole detectors, which are firing on the wrong digits: many 3s, 5s, 8s and 9s are coming out as 0. The medium hole detector seems to trigger on open shapes like 3s and 5s, and the 0 weight is also overlapping with the 8 and 9 loops. Stepping back, I want a different approach that doesn't rely on these detectors.

I'm thinking about a different route, since tuning the hole detectors by reasoning alone isn't working. The confusion matrix is my only real feedback, and my templates may be placing strokes in the wrong spots. Blurring the templates heavily, or using simple ink density without orientation, might give a more reliable classifier.

I'm weighing whether to rely on magnitude-calibrated features with near-binary ink, since the scale-invariant projection approach may be pulling thin digits like 1s toward one class. Per-class biases tuned from the confusion matrix look like a possible fix, though they would interact with logit scale in ways that are hard to predict.

I'm now weighing a more structural approach, using features like the ink's width and height and where it sits in the grid, since the nearest-centroid method ignores which features actually vary. Without data to show that, I'd be guessing, but I can at least sketch what the typical digit shapes look like, such as the narrow vertical bar of a 1 or the top arc and bottom bar of a 2.

I'm checking whether the orientation detectors are misfiring on vertical strokes, and they look fine. The projection step is where the "1" attractor comes from, since the 1 template pulls the residual toward its own centered column.

I'm now thinking the narrow 8s and 9s get pulled toward the 1 template, since their ink sits in the center column, and I've been wondering whether my templates are simply too wide for those digits. Thin, slanted digits like 7 likely do the same. Right now 0, 1 and 6 seem to work, while 3, 8, 9, 7 and 5 are weak. I'm considering making the templates more varied, so they don't each assume one fixed width and slant.

I'm weighing whether to blur the templates more along the horizontal axis, with a wider kernel of about 4.5 pixels, so they absorb slant and width variation without generating synthetic samples to average over. A blur at around σ 2 to 3 pixels could make the local features more tolerant while keeping them local.

I'm weighing whether a translation-tolerant design could come from max-pooling over part detectors in the second conv layer, since their receptive field is large enough to cover a whole stroke pattern. That would be a sizable redesign, though my orientation features already behave somewhat like part detectors. Given how little feedback I have, I'm leaning toward iterating on the templates and per-class biases using the confusion matrix.

I'm weighing whether per-class biases, tuned from the confusion counts, can pull the 1, 6 and 0 predictions back down, while 8, 9, 3 and 7 need a boost. The logit spread is unknown, so I'd have to guess at bias magnitudes, such as about -0.8 for class 1.

I'm weighing per-class biases to counter the over-predicted 1s and 6s while boosting 8s, 9s and 3s. The 8s are being pulled toward 1, probably because my 8 template is too wide compared with real narrow digits.

I'm weighing whether dropping the hole detectors would help, since they seem to push 3s, 8s and 9s toward 0, and the medium one fires on too many open shapes. Keeping only a lower-weighted small hole channel might preserve the useful signal without the false 0s.

I'm settling on a small hole channel only, dropping the medium and large ones, with weights favoring 9 and 8 on the top channel and 6 and 8 on the bottom. The other classes get a penalty there, and I'll rely on per-class biases to correct the rest.
