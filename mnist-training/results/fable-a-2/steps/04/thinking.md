The feature responses are nearly flat: the cavity detectors hardly fire, and the changes are small (+45, +21, −12), so the features are mostly zero. My amplitude assumptions for pool1 look wrong, since the real activations are probably below 0.65 or the patterns don't match. I need to measure actual activation magnitudes, so I'm thinking about a probe network that would let me read them out through the confusion matrix and loss.

I'm planning to read out feature statistics by building a probe that maps a scalar statistic into ten bins through the logits, so the confusion matrix gives a histogram per class in one step. Across 47 steps that could measure several key scalars, though a full class-mean of the 256-dimensional feature vector is too many to track, so I'd settle for coarse calibrations like orientation-channel magnitudes and cavity detector responses.

I'm reconsidering the amplitude estimate: MNIST strokes have bright cores near 1.0 with softer edges, so the filter response on real strokes is probably around 0.4–0.6 rather than 0.65, and curved strokes likely come in lower still.

I'm still weighing how to measure the cavity detector responses: lowering the threshold might be needed first, since the sum over cells is a poor stand-in for the max response.

I'm weighing a probe design that would read out the response distribution through the confusion matrix, though the 256-dimensional class-mean is too large to track, so I'd settle for a few coarse scalars; I can also just lower the threshold to around 0.3 and adjust the gain, but that's a blind guess, so I'd rather choose a probe direction first.

I'm weighing a probe that reads out one scalar per step, where a histogram per class would need 64 separate steps to cover the grid features, so that's too slow. I'm considering instead a single probe on the total sum across all orientation features, which would give a coarse calibration of overall activation magnitude.

I'm considering whether the cavity detectors can be made amplitude-invariant by dropping the threshold and balancing excitation against inhibition. Partial wall patterns would then respond in proportion, so the relative strengths still carry information, and a linear readout of that output is close to what the FC layer already gets.

I'm considering a contrast-normalised detector instead: subtract a fraction of the total oriented energy in the window, so it fires only when the pattern's share of that energy exceeds a threshold, which would make it scale-invariant.

I'm working out a contrast-normalised version of the detector: weight the pattern cells against the total ink in the window, so the response depends on what fraction of the energy matches the pattern rather than on absolute amplitude.

I'm checking whether the contrast-normalised detector stays selective, since a single straight stroke in the window would also put ink on the pattern's cells.

I'm checking whether a lone wall stroke could still trigger the contrast-normalised detector, since its on-pattern share might beat the threshold. Comparing the lone-stroke response against the full-pattern response suggests the ratio isn't selective enough, so I'd need a larger inhibition weight to push a single wall's response to zero or below.

I'm checking whether a fully scale-invariant pattern detector can also enforce the conjunction of walls. Each wall on its own matches the pattern, so a fraction-based threshold can't require all of them at once, which leaves an absolute threshold as the only way to get AND behaviour. That absolute threshold depends on amplitude, so I'm considering scaling it by the window's own ink level instead of keeping it fixed.

I'm looking at whether I can skip the full-pattern conjunction and just probe the amplitude instead, since the absolute threshold needs calibrating anyway. A cleaner option may be to zero the conv2 bias and read the max-pooled response directly.

I'm weighing a probe that sums the grid features across all cells and orientation channels, since a per-cell readout would be confounded by multiple active cells. Comparing that total against the sums my template model predicts for each digit should give a per-class amplitude estimate in a single step.

I'm now thinking about calibrating the amplitude by probing a single cell where a stroke is almost always present, such as the vertical stroke of a 1 in the centre, since a sum across cells would be confounded.

I'm now trying to get the amplitude from a single pooled cell instead of a sum, since a sum over cells is confounded. The catch is that a "1" stroke can straddle two cells, so the two-cell sum only bounds the value between one and two times the per-cell amplitude.

I'm now considering a 1-D probe: a kernel that sums the vertical-stroke channel across a row of five pooled cells, so a "1" gives roughly the same response wherever it sits in that span. I'm checking that the final cell at the centre always covers x=13.5, so the readout stays tied to one clean amplitude.

I'm sizing up the amplitude of vertical strokes for the digit 1 by summing the vertical-energy channel along a single row near the centre. For a "1" that row should give one crossing's worth of response, which lets me read off the activation distribution as a histogram over thresholds.

I'm weighing a single 1-D probe that sums the vertical-stroke channel along one row near the centre, so a "1" should give one crossing's worth of response and each digit's distribution can be read off. Then I'm considering whether knowing that amplitude is enough to fix the cavity detectors, since the geometry is still uncertain, and a more direct option would be to lower the threshold step by step and watch how accuracy moves.

I'm weighing whether a data-driven approach, using histogram probes to learn the class-conditional activation statistics and then fit the classifier from them, would beat hand-tuning the thresholds. The feedback from the confusion matrix counts as measurement, so a little calibration this way seems reasonable, though coordinate-wise learning over the 2560 FC weights is far too slow to run within the remaining steps.

I'm thinking about using a global parameter, such as box size, shear, or blur, to build a shared bank of ten template variants that works across all digits. Then the confusion matrix rows would show which variant each true digit matches best, giving the distribution in a single step instead of one digit at a time.

I'm weighing a different way to pick templates: for one digit at a time, I'd score ten candidate variants of its template and let the confusion-matrix row for that digit show which variant matches the real data best. That takes about ten steps to settle each digit's geometry, which is affordable.

I'm weighing whether to treat each digit's template as a weighted mix of ten hand-drawn variants, with the weights set by how often each variant wins on real data. The open question is whether cosine matching against those mixtures would actually discriminate well, since a linear template model may still cap accuracy well below what a trained linear classifier on the same features could reach.

Estimating each class's mean vector directly would take about a hundred linear probes, which is too many. I'm leaning toward voting among hand-drawn template variants instead: the confusion-matrix row for each digit would show which variant matches real data best, and I could weight a mixture by those votes.

I'm weighing whether a cavity-detector approach with calibrated thresholds could fix the confusions between 4/9, 2/3, 5/3 and 7/9, or whether the gain is too uncertain. Before committing to that, I want a cheap calibration of the activation amplitude, so I'm planning one probe on the vertical-stroke energy along a middle row, with thresholds spread from 0.1 to 0.9 to build a histogram.

I'm thinking about using a single 1-D probe along a middle row with nine thresholds, so a lone crossing lands around 0.6 and a double crossing near 1.2. I'll keep the H-channel column sum for later, since I'd rather not change two things at once. I'm also weighing a quick test of the classifier with a lower cavity threshold, which would show direction even if it's noisy. I'll run the probe first, because the amplitude estimate is needed for any threshold choice.

I'm defining the probe's kernel on the vertical-stroke channel and working out which pooled cells feed the final cell at the centre, checking whether a digit 1 at x=13 falls inside their pixel span.

I'm checking that the pooled cell at the centre covers the stroke's position, since a slanted 1 should still fall inside its span. I'll read the vertical-stroke response from that cell, knowing it's a slightly optimistic max over two rows. Slanted 1s should give a weaker response, so the histogram will show a spread rather than one value.

Sizing up the cavity detectors against the misclassified counts: 4s only gained 45 of roughly 870 errors, so detection is under 10%. If the true amplitude is nearer 0.45 than 0.65, real responses land around 0.4 to 0.5, just under a 0.55 threshold. Lowering the threshold to about 0.25 would catch many more, though single walls would then start to trigger false positives. I'll run the amplitude probe with finer thresholds to settle that.

I'm checking the crossing counts expected for a 0, a 1, and a 4 in a row band at the centre, working out whether the walls fall within the pooled cell's span. The main goal is the single-stroke response A for straight strokes, with the other digits giving more complicated counts.

I'm considering whether to compare the measured total energy against the model's predicted total for each class, since the ratio would give the amplitude factor directly. Still, the V-crossing probe is the cleaner route for pool1 amplitude, so I'll use that. I'm also setting up the threshold sequence so each step up in count adds a positive log-odds increment.

Setting the threshold probe's outputs to bins of the pooled response, with ten thresholds spread from 0.1 to 1.1 and a large scaling factor, so argmax counts how many thresholds the response clears. The feature sits at index 5 with bias terms as cumulative sums.

I'm thinking about whether a single combined probe could return two scalars at once, since argmax over a 2D grid of threshold bins would give a coarse joint histogram. A 3×3 split would fit in nine outcomes, though it would trade away resolution on each scalar.

I'm settling on a single scalar probe with ten bins rather than a two-scalar split, since a coarse 3×3 grid would cost too much resolution on the amplitude. The V-crossing along the centre row should still show what a curved zero does, and I'll check the response rows for every digit afterward anyway. I'm writing the probe now and will explain it as a measurement step.
