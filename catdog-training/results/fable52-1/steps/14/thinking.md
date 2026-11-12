I'm working out the step-13 result: reversed luminance gives +0.0014 over base, and the forward step gave +0.0075, which lets me solve for the curvature and linear terms.

Now I'm pinning down the reversed-luminance gain, which comes out to only about +0.0005 and is marginal. Next I'm listing the feature channels I haven't used yet, and I'm thinking about whether the shape and spot channels are likely to add anything beyond edge energy. I plan to probe spatial profiles of edge energy and luminance, comparing top against bottom and centre against border.

Now I'm weighing whether the remaining scene features can give any real gain, or whether the per-step measurements are the real limit. Each probe I run should target one spatial pattern, so I'll pick coarse profiles of edge energy and luminance to cover the main directions.

Next I'm considering a coarser-scale energy measure, perhaps the ratio of fine-scale edge energy to large-scale gradient, since that might strip out overall lighting contrast and sharpen the signal that edge energy alone gives.

I'm thinking about whether the smooth-cell fraction on top carries any signal, since its weight could be negative if smooth regions point toward cat. I'm also considering scaling the whole model's weights down by about 0.85, which I'd expect to give roughly 0.001, though that gain is getting small. I want something that could bring 0.005 or more, so I'm looking past these per-step tweaks.

I'm thinking about whether the animal's own colour could separate the two classes, since cats come in grey, black and white while dogs also run to tan and brown. The warm-tone signal already showed up in the overall measure, so the open question is whether it is stronger in the centre, where the animal usually sits, than at the border, which tends to show background. I'd expect the centre to be more dog-like, but indoor wood floors could muddy the border comparison.

I'm considering whether the eyes could serve as a cat signal: a dark pupil inside a bright iris, with a dark fur outline around it. At this resolution the eyes would be only a few pixels across, and for dogs the same spot would be a plain dark blob in lighter fur, so I'm not sure a detector could separate the two.

I'm sketching out a few ideas for detecting eyes and nose, but a dedicated detector would need several steps to test and probably wouldn't beat the simpler channels, so I'm leaning toward cheap spatial probes instead.

I'm comparing a few ways to combine the spatial probes: two steps with opposite signs on one channel isolate its gradient, but the sum step confounds the other channel with the quadratic term. Three steps cover all the gradients, and single-sided probes with estimated quadratic terms would take only two.

I'm working out how much variance the contrast features have, since that sets how big a step to take for the curvature term. The edge-energy total gives a usable reference, and I'm treating each cell's variance and their correlation as unknowns that I'll need to estimate.

I'm checking the variance estimate for the contrast features, which comes out to about σ ≈ 1–1.5, so a probe at ε = 0.06 gives a usable curvature term. Since that term is only uncertain by about a factor of two, I can still read the sign of the gradient from the measured change. I'll run the four spatial probes in order: centre-minus-border for W first, then top-minus-bottom and centre-minus-border for E, and finally top for W.

I'm considering whether the vertical-versus-horizontal edge energies, rather than their sum, separate the classes better, since vertical structure like legs and fences might point toward dog. I'd put that at about 60% odds, so I'll probe the difference between the two orientation channels with a step of around 0.07, similar to the diagonal test.

Now I'm setting up the next probe: a centre-minus-border contrast on the W features, with the centre cells weighted +1 and the border cells weighted −9/16. Working through the variance, it comes out to roughly σ ≈ 0.8 to 1, which is enough for a usable curvature estimate.

I'm settling on the luminance change: rather than folding it into this step, I'll keep the base at the step-12 model exactly, with the pink term at zero, so the centre-minus-border result stays clean. At ε = 0.08 I expect a contrast-driven shift of about 0.06–0.09 in the feature, and a positive sign would mean the centre is warmer than the border, which points toward dog.

I'm settling the base for the next probes: I'll hold the model at the step-12 weights, with the pink term at zero, so the centre-minus-border result stays clean, and I'll fold the learned tweaks in later in one consolidation step.
