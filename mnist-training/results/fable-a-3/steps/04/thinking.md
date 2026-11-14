The loss came down a little to 1.0856 while accuracy slipped to 68.3%. Digit 1 is now over-predicted, with about 1737 predictions against 1064 true examples, pulling in errors from 6, 8, 4, 9 and 2. That matches the sparse-template attraction I expected under the Bernoulli model.

The misclassification counts show a lot of mass flowing into digit 1, so the features I'm checking are probably sparser than my templates assume. I'm considering lowering the presence probability to around 0.65 while keeping the absence probability near 0.1, since expected-but-absent features seem to be the common failure.

I'm working through the per-class scores for a "6" image: with 15 of its expected features present, the score for class 6 comes out around −32. I'm now setting that against class 1, which has fewer expected features, so I'm tallying how many of the image's present features match its template.

I'm checking the scores again with symmetric probabilities of 0.88 and 0.12, and class 6 still wins, about −38 against −52 for class 1. That means 6 images can only be pulled into 1 if they have very few present features inside the 1's template, which I still need to test.

I'm reasoning that narrow 6s could look like 1s because their small loop features fall below the threshold for presence, leaving mainly the slanted vertical stroke. I'm also considering whether 8s and 4s that are narrow follow the same pattern, since the 1 class seems to catch anything that lacks its distinctive features.

I'm considering whether the presence threshold is too strict for small features like loop tops and short bars, and whether lowering it would make the model more sensitive to them. I'm also weighing which distinguishing strokes, like horizontal bars or diagonals, separate a 1 from the 6s, 8s, 4s and 9s that keep getting pulled into it.

I'm weighing a lower presence threshold, around 1.2, so that a single stroke segment counts as a feature, but that risks picking up noise from junction blobs. A middle value near 1.8 might balance sensitivity against spurious detections.

I'm thinking about how to make the lenient presence signal: the idea is to add four channels with a shifted ReLU, so that the saturated value min(maxS, τ)/τ can be recovered by subtracting them from the existing count channels.

I'm looking at whether the lenient presence signal, built from a max over shifts with a subtraction, would pick up the horizontal bits in those 6s and 8s that the strict version misses. I'm also wondering if asymmetric probabilities change the margins enough to matter, since the earlier numbers barely moved. Before going further, I want to check whether 23% of the 6s really look that narrow.

I'm looking at why narrow 6s get pulled toward class 1: the bias change alone shifted predictions toward 1, and under the Bernoulli model each unexpected presence in a 1's template costs relatively little. I'm wondering whether a 6 whose loop sits slightly off the template's position gets penalised for expected features that aren't actually there.

I'm thinking about whether the over-prediction of 1 comes from misaligned templates, where a slightly shifted 6 gets penalised for expected features that are absent while the sparse class 1 only pays for unexpected presences. Asymmetric presence probabilities might soften that, but I'd need the true class-conditional frequencies to set them properly. Spatially softening the expected-feature templates, so that neighbouring positions count as partial matches, looks like a more direct fix.

I'm thinking the misalignment problem could be softened by treating expected features that sit next to an actual feature as partial matches, so a shifted stroke costs much less. Under that view, a 1 has a forbidden zone that a 6's horizontal bottom stroke falls into, since horizontal and vertical strokes are 90 degrees apart and so never neighbours.

I'm weighing whether making expected features soft in space, so that neighbouring cells count as partial matches, would keep 4 and 9 apart, and I'm checking where the crossbar's spatial neighbours fall.

I'm weighing a spatial dilation with a smaller factor, around 0.25, since it softens the mismatch without wiping out the 4-versus-9 cue from the top crossbar. I'm also considering whether just rescaling the absence probability would do the same job more simply, and I'm thinking about running a small experiment to estimate the real feature statistics.

I'm weighing a diagnostic step where the logits encode a single scalar quantity into ten thermometer-style bins, so that the argmax reveals a histogram of feature presence per true class. That would let me measure the real class-conditional feature frequencies instead of guessing the presence and absence probabilities.

I'm weighing whether diagnostic steps are in the spirit of the task, since they use the feedback loop to probe the network's feature statistics instead of only optimising the loss. I think it's a fair use of the feedback, because each probe can reveal per-class feature distributions that guesswork can't.

I'm considering whether the feedback can be used for a few targeted diagnostic probes, since encoding a scalar into the ten logits would show per-class feature statistics, but mapping all 64 features that way would take far too many steps. So I'd pick only the most useful summaries, such as total stroke mass per class, to check the mass model, and I'm wondering whether the Bernoulli margins would be worth probing too.

I'm weighing whether a diagnostic probe is worth it, since measuring per-class presence for a few features would cost steps but could show which features really separate the 1s from the 6s, 8s, 4s and 9s. Mapping all 64 features that way would need roughly 21 steps, which is probably too expensive, so I'm considering whether a naive-Bayes weighting built from those measured frequencies would beat my current hand-set templates.

Next I'm weighing whether a few targeted probes are worth their steps, since a confusion matrix can encode about nine values per class in a single run, though full coverage of all 64 features would take roughly seven or more steps. I'm also considering whether hand-set templates could be replaced with measured per-class feature frequencies.

I'm considering measuring the per-class feature statistics with a few targeted probes instead of hand-setting everything, since three features per step can be read from eight joint outcomes. Covering all 64 would take about 21 steps, which is probably too expensive, so I'd focus on the most uncertain or discriminative features for the main confusions.

I'm considering whether a full naive-Bayes approach, with feature frequencies measured through probe steps, would beat the hand-set templates. Covering all 64 features this way would cost around 21 steps, which is probably too expensive, so I'm weighing whether to measure only the most discriminative features for the main confusions instead.

I'm considering whether a few thermometer-style probes could measure each feature's distribution per class, with three binary features per step giving eight joint outcomes.

I'm working out how to wire up the three-feature probe, where each logit sums signed terms for its bit pattern so the argmax reads out the pattern, with the remaining two logits pushed to minus infinity. Before committing 20-odd steps to measuring feature frequencies, I want to check whether the Bernoulli feature definitions themselves are limiting, since the measurement only pays off if the feature set is settled first.

I'm considering a cheaper route: instead of measuring every feature's frequency, I could measure a few shape parameters of real digits per class, like average slant or where the stems sit, and then fix the templates to match. Another option is to read the confusion matrix directly, since the heavy 6-to-1 confusions point to a poor 6 template that I could correct and test.

I'm weighing parallel per-class tweaks instead: each step, I could test one template change for each digit at once, since each class mostly affects its own row and column of the confusion matrix. For example, I could adjust the 6 template's loop, the 8 template, and the 0 template's slant in the same run and read each row's change separately, accepting some interaction. I'm also leaning toward a few targeted measurements of crucial geometry like slant and width later, though those only reveal information about all classes together, not class by class.

Now I'm weighing a cheap diagnostic: a single probe that counts how many features are present across the whole image, binned into ten ranges, to check whether real digits have fewer active features than my templates predict. That would directly test the sparsity explanation for the 1-attraction and inform the asymmetry and threshold settings, and I'd also consider normalising for sparsity instead of probing.

I'm weighing a simpler fix for the over-predicted 1s: a negative bias on class 1 would cut its false positives from 6, 8, 4 and 9, at the cost of some of its own recall. I'm also considering a more sensitive test for strokes a 1 should never have, so that any stray ink in the forbidden zones pushes the score away from 1.

I'm adding a lenient presence channel for negative evidence, so that any stray ink in a region where a class should have none pushes that class's score down more sharply than a strict check would.

I'm working out the lenient presence channel now: saturated count channels would let any stray stroke in a forbidden zone lower a class's score, and that's the principled fix for the over-predicted 1s. Writing the FC weights for the lenient features next...

I'm settling on a threshold of about 1.5 for the lenient count channel, so that a single pooled cell of ink is enough to count as present. The remaining worry is spurious responses at the blobby ends of a thick stroke, which could fire the horizontal filter and wrongly penalise a 1.

I'm settling on a "forbidden zone" penalty: for each class, any pooled ink in a region where its template has none would push its score down, using a wide brush and softened neighbouring orientations so nearby strokes aren't over-penalised.

I'm setting the forbidden-zone penalty weight to 0.3, since a stray stroke lights up several cells and that adds up to roughly 1.5 per stroke. I'm leaving the class-1 bias at −0.1, because the new penalty should already make 1 less attractive. The confusion counts for 3→5, 0→2 and 9→7 are still the next things to look at.

I'm checking the column totals for digits 3 and 5 to see where the 3→5 confusion is coming from, and I'm considering whether trimming part of the 3's bias, from −0.3 toward −0.15, makes sense given how its upper bowl reads.

I'm rechecking the column totals now: digit 5 is over-predicted by about 300 and digit 3 is under-predicted, so I'll lower 3's bias and adjust 5's. Columns 0, 4, 6 and 8 are well under their true counts, while 2 and 7 are over, with most of digit 2's excess coming from 0s. I'm starting to wonder whether slanted 0s are being read as "/" strokes.

I'm checking whether the left-side vertical stroke of a 0 would be penalised under the class-2 template, since the neighbour-orientation softening seems to let it pass, and I'm also looking at where the 0-to-2 confusion comes from.

I'm checking whether real 0s fit the template at all, since a narrower or more slanted 0 would leave its right side unmatched and lose ground to class 2. I could probe the width of 0s directly or just widen the template's don't-care zones and see whether the 0-to-2 confusions drop.

I'm checking whether real 0s fit their template, since a narrower or more slanted 0 would leave its right side unmatched and lose ground to class 2. I could simply widen the template's don't-care zones and see whether the 0-to-2 confusions drop.

I'm weighing a "hole" feature for the 0s, since the 2 template expects centre ink that a real 0 lacks, and a strict Bernoulli penalty would catch that absence. I'm also thinking about whether the lenient forbidden-zone channel could handle the 1-attraction first, as it's the largest excess, and maybe adjust the strict model's asymmetry as well.

I'm setting the lenient channel's threshold and its forbidden-zone weight, with the allowed mask built from a wide count template and softened by neighbouring orientations.

I'm checking how the wide count windows treat a vertical stroke in class 1: at these distances nearly every column still counts as allowed, so the forbidden penalty would not catch stray ink on the sides. The window is simply too broad for a 28-pixel image to separate columns cleanly.

I'm working out how the wide brush and low threshold affect the forbidden penalty: with a broad window, nearly every cell stays allowed, so the mechanism only catches clearly wrong orientations. For the 1-problem that's enough, but to discriminate better across classes I'd raise the allowed-mask threshold to around 2.5, which makes the allowed values fractional.

I'm weighing hand-written rules against the template-derived forbidden mechanism, and I'm leaning toward the template version: allowed masks clipped from the wide count windows, with neighbouring orientations softened to 0.5. A stray horizontal or backslash stroke in a 1 would then cost about 0.3 per fully forbidden cell, and I'm about to check how much a couple of stray pooled cells actually move the lenient presence score.

I'm settling the stray-stroke penalty at 0.2 per pooled cell rather than 0.3, since a small stroke fragment can light up up to nine cells in the lenient presence channel and that would otherwise add up to too large a penalty. For class 1, a few horizontal and backslash fragments would then cost around 3, which is still a meaningful push against over-predicting 1s.

I'm settling on a softer asymmetric Bernoulli probability, 0.10 plus 0.70 times the pixel's template value, so a missing expected stroke costs less than an unexpected one. I'm also starting to revisit the class biases, with 0's nudged up to +0.15 since the new penalty should reshape how 1s compete.

I'm going through the remaining bias values for each digit, nudging several classes up or down. I'm also planning some template adjustments in parallel, starting with 6, where the confusions with 1, 5 and 0 suggest its loop may be shaped differently than I assumed.

I'm checking whether a horizontal bar near the bottom of a 7 would be allowed, since the wide brush seems to treat it as within range, so the template may not separate the two cleanly. That would need a finer distinction than the current windows give, so I'll leave it alone for now.

Writing the lenient-presence code...

Writing the lenient-presence code...
