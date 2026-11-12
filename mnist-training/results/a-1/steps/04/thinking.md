Eight is now dominating with the logits too large, and the alpha values that work fall between 0.3 and 1. Step 1 at alpha 1 pushes everything to 1, though. What stands out is that 7 never gets classified as 7 and 4 never gets classified as 4, which points to template misalignment or a wrong orientation definition. I'm wondering whether swapping '/' and '\' would explain it, since a 7's diagonal would then mismatch.

I'm checking the diagonal direction for the 7 against the filter definition, and the orientation comes out consistent with the dot-product template tuning. I'm also confirming that the convolution uses cross-correlation indexing, so there's no hidden flip. The thick MNIST strokes should make max-pooling reliable, which leaves the blurred, overlapping templates as the more likely culprit.

I'm now weighing whether the templates themselves are the problem: since they're all positive and overlapping, a 7 input lines up with the 9's top stroke and stem, and bigger templates win unless α penalizes them. At α=1 everything collapses to class 1 because its small norm gives it the smallest penalty, so the positive-only setup has no real way to penalize the wrong classes.

I'm noticing that centering the templates by subtracting a shared mean wouldn't change the argmax, since it just shifts every class's logit by the same amount, so only the per-class bias and template shape matter. The cosine version, which normalizes by template norm, still seems to favor 8, so I'm considering dividing by the norm raised to a power between 0 and 1, or adding a bias term.

I'm considering whether sharpening the templates with a smaller sigma would make them more distinct and reduce the dominance of 8. I'm also noting that a linear one-template classifier only allows per-class scaling and bias, since any shared penalty term shifts all logits equally, so the template shape and per-class bias are what can actually change the outcome.

I'm considering whether centering the templates and normalizing by their centered norm would emphasize what sets each class apart, since 8 stays positive over most of the image. I'm also looking at the step-2 confusions, where 4, 2, and 9 keep getting pulled toward 8.

I'm checking whether the 7 and 4 misclassifications come from the template shape or from thick MNIST strokes, but the stroke thickness looks fine for max-pooling. I'm also questioning my hand-built 7 template, since its slant and bar placement might not match how real 7s are drawn.

I'm thinking about whether the detector responses might be too broad, since a diagonal filter also picks up nearby cells with partial weight. I'm also considering that a per-class bias, tuned against the confusion counts, might fix the 8 dominance more directly than changing the template shape. The cosine-normalized version still looks like the best starting point to build on.

I'm now looking at the per-class counts, where 8 is over-predicted and 4, 5, and 7 are under-predicted. I'm weighing whether to center and normalize the templates, sharpen them with a smaller sigma, and apply per-class bias adjustments, though changing several things at once will make it harder to tell which helped.

I'm wondering whether centering the templates and normalizing by the centered norm would help the 8 problem, since the centered 8 template is positive over a broad area but its norm is hard to predict. I'll try it.
