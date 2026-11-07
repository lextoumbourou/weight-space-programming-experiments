I'm pushing for more steps while keeping early stopping in mind: the gain has to clear 0.5 points over the last five steps. Accuracy is at 75.04 now, against 70.92 back at step 10. I'm reading the rule as comparing the best result in the recent window with the best before it, and since steady gains aren't guaranteed, I'll try bolder structural changes.

I'm looking at which digit pairs are still getting confused: 5→8 is the worst, followed by 4→9 and 3→5. For structural changes, I could repurpose the 16 conv2 channels, since the second group looks like a shifted copy, or keep the 8 orientations and use finer spatial cells. The 0→2 confusions are puzzling, since narrowing the 0 template made things worse, so I'm considering a wider or tilted 0 variant to test.

I'm weighing whether the 4s that look like 9s point to a problem with the 4 template or with the features, and I'm thinking the blur might be too heavy now that there are variants, so I could try lowering it to 2.5. I also want to test SHEAR, LAMBDA, and OCUT, one change per step, while still meeting the 0.5-point gain needed over five steps.

I'm weighing whether to change the loss or the features, since accuracy is the metric I care about. One option is to make the second conv2 group capture something other than a shifted copy of the first, like ink without orientation for a finer location map. I'm leaning toward topology instead, such as whether a loop is closed, since that could separate 4s from 9s, where stroke endpoints matter.

I'm comparing 5 and 8: the 5's top bar and upper-left vertical resemble the top loop of an 8, but the 5's bowl ends open at the lower left, which an 8 doesn't have, and I'm checking whether that difference is what separates them.

I'm now weighing whether a missing-ink signal could help: a feature that fires when a region is empty, since 5 and 8 differ mainly in what is absent from the top right. A bias-driven detector that goes high when the window has little ink might capture that gap, which the current cosine-based scoring doesn't penalize.

I'm thinking about an "emptiness" feature: a detector that fires when a region has little ink, which could penalize the missing top-right stroke that separates 5 from 8. Since max-pooling over conv2 would keep that signal, I'm considering dedicating some of the conv2 channels to it instead of the shifted orientation copies.

I'm working out whether a detector that fires on empty regions could be built from the conv2 channels, since a "whole region empty" signal would be stronger than what a max over sub-windows gives. A large-window sum over pool1 taps, pooled over 2x2 positions, looks like the most workable version.

I'm thinking about an emptiness detector built from conv2 channels, since 5 and 8 differ mainly in whether a stroke is missing from the upper right. A 3x3 tap version over pool1 might fire on that gap, and I'm considering several variants across the eight channels.

I'm settling on a set of emptiness detectors, using shifted 3x3 and 2x2 tap windows over pool1, so the gaps that separate 5 from 8 can be measured directly.

I'm settling on an emptiness detector: a conv2 channel with negative weights on the orientation inputs and a positive bias, so it fires when a window contains little ink. The idea is to tune the weights so that any stroke crossing the 3x3 tap window shuts it off, which would let the missing top-right stroke that separates 5 from 8 register directly.

I'm working out how to estimate emptiness from the template side: for each conv2 position, I'd sum the orientation ink and turn that into an emptiness value that drops toward zero as ink increases, then take the max over each 2x2 group.

I'm working out how to estimate emptiness from the template side: for each conv2 position, I'd sum the orientation values and convert that into a score that drops toward zero as ink increases.

I'm working out how to weigh the emptiness features against the orientation features, planning to normalize each group's template separately so the missing-ink signal doesn't get drowned out.

I'm considering whether to combine the emptiness features with a weight μ, but normalizing them would give 8 an outsized reward from the corners, since every digit has empty corners. So I'm leaning toward using the raw count of matching empties instead, which means classes with more expected empty regions, like 1 and 7, would receive a larger reward.

I'm checking whether the emptiness reward holds up: a sparse image lets classes with many expected empty regions, like 1, collect more reward, which is fine for a 1 but could also pull in other sparse images. For 5 versus 8, the extra reward for 5 comes from empty regions that 5 expects and 8 doesn't.

I'm weighing an emptiness term with a small scale, around 0.15, so that a difference of about five matching empty regions moves a class's logit by roughly one point. I'm not sure that magnitude is right, since it depends on how the orientation features are scaled, and I still need to check how they combine with the cosine part.

I'm dropping the shifted orientation copies and keeping only the 8 unshifted orientation channels, with the remaining 8 channels reserved for emptiness detectors. That's a real loss on the orientation side, but the emptiness features might more than make up for it, so I'll go ahead and see.

I'm now splitting the emptiness channels into two sets: four 3x3-tap detectors at shifted positions over pool1 (channels 8 to 11), and four 2x2-tap detectors covering a 4x4 pixel area each (channels 12 to 15), for finer resolution on where ink is missing.

I'm working out how to calibrate an emptiness value for the template: a 3x3 tap window spans about 6 pixels, a stroke crossing it contributes roughly 2.3 in summed orientation membership, and I'm considering a clip of 1 minus that ink over 1.0.

I'm working out how a crossing stroke should drive the emptiness value: the template estimate would be roughly half the summed orientation value, clipped at zero, so a stroke crossing the window shuts the detector off. I'll take the maximum over each 2x2 group next.

I'm settling on how to combine the two feature groups: the emptiness channels will be averaged across variants rather than summed, while the orientation channels stay summed, and the orientation weights will only use the unshifted windows. I still need to decide how the emptiness weights should be scaled and whether the biases from before still hold once the emptiness offsets are added.

Writing the conv2 weights in code now...

Writing the conv2 weights in code...

Still writing the template windows and orientation helper...

Now I'm working on the feature-layer details: normalizing the orientation and emptiness channels to the same scale before I wire up the fully connected weights.
