The model has moved to 47%, but digits 6, 8 and 9 keep absorbing predictions from others, while 4 and 5 are almost never predicted. I suspect the nearest-centroid rule favors digits whose templates are broad and heavy, so I'm checking whether 0 is being pulled toward 6 for that reason.

I'm checking whether the 0 image lands closer to the 6 template because of how the norm correction interacts with the feature scale. If my template values are off from the real ink values, the bias term could be favoring the wrong classes.

I'm now checking whether the 4 template is off, since 4→4 is only 36 while 4 keeps leaking into 9 and 8. The 4 template's left stroke looks too diagonal compared with typical 4s, which would explain why 4 loses to the 9 template's circle-and-stem shape.

I'm now checking the 5 template against the 6: both have a bowl at the bottom, but a 5 has a top bar running across with no ink on the left between the bar and the bowl, which the 6 template doesn't capture.

I'm weighing whether to fix the 4 and 5 templates directly or to tune the class biases from the confusion matrix, since the bias route is faster with the step budget I have left.

Now I'm working through the per-class prediction counts against the true counts, since the class biases look like the easiest thing to correct. Classes 4, 5 and 0 are badly under-predicted while 6 and 8 soak up far too many guesses, so I'm estimating bias shifts from the log ratio of true to predicted counts.

I'm now converting the per-class prediction gaps into bias corrections, so 4 and 5 get a large boost while 6 and 8 get pulled down, with the step sizes capped so the adjustments stay modest.

I'm weighing whether the 4 and 5 templates are the real problem or whether bias correction alone will do, leaning toward a damped bias adjustment plus a shape fix for the 4 template.

I'm working out whether the 4 template needs its left stroke pulled more vertical and its bar placed lower.

I'm adjusting the 4 and 5 templates' stroke positions, moving the 4's bar lower and the 5's top bar across the top, so they separate better from the 9 and 6 shapes.

I'm wondering whether the 6 template is pulling in the 0s, since the 6 has a bowl shape that overlaps the 0 ring and the template's scale might be off. I'll keep the 0 case in mind alongside the 5 and 6 overlap.

I'm wondering whether the 6 template is pulling in the 0s, since the 6's bowl overlaps the ring of the 0 and the template scale may be off. Real 0s also vary a lot in slant and width, so the class mean might be too fat, and the -½||μ||² term would then penalize the big ring.

I'm checking the 0-versus-6 score: if the ring template's mass sits where the real ink is, the 0 should win easily, so the gap must come from the norm term penalizing the fat ring more than the 6's bowl.

I'm working out the scale of the ink response: a 3-pixel stroke through a σ=1 Gaussian gives a center weight of roughly 0.4 with its neighbors contributing the rest, so the template values depend heavily on how the blur is normalized.

I'm now estimating how much a stroke's ink spreads across neighboring cells after the blur and max-pooling, since the real feature values may run higher than the templates assume.

The rough scale check holds up: the ink maps are fat bands near 0.8, and my templates are narrower, so nearest-centroid may just be blurring the classes together rather than one template being badly wrong.

I'm going to correct the class biases from the confusion counts, damping the step so it stays modest. I'll also make the templates fatter and flatter so their scale is closer to the real ink, since the true class means are blurrier than my templates.

I'm settling the fatness at 0.55 and bumping the orientation-feature weight to 0.2, since the H/V/D templates are only rough approximations. Then I'm applying the damped per-class bias corrections, with 4 and 5 boosted and 6 and 8 pulled down, though the templates are changing too, so those numbers may need another pass.

Writing the code now.
