Loss has improved a little to 1.036, but it's still stuck on a plateau. The 7→9 confusion (272 cases) is now the biggest error, ahead of 7→2 (135). I suspect the templates themselves are the bottleneck. A 7's top bar and stem look a lot like the top and right side of a 9's loop, so I'm checking which cells set them apart, mainly the left side of the 9's loop in the upper-left corner.

I'm weighing whether a simple reweighting would help, but without knowing the covariance of the features, that's guesswork. Pairwise differences just reduce to the same mean-centered weights, so I'm considering a sharpened, nonlinear selection instead. Given the 7/9 and 3/5 confusions, I'm leaning toward building part detectors in the second conv layer.

I'm now considering loop detectors for the confusable pairs, since the existing HB/VB features don't seem to fire reliably on loops. The idea is a hole detector: background at the center with ink on all four sides, using a few taps per direction at the pooled scale.

I'm checking whether a hole detector, with weak background at the center and ink on all four sides, can separate loops like 9's and 6's. The weights need to be low enough that the center doesn't dominate, with the threshold set between a full loop and a partial one.

I'm checking whether the hole detector's bias is the problem, since the background term inside a small loop may fall below what I'd assumed. Something seems off with HB/VB too: the loss didn't move between steps, so those features may not be firing inside loops at all. I'm working through the blur at the center of a 4-pixel hole to see what the background term actually contributes.

I'm checking the hole detector's bias term, since the background value at the center of a small loop might be lower than I assumed. Working through the numbers, the HB sum for a loop could land anywhere from about 1.2 to 1.8 against the -1.6 bias, which makes the outcome close to the threshold.

I'm thinking about recalibrating the background term so it doesn't drop to zero on strokes, since at the moment the hole detector rarely fires inside small loops. I'm also considering giving those loop features a larger weight in the template, because they look like the most informative signal for the confusable pairs. I'm not sure this will work, and I'd like to probe the features' activity directly before committing to it.

I'm recalibrating the background term for the loop detector so it doesn't drop to zero inside small holes, with the ink taps weighted lower and the bias set so partial loops fall below threshold.

I'm checking the hole detector's bias against horizontal strokes, which could give a false positive if the ink taps along the stroke add up. The bias needs the background term to carry more weight, so that ink on two sides alone can't push the detector over threshold.

I'm sizing the two hole detectors now: a small-scale one that samples only the taps at ±1 offset on each side, so a single inked tap is enough to rule it out, and a larger-scale one for wider loops.

I'm testing two weighted detectors for small holes: one with the background at the center plus ink at one tap on each side, and a=1, w=1 giving about 2.2 when both sides are present, 1.5 with one side, and 1.6 on a stroke, so the threshold of 1.8 separates a true loop. I'm checking how the pooled background at the center of a 4-pixel hole, two pixels from both strokes, would change those values.

I'm checking the background term inside a small loop: a 4-pixel gap between stroke centers leaves only about 1 pixel of clear space, so the blurred value there is low. For a 9's loop with roughly 3-pixel stroke-center spacing, though, the background should still sit near full strength, so the hole detector can work if the gap is big enough.

I'm sizing the loop detectors to the hole diameters: a ±1-tap version for holes around 6 pixels across, and a ±2-tap version for wider ones, with the same pattern repeated for the vertical direction. I'm also considering a combined loop detector that needs ink in all four directions, though for the smallest loops the taps at both offsets may catch the same stroke.

I'm setting the loop detector's weights for each digit: a large-hole channel for 0, the lower and upper loop regions for 6, 8, and 9, and a weaker closed-loop variant for 4.

I'm setting the loop detector channels: 5 and 6 as the larger-scale horizontal and vertical hole detectors, 7 and 8 as the small-scale ones, and 9 as a four-direction loop detector. Then I'll fill in the templates, starting with the small horizontal detector.

Still writing the template channels...

Setting the loop detectors aside for a moment, I'm settling the last details: the two-tap versions at ±2 for the wider holes, the same pattern vertically, and the weights for the 9's loop features, which I'll include in the templates with a 1.5 multiplier since they're the most informative for the confusable pairs.
