The loss is high at 4.77, with class 1 again coming out on top. The templates seem off compared with the real data, and sparse templates keep winning, which pushes everything toward class 1. I'm wondering whether I've got the wrong features active altogether, possibly my conv1 orientation responses.

I'm weighing whether the probes can help: the loss, accuracy, and confusion matrix are the only feedback I get, and with 42 steps left I need to choose carefully. The confusion matrix gives 100 numbers per step, so I'm considering setting each output's logit to a different feature and reading which class wins for each true class, which would reveal per-class feature statistics.

I'm working through a more robust approach than probing with the confusion matrix, which would take a lot of engineering. A pixel-level template idea might hold up better: since the architecture pools down to a 4x4 grid, I could use the 16 channels to encode ink at different sub-offsets within each block, so the final features keep much finer spatial detail.

I'm checking which pixel offsets the 4x4 max-blocks land on across the 16 channels. The starting positions repeat with overlap, and they come out as a set of ten distinct offsets, 2 through 20 in steps of two.

I'm checking how the 4x4 max-blocks line up: across the 16 channels they land on ten distinct offsets, so the pooled grid works out to roughly a 10x10 dilated image. I'm considering whether average pooling would keep more detail than max, since taking the max of each block loses a lot of the stroke structure.

I'm weighing whether the templates are the real limitation, since my hand-drawn digits probably don't match MNIST statistics. I could tune them using feedback, but I'm leaning toward probing the class-conditional feature statistics through the confusion matrix instead, setting one logit to a fixed threshold as a baseline.

I'm weighing whether probing the confusion matrix per threshold is worth the cost, since interference between the class logits would make the readings messy. It's allowed, since feedback is my only information, but it's slow with the steps I have left. I'm turning instead to why cosine similarity on HOG features fails here. Nearest-mean on HOG should do fairly well on MNIST, so my templates probably aren't really class means, and the common confusions of 0 and 8 with 2 point at the top-arc and diagonal shapes of the 2 template.

I'm wondering whether the 0-versus-2 confusions come from my 0 template being too tall and narrow, since real zeros are often slanted, and the "/" diagonals in the 2 template would match those tilted strokes.

I'm wondering whether blending a few hand-described variants into one template counts as averaging over generated samples, since it's still drawing by hand. A small fixed set of slant shifts, like -0.25, 0, and 0.25, would act as a shear-blurred template, which seems more defensible as an analytic construction than as sample averaging, though it's a borderline case.

I'm questioning whether the template approach is the real problem, since 0 keeps getting called 2 even with blurred templates. Maybe the orientation channels respond unevenly, with diagonals reacting more or less strongly than horizontal and vertical edges, and that imbalance could be why the scores keep drifting toward class 1.

I'm going to lean on the column sums from step 7 to correct the bias, using a modest factor rather than a large adjustment, and skip the probing approach. The sums show class 2 at 1815 and class 4 at only 561, which tells me where the imbalance sits.

I'm tallying the per-class counts from the confusion matrix and taking the log ratio of true to predicted totals, which shows class 4 is under-predicted by the most and class 2 is over-predicted by the most.

I'm halving the bias correction to avoid overshooting, since the class 4 and class 2 imbalances are large. Structurally, I want a hole or loop detector in conv2, but a linear layer can't require ink on all four sides at once, so a ring-minus-center approximation is the best I can do.

I'm weighing whether to probe the confusion matrix for per-class feature statistics or just accept roughly 65-70% and refine from there. Each step gives only aggregate feedback, so estimating class means feature by feature would take far too many steps to be practical.

I'm checking whether the orientation channels respond evenly across diagonal and straight edges, since an imbalance there could explain why scores keep drifting toward class 1. My suspicion is that the templates don't match the real responses, and the long along-stroke filter may be part of that.

I'm weighing whether to finish the feature-level approach or switch to a simpler pixel-space template, and I'm leaning toward sticking with the current design. The plan is to first apply a bias correction at half the computed strength and then add a second blur pass to the templates, keeping each change mild. The loss is already reasonable at 1.32, so I'll keep the alpha setting as it is.
