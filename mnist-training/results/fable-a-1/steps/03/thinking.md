Next I'm tallying the remaining transition counts for each state pair, and then I'll total the column sums across states 0 through 4.

Now I'm weighing whether the 8 template is simply too broad, since it pulls in 2s and 3s that happen to be curvy.

I'm looking at whether the real feature strengths are sparser than my templates assume, since the 45° cross-talk I estimate for the template looks higher than what real strokes would produce. Rather than run a broad sweep, I'm considering one test: raising the clipping threshold and the template threshold together, to see if the loss drops.

I'm weighing a per-class bias correction tied to each digit's template density, which would fix over-prediction of dense classes like 8 and 6 without changing the features themselves. The over and under pattern across the digits suggests the calibration is off in a systematic way, so one scaling knob might be enough.

I'm now looking at the 2s, which are being under-predicted: the 2→8 and 2→3 confusions are still large, so my template for 2 is probably not capturing how real 2s are drawn, with the arc, the diagonal neck, and the base stroke.

I'm weighing how the 2s fit against the 8 template: real 2s share most of their strokes with an 8, such as the top arc, the central diagonal, the bottom base, and the lower-left loop, so the 8 template only loses ground where a 2 lacks a stroke it expects.

The 2s still don't line up with my template, while the 8 template picks up most of their strokes, so a missing feature only costs a small logit penalty. With 64 noisy features the templates are simply too imprecise, so I need either sharper features or a better model of how digits vary.

I'm thinking about the 2s versus the 8s and 3s in human terms: a 2 has a full-width base at the bottom and a diagonal running through the lower left, while the lower right above the base stays empty. A 3 bulges at the lower right, and an 8 has features on both sides. Cell positions near the center should separate them, though the 8-pixel cell width may blur those distinctions.

I'm checking how well the 2 template fits real digits by looking at the confusion counts, since that will show whether the templates or the features are the weak point. I'd rather find a structural fix, such as sharper, non-overlapping cells, than keep tuning the template strokes by hand.

I'm thinking about the 5-versus-6 confusion, where the 6's closed loop puts a stroke at the lower left that a 5 lacks, so that's the feature I'd want to check for.

I'm weighing whether to pair up the hard confusions, like 3 versus 5 and 3 versus 8, with dedicated discriminator features on top of the naive Bayes weights. Since NB already gives those pairs equal weight, the real problem may be noise from unrelated features rather than missing pair-specific evidence. That suggests sharpening the squash so confident matches and mismatches count for more than uncertain ones.

Now I'm wondering whether the squash parameters could be the bottleneck: tightening the probability bounds to 0.04 and 0.96 while lowering the temperature to 0.15 might sharpen the confident matches. Since loss is 0.97 at 76% accuracy, the logits may be underconfident, so I'm considering trying a higher temperature of 0.3 as a single step to see which direction the loss moves.

Now I'm thinking through how to sharpen the 3 template against the 8 and 5 confusions, starting from the typical shape of a 3's upper bowl and lower bowl.

I'm weighing whether the 3 and 5 confusion comes from the upper arc: a 3's top is flatter, with a diagonal, so the template's right-side V may be misplaced. I'm also wondering whether the digit scale (the 17.5 assumption) is off, which would push strokes toward the edges and blur the templates there.

I'm weighing whether the feature set is the real bottleneck, since the remaining errors look more like shape variability than a wrong skeleton scale. Shifting the center by half a pixel and the digit scale by a point would change little, so I'm leaning toward better features or reweighting instead. A quick win might come from per-class bias adjustments that pull predictions for 8 and 6 down and for 2 and 5 up.

Next I'm considering whether to fold per-class bias shifts into the same pass as the template changes, so the confusion patterns stay easy to read afterward. I'm thinking about a bias adjustment that lowers 8 and 6 and raises 2 and 5, then wondering whether a structural feature change, such as finer resolution, would help more with the specific confusions.

I'm considering whether a 5x5 kernel in conv2 could capture larger structures, like a horizontal stroke over an empty region. Comparing the confusing pairs, 2 is distinguished from 8 and 3 by an empty bottom-right above the base, which the current negative weights should already cover. The 5/6 pair hinges on whether the loop is closed, while 4/9 hinges on the closed top, and 7/9 on the loop's presence, since 9 has a left side and a middle bar that 7 lacks.

I'm thinking about adding a hole detector, since closed loops separate 6, 8, 9, and 0 from 1, 3, 5, and 7, and that would resolve several of the biggest confusions, roughly 700 errors. I'm weighing how to build a reliable one from the 5x5 conv, pooling, and linear layers, starting from the fact that a hole is a background region fully enclosed by ink, about 8 pixels wide and 12 tall in a 0.

I'm sketching a center-surround conv1 filter that fires when a small blank center sits inside a ring of ink, since a 5x5 window could catch holes of about 2-3 pixels. Corners and U-shapes would only partly fill the ring, so the threshold has to sit high, around 12 of 16 ring pixels.

I'm weighing a way to detect holes with conv filters: the ring of ink around an empty center, which would separate 6, 8, 9 and 0 from 1, 3, 5 and 7. Pooling and the 5x5 window limit how precisely that enclosure can be checked, so I'm looking at how to approximate "ink on all four sides" with directional terms.

I'm working out how to detect the hole inside a digit's loop: an edge with ink on one side and blank on the other, facing inward, would mark each wall of the hole. Those inward-facing edges are thin, so after pooling each wall should show up as roughly one cell.

Still working out the hole detector: a signed edge filter whose inward-facing responses on each side of an empty center add up to a threshold, with the open-U shapes having one side missing.

I'm designing the hole detector as four signed edge filters on conv1, one for each side of an empty center, since each wall of a loop shows up as a thin inward-facing edge. Then a conv2 channel can check that all four walls converge on the same center. I'm now sketching which pooled positions around the center should carry those weights.

I'm working out the hole detector for the 6, 8, and 9 loops, using the vertical walls on either side of the center. The top and bottom walls would not both fall within reach for a 0, so I'm treating the 0 separately, and the position of the detected hole in the pooled map would separate 9 (upper), 6 (lower), and 8 (both).

I'm now sketching the directional edge filters, with a 5x5 profile of two ink pixels and two blank pixels, so a thin wall of a small hole gives a strong response. The concern is that if the hole is only about two pixels wide, the blank side of the filter could pick up ink from beyond it, which would weaken the edge.

I'm settling on the edge filter's shape: a column profile of two ink pixels, a neutral center, and two blank pixels, with row weights that taper at the ends so it stays local to small loops. I'm normalizing it so an ideal wall edge gives a response of about 1, and checking that the profile sums to zero.

I'm checking whether a simple edge detector can tell a hole's wall from the right side of an ordinary stroke, and it can't on its own. So the hole test has to be the conjunction of four inward-facing walls around an empty center. A U or C shape only supplies three walls, and parallel strokes or a corner supply two, so the threshold has to require all four.

I'm checking the four-wall conjunction against the three-wall shapes like 2, 4, and 5, since a simple sum of edge responses can't tell 4 from 3 without a sharper threshold. I'm considering whether a pairwise combination could approximate the AND more reliably than a plain relu over all four terms.

I'm considering an alternative to a four-way AND: since a hole means no ink in any direction from the center, I could check openness along each ray instead. Another option is to have conv2 compute partial enclosure channels, such as left-right and top-bottom, and let the later layers combine them, though a linear FC layer alone can't perform the final AND.

I'm considering a min(L, R) style approximation for the left-right enclosure, since a plain sum of the two walls can't require both to fire at once.

I'm noticing that a plain sum of the four wall responses can't cleanly separate a closed loop from a three-wall shape, so I'd need a sharper threshold. Checking the two-layer min trick doesn't work either, since pooling sits between the layers. I'll fall back on a soft AND, though the overlap between full loops and three-wall shapes is still a concern.

I'm weighing whether a conv1 pattern of blank pixels flanked by ink on both sides could catch a hole, but a pooled max only gives an OR over positions, so it can't supply the AND across the four directions that I need.

I'm turning to corner-based detection: each of the four inner corners of a loop would be a conv1 pattern, ink on two sides with blank at the diagonal, so the hole test becomes a combination of those four corner responses in conv2.

I'm noting that a "U" shape only closes two of the four inner corners, so with the corner test a true loop should score 4 while open shapes score around 2, a wider gap than the wall-based version gave me. Near-closed loops with small gaps may land at 3, so I'll need to set the threshold between 2 and 3.

I'm checking how the corner-based hole score behaves at the threshold: two corners at full strength give about 2.0, below a 2.5 cutoff, while four corners at 0.7 or more clear it. The risk is that a corner response spread over two pooled cells could push a two-corner shape past the threshold.

I'm now weighing a fix for the false fires: instead of summing corner responses over a region, I'd use separate hole-detector channels tuned to fixed corner separations, so each corner blob lands in one cell.

I'm sketching the top-left inner-corner filter now: ink along the top and left, with blank pixels at the bottom-right, so it fires where a loop's interior curves in.

I'm now testing whether diagonal edge detectors, one for each inner corner, could stand in for the four walls; a U's vertical walls would partly trigger the TL and TR detectors under broad tuning, which threatens the separation between loops and U shapes.

I'm settling on a corner detector instead of a diagonal edge, since a plain diagonal filter would still catch a U's vertical walls. Each corner filter needs ink on both its top and left arms at once, so a single wall only gets about half the response, and a bias set just above that keeps walls silent.

I'm sketching the top-left corner filter with positive weights on the top and left bands and a negative block over the lower-right center, so a wall alone only gets about half the response.

I'm sketching the response for the corner filter's positive and negative cells: each positive cell gets weight a, each negative cell gets weight −b. A straight vertical wall covers ten positive cells, and I'm checking how much the negative block subtracts when the wall sits further right.

I'm working out the diagonal-edge case for the corner filter, where ink sits on the upper-left triangle, and I find it totals the same ten positive cells as a straight vertical wall, so a plain diagonal test won't separate them.

I'm checking whether a diagonal edge can fake a corner: a "/" stroke's lower-right side scores as a top-left edge, so the corner filter still needs a way to separate it from a true inner corner.

Now I'm testing whether a corner filter can separate a true inner corner from a diagonal "/" stroke, since the stroke's edge would trigger the same response.

Working through the corner filter's numbers, I'm finding that a diagonal arc inside a round hole reaches about 14a − b, which sits close to a true corner's 16a. So a plain diagonal edge can't be told apart from a real corner at this scale. Setting a = 1/16 keeps a full corner at 1.0, and b around 0.15 seems to keep the solid region from firing.

I'm checking the numbers for the bias: a wall alone gives about 0.625 and a diagonal edge about 0.725, both close to a full corner at 1.0. A bias near −0.65 would silence walls but leave diagonal arcs with only a weak response, which makes the detector fragile for thin strokes.

I'm thinking about making the top-arm positives heavier, so that a vertical wall, which only has ink on the left, scores lower than a diagonal edge that has ink on both sides.

I'm assigning weight only to the arm cells and leaving the shared corner block at zero, so a straight wall gets half the response. But a diagonal stroke's edge also collects about six arm cells, the same as a wall, so the weighting alone doesn't separate them yet. Extending the diagonal out to r+c≤4 is what pushes it higher.

I'm settling the scaling: with a = 1/12 and b = 0.12, a true corner scores 1.0, a diagonal arc at best about 0.6 to 0.7, and a plain vertical wall only 0.5. A bias of −0.5 silences walls entirely while leaving diagonal arcs a weak positive response, and doubling everything gives corners 1.0 and diagonals about 0.42.

Now I'm checking how a round loop's inner curve fits the top-left filter: a small circle around the window's center puts ink along the top row and the left column, so it should land near the corner response.

I'm working out how the corner responses in the hole detector land relative to the loop's center, since the TL, TR, BL, and BR filters each fire near a different inner corner and their offsets from the center determine whether they add up.

I'm checking how far apart the four corner responses land: for a hole of radius 2 the separation is about 1.4 pooled pixels, for radius 3 about 2.1, and for a tiny loop about 1. So the conv2 kernel needs to place the TL, TR, BL, and BR taps at offsets that match those spacings.

Now I'm working out the spacing of the four corner taps, since the loop sizes I care about range from tiny to large and each one needs its own offset pattern.

I'm settling the threshold: a true corner scores about 1, a small round loop's corners about 0.6 to 0.9, and larger loops only about 0.4, so a loop should sum to roughly 2.4 to 3.6 across the four corners. Shapes with at most two corners stay under 2, and near-closed shapes like a 6 with an open loop land around 2.4, so the threshold has to sit between those ranges.

Setting the threshold at 2.2 means the loop responses (0.2 to 1.4 after subtracting it) can drive the hole feature, while any shape with only two corners tops out at 2.0 and stays silent. Each corner response is bounded by 1, so the summed value stays in a predictable range, and I can feed it forward with a weight and maybe a scale factor.

I'm checking the false negatives next: thick strokes or very tight loops, like a filled upper loop on an 8, can leave no detectable hole, and large loops in a 0 won't fit the kernel spacing.

Now I'm looking at how the four corner taps for the hole detector should be spaced, since the sizes I want to catch are a few different loop widths and each needs its own offset.

Now I'm weighing how to scale the hole detector's output, since the unclipped sum across size channels can range from about 0.2 to 3. I'm leaning toward a moderate linear weight so that a clear loop gives strong but not runaway evidence.

I'm mapping the final 4x4 cells back to the input: each one covers two conv2 outputs, so the hole center for cell a lands around input rows 4a+6.5 to 4a+8.5.

Now I'm placing the 9's loop center in row 1 or 0 of the cell grid, and the 6's loop center near row 2, based on where their vertical positions fall.

Now I'm assigning hand-set weights to the hole features by row: the top two rows should push positively for 9 and 8 and negatively for most other digits, while the bottom two rows should favor 6 and 8.

I'm settling the hole-feature weights by row: in the upper rows, 8 and 9 get positive weight while most other digits are pushed negative, and in the lower rows, 6 and 8 take the positive side. I'm also thinking about how to handle the case where no hole is detected at all, which would mean adding a negative bias to the hole-dependent classes.

I'm settling the hole-feature weights for the rows: the detector's effect shifts with the explicit bias term, so I'll drop the absence penalty for now and give 0 a small positive weight everywhere. Since the loop detector can miss a lot, my main worry is that it will misfire, so I'll judge it by whether accuracy moves on the confusable pairs. I'll start with a moderate scale, since the summed hole signal across size channels could reach two or three.

Now I'm checking the thin-stroke case: with a 1-pixel stroke the corner responses drop to about 0.5, which the bias cancels out, so the detector would miss those loops. Thick strokes are fine, but small inner holes around 2 pixels are the worry, since the negative region of the corner filter picks up ink from the opposite walls.

I'm checking the corner-tap weights for small loops: the negative region shrinks to a 2x2 block with a larger penalty, which keeps a 2-pixel hole from being cancelled by ink on the opposite walls. The wall and diagonal cases still come out right under the new weights.

Now I'm checking the diagonal and curved edge cases against the corner filter's thresholds, and confirming that small circles still fire while straight edges stay below the bias.

I'm checking the response for an inner circle of diameter 7: the filter sees only about four of six ink cells on each arm, so the corner response drops to roughly 0.33. A tighter loop of diameter 5 still gives a full response near 1.

I'm settling the corner-tap weights for the loop detector: each arm cell gets 1/6 and each negative cell 0.6, with the bias moved to zero so the response is centered where I want it. That keeps small loops firing while straight and diagonal edges stay near the cutoff.

Working out the trade-off between the corner threshold and the bias: walls land near 0.1 after the shift, so a shape needs about three real corners to get past the cutoff. A C-shaped bowl with only two corners stays quiet, and a loop that is mostly closed but has one corner open could still reach it, which is the case I want the detector to pick up.

I'm settling the corner-tap threshold at about 2.1, since a perfect pair of corners sums to 2.0 and should stay silent, while three slightly imperfect corners should clear it. The pooled map already takes a max over each 2x2 block, so small positional misalignment between the kernel and the corners won't cost much. Next I'm working out where each corner response peaks relative to the hole's center, which tells me how far apart the tap offsets need to be.

I'm working out where the corner responses peak for small loops: for a radius-1.5 circle the taps sit about 1 pooled cell apart, and the separation grows with the loop size.

I'm working out how far apart the corner taps need to be for different hole sizes: roughly one pooled cell for the smallest loops, growing to about two for larger ones. Tall and wide ovals would need offset taps in a different arrangement. I'm also wondering whether a hole of only about two pixels, with all four corners landing in one pooled cell, could still be told apart from other sizes.

I'm sorting out the pooled-coordinate kernel placement for the eight corner channels, with each channel's row offset set by its vertical separation.

Now I'm pinning down how the pooled-grid coordinates map back to the input: each corner response is tied to a conv1 index, and a hole's center falls midway between the top and bottom corner rows, which I'll convert into an input row position.

I'm mapping the hole centers back to input rows: each pooled cell covers a band of about four rows, so a 9's loop lands in row 1, a 6's in row 2, and an 8 splits between rows 1 and 3 depending on where its loop sits. That leaves "upper" as rows 0 and 1 and "lower" as rows 2 and 3, with a 0's center falling between rows 1 and 2.

Now I'm settling the row-based FC weights: the rows of the hole-detector output map onto the upper and lower classes, and I'll use full weights throughout since the boundary near row 2 is soft.

Now I'm writing out the per-row weights for the hole channels, with the upper-class values pulled from a table of positive and negative weights for each digit class.

Now I'm assigning the per-class weights for the lower-half hole channels, with 0 and 1 weighted strongly against and 2 slightly positive since some loopy 2s have a hole at the bottom-left.

I'm settling the hole-channel weights per digit class, with the upper and lower halves handled separately. Then I'm considering how large the logit swing becomes if the loop detector fires reliably, since a strong positive or negative contribution could outweigh the other features.

Writing the corner filter weights for the top-left detector: arm cells get 1/6 each, the four center cells get a negative penalty, and the corner block stays at zero.

I'm checking the corner filter against the wall cases: a left wall gives 1.0 minus the 1.0 bias, which is zero, and a corner gives 1. A thick wall, a blank patch, and a solid block all fall below zero. Next I'm looking at whether a crossing stroke could push the response above 1 without a real concave corner.

I'm checking how a "+" crossing lays out its four inner corners, since each quadrant's corner type is flipped relative to the hole detector's arrangement, so the taps need to account for that.

I'm checking that the TR, BL and BR filters are just the TL filter mirrored or flipped, and that the corner placement lines up with the upper-left inner corner of a hole.

Now I'm writing out the hole detector kernel: each of the four corner channels gets weight 1 at its offset, with a negative bias so it only fires when all four corners line up.

I'm weighing whether the corner threshold should move, since with the current bias a loop with real-world soft edges might only sum to about 2.0 and miss the cutoff. Lowering the conv1 bias to about -0.8 would let real corners contribute more, though it also lets walls get closer to firing, so the threshold would need to be set against both cases.

I'm settling the conv1 bias at −0.9 and the hole threshold at 2.0, since real loop corners tend to come out weaker than the ideal sum while a U-shape's walls stay below the cutoff. I still need to check that the pooled cells line up so the four corners of a loop land consistently.

Writing the corner filters now: the TL kernel gets weight 1/6 on its top and left arms, a negative penalty in the centre, and the other channels are flipped copies of it.

Writing the transition filters now: the TR, BL and BR kernels are mirrored or flipped copies of the TL one, with the same bias.

Writing the sizes loop for the second conv layer now, mapping each of the eight hole-detector offsets onto the four corner channels.

Still writing the weight loops for the hole channels...

Now I'm weighing a constant negative bias on the 6, 8 and 9 outputs, since the hole channels only push those classes up when a hole is present and wouldn't stop 5s and 3s from being mistaken for them.

Setting the bias adjustments now: a negative shift on 6 and 8, a smaller one on 9, and slight positive nudges for 2 and 5. Those counter the hole channels' pull toward the loop classes, and the hole weight α gets scaled so that a detected loop adds to the loop classes while its absence pushes them down.

Next I'm checking the detector's sensitivity by tracking how the confusion counts shift: 9→7 and 7→9 should drop if the loop signal is picked up, along with the 5→6, 3→8 and 2→8 errors. I'll also watch whether recall for 6, 8 and 9 holds up, since a big drop there would mean the detector is too weak.
