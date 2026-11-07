The eight is now absorbing the other digits, and the orientation features I added seem to be what gave it extra positive weight, since its ellipse strokes cover every orientation near the center. I suspect the orientation channels are simply too strong and are bleeding into each other, so I'm considering scaling them down to about 0.7 and recalibrating the bias.

I'm weighing whether to scale the orientation features down to about 0.7, or to drop them and revert to the earlier version at 41.5%. The orientation channels seem to fire almost everywhere there is ink, so the feature mostly tracks ink density and favors the 8 template, and I'm considering making each class's orientation weights zero-sum to measure contrast instead, with a modest scale of 1.0.

I'm going to keep the biases from step 7 and apply a per-class zero-sum to the orientation maps, so the term measures contrast rather than raw ink. I'll try that with the scale at 1.5.
