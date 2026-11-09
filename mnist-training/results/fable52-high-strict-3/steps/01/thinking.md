I'm sketching a hand-built CNN for MNIST: a 5x5 first conv with 8 channels, ReLU, and 2x2 max pooling down to 12x12. The second conv takes those 8 channels to 16 at 8x8, followed by another pool to 4x4, and a final fully connected layer maps the 256 features to 10 classes. I'm starting to work out how to set the first conv's weights by hand.

I'm weighing a template-matching approach: conv1 gets oriented stroke detectors in four directions, conv2 blurs and combines them into 16 channels on a 4x4 grid, and the final layer holds hand-drawn per-digit templates. I'm also working out how the conv2 receptive fields map back to pixel positions.

I'm working out where each final 4x4 cell's receptive field lands on the input: the top-left cells cover roughly pixels 0 to 15, and each step right or down shifts it by four pixels, so the cells overlap heavily. The digit sits in about the 4 to 23 pixel range, which is the box my 256 features need to cover.

I'm now working out how to set the FC weights by imagining digit shapes, since I can't look at the data. I can draw digit templates directly from strokes on a 4x4 grid for each orientation channel, as long as I don't run the network on those drawings.

I'm settling on the template approach: one hand-described prototype per digit, built from strokes in the orientation channels, rather than averaging generated samples. Drawing stroke weights directly into the templates feels allowed, since I'm not running the network on anything.

I'm weighing a simple design: first-layer 4-direction stroke detectors, possibly with polarity, so the network can tell which side of a stroke the ink sits on. I'm still settling how fine the orientation features need to be to separate digits well.

I'm considering whether the other channels could capture something beyond line orientation, such as ink blobs or curvature, though a 5x5 linear filter with ReLU makes end-stops hard to build. I'm also thinking about using eight finer orientations, but at 5x5 the angular resolution would be too coarse to help much. For conv2, I'm looking at larger combinations, like a horizontal stroke on top joined by a vertical one below and to the right.

I'm checking how the final 4x4 cells line up with the input when conv2 is a single center tap: each cell should cover roughly input centers 6 to 21 across the digit area, with the pooling setting the spacing.

I'm checking how the 4x4 cells line up with the input when conv2 uses off-center taps: a tap shifted by one pool cell moves each cell's coverage by 2 pixels, so 16 channels could cover four orientations at four sub-positions.

I'm weighing a max-pooling offset: with the tap at (3,3), each window covers pool cells 2k+3 and 2k+4, so combining offsets of 0 and 2 pixels could give the linear layer roughly 2-pixel resolution. I'm not sure that's the best use of the channels, so I'm considering blurring the conv2 kernels over small neighborhoods instead for tolerance. Still, I'm leaning toward the view that good oriented features with a trained linear layer reach around 97 to 98 percent, compared with about 92 percent on raw pixels.

I'm considering whether conv2 could detect loops directly: a unit that needs ink on all four sides of a center and none in the middle would respond to a hole, which might give the linear layer something more invariant than orientation alone.

I'm weighing a mixed design: orientation-map templates for most of the signal, plus a few structured loop detectors to separate 6, 8, and 9. Since I can't test anything, I want to start with a simple template approach, check accuracy through the feedback steps, and only then add the more complicated detectors.

I'm going to consider how the first-layer filters should be laid out, starting with the orientation options for the 5x5 kernels.

I'm laying out the first-layer bar detectors as zero-mean 5x5 filters, with a positive center line and negative flanks. A horizontal version responds strongly to a roughly 3-pixel-thick horizontal stroke and gives zero for vertical strokes, and I'm going to rotate that pattern to get the diagonal ones.

I'm weighing how the first-layer bar filters should be built as zero-mean profiles that respond to strokes but not to flat ink, and I'm considering the eight-direction edge option as well. I'm not sure it helps much at this resolution, so I'm looking at what the second layer can extract instead.

I'm checking the receptive field arithmetic for each final 4x4 cell: with a center tap, cell k covers input centers 4k+6 through 4k+9, so the four cells span 6 to 21 and line up with the digit box. I'm also noting that strokes near the box edge, around rows 5 or 22, would only register partially in the outer cells.

I'm considering whether a 3x3 blur in conv2 would make the template more tolerant to shifts, at the cost of some precision. Pooling over a wider window would give overlapping 8-pixel regions at stride 4, and I'm weighing that against using four orientations at fine resolution versus four orientations at several shifts.

I'm settling on the nearest-centroid form for the final layer: each digit's logit is the dot product of the features with its template, minus half the template's squared norm, which makes it a Euclidean prototype match when the features are on a comparable scale to the templates. Negative weights go where a stroke is not expected, such as horizontal ink at the top to separate 1 from 7.

I'm comparing nearest-mean style templates on oriented pooled features against raw pixels, which tops out around 82% on MNIST, and I expect hand-drawn prototypes to land somewhat lower. I'm considering using confusion-matrix feedback to tune biases and templates, and adding structural conv2 detectors to push past that.

I'm now considering a loop detector for conv2: a unit that needs ink on all four sides of a center and none in the middle, so it would fire on a hole. The difficulty is that a linear sum can't enforce a true all-four-sides requirement, and the one-sided ReLU outputs of conv1 don't saturate, so the threshold would be fragile.

I'm comparing the digit pairs that are hardest to separate with orientation features: 3 versus 8, 5 versus 6, 4 versus 9, and 7 versus 9. Each one hinges on a stroke that is present in one digit and absent in the other, so negative weights in the templates should help tell them apart.

I'm considering using the confusion matrix as a measuring tool: each row shows how often a true class gets predicted as each label, so I could design probe networks that test whether a feature exceeds a threshold, and read off per-class feature means from the results.

I'm thinking about whether the confusion matrix could serve as a measuring tool, since each step gives about 90 numbers and I'd be trading some of the 15 steps for information about per-class feature statistics. That bandwidth is too low to estimate hundreds of class means, so I'm leaning toward using the steps mainly to test hypotheses about the templates and then refine from there.

I'm going to stop trying to get the first design perfect and focus on writing a high-quality set of templates, since that's where most of the accuracy will come from. The one concern is that feature magnitudes vary with stroke thickness and total ink, so I need to check that the nearest-prototype formula still behaves sensibly, especially for the digit 1, which has little ink.

I'm checking how the nearest-centroid score behaves: each digit's logit is its template dotted with the features, minus half the template's squared norm, which amounts to Euclidean prototype matching. The catch is that the single template per class can't capture several shapes of the same digit, since a linear layer can't take a max over alternatives.

I'm weighing how to define each digit's template as expected features, possibly by subtracting the shared average so the classifier leans on distinguishing signals, and I'm considering hand-set negative weights where a digit should show no stroke, such as the "1" template.

I'm writing each class's weights as its expected template minus a penalty wherever that digit should have no stroke, with a bias to balance the classes that I'd adjust from the confusion matrix. Next I'm laying out the first conv layer's eight channels, starting with four orientation bar detectors and considering what the other four should capture, such as stroke endings.

Next I'm considering endings as features: a stroke terminating on the left, right, top, or bottom, which separates pairs like 3 and 5 or 2 and 7, and I'm checking whether a simple edge detector with a fixed polarity can capture that.

I'm working out an edge-ending detector for conv1: positive weights along the center row on the right side, negatives everywhere else. The aim is for a vertical stroke's edge to come out roughly neutral while a stroke that terminates shows a clear response, and I'm checking how a three-pixel-thick horizontal stroke would behave under the same weights.

I'm working out a 5x5 edge-ending filter for conv1: rows 1-3 on the right side are positive, while the top and bottom rows and the left columns are negative. A horizontal stroke that stops partway should respond strongly, but a full stroke passing through or a vertical edge should cancel out, which means the negative weights need to be at least about 1.5 times the positive ones.

I'm settling on a corner case for the endings filter: the top-left and bottom-left cells stay at zero or slightly negative. A stroke that turns a corner would pick up a partial response, which is noisy but might still help, since absent orientation in neighboring cells gives similar information linearly anyway.

I'm now comparing which pairs of digits would be easiest to tell apart with orientation features: a 4 has two vertical strokes at the top and no horizontal cap there, while a 9 has a horizontal arc across the top.

I'm weighing whether to split the first conv's eight channels between four orientation detectors and four stroke-ending detectors, since endings could separate pairs like 3 and 5 that orientation alone might miss. I'm also considering whether conv2 could capture those endings more coarsely, so I'm not yet settling on one layout.

I'm thinking about how to turn the stroke drawings into feature values: I'd rasterize each digit as polyline strokes on a 0–1 grid, then deposit each segment's contribution into cells according to its orientation.

I'm settling on how to build each feature value: deposit a soft contribution per stroke segment according to its orientation and position, then cap the total at one. That keeps the templates in feature space and avoids fitting them to example inputs, which is the approach I want to stick with.

I'm settling on scaling the conv1 filters so that a stroke of the matching orientation and typical thickness produces a response near one, which keeps the bias calibration consistent with the real feature magnitudes.

I'm now considering a cosine-similarity classifier instead of Euclidean prototype matching: each digit's template gets normalized to unit length, so the score doesn't depend on how bold or thin the digit is. That would also remove the need for per-class biases.

I'm now weighing a cosine-style classifier instead, where each digit's template is normalized to unit length so the score doesn't depend on stroke boldness, and I'm considering adding a small negative penalty wherever a digit should show no ink.

I'm weighing whether a penalty for ink in unexpected places would shift the balance between classes, since a digit with few strokes like the 1 has a large penalty area. I'd rather let that play out than predict it, but I want the starting point to be principled, so I'm looking at a Gaussian-style model where each class's log-likelihood is a dot product with its template minus half its squared norm.

I'm weighing whether a plain Euclidean nearest-template classifier with calibrated scale will hold up, since a digit that matches no template well tends to pull toward the low-norm ones like 1. I'm planning to start there, check the confusion matrix, and tune the biases from it, and I'm considering how to push accuracy past roughly 80%.

I'm weighing 16 channels as four orientations times four window offsets, so the pooled features keep finer position information. I'm checking which conv1 tap offsets cover the 4-to-23 range without gaps.

I'm laying out the window offsets for conv2: taps 1 and 2 give two interleaved sets of 4-pixel windows that together cover the range from 4 to 21. I'm also considering a box-sum pooling alternative, which would smooth the features but lose some resolution.

I'm laying out the 16 channels as four orientations times four offset combinations, which gives a full 8x8 grid of window positions at stride 2 and 256 features in total. The window centers for the two tap offsets come out to 5.5, 9.5, 13.5, 17.5 and 7.5, 11.5, 15.5, 19.5, so together they cover eight positions.

I'm checking which conv1 tap offsets cover the digit's range without leaving gaps, and I'm weighing taps 2 and 3 against 1 and 2. Taps 1 and 2 cover centers 5.5 to 19.5, but strokes near row 22 would only be partly caught. Since MNIST digits are roughly centered on 13.5 and span rows 4 to 23, I'm thinking about whether that box works as the reference frame.

I'm checking whether shifting the conv1 filters by one pixel would center the window coverage on the digit's rows, so the 4-to-23 span is covered symmetrically.

I'm checking whether the conv1 tap offsets leave a gap or an asymmetry against the digit's 4-to-23 span, and I'm weighing the even-sized filter alternative, which would shift the centers by half a pixel. Taps 1 and 2 cover centers 4 to 21 and taps 2 and 3 cover 6 to 23, so neither is perfectly centered on 13.5.

I'm checking how the vertical extent of digits fits the window offsets: centering on mass shifts tops and bottoms, so the content spans roughly rows 3 to 24. I'm weighing whether to spend the offsets on rows with three positions instead of two, and dropping some column coverage to make up for it.

I'm checking whether the column offsets can be reduced to a single one, since digits are narrow and centered near 13.5, so one offset already gives four symmetric windows. That frees up channels for the rows, where I'm weighing three offsets against the digit's vertical extent, and I'm wondering whether the leftover channels should go to other variants or special detectors.

I'm checking whether the column windows leave a gap at the 13.5 boundary, since a vertical stroke there would split between two cells, which I think is fine because the sum still captures it. I'm also weighing the horizontal alternative of three column offsets, which would give 12 overlapping windows and cover the full width, though that starts to look like just the full 12x12 pooled map again.

I'm now weighing the 9 offset combinations against the 16 available channels, and whether to pick a 2x2 subset or spread offsets along one dimension. I'm also considering box-blur pooling in conv2 as a smoother alternative, and settling on a simpler view where each orientation's response map is aggregated in windows over a 12x12 grid.

I'm comparing the two tap pairs for the row offsets: {1,2} reaches down to about row 21 and leaves the lower tail of digits like 6 and 2 partly uncovered, while {2,3} shifts coverage downward. Neither lines up perfectly with the digit's center at 13.5, and the bottom edge of the digit is what I'm trying to weigh.

I'm checking the row offsets for the bottom edge: offsets {2,3} would reach row 23 but detect a 2's bottom stroke only weakly, while a mix of {1,2,3} for rows could cover the full span with overlapping windows.

I'm considering a conv2 kernel with weights 0.5, 1, 0.5 over neighboring pool cells, which smooths the row response before the max-pooling step. That would make each pooled window a triangular blend centered on the conv1 positions, so the coverage gaps I was worried about might close without spending extra channels.

I'm considering soft, triangular-weighted conv2 kernels in place of hard max windows, since they might be more forgiving for template matching. I'm also weighing a two-tap box kernel over neighboring pool cells as another way to get a centered window.

I'm checking whether two-by-two box sums over neighboring pool cells, at offsets that give centers 6.5 and 8.5 up to 20.5, cover rows 4 to 23 symmetrically around 13.5, with each feature a soft window about six pixels wide.

I'm settling on 2x2 box sums over adjacent pool cells, with two offset kernels per dimension, which gives 16 channels across the 8x8 grid. Each window will sum to roughly 2 when a stroke runs straight through it, with the neighboring cells picking up the spread of the bar response.

I'm now working out the flattened index for each feature: the channel comes from the orientation and the two kernel choices, and the position within the 8x8 grid maps onto the 16 slots per channel. Four orientations only use four of the conv1 channels, so I'm wondering what to do with the other four.

I'm weighing whether the spare conv1 channels could sharpen the orientation detectors, through two stroke scales or finer angles, but merging them back into broader channels gains little. I'm also asking whether 256 features is best spent on four orientations over an 8x8 grid, or on a different split of offsets and orientations.

I'm now considering whether the spare conv1 channels could go toward loop and ending detectors, which might separate digits like 4 and 9 or 3 and 8 better than orientation templates alone. I'm doubtful, though, that loop detection can be made reliable with just these two convolutional stages.

I'm considering a hole detector at conv2: the hole's center cell should have no ink while ink sits at a distance in every direction, so the response would need to reward that pattern across the four sides. Summing the four directional ink responses minus a threshold is the simplest form, though I can't take a true minimum with these operations, so the test stays approximate.

I'm checking whether a saturated background indicator, clipped at 1 for empty pixels and 0 where ink is present, could make a hole detector reliable, since it would stop thick strokes from inflating the directional sums.

I'm working out how to make a hole detector saturate: a conv1 background indicator clipped at 1 for empty pixels, then pooled so that a cell only counts as ink when all of its positions are strongly inked. The aim is to pick a threshold so the ink band is roughly one 2-pixel cell wide, so that a cell fully inside a stroke can be identified.

I'm checking whether a 2-pixel cell can sit fully inside a diagonal stroke, since that depends on how thick the band is at 45 degrees.

I'm checking whether a dilated ink band would fill in the small loops of 8, 6, and 9, since a 4-6 px band could close holes only 3-4 px across. The concern is that the background-indicator approach would erase exactly the openings a hole detector needs.

I'm settling on a background indicator that is clipped at 1 for empty pixels, using a small center-weighted blur so that tiny holes still register as empty. Pooling with max keeps a cell marked as background whenever any of its pixels is empty, so a hole's center cell should survive pooling. Then I'm working out how to mark a cell as enclosed by ink.

I'm working out how to make large loops detectable: a 5x5 conv2 kernel can't span a 0's hole, so closedness of big loops has to be inferred from stroke orientations at particular positions, such as an H-stroke at the top of a 9 versus the open top of a 4.

I'm checking whether bottom arcs and small loops are worth detecting explicitly, and I'm leaning toward skipping that for now. I'm turning to stroke endings next, since the four spare conv1 channels could carry directional ending detectors, and I'm wondering whether diagonal endings would still be picked up by the up, down, left and right ones.

I'm going through where the strokes end in each digit, noting for example that a 2 has an end at top-left and another at bottom-right, and that a 1 has ends at top and bottom. Those endings look distinctive enough that left-pointing and down-pointing end detectors might separate 3s and 5s from 9s.

I'm weighing whether the four spare conv1 channels could carry ending detectors, and then whether 16 conv2 channels would have to be split between orientations and column positions, since column placement matters nearly as much as row placement for a 20-pixel-tall digit.

I'm settling on a column layout for the orientation channels: a 3-tap kernel centered on each 4-pixel stride, with the effective window around 6 pixels, which gives an 8-row by 4-column grid. That would leave room for eight channels of orientation detail alongside the other spatial splits.

I'm comparing two options for the spare conv1 channels: finer column positions with more template detail, or four soft column windows at 7.5, 11.5, 15.5 and 19.5. The four-window layout looks adequate horizontally, since the vertical strokes of 4s, 9s and 7s would land in the center-right and right windows. I'm still unsure whether my hand-drawn templates are precise enough to justify eight column positions.

I'm now asking whether the 8 orientation channels should cover 8 rows by 4 columns, since digit heights are normalized and vertical placement is more reliable than horizontal. I'm also weighing a layout of four endings channels on a 4x4 grid against a 4x4 orientation grid with extra mid-level detectors, and I'm not sure yet which split serves the digits best.

I'm now adding composite features at the conv2 level, starting with concavity detectors that look for bays opening in a given direction. Digits like 3, 5, 9, 7 and 4 each have bays in distinctive places, which makes these features robust and discriminative.

I'm checking whether a 5x5 kernel's reach of about 4 px in each direction is enough to tell a 3's bays from an 8's loop. In 8's narrow upper loop, a cell on the right inside would see ink above, below and to the right, and nothing to the left, so the two cases look too similar.

I'm reconsidering whether the spare conv2 channels should go to corner or curvature detectors, since those would be built from horizontal and vertical features that are already present. The alternatives are a second offset for the endings or a coarse ink-density channel, which would give the pixel-template approach a cheap extra signal.

I'm settling on 8 conv1 channels as 4 orientation and 4 ending detectors, and making the conv2 layout symmetric with each group split across two row offsets. Before committing, I want to check whether a 5x5 ending detector can really pick out the stroke ends reliably, since MNIST strokes vary a lot in thickness. I'm starting with a left-pointing ending filter, where the stroke runs to the right of the center and the background sits to the left.

Now I'm writing the left-pointing ending filter: a positive block on the right side of the center with a negative block to its left, plus a negative band above and below. For vertical edges, the positive sum of about 6 needs only one unit of negative weight to match.

I'm checking how the ending filter responds to thick strokes: a 5-pixel stroke cancels out to zero, so only thinner endings would register. For a diagonal stroke end running toward the upper right, I'm looking at which cells carry the ink.

I'm checking how a diagonal stroke end would respond to the left-pointing filter, and it comes out weak, around 1.5. The down-pointing one looks similarly weak, so diagonal endings aren't well covered. I'm wondering which four ending directions would best serve typical digit endings, since 8 would be needed to cover them all.

I'm now weighing how well the ending detectors would hold up for each digit, since typical endings point in the four cardinal directions and I'd need to know where each digit's strokes terminate to decide how to lay them out.

I'm now thinking about how the ending detectors should respond: each stroke endpoint would be given a direction pointing outward, and the detectors would be tuned to the four cardinal directions. I'm also noting that corners and sharp curves only partly trigger these endings, which the templates won't capture. Next I want to consider how negative evidence and the classifier form fit together.

I'm weighing a Euclidean template rule against a cosine rule, since the cosine version doesn't depend on getting the feature scale right. I'm leaning toward cosine for the first pass, and I'll come back to whether mean subtraction helps.

I'm weighing a cosine rule against a Euclidean one, since cosine doesn't depend on getting the feature scale right, so I'll start there. To sharpen the classes, I'm considering subtracting a scaled mean of the other templates from each class template, since shared components cancel out and don't change the argmax.

I'm comparing the templates through their differences, since in a linear rule the choice between two classes depends only on the gap between their normalized templates. For a 7 image, the score for 1 depends on how much the normalized 1-template overlaps the 7's ink, so I'm checking whether that normalization leaves the 1 template too heavily weighted.

I'm considering why cosine similarity suits this: the best-matching template wins whenever the image matches it exactly, so errors come only from variation within a class. Blurred class-mean templates should help with that, and I'll likely add hand-set discriminant weights for confused pairs like 4 and 9 once I see the confusion matrix.

Now I'm settling how the templates should cover style variants, like slanted versus vertical 1s and crossbar versus no crossbar on 7s. A soft blur over each template should approximate the class mean, and I'll tune the rest from the confusion matrix.

I'm defining the orientation filters for the first conv layer: four 5x5 bar detectors at 0°, 45°, 90° and 135°, with the stroke direction set up in image coordinates. Each one would be a profile across the stroke, minus a constant so it sums to zero.

I'm making the orientation filters zero-sum along each stroke's cross-section, so a perpendicular stroke gives no response, though the diagonal ones only come close to that.

I'm working out how to normalize the orientation filters: rather than scaling them by their response to an ideal stroke, I'm considering scaling by the sum of their positive weights so the normalization stays simple and doesn't rely on running the filter on a generated input.

I'm making the first-layer filters zero-sum across the stroke, then setting their scale by the sum of their positive weights so a full stroke gives about 1.2. Thicker strokes should respond less, since their ink reaches the negative flanks, so I'm sketching a cross-profile with a peak of 1, shoulders of 0.6, and negative outer taps that balance it to zero.

I'm checking how thick strokes affect the response: a 4-pixel stroke gives about 1.1 and edges come out around half the ideal value. Bold writing still produces usable responses, so I'll tolerate that and maybe soften the negative flanks a little.

I'm considering a non-zero-sum profile with a slight positive bias, which would help with thick strokes but could hurt faint thin ones. I'll keep the filters zero-sum for now since that's simpler.

I'm building the diagonal orientation filters with a Gaussian cross-profile and an along-stroke envelope, but subtracting one overall mean won't make each column sum to zero, since the envelope varies across the patch.

I'm making the diagonal filters zero-sum by subtracting a Gaussian-weighted mean of the cross-profile, so the balance holds even where the along-stroke envelope varies. Then I'll scale each filter by the sum of its positive weights so a full stroke lands near 1.2.

Still writing the ending filters...

Still working out the negative flanks of the ending detector, weighing whether the background should be required at one column or two.

Still working out the negative flanks of the end detector, checking whether the corner case with a vertical stroke below and a horizontal one to the right gets penalized enough.

I'm checking the corner case for the end detector: with the filter shifted one pixel right, the vertical part of the corner gets heavily penalized, and with it shifted up, the horizontal stroke fills only two of the positive rows, so both placements come out well below the aligned response.

Still working out the end detector's negative weights, checking how strongly the background should penalize a vertical stroke that runs straight through.

Still checking the diagonal end-detector weights against a stroke running through the center.

I'm checking the end detectors' negative weights: one negative cell per top and bottom row, two on the left, and corner penalties, which works out to a net-negative filter, so thick ink won't trigger it. I'm also noting that a small blob will activate all four end detectors, and that diagonal ends respond only partially, which is acceptable.

Still working out the second conv's column window, weighing whether to use a centered soft kernel or plain three-column taps.

I'm working out the second conv's row grid: each output row takes two adjacent conv1 rows, so the centers land at 6.5 + 2m for m from 0 to 7.

I'm laying out the second conv's row windows: each output row covers two adjacent conv1 rows, with centers at 8.5 up through 20.5. The endings channels follow the same pattern. For the scale, I'm estimating a horizontal stroke passing through a window gives about 3, and a vertical one about 3 as well, so both sit in a similar range.

I'm settling the endings' scale: they respond more weakly than the orientation features, so I'll scale their conv2 kernels by about 0.7 to bring typical values near 1. Their relative weight against orientation can then be tuned through the template magnitudes.

I'm turning to how the templates will be indexed: one per feature type and digit position, with rows and columns mapped to pixel centers on the 28x28 grid. I'll describe the strokes directly in pixel coordinates, then deposit each sample point with its local stroke direction to build the response.

I'm defining the receptive windows for the second conv: row features are weighted fully within about 2.5 pixels of their center and taper off out to 4.5, and the column weights follow the same idea.

I'm now weighing how a stroke's partial coverage of a window should shape the feature value, leaning toward a trapezoidal falloff in the column direction so that a stroke crossing only part of the window still registers in proportion to its length.

I'm settling the feature scaling: a stroke that crosses a whole window should count as roughly 4 pixels of length, so I'll normalize by that to get a value near 1.

I'm now checking how a diagonal stroke tilted about 22.5 degrees responds to the horizontal and diagonal filters, since the template values depend on those partial responses.

I'm checking how the end-detector templates should respond at free endpoints, weighting each by how well its outward direction matches the filter. Then I'll turn to describing the digit strokes in pixel coordinates, allowing for the rightward slant typical of MNIST digits.

I'm going to position each digit so its center of mass sits at (13.5, 13.5), drawing the strokes in a nominal frame first. The code will then rescale them so the centerline spans about 17 pixels and recenter on the centroid.

I'm drafting the digit shapes in a unit box, starting with the zero as an ellipse of about 0.6 width relative to its height, with a slight rightward slant.

Next I'm sketching the digit shapes as centerline polylines in a unit-height box: the zero as a slightly slanted oval, the one as a near-vertical stroke leaning a touch to the right, and the two as an arc over the top that drops diagonally to the lower left and then runs across the bottom.

Now I'm sketching the digit shapes in pixel-free unit coordinates: the 2 as an arc over the top that drops diagonally to the lower left, then runs across the bottom to the right, with its start pointing down-left and its end pointing right.

Now I'm placing the digit shapes as centerline points: the 3 as a rounded top curving into a middle junction and a rounded bottom, and the 4 as a left stroke, a crossbar, and a long right vertical.

Still placing the digit centerlines: the 4 as a long right vertical with a left stroke and crossbar, and now starting the 5's top bar.

Now I'm working out the rest of the digit shapes: the 5 with a top bar, a short vertical, and a rounded bowl curving down to the lower left, and the 6 starting from the upper right and sweeping down into a loop at the bottom.

I'm drawing the 8 as two touching loops, a smaller one on top and a larger one below, and I'm working through how the crossing point between them should be drawn.

I'm parametrizing the 8 as a figure-eight curve, with y running from the top down through the center and x swinging left and right twice per loop. The crossing at the middle should come out as a diagonal X, since the x-offset peaks while y passes through the midpoint.

I'm checking the widest point of the figure-eight: a plain cosine parametrization puts it too high, so I'll raise the exponent to pull the loops out to around y≈0.2. If that still looks off, I'll just hand-place the points, tracing from the center out to the upper right and up over the top.

I'm finishing the 8 by hand as a point sequence through the crossing at the center, then sketching the 9 as a loop at the top with a tail running down to the bottom.

I'm applying a shared rightward slant to every digit template and weighing whether the 1s and 7s need separate handling, since real MNIST variation is large. I'll use a broader deposit window than the strokes themselves to imitate the position jitter in real digits, and then I'm checking whether the cosine-based normalization still holds.

I'm checking whether the output scaling holds up: the logits are roughly the feature magnitude times the cosine, so I'll multiply by a factor like 3 and tune it later from the loss. I expect accuracy somewhere around 60 to 75 percent before tuning.

I'm weighing whether cosine similarity is the right scoring rule, since a narrow single-stroke 1 that's slanted more than its template could lose overlap with the 1 template while still matching the broader templates less well than expected. I'll go with cosine first and compare against alternatives later using feedback.

I'm checking the 7 template's partial response and then working through the index conventions for the conv and pooling layers, so the geometry lines up before I write the code.

I'm working out the index mapping for the second pooling stage: the flattened feature index is channel times 16 plus row times 4 plus column. For the row offsets, the taps at each output row cover pooled cells that shift with the kernel offset a, which gives a pool center of 4k + 2a + 6.5.

I'm checking the pooling geometry for the second conv: the row grid runs over offsets 0 to 7, each centered at 6.5 plus twice the offset, and the column taps use weights of 0.5, 1, and 0.5 to set the center.

I'm checking how a single vertical stroke responds to the 5-wide first-layer filter: when it sits right on the filter's center the response is strong, but offset by one pixel it drops to about a quarter of that.

I'm checking how a vertical stroke lands on the pooled cells: the column cell under the stroke gets close to full response, its neighbors only a fraction of that, so the feature value comes out around 2.3 in the core and about 1.2 at the edges.

I'm checking how a diagonal stroke lands on the 2x2 pooling cells: the cells along the diagonal should give close to full response, with the neighbors touching it picking up a partial value from the max.

I'm setting the deposit window's row weighting so a full-height stroke counts for about four pixels of the template, which fixes the normalization constant.

I'm settling the deposit window's weighting: rows get full weight out to about 2.5 pixels and taper to zero at 4.5, so a stroke ending mid-window still contributes roughly 0.87 after normalization. I'll accept that as a rough match and add some variation tolerance. Columns use a trapezoid, full weight within about 2 pixels of the center and tapering to zero at 3.5.

I'm settling the column weighting for the deposit window: full weight within about 1.75 pixels of center, tapering to zero at 4.75. That gives roughly 0.58 at a 3-pixel offset. Checking the normalization, a horizontal stroke across the full column width comes out near 1 after dividing by 4, and a vertical stroke at the center also caps at 1, which keeps the template values in range.

I'm checking the deposit window's shape, since a plain cap would make a stroke's fringe look fully filled. I'm considering a narrower core width with a smaller normalization constant, which would still saturate for a central vertical stroke but leave offset strokes lighter.

I'm checking the horizontal stroke's response across the row window: it stays near full out to about 2.5 pixels from center and drops sharply past 3, so the row weighting should be flat over that range and then fall off.

I'm trying a shortcut for the deposit template: a hard cap on the row accumulation makes a vertical stroke's fringe look too full, but a soft saturation doesn't fit cleanly either. I'll keep the cap and adjust the window widths instead: row weight full to about 2.5 and zero at 4.0, column weight full to 1.75 and zero at 4.75, with the normalization constant set to 5. That gives a center vertical stroke a value of 1 and a stroke offset by 3 pixels roughly 0.75.

I'm checking the feature response for a horizontal stroke at the window center, where the template saturates to 1, and for a vertical stroke ending at the center, which comes out near 0.65. I'm settling on scaling the conv2 output by about 0.8 so the endpoint features land near 1, and I'll then weight each template cell by the row and column window values at that endpoint.

I'm weighing the endings separately from the orientation features: a digit's stroke gives roughly 35 units of mass across overlapping windows, while each endpoint contributes only around 3, so two endpoints total about 6. Weighting endings by 2 raises that to about 12, but since ending detection is noisy I'll settle on a weight of 1.

I'm now checking where the ending detectors could false-fire: a tight arc, like the top of a narrow 0 or the small loop of an 8, can look like the upward-pointing end of a thick stroke, so I'm weighing whether the filter's negative side around it is enough to suppress that.

I'm checking that a wide arc doesn't trigger the upward-end filter, since its sides land on the negative cells and cancel the positive response. Only a narrow loop with a hole of one or two pixels would partly fire it, which I'll accept. I'm starting to define the positive block weights for the left-pointing end detector.

I'm finishing the normalization for the endpoint detector: an ideal three-pixel end would sum to about 6, but with antialiasing and rounding a realistic stroke end comes closer to 4, so I'll divide by 4. For the bias, I'm leaning toward a small negative value around −0.1 so that weak off-orientation responses don't add up across the six cells of the second conv.

I'm now setting the classifier weights for each digit template as a cosine-style match, scaled by the endpoint importance and normalized so each class's weight vector has the same magnitude. I'm also noting that since all features are nonnegative, the cosines will sit high overall and the separation between classes will come from their differences. I'm checking whether a strong central vertical stroke in other digits, like a 4 or a 9's tail, could push the "1" template's response up.

I'm checking the "1" template's response against a 9's tail: the horizontal offset from x=13.5 to x=16 shows up mainly in the k=1 and k=3 column windows, so there is enough separation to keep the two apart.

I'm moving on to the digit shapes themselves, starting with a 0 drawn as an ellipse with a slight rightward slant, and I'm thinking about how the polylines should be placed inside the 20-pixel box.

Now I'm placing the digit-1 stroke and the digit-2 outline points inside the 20-pixel box, while settling the slant.

I'm laying out the digit-3 polyline now, with its top arc and a middle bend where the stroke doubles back, and I'm checking how the pieces connect.

I'm placing the digit-4 strokes: a left diagonal from the top, a crossbar near the middle, and a long vertical on the right, and I'm checking which way the left stroke should lean once the global slant is applied.

I'm placing the digit-5 polyline inside the box, starting from its top-right corner and sweeping left across the top bar before curving down to the bottom. Its endpoints point right at the start and left at the end, and I'm checking how the top bar will sit.

I'm writing out the digit-6 polyline, starting it at the top right and curling down through a loop, and noting that its start points up and to the right. Then I'm defining the digit-7 stroke as a top bar sweeping left to right and a long diagonal down to the bottom, with the global slant still to be applied.

I'm settling on a per-digit slant rather than one global value, since a 7's stem leans more than a 1 needs to. For the 7, the stem from its top right to its bottom works out to about 27 degrees from vertical, which sits within the usual range. Next I'm defining the digit 8 polyline, then the digit 9 as a loop starting at the right side and sweeping counterclockwise.

I'm giving each digit its own slant, around 0.15 for most and 0.2 for the 1, and I'll scale the drawings so the larger dimension is 17 pixels. Then I'll center each one on its centroid at (13.5, 13.5) and check the vertical extents.

Now I'm working out how the row and column windows line up with the digit's centered position, and how the orientation angles get defined from each stroke's direction.

I'm working out the first conv's filter form: each orientation filter weights pixels along the stroke direction with a Gaussian and applies a zero-mean profile across it, so the response peaks on a line at that angle.

I'm settling on a wider filter profile, σ=1.1 across the stroke, which gives a flatter centre and lets a 2-pixel stroke still register strongly.

I'm settling the profile function for the orientation filters: piecewise-linear knots at the center, at one pixel, and at two pixels, with the far tail held at the same negative value. For diagonal orientations I'll subtract the weighted mean so each filter sums to zero.

I'm checking the diagonal filter's sample values: a center of 1, about 0.72 at one diagonal step, and negative values beyond that. Subtracting the mean puts the sum at zero, which gives a diagonal filter with a positive center and negative flanks, and a diagonal stroke should fill its positive lobe.

I'm checking how the diagonal filter's positive lobe compares with a 3-pixel horizontal stroke: the diagonal comes out around 0.84 of the horizontal's response, which seems acceptable.

I'm settling the smoothing-related constants: the Gaussian weight along the stroke is flat or mildly peaked, and the across-stroke profile is zero-mean so that perpendicular strokes cancel. I'm also setting the conv1 bias to a small negative value and normalizing each filter by its positive mass, and I'm starting to lay out the channel order for the first conv.

I'm defining the edge-ending filters for the first conv: one for a stroke ending that points left, with ink on its right, plus its mirror for the right-pointing case. I'm also working out the vertical versions, pointing up and down, by swapping the roles of the axes.

I'm working out the second conv's kernel: each of the 16 output channels pulls from a pair of first-layer orientation channels, with a row-and-column weighting that peaks in the middle, scaled per orientation. The ending-feature channels get their own scaling and feed through the same pattern.

I'm now defining the fully connected weights: each class's template is indexed by feature channel, row, and column, and I'm considering whether to use a cosine-squared response for the stroke-end detectors, scaled by a tuning factor.

I'm settling on the classifier's final step: a cosine-based template score for each class, with a scale factor around 3 so the logit margins stay moderate. I'll tune that value and the other constants later.

Now I'm defining the template drawing function: it applies the slant to each point, resamples the strokes densely, shifts them so the centroid sits at the center, and accumulates orientation responses into a grid of cells.

I'm adding weighted variant strokes to the templates, such as a lighter crossbar on the 7, since some handwritten digits include them.

I'm settling on how the orientation weights ω get set, and I'm deciding whether to add variant strokes like a crossbar on the 7. I'm leaning toward skipping them for now to keep the first version clean. I'm also noting that the neighboring windows already overlap enough that extra blurring across rows probably isn't needed.

I'm reconsidering whether the cosine-based scoring will work for '1': a sparse template has few features, so its normalized weights are large, and slanted 1s may pull toward 7 or 2 instead. I'll check that against the confusion matrix once I have it, and I'm also thinking about normalizing the scores differently, perhaps with Euclidean distance rather than cosine.

Next I'm settling the cosine scoring and whether a Euclidean distance would be more robust, but cosine avoids having to calibrate feature scale.

Writing the orientation filter kernels now...

Writing the orientation filter kernels now...

Writing the edge-ending filters now...

Writing the second conv's kernels now...

Next I'm checking the grid positions for the template windows, and I'm working through the "1" template by hand to see whether a slanted stroke still lands in the right windows.

Now I'm picturing the "1" template's stroke angle and how its response splits between vertical and diagonal features, which should be fine. Next I'm going to start laying out the outline for each digit, beginning with the 0 as an ellipse.

Now I'm checking the 4's centroid, working through its two strokes and where their midpoints fall.

Now I'm checking the 7's centroid, weighing its top bar against the two stem segments to find where the horizontal midpoint lands.

I'm checking the 7's centroid against the bounding box: the top bar sits near row 8 and the bottom near row 25, which seems low, so I'm wondering whether the bounding box would push the digit higher.

I'm checking the typical width of MNIST digits next, and I want to confirm that the centroid shifts I just worked out, such as roughly 3.5 px down for the 7 and about 1.7 px down for the 9, fit how the digits actually sit in the frame.

Still writing the 8's polyline...

I'm checking the 5's shape and the 2's start, then settling the stroke-end flags. I'm also weighing whether to adjust the overall scaling and the fully connected bias, and I'm considering whether the cosine normalization is sound. I'm wondering whether real feature maps will carry enough background responses to blur the cosine scores.

Still writing the template code for the convolution weights...

Still writing the template code, now the helper that turns each stroke into segments and collects its free endpoints.

Still writing the template helper: it collects segments and free endpoints, computes the weighted centroid, and starts accumulating the orientation responses into the grid.

Still writing the template helper, now the endpoint pass that turns each free stroke end into an ending-feature response.

Still writing the template helper, now the code that maps each free stroke end into an ending-feature response.

Still writing the template weight code, now normalizing each class's features by the scaled template norm.

I'm checking the logit scale: with about five-unit feature norms and a scale of 3, the class margins land around 1 to 3, which seems reasonable. I'm also confirming that the ending responses in the second conv come out near 1, so the template peaks line up.
