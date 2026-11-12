Everything is stuck around 50%, and the 8s seem to be pulling everything toward them. My templates expect less ink than real images contain, and the max-pooled presence feature saturates across the whole center, so it stops telling digits apart. I'm thinking I need graded features closer to linear in local ink amount rather than binary presence.

I'm considering making the features smoother, blurring the ink map before pooling so the max pool roughly tracks local ink density instead of saturating. That would make the features graded and closer to linear, which could make template matching more robust. I'd still need to get the magnitudes right, so I'm working out how to compute the expected template values analytically from the strokes.

I'm checking whether the effective kernel's normalization holds up analytically, and noting that since the features are roughly linear, template magnitudes should match up to stroke-thickness variation. Thickness varies a lot across bold digits, so total ink magnitude shifts, which points toward cosine similarity to absorb uniform scaling. I'm also weighing whether a contrastive form with normalized templates would do better than the raw nearest-centroid cosine.

I'm weighing an alternative that uses the network's nonlinearity to match parts at the second conv layer, but that's hard to design by hand. I'm leaning toward orientation features instead: four orientation channels with graded blurred energy, and templates built analytically from the strokes with orientation weights, something like a HOG-style nearest template.

Now I'm setting up the second conv layer: averaging kernels over the pooled first-layer maps, with 3x3 versions at fixed offsets for the orientation channels and the ink channels.

I'm working out the effective receptive field by approximating the max-pools with averages, though a sharp 2px stroke makes max-pooling behave more like a saturating presence check than a smooth blur.

I'm estimating the effective window each feature covers, roughly a 6x6 region of input around each cell center once the two pooling stages are accounted for. Max-pooling inflates a 2px stroke to about 3px, so the ink fraction in that window comes out near 0.5. The template sums stroke points weighted by that kernel. I'll compute the shape first, since cosine similarity is scale-invariant and the exact magnitude matters less.

I'm weighing whether cosine scoring with these graded features is worth the risk, since a shared component could skew matches toward templates with ink concentrated in the center. A Gaussian view with normalized features leads to the same cosine distance, so it doesn't change the choice. Now I'm about to write out the template kernel.

I'm settling on a kernel for the template values: a soft box about six pixels wide on each axis, which roughly matches the effective window after pooling. I'll use a scale of about ten for the logits, since the feature norm is around three and the cosine gaps are small. The second conv layer will use 3x3 averaging kernels built from a binomial pattern, and I still want to sanity-check that the first-layer orientation detectors give sensible positive responses.

Working out the response of a horizontal-edge detector on a two-pixel stroke: the weights come out to roughly 0.92 for the stroke rows, minus a small penalty from the negative outer rows, leaving about 0.82. I'm about to check the vertical stroke case next.

Checking the diagonal detector next: on the pixel grid the response peaks on the diagonal and falls off to neighbors, so that's fine. Then I'll write the code.
