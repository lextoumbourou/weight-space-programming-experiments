The test came in worse at 49.4%, with the penalties landing mostly on classes 1, 0, 4, 7 and 2, the ones with the biggest forbidden regions. So real digits seem to put ink where I assumed none goes, either because they vary more than I allowed or because my coordinate frame is off.

The 1s being predicted as 3 doesn't fit any reasonable geometry: 3's template puts ink in the center column at the top, middle and bottom, so a centered vertical stroke overlaps it heavily. I'm now checking how much of the 1's own template covers that same column.

I'm checking whether the numbers still favor a 1 being called a 3. Working through the logits, a centered 1 should score well above a 3 on overlap, so something about the real 1 images must be heavier or wider than my templates assume, which would also explain the forbidden-region penalties.

I'm checking whether the 1→3 confusion and the 1→2 confusions fit the geometry I've assumed. Both 2 and 3 carry strong center-column ink, and slanted 1s look like a 2's diagonal, so those overlaps may explain part of it. I'm also confirming that MNIST digits are size-normalised to a 20x20 box and centred by center of mass, so the digits occupy at most 20 pixels.

I'm weighing whether a much better approach exists, since the best step so far is only 52.6% against a ceiling near 80% for the true class means. My guess is that the templates are badly off in overall size: a 20-pixel digit spans more cells than my 8-row grid allows, so the ink overflows at the top and bottom.

I'm checking the template placement again: cell R=0 at rows 6-9, column mapping looks consistent. Stroke thickness of about 2-3 pixels in the 20x20 box seems right. The orientation maps might matter for curves and junctions, where the ink templates pick up extra density, but that's a secondary concern. The bigger suspicion is that real class variability, especially for 1s, is much wider than my templates allow.

I'm thinking about whether a blurrier template would match the real class means better, since my σ=0.8 strokes are sharper than the actual spread in the data. Smoother templates should also tolerate strokes that sit a cell off, so I'll try σ=1.1 for the ink and keep the norm consistent with it.

I'm weighing a blurrier template, around σ=1.1, since the sharper strokes may be missing real variation, and I'm checking how the normalization would change at ±1 and ±2 cells. I'm also considering whether averaging several template variants could help, though I'm not convinced yet. The best bias settings so far suggest this template family may top out around 56%, so I'm looking for a more substantial change.

I'm weighing whether the orientation features are helping or hurting, and I could test that by zeroing their scale for one step. Before committing to that, I want to see what the normalization of those H/V/D maps actually does to the values.

I'm weighing whether the orientation features are the problem: their H response may sit well below the ink response on real strokes, so the penalty for oriented structure could be too heavy. Next I'll try a step with blur at σ=1.0, the orientation scale cut to 0.12, and the forbidden regions dropped, keeping the step-3 biases.

Dropping the forbidden-region penalties and shrinking the orientation scale to 0.12 is the next experiment, along with blur at σ=1.0. I'm reverting the 6 template to its step-3 shape since that change seems to have hurt, but keeping the new 9 shape, which looked like a gain.

I'm reasoning that the norm penalty assumes the real images have about the same ink as the templates, which may not hold. If real digits carry more ink, classes with larger templates would gain an edge, since their dot product grows while the penalty stays fixed.

I'm checking whether the penalty on template magnitude is calibrated: if real digits carry about 1.5 times the ink of my templates, classes with bigger templates get an unfair edge, so the penalty factor should scale with that ratio.

I'm working out the scale mismatch between the real digits and my templates: if the real ink is about 0.78 of the template magnitude, the norm penalty should drop to around 0.39 rather than 0.5, though lowering it would favor the larger templates, so the direction needs checking.

I'm now checking whether the nearest-centroid rule stays robust if the template magnitudes are off by a constant factor. Working through the cases, the correct class still wins over a competitor in each example, so a global scale mismatch seems tolerable here and the real problem is the template shapes themselves.

I'm considering stronger blur (σ=1.0) as a way to make the templates tolerant of strokes sitting a cell off, and wondering whether cosine-style normalization would help. I'm also reconsidering the vertical extent: most MNIST digits are scaled so their larger dimension spans 20 pixels, which means my templates may be sized too small relative to the real images.

I'm checking where the center of mass lands in the 28x28 field, since the template offset depends on whether it sits at index 14 or 13.5. The difference is only about half a pixel, so it's a small correction, but I'm considering nudging the vertical center to 3.6 as a hedge.

Looking at the zero class again, the forbidden center region gave a worse result (464 versus 713), which suggests real zeros carry ink where I assumed none, so I'm checking the center of the ring against the 0.3 to 0.7 window.

I'm checking why the zero-class center penalty backfired: real zeros often have narrower holes than my templates allow, so the forbidden center region catches ink it shouldn't. My dilation seems to be making the holes too small in the template.

I'm looking at how fat the pooled ink maps are: a 3-pixel stroke spreads across roughly 3 cells, so an 8x8 grid ends up mostly filled blobs, and a zero's hole shrinks to about a single cell. Discrimination has to come from somewhere other than the ink shapes themselves.

Orientation maps are max-pooled just like the ink maps, so they come out equally fat and add little separation. That would explain why 0, 6 and 8 all look like blobs in the centroid comparison. The conv2 layer could carry finer information if it works on the 12x12 pooled map instead of simply passing pooled features through, though that map still has bands a few cells wide.

I'm working through a sharper ReLU-thresholded ink detector to thin the strokes before pooling, which should shrink the bands to about two cells instead of three or four.

I'm now thinking the thinner ReLU-thresholded features might be sharper but more sensitive to small position shifts, so the template blur would have to widen to match the variability in real strokes. I'm weighing whether scaling the conv1 output up to roughly 0 to 1.1 is worth it, given it trades away some sensitivity to faint strokes.

I'm now weighing a different idea for conv2: detecting empty regions at the pooled level, such as holes in 0, 6, 8 and 9, and the gaps in 4, rather than just passing ink through. The hope is that these emptiness features, after pooling, would give the fully connected layer the hole information the blurry ink maps are losing.

I'm now weighing a thresholded ink detector against the fat features, and I'd try a thinner set of ink maps with templates blurred to about σ=0.9 and the forbidden regions dropped. Orientation scale would go to 0.15 with the step-3 biases kept.

I'm settling the bias values and the scaling for the thresholded ink features, then sketching the template profile around a center of 1 with the neighbouring cells falling off.

I'm settling the template's blur at σ=0.9 with a normalization of 0.75, which should land the center near 1 and the neighboring cells at about 0.72 and 0.11.
