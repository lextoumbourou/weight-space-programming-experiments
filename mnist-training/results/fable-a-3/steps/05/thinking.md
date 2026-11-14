The model reached 69.9% accuracy with a loss of 1.099, and the over-prediction of 1s is now fixed. Class 2 is still badly underpredicted, with only 238 correct and many going to 3 and 8, so I'm looking at the confusion pairs to see where the errors cluster.

The per-digit totals now show which templates are too narrow: 8, 6, 9 and 3 sit well above their true counts, while 2, 7, 4 and 0 fall short. For 2 specifically, I suspect the template forbids strokes real 2s contain, like the looped or wavy base, which would explain the 2→8 confusions.

I'm checking whether 7's and 4's strokes are being forbidden by their own templates, which would push those digits toward 9. The bias shifts for 7 and 9 look like they contributed too. Next I'm turning to the 0→6 confusions, which jumped from 30 to 248.

I'm now checking why the 0 and 6 classes trade confusions, since both templates seem to allow nearly every stroke in the wide brush, so the template shape alone doesn't explain the jump from 30 to 248. The bias change (6 up to +0.2, 0 up to +0.15) and the asymmetric expected-absent cost may be what favours 6 here.

I'm weighing whether to stop tuning the templates by hand and instead measure real feature frequencies from the data, since naive Bayes on those could plausibly beat the current 70%. The probing would cost about 22 steps of the remaining 46, so I'm checking whether I can gather more per step.

I'm thinking about how to estimate the feature frequencies without spending the full probe budget: if each outcome reports one randomly chosen feature's bit, the 10 outcomes could cover five features at once, with each feature sampled from about a fifth of the images.

I'm weighing whether a selector that picks one feature per outcome could cover more features per step, but it would have to be a pseudo-random function of the image, which is hard to build in the network and could bias the estimates. Measuring global scalar quantities like total stroke mass in a row is another option, though it still gives only one number per step. I'm also looking at whether two features with three levels each, giving nine outcomes, would be a better use of the probe budget.

I'm weighing whether to pick which probe cells to measure by asking which of the ten cells holds the strongest ink for each class, since that tells me where the geometry sits, though it gives only indirect information. Measuring the frequency of each feature per class is more direct, at about 30 numbers per step. I could cut the probe count by merging neighbouring cells so each step covers more of the image.

I'm weighing whether to measure feature frequencies directly, which would take about 22 probe steps, against tuning the templates further. The probes would give true presence rates for the 64 binary features, and a naive Bayes classifier built on those might plausibly reach around 93%, though that's an estimate I haven't verified.

I'm weighing whether to measure the 64 feature frequencies directly, which would cost about 22 probe steps, against more hand-tuning of the templates. Naive Bayes on true frequencies could plausibly reach around 85%, well above the current 70%, with the remaining steps left for bias tuning and fixing the pairwise confusions. I'm also checking whether this counts as fair use of the feedback, since it's still feedback-driven improvement.

I'm weighing a cheaper option: fewer probe steps to check sparsity and key geometry, perhaps by using a coarser 4-orientation by 3x3 grid of 36 features (about 12 steps) instead of the full 64. That would give less detail than the 22-step plan, but it would still be more reliable than guessing the templates by hand.

I'm weighing whether to measure the strict presence features directly or try a lenient version instead, since the strict threshold may not be the most informative binary feature to probe.

I'm weighing which probe features to keep, leaning toward the strict presence version since the lenient one would be too blurry on a 20-pixel digit. I'm considering a slightly lower threshold for sensitivity, and checking how a horizontal stroke of about six pixels would respond under the filter's coverage requirement.

I'm checking whether a strictness threshold of 2.5 holds up for a 3-cell-wide stroke, and it does, since the aligned and shifted cases both stay above it. Smaller loops with 4-pixel tops land near the cutoff, so I'm considering lowering it to 2.0 for more sensitivity.

I'm settling on a threshold of 2.0, since small features like loop tops need the extra sensitivity. I also notice that thresholding the soft presence value at 0.5 corresponds to a more lenient cutoff, so for a naive Bayes model I should probably use each class's mean of the fractional values rather than the probability of crossing 0.5.

I'm working out how to make the probe output match how the features get used: the fractional presence values would be thresholded at 0.5 by the probe but used linearly by the classifier, so I need a sharper mapping. The simple ReLU form already keeps values in range, but I still need a way to push it toward a clean step around a chosen threshold.

I'm weighing a sharper feature definition: the probe thresholds the soft presence value at 0.5, which makes it lenient, so a simple ReLU can't produce a clean step. Using a smaller tau would keep the values mostly binary, but it would also pick up tiny stroke fragments that are mostly noise.

I'm settling on τ=2.0 so small features like loop tops still register, and I'm accepting a slight mismatch where the probe's 0.5 threshold and the classifier's linear use of the fractional values don't line up exactly. The mismatch looks tolerable, since images in the borderline band still land on the right side of the evidence.

I'm weighing whether to cut the probe count by measuring fewer features, since each step only yields three binary outcomes and 22 steps is a large share of the budget. I'm checking whether rarely present features can be skipped.

I'm weighing whether a cheaper probe design could work, such as grouping features or first checking which ones are almost never present for any class, so I don't spend steps on them.

I'm now weighing whether a priority-style readout could pack more information into each probe step, since the outcome space is ten wide but I'm only using eight combinations of three binary features.

I'm checking whether a priority-style readout could work, where each probe reports the first feature present. The hazard for each feature is only a clean estimate if the features behave independently, and neighbouring cells are correlated, so the estimates would be biased relative to the marginal frequencies.

I'm weighing a priority-style readout where each probe reports the first feature present, which works well for rare features since later features would otherwise be measured only on an atypical subpopulation. A count-based outcome is the other option I'm considering.

I'm settling on about 22 probe steps with three features each, though I could trim the count by skipping features that seem irrelevant, such as some corner cells. Since the budget is limited, I'm weighing whether a coarser grid would be worth the lost detail, and whether the remaining steps should go to bias tuning afterward.

I'm still weighing whether probing is worth the budget, since measuring the 64 features directly is costly and I'd be relying on feature choices I can't yet verify. One idea is to measure a different subset or group features differently, but I haven't settled on anything specific.

I'm settling on probing rather than trying to shortcut it, since the three-features-per-step design is the best use of the budget. I'll measure the most discriminative features first, like the central cells and horizontal and vertical strokes, and after about eight steps I'll switch to a classifier step that combines the measured values with template-based estimates for the rest. Before spending steps, I still need to pin down the final definitions for the E channel features.

I'm fixing the remaining details: threshold τ=2.0, the taper kernel, and conv1 thresholds 0.45 and 0.75 all stay as they are. For the probe network, I'm defining the logits over three features per step, where each outcome encodes which of the three is present and the logit depends on the signed evidence from their E values.

Now I'm working out the exact weights and bias for the probe: each outcome sets a sign per feature, with G=20 and the two unused outcomes pushed to a large negative bias. Then I'm deciding the order of the 64 features, starting with the central horizontal and vertical cells before going through the rest.

I'm weighing a different probing strategy: packing four features into a single step by splitting the common outcomes, but the resulting marginals would only be known within strata, so that doesn't give clean estimates. I'm leaning toward dropping that idea and looking for a more step-efficient probe design instead.

I'm now considering whether the probe outcomes could act more like a single-choice readout, since if features were close to mutually exclusive, one step would return which feature is present rather than three separate yes/no answers. That would use more of the outcome space, though it would measure argmax locations rather than plain presence rates, so I'm not sure it suits the classifier.

I'm considering a priority-encoder probe over features that are rare in every class, which could measure several marginals in one step with only small bias. I don't yet know which features qualify, though my templates suggest a few candidates, and the set would likely be small, perhaps saving only about three steps.

I'm weighing a hierarchical probe: a priority encoder over nine features ordered by expected frequency, so the rare ones are measured accurately and later ones are measured only where earlier ones were absent. Correlated features within a group could bias the later estimates, but since the classifier is naive Bayes anyway, slightly biased hazards may be acceptable, though the bias could be large for features measured on a small leftover subpopulation.

I'm weighing a hierarchical probe with small-frequency features grouped together, which could cut the step count but risks bias for features measured on leftover subpopulations. The simpler option is three features per step across all 64, about 22 steps total.

I'm considering whether to drop one orientation or the corner cells of the diagonal features to get under the 64-feature budget, though it's unclear which would lose the least. Measuring all classes across every feature may be more than needed, so I'm thinking about a prioritised order with an intermediate classifier check after about eleven probe steps to see whether the loss improves before continuing.

I'm weighing whether to measure the E-channel features directly, and I'm leaning toward keeping to the 64 strict presence features rather than designing new binary detectors like endpoint or hole checks. Those would each need roughly five or six probe steps per channel, which is too costly for the budget.

I'm sticking with the strict presence features at τ = 2.0, since they localise better within the 8-pixel windows. I'm also checking how τ affects the probe: a smaller value pushes E toward binary, but that only matters for the cells whose shift falls below the threshold.

I'm settling on a threshold of τ=1.6, so the strict presence cutoff sits at S>0.8, roughly one full-weight pooled cell of the right orientation in the worst-shift window. I want E to reach zero only when S is at least 1.6, which keeps small strokes like loop tops in play despite some noise risk. I'm still wary of tiny bits at junctions and curve transitions, where the feature could flicker.

I'm settling the threshold at τ = 1.6 rather than 2.5, since the change is small enough to accept. Next I'll order the probe features by orientation and cell, starting with the horizontal ones and grouping them in triples along the same row.

I'm considering a raster-order probe over the H, V, "/" and "\" features, with a possible fourth feature measured only in the strata where the first three are all absent.

I'm considering a priority-encoder variant: if the three rare features are mostly absent, the leftover outcome could be split further, so a fourth and fifth feature get measured only within that common case, adding information without extra steps.

I'm weighing whether a priority encoder could save probe steps: if the first feature is rare, the bias from measuring the second only where the first is absent stays small, so the steps could be shared without much loss.

I'm thinking about choosing a first probe triple of central horizontal features, and I'm not sure the peripheral ones are rare enough to justify a priority-encoder scheme. I'll run one triple first and look at the actual numbers before committing to a layout.

I'm weighing a probe that measures the top horizontal features at (0,1) and (0,2) together, with (1,1) as a possible third, to see which ones separate the digits best. Raster order would avoid duplicates, but a 5-feature hybrid scheme could save steps if the joint triple captures the common features and the remaining pair is measured only where the triple is absent.

I'm weighing a joint probe on the top row, H(0,0), H(0,1) and H(0,2), and I'm treating the 22-step budget as the main constraint, leaving about 24 steps afterward for classifier work.

I'm going to probe the top horizontal row as a triple, H(0,0), H(0,1) and H(0,2), since that keeps the features in raster order. I'm also considering adding extra features inside the all-absent outcome to squeeze more information out of each step, though H(0,3) would be biased there because it's correlated with H(0,2).

I'm deciding to probe the top horizontal row as a triple first, but I'm also thinking about adding extra peripheral features that are far from the triple, like the bottom-corner diagonals, since they'd sit in a mostly-absent stratum and could yield extra information for free, as long as I check their sample sizes per class.

I'm setting the probe triple as the top-row horizontal features, with two bottom-corner diagonals as extra features to measure when the triple is all absent. The outcome encoding then splits the all-absent case into 8 if the first extra is present, 9 if only the second is, and 0 otherwise, and I'm working out the logit for outcome 8 relative to outcome 0.

I'm working out how the extra probe features combine with the triple: if the first extra is present the outcome should be 8, and the second extra separates 9 from 0. To keep 8 ahead of 9 whenever the first extra is present, its weight needs to be much larger than the second's.

I'm checking whether the priority-encoder split inside the all-absent case holds up, since a feature measured there could bias the logits if it's only marginally present. Outcome 8 has to win whenever the fourth feature is present, even with a large weight, and that only breaks down when a feature sits right at the 0.5 midpoint.

I'm setting the outcome weights so the top-row triple dominates, with the bottom-corner extras giving a much smaller, tie-breaking nudge. The big multiplier on the first extra keeps it ahead of the second, and the only risk is a feature sitting almost exactly at the midpoint.

Still working out the probe function and the logit weights for each outcome, with the extra features only acting as tie-breakers behind the top-row triple.

I'm setting the output weights so the outcome for the all-absent triple is decided by the bottom-corner extras: if the first one is present, the outcome is 8, and if only the second is, it's 9. The first extra gets a much larger multiplier so it wins over the second, and the triple keeps enough margin that these tie-breakers can't override it.

I'm mapping the predicted column index to its three bits, where each bit corresponds to one of the top-row horizontal features.
