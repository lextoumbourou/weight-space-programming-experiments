I'm checking the threshold of 12, which looks too low since about 93% of cats and 97% of dogs fall above it. Converting those rates to z-scores gives roughly 1.50 and 1.91, so d' comes out near 0.42. The tails make the Gaussian assumption shaky, but the direction is clear: dogs show higher energy. The loss difference of about 0.05 needs to match the −E[yz]/2 term.

I'm working out the mean and spread of the energy values, using a quadratic in σ and adding a fourth-order correction term so the loss gap matches. That gives σ ≈ 0.45 and a mean z near 0.78, which puts the energy mean around 21.7.

I'm sanity-checking the energy-based estimates: a class-mean gap of about 2.35 and a d' near 0.41, though the tail-based estimate may be off if the distribution is skewed. From there I'm working out the optimal linear weight and the expected loss, which comes to roughly 0.67. Next I want to see how the energy and the other feature correlate, possibly through a combined model to find a candidate below 0.69.

I'm weighing whether to run a combined model with a moderate weight on the second feature, or to isolate energy at the corrected threshold first. Combining them now would confound the two effects, so a cleaner energy-only step seems more useful, since energy looks like the strongest signal.

I'm now weighing a few isolated probes against a combined model, since adding the second feature now would confound the energy effect. Several candidate checks are on the list (color, spatial contrast, brightness levels, orientation, blobs), and I'm considering whether to fold each one into the best model as a small added term instead of testing them separately.

I'm weighing how to estimate the new term's offset and slope, since with only the loss difference and the shift in predicted-dog fraction I can't separate them cleanly. The calibrated baseline should keep the bias-related loss change small, so the change should mostly reflect the added term's effect.

I'm weighing how to combine the isolated probes with a periodically refit model, since the feature groups look weakly correlated. Edge energy looks like a dog-leaning signal, so I'm wondering where in the image it concentrates and whether smoothness pulls toward cats. Brightness might also separate them if cats tend to be darker indoor shots.

I'm weighing a set of isolated probes next: green and blue colour, a bright-minus-dark contrast, warm tones, achromatic images, pink, dark and bright blobs, spot counts, orientation contrasts, and the top-versus-bottom and centre-versus-surround energy differences.

I'm estimating the mean luminance levels for the bright and dark features, roughly 5 and 7 after pooling, though those numbers could be off by about a factor of two. Since my earlier energy guess was low, I'm planning to treat these as rough and robust to threshold errors.

I'm weighing whether to pin down the energy threshold properly before adding anything else, since the tail-based d' could be off. Running energy alone would give a clean candidate, but I'm leaning toward a combined model with energy and the green/blue colour feature, which should be weakly correlated, and checking that the result matches the predicted loss.

I'm weighing whether to test energy alone with fitted weights, which would give a cleaner d' and σ, or to combine it with the green/blue colour feature now. If the combined loss lands near 0.66 it confirms the estimates and saves a step, but a result near 0.68 would be ambiguous, so I'd need to split the components afterward.

I'm now setting the green and blue weights at 0.12 and 0.10 with an offset of about 0.076, reasoning that a heavily green image should push the dog logit to roughly 1.4. I'm also weighing whether a direct test of the combined green-and-blue feature would be more informative than isolating it, since I only have indirect stats for it so far.

I'm weighing whether to test energy alone at the corrected threshold or to combine it with the green-and-blue colour feature, since mixing them would make it harder to attribute any change in loss to one or the other.

I'm weighing isolated probes against a combined model here: isolated probes are cheaper to discard, so I'd rather screen features one at a time and then combine the strong ones, instead of tuning a combined model from the start.

I'm weighing whether to test the green-and-blue colour feature by itself, since I only have rough stats for it so far. The energy stats are also still uncertain, so combining them now would confuse the picture, and I'd rather isolate features and pick the strong ones before merging. Next I'm considering a dark-versus-bright contrast probe, along with a smoothness check, which is roughly the opposite of the energy feature.

I'm considering whether to test the dark and bright luminance features separately, since combining them into a single contrast sum could hide a signal if both point the same way. I'd rather probe dark alone at a threshold near 7 and bright alone near 5, then decide whether the shape features are worth a look at all.

I'm looking at shape contrasts that subtract one shape from its counterpart, like pointing-up minus pointing-down or the vertical versus horizontal edge pairs, since those should centre near zero and avoid the energy signal. Several other pairs fit the same idea: bright and dark blobs, the spot contrasts, and the luminance-level differences. I still need to probe warmth, pink, achromatic, brightness, darkness, and smoothness, plus the top-versus-bottom spatial split.

I'm ranking the next probes by how useful they're likely to be: the upper-minus-lower pointing contrast first, then brightness and energy split by position, then the vertical-versus-horizontal and warm-colour checks. Each isolated probe costs a step, and many will probably be weak, but that's acceptable.

I'm looking at a contrast probe that subtracts the vertical-detector energy from the upward-detector energy over the same profile, so the shape signal is measured without the overall energy term. Both channels should centre near zero, which lets me use a threshold at zero. I'm still working out the weight and the expected spread.

I'm sizing the noise for the upper-profile contrast at about 0.36 and picking a row and column weighting that keeps it comparable to the earlier probe. I'm wondering whether the V shape between the ears, which looks like a background U, could also lean cat-ward, so I'll just measure it and see.

I'm thinking about whether to rank features by likely strength instead of by how interesting they seem, since the weaker ones will cost steps to rule out. Level-type features like dark overall, bright at the top, and warmth look like they could reach about 0.2 to 0.4 in d', so I'll weigh them against the shape contrasts.

Next I'll test warm colour (feature 19) on its own, since my rough guess is that most indoor photos carry a slight warm cast.

I'm estimating the warm-colour feature at a mean of about 6 to 8 with a spread near 4, so I'll set the threshold at 6.5 with a small weight of 0.1, which gives a z-spread of roughly 0.4. I'm picking warm first over dark, since both are about equally uncertain, and I'm not treating the positive sign as meaningful yet.
