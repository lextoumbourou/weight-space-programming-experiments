I'm stuck at about 67%, so I need a structural change rather than tuning. One suspect is max-pooling over orientation features on thick strokes, which may leave too many channels active and blur the signal, or the line detectors may just be responding poorly. I'm also considering adding downsampled raw pixels as features, since nearest-centroid on pixels reached about 82% with true means, while hand-made templates did worse.

I'm weighing a more robust alternative: hand-built structural features like loop or endpoint counts, though that seems too complicated for this network. I'm also checking whether something is broken, since digit 1 recall is only 85% and its confusions with 7 look plausible given the diagonal stem. Slant variation seems to be the main source of within-class spread, so a single blurred template can't capture it, and I'm considering a union of sheared versions as a template instead.

I'm weighing whether to render each digit template as a max over several slanted versions, since slant is the main within-class spread. Averaging across those slants would approximate the class mean better than a single blurred stroke, though a broader template may pull predictions toward it, so I'd need to watch the biases.

I'm settling on rendering each digit template as a blur over several shear versions, since slant is the main source of within-class spread. Averaging over those shears should bring the template closer to the class mean, though I'll need to watch for biases. I'm also considering a width blur, but for now I'll keep to shear alone and recheck the prediction counts after the change, since 8 has been climbing.

Next I'm checking the bias adjustment, since the templates are changing and the earlier corrections may no longer fit. I'm also weighing a higher β, though I'll keep it at 3 for now so the template change is the only variable. Then I'll switch the stroke definitions to unsheared coordinates and apply the shear transform at render time.

I'm deciding how the shear will work for each digit: the base shears are -0.08, 0.12, and 0.32, with an extra shear added for 8, and the template will be the mean across those three shears.
