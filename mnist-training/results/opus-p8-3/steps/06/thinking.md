I'm moving to loss 1.1 and checking the persistent confusions, mainly the 160 ones being read as sevens. My guess is that the slant of those 1s lines up with the stems of my 7s, which is why the network keeps making that mistake.

I'm weighing a fix for the 1→7 confusion: one option is to boost the top bar weight for the 7 template, another is to penalize features that appear in 1s but not in 7s. I'm also considering a discriminative weighting scheme, though working through the linear algebra suggests it reduces to a per-class rescaling plus a shared offset, so it may not change the decision boundary the way I'd hoped.

I'm weighing a per-class scaling or a per-feature reweighting for the 7 template, since a uniform shared offset only rescales the scores. Emphasizing the top bar of the 7 template would target the 1→7 confusion more directly. I'm also thinking about downweighting features with high within-class variance, though for now I'll keep the weights uniform.

I'm considering normalizing each class template to unit length and then scaling, so that large templates like 8 and 0 don't dominate the scores. The idea is that cosine-style weighting could change the relative scale per class, though I'm not sure it addresses the specific 1→7 pattern.

I'm considering a more expressive template for the 1-vs-7 case, possibly with a top-bar emphasis on the 7 template or a variant 1 with a slanted stem. Some of those 160 ones may carry a top flag that makes them look like sevens.

Checking the 7→2 confusions next: 231 sevens land on 2s, and the 2 template's top arc and bottom bar may be overlapping with where a 7's top bar sits, so I'm considering whether the 7s are drawn lower or the stem sits differently than my template assumes.

I'm looking at the 2→8 confusions next, where the 8 template's broad coverage seems to win too often, and I'm considering whether its penalty is simply too weak.

I'm considering whether the templates could be sharpened, such as raising them to a power to favor their stronger features, or clipping them. I'm also wondering if increasing the weight β further, which already took the loss from 1.5 down to 1.1, would be the simplest next step.

Next I'm bumping β to 2.5 and scaling the bias to match, since the loss has been dropping as β grows. I'm also adding targeted emphases on the 7 top bar, the 2 bottom bar, and the 5's vertical stroke, aimed at the 7→2 and 3/5 confusions.

I'm adding a few targeted emphases to the templates: a vertical boost on the 1, plus extra weight on the 5's left stroke and top bar. I'm also setting β to 2.5 and scaling the bias to match.
