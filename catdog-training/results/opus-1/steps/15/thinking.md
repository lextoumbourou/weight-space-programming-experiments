I'm reconsidering the feature set, since the current scale is about right and what's needed now are better discriminating features. One idea is a spatial split, comparing fur color at the center against the border, with warm centers possibly pointing to dogs and white centers to cats.

I'm now considering a gray-fur feature for the cat side, since low saturation with mid brightness should separate it. Gray-ness is hard to get with a single ReLU at conv1, so I'm thinking about computing it in conv2 from combinations of the color channels instead.

I'm weighing a spatial probe: whether center texture leans toward dog or cat versus border texture, which would show up as the center texture weights pulling against the border ones. If the loss drops when center texture gets a small counteracting weight, that suggests the center is less dog-indicative than I assumed. I'm holding off on running it, since each probe costs a lot.

I'm going to test whether warm colors matter more at the center of the image than at the border. The plan is to move all of the warm weight onto the center cells and zero it on the border, keeping the bias as it is. Probes are expensive, though, and each one has only been giving around a 0.002 gain, so I'll hold off on running it.
