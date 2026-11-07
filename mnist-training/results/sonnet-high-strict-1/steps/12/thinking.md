I'm at a plateau around 57% with four steps left, and the hole channel isn't adding much. Nothing I've tried so far is producing a big gain, so I'm considering either dropping the noisy channels or shifting toward narrower features with a sharper positional template and less cell-mean removal, possibly a pure version of that, though it's hard to judge without running experiments.

I'm weighing whether to boost the hole feature's weight, since the loop-based digits might be underweighted, though step 9's recall shifts are mixed. I'm also checking the conv1 orientation convention, which looks consistent, and considering dropping the per-class cell-mean removal to let ink amount separate digits like 1 and 8.

I'm weighing a shear correction for the slant: MNIST digits lean right by roughly 5 to 10 degrees, so I could shear every stroke by about 0.1 times the distance from the baseline. Some of my glyphs may already lean that way, but applying it uniformly looks cheap to test.

I'm settling on two changes at once: applying a shear of about 0.1 to all strokes and bumping the hole feature to a weight of 2.0. The results could be confounded, but with only a few steps left I'm willing to accept that.
