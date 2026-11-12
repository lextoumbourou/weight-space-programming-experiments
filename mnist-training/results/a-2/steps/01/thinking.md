I'm settling on a hand-designed architecture, where the first conv layer would have eight channels, one of them a blurred intensity map and the rest oriented edge detectors, since simple passthrough filters followed by template matching at low resolution would be too weak.

I'm now thinking about how the later layers would combine the features: after a second convolution and pooling, the grid would shrink to 4x4 with 16 maps, and the final linear layer would classify from those. One practical idea is to pass most of the first-layer channels straight through the second convolution and then hand-set digit templates over the 4x4 grid. I'd also need to decide how to write those templates, and I'm wondering whether drawing the digits as strokes would be an acceptable way to define them.

I'm going to define the fc weights directly in feature space instead of rendering digits and running the network, marking which orientation appears in which 4x4 cell for each stroke. Mapping positions through the two conv-and-pool stages, the 4x4 cells land at roughly input rows 7.5, 11.5, 15.5 and 19.5.

I'm checking where the 4x4 cells sit in the input: the digit spans roughly rows 4 to 24, and tracing the receptive fields through both conv-and-pool stages puts the final cells' coverage at about rows 0 to 15 for the first cell and 12 to 27 for the last.

I'm weighing a shortcut where conv2 just duplicates the conv1 channels, each in a centered and a blurred form, to get the 16 maps. I'm also considering a nearest-mean classifier in feature space, but without data I'd have to guess what an average digit looks like, which makes that riskier.

I'm thinking about how to write the fc weights directly from stroke geometry, sampling points along each segment and assigning them to 4x4 cells by angle, which avoids running the network on any input. I'll then plan to refine the weights based on the confusion matrix and tune a global logit scale for the loss. I'm now sketching the first conv layer as eight oriented line detectors, starting with the four orientations.

I'm weighing polarity edge detectors against plain line detectors, since a polarity edge would show which side of a stroke has ink, which matters for loops like 0.

I'm now weighing whether unsigned 4-orientation line detectors are enough, since signed gradients lose their polarity at this coarse grid. The other four channels might be finer orientations like 22.5° steps, or I could leave them as something else.

I'm now working through the first conv layer's channels: four line detectors at 0, 45, 90 and 135 degrees, with a fifth channel for blob intensity still being considered.

I'm weighing the first conv layer's remaining channels: the rest could be signed edges in four directions or a blur, but at this coarse grid the polarity would be lost anyway. A better use might be eight elongated Gaussian line detectors at 22.5° steps, though a 5x5 kernel may not be selective enough to tell those orientations apart.

I'm going with eight conv1 channels: four oriented line detectors, an intensity channel, and a few spare slots. Conv2 would carry smoothed versions of the first channels down to a 4x4 grid, and the fc template would then run over those 80 features as a baseline.

I'm considering using the conv2 channels to sample different spatial offsets of the first-layer features, so that taking each channel at a shifted position gives finer localization before the final pooling.

I'm working out where the conv2 taps land relative to the input: pool1 index maps to input centers at 2p+2 and 2p+3, so each 4x4 cell covers roughly input columns 6 to 9 for the first and 18 to 21 for the last. That leaves the outer edges of the digit (around rows 4-5 and 22-23) uncovered, so I'm considering a 5x5 blur in conv2 to extend the reach.

I'm now writing the template weights from the stroke geometry: for each 4x4 cell and orientation, a sum over sample points on the strokes, weighted by angle match and distance to the cell center, and then normalized and centered across classes.

I'm sizing the line-detector responses now, using a kernel that is zero-sum across its perpendicular profile so flat regions give no signal, and I'll tune the fc weights against those magnitudes afterward.

I'm normalizing the line kernel so its positive weights sum to one, which should give roughly unit response on a stroke, and I'll accept a small negative contribution from the surround.

I'm settling the feature scale for the fully connected layer: conv2 channels become Gaussian-blurred, normalized copies of the first-layer maps, so features stay roughly between 0 and 1. The templates get unit norm per digit, and I'll start with a logit scale around 5 and tune it afterward.

Now I'm laying out the template weights for each digit: normalizing each to unit length, then subtracting the mean across classes so the classifier separates them. I'll start the digit stroke definitions with the zero.

I'm now writing the digit stroke definitions, starting with the zero as an ellipse and the one as a near-vertical line with a slight slant.

I'm now writing the stroke definitions for digits 3 and 4: the 3 as two stacked arcs bulging to the right, and the 4 starting with a near-vertical left stroke.

I'm now defining the 5 as a top bar, a short left vertical, and a bottom arc that sweeps clockwise from the upper left around to the lower left.

I'm now defining the digit 9 as a top loop centered near (14, 9.5), with a stem running down from it, the same way I set up the 6 with its loop at the bottom.

I'm checking where the cell centers fall: working through the conv2 and pooling offsets, the four 4x4 cell centers come out near rows 7.5, 11.5, 15.5 and 19.5, so the digit's midpoint at 14 sits between the middle two.

I'm turning to the weighting for the template: each point's contribution falls off with a Gaussian of its distance from the cell center, and the orientation match is squared so it drops to zero at right angles. The intensity channel gets a similar proximity weight at about half strength. I'm also considering whether to use a saturating form like one minus an exponential of the summed weights, since max-pooled presence values don't add up the way sums would.

I'm thinking about the feature scale again: conv1 line responses are around 0.5 to 1, the conv2 blur drops them to roughly 0.3, so the 80 features land near 0 to 0.4. Scaling the logits by about 15 seems reasonable, and I'll check that against the loss once it runs.

I'm writing the line-detector kernel for each orientation: a Gaussian along the stroke direction, times a center-minus-surround profile across it, then mean-subtracting it so flat regions give no response.

I'm defining the line-detector kernel as a Gaussian along the stroke direction times a narrow profile across it, then zero-centering it and normalizing its positive weights to sum to one. Next I'm setting up the eight orientations at 45° steps, with the intensity channel as a unit-sum Gaussian and zero bias.

Writing the template weights now: each cell's raw score sums stroke points weighted by proximity and orientation match, and I'm saturating it with one minus an exponential so the max-pooled values stay bounded.

I'm turning the template into something the classifier can use: the raw stroke scores get squashed into bounded values, then each digit's template is centered against the others and scaled to unit length. Features are on a smaller scale than the templates, so I'll score each class by a cosine-like dot product and pick a logit scale around 20 without a bias term.

Writing the line-detector kernel code now...

Writing the line-detector kernel code now...

Still writing the stroke sampler...

Still writing the digit stroke definitions...

Still writing the digit stroke definitions...

Still writing the digit stroke definitions...
