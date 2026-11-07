Edge features came out worse, at 76% against 82%, and the loss of 0.95 suggests the biases didn't help much either. So I'll go back to the ridge setup from step 8, which hit 82.65% with a loss of 0.553. For the next improvement inside the ridge framework, I'm considering thickness tolerance, though a 5x5 thick ridge can't be zero-mean with a wide center.

I'm weighing a few options for the next step: thickness tolerance and "ink" filters, but a zero-mean thick ridge doesn't work out well here. I'm also considering reworking the conv2 channels or adjusting the fc weights from confusion pairs, nudging the classes that get mixed up apart from each other.

I'm wondering whether the real problem is that my synthetic data misses the thickness and stroke variation in real digits, since ridge responses drop as strokes get wider. Per-sample amplitude could model some of that, though it doesn't cover orientation-specific differences. The main confusions are 3 vs 5, 2 vs 3, and 7 vs 9, so I'm looking at whether the 2 and 3 templates need to change shape.

I'm planning to add elastic deformation to the synthetic samples, using low-frequency random displacement so the within-class variation runs in the right directions for LDA. I'd keep the step-8 ridge config (gamma 0.7, alpha 2) and go to 500 samples.

I'm keeping the step-8 biases, since the extra correction in step 9 didn't help. Next comes an elastic warp for the synthetic samples: random low-frequency sinusoidal displacements applied to the normalized coordinates before the shear.
