The combined model reaches about 61% accuracy and a loss of 0.656, which is better than the additive estimate predicted, and its predictions lean slightly toward cat at 52.3%, so I'll nudge the bias by +0.03. Next I'm looking for more signals, either by adding features incrementally or probing them one at a time. Since horizontal versus vertical structure matters so much, I'm wondering whether finer spatial detail helps too, such as vertical edges near the bottom (the legs) versus the top, and whether edge polarity adds anything.

I'm weighing whether to scale the overall weights, since the loss might not be minimized at the current scale, though that test can wait. Next I'm ranking candidate features by expected value: top-versus-bottom spatial contrast and texture look most promising for zero-centred probes, while the fine spots, line orientations, colours, and blobs are better checked with threshold probes. I'm also considering whether adding features to the combined model would be more informative than probing them alone, but a small mis-centring could shift the bias and muddy the comparison.

I'm weighing individual probes against adding features to the combined model: with unknown scale, single probes give a cleaner read on each feature's sign and discriminability. Individually probing the fine-spot feature would be confounded with texture, though, so I'm considering a contrast that subtracts texture, but I don't know the right coefficient yet.

I'm considering a top-minus-bottom texture contrast, guessing that bottom texture like grass points toward dog. Rather than probing it alone, I'm thinking of adding it incrementally to the combined model with a modest weight, since the zero-centred contrast makes mis-centring less of a worry.

I'm going to run individual probes rather than add features to the combined model, since I can't tell the right scale yet and probes give the sign and discriminability directly.

I'm weighing an incremental test: add a top-minus-bottom texture contrast to the combined model with a small weight, so the quadratic penalty stays negligible, and read the sign of the loss change. Either way, the result tells me the direction and rough strength of the signal without needing to know the right scale in advance.

I'm settling on a method: test each feature by adding it to the combined model at a small weight, and read the loss change to see its direction and strength. If the loss drops, I'll scale that weight up toward its estimated optimum and test another feature alongside it, attributing the rest of the gain to the new one.

I'm going to fix the bias at +0.03 as well, since its effect on the loss is negligible and it won't muddy the comparison. I could test two zero-centred contrasts together if I trust both signs, but I can't separate their effects that way, so I'll keep testing them one at a time.

I'm settling on a quick test for the top-minus-bottom texture contrast: add it to the combined model at a small weight and read the loss change. The sign of that change will show whether bottom texture points toward dog, and I'll use a custom row-weight vector, since the usual profile normalization would zero it out.

I'm settling the custom row-weight vector for the top-minus-bottom contrast, since the usual profile normalization would zero it out.
