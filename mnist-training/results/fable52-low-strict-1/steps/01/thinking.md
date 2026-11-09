I'm sketching a hand-written CNN for MNIST: eight oriented 5x5 edge detectors first, then pooling down to 12x12, then sixteen 5x5 filters into 8x8 and pooling to 4x4. The final layer would match per-class templates against those 16 channels on the 4x4 grid, and I'm going for a simple design I can trust.

I'm now weighing a Gabor-style bank of four oriented line detectors for the first layer, with optional blob and endpoint detectors, and a second layer that mostly smooths each channel into a coarse orientation map. The 4x4 grid cells would be centered at roughly 7.5, 11.5, 15.5, and 19.5 pixels, each with a wide receptive field, and I'm considering a smaller central kernel to localize them better.

I'm now settling on the template approach: rather than estimating the fc weights from examples, I'll hand-describe each digit as line segments in 28x28 coordinates, accumulate each segment's orientation into the matching channel at its 4x4 grid cell with Gaussian weighting, then mean-center the templates across classes so they work as discriminative weights.

I'm settling the fc layer as a template match: I'll centre the per-class templates across classes and scale them, then tune the bias from feedback. Next I'm working out the first-layer filters, weighing eight orientations at 22.5° steps against four orientations plus four edge-direction detectors.

I'm weighing how to set up the second convolution layer's channels: either eight orientation-smoothing channels, or a mix of orientation maps with end-of-stroke and curvature detectors, since those could carry more discriminative signal than line orientation alone.

I'm settling on a template-based stroke model for the templates: each digit's segments get rendered as orientation responses (roughly a cosine-squared falloff with angle) and accumulated into the matching channel at its 4x4 grid cell. Next I'm checking which first-layer option separates the confusable pairs better: eight orientations, or four orientations plus four gradient-direction edge detectors.

I'm settling the classifier as a cosine-style template match: each digit's logit comes from its template dotted with the features, scaled by a constant, and I'm still working out the exact form of that score.

I'm noting that the centering step doesn't change which class wins, so I can drop it and just use the normalized templates scaled by a constant. Cosine matching works here because the dot product with the normalized template is largest when the features point in the same direction. So the classifier weights become W_d = α·T_d/|T_d|, with bias zero to start.

I'm noting that adding negative evidence to the normalized templates just shifts every class by the same amount, so it doesn't change the argmax. Linear matching with normalized templates ends up equivalent either way. The alternative is nearest-prototype with a norm penalty, but that needs scale calibration, while cosine matching is scale-free, so I'll go with cosine and treat the loss scale α as unknown for now.

I'm estimating the feature magnitudes so I can set the loss scale α, and I'll tune it against the feedback, since the scale can't be pinned down exactly beforehand. Next I'm sketching a zero-mean, center-surround line filter in the first layer.

I'm defining a zero-mean line filter for the first layer, with a Gaussian-like profile across the stroke scaled so its positive part sums to one. I'm estimating its response to a stroke of about 2.5 pixels, and planning a small negative bias to suppress noise. An orthogonal stroke should give roughly zero response, since the kernel's perpendicular profile sums out.

I'm settling the first layer around four zero-mean line filters and checking that an orthogonal stroke gives roughly zero response. For the second layer I'm treating each pooled channel as a 5x5 box smoother, which should give a stroke roughly 0.75 in response, so the feature vector ends up with a norm near 3. Cosine differences between classes should be around 0.1 to 0.2, so I'll start the loss scale α at about 6 and tune it from feedback.

I'm now weighing what the other four first-layer channels should detect. Plain polarity edges would just duplicate the line orientation signal at this coarse resolution, so I'm considering end-of-stroke detectors instead, though a single 5x5 kernel may not isolate an endpoint cleanly.

I'm weighing whether a closed-loop detector in the second layer could separate 4 from 9, 6 from 5, and 8 from 3 better than plain line orientation, since it would need an ink channel to confirm the center is empty.

I'm considering using the remaining first-layer channels for concavity-style features, since a 5x5 pooled window could capture whether a region is open upward or closed, which would help separate 4 from 9 and 3 from 2.

Now I'm weighing whether to use four polarity edge detectors (top, bottom, left, right) for the first layer, since a stroke at any angle would light up both of its edges. I'm leaning toward a simpler first version and refining the architecture once I see the confusion matrix.

I'm considering whether the second convolution could use four spatial offsets per orientation to keep an 8x8 grid, rather than the coarse 4x4 that the pooling leaves me with. The snag is that the 2x2 max pool would blend those offsets back together, so I still need to work out whether the phase split actually survives.

I'm working out whether shifting the second-layer kernel by one pooled cell gives finer position coverage, with windows at alternating 2-pixel offsets, so the 4x4 pooled output effectively samples a finer grid.

I'm testing whether shifting the second-layer windows by one pooled cell, alternating between offsets, gives the 4x4 output finer coverage of the digit's area.

I'm checking whether shifting the second-layer windows by a pooled cell at a time, in both row and column phases, could give an 8x8 grid of orientation features instead of 4x4. That would mean four channels per orientation, and the overlapping windows should cover the digit's area with finer positional detail.

I'm working out the pooling geometry for the second layer: each conv2 output reads a 2x2 block of pooled cells, and I'm checking which pooled positions each shifted window covers so the 4x4 output gets finer positional coverage.

I'm checking the pooling arithmetic for the second layer: with a 3-wide window the offsets could be 0 through 2, which would smooth more, so I'm weighing that against the current 2-wide version.

I'm working out the effective window for the template rendering: roughly a 6-pixel-wide region from the pooling plus the conv1 filter, so I'll deposit each template with a Gaussian of about σ=3 to allow for handwriting variation. Then I'm settling the flattened feature index as channel times 16 plus row times 4 plus column, with each channel's row-phase and column-phase offset setting where its pooled windows sit.

I'm mapping each pooled cell to its input-pixel centre, then flattening the features so channel, row and column each get a fixed slot. For the template I'm treating the feature as saturating rather than linear, so I'll compress the deposited amount with tanh.

I'm defining the first-layer line kernels as Gaussians of their perpendicular distance from the centre, zero-meaned and normalised to a unit positive sum. For tuning I'm assuming a response that falls off roughly with cos(2Δ), so a stroke 45° off the kernel's axis gives close to nothing.

I'm settling on a response curve for the first-layer detectors, leaning toward a wider exponential falloff over angle rather than a strict cosine cutoff, and adding a small negative bias to suppress noise. Next I'm checking how a stroke's profile across the kernel sums to a zero-mean response.

I'm tuning the width of the line response now: with a slightly broader Gaussian, a width-3 stroke scores highest, thinner strokes come out a bit weaker, and very thick strokes get pushed toward zero by the negative surround.

I'm now setting up the digit stroke prototypes in a normalized coordinate frame, mapping the 20-pixel digit box into the 28x28 image, with the height spanning the full box and the width varying per digit.

I'm settling the stroke templates in a normalized frame: each digit's height fills the 20-pixel box, its width scales per digit, and then I'll shift the rendered strokes so their centre of mass sits at the image centre. I'm holding to one template per class rather than averaging many samples, drawing only the hand-described strokes.

I'm now laying out the digit prototypes as slanted polylines and arcs in a unit box, with a slight rightward lean to match typical MNIST handwriting. I'm defining a helper that samples points along an arc from one angle to another, so the curved strokes of digits like 0, 3, 6, and 8 can be built from the same primitives.

I'm setting the digit box width at roughly 14 pixels for most digits, with the 1 much narrower, and placing each stroke in a 20-pixel unit grid before recentring. I'm starting with the 0 as a slanted ellipse and the 1 as a near-vertical line with a slight lean.

Writing the digit-3 arc as a continuation of the stroke prototypes...

Now I'm listing the stroke coordinates for digits 3 through 5: the lower bowl of the 3, the diagonal and crossbar of the 4, and the top bar, vertical and bowl arc of the 5.

Now I'm writing out the rest of the digit prototypes: the 6 as a curved stroke ending in a loop, the 7 as a top bar with a diagonal down, and the 8 as two stacked ellipses. I'm starting on the 9 as a loop at the top.

I'm placing the digit strokes with a small per-digit slant and then shifting the rendered result so its centre of mass lands at the image centre.

I'm now checking the feature-cell coordinates, working out that each pooled cell's centre sits at 4i+2or+6.5 in input pixels, and I'll deposit the stroke samples into the template using that mapping.

I'm settling how the deposited stroke weight gets compressed: a stroke crossing a cell centre integrates to about 6.3 at σ=2.5, so I'm weighing a tanh squash against a milder square root. The aim is that a stroke through a window lands near 2 after pooling, with two parallel strokes staying in range.

I'm settling the template weights now: each class's weight vector is the normalised template, possibly with a penalty wherever that digit has no ink, so the penalty pushes against classes whose shapes aren't present.

I'm thinking about the penalty term for classes that have no ink where the template is empty, like the 4's open top. The worry is that normalising the templates makes penalties skew toward digits with little ink, such as the 1, so I want to check that balance properly.

I'm weighing whether to add an orientation-free penalty for each digit's empty regions, scaled to keep it modest. Comparing the cosine match against a Euclidean form, the squared-norm bias would penalise large templates, so I'm leaning toward cosine with no bias and a small negative term on the no-ink cells.

I'm working out the scale of the template logits now, estimating the feature magnitudes and the cosine differences, and I'm leaning toward a second-layer box weight of about 0.25 so the correct class's margin lands near 3.

I'm writing the first-layer weights now: each of the eight oriented kernels gets a 5x5 pattern from its angle, with the offset of each cell measured along the stroke direction, so the code can build all of them from one loop.

Still writing the first-layer kernels and their orientation logic...

Still working through the tuning and coordinate conversion: I'm mapping points to pixel positions and recentring by the centre of mass, with a length-weighted centroid.

I'm writing the digit prototypes next, starting with the 6 as a curved stroke that runs into a loop, then the 9 as a loop with a stem, and the 5 as a top bar, a downward stroke, and a bowl arc.

Still laying out the digit prototypes as arcs and lines: the 3 as two stacked bowls, and the 2 as a top arc running into a diagonal and a base stroke.

Still writing the digit prototypes: the 7 as a top bar with a diagonal, the 4 as a crossed pair of strokes, and the 0 as a tall ellipse. I'm now setting up an arc helper and starting to deposit the sampled stroke points into the template grid.

Still writing the template deposit code, mapping each feature channel and pooled cell to its index in the fully connected weights.
