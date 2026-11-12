We're stuck around 62%, so a template-matching approach with hand-drawn prototypes probably tops out near 70% and won't get us where we need to be. I'm wondering what a stronger handcrafted feature design could look like, and I'm comparing it against known baselines: a trained linear classifier on raw pixels reaches about 92%, and nearest-centroid on class means about 82%, while my hand-drawn templates aren't true class means.

I'm weighing whether the features can keep more spatial detail, so the classifier sees something closer to the raw pixel layout. One idea is to spread single-tap conv2 channels across pool1 offsets so they reconstruct a coarse ink map, though I'd need nine channels just for one feature type.

Now I'm weighing whether a handcrafted design could approach the trained baselines. A 7x7 downsampled MNIST linear classifier should reach around 85% when trained, though hand-drawn templates are the weak point. Comparing my prototypes against true class means, a nearest-centroid classifier on 7x7 might land around 75-80%. I'm also considering whether richer structural features, like hole detection or endpoints, would help, but they look hard to get from this network.

I'm checking whether my templates are miscalibrated because of the max-pool and receptive-field geometry, so I'm tracing where each conv2 box's center lands in the input image.

I'm checking the receptive-field geometry again: the pooled cell centers land around 7.5 and 9.5 plus multiples of 4, and the top-row cell covers the digit's top strokes, so the mapping looks right. The templates themselves may be fine, and the weakness is likely that blurred orientation maps correlate heavily across classes. I'm considering sharpening the spatial kernel (sigma 3 to 2) so the differences between classes come through more clearly.

I'm setting aside the linear-discriminant idea, since computing a covariance from my hand-drawn variants feels too close to generating samples. Instead I'm considering orientation features with signed gradient direction, using edge polarity to tell whether ink sits above or below a stroke edge, which might help separate loop-shaped digits.

I'm considering edge-polarity features with eight directions, since each stroke produces paired edges that could localize it finer than a single cell. The 4x4 grid still looks like the main bottleneck, so I'm weighing how to spread the 16 channels across orientations and offsets to recover more spatial resolution.

I'm checking whether a smaller sampling box, or a single tap per pool1 cell, would sharpen the spatial detail. The concern is coverage: with offsets of 0 and 1, the pooled rows only reach pool1 rows 1 through 9, leaving the top row and the last rows uncovered.

I'm checking whether offsets (1,2) or (0,2) cover the pool1 rows well, and I'm not convinced that sharpening the box would help template matching, since the blur gives some tolerance. Rather than tuning the templates by hand, I'm considering whether conv2 could learn class-specific part detectors, since the fc layer is linear and the bottleneck is at the feature level.

I'm considering building conv2 filters as hand-drawn part detectors over the orientation maps, such as a closed loop in the upper half or an open top, with thresholds so they only fire on a good match. The fc layer would then combine those parts through a hand-assigned table of part-to-digit weights.

I'm working out the pooled cell positions for conv2, which land at 7.5, 11.5, 15.5, and 19.5 in the input, so each part detector covers about a quarter of the digit. Next I'm sketching part templates over the four orientation channels, starting with arc segments such as the top arc.

I'm sketching part detectors for the conv2 filters, covering arcs, bars, diagonals, junctions, and small loops, roughly a dozen to sixteen parts each found at the four pooled locations. The open question is how to assign digit templates over those parts without falling back on hand-drawn whole-digit prototypes.

I'm settling on hand-written part-location tables for each digit instead of computing matches on rendered prototypes, since running any part of the network on generated inputs is off limits.

I'm weighing a larger redesign with hand-written part-presence tables and weights, but I'm uncertain whether the part detectors would fire as intended, since their activation thresholds are unknown. The current approach is capped near 62%, so I'm considering whether the gap comes from writer variance rather than the features.

Simple ink features might hold up better than orientation maps here, since they're less sensitive to stroke thickness. I'm checking whether combining ink with the orientation channels could help before settling on a design.

I'm settling the channel layout for the first two layers: the first layer gets an ink channel plus four orientation channels with a gentler threshold, and the second layer splits its sixteen channels between ink taps and orientation taps at different offsets, weighing whether the uneven split of orientation offsets is worth it.

I'm weighing how to weight the ink and orientation feature groups separately instead of normalizing them together, since their magnitudes may differ and one could dominate the dot products.

I'm going with ink features alongside the orientation channels, using a Gaussian blur so thick strokes still register, and I'm working out the offsets for the ink taps in the second layer.

I'm settling the offsets for the second-layer taps: the ink channels use 2x2 boxes at offsets 1 and 2, which puts their cell centers at 6.5 through 20.5 and keeps the grid symmetric about the middle. For the orientation channels I'm weighing three offset choices, since the asymmetric pairing is awkward, and I'm leaning toward reducing them to two offsets to keep the layout balanced.

Still settling the channel split: four ink channels using 2x2 boxes at offsets 1 and 2, and twelve orientation channels across three offset pairs, accepting a slight asymmetry in the third pair.

Next I'm setting the ink template width at σ = 2.5 and the orientation template at σ = 3, then settling the orientation bias at -0.2 since the two earlier bias values scored about the same.

Next I'm setting up the code: the feature template will take a list of channel specs, each giving the feature type, orientation index, offset, and box size. The first four channels are ink taps and the rest are orientation taps.

Settling the offsets for the orientation taps: I'll use (1,1), (2,2), and (1,2), accepting that this leaves the layout slightly asymmetric. The first layer keeps orientation channels 0 through 3 and puts the ink channel at index 4, which the second layer reads accordingly.
