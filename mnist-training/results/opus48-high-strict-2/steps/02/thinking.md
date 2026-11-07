The network is overpredicting 1, and the loss of 6.9 suggests the logits are too extreme. The digit 1 template is centered vertically, so its ink sits in the middle columns, and because the image is blurred and centered, it picks up general central ink. I'm also noting that template 8 is all ones, so after mean subtraction it goes to zero and its logit comes out as zero.

The network's predictions collapse onto 1, with the template for 1 positively weighting the central cells, and the blurred input has the most ink in the middle, so it correlates best with that template. The loss of 6.9 says the wrong class is being given very confident logits, which might mean the gain of 20 is too aggressive and the templates simply don't match the input well.

I'm weighing whether to pull richer features from the conv1 channels, which could pick up different stroke orientations and positions. First, though, the over-prediction of 1 needs fixing. Since all the templates correlate about equally, I should make them more distinct and maybe lower the gain, because the 6.9 loss shows the logits are far too confident.

I'm sketching the conv1 channels to detect oriented edges, with one channel for horizontal strokes via a vertical gradient filter, so that features like a plain vertical stroke can be told apart from other digits.

Still designing the conv1 kernels: one for vertical strokes, one for horizontal ones, plus diagonals and an overall ink blob, so that a plain vertical stroke can be told apart from something like a 7.

I'm now laying out the conv2 layer, which has 16 output channels over 8 inputs with 5x5 kernels, and the fc layer on top. Doing that by hand is getting complicated, so I'll keep conv2 simple and have each channel just pass through an averaged version of one orientation map.

Now I'm assigning the conv2 channels: the first five each carry the averaged map from one conv1 orientation channel, and the rest stay zero.

I'm settling on five feature channels, each a 4x4 map, which gives 80 features for the fc layer to use. The idea is that "1" leans on the vertical map while "7" leans on the horizontal top stroke and the diagonal. Hand-tuning that will be harder, and I can't test it here, so there's a real risk of another bad step.

I'm going with orientation features now, since spatial density alone keeps favoring "1". For the conv1 layer, I'm starting with a vertical line detector: a 5x5 kernel that is positive down the center columns and negative on the sides, so it responds to thin vertical strokes.

I'm settling on a vertical-stroke detector for conv1: a kernel that is positive down the center column and negative on the sides, so it responds to thin vertical ink but stays near zero for horizontal strokes. I'm still weighing the exact column profile, since a stroke might be two or three pixels wide and a single center column may be too narrow.

I'm settling the vertical-stroke kernel: I'll make the column profile sum to zero so that a plain vertical line lights it up while a horizontal stroke doesn't. The exact weights are still uncertain, so I'll check the response on a few sample inputs before committing to it.

I'm weighing a design where each digit's logit is a tunable linear function of interpretable features, such as total ink, top-versus-bottom and left-versus-right balance, vertical and horizontal stroke strength, and center-versus-periphery ink, so I can adjust the weights against the confusion matrix after each round of feedback.

Next I'm setting up conv1 with eight channels: plain ink averaging, a vertical-stroke detector, a horizontal-stroke detector, two diagonals, and three spare channels left at zero. Then conv2 will carry one conv1 channel forward through spatial averaging into each of its outputs.

I'm now sketching the digit profiles by orientation: a 0 is a ring with vertical sides and horizontal top and bottom, a 1 is mostly a strong central vertical with little horizontal, and 2, 3 and 4 each have their own mix of horizontal, diagonal and vertical strokes.

I'm weighing an orientation-based design over spatial density, since that's what keeps "1" from winning every time. Vertical-stroke detection is the key tool for telling 1 apart from the others, paired with total ink as a secondary check. I'm going to commit to a reasonable orientation-based setup and iterate from there, accepting that the hand-set signs may need correcting.

I'm building the vertical-stroke kernel for conv1 now, with positive weights down the center columns and negative weights on the flanking columns so that it responds to thin vertical ink but not to horizontal strokes.

Still working out the conv1 edge kernels: the vertical and horizontal stroke detectors, with the ink channel scaled to match.

Still working out the vertical-stroke scaling, since the raw response would dwarf the ink channel and I'll need to divide the kernel down before the features are comparable.

I'm settling the vertical-stroke kernel's scale so it's comparable to the ink channel, and I'm dividing the whole kernel by the five rows so the two channels are on similar footing.

Setting the vertical and horizontal stroke kernels to a 5x5 pattern scaled by 1/25 keeps their responses comparable to the ink channel. A single-pixel vertical line would come out around 0.8, which is in the same range as the ink signal.

I'm settling on three channels, ink, vertical and horizontal strokes, since a "1" should show strong vertical and weak horizontal response while other digits carry horizontal strokes that keep them off the "1" template. I'll set per-digit weights over those 4x4 positions.

I'm sketching the per-digit weights now: an ink template over the 4x4 grid, plus one scalar for vertical-stroke preference and one for horizontal, each spread evenly across positions.

I'm assigning each digit a rough vertical-versus-horizontal stroke profile: 1 gets strong vertical and negative horizontal, 3 and 7 lean on horizontals, and 4 and 6 sit more on verticals.

I'm giving each digit a rough vertical-versus-horizontal stroke weight, though these are guesses. The ink templates will be mean-subtracted to handle total ink, but the orientation weights may still favor dense digits like 0 and 8, so I'll watch for that and keep the gain modest.

I'm weighing how strongly to scale the ink, vertical and horizontal features against each other, since the vertical map can run several times larger than the ink channel. The next step is choosing the gains so no single feature dominates the logits.

I'm settling the gains for the three feature channels, starting with ink at 8 and vertical and horizontal at 6 each, to keep the logits moderate. The earlier loss blew up because a wrong class got high confidence, so I'm holding these lower and will check whether the loss stays reasonable.

Setting up the first convolution with a plain ink channel and a vertical-stroke channel, both scaled to 1/25.

Still setting the feature weights for the convolution channels and working out the per-digit spatial templates.

Setting the gains at Gi=8, Gv=6, Gh=6 with zero biases, and leaving the diagonal channels unused, so the three features stay balanced.
