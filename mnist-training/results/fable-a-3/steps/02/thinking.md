Baseline sits at 60% with a loss of 1.64, so now I'm digging into the confusion matrix. The standout problem is class 2 being predicted as 3 (510 cases), and the 3 column looks heavily over-predicted, with a total of 2253 predictions.

Now I'm weighing why the 3 template keeps winning, and whether a negative bias or added discriminative features would fix it. The 2-versus-3 confusion is the hard part: their bottom strokes look alike under blur, and I can't tell yet whether the template mismatch or the real 2s' shape is causing most of the 510 errors.

I'm weighing a per-class bias or anti-template penalties, where the idea is to subtract evidence from pixels a digit shouldn't have, though in plain Euclidean nearest-prototype that term cancels out and only a whitened, variance-aware version would produce it.

I'm weighing a Poisson naive-Bayes style weighting, where each template's log-values become the per-pixel weights and the summed template mass becomes the bias. Under that model, pixels where a digit's template is near zero would get strongly negative weights, which is the penalty I was missing. The catch is that it only works if the scales of the template and the input features line up.

I'm working out why the weighting should work in a Poisson model: the scale factor only shifts the log terms by a constant shared across classes, so only the bias changes, and that leaves one tunable parameter. I'm now writing the Poisson log-template form, where the epsilon sets how hard ink outside a template gets penalized.

I'm asking whether the 3 template's broad, generic coverage makes cosine similarity favor it over many digits, since the 2-versus-3 bottom strokes overlap and the 3 template touches many common features at moderate weight.

Now I'm thinking about which features would separate the digits best, and whether conv2's remaining 12 channels could host explicit detectors for them. The saturated orientation maps at 2-pixel cells might support endpoint detection in several directions, finer orientation maps with a smaller kernel, and convexity cues like right-closed versus left-closed arcs to tell 3 from 2 and 6.

I'm now considering "empty" detectors that fire where there is no ink, with the idea that a saturated presence feature could be turned into an emptiness signal for the classifier.

Now I'm thinking about the Bernoulli-style weighting: if each orientation's presence is binary, the log-odds per pixel would give strong negative weights wherever a digit rarely has ink. I'm considering whether a saturated per-orientation "empty" channel could supply those binary presence features, and how max-pooling over shifted windows would change what the feature actually means.

I'm now turning to features that could separate the confusable digits, especially 2 versus 3, by looking at their geometry. The 2 has a long bottom stroke ending at the lower right and a diagonal in the lower left, while the 3 carries a curve on its lower right and ends at the lower left, so the orientation maps in that region are where the difference should show.

Now I'm checking the orientation cues that separate 2 from 3 in the lower half: a right-side "V" should show up for 3 and not for 2, while a "/" in the lower-left points to 2. The 3's bottom-left arc reads as "\" instead, so that diagonal is the detail to test.

I'm weighing whether a discriminative weighting could help, where each template's weights get shifted to emphasize what sets it apart from the others, though subtracting a shared mean just cancels out. The 2 template itself is uncertain: many real 2s have a bottom-left loop and a curved diagonal, so it may not capture the confusable cases well.

Now I'm noting that a linear recombination of templates across classes just shifts everything by a shared vector, so it changes nothing beyond scale. Any real effect has to come from per-feature weighting, like a metric that downweights high-variance features or a Poisson log-ratio that makes a feature where one template is ten times another count far more.

I'm checking whether the 0 and 6 confusions come from shared left-side strokes, and whether real 0s are rounder or more slanted than my template assumes, since the 0→6 errors are frequent.

I'm checking whether the 4-versus-9 errors come from the missing top closure, since a 4 has no H at the top between its arms while a 9 does. A negative weight on that top H region for 4 would help, but in a cosine setup it stays small next to the other mismatches, so the 4 template's arms may be pulling the score the wrong way.

I'm considering switching to Poisson log-weights, where a template's near-zero pixels get strongly negative values, which should penalize the 4 template's missing top closure against 9. The catch is the bias term, since the summed template mass differs a lot between digits (1 is much lighter than 0), so a 30% scale error could shift the result by tens of units.

Scale mismatch could shift the bias by tens of units, which is risky. Normalising each template to sum to 1 would make it a probability distribution over stroke locations, so the scale problem goes away, and a multinomial naive Bayes score could replace the bias term.

I'm considering a multinomial naive Bayes variant: normalize each template to sum to 1 so it becomes a distribution over stroke locations, which removes the scale problem, and score with log-probabilities plus a small smoothing constant. That keeps the scale-robustness of cosine while letting missing ink in a template's empty bins count as strong negative evidence.

Checking the multinomial version against the 7-versus-1 case: 7 puts about a third of its mass on the top bar, where 1 has almost none, and about two-thirds on the stem, where 1 concentrates its mass. Whether the stem term outweighs the bar penalty depends on the smoothing constant, so I need to compute the actual log-ratios before trusting the naive Bayes score.

Checking the 7-versus-1 case under the multinomial score, the bar penalty for class 1 outweighs the stem gain, so 7 still wins by a small margin per unit of mass. The real question is the smoothing constant ε: too small and any unexpected ink is punished harshly, which would favour whichever template is narrowest.

I'm weighing whether averaging several real examples per class, which blurs the templates, would counter the broad-template bias that the multinomial log score seems to favour.

I'm weighing whether to fix the features or the classifier weighting first, since the 60% baseline suggests the single blurred prototype match is the weak point. A trained linear classifier on these 64 features would likely do much better, and the confusion matrix is the only real data I have to adjust biases and pairwise features with.

I'm thinking about what a manual coordinate descent over the 48 steps would look like, with the feedback from the confusion matrix guiding each adjustment. Then I'm sketching a feature set at the 4x4 level, built from things that hold up under deformation: where strokes end and which direction they point, coarse orientation presence, how many strokes get crossed along a row, and whether there are closed loops or holes, which I'd try to detect with a 5x5 convolution on the pooled map.

Working through the ring detector: I'm checking whether a 5x5 convolution on the pooled map can tell a real loop from a single missing side, since a plain sum over each side could let one strong side hide a gap on the opposite side.

I'm checking whether a 5x5 ring detector can work with saturated side inputs: since each side's contribution is capped by its kernel weights, requiring all four sides to be present acts like a logical AND through a threshold. The catch is that fixed-size rings only fit loops of certain dimensions, so I'd need orientation-specific side detectors to handle the range of loop sizes I'm likely to see.

I'm working out how to make the ring detector tolerate different loop sizes by letting each side use one of two rows or columns, with weights scaled so a single stroke still contributes about one unit. That gives rings a range of heights from about 4 to 8 pixels, with inner holes roughly 2 to 6 pixels wide.

I'm checking whether the loop detector can cover the common digit loops: a 0 is too tall for a small ring, while 6, 8, and 9 fit only at the edge of the size range. Loops are also rounded, so the straight top and bottom sides miss the curved corners, and I'm weighing whether to add diagonal corner channels, though requiring all eight parts would be too strict.

I'm weighing whether a coarse 4x4 feature for the top closure, checking for a horizontal stroke around y≈7–9 versus the crossbar near y≈14–16, could separate 4 from 9 without needing a full loop detector.

Checking how much the key top-closure feature actually contributes to the score for 9 compared with the rest of the template mass. The weight looks small, since the arc's top contributes only a few units against the whole template's total.

I'm weighing a move to log-weights in a multinomial naive Bayes style, since that would give explicit negative evidence where a template has no ink, such as the 4's empty top. I'd also widen the template, both in orientation and in position, to absorb natural variation, and perhaps tune class biases from the confusion matrix.

Now I'm working out the scale of the log-multinomial logits, since the right α depends on how large the total feature mass ΣF actually is. The loss of 1.64 at 60% accuracy hints at moderate confidence, though I can't pin down the feature norm from that alone, and if it's twice my estimate, the margins would blow up.

I'm settling on α around 0.02–0.025 for the log model, since the effective per-feature weight should roughly match the cosine version's range. I'm also weighing whether changing the classifier type and the features at the same time will make it hard to tell which change helped.

I'm looking at the first-row errors next: 1s getting called 7s and 2s, which suggests my upright-leaning 1 template misses the strongly slanted ones. Widening the 1 template's slant range, so it covers both vertical and "/" strokes, could fix that without touching the other classes.

I'm reasoning about why 7s get read as 9s: the bar's hooked end can look like a loop's left side. The 9 template has ink in the upper-left loop and the middle, while a 7 has none there. Under the multinomial model, 9 spends probability on those loop bins, so its stem and top bins end up weaker than the 7's, which is the trade-off I need to keep in mind.

Now I'm checking whether the 2s that look like 3s are the ones with a bottom loop, since their lower-left stroke and middle horizontal could be pulling mass toward the 3 template.

I'm checking whether the 2s that get mistaken for 3s have a more curved diagonal, since that would pull their mass toward the 3 template. My straight-line 2 template sits at about 51° from horizontal, so it mostly hits the "/" bin and only weakly the vertical one, and a slant of 0.12 would shift that balance.

I'm checking the 2-versus-3 distinction at the lower right: a real 2 has an empty right side there because its diagonal has shifted left, while a 3 fills that region with its lower bowl. A 5 has a bowl there too, so that region is a useful feature for separating all three.

Now I'm checking the lower-right region: a 3, a 5, and several other digits have ink there, but a 2's diagonal has shifted left, so that area stays empty. Using log-weights means that empty region mainly rules out the 2 template rather than helping it win.

I'm weighing a Bernoulli presence model, where the absence of a stroke counts as evidence. A 2 has no ink in the lower-right region, while a 3 or 5 does, so that empty region could separate them.

I'm switching from presence counts to a Bernoulli model, where each window gets a binary on/off feature and an empty window counts as evidence against a class. Then I'm weighing how to set the presence threshold, since it's unclear how much stroke mass a window needs before it counts as present.

I'm now working out the presence threshold for the Bernoulli features: a window counts as saturated once it holds about 3.5 pixels of a given orientation. Taking the max over the pooled positions means a feature is absent only if every shifted position lacks that stroke, which makes the absence window narrower than the plain count window.

I'm checking the presence-window widths for the E channels: within about 2 pixels the cell reads as fully present, falling to half between 2 and 4, and zero past that. Taking the min over the four shifted pooled positions makes the absence windows sharper than the plain count windows.

Now I'm thinking about using a Bernoulli presence model on top of the count features, where each window is simply on or off, so that an empty window counts as evidence. I'd combine it with the existing logits as a product of experts, then work out how to turn template stroke amounts into presence probabilities for each class.

I'm settling the Bernoulli weights: with q around 0.85 for present and 0.1 for absent, each feature contributes about ±2 to ±2.4 in log-odds, so a dozen or so mismatches would push logits apart by tens. That points to a scale of roughly α_B = 0.05–0.1. The open risk is the E channel: where there's no ink, E sits at 1 everywhere, so the fully-connected layer just gets a constant contribution from its weights, and I need the weight and bias to be set so that constant behaves correctly.

I'm weighing whether to keep the cosine count features, which reached 60%, alongside a new Bernoulli presence model. The presence model could add negative evidence, so an empty lower-right region counts against the 3 and 5 templates, and I'm considering how to combine the two.

Now I'm thinking about whether a few more features with elongated shapes could help: a long vertical-stroke detector, covering roughly 8 to 10 pixels, would respond to the stems of 1, 4, 7 and 9.

Now I'm deciding whether to rely on a simple horizontal or vertical stroke detector, which could be cheap and sharp, instead of adding more complicated features. Since I'm running short on steps, I'll make one substantial change at a time: add the presence channels with Bernoulli template weights, keep the cosine features as they are, and then see how accuracy moves. I'll also make a small fix to the slant of the 1 template, and hold off on a negative bias for 3 until the new model's results are in.

Now I'm sizing the presence threshold: a unit counts as saturated at τ = 2.5 of stroke mass, which works out to roughly 4 px of stroke falling inside the core of the window. A straight vertical stroke through the middle gives about 5.6, while a short corner crossing only gives 1 to 2, so the threshold separates those cases.

Now I'm working out the template side of the presence features: each template's value gets clipped to a presence score, with a kernel that falls off from full weight at distance 2 to zero at distance 4.5, and then I'll set q from that score.

Now I'm settling the Bernoulli scale: I'll set q to 0.12 plus 0.76 times the presence score, which gives log-odds of about ±2 per feature. Each feature that disagrees with a class costs it roughly 2 in log-odds, so around ten extra mismatches push the logits apart by about 20, and I'm weighing whether α_B = 0.1 is the right weight to keep that margin reasonable.

Next I'm settling the Bernoulli scale: with the template presence values feeding q, the weight α_B is around 0.08, since each mismatched feature costs a class about 2 in log-odds. I'll leave the cosine count weight at 0.3. For the confusion, I'm checking whether the 1 template's slant should rise to about 0.25, since 1 is often read as 7 and 2.

Now I'm checking each template against the others, starting with 1 and its slanted stroke. A lean of about 14° puts the diagonal near the middle of the partial range, so that feature shouldn't count for or against 1. For 7, the top horizontal bar is present, and a slanted 1 without that bar would cost 7 a few points. For 4 versus 9, the top bar separates them, and I'm also looking at whether the loop shape of 9s causes problems.

Now I'm checking the 0 template against the 6s: a real 0 has a right-hand stroke at the top that a 6 lacks, and a 6 has a horizontal stroke through the middle where a 0 stays empty, so the presence features should separate those two cases.

Now I'm coding the presence channels: each one sums the stroke mass in a window, with a threshold that saturates at about four pixels of stroke. On the template side, I'm setting the Bernoulli weights from a smooth presence score and tying the scale to roughly ±2 log-odds per feature.

Now I'm checking the presence estimate on a slanted 1: the two centre columns sit within reach of the stroke, so their presence score saturates, while the outer columns come out at zero.

Now I'm checking how the 1 template's vertical stroke lines up with the pooled windows: the stroke at x=13.5 sits two pixels from both of the centre cells, so both should register as present, and I'm working through which unit centres feed into that pooled check.

Now I'm checking which pooled columns the stroke at x=13.5 lands in: it falls into pooled columns 5 and 6, and the unit centred at 10.5 is offset by about 3 pixels from it, so I'm working through how that offset affects the presence check.

Now I'm working out how the pooled columns line up with the 1 template's stroke: the offset from the nearest unit centre still leaves both central columns strongly active, so the presence check holds for a vertical 1. Then I'll look at whether the Bernoulli presence features hold up when stroke mass is thick or scattered.

Now I'm working out the Bernoulli scale, estimating how far each feature's log-odds can push the class logits apart. With α_B at 0.08, a single feature swings about ±0.16, but a class that disagrees on 20 of the 64 features falls behind by roughly 3.2 on an image that matches the other class exactly, which is a workable margin.

Now I'm settling on α_B = 0.08, since it keeps the Bernoulli margin workable without letting a poor model dominate the loss. I'll leave the cosine weight at 0.3, and I'm going to raise the 1 template's slant to 0.25, because the 1→7 and 1→2 confusions likely come from slanted 1s.

Writing the feature-extraction and weight-setting code...

Now I'm settling the Bernoulli scale: the two class log-probabilities combine into a single term, and the leftover constant works out to log(1−q) for each feature.
