I'm settling on 8 for now, since it has the most ink and so the least penalty, but these are uninformed guesses. I need feedback to calibrate them properly. I'm considering using the confusion matrix as a measurement device, where the network's outputs act as probe features and each row shows which probe is most often maximal for that class. That gives a distribution of winners rather than the means I actually want, so I'm looking for a better way to extract the information.

I'm considering threshold probes next, where each output reads whether a feature crosses its own threshold, though that isn't guaranteed to isolate one feature at a time. A quantizer could give class-conditional histograms instead, but the real problem is that I can't get gradients for all 2560 parameters. Maybe the more useful check is whether my model of the conv1 orientation filters is wrong, since they may respond to stroke edges at several orientations and blur the features together. I'm working through the horizontal filter's response to a vertical stroke, combining its profile with the taper weights.

I'm checking the vertical stroke response for the horizontal filter: with all five rows inked, the centre column gives about 0.15 after subtracting the mean, and a three-wide stroke drops to about 0.29. Next I'm working out the normalisation, summing the positive contributions from the centre row and the two adjacent rows at each taper weight.

I've checked the horizontal filter against a vertical stroke and a horizontal one, and both come out as expected. The vertical stroke nets to roughly zero after normalisation, while the horizontal stroke gives the full response of 1.0. A uniform blob also scores zero, so the filter looks selective.

Thick strokes look like the weak point here: a width-5 stroke sums to roughly zero on the horizontal detector, and width 4 only reaches about half the response. Since real digits often have thicker strokes than my template assumes, I'm considering a filter with a narrower negative surround so that thick strokes aren't penalised as heavily. I'll also look at edge-based features as an alternative.

I'm now weighing edge-based features: a first-derivative, Sobel-style detector for each of four orientations, with both polarities kept as separate channels so thickness doesn't wipe out the response. Polarity should also show which side the ink sits on, which helps with shapes like the outer edge of a 0.

I'm settling on combined edge-orientation channels, summing both polarities within each 3x3 cell, so the template is essentially one orientation energy per direction.

I'm now shaping the edge filter itself: an odd derivative profile across the stroke direction, normalised so a clean step edge gives a response of 1, with a small bias subtracted. Because it keys on both sides of a stroke rather than its full width, thick strokes should still produce strong responses.

I'm checking whether dropping the ink channel leaves enough information, since the edge channels should carry the stroke presence implicitly. The templates will just sum both polarities per orientation, with the perpendicular offset smoothing things a little. I suspect thick digits were the main source of near-zero features, so this change should help more than tuning the scoring.

I'm defining the edge filter as an odd derivative profile across the stroke, normalised so a step edge gives 1, and I'm keeping the two polarities as separate channels.

I'm setting each orientation's two polarities up as separate channels, then summing them with a 3x3 convolution so each orientation gets one energy value. The template matching step stays as it was, since the edge detectors already track stroke direction closely.
