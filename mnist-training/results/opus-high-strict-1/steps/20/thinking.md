Step 15 sits at 75.04, so reaching step 20 around 75.54 looks fine, but I need steady gains to keep climbing. Comparing against step 16's 76.19, step 21 would need to reach 76.69, so I'm looking for real improvements. Two structural ideas stand out: the empty-features change added about 1.2, which suggests tuning ERAMP or the emptiness thresholds, and the orientation group is worth revisiting since it once had a shifted copy.

I'm weighing whether tuning the kappa or eta weights could help, since the orientation and emptiness terms trade off against each other. I'm also thinking about a hole detector, though the interiors of these loops are probably too small for the current emptiness windows.

I'm checking whether the 3-versus-5 confusion comes down to a particular feature, like the upper-left vertical that 5 has and 3 lacks. I'm also questioning whether the emptiness windows are even local enough to pick up on that difference, since their effective input coverage seems large.

I'm weighing whether a finer emptiness signal would help, but max-pooling over the 2x2 conv2 positions turns the detector into an OR, so almost any region will look empty somewhere and the signal goes uninformative. What I'd need is something closer to an AND, like a min over the cells.

I'm weighing whether a stronger penalty weight (LAMBDA) could help, since the emptiness channel only adds a saturating non-linearity on top of what the fc layer can already do with negative weights on ink presence.

I'm considering hyperparameter sweeps with small steps, since each could plausibly add a few tenths of a percent. The candidates include the penalty weight, the kappa-to-eta balance, the shear, the ramp, the orientation cutoff, the conv1 bias, and the emptiness threshold. Shear looks most promising to me, since my templates lean about 7° while handwriting usually leans more, so I'm thinking about trying a shear of 0.2.

I'm going to try a shear of 0.2, since handwriting usually leans more than my templates do. I'm also nudging the biases: the 3 column is still under-filled, so it gets a small boost, while 6, 7, and 9 get a slight reduction.
