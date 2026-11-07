I'm checking why every input comes out as 9: the fc bias is zero, so the constant has to come from the features. On a blank background, the conv1 biases are zero or near zero, so after the ReLU the activations drop to zero and conv2 sees nothing but zeros.

I'm now testing whether the bias on a blank background could be the source, since background activations on channel 4 come out to zero. Class 9 has positive weights on several channels and negative weights on a couple of others, and a large positive channel-4 sum should compete with it, which makes the all-9 result look suspicious. I'm also wondering whether the fc weight indexing could be off.

I'm now weighing whether the features themselves are the problem: the conv2 channels are mostly positive for strokes, and class 9's weights sum to the largest total in the upper region, so it may just win for every input regardless of the digit.

I'm weighing the class-9 weights against the others: the mask-based terms for 8 should push it up, yet 9 still wins, so I'm suspecting the negative terms on channel 0 and channel 1 are shifting the balance in a way I haven't accounted for.

I'm now thinking the features may not be what's separating the digits, so I'm considering a different readout: centering the fc weights across classes so no class gets a generic advantage, and balancing the logits on an average input.

I'm going to center the fc weights across the ten classes, so that for each feature position no digit gets a generic advantage from ink alone. After that, I'm planning to sketch a coarse ink template for each digit as a more discriminative readout, though I don't have data to check it against yet.

I'm checking whether conv2 channel 7 is just a box average of the conv1 density channel, which would make the fc input a coarse 4x4 blurred image of the digit.

I'm weighing a cleaner readout: centering the fc weights across the ten classes so no digit gets a generic advantage, and using each class's 4x4 density template on the channel-7 blur. The grid is coarse, so I'm not expecting strong accuracy from that alone.

I'm weighing whether the 4x4 grid is the real limit here: with 16 channels I could try encoding sub-cell ink position in each channel, though that's 256 features to hand-design with no data to check against.

I'm settling on two fixes for the all-9 problem: center each feature's weights across the ten classes so no digit gets a generic advantage from ink alone, and replace the prototypes with 4x4 density templates per digit, plus the stroke-channel terms, all mean-centered.

I'm sketching each digit as a 4x4 density template, starting with the zero as an oval ring that sits mostly in the central cells.

I'm writing out the 4x4 density templates digit by digit, with the zero as a ring and the one as a central stem, and now starting on the two.

Now I'm writing out the 3 template, with the top arc on the right side and the middle bar sitting in the central cells.

I'm sketching the 4x4 density templates digit by digit, now working on the four, with its stem at the right column and the crossbar in the middle row.

I'm continuing the 4x4 density templates, with the 4 drawn as a stem on the right and a crossbar in the middle row, and now starting on the 5.

I'm working through the 6 template now, with its ring-like loop at the bottom and the upper cells mostly empty.

I'm now working through the 7 template, with the top bar across the upper cells and a diagonal sloping down to the left, and then moving on to the 8.

I'm writing out the density templates for the 8 and 9, and I'm about to center each digit's weights across the rows so that the readout doesn't favor one class by default.

I'm working out the scale of the channel-7 feature: a stroke-dense 5x5 patch gives roughly 1 after the ReLU offset, and the box average and max-pooling keep the pooled values in about the 0 to 5 range.

I'm checking whether the density-based 4x4 templates, centred across the ten classes, will give a real correlation with the pooled channel-7 features, and I'm estimating roughly 50-70% accuracy from that.

I'm settling on keeping only the density channel for this step, since channel 7 is the single pathway that carries the pooled ink signal. I'm also weighing whether the 4x4 grid loses too much shape detail, though the blur from the conv2 window and pooling probably spreads things enough to be workable.

I'm settling on a scale of about 1.5 for the centred density weights, and I'm keeping the conv layers as they are while zeroing the fc weights for the channels I'm no longer using. I'm also noting that blank images would give all-zero logits and default to class 0, which I may need to handle with a small bias.

Writing the centred readout code now...

Writing the centred readout code now...
