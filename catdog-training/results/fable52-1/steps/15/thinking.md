The centre-versus-border weighting gave only a +0.0005 difference, which is within noise, so I'm treating it as neutral and keeping the uniform weighting. Several simple directions have now come back neutral, which suggests the model is close to a local optimum, and further gains will probably need genuinely new information rather than tweaks. With 36 steps left, I'm going to think about what could add meaningful signal.

I'm now listing what's been tested so far, and the list is mostly neutral results: fine edges, colours, corners, orientation, luminance and spatial weighting. Combined, that gives about d'≈0.6. The untested options are the spatial frequency mix, the layout of edges, and object-level cues, with eye appearance looking most promising for a 64px image.

I'm weighing whether a small yellow-green eye blob on a grey surround could be picked up by a warm centre-surround filter at small scale, and I'm noting that grass would trigger the same green response. My worry is that the 5px eye gets diluted by the pooling in the second layer, so only blobs of about 6px or smaller would survive a centre-surround comparison. Then I'm starting to ask how often cat eyes actually show green dominance over red and blue.

I'm checking whether a yellow-green eye blob would stand out against the warm and green channels: eyes read as warm and green at once, while dog eyes are dark and weakly warm, so a small-scale centre-surround filter on the warm-plus-yellow channel might separate them.

I'm now considering a small-scale yellow-green blob detector, since eye-like spots could carry signal that the earlier neutral features missed, and I'm estimating it could give a partial d' of around 0.1 to 0.2. Dogs rarely show small yellow blobs, so the test seems worth a step or two. I'm also weighing a pink blob detector for tongue or nose cues, but I'll set that aside for now. Next is coarse versus fine structure: I'm starting to think about how to compute coarse-scale edge energy from the pooled luminance maps.

Now I'm looking at the luminance channel. Bright and dark rectifiers leave a dead zone in the middle, so I'm considering a smooth luminance map instead, and then coarse edge detectors on that map, with conv3 summing them into a coarse-edge energy.

I'm thinking about a coarse-scale edge channel built from a smooth luminance map, summed into a coarse-edge energy. My guess is that coarse energy, once fine energy is accounted for, would lean toward cats, so I need to decide whether to probe it alone first or test it on top of the existing feature, which takes two steps.

Next I'm looking at the remaining budget: a spatial-layout probe of the edge energy, a global scale-and-bias tweak, and a relative-weight tuning between the W and E terms, each worth only about 0.001. I'm also considering a couple of more distinct ideas, such as image borders, human presence, and tabby-stripe texture as a cat-specific cue.

I'm testing whether the fine edge energy is stronger in the centre than at the border, on the idea that cat fur texture sits on the animal while dog photos carry more background clutter, so a negative sign on the centre-minus-border term would point toward cats.

I'm estimating the noise and signal for a centre-minus-border probe on edge energy: with a small contrast of about 0.07 the expected gain is only around 0.003, so the test is worth running but it is weak. I'm also wondering whether the centre might simply carry more energy, which would shift the mean rather than the variance.

I'm running a centre-minus-border probe on fine edge energy with a negative sign, since tabby texture and face detail could make cat centres more energetic than dog backgrounds. The contrast mean will probably be shifted by around 0.9 per cell, so I'll read the bias offset from the result rather than assume it.
