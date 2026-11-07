I'm designing a hand-written CNN from scratch, starting with a first layer of eight oriented edge and stroke detectors, then a second layer of sixteen channels that combine them.

I'm sketching the first conv layer as eight oriented detectors (horizontal, vertical, two diagonals, a blob filter, and edge types), and I'm mapping out how the second layer will combine them on the pooled grid. I'm also considering hand-set digit templates for the final layer.

I'm working out the hand-written digit templates, and I've ruled out running the network on synthetic inputs to compute the feature maps, so I'll write the 4x4 maps by hand. For the second layer, channels 0-7 will sum-pool each first-layer channel with uniform positive weights, while channels 8-15 will try a hole detector, roughly relu(bias minus the blob response), to pick up empty regions like the centers of 0s and 8s.

I'm laying out the fully connected weights by hand, one 4x4 grid per digit for each channel, using +1, -1 and 0 entries. I'm keeping the focus on ink and empty-region channels, and I'm planning to write the rows as compact strings and parse them afterward.

I'm settling the layout of the digit grids now: a 4x4 cell per digit, where the middle cells are the central part of the digit and the borders are the outer edges. For the empty-region channel I'm checking whether a max-pooled hole detection fires in those central cells.

I'm checking whether the empty-region detector can actually pick out the centers of 0s, since max pooling fires on any empty spot in a cell and the border cells would always light up. The receptive field of the second layer is large enough that the center cells only respond when the whole neighborhood is blank, so the bias and weights will need to be tuned to make that work.

I'm settling on a blob-density feature for the second layer: normalize the conv1 blob output so each value reads as local ink density, then use a negative mean over a 5x5 window with a positive bias to flag empty regions. Strokes should sit around 0.4 to 0.5 density in that window, so the threshold needs to sit below that to separate hollow areas from ink.

Next I'm picking the conv1 filter scale so line responses land near 1, using a difference-of-Gaussians ridge along each orientation with a taper and then zero-meaning the kernel.

I'm settling the edge detectors now: a horizontal top edge with ink below, a vertical left edge with ink to the right, and a vertical right edge with ink to the left. For the second conv layer I'm weighing a uniform pooling of each first-layer channel, though I want the scale to be more localized than what I first had in mind.

I'm assigning channels 9 through 15 to be mostly zero for now, with channel 9 as a center-weighted empty-region detector using a higher bias, which could pick out loop-like shapes.

I'm now setting up the fully connected weights per digit, using the ink, directional, and empty-region channels. I'm scaling the weights up a bit so the logit differences are large enough to matter for the argmax.

I'm now assigning the digit templates on the 4x4 grid: for 0, the center cells get empty-region and negative ink weights, with vertical strokes down the sides and horizontal ones across the top and bottom. For 1, the middle columns get vertical weight, the outer columns get negative weight, and the sides get empty-region weight. For 2 and 3, I'm laying out horizontal bars at the top, middle, and bottom, a diagonal for 2, and vertical weight on the right for 3.

Still writing the digit encodings as sparse entries, listing which channel and row each digit's weights go in.

Still writing the digit encodings, and I'm using short strings for each channel's 4x4 grid, with symbols mapped to weights.

Still writing the digit grids as compact strings, and this is code continuation.

Still writing the digit grids as compact strings, this time for the 4 and 5 patterns.

Still writing the digit grids as compact strings, this time for the 6 and 7 patterns.

Still writing the digit grids as compact strings, this time for the 8 and 9 patterns.

Still writing the digit grids, and this is the same code continuation.

Still working out the edge and blob filters: normalizing the ridge kernels so their positive weights sum to one, using gradient-of-Gaussian edges on the same scheme, and a sigma-1.2 blob with unit sum. I'm also starting the second-layer weights, setting each diagonal channel to a uniform 0.04 average across the first eight channels.

Still tuning the second-layer empty-region channel: with a bias around 0.15 and a negative weight over the 5x5 window, stroke density should keep it near zero while open areas still fire. Next I'll set the fully connected weights by scaling them up, then finish.

I'm settling the feature scale: the empty-region channel tops out near 0.15 while the other features sit around 0.3, so I'll multiply the fully connected weights by 5 to keep the logit differences meaningful.
