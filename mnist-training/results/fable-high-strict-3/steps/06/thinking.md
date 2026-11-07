The 8 template is the sticking point: a small bias shift swings its predictions from about 210 to about 1817, so I'm reading that as a sign the 8 is sitting near the center of the digit space and gets pulled toward many other digits.

I'm now thinking the real problem is that the hand-drawn centroids don't discriminate well enough, so I'm considering a better design that mimics trained linear classifiers, with class-specific positive weights and negative weights on regions that indicate other digits. I'm weighing hand-designed region corrections, such as a strongly negative center for 0, as a knowledge-based alternative to the confusion-based alphas.

I'm going through the per-digit negative regions for each template: 1 is pushed down by ink in the side columns, 3 by the left-middle, 4 by top-center and bottom-left, 5 by the upper-right, and 6 by the upper-right as well.

I'm sketching out which regions should be penalized for each digit: 7 and 9 look like they need negative weights in their empty corners, while 8 has only weak signals since its ring covers most of the grid.

I'm realizing that nearest-centroid scoring already accounts for this: where a template is empty, its logit ignores ink, so ink only helps classes whose templates overlap it. Extra penalties on empty regions would amount to a per-class anti-template, which goes beyond plain centroid matching.

I'm noting that LDA with a shared covariance yields negative weights much like the forbidden-region idea, so explicit negative regions move the classifier toward a discriminative form. Estimating the scale, a −0.3 weight over empty cells where a confusing digit has about six inked cells gives roughly −1.4 logits, which is substantial given the soft logits. I'm now considering a cleaner formulation, W_d = s(μ_d − κ·N_d), where N_d is a hand-drawn forbidden-region mask and κ is around 0.5 to 0.7, and I'm starting to work out the bias term.

I'm considering whether to penalize the 8 template's waist regions, but the bands there are fat and would be risky. Another option is to lower the 8 bias so it predicts less often, rather than leaving it as the sink.

I'm now weighing whether the 8 needs its own negative region, since without one a 0 image could still score close to 8 on the parts the two templates share. The 8's waist is narrow, so a penalty there would be the only thing separating it from 0, and I'm deciding whether it's worth the risk of blurring.

I'm settling on the forbidden-region mask for the 8: a narrow band at the waist on both sides, which should separate it from the 0 and 6 without blurring, though the scaling and centering transform will have to be applied to those rectangles too.

I'm turning each forbidden region into a rectangle in unit coordinates, mapping it into template space with the same scale and shift, and rasterizing it into the 8x8 grid. To keep it safe, I'll zero out any cell where the template already has ink, so a region only penalizes places the template leaves empty.

I'm defining the forbidden regions in unit coordinates, starting with the 0's center hole and then the 1's flanking areas outside its narrow stroke, and I'm working out how those rectangles map into the 8x8 grid.

I'm now defining the 2's forbidden regions: a left-middle band and a lower-right patch near its base, with the right one shifted a bit so it avoids the arc's diagonal. Then I'm starting on the 3, looking at its left-middle area.

I'm defining the forbidden regions for the 4 and 5 now: a top-center band and a bottom-left patch for the 4, and an upper-right area for the 5, each to be masked out wherever the template already has ink.

I'm defining the 5's forbidden region in its upper-right, where the top bar and bowl leave the cells empty, and I'll mask out anything the template already covers. For the lower-left, I'm marking a band at the open left side of the 5 around y 0.55 to 0.8, which separates it from the closed loop of a 6.

I'm finishing the forbidden regions for the 6 and 7: an upper-right area for the 6 that should be empty, and for the 7, two side patches on the lower left and right that the diagonal leaves open.

I'm settling the 9's forbidden region as the bottom-left, below the middle, since its stem runs down toward the bottom center and leaves that area open. That should keep it apart from the 8, 6, 0, 2, 3, and 5, and I'll rely on the template-ink mask to clear any overlap at the stem's end.

I'm now working out the bias term for the classes, starting from the counts in step 5 where the predictions per digit are tallied.

I'm working through the bias calibration now, using the per-digit prediction counts against the expected counts. The adjustments come out small for most digits but larger for 6, 8, and 5, so I'm tallying the new values for each class.

Now I'm working through the 6's bias: it's predicted only 239 times against an expected 958, and the earlier template tweaks didn't lift it. I suspect the forbidden regions for 8 and 5 are catching 6 images, since 6s carry ink at the waist and bottom-left.

I'm finishing the mask step: each region's cell value is the fraction of overlap with the transformed rectangle, scaled down where the template already has ink. The shift is set so the transformed strokes stay centered, and I'll store the scale and offsets for each digit.
