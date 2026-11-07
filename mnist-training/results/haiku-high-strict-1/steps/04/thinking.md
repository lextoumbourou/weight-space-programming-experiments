The accuracy fell to 30.8%, and class 1 has become a sink. I suspect the vertical template for 1, which is +1.0 across the center columns, is pulling in any image with strokes there. The horizontal -0.3 seems to cancel out after zero-meaning, since a uniform row gives zero.

The vertical template for 1 looks like the main problem: after zero-meaning it gives center columns +0.5 and outer columns -0.5, so any image with strokes down the middle picks up a lot of positive weight. The horizontal one is zero after centering, so it has no effect. The ink template for 1 does something similar, favoring anything with center-column ink. The hole template only penalizes 1 for digits that have holes, which seems fine, but the vertical and ink terms are what seem to be dragging class 1 into a sink.

The fixed templates are running into their limits. Each new hand-built feature has an unknown scale, and the vertical and ink templates for class 1 are triggered by any digit with center ink. I'm considering whether a hand-tuned linear classifier can work here at all, or whether I should find a more discriminative design, with 12 steps left.

I'm switching to a Bernoulli naive Bayes form: each cell gets a hand-set ink probability per digit, the weight is the log-odds of that probability, and a bias sums the log(1-p) terms. That should handle the total-mass problem that the zero-mean templates keep running into.

I'm weighing a Bernoulli naive Bayes setup: each cell's weight would be the logit of its hand-set ink probability, with a per-digit bias summing log(1-p) to account for expected ink mass. The features are continuous rather than binary, but that's workable. My remaining worry is that a 4x4 ink silhouette may just not carry enough discriminative detail for this to fix the class-1 sink.

I'm considering whether asymmetric kernels could let the channels carry sub-cell position information, since the 4x4 pooled grid alone may be too coarse.

I'm considering conv1 kernels with asymmetric 5x5 windows, so a channel only responds to ink in one sub-region, such as the top-left 3x3, and that could recover position detail the 4x4 grid loses.

I'm considering whether a max-pooled quadrant-sensitive channel could recover sub-cell position, since the shifted windows would each pick up ink in a different part of the pooled cell.

I'm weighing whether 4x4 pooled features can carry enough signal here, since my hand-set templates keep hitting limits. Trying to squeeze finer position detail out of shifted kernels looks too fiddly for the gain, so I'm leaning toward accepting a modest accuracy ceiling and focusing on a more reliable scoring scheme.

I'm switching to a Bernoulli naive Bayes scoring, with per-cell ink probabilities I'd estimate for each digit, so the weight is the log-odds of that probability. The vertical template giving class 1 a huge score is the main failure, and with 1 having high ink probability in center cells and low elsewhere, the bias term would need to absorb a large negative sum of log(1-p) terms.

I'm going to use the probability-based scoring with hand-estimated cell probabilities per digit, so each digit's weight comes from a logit of its ink probability, and I'll check whether that avoids the class-1 sink.

I'm turning the template values into per-cell ink probabilities, roughly +1 mapping to 0.85 and -1 to 0.1, then taking logits as weights and summing log(1-p) into a bias. Since the features are continuous rather than binary, I'm allowing for ink values that come out lower than full strokes, though the ordering should still hold.

I'm weighing a per-cell Bernoulli scoring for the hole channel as well, but its values are small (roughly 0 to 0.5), so I'd need to scale those weights up to keep them from being swamped by the ink terms.

I'm checking whether the naive Bayes setup would still let class 1 win on 8s, since the center-cell probabilities for 1 and 8 look close and the bias terms pull in different directions.

I'm weighing whether to drop the hand-set templates and move to a naive Bayes scheme that uses several channels at once. Ten digits by sixteen cells by five channels is a lot of probabilities to enter by hand, so I'm wondering whether I can generate them from the existing templates with a mapping. I'm also considering a simpler fix, but without data I can't calibrate biases directly.

I'm checking the class-1 template next, since its center-column weights look like they'd score strongly on 8s with their central crossing.

I'm checking the ink template for 1 against 0: the center-column weights tie them out, so the hole template for 1 and 0 has to decide it.

I'm checking the vertical template for 1 next: its center columns come out at +0.5 and the outer ones at -0.5 after zero-meaning, which is a large weight that could push 8s toward class 1.

I'm checking whether the vertical template for 1 is the source of the sink: its +0.5 center and -0.5 edge weights could reward center-column ink from many digits, including 8, 0, and 4. The class-1 score probably gets a large boost from the center columns across rows 0 to 3 for several digits at once.

I'm wondering whether the 1 template's center-column weights are simply too broad: digits like 8 and 0 also have ink in the middle columns, so the sink may come from that overlap. Making the template more distinctive, with strong background penalties on the outer columns, might help, but the zero-meaning muddies that. A per-cell probability model could handle the scale issues more cleanly, if I can define those probabilities sensibly for each channel.

I'm now looking at a Gaussian template scoring instead: the negative squared distance to a per-cell mean reduces to a linear score, since the sum of f squared is the same for every digit.

I'm treating each digit as a prototype of expected feature levels per cell and scoring by squared distance, which reduces to a linear weight plus a bias that penalizes prototypes with more expected ink. That bias should counter the class-1 sink, since its large center-column mass gets a bigger penalty.

I'm treating each digit as a prototype of expected feature levels per cell and scoring by a Gaussian likelihood, which gives a linear weight plus a bias that penalizes prototypes with more expected mass. I want the hole and orientation channels to get their own variance so their scale doesn't get swamped by the ink terms.

I'm mapping each template value to a prototype feature level with mu = clip(0.45 + 0.4·v, 0.05, 0.9), so +1 becomes 0.85, +0.5 becomes 0.65, and 0 stays at the neutral 0.45.

I'm checking whether a Gaussian prototype score avoids the class-1 sink: with a shared variance per channel, the sum of squared features is the same for every digit, so each class reduces to a linear weight on its expected feature levels plus a bias that penalizes prototypes carrying more expected ink. Testing that on the 1 versus 8 case, the center cells for 1 should score well on the 8's crossing, and the bias should hold it back.

I'm working out the score for class 1 on the 8-image, using a Gaussian prototype with a per-cell expected level and an extra penalty for high expected ink mass. The center cells should contribute most of the match, and the sum over the four rows needs to be finished before I compare it against class 8.

Now I'm working out the score for class 1 on the 8-image: the centre cells should contribute most of the match, and the outer cells pull very little. I'm checking the 8 prototype's ring values next.

I'm now scoring class 8 with the same prototype setup, where the ring cells carry most of the expected ink and the sum of squared prototype values gives the bias. I'm working through the per-row contributions to get the total for the 8 prototype.

Checking the 8-image against the 8 prototype now: the linear term comes to about 32, the quadratic penalty about 9.2, giving roughly 22.8, which beats the 1-prototype's 15.6 on the same image.

Checking the 8 score against the 1 prototype: the centre cells are where the 1 prototype is most confident, and the 8's ink there only yields about 6.0, well below the 22.8 the 8 prototype gets.

I'm setting the prototype mapping per channel: ink keeps the 0.45 neutral base, while the hole and orientation channels use a 0.1 base so absent features stay near zero. The quadratic penalty should be fine there, since those prototypes sit mostly at 0.1 and the features they're compared against are mostly 0. I still need to check whether the ink features, which are roughly in [0,1] from the 5x5 pooling, are on a scale comparable to the prototype levels.

I'm settling on a per-channel Gaussian prototype score, with each cell's expected level mapped from the template value, and each channel given its own variance. The next step is working out how the hole and orientation channels should scale against the ink terms.

Now I'm settling on a single variance of 0.2 for every channel, so each channel's weight is its expected level divided by 0.2 and the bias is the squared expected levels scaled to match. That keeps the ink, hole and orientation terms on comparable footing, and the ratio between the linear and quadratic parts works out the same as in the earlier check. I'm also noting that the orientation channel prototypes for 1 still need their centre-cell levels checked.

I'm settling on one variance of 0.2 across all five channels, the ink, hole, vertical, horizontal and slash ones, so their terms stay on comparable footing. The vertical channel's prototype for 1 puts high expected levels on the two centre columns and low ones outside, with absent cells at 0.1. I'm also weighing whether to add a backslash channel for 7 alongside the others.

I'm setting up the hole and orientation prototypes the same way as the ink ones, but with a lower base level so absent features sit near zero, and I'm working out how the -0.5 "no hole" cells should map.

I'm applying the same mapping to the hole and orientation channels, where a raw value of -0.5 or -0.3 just means the feature is expected to be absent, so it lands near the floor, and the cases that clip to the minimum barely change the score.

I'm now setting the prototype levels for the ink channel from the raw template values, leaving out the zero-meaning step so that the centre-column values for 1 keep their sign and size. The outer cells carry the negative expectation, and that gives the same overall shape I already checked against the 8-image.

Checking the mu mapping for the hole and orientation channels now, to see whether their feature magnitudes match the ink terms before I write the FC construction.

Now I'm weighing per-channel weights so that the hole and orientation terms don't swamp the ink term, and I'm settling on a scale factor for each channel that multiplies both the linear and the quadratic parts of its score.

Setting up the prototype templates for each channel, I'm writing out the raw ink values for digits 0 through 3 with the softened outer and centre cells.

Still writing the ink templates for digits 5 and 6...

Still writing the digit 9 ink template...

Still working out the mu mapping for the hole, vertical, horizontal and slash channels, with the ink values using 0.45 + 0.4v and the others using 0.05 + 0.55v.

Switching to a per-channel Gaussian prototype score so the ink, hole and orientation terms are on a comparable footing. I'm writing out the remaining ink templates for digits 5, 6 and 9, then mapping the hole, vertical, horizontal and slash prototypes.

Now I'm settling on the norm correction as the way to offset the ink mass, so the scoring stops favoring digits with lots of expected ink.
