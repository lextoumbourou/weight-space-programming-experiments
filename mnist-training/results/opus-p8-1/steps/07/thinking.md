Accuracy rose a little but loss went up, which looks like overconfidence with alpha set too high. Most predictions are landing on class 2, and its template spreads its weight across every orientation, so it's broad. Cosine similarity seems to favor those diffuse templates, since real features are blurrier than the sharp templates. I'm considering smoothing the templates to match the blur in real class means, and normalizing the cosine to handle noise in the features, possibly by standardizing them first.

I'm considering centering both the features and the templates by subtracting the average template across classes, which would turn this into a centered cosine that emphasizes the discriminative directions. The catch is that the bias term could push toward class 1 for sparse digits, which is the same failure I saw before. A nearest-centroid form with a fitted scale factor might be a more principled alternative.

I'm thinking about a centered-cosine version that subtracts the average template, though the bias term may still push sparse digits toward class 1. Scaling the dot product with a tunable factor s, between plain dot product and cosine, looks worth trying, and I'd lower alpha to around 4 while blurring the templates.

I'm going to check the column sums for class 2 and class 8 to see whether a bias correction is worth adding. I'll skip that for now and first try blurring the templates with a light kernel and lowering alpha to 4.

I'm settling on a light blur kernel, roughly [0.25, 0.5, 0.25], to apply to the templates and soften their sharp edges.
