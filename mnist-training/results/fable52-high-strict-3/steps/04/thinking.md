Now I'm checking the false-positive counts: the rate got worse at 72.6%, and class 8 is now over-predicted, with 927 false cases going to it, while classes 1 and 9 also pick up many errors.

The false positives for class 8 are now at 927, and recall for 8 went from 521 to 770. A 0.7 shift in bias moves around 900 images, so the margins near 8 must be very tightly packed, which means the logit scale is small relative to the bias. A bias of about −0.95 looks like the balance point, though it suggests the class logits are clustered closely enough that discrimination itself is weak.

The fan made class 1 over-predicted, since its broad template now catches many vertical-stroke images from 4 and 8. A bias of around −0.5 on class 1 might help. Class 7 and 9 are similarly sensitive: moving 9's bias by 0.5 shifts about 300 sevens, so separating them will need better features rather than bias tuning.

Now I'm working out why the rules for 0 might be hurting real zeros: the 0→8 confusions rose to 260 even though class 8's bias didn't change, which suggests the center penalties are catching genuine zeros whose windows extend into the fringe.

I'm now asking whether the rule for 0 is hurting real zeros, since the center penalties don't fit slanted zeros whose sides are oriented differently. I think I'll keep only the horizontal penalty at 0.4, since the others catch real zeros. Even so, each small bias change moves many images, so the class scores overlap heavily and more fundamental changes to the features are needed before accuracy improves much past about 77%.

Now I'm re-checking the pipeline for a bug, since accuracy around 77–80% from bias tuning alone seems too limited. I'll verify the template-to-feature index mapping, the orientation convention, and the conv1 filter direction, starting with the cross-correlation and the horizontal filter's row profile.

Checking the pipeline's orientation math next: the "/" diagonal ridge sits where x + y = 0, so it runs from top-right to bottom-left, and the angle works out to 45° in the template. For endpoints, I'm computing the outward direction from the neighboring point to the endpoint, so a stroke ending on the left gives 180°.

Checking the feature-index mapping now: the channel-to-template convention and the column-center weights both line up with the orientation setup.

Checking the centroid math and pixel-center offsets next: the pooled cells land at px 4l+7.5, and the centroid shift to 13.5 lines up with the 0–27 index range, so that part looks consistent.

I'm weighing whether blurring the templates toward class-like averages would help more than tightening the features, since a single sharp prototype per digit can't cover the range of widths and slants. Nearest-mean on raw pixels reached about 82%, and I'm at 76% after heavy bias tuning, so I'm considering more invariant features that capture relative stroke structure within a row band rather than absolute positions.

Now I'm thinking about the horizontal crossing counts for each digit, and how they could separate the classes: zeros have two crossings through the middle, ones have one, and the others vary by top and bottom halves. Vertical crossing counts could work similarly. A conv2 detector that fires when two near-vertical strokes sit side by side with a gap of about 4 to 8 pixels looks like a promising way to capture that structure.

I'm sketching a detector for two near-vertical strokes side by side, with a gap of roughly 4 to 8 pixels, using left and right column groups in the conv2 kernel and a threshold so both sides must fire.

I'm sketching a detector for a pair of near-vertical strokes on opposite sides of a 4–8 pixel gap, using left and right column groups with a threshold so both sides have to fire. A single stroke would stay below the threshold while two strokes would clear it. I'm not yet sure how a thick stroke, whose two edge ridges sit in adjacent cells on one side, would be handled.

I'm checking whether a double-vertical detector, with two near-vertical strokes on either side of a 4–8 pixel gap, could separate 8, 9 and 6 from the rest. The spacing fits those loops well, while the 0's sides look marginal at about 8 pixels apart. That leads me toward a 4x4 grid of top-versus-bottom double-V features as a stronger discriminator.

I'm considering whether a double-V detector and a double-H detector, firing together at the same spot, could mark loop-like structure in 8, 9, 6 and the top of 4. I'd still need to keep the earlier features in place alongside them, so the final layer has to weigh everything.

I'm weighing whether blurring the templates would move my accuracy closer to what the feature model can reach, since the gap seems to come from template quality rather than the features themselves. I could also try a more invariant feature, such as a double-vertical or double-horizontal detector for loop-like structure, though that would mean giving up some of the existing channels.

I'm considering a coordinate-wise search over a few global template parameters, such as the digit scale, slant, and blur width, adjusting one scalar at a time. The stroke height might be a bit too large, which could explain some of the mismatch. I also want to blur the templates horizontally, since the column windows are already wide and the row windows are fairly tight.

I'm wondering whether the features are simply too diffuse: the templates are sharper than the real images, so each digit's match ends up low across the board. Energy outside the template may be swamping the cosine similarity, which would explain the weak separation even though the features are already fairly blurred.

Now I'm weighing whether the features themselves are too diffuse: real strokes, curved and varying in thickness, may produce partial responses across all orientations, so the templates capture only part of the feature energy. I'm wondering whether sharpening the real feature responses would bring them closer to the template model.

I'm wondering whether the features are too noisy: maybe the real responses carry a lot of energy the templates don't model, and that could be why the class differences look so small. Cross-orientation inhibition or mean-subtraction might clean that up, though I already tried bias adjustments.

I'm working out whether a scale-free formulation would fit better, since the logits may be compressed if the feature magnitudes are small, which would let constant biases dominate the decisions. I'd subtract a per-class constant from all weights instead of using fixed biases, and pick those constants from the confusion feedback, which should at least stay consistent across images. I'm also trying to estimate the feature scale from the data, starting with the bias change for class 8 between the first and second steps.

I'm comparing cosine and ZNCC scoring here: the cosine score mixes in diffuse noise energy, and that noise hits broad templates harder, so mean-centering the features might separate the classes better.

I'm going back over the ZNCC idea: subtracting the mean removes the advantage that uniform diffuse energy gives to broad templates. I could try a centered template structure with a tuned κ, but each bias adjustment shifts large numbers of predictions, so I'd need small steps and would have to disentangle the effects of the rule changes made between steps 2 and 3.

I'm comparing the step 3 changes, starting with the 1-fan: recall for 1 rose, but false 1s jumped from 69 to 635. Most of that comes from 4 (14 to 202), with 6, 9, 8 and 7 also feeding in, which is odd since the fan should only penalize 1 where the image has ink far from the fan.

I'm weighing the fan-shaped 1 template, which seems to cover too much of the center. The 1 penalties from the ink-based checks clearly aren't strong enough to stop 4s and 6s from being labeled as 1s. A negative bias on 1 might help, but the sensitivity is high, so I'd rather reduce the extreme stroke's weight to around 0.3 or go back to a single near-vertical stroke with a bit of broadening.

I'm weighing whether a negative-weight "missing feature" channel could help, since a max-pool over nearby windows might flag places where a stroke is absent, though that only captures absence somewhere in the pool rather than everywhere.

I'm considering a saturating presence signal, where each window sum is clipped at a threshold so strokes of different thickness look alike, and a NOT-style absence channel built from the shifted minimum. With those, the readout would be a weighted sum of clipped features, which behaves more like a binary template match.

I'm considering a Bernoulli naive Bayes setup, where each binarized feature gets a log-odds weight from its template probability and the biases come from the summed log-complements. The idea is that saturating the feature presence would make the votes less sensitive to stroke thickness.

I'm weighing whether clipping the window sums at a threshold, using the minimum over nearby shifts, would turn each feature into a near-binary presence signal. That would make the naive Bayes votes less sensitive to stroke thickness.

I'm checking whether the presence signal can be made to saturate: taking a minimum over the four shifted patches would require the stroke to appear in the overlapping cells, so each feature responds to a narrow band regardless of thickness.

I'm working out the row coverage for the saturating presence windows: taking the minimum over the four shifted patches leaves a 2-pixel band per window, so the eight windows tile rows 6 through 21 without overlap, narrower than the earlier 4 to 23 span.

I'm weighing whether a saturating presence signal can be built by taking the minimum over the four shifted patches, so a stroke only counts when it sits in the overlapping cell. That narrows each feature to a two-pixel row band, though a stroke that straddles a cell boundary could still leak into a neighbor, leaving a fuzzy edge of about one cell.

Now I'm looking at how to make the window minimum saturate, trying larger row patches so the intersection across the two shifts covers two to three cells instead of one.

I'm working out the row coverage for the presence windows: with a three-cell patch, the intersection across the two shifts gives a 4-pixel band, centered at rows 5.5, 9.5, 13.5 and 17.5 for one offset and 7.5, 11.5, 15.5 and 19.5 for the other, which together span rows 4 through 21 with some fuzz at the edges.

I'm working out the column side of the same presence windows: a four-cell patch with a three-cell intersection gives the same 6-pixel span, so the saturated feature covers the same region as before, just with a strict presence test.

I'm comparing the column windows the same way: a 4-cell patch gives an intersection centered at 6.5, 10.5, 14.5 and 18.5, which is asymmetric, whereas a 5-cell patch centers at 7.5 but overlaps heavily. A 3-cell patch offset to [v+1..v+3] looks like the cleanest choice, giving a symmetric 4-pixel width at stride 4.

I'm settling the new conv2 design: each channel becomes a ReLU of the threshold minus the windowed sum, pooled by taking the minimum over shifts, so the output is an absence signal. Rewriting the readout in those terms, the logit becomes a negatively weighted sum of the absence features plus a bias that absorbs the weights.

Still checking whether the min over shifted patches should require the stroke to fill all four windows, and settling on thresholds around 1.5 for orientation and 0.6 for endings.

I'm settling on a Bernoulli naive Bayes classifier, with each class's per-feature presence probabilities estimated from its blurred template with a small noise floor. The per-feature log-odds would then be summed, though the features overlap heavily, so that sum will be overconfident.

I'm settling the class likelihoods as Bernoulli naive Bayes, where the missing-feature terms do the work of a presence requirement, so a broad template pays for every expected feature that is absent. Adding an epsilon floor keeps each weight robust, and a temperature on the summed log-odds would calibrate the overconfident votes without changing the argmax.

I'm checking how the threshold and naive Bayes weights hold up if the feature strengths turn out different from my estimates.

I'm now defining each template's presence score as a weighted coverage of its strokes, so the mapping from template strength to saturated probability is a soft threshold I can tune.

I'm settling the presence windows as strict intersections: a three-cell span gives a 6-pixel region around each center, and each window needs all four shifted patches to saturate. I still have to check whether the all-patches condition on the row offsets leaves gaps at the edges.

I'm checking how far the intersection window extends: the 4k+2a+4 to 4k+2a+9 span gives the core, and I'm estimating about 1.5 px of fuzz on each side from the minimum length a stroke needs inside each patch.

I'm checking whether the horizontal strokes clear the threshold in both column patches: they need roughly 2.5 to 3 pixels of run inside each one, which keeps the column window centered near 4l+7.5 with about ±1.5 pixels of fuzz.

I'm checking the column windows for the vertical strokes: a stroke has to sit inside both overlapping patches, so each window is about 4 pixels wide with roughly a pixel of fuzz at the edges. That leaves a stroke sitting right on the boundary near column 13 ambiguous, since it could land fully in either neighboring window.

I'm setting the template-to-probability mapping: row weights stay at 1 out to about 2.5 and fall to zero by 4, column weights are narrower, falling to zero by 3.5. The presence probability is then a clipped linear ramp of the normalized template response, so the naive Bayes terms stay soft near the boundary cases.

I'm tightening the presence weights in the template model: the row weight should stay at 1 out to about 2.5 and drop to zero by 3, since at 3.5 the stroke only leaks in through the ridge and falls under the threshold.

I'm going to blur the template so the probabilities reflect natural variation: each feature's presence probability would be a smoothed version of the prototype map, high at the core of a stroke and lower at its edges, with a small floor and ceiling to keep the naive Bayes terms robust.

I'm now writing the naive Bayes log-odds in terms of absence: each feature's weight on its normalized absence is the log-odds gap between missing and present probabilities, scaled by the threshold and temperature, with the summed log-probabilities folded into the bias.

I'm setting the temperature around 6 so the naive Bayes margins stay in a reasonable range, and clipping the probabilities at 0.1 on each side to keep the log-odds bounded. Endings are noisier, so I'm giving them a wider floor. I'm not yet sure whether this hand-estimated model can beat 76%.

Still settling the conv2 layout: I'm defining each channel as a ReLU of the threshold minus a windowed sum over the four shifted patches, with the weights set across three columns.

Checking the conv2 geometry now: each output cell reads a 4-row window from the pooled conv1 map, and the pooled cell k covers windows at offsets 2k and 2k+1, so the intersection lands at pixel rows 4k+2a+4 through 4k+2a+9, centered at 4k+2a+6.5.

Estimating the false-positive threshold for the stroke-strength cutoffs next: a diagonal crossing an 8×6 px window hits about three cells, so the orientation threshold of around 1.2 to 1.5 looks like a reasonable middle ground, though summed weak leakage from neighboring orientations could still push it over.

Working out the ending response levels now: the conv1 ideal value is around 1.5, but realistic ones land near 0.7 to 1.2, so I'm weighing whether the ending threshold of 0.5 lets corners through.

Now I'm working out the response levels for the ending detectors: the raw response should stay low for corners, while true endings saturate at about 0.8, so the 0.5 threshold separates them. I'm also raising the ending weights' uncertainty to match how noisy endings are, which narrows their log-odds range.

Now I'm weighing the temperature for the naive Bayes logits: with the per-feature costs I've set, a single missing or extra stroke segment is worth roughly 12 to 20 nats, and class gaps could reach 30 to 100, so a temperature around 6 leaves the logits overconfident on errors. I'm considering 10 as a starting point, though accuracy won't tell me which is right, only the loss will.

Now I'm turning the stroke amplitudes into a template probability: a window-weighted sum over the row and column distances, with the row weight at 1 out to about 2.5 and the column weight narrower, then a clipped linear ramp to get the presence map.

I'm settling the variation blur: rows get weights of 0.2, 0.6, and 0.2 across neighboring rows, columns 0.15, 0.7, and 0.15, and I still need to decide how to handle the edges and whether to mix adjacent orientations.

I'm settling the variation blur for the endings: endpoint responses get clipped and smoothed across rows and columns, and the presence probability lands in a range of about 0.15 to 0.75. Then I'll turn these probabilities into per-feature weights on absence, scaled by the threshold and temperature, with the summed log-probabilities folded into the bias.

I'm checking whether the normalized absence values stay in [0,1] and whether the class biases can be centered by subtracting their mean. Next I'm working through the template design: a single slanted stroke would trigger features that are unexpected for a 1, so I'm considering a weighted three-stroke fan instead.

I'm turning the stroke amplitudes into a probability map by combining each stroke variant's contribution with a probabilistic OR, so a digit's variants each count according to how likely they are.

I'm choosing the fan weights for the digit-1 template: the near-vertical slants get the highest weight, and the steeper tilts taper off, since real 1s mostly lean only slightly.

I'm now looking at the feature-template design: each digit becomes a fan of weighted strokes, and the probabilities come from combining each stroke's contribution. I'm also considering whether the endpoint features can use the same weighting, and I'm dropping the hand-written rules since the naive Bayes costs should handle unexpected features on their own. Finally I'm checking whether blurring across column positions is enough to cover the natural width variation in digits like 0.

Now I'm settling the ε and δ values at 0.12, which keeps the presence probabilities between 0.12 and 0.88 and bounds the log-odds around ±2.0. I'm also checking that the shifted-window minimum still behaves correctly on diagonal strokes.

Now I'm checking the conv1 response on a vertical stroke: it lands at about 0.78 in its own column and drops to about 0.09 next to it, so over a four-row patch the sum comes to roughly 4 × 0.78 + 4 × 0.09.

Checking the horizontal stroke's response across three column cells, I'm estimating the summed strength and whether it clears the 1.2 threshold.

Checking the 45° case next: a diagonal filter on a near-vertical stroke should give only a weak response, so the summed strength stays well under the threshold.

I'm weighing a bias on the diagonal filters: a near-vertical stroke leaks a small response into them, so the true class would be penalized about as much as the others. I'm considering a slightly higher bias on those filters, and settling on −0.15 for all orientation filters, with the endings' bias at −0.3.

Setting the ending bias to −0.25 and the ending threshold to 0.45, since real endings land around 0.6 to 1.0 once the bias is subtracted. Each ending's presence probability then comes from the maximum weighted response across ends, blurred and mapped into roughly 0.12 to 0.67.

I'm settling the scoring temperature at 12 and the ending bias at -0.25, which should leave the true class with margins of roughly 2 to 3 nats.

Still tuning the conv2 thresholds and building the template probability maps for each digit.

Now I'm writing the blur for the template probability maps, mixing each row with its neighbors in a 0.2/0.6/0.2 pattern and dealing with the edges.

Writing the blur code for the template probability maps...

Writing the digit templates now: each digit is built from weighted strokes, with the digit 1 getting a fan of near-vertical slants weighted more heavily than the steep ones.

Checking how the fan of digit-1 strokes combines: each stroke's weight folds into a probabilistic OR, so the central region comes out near 0.96. I'm also weighing whether the weaker 0.5-probability features might let class 1 over-predict, since those cost little either way.

Still writing the code for the digit probability maps...

Still writing the probability-map code...

Still writing the endpoint probability code...

Still writing the probability-map code, now the ending detection and the per-stroke probability combination.
