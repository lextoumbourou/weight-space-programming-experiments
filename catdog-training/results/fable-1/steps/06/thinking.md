Brightness turns out to be negligible, with both cats and dogs near 53–55% for F above 0.55 and a median around 0.56, so it isn't useful and leans slightly toward dogs. Texture looks like the key signal, so next I'm turning to texture features and weighing how to split the remaining 45 steps between a combined baseline and incremental tests. I'm still working out which texture sub-probes to run.

I'm now weighing a set of texture contrast probes: top versus bottom, centre versus border, vertical versus horizontal energy, and a diagonal-versus-average comparison, each kept near zero so the thresholds stay clean. I'm also considering fine-scale spot features separately, and whether folding a contrast into the combined baseline would be more step-efficient.

I'm weighing whether a centre-versus-border texture contrast would separate the classes better than testing each feature alone. For close-up cat photos the centre may hold the sharp facial edges while the border stays smooth, whereas dog scenes might show more texture around the edges, so I'm planning to test centre minus border as step 6, using the 3x3 centre and the 16-cell border.

I'm setting the sign convention for the centre-minus-border probe: a positive value means the centre is more textured, which would point toward dog. Then I'll just measure it.
