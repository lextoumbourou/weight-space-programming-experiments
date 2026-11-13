The error list is still long at 77.8%, with the largest misses in pairs like 0→2, 2→8, and 3→5. The orientation-template naive Bayes looks like the weakest piece, and I'm starting to check what's driving it.

I'm weighing whether to measure the orientation features' class-conditional rates through diagnostics. That would take far too many steps to do for all 64 features, and it starts to look like fitting the naive Bayes by hand. I'm leaning toward using a few aggregated diagnostics only to check whether the templates are miscalibrated in specific regions, which is ordinary debugging.

I'm looking at the biggest error pairs now, and zeros bleeding into 2s and 5s stands out, about 156 misses combined. My zero template is an ellipse with sides around columns 7.5 and 19.5, and I'm checking whether real zeros are wider or sit differently than that, since 2 and 5 share top and bottom horizontals.

I'm checking whether the orientation templates are miscalibrated, weighing a single probe that compares how much each orientation's features fire against what my rendering model predicts, to tune the tuning width and window instead of hand-fitting weights.

I'm considering whether to calibrate the template model by comparing a per-class total of feature activations against measured values, which would let the code rescale the templates rather than fitting weights by hand. I can't run code myself, so any such comparison would have to be built into the program.

I'm weighing a full measurement of the features against the cost in steps: 64 features would take about 22 probes, and fitting naive Bayes from measured rates is close to hand-training, which seems to cut against the spirit of the task. The designers likely expect iterative improvement from the feedback, but I'm not sure a probe-based calibration counts as legitimate, so I'll keep the diagnostics sparing.

I'm weighing whether diagnostics that measure the features' class-conditional rates count as fitting the weights by hand. I'm leaning toward keeping the probes to a few aggregated checks on specific template hypotheses, like where real 2s put their stroke mass compared with my template, and then redrawing the strokes myself.

I'm considering a cheaper route: tuning the bias terms from the column sums, and maybe leaning on the hole feature and the template scaling parameters instead of probing every feature.

I'm comparing 3s and 5s now. Their lower halves look nearly identical, so the difference has to come from the upper strokes: a 5 has a top bar and a left stroke that drops from the top, while a 3 has a top arc and a short upper-right stroke.

I'm comparing the upper-left strokes of 3s and 5s. A 5's vertical stroke there leans toward "/" at a steep angle, while a 3's top arc curves up-right from its left end, so both carry a similar diagonal in that cell. My current 3 template starts its upper arc too far inward, so it misses that stroke.

I'm comparing the upper-right region of 3s and 5s now. A 3's upper bowl has a stroke running down-left from its right side toward the center, while the same area in a 5 stays empty, and its bowl begins lower, near the middle.

I'm now comparing where the strokes sit for 3s and 5s: a 5 has its stem on the upper left, while a 3 has its diagonal on the upper right, and I'm working out how the center of mass shifts their positions.

I'm working out how the 3s that get misread as 5s might differ from the usual 3, perhaps with a flat top bar that angles down to the middle rather than a bowl with a stroke on the upper right, which would explain why my template misses them.

I'm weighing whether a few targeted probes of the template model are worth the cost, since they would shape the templates by feedback rather than hand-fitting weights. Setting that aside, the next lever is the template shapes themselves, and I'm considering whether re-tuning the clip channels could free up capacity for more useful features.

I'm thinking about whether a few targeted probes could reveal stroke layout for the 3-versus-5 confusion, such as checking for a vertical stroke in the upper-left versus the upper-right. I'd be weighing that against the cost of measuring each feature, since probing reads out only a small amount of information per step.

I'm noting that the 9 remaining probes would only give a few features per step, so I'm weighing whether a priority-encoded readout could recover marginals for more features at once, but it only works if the features are roughly independent. Measuring around three features per probe means about 22 steps for all 64, which would leave little room for tuning.

I'm now considering whether a few targeted probes could measure the key discriminative features for the top confusions, since full measurement of all 64 would cost about 22 steps, and I can only read roughly three features per probe.

I'm considering a different probe: give the ten outputs ten alternative hand-drawn variants of one digit and see which variant real examples of that digit match best. Each step would test ten candidate shapes at once, which is far more efficient than measuring features one at a time.

I'm now thinking about using a set of hand-drawn variants per digit and seeing which variant real examples of that digit match best, so the win counts reveal the style mix. Testing several variants at once would be much more efficient than probing single features, and the resulting mixture could feed a naive Bayes model.

I'm thinking about how to split the probes across digits: either five steps with five variants each, or three to four variants per digit with three digits per step. The variants would cover the main style questions, like whether a 2 has a loop, whether a 3 has a round or flat top, and whether a 9 has a straight or curved stem. I'd also like to test global parameters such as shear and aspect ratio, starting with a few shear values for the digit 0.

I'm weighing a "variant tournament": hand-draw several alternative shapes per digit and see which one real examples match best, which would reveal the style mix. The final naive Bayes would then use mixture-averaged probabilities, which should approximate the true marginals better than one drawing, maybe reaching 83–85%, though that's uncertain. Direct measurement of the probabilities would take about 22 steps and could reach higher accuracy, but it costs much more.

I'm weighing whether to measure class-conditional probabilities directly from feedback, but that amounts to training a naive Bayes model from data, which the task rules out. Instead I'm leaning toward hand-drawn variant tournaments, where each probe tests several alternative stroke shapes for a digit and the win counts show which styles real examples favor. The hand-drawn strokes stay the source of the weights, so this is still in the spirit of the task.

I'm planning to run "variant tournaments" next: for each digit, I'd hand-draw several alternative shapes and see which one real examples of that digit match best, starting with a few global parameters like slant and width on the zeros.

I'm sketching a few "variant" probes: for the digit 0, testing scale and aspect combinations, and for the digit 1, testing slant and length, so the win counts can calibrate the geometry that every digit depends on.

I'm weighing a pair of probes: a digit-0 set that varies scale and width, and a digit-1 set that varies slant, to see which variants real examples favor.

I'm weighing whether to probe the 2, 3, and 5 templates one digit at a time for higher-resolution feedback, or to combine easier digits, with about 45 steps left and room for roughly eight probes. I'm also questioning whether template fidelity is really the bottleneck, since true marginals on the 64 features might only get to about 85%, against our current 77.8%.

I'm sketching hand-drawn variants for the digit 2, such as a looped bottom-left stroke, a narrower version, and one with a swash at the base. For the digit 3 I'm considering a flat top, a longer middle bar, a more slanted shape, and a smaller upper bowl.

I'm thinking about cheaper ways to improve robustness, like testing a blur level on the templates or a different sharpness parameter in a normal classification run, since each of those is a single step with a direct accuracy readout. I could also vary the overall scale (SKEL) across all digits at once, which avoids building per-digit tournaments.

I'm thinking about whether broad knob sweeps, like scale, shear, and blur, are worth a few steps before per-digit tournaments, since each one gives a direct accuracy readout. A variant tournament across knob settings could also show which setting best fits a simple digit like 0.

I'm going to run a tournament over global geometry instead: scale, aspect width, and the baseline shape, using the digits 0 and 1 since their simple forms should show the geometry effects cleanly.

I'm now going through the slant options for the digit 1: 25°, 38°, and a left-leaning −12° to cover the less common writing style. The stroke length can stay at the same value, since slanted strokes still fill the same 20-pixel height.

I'm settling on a first probe that compares several sizes of the digit 0 and several slants of the digit 1, since the 0's scale and the 1's slant should inform the geometry used for every digit. I'm also considering a combined probe on the hard digits, but I'll start with these cleaner shapes.

I'm planning a tournament scoring setup where each variant's naive Bayes score is computed from its per-feature probabilities, with the zero-digit row as the main signal and the other rows treated as noise. The implementation would treat each variant as a class, with the hole channels zeroed out.

I'm setting up the digit 0 variants as arcs with a few radius and offset choices, and the digit 1 variants as slanted strokes at 12°, 25°, 38°, and −12°. The 38° stroke is still height-normalized, so it fits the same box. I'm also weighing whether five variants per digit is the right budget, since slant looks like it matters for the zeros too.

I'm settling the probe design: I'll scale the zero variants and aspect ratios on the zeros, while the slant comes from the one variants' result, since writers' slant tends to be shared across digits.
