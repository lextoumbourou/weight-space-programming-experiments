I'm stuck at 73.6% with 30 steps left, so I need a bigger idea. The endpoint maps fire everywhere, which makes me suspect the detectors are weak, and I'm considering sparser detectors with a bias of -0.4 to get better endpoint features. I'm also wondering whether conv2's nonlinearity could let the fc template matching work with multiple templates per class.

I'm weighing a part-based design where conv2 channels act as local detectors for pieces like top or bottom loops, with the ReLU giving a nonlinear per-class score. Max pooling over conv2 positions would add some shift tolerance, though I'd lose the orientation grid features the fc layer currently relies on.

I'm looking at a part-based design where each conv2 channel detects a 14-pixel piece of a digit, with max pooling giving about 4 pixels of shift tolerance. Splitting a digit into top and bottom halves would need 20 channels, more than the 16 I have, so I'm weighing other ways to divide the work.

I'm weighing a steadier route than the part-based design: keep the current incremental approach, but improve the linear classifier on these features. Per-class scale adjustments and downweighting the noisier features might help more than a high-variance redesign with only 30 steps left.

I'm revisiting the orientation tuning in the templates, since the detectors show some cross-talk at 45° and 90°. I'm also wondering whether the 8 shear range needs to be wider, since many 8s are drawn strongly slanted.

I'm going to check whether a sharper calibration scale of 5.5 helps, and I'll pair it with the sparser endpoint bias of -0.4 to see which direction improves things. Each probe uses one of my remaining 30 steps, so I'm picking them carefully. I also want to look at why the 1s get confused with the 2s, since their endpoints tip up and down.

I'm trying to see why 1s get mistaken for 2s: a 1's bottom tip points down-left at the bottom center, and a 2's bottom-left corner might trigger a similar tip detector. Since I can't inspect the zero-mean template weights directly, I'm guessing that thin 1 strokes give weak overall responses, so their logits stay small and the biases could decide the outcome.

I'm checking the class biases next: the 2 and 3 biases look too high given how often 1s get pulled toward 2 and 3s get over-predicted, so I'm considering lowering both by 0.3 and nudging the 5 bias up slightly, while leaving 8 and 9 as they are.

I'm lowering the endpoint bias to -0.35 as well, though that means I'm changing two things at once again.
