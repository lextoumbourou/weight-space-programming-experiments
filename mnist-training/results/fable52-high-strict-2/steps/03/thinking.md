The result came out worse overall, so I'm working out what changed. The column sums look uneven, and class 7 stands out: its recall dropped sharply, from 692 down to 230, and many of its predictions went to classes 9, 3 and 2 instead.

I'm checking whether class 7's vetoes are firing on real 7s, since its recall fell from 692 to 230 with many predictions going to 9, 3 and 2. A left tick on the bar might be triggering the vertical feature, and that could explain the 7→9 shift.

The scale mismatch looks like the real issue: if the features are two or three times larger than I assumed, the vetoes on 7 are overpowering it and the bonuses on 6 and 2 are beating the bias, so I'll check the actual magnitudes before adjusting anything else.

The 0s are losing recall to 2 and 6, and I suspect the centre-ink veto is leaking in from the sides of narrow zeros. With the sides about 4.5 px from the middle and a blur of roughly 2.6, the leakage alone comes out near 0.22, which could be enough to trigger that veto on real 0s.

I'm trying to pin down the actual feature magnitudes, since the bonuses and vetoes look several times stronger than I assumed. A probe that reads out a total activation sum per bank would show how far off my template estimate is, and that scale drives every bias and veto adjustment that follows.

I'm setting up a probe that counts how many thresholds the summed bank-A activation clears, using offset logits so each class boundary sits at a chosen threshold, with the cutoffs spread from 10 up to 65 to cover the unknown scale.

I'm now weighing whether to spend a probe step measuring the actual feature scale, since every bias and veto adjustment depends on it. Rather than sorting by a scalar sum, I could fall back to scale-free cosine templates and refine from prototypes, though I'm not sure the vetoes can be set sensibly without first knowing the magnitudes.

Since the vetoes and bonuses are all linear in the features, their effect relative to the template scores doesn't depend on the overall scale. Only the biases do. Against typical margins of about 0.5, a veto of around 0.8 is too strong, and the bonuses for class 6 were not offset by a large enough bias.

I'm weighing two paths: go back to the step-1 setup with only vetoes at a smaller weight, or run a calibration probe first. Step 2 showed that the bonuses were too strong to be offset by the biases, so the first option needs to drop them.

I'm reconsidering the approach: the step 2 vetoes and bonuses were added by hand at too large a scale, and the 6 and 2 attractors came from bonuses that the biases couldn't offset. A cleaner way to separate the pairs would be a contrast-style weighting, though I'll need to check whether subtracting the mean template changes anything in the argmax.

Next I'm weighing a nearest-mean classifier, where the weights are the class means and the biases come from their squared norms, which only works if I know the feature scale. A cosine version would normalise each template instead, and it's unclear how the two differ once the norms are handled. Either way, a probe to measure the scale looks like the way to make the rest of the adjustments sensible.

I'm weighing whether the vetoes, without the biases, can carry the pair distinctions, scaled down by about 0.4 to avoid the overshoot I saw in step 2. Since the bonuses alone would just pull classes toward 6 and 2, that part needs rethinking.

I'm going to drop the bonuses and biases and keep only vetoes, at half strength. Class 7 took the most damage, since its own vetoes stacked up and bonuses on 9 and 3 pulled its predictions away, so I'll plan the next step around that.

I'm weighing whether to keep only the vetoes at half strength and drop the bonuses and biases, since step 2 showed those were pulling classes toward 6 and 2. I'm also considering a calibration probe to measure the real feature scale first, which would let me make the bias-compensated bonuses work properly.

I'm estimating the expected feature totals per class from stroke lengths, for instance about 15 for a 1 and about 26 for a 0. I could just assume a scale ratio and test it, but a probe would be more reliable. The open question is whether that ratio alone is enough to set the biases.

I'm considering re-weighting the 9 template so the loop strokes count for more and the stem and top count for less, which would lower the score for a 7 without touching the bias. Since the template is unit-normalised, a 9 image should keep roughly the same score while a 7 image, which has stem and top but no loop, would drop.

I'm now treating the prototype weights themselves as the scale-free stand-in for the bonus and bias: emphasising the discriminative strokes and de-emphasising the shared ones before normalising. The vetoes would then be added as negative strokes, and the open question is how large the veto strength should be relative to the typical margin.

I'm halving the veto strengths and dropping the bonuses and biases, since the penalty relative to the template score is what matters and that ratio is scale-free. Keeping the prototype stroke emphasis mild should be enough to separate the pairs without the overshoot from step 2.

I'm working out whether a probe is worth running now to pin down the feature scale. A rough check on the step-1 loss suggests the scale is about 1, which would let me set the veto strengths without another measurement.

I'm checking the bonus-and-bias figures from step 2 against the veto sizes, and the numbers suggest the bonuses for 6, 2, 3 and 9 each outweighed their biases by a wide margin, which would explain the attractors.

I'm now treating the bonus and bias as one symmetric term: a bonus of g with a bias of -g, so the net is +g when the feature is present and -g when it's absent, and the same idea applies to vetoes with the signs flipped.

I'm now treating each item's contribution as symmetric evidence: a bonus g paired with a bias of -g, so the net effect is +g when the feature is present and -g when it's absent. The open question is whether a g around 0.2 is large enough to separate the pairs without the overshoot from step 2, given that a present feature only gives a response of about 2.

I'm looking at the 0 class, which loses ground to 2 and 6, and suspect the centre veto for item 9 is hurting 0's own score. The tip vetoes and the bottom-bar bonus for 2 may be adding to that, so I'm considering narrowing the centre veto to horizontal strokes only.

I'm dropping most of the vetoes for 7 and keeping only a couple of light ones, since its false positives came mainly from 1, 9 and 8. For the 0 class, the centre veto is probably leaking into its own score, so I'm considering restricting it to horizontal, diagonal orientations at a weaker strength.

I'm setting up the symmetric bonus-and-bias pairs for the remaining adjustments, with each item's strength around 0.25 or below. Vetoes will stay uncompensated, and the 3 class gets a light veto on two items plus a bonus on the lower-right vertical stroke.

I'm adding a bias-compensated bonus of 0.2 for the top horizontal stroke on class 9, though that also nudges 7 images toward 9. To offset that, I'm looking at adding evidence against 7 through the loop.

I'm checking whether the 4-to-9 errors come from the 9 template's tip vetoes and its top-bar bonus, and I suspect the tips are firing on 4s even though the 9 bonuses were uncompensated.

I'm going through the remaining veto adjustments: a veto on the upper-right vertical for class 5 and on the lower-left vertical for class 3 to cut the 9-to-3 and 5-to-3 confusions, and a light veto pair on class 7 to hold back the 9 and 1 false positives.

I'm checking which items feed the confusions between 1, 2, 4 and 7. For 2, a bonus on the bottom bar with a matching bias, plus light vetoes on the tips, should keep it from absorbing 1s. For 7, a top-left bonus with a bias offset should pull 1s away from it. Next I'm looking at 6 and 9, where a veto on the top-right stroke and a veto on the bottom bar should cut the 4, 5 and 2 errors.

I'm listing the veto and bonus strengths per item, with the 9 template's top-bar bonus offset by a matching bias and the 4s and 5s given opposite signs.

Still working out the per-item veto and bonus weights, with the strengths for items 3, 5 and 8 being set.

I'm assigning each item a set of per-class strengths, with the 9 template's top-bar bonus offset by a matching bias and the 4s and 5s given opposite signs. Still working out the per-item veto and bonus weights, with the strengths for items 3, 5 and 8 being set.

Still setting the per-item strengths, and this stretch is mostly the weights for the tip items and the bias compensation for the bonuses.

Still setting the per-item strengths, and this stretch is the bias compensation values for each class, working out the offsets from the bonus strengths.

I'm now setting the bias compensation values: each class's bias drops by its bonus strengths times a factor of about 0.9 for stroke items and 0.35 for tip items, so classes like 9 end up with the largest offsets.

Checking the veto strengths on classes 3, 5 and 9 next, along with the bias offsets for the bottom-bar veto. I'm also deciding whether the centre-stroke item needs separate orientations for its horizontal and diagonal versions.

Next I'm writing the centre item with its three orientations, which should keep the 0 class from being hit by its own veto, and then I'll update the code that handles the evidence and bias terms.
