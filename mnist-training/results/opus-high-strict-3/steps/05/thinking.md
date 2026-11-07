The loss jumped sharply, so the projected logits may be producing large negative values. The template approach seems to be running out of capacity, and I need better features. Pooling over overlapping 4x4 windows and the spatial softness of the templates could both be contributing, and thick strokes may be weakening the line detector responses.

I'm weighing whether thick strokes are weakening the line detector responses, and whether the orientation features are simply too noisy to help. A simpler alternative is blurred raw ink on an 8x8 grid, since nearest class mean on pixels gets roughly 82% on MNIST, and my 69% suggests the templates are the problem: they're sharper than real class averages, so I'm considering blurring them more.

I'm considering dropping the overlapping shifts, since the max-pooling windows are redundant, and going back to the cosine-similarity approach with blurrier templates. I'm also weighing per-class bias corrections based on which classes the confusion matrix shows being over- or under-predicted, though the right magnitude isn't clear yet.

I'm thinking about whether cosine similarity with carefully drawn templates and some per-class bias calibration could reach around 75-80%. Next I want to go through each digit's typical shape: the 0 as a slightly right-leaning oval, the 1 as a thin line tilted a few pixels to the right at the top, and the 2 as a diagonal top arc ending in a flat bottom bar.

Now I'm going over the spatial details of the digit templates: the 4's open top and right stroke running from near the top down to the bottom, the 7's top bar and diagonal, and how centering might shift the 7s downward.

I'm checking the center-of-mass assumption, since I'm not sure whether MNIST's mean is at 14 or slightly off. Next I want to verify the conv2 tap mapping for the shifted windows, and I'm considering a test with blurred ink plus two orientation channels to see whether the orientation features are the weak part.

I'm weighing a bigger structural change: give each of the 16 conv2 channels its own tap offset, so the features sit on a finer grid of pooled cells instead of the current overlapping shifts.

I'm checking how the 2x2 shift offsets map onto the pooled grid, and whether the conv2 taps are actually giving distinct positions or just overlapping ones. It looks like only about 2-pixel spacing is really distinct, so the extra taps are mostly redundant. I'm also wondering whether a template matcher could sit directly on conv2 with a 5x5 kernel, though that only sees a 10x10 patch of input.

I'm weighing whether to use the spare conv1 channels for orientation coverage or thick-stroke detectors, but neither looks like it would clearly help the conv2 structure. I'm leaning toward keeping the current setup and just trying blurrier templates with a 3.5 falloff.

I'm settling on the loss scale next: at s=8 the loss is about 1.07, so I'll try s=10. For the biases, I'm thinking about small logit offsets, roughly -0.4 for 6, -0.3 for 9, -0.2 for 2 and -0.1 for 8 since they're over-predicted, and about +0.4 for 5, +0.3 for 4, +0.1 for 3 and 0, since they're under-predicted. The template change could shift those, so I'll keep them modest.
