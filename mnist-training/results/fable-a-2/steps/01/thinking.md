I'm settling on a small hand-built CNN for MNIST: two 5x5 convolutions with 8 and then 16 filters, each followed by ReLU and 2x2 max pooling, and a final fully connected layer from 256 features to 10 classes. I'm starting to check the receptive fields after the first conv and pooling stage.

I'm working through the receptive field arithmetic for the final layer: each of the four output cells covers a 16-pixel window, with the starting rows at 0, 4, 8 and 12. I'm also sketching how the first conv layer could be oriented edge detectors, with the second layer combining them into more complex stroke features.

I'm considering using conv2 as a pass-through for each orientation channel, with a delta kernel at the center, so the 8x8 map lines up with the 20x20 digit box. After pooling that gives a 4x4 grid per orientation, and I'm weighing whether to fill the other 8 channels with more complex features or shift the kernel offsets to get finer positional coverage.

I'm checking how offset kernel positions shift the pooled grid: with different offsets, the same orientation channel covers staggered pixel windows, which could give finer positional coverage. I'm weighing a few offset combinations, and I still need to work out the FC templates for each digit, since I can't see the images.

I'm checking whether hand-placing digit strokes as oriented line segments in the 4x4 feature grid counts as a template, since that avoids running the network on any input. I think it does, as long as the templates are built directly from described strokes rather than from rendered images.

I'm settling the FC weights as templates drawn directly from hand-described strokes, one per digit, rather than from any network run on inputs. I'm weighing whether to add a couple of stroke variants per class, and I'm thinking about logit scale since the cross-entropy loss depends on it.

I'm weighing the logit scale next, since with roughly 70% accuracy a smaller scale would suit the loss better, and I'm planning to estimate the feature magnitudes first. Then I'll design the conv1 filters, starting with oriented line detectors that respond to the 2-3 pixel wide MNIST strokes.

I'm checking a first-pass conv1 design: zero-mean line detectors with a center band of +2 flanked by -1 on each side, scaled down so the peak response is about 1. A perpendicular stroke should give a near-zero sum because the profile sums to zero across the stroke.

I'm shaping the diagonal filters by setting each weight from its perpendicular distance to a line at the target angle, with a positive band at the center and negatives outside, then zeroing the mean. For the other four channels I'm weighing endpoint detectors against polarity-sensitive edge detectors, and I lean toward keeping four line orientations and using the remaining four for something more distinct.

I'm weighing whether to add a raw ink-blob detector for density and negative evidence, and I'm considering end-stop filters for stroke endings, which are harder to build with a 5x5 kernel.

I'm weighing the conv2 layer as the place for more complex shapes: over the pooled orientation maps, it could pick up corners like a 7, or loops around an empty center that mark 0, 6, 8 and 9. I'd rather keep the design simple and interpretable, since I'll only get confusion-matrix feedback to debug it.

I'm working out the 4x4 feature layout for the FC layer: the first four channels use the four line orientations on one offset grid, and the next four repeat them on a staggered grid.

I'm considering smoothing in the conv2 kernels rather than hard delta kernels, and I'm weighing whether the remaining channels should hold compound features. A plain ink-sum channel would be redundant with the orientation channels since the FC layer is linear, and an "empty region" detector would largely duplicate that too. Loop detectors that fire on an empty centre surrounded by ink look more promising for separating 0, 6, 8 and 9.

I'm now turning to concavity features: cavities that open to one side, like the open left side of a 3 or the upper cavity of a 5, which I can pick up in conv2 from an empty spot with ink on three sides.

I'm sketching a detector that fires on empty centers with ink on some sides and none on others, which could separate open-sided shapes like 3s and 5s, though it's fiddly to wire up with ReLU thresholds. Given that I can't inspect the images, I'm leaning toward a simpler orientation-based baseline first and reserving the remaining channels for cavity, loop, or endpoint features to add later.

I'm going to derive the FC templates from the stroke geometry instead of from network outputs: describe each digit as polylines on the 20x20 box, rasterize them, and bin the sampled points into the 4x4 grid by orientation and position.

I'm settling on the FC weights as a nearest-prototype classifier: each digit's template T_d gets logit α(T_d·x − ½|T_d|²), which is equivalent to a Euclidean distance match. The open question is scale, since the real activations need to match the template magnitudes, and I'll estimate that by hand from the stroke intensities and widths.

I'm settling the FC weights as scaled templates, W_d = α·T_d, with each bias set to −α/2·|T_d|². That makes the classifier a Euclidean nearest-prototype match, and digits with fewer strokes get a less negative bias.

I'm checking how the dot product with a template and half its squared norm play out for an 8 versus a 1 when the input is scaled down, and whether that comparison still favors the right digit.

I'm picking a scale α around 0.3 for the FC logits, since with only about 70% accuracy a large scale would make the wrong predictions too confident. I'll leave per-class bias offsets and the global scale adjustable so I can tune them from the confusion matrix later.

I'm sketching out the coordinate system for the convolution layers now, working through which pixels each conv1 output cell covers.

I'm mapping where each pooled cell's receptive field lands in pixel coordinates, working out the centers for the second-layer kernel offsets.

I'm checking how conv2 covers the box edges: a pure delta at offset 2 misses strokes near rows 4–5 and 22–23, so I'm considering a blurred 2x2 or 3x3 footprint for the grid kernels instead.

I'm checking where the conv2 footprint lands: a 3-wide kernel with weights 0.5, 1, 0.5 over two conv2 rows would cover pixel rows 4 to 11 for the top cell and 16 to 23 for the bottom, so the whole digit box gets included.

Weighing two-grid layouts against a single set of smoothed 3x3 or 4x4 orientation kernels: one set covers the 4 channels at a coarse 4x4 resolution, while staggered grids would sharpen the spatial detail a trained classifier could use, though hand-built templates may not benefit as much.

I'm planning to split the 4x4 layout into two grids: the first four channels use the orientations on a smoothed grid, and the next four use the same orientations on a grid shifted by half a cell, so the box edges and stroke positions get covered more evenly.

I'm now weighing a different set of channels: the first four cover the orientations, and the remaining four could carry gradient-polarity or endpoint cues instead. I'm checking which digit pairs the orientation maps would confuse, like 4 against 9, 3 against 5, and 7 against 9, since loop and cavity features should help with those. I'm starting to consider whether a cavity detector can be built reliably in conv2, looking at how ink in a given direction from each location might signal an open or closed shape.

I'm now checking whether a cavity detector can be built from conv2 by combining directional ink sums, since pooled activations aren't saturated and a single heavy stroke could dominate one direction.

I'm checking whether a cavity detector can be read off the pooled activations: sums of ink above, below and to the left of a location should separate an open-sided shape from a closed loop, with a threshold set so one heavy stroke alone can't trigger it.

I'm checking whether a ring-shaped kernel at two-cell radius can pick up loops, since the 5x5 pooling window roughly matches typical inner cavity sizes for 0s and 9s.

I'm working out whether a cavity detector can be built from the center-empty, ink-around-the-edge pattern, using the four orientation channels at radius one to two cells and a negative weight on the center cell. The catch is that a line filter sitting right at a loop's inner edge responds negatively, which ReLU clips to zero, so that part should behave.

I'm weighing whether to add cavity and loop features right away, or start with a baseline of orientation templates and tune later. Feedback is only aggregate, so I'm leaning toward including the structural channels with considered weights from the start, since they're what usually separate confusable pairs like 4 and 9.

I'm now defining the first conv1 channels as line detectors: horizontal, vertical, and two diagonals. For the remaining four, I'm weighing a blob or low-pass ink channel that would help check for an empty center.

I'm now listing the endpoint cues digit by digit: 1 has endpoints at top and bottom centre, 2 at the top-left and bottom-right, 3 at the top-left and bottom-left, and 4 at top-left, top-right and bottom. I'm thinking about whether a dedicated endpoint channel in the last four conv1 slots would separate these shapes better than the blob idea.

I'm testing whether endpoint detectors can be built from conv1 by requiring ink in a band on one side of the patch and empty space above it, with side columns penalized so a horizontal stroke's edge doesn't trigger them.

I'm checking the endpoint templates for the "ends pointing up" case: a stroke ending with ink in the lower centre and empty space above should fire, but a horizontal stroke would also match unless the side columns are penalized, so I'm setting the side weights to about 1.5 times the centre weight to cancel that out.

I'm weighing vertical-stroke endpoints in conv2 as a coarser, more robust alternative to pixel-level end-stop templates, checking for ink below a centre column with nothing above it.

I'm weighing whether to start with pure orientation templates as a safe baseline, since hand-tuned structural features could help but might also hurt if they're mis-specified. I'm leaning toward building the baseline first, checking how it does, and then layering in the feature groups with adjustable weights.

I'm weighing whether to start with a full incremental design, with structural channels included from the outset, or to keep step 1 to pure orientation templates. Endpoint detectors in the leftover conv1 channels, pointing up, down, left and right, look like a reasonable way to fill those slots, and I'm considering how the following conv2 channels could carry them forward.

I'm sketching each cavity feature in enough detail to decide whether it's worth including, and I'm also fixing the line filters by their orientation and perpendicular distance from the centre. The four line orientations could also serve as the ink measure for the cavity logic.

I'm defining each oriented line filter as a zero-mean Gaussian ridge across its perpendicular distance from the centre, then normalising it against an ideal stroke so every orientation gives comparable responses. That normalisation can be computed directly in code rather than tuned by hand.

I'm normalizing each line filter by formula so its positive weights sum to one, rather than testing it against an ideal stroke. Then I'm working out the mean of the horizontal Gaussian profile, using the cross-profile values at distances zero, one and two.

I'm normalizing the horizontal filter so its positive weights sum to one, which gives a full-width stroke a response of 1 and a width-2 stroke about 0.85. Thicker strokes get penalized because their edges land on the negative flanks, and that would hurt bold digits with 4-5 pixel strokes, which would give a response near 0.5 or even 0.

Thick strokes are the weak point of a plain zero-mean line filter: a width-4 or width-5 stroke lands on the negative flanks and its response drops to around 0.5 or even 0. Widening the positive core helps only a little, so I'm considering edge-based filters instead, which respond to each side of a stroke regardless of its width.

I'm weighing edge-based filters against line detectors: edge filters respond to both sides of a stroke regardless of width, but they carry little extra information at coarse cell scale, so line detectors still make more sense, provided the tolerance for bold strokes is handled.

I'm considering relaxing the zero-sum requirement so that thick strokes of width 5 don't drop to zero, perhaps with a profile of roughly [-0.6, 0.5, 1, 0.5, -0.6] that keeps a small positive bias.

I'm weighing a relaxed profile with a small positive bias so the bold-stroke response doesn't collapse to zero, and I'm noting that a slight bias would reduce orientation selectivity, so the trade-off needs checking.

I'm weighing whether a normalized template dot product can stand in for a linear classifier that is robust to amplitude scaling. With unit-norm templates and no bias, the argmax becomes a cosine-style similarity, so overall intensity changes shouldn't flip the predicted class. I'm checking that with Cauchy-Schwarz: a simple digit like 1 matched against a richer template such as 7 can't score higher than its own norm.

I'm checking whether subtracting a shared mean template would change anything, and it wouldn't, since a common offset shifts every class score equally. That leaves the question of how to sharpen the cosine matching beyond simple nearest-angle classification.

I'm considering whether to keep the template weights as they are, or to add negative penalties for ink where a digit should have none, such as the sides for a 1 or the lower-left for a 7, and whether that is needed once the cosine matching is in place.

I'm weighing a normalized-template cosine approach against the Euclidean one, since the two are equivalent once the templates are unit-norm. I'm planning to add a mild negative term for background cells where the digit has no stroke, and I'll tune that weight later.

I'm checking whether a uniform negative offset would help, but it wouldn't: it subtracts the same amount from every class score, so it can't change the argmax. I'm weighing instead a per-cell penalty that scales with how far each orientation channel's template value falls from the class's expected ink.

I'm noting that a per-class penalty for ink where a digit has none is just a shifted version of adding a binarized mask template, so it doesn't need a separate term. That makes the background handling a question of template shape, sharp versus broad, which I can adjust with some blur and maybe a square-root compression. I'm now turning to normalising each class template, W_d = T_d/|T_d|, and I'm wondering how classes with small templates, like 1, will behave under that scaling.

Now I'm sizing the overall scale for the normalised templates, estimating how much ink a typical input produces across the pooled grid.

I'm sizing the convolution kernel so its output stays in a sensible range: without scaling, a stroke running through the centre can double the feature value, so I'm dividing the kernel by 2 to keep a long straight stroke near the single-cell level.

I'm estimating the feature magnitudes per grid, which comes to roughly |x| ≈ 2.8, so the gap between the true class score and the others is only about 0.6 to 0.9. To get a reasonably confident softmax over ten classes, I need a scale factor α that pushes that gap to around 3 after multiplying.

I'm settling on α = 4 for now, since the estimated gap of about 0.7 between the true class and competitors gives a reasonable softmax confidence, and I'll tune it once I can test.

I'm weighing whether to add structural features like end-stops and loops now, at a lower weight, since they may add noise if their template placement is off.

I'm weighing a conv2 concavity unit that fires when the left, top and bottom regions carry ink but the right and centre do not, in the spirit of left- and right-open detectors, with the exact channel weights still unsettled.

I'm defining a left-side "wall" as any ink, and treating all four orientation channels equally so their sum acts as a stroke-presence measure. Where several channels fire on the same spot, such as on a 22.5° stroke or a curve, the total stays near one, and neighbouring cells pick up only partial response from the roughly one-cell-wide ridge.

I'm working out the left-wall feature: summing ink over the left column band should give a strong signal for a vertical stroke, weighted down so it lands near one. For the open-right check I'm considering a negative weight on the centre cell and maybe a few cells to its right, so that a ray with no ink scores high.

I'm checking how the open-left and open-right detectors behave on wide zeros: a point just right of centre sits close to the right wall and far from the left one, so the kernel reach could wrongly flag it as open to the left.

I'm noticing the open-left and open-right detectors would both fire in the middle of a wide zero, since the kernel's reach doesn't extend to the far wall on the other side. I'll have to live with that confound, or accept that the zero's shape partly covers it. Rather than keep hand-tuning these weights without feedback, I'm thinking about whether a single prototype per class is enough, since different writing styles of the same digit, like a slanted 1 or a 7 with a crossbar, might need separate templates.

I'm thinking about adding extra feature channels for end-stops and cavities, but I want a clean baseline first, so I'll start with the orientation channels and give any structural features a low weight. If they turn out to add noise, I can zero their weights in the next step and still learn from the comparison.

I'm weighing whether to start with a clean orientation-only baseline before adding end-stops and cavity features, since that makes any problem easier to trace to its source. I'm leaning toward the baseline, and I'm still deciding what to put in channels 8 through 15 so they stay useful without adding structure I haven't checked yet.

I'm weighing whether conv1 should spend all eight channels on finer orientations, or keep four line orientations and leave the rest free for structural features, since I think structure matters more than extra angular resolution here.

I'm weighing whether to keep the baseline strictly to line orientations and zero out channels 4-7 for now, or use them for endpoint detectors with their own weight. I'm leaning toward a clean baseline so any problems are easier to trace to their source.

I'm considering a clean baseline first, with channels 8-15 set to zero, and wondering whether staggered grids at different offsets in those channels could add useful coverage without bringing in structure I haven't checked.

I'm deciding to keep channels 8 through 15 at zero for the first run, so any problem traces back to the orientation channels alone. Staggering extra grids would only give a smoother 8x8 map with broad cells, and I'd rather save those channels for structural features I can test separately later.

I'm reasoning about where the digit's bounding box sits within the 28x28 field: the 20x20 box is centred by centre of mass, so the vertical shift is limited to about ±4 pixels, and it depends on whether the mass sits high or low, as with a 7 or a 6. For templates, I'll need to compute each stroke's centre of mass.

I'm setting up the digit strokes in a normalized unit box, then scaling them so the bounding box fits a 20-pixel height (or width, if it's wider). After that I'll shift everything so the stroke centre of mass lands at the 28x28 field's centre, at 13.5.

I'm now turning the stroke samples into orientation responses, where each sample's angle is scored against the four filter orientations with a cosine-squared falloff, so a 22.5° stroke lands near 0.7 on the nearest filters and a 45° stroke barely registers on the horizontal one. I'm weighing how sharp that tuning should be, since a 5x5 filter with a width-3 stroke probably responds only around 0.2 to 0.3 at 45° off, and I'm still deciding the exponent that matches that.

I'm checking how the grid A footprint maps onto the pixel field: a conv2 output at row r pulls from pool1 rows r+1 through r+3, so its centre lands at pixel 2r+6.5, and each pooled cell i covers the two conv2 rows 2i and 2i+1.

I'm now placing the grid A cells at centres 7.5, 11.5, 15.5 and 19.5, and working out how a stroke at a given pixel row feeds into each cell's footprint, with a plateau near the centre that tapers off over a few pixels on either side.

I'm settling the footprint falloff: a plateau of full weight within about two pixels of each grid cell's centre, tapering to zero at six pixels away, so the cell responds mainly to strokes near its centre.

I'm settling the footprint falloff as a smooth ramp that drops to zero a few pixels from each cell's centre. Along the stroke, I'll weight each sample by its length and by the spatial and orientation responses, then scale the total so a long straight stroke through a cell gives roughly a unit value.

I'm settling how the template value should be scaled: summing each sample's length times its spatial and orientation responses, then dividing by the footprint's total, so a long straight stroke through a cell comes out near 1. I'm considering capping the result at 1, or applying a mild compression, since only the relative shape of the templates matters.

I'm checking whether grid B should sit two pixels above or below centre, since its cell positions would then run 9.5 to 21.5 or 5.5 to 17.5, and that asymmetry matters for where the template lands.

I'm weighing whether a second grid with a two-pixel offset is worth the extra channels, or whether I should use channels 4-7 for a narrower, non-overlapping version of the same grid to capture finer structure.

I'm now weighing how grid B should be offset, whether shifted by two pixels in both directions or only in one, since each option moves its cell centres and changes how the left and right strokes of digits like 5 and 3 fall across the cells.

I'm sticking with the baseline: grid A on channels 0-3, a quincunx-style offset grid B on channels 4-7, and channels 8-15 left at zero for now so any problem traces back to the orientation channels.

I'm now sketching the digit shapes as centre-lines in a height-1 coordinate system, starting with the 0 as an ellipse centred around the middle of the box.

I'm drafting the digit 1 as a vertical stroke with a slight lean, since real MNIST ones range from upright to roughly 30° to the right. That means the template should also pick up some of the "/" orientation, so I'm considering superimposing two variants to cover both.

I'm sketching the digit 1 as a near-vertical stroke with a slight lean, from top-right to bottom-left, so it mostly reads as vertical with some diagonal response. Its tilt is roughly 11 degrees, which puts most of its energy on the vertical channel and a smaller share on the "/" channel.

I'm defining the four orientation filters for the first convolution, with each angle's response falling off with the perpendicular distance from the kernel centre.

I'm now defining the orientation filters as ridge profiles that depend on each pixel's perpendicular distance from the kernel's centre line, with a Gaussian falloff. I'm then leaning toward a zero-mean version so flat regions give no response.

I'm checking whether a wider core is needed for thick strokes, since the σ=1.0 profile gives a narrow positive band and the thicker MNIST strokes might not fill it well.

I'm checking the stroke profile against the bold-digit case: a wide, heavy stroke would score only about 0.2 on the centre-weighted template, while a thin one scores around 0.67, so the zero-sum profile is hurting thick digits.

I'm weighing whether to relax the zero-sum constraint on the stroke profile, since strict zero-sum weights hurt thick strokes, and considering whether a slightly positive total would help or whether a bias term could separate strokes from flat regions.

I'm checking whether a slightly positive sum on the stroke profile, something like [-0.25, 0.11, 0.5, 0.11, -0.25], helps thick strokes without letting perpendicular ones through too easily. Aligned thin and typical strokes still score well, and bold digits recover a lot of response, though the perpendicular ratio of about 0.27 is still something I need to judge.

I'm checking whether the perpendicular leakage of about 27% is acceptable, and whether a small negative bias could suppress it. Keeping the profile strictly zero-sum would be cleaner, though thick strokes would then score weaker. Since cosine matching is scale-invariant, that might be fine as long as all orientations weaken together. I'm also running a thick-stroke case by hand and getting a normalised response around 0.47 on the edge row, which looks better than I expected.

I'm finishing the zero-sum Gaussian profile with σ=1.0 for the horizontal and vertical filters, since it still gives thick strokes a response near 0.45. For the diagonal filter I'm working out the mean over the 25 cells from their distances to the centre line, which puts the on-line weight at about +0.44 and the next band at about +0.22.

I'm normalising the first-layer responses and checking the bias, settling on a small negative value so the weak cross-talk drops out. Then I'm moving to the second convolution, where the first four channels get an outer-product grid A kernel.

I'm setting up the fully connected layer's weight matrix, indexing the flattened features by channel and position, and I'm about to fix how those entries map onto the pooled 16-channel grid.

I'm now working out how each stroke point deposits weight into the pooled grid: a point's position maps to a conv1 row and then to a pool1 row, with some spillover to neighbouring rows at reduced strength.

I'm working out how each grid-A cell collects stroke weight from pool rows 2i+2 and 2i+3, with weaker contributions from the neighbouring rows, so that for the first cell strokes at pixels 4–5 count at half weight.

I'm working out the Gaussian falloff for the footprint function, weighting cells by distance and tapering them to zero beyond a few pixels. I'm thinking the templates should be a bit blurrier than the exact footprint so they tolerate position variation of about two pixels.

I'm laying out the digit templates now, starting with the 0 as an ellipse.

I'm placing the ellipse for the digit 0 as a slightly slanted loop, then sketching the 1 as a near-vertical line with about a 10° lean. Next I'm starting the outline of the 2, beginning with its top arc.

I'm sketching the digit 2's top arc as a circle about a quarter of the way down, sweeping from the upper-left around over the top, then down to the right. I'm starting the next section of the 3 as an upper arc centred near the top of the digit.

I'm sketching the digit 3's lower arc as well, then moving on to the 4, where I'm weighing an open-top version with a left stroke, a horizontal bar and a right vertical stroke.

I'm sketching the 5 as a top bar running leftward, then a short stroke down the left side and a bowl curving round on the right.

I'm placing the digit 6 as a loop at the bottom, starting from an arc that sweeps down the left side from the top.

I'm sketching the digit 7 as a top bar with a diagonal stroke running down to the lower left, leaning about 19° from vertical. Then I'm moving on to the 8, which I'm starting as two stacked loops, a smaller upper one and a larger lower one.

I'm working out the shape of the 8 as a figure-eight: a parametric curve where x follows a sine of twice the angle and y runs smoothly from top to bottom, so the two loops cross at the centre.

I'm checking the figure-eight parametrisation at its key points: the top, the crossing at the centre where the tangent is diagonal, and the bottom. The curve's widest extent falls near y≈0.15 and y≈0.85, where the loops bulge outward.

I'm sketching the 9 as a small loop at the top with a stem running down its right side, slightly slanted toward the left at the bottom. Then I'll scale all the digits so they're about 17.5 pixels tall, allowing for stroke thickness within the 20-pixel box.

I'm checking the digit 7 against the centre-of-mass rule: its top bar sits near y=0 and the diagonal runs down to the bottom, so the centroid lands around 0.32 of the height, which puts the top near row 8 and the bottom past row 25. I'm working out whether shifting the image up by a few pixels within the 20-pixel box keeps the tip from being clipped.

I'm checking the digit 7's centroid against the MNIST convention, where strokes sit in a 20-pixel box and the image can shift a few pixels, so its bottom tip landing near row 25 is expected. I'm also confirming the grid coverage ranges for the A and B templates and that the tapering covers the edges.

I'm estimating the magnitude of the feature vector x more carefully rather than guessing: a stroke's conv1 response is around 0.6 along its centre for a matching orientation and about 0.4 when it's 22.5° off, which carries through pooling and the second convolution to roughly 0.6 per active cell, with some extra from spillover into neighbouring rows.

I'm estimating the total feature mass by spreading each stroke point's weight across the grid cells and orientations, which gives a rough per-cell magnitude near 0.5 to 1 for the active cells.

I'm estimating the total feature mass in the grid more concretely: a stroke of roughly 46 pixels, with each pooled cell around 0.6 and the second convolution's kernel summing to about 2, gives a sum near 28 over the conv2 map before max-pooling. Max-pooling then keeps only a fraction of that, so I'm checking what per-cell magnitude that leaves.

I'm estimating the feature vector's magnitude at about 3.2, so the own-class projection comes out near 2.2 against roughly 1.0 to 1.6 for the other classes. That puts clean-case logit gaps around 0.6 to 1.2, and I'll set the scale α to 4 to bring them into a workable range.

I'm going back and forth on the temperature: if accuracy is around 70%, the average loss lands near 0.9 to 1.0, so over-confidence is a moderate risk, and I'll keep α at 4. I'm also wondering whether the cosine between similar digits like 3, 5, 8 and 9 is really as low as I assumed, since their blurred orientation maps probably overlap more than that.

I'm weighing whether cosine or Euclidean matching holds up given the uncertain feature amplitude, and I'm leaning toward cosine with a tunable per-class bias.

I'm checking whether a "1" with little ink still gives a clear margin against the other templates, and it does: its own-class logit sits about half an α above the rest. I'm also thinking that a bold 8 should overlap little with the 1 template, since its crossing strokes are diagonal and horizontal while the 1 template lives in the vertical centre columns.

Writing conv1 filter setup code...

Still writing conv2 weights...

I'm putting together the template-building code now, with helpers that sample each digit's strokes as short segments and record their positions, angles and lengths.

Still writing the template code...

Still working through the template code, and now I'm weighing how to handle the 1 digit, which appears both as a near-vertical stroke and a slanted one in MNIST, so I'm considering adding polylines at different slants and blending them with weights.

Still working on the 7 template and its crossbar, weighing a short horizontal stroke through the middle of the diagonal against leaving it out.

I'm weighing a slanted variant of the 1 and 9 strokes, since MNIST digits lean slightly right, but I'm leaning toward skipping extra variants for the 4, 2 and 9 to keep the templates simple.

I'm settling the shear: rather than drawing each digit slanted, I'll draw them upright and apply one global shear of about 0.1 to everything, which gives roughly a 6-degree lean. For the 9 I'll set the stem to run from near (0.23, 0.2) down to (0.2, 1.0) before shearing, and I'm still working out the left edge of the 4.

Still working out the 2's arc and the endpoints of its strokes, checking where the arc ends before the base line runs across.

Still working out the 3's arcs, checking that the upper bowl's bottom stub meets the lower bowl cleanly at the waist.

Still working out the 5's top bar and bowl, checking that the bowl's end meets the stem cleanly. Now I'm setting up the 6 as a large arc, placing its centre and radii before I work out its start point.

Still working on the digit 6 and 8 templates, and now I'm setting up the 9's loop and stem.

Still working on the 0 and 7 templates, checking the 4's left stroke: I'm weighing whether its top should sit further left to give it more of a slant.

Still working out the stroke weighting and scaling for the templates.

I'm checking the template for 1, where the vertical ink sits in the centre columns, and the grid cells near x=13.5 pick up equal weight from both neighbouring columns. I'm also setting the fully connected bias to zero and wondering whether the cosine matching will let one class dominate the predictions.

I'm deciding to keep the template channels at zero for now and rely on the baseline, since later steps can add structural features. I'm also double-checking the conv2 normalization against the template norm of 7.5.

Still writing the sampling helper...

Still working on the sampling helper, pinning down how to split each stroke into short segments and how the shear changes their direction.
