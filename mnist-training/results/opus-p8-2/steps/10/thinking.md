Progress has stalled at 68%, so I'm weighing a different approach: a network that behaves more like a pixel-level linear classifier with hand-set weights. I can't recall the exact weights for that, so I'm considering a known hand-designed method instead, such as k-NN or template matching at modest resolution, which reportedly reaches around 80% on MNIST.

I'm looking at the blobbiness problem: the 8x8 ink map takes a max over a block, so a simple subtraction in conv2 won't undo it. Orientation features look more specific, so I'm weighing higher-resolution orientation maps, though that costs channels and may lose hole information. The confusion pairs (2→3, 8→2, 1→7, 7→9) suggest the real limit is how slanted strokes of 1s overlap with the diagonals of 7s and 2s.

I'm weighing whether learned-style weights could be replaced by an analytic model of within-class variation, for instance blurring each class template with a Gaussian kernel rather than sampling shifted or slanted copies. Cosine-normalized template scores might still handle the 1-versus-7 overlap, since the small-norm 1 template produces high normalized values, though I'm not certain that holds.

I'm considering hand-setting pairwise weights for the top confusions, like 2 versus 3, using where each digit has ink in the lower-right and bottom-left regions. The existing templates may already encode this, but explicit adjustments for those specific features could still help, even though it will be tedious.

I'm also wondering whether the readout could approximate a per-class linear model better, since negative weights matter: a class should be penalized where it has no ink but other classes often do. Nearest-mean scoring, 2T·f − |T|², captures this in principle, though cosine normalization only handles part of it. The real gain would come from covariance, which a shared isotropic model like nearest-mean ignores.

I'm thinking about adjusting the group scale factors: a test with ink weight down to 1.5 and orientation weights up to 3.0 to see which direction helps, and I also want to update the bias using the step 9 column sums.

I'm working through the per-class bias corrections from the step 9 column sums: most classes sit near balance, so the adjustment should be small, roughly 0.7 of the log ratios. I also want to try a group scale test next, lowering the ink weight to 1.5 and raising the orientation weights to 3.0 to see which direction helps.

I'm trying the group weights at ink 1.5 and orientation at 3.0 for both tight and wide groups, and I'll keep the hole weight unchanged so only one thing shifts at a time.
