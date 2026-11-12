Zero-sum weights made the one-class template dominate after double centering. I'm now reconsidering why: the features are mostly background zeros and only active where strokes fall, so sparse templates end up with a large positive region and small negative values elsewhere.

I'm now sanity-checking how strongly the background zeros shape the templates, and considering a nearest-centroid rule with a scale factor α matched to the feature magnitudes. To pick α, I'm estimating typical conv1 and pooled responses for a stroke of about 2–3 pixels.

I'm estimating the feature scale α at about 0.4 from the conv and pooling responses, and I'm going to use the raw, unnormalized templates instead of unit-normalized ones. The nearest-centroid logits then depend on squared template distances, so I'm working out how the scale factor s and the template norms ||T||² set the margin between the true class and the others.

I'm weighing whether nearest-centroid with a tuned scale can work, since that would be template matching with a penalty on large templates. Without knowing the true feature scale I'll treat the scale parameter as something to tune, which handles the earlier issue more directly than double centering did.

Cross-class centering turns out to do nothing, since shifting every row of the weights by the same vector changes all logits equally and leaves the softmax unchanged, so the normalization was the part that mattered. I'll switch to a nearest-centroid rule with α around 0.4 and a scale of about 12, keep the slanted-1 template, and skip any extra bias term.
