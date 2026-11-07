I'm stuck at about 62% with template matching, so I need a better approach. I'm considering more discriminative features and using the fc weights as contrast between classes rather than as prototypes. My guess is that the stroke placement in my templates is off, and since I have no data, I'd tune per-class biases using feedback from the confusion matrix.

I'm weighing a different architecture, since the hand-drawn templates look like the real bottleneck. A linear classifier on pooled oriented-edge features could plausibly reach around 90%, and the question is how to get good templates without data. I'm also considering whether conv2 channels could act as nonlinear detectors for digit parts, since a single linear logit per class can't take a max over several prototypes.

I'm thinking about why the 7→9 confusion happens: the 7's diagonal runs down toward the center-left, while the 9's right-side vertical sits in a different place. I suspect the template centering might be shifting strokes enough to cause these overlaps.

Now I'm weighing whether a linear classifier on pooled oriented-edge features, with better-placed strokes, could beat the template plateau. I'm also considering tuning a few global hyperparameters and per-class biases through feedback, though I expect the gains to be limited.

I'm looking at per-class bias tuning from the confusion matrix, estimating logit offsets for the classes that get overpredicted, like 6, 8 and 9.

I'm thinking about per-class bias corrections for 6, 8 and 9 that could give a small gain. Blurring the templates to look more like real class means might also help, since my crisp strokes are sharper than actual averages.

I'm going to soften the templates by blurring them spatially, since real digit means are blurrier than my crisp strokes and nearest-mean matching should favor that. I'm starting with a blur of about sigma 1 to 1.8, and I'm weighing whether to add mild bias changes for 6, 8 and 9 at the same time or keep this step to the blur alone.

I'm going to keep the blur change on its own this step, and I'm setting the spatial blur on the wide channels to match the tight ones at sigma 1.5.
