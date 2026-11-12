The baseline sits at 60%, so I'm looking for gains from more features and better scaling. A lot of the 8s are being predicted as 1, which is 323 cases. The 1 template has few features, and after centering and normalization its weights on the central vertical cells come out high, so images with central vertical strokes score strongly for 1. I'm considering adding class biases, or penalizing features that are absent from a template more heavily.

I'm weighing whether cosine normalization is what favors sparse templates, and considering a constant-baseline version of the weights instead, where each template is shifted by a fixed c around 0.3 so that features an 8 has but the 1 template lacks get penalized rather than ignored. The idea is that an 8 would then score highest on the 8 template and low on the 1 template.

I'm settling on c = 0.35 and α = 1.0, expecting the correct class to lead by a few units. I'm also thinking about lowering the ink channel's weight and giving the 4 and 1 templates softer, half-weight extra strokes for closed tops and slants. Then I realize the −c·Σf term is the same for every class, so it can't change which digit wins.

I'm realizing the −c·Σf term is identical for every class, so subtracting a constant baseline doesn't change the argmax, and the score is really just the plain template dot product. That means unexpected features only fail to add to a class rather than being penalized, which is why large templates keep winning.

I'm switching the scoring to a Bernoulli log-likelihood, with each template entry clipped to a probability and the log-odds weighted by the feature values. The added term Σ log(1−p) penalizes large templates, which is the bias I was missing, and I'll scale the whole thing by about 0.3.

Working out the numbers now: a stroke that lines up exactly with a filter's center column should give a response of about 1, and neighboring columns fall off to roughly 0.54 at one offset. I'm estimating how strong a conv1 line response gets, then how much conv2 blurring adds on top, to see what range the features actually land in before I pick a scale.

Working through the normalized column weights for a vertical line filter, the center column comes out around 0.19 with small side contributions, and I'm estimating a stroke's total response across the taper.

Estimating the stroke response, I'm finding that a thick stroke spanning two columns each side drops to zero because of the negative flank, so the flanks may need softening. A typical stroke should land around 0.5 to 1.0 on conv1, and after the conv2 blur the pooled response for a line through the middle is roughly 2, which is the scale I'll work with.

I'm settling the scale for each channel: orientation features get s=2 so a present feature sits near 1, and the ink channel gets s=3. I'm weighing whether to drop the ink channel, since it's almost always on near a digit, but I'll keep it because it's the only signal for the empty center of a 0. The logit then becomes a γ-weighted sum of the scaled presence times the log-odds, plus the log(1−p) bias, with γ set to zero for now.

I'm settling the constant at γ = 0.3, with present features scaled so they sit near 1, and I'm noticing that the Bernoulli terms make each expected-but-absent feature cost about 3 units. That means classes with many expected strokes only win when those strokes are actually there. I'm also planning to add stroke variants for 1 and 4 at half weight.

Adding the slanted variant for 1 and the closed-top variant for 4 at lower weights, then setting the stroke for 4 to 0.7 as the first step.
