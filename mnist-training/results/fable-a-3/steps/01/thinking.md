I'm sketching a small hand-built CNN for MNIST: two 5x5 conv layers with 8 and 16 filters, each followed by ReLU and 2x2 max pooling, ending in a 4x4x16 feature map. Now I'm working out how that 256-value map feeds the final fully connected layer to 10 outputs.

Now I'm tracing where each 4x4 cell sits in the input: the final pool cells center around input rows 7.5, 11.5, 15.5, and 19.5, each with a 16x16 receptive field, and the digit spans roughly rows 4 to 23. So the grid lines up with the digit, and I'm considering whether stroke-style templates can work at that resolution.

I'm settling on a single design step, and the first one needs to be solid. Rather than running the network on templates, I could hand-draw the fully connected weights directly from digit strokes, placing each segment's orientation into the matching channel at the nearest 4x4 cell, which is a legitimate way to build templates without executing the model.

I'm checking whether stroke-based templates really count as a legitimate design here, since I'd be converting digit strokes straight into fully connected weights without running the network. Drawing the weights directly from stroke descriptions seems allowed, so I'll go with that and place each stroke's orientation into the matching channel at the nearest 4x4 cell.

Now I'm weighing how to turn the first conv layer into useful features. Signed, orientation-sensitive edge detectors could give more shape information than plain bars, since they distinguish the two sides of a stroke. I'm also checking whether a hand-drawn template can get reasonable accuracy on 4x4 cells with those features.

I'm weighing whether conv2 should detect larger structures like curves, stroke endpoints, and junctions, or simply pass along the oriented edges so the fully connected layer can do the matching. Either way, the 4x4 grid is coarse, so each cell has to carry a lot of the shape information.

I'm considering how blurring conv2 would work: a uniform 5x5 kernel over the pooled map would make each final cell summarize a broad 12x12-pixel window, with cells overlapping at a 4-pixel stride. That keeps tolerance high but covers only the central region of the digit. A linear classifier on raw pixels might reach around 92% when trained, and hand-drawn templates would likely land well below that, maybe 60-70%, while a trained classifier on oriented, pooled features could exceed 98%.

I'm now sketching the first conv layer as oriented line detectors, with a horizontal-line filter built from a center row of positive weights and negative flanks.

I'm working out the first conv layer's horizontal-line filter: a center row with positive weight and flanking rows with negative weight, which gives a response of about 2 on a 2–3 pixel stroke and stays zero on uniform ink.

Now I'm writing out the first conv layer's diagonal filters, weighting pixels by their distance from the stroke's center line, with a negative bias to suppress weak responses.

I'm sketching the first conv layer's diagonal filters by weighting each pixel according to its perpendicular distance from the stroke's center line, with a profile that is positive at the center and falls off to negative at the flanks.

I'm settling the first conv layer's filters from a formula over the angle: each pixel's perpendicular distance from the line, zero-summed, and scaled by the sum of its positive weights so the strongest possible response is 1.

I'm weighing whether the four remaining conv1 channels should be signed edge detectors, with top, bottom, left, and right edges kept separate, so that conv2 can spot stroke endpoints by checking for a line with no ink above it.

Now I'm thinking about which features actually matter for telling digits apart. Loops and holes are the classic cues, but detecting an empty center surrounded by ink is hard for a single conv layer at this scale, so I'm considering a rough center-surround approximation built from summed ink around the hole.

I'm weighing whether a ring-shaped detector for the hole in digits like 0 can work here, since a single linear-plus-ReLU layer only approximates it. Then I'm considering a different route: classifying on oriented feature maps with coarse position, and planning to tune the weights against the confusion matrix, for example by adjusting how 4 and 9 are separated.

I'm now laying out the next conv2 channel groups: endpoint detectors for stroke ends in each direction, checked against which digits have endpoints where, and then concavity detectors that respond to ink on three sides with an opening on the fourth.

Now I'm weighing how to split the remaining conv2 channels: a few for curvature and arc shapes, a few for a blurred ink mass, and maybe one for a rough hole or junction detector, since the 4x4 grid leaves little room for anything finer.

I'm now thinking about building each digit's weights from an expected feature map, taken from its stroke templates in 28x28 coordinates and centered on the 4x4 cells that cover each stroke point, and then subtracting the mean across digits so only the distinctive features drive the classification.

I'm weighing the template-matching route: the fully connected weights could be set to the prototype of each digit, with a bias that offsets its squared norm. That depends on the prototype matching the real feature scale, which I can't check without running the network, and a mismatch would favor digits with more ink.

I'm considering whether to make the features scale-controlled with saturating responses, since conv1 outputs are bounded and pooling and blurring keep conv2 bounded too, so the scale mismatch would be easier to manage.

I'm considering whether I can compute the expected feature map directly from stroke templates by rendering the digit and running the conv net, but that's ruled out, so I'll approximate the features geometrically instead. I'm aiming for a feature-space formula where each final cell's response comes from the max over the 2x2 conv2 positions of the pooled orientation map, so the expected values can be predicted without running anything.

Now I'm checking each cell's coverage on the input: with the 12-pixel effective window and a stride of 4, cell 0 sees rows 2 to 13, cell 3 sees rows 14 to 25, and the windows overlap so the whole 4-to-24 digit span is covered.

I'm checking the coverage of each final cell with a smaller 3x3 kernel, which would give 8-pixel windows with stride 4, sharper localization but less tolerance to shifts. Then I'm weighing a 5x5 Gaussian-weighted kernel as a middle ground, and wondering whether conv2 could carry richer signed context, such as endpoints and curvature direction, rather than just blurs.

I'm now weighing which digit pairs the orientation-and-position template can separate, such as 4 versus 9 by whether the top is closed, and 3 versus 5 by which side the top vertical sits on. I'm settling on four line-orientation channels with matching templates, and I'm considering signed edge detectors for the extra conv1 channels so conv2 can tell the top edge from the bottom edge.

I'm noting that the edge detectors add little at this 4x4 resolution, since top and bottom edges blur into the stroke itself. I'm considering instead using the four extra conv1 filters for finer orientation, eight directions spaced 22.5 degrees apart, because slanted verticals in digits like 1, 7, 4, and 9 could be told apart more reliably that way.

I'm now considering a pair of 5x5 conv1 filters for endpoint detection: one that fires on a vertical stroke ending in the lower half of the patch, with negative weights on the upper rows to suppress continuing lines. That would be a cleaner signal than the extra orientation channels, though I'd need to check that it doesn't just duplicate what the orientation filters already capture.

I'm checking whether a signed endpoint filter can avoid firing on horizontal strokes, which would mean adding negative flank weights so that a wide horizontal line cancels out.

Now I'm checking the filter for stroke ends: a top-edge response cancels out because the negative flanks balance the positive center, so only a vertical line ending in that patch gives a strong response.

I'm checking whether a 5x5 endpoint filter in conv1 holds up, and it does on thin strokes but breaks down on thick ones, since the negative flanks cancel a wide stroke's response. So I'm considering endpoint detection at the pooled conv2 scale instead.

I'm thinking about whether a conv2 endpoint detector could work on the pooled orientation channels: positive weight on the vertical channel at the cells below the top, and negative weight on every channel in the rows above, so only a stroke that stops there fires. The open question is whether it would also respond to the top of a 0.

I'm now reasoning about whether a 5x5 top-end detector would hold up, since the left arm of a 4 and the right arm sit about four cells apart and the region above them should be empty. I'm also conceding that endpoint features are hard to rely on because MNIST handwriting varies a lot, so I'd have to assign their weights by rough guesses rather than by anything I can verify.

I'm weighing whether to use 8 orientations instead of 4 at conv1, since finer angles might separate slanted verticals in digits like 1, 7, and 4 more reliably. Before settling the numerics, I'm thinking through how the feature magnitudes will come out.

Now I'm weighing whether to use eight orientation channels at 22.5-degree spacing instead of four, and how conv2 could draw its extra channels from the same orientation maps by sampling them at a half-cell offset.

Now I'm checking how a 3x3 kernel offset by one pooled cell would land on a half-step grid, working through the conv1 row indices to see where each cell's centre falls.

Now I'm working out where the pooled cells fall in the input: a kernel centred on one set of conv2 rows lands at input centres 5.5, 9.5, 13.5, and 17.5, while the shifted kernel lands at 9.5 through 21.5. Together they would cover the full grid at 7.5, 11.5, 15.5, and 19.5, so two half-offset variants could give a finer sampling.

I'm settling the grid question: shifting the conv2 kernel by one pooled cell gives centres at 5.5 to 17.5, and the centred kernel gives 7.5 to 19.5, so the two together barely add resolution. I'll leave the extra conv2 channels for structural features in later steps.

I'm settling on an eight-orientation set for the first conv layer, since broader angle coverage may help tell apart slanted verticals in 1, 7, 4 and 9. Next I'm working out how a line filter at a given angle should respond to strokes of different widths and positions.

Now I'm weighing whether four orientations at 45-degree spacing are enough, since a stroke at 22.5 degrees still gives roughly half response in its two neighbours. Eight orientations would overlap more and code angles more smoothly, but for hand-set templates four should do, which would leave the remaining conv1 filters free for other uses like signed edges.

Now I'm weighing signed edge features against unsigned line orientations, and concluding that at this coarse 4x4 resolution the top and bottom edges of a stroke blur together, so signed edges add little and line filters remain the better choice.

Now I'm estimating the stroke profile: about 2 to 3.5 pixels wide after normalising to 20x20, with intensity peaking near 1 in the centre and fading at the anti-aliased edges. That gives a rough ink mass of 2.5 to 3.5 per unit length, and a typical digit's stroke runs about 40 to 50 pixels, which I'll use to sanity-check the feature magnitudes.

Now I'm weighing the typical stroke width against the ink count, landing on about 3 pixels. For a horizontal line detector I'm considering a five-tall profile with negative outer rows and positive centre rows, which responds strongly to a centred stroke of that width but only weakly when the stroke sits a row off.

Now I'm testing how a zero-sum line filter handles thick strokes: a 5-pixel-wide stroke fills its whole window and cancels to zero. A positive-biased profile would keep responding to blobs, which might be the better signal for bold writing.

I'm weighing whether a saturating nonlinearity could keep feature magnitudes steady across thin and thick strokes, since the zero-sum filter and the bias threshold each trade off one case for the other.

I'm considering using the eight conv1 channels as paired positive and shifted ReLU responses to saturate feature magnitudes, since max pooling commutes with this clipping. That would let conv2 compute a clipped stroke signal that stays steady across thin and thick strokes.

I'm considering saturating the conv2 input by pairing each orientation channel with a second, higher threshold, so the features become near-binary and thin and thick strokes look the same. I'm also wondering whether the same trick should apply at the fully connected layer, though that would halve the number of feature types there.

I'm weighing how much a count-style feature for stroke length depends on where the stroke falls relative to the pooling grid. A 3-pixel stroke can cover one or two pooled rows depending on alignment, so the same stroke could read as noticeably stronger or weaker. That makes me wonder whether these length features are reliable enough to use on their own.

Now I'm weighing whether saturation is needed at the final layer, or whether a graded linear response is enough there. I'm also sizing the conv2 feature set: four orientation blurs plus about twelve structural detectors, such as endpoints and curve types. Next I'm picking thresholds for the saturated conv1 outputs so thin, faint strokes still register.

Now I'm checking how the saturated orientation channels respond to strokes at angles in between: a stroke about 22.5 degrees off still drives two neighbouring channels fully, so each channel covers roughly ±28 degrees, which is good enough coverage.

Now I'm checking the horizontal line filter numerically: a three-pixel-wide stroke centred in a five-row profile gives a response of about 2, and the soft anti-aliased edges pull that down a little.

Now I'm checking how the thick-stroke response falls off, since a 4-pixel stroke against a zero-sum filter drops to about 0.5 while thinner strokes still give 1.4 to 2.

I'm comparing a milder, non-zero-sum surround profile against thick strokes: a solid 5-pixel stroke only gives about 1 per column, while a 3-pixel stroke gives around 1.7. A vertical stroke of width 3 would still add up to about 3.6 across the window, which is uncomfortably high.

Now I'm checking a middle-ground surround with a small non-zero sum, which should balance thin and thick strokes: about 7.6 for a width-3 stroke versus 4 for a solid one. The first ×5 column sums come out near 7 to 7.5 for typical strokes, and I still need to check the orthogonal case.

Now I'm checking a diagonal stroke against the same filter: at the centre column it gives a response of about 1.1, and the neighbouring columns pick up partial coverage as the stroke shifts off the filter's centre row.

Now I'm working through the diagonal case column by column: the centre column gives about 1.1, and the columns one and two away pick up partial overlap as the stroke shifts off the centre row.

I'm working through the diagonal case, where a stroke at 45 degrees gives a response of about 3.7 against the milder filter, about half the horizontal case. With a zero-sum profile the diagonal total drops to roughly 2.7, so I'm comparing how each surround choice separates the orientations.

Now I'm checking how the thick-stroke response drops off: with the zero-sum filter, a 4-pixel-wide stroke only reaches about 0.36 of the ideal response, which would fall below the lower threshold and disappear entirely.

I'm considering whether edge detectors would handle thick strokes better than line filters, since an edge response should stay roughly the same however wide the stroke is. Their orientation tuning is broader, though, so I'd need to check how much that costs.

I'm checking how a diagonal edge fares against the same kind of profile: its response falls to about 6 from the aligned 10, since the ink region only partly overlaps the weighted rows. For a finite stroke, the columns near the centre pick up most of that response.

Now I'm checking a different angle: a five-pixel edge-style profile responds to thick strokes as well as thin ones, but its tuning across orientations is too broad to separate them cleanly, so I'm weighing whether oriented line filters with a longer reach could handle thick strokes instead.

Now I'm checking the thick-stroke case with the filter placed off-centre: against a solid stroke at the edge, the response holds at about 1 per column, so the response doesn't vanish for wide strokes after all.

Checking the thick-stroke case with the surround shifted off-centre: the soft edge drops the response to about 0.75 per column, so about 3.75 across five columns, roughly half the ideal thin-stroke response. Thin strokes still land near 7.5, so the filter keeps a clear margin between them.

Now I'm testing a profile with smaller outer weights, [-0.75, 0.25, 1, 0.25, -0.75], to see how it handles thick strokes.

Now I'm checking the thick-stroke case with the sharper outer weights: a solid stroke gives about 0.75 per column, and a softer edge about 0.6, so the ratio to the normal response is roughly 0.6 to 0.7. On a 45-degree diagonal the same filter totals about 2.1, against 5.25 for a normally-oriented stroke.

Now I'm checking the thin diagonal stroke: its cross-section is about 2.1 pixels, so the centre column gives a partial response and the neighbouring columns add a little more.

Now I'm checking the thin diagonal case, where the response at 45 degrees comes out to about 0.83 against 6.25 for an aligned thin stroke, so thin strokes are tuned sharply. The thick diagonal still needs working through.

Now I'm defining a filter profile as a function of distance from the centre line, tuned so diagonal orientations can be built from the same shape.

I'm calculating how the pixel distances map onto the profile values for the diagonal filter, and the weighted sum comes out to about 3.3 instead of zero. So I'll shift every diagonal weight down by roughly 0.13 to make the filter zero-sum.

Now I'm checking the diagonal filter's sum: the positive weights come to about 8.8 and the negative ones to about 5.5, so I'll scale the negative side to balance them out.

I'm normalising each diagonal filter by its own ideal response instead of the horizontal one's, since their positive-weight sums don't match, and I'll just hand-set those constants.

I'm now trying a windowed diagonal filter, cutting off the corners with a circular aperture, but that would shift the H filter's sum too. So I'm leaning toward a Gabor-style formula with a Gaussian envelope and a DC correction instead.

I'm now weighing a Gabor-style filter built from a cosine across the stroke with an isotropic Gaussian envelope, which should make its response roughly equal across orientations. I'd then subtract the mean to make it zero-sum, and check the rough response values at a few distances from the centre.

Now I'm sketching the next row of the Gabor-style filter, with the envelope weights and cosine values for the centre row and its neighbours.

Now I'm checking the thick-stroke response against the normal one for this filter: a wide stroke gives about 2.3, and a softer edge about 1.9, against 3.2 for a normal stroke, so the ratio stays around 0.6 to 0.7.

Now I'm writing out the H filter as a 5x5 array, with outer rows at -0.75, middle rows at 0.25 and 1, and normalising it so a normal-width stroke gives about 1.05.

Now I'm checking the thick-stroke responses once more, which land around 0.6 to 0.75, and noting that MNIST strokes are usually close to saturated. I'm also weighing how stroke ends and curves reduce the response, and where the pooling thresholds would cut off short segments. Next I'll define the diagonal filters by perpendicular distance from the centre line.

I'm filling in the diagonal profile by distance from the centre line, trying values like 1, 0.4, -0.45, -0.9, -0.95 so the filter sums to zero.

Now I'm checking the thin diagonal profile, where the intensity at 0.707 comes to about 0.65 and the ridge spreads over the nearby columns.

Now I'm checking the thin diagonal against the thick one, which lands around 0.82 on the same normalisation, so the diagonal filters seem to hold their ground against the horizontal one.

Now I'm checking how the horizontal filter responds to a 45-degree stroke, which comes out weak, and how the diagonal filter responds to a horizontal stroke, working through the row-by-row weights.

Next I'm checking the diagonal responses: at 45 degrees they come out around 0.25 to 0.5, while a 22.5-degree offset should land nearer 0.8. I'm picking thresholds near 0.45 and 0.75 so that normal-width strokes saturate and off-angle strokes stay near zero.

Now I'm setting the conv1 biases: each channel takes its filter scaled by 1/5, with a bias of minus the lower threshold for the first four and minus the higher threshold for the rest. The difference between each pair of pooled channels will then lie between 0 and 0.3, so I'll scale the conv2 weights by 1/0.3 to compensate.

Now I'm checking how a thin stroke shows up in the first conv layer: after the filter and the threshold, its response across the stroke comes out to about 0.4, 1, 0.4, so the centre row dominates before pooling.

Now I'm checking how thin strokes come out of the pooled layer: the offset response falls below threshold, so they produce nothing in that orientation.

Now I'm estimating how a horizontal stroke's pooled response grows with its length, accounting for the ends where the filter isn't fully covered.

Now I'm working out how the pooled stroke masses add up across the conv2 kernel, and trying to turn each stroke's contribution into an expected feature template.

I'm checking whether building a feature template from hand-described strokes, by rasterising them through an analytic window, still counts as drawing templates rather than generating example inputs and learning from them.

I'm checking whether subtracting a cross-class mean template would amount to fitting weights statistically, or whether it's just a normalisation that leaves the softmax unchanged. I'm leaning toward keeping the bias as a simple function of the template itself, since that reads as hand-drawing the weights rather than learning them from generated examples.

I'm settling on the template-matching approach: each digit's fully connected weights are drawn directly from stroke layouts, with a per-template energy term in the bias so heavier-ink templates aren't favoured. I still need to check whether the features' actual magnitudes line up with the template scale.

I'm weighing whether a single nearest-prototype rule on these features will hold up against the class biases the energy term introduces, and I'm considering a global gain to correct systematic over-prediction of heavier templates like 8 and 0. I'd also like to check whether the positive-and-negative evidence form of the logit works better here than the plain template match.

Now I'm estimating how well a single hand-drawn prototype per digit might do on these blurred orientation features, guessing somewhere in the 60 to 80 percent range before refining it against the confusion matrix. I'm also considering whether the remaining twelve conv2 channels should be used now or left for a later step.

I'm weighing whether a few extra conv2 channels could be spent on finer and coarser blur scales of the same orientation maps, since a fine window and a coarse one might complement each other better than a single Gaussian-like kernel.

Now I'm considering shifted sampling grids: offsetting the conv2 window by two pixels in rows and columns would place the pooled cells at more positions, giving 16 channels across four orientations.

Now I'm weighing whether to spend the remaining conv2 channels on shifted sampling grids, which would cover the edges better but mostly repeat interior positions, or on structural features that could do more work but can't be tested yet. I'm leaning toward giving them small initial weights so I can still debug if accuracy turns out poor.

I'm keeping step one to pure four-orientation templates with the other conv2 channels zeroed, so I can tell which part fails if accuracy is poor. Once that baseline works, I'll tune the gains and add features. I'm also thinking about how the max-pool after conv2 interacts with the kernel, and how each conv2 output maps onto the final pooled cells.

I'm modelling the second conv layer's kernel as a tapered window centred on each final pooled cell, with a response that stays full within about four pixels of the cell centre and falls off to zero by about seven.

Now I'm sorting out the shape of the final window: I'm treating the second conv kernel as a tapered window that counts fully for strokes within about four pixels of a cell's centre and half-weight out to six, and I'm considering whether a smooth falloff is a better fit than those steps. Now I'm asking whether a window that wide is actually what I want, since each cell would then pool strokes over a twelve-pixel region.

Now I'm comparing a narrower 3x3-style window against the wider tapered kernel, checking how far each one's support reaches from a cell's centre.

Now I'm weighing a 3x3-style window against the wider tapered one: the narrow version gives a crisp tiling where each point lands in about two cells per axis, while the mid-width kernel with half weights at the edges should tolerate deformation better. I'm leaning toward the smoother mid-width kernel, and now I'm starting to work out how much each stroke adds to the feature value.

I'm estimating how much each stroke adds to a feature: a horizontal or vertical stroke contributes about half its length in pooled cells, while a diagonal one spreads its response over neighbouring cells, so its contribution is smeared across a wider area.

I'm working out how a diagonal stroke spreads across the 2x2 pooling blocks: when it lines up with a block it stays in one cell, but when it straddles blocks its response gets split across neighbouring cells.

I'm estimating how much each stroke adds to the feature: a horizontal or vertical stroke contributes roughly 0.7 per pixel of its length inside the window, and diagonals come out about 1.3 times that per unit length because they touch more pooled blocks, so the two are close enough to treat alike for now.

I'm settling on a tapered kernel for how strokes contribute to each feature, with a tuning curve that fully saturates for orientation differences up to about 20 degrees and drops to zero by 40. I'm now checking whether a 22.5-degree offset lands right on the saturation threshold.

I'm settling the tuning thresholds: strokes near 0 degrees saturate, and I'm checking whether a 22.5-degree offset still counts as fully saturated or falls just short.

Now I'm settling the tuning curve as a falloff that reaches zero around 45 degrees, and I'm noting that across the four channels a stroke at an intermediate angle counts twice as much as one aligned exactly with a channel.

Now I'm defining the diagonal filters: the "/" one keys on stroke pixels where r + c is constant, and the "\" one on where r − c is constant.

I'm working out where each final pooled cell sits in the input: the second conv unit's center lands at 2u+6.5, so the four final cell centers come out near 7.5, 11.5, 15.5, and 19.5 pixels.

Now I'm checking how the final cell centres line up with the image centre at 13.5, and noting that MNIST digits are scaled to a 20-pixel box and centred by mass, so strokes typically span rows 4 to 23. I'm estimating centre-line extents of about rows 5.5 to 22.5 and widths that differ by digit, with 1s narrow and 0s wide, and I'm starting to think about how the first conv filters should respond to those strokes.

I'm placing the digit template in normalised coordinates, mapping the vertical range to rows 5 through 22, and I'm checking how much horizontal extent a typical digit needs. I'm also noting that centre-of-mass centring will shift lopsided digits like 7, 9, 4, and 6, so I'll have to account for that offset.

Now I'm settling how digits get centred: I'll compute the stroke-weighted centroid of each drawn template and shift it so the centre of mass lands at the image centre, the way MNIST preprocessing does.

I'm settling the slant and scale for the digit templates: about 8.5 pixels per unit vertically, with the same horizontal scale, and a mild rightward lean of roughly 0.12 so the strokes sit close to the vertical channel's tuning.

Now I'm checking whether the tuning response for a stroke 15 degrees off vertical really reaches the diagonal filter at about 0.83, since the raw curve at that offset looks like it would only give around 0.77. I'm unsure of the exact value, so I'll work out the horizontal filter's response to a stroke at angle δ to calibrate the curve.

Now I'm checking how a horizontal filter responds to a stroke tilted at angle δ, working through the per-row weights column by column as the stroke shifts vertically.

Now I'm checking the horizontal filter's response at δ=22.5°, where the stroke's vertical offset at the edge columns comes out near 0.41 and 0.83 rows. Averaging the per-column weights gives roughly 0.78, after allowing for the slight widening of the stroke.

Now I'm checking the horizontal filter's response at steeper tilts: at 30° it drops to about 0.67, and at 37° it falls to roughly 0.2 to 0.4 once the stroke widening is accounted for. That points to a tuning curve that saturates near 22.5° and is essentially zero by 45°, with the transition somewhere around 30° to 37°.

Now I'm comparing the horizontal filter's response at a thin stroke with a narrow tuning peak, where a 22.5-degree tilt still gives a strong but smaller response than the thicker stroke, and the falloff is steeper past the saturation point.

Now I'm adjusting the tuning curve so it maps orientation offsets to a response from 1 at 22.5° down to 0 by 41°, and I'm setting the per-pixel mass for each channel, around 0.7 for the horizontal and vertical ones and a bit higher for the diagonals. I'm still weighing whether the mass should differ for horizontal strokes once the max-pooling after the second convolution picks the best alignment.

Now I'm setting the scale of the fully connected layer, since the squared distances between the feature map and each class template will run into the hundreds, so the multiplier has to be kept small to avoid overconfident outputs.

I'm setting the logit scale α to about 0.03, since class-template distances run into the hundreds and a larger multiplier would make the outputs overconfident. I'll check the loss afterward and adjust α up or down from there.

Now I'm setting up the digit prototypes in normalised (u,v) coordinates, with a helper for drawing lines and arcs so each digit's strokes can be built consistently.

Now I'm setting the digit 0 as an ellipse with a wider horizontal radius, about 0.62 against a vertical radius of 0.95, since MNIST zeros tend to be round and broad. For the 1 I'm starting a near-vertical stroke with a slight rightward lean at the top, roughly 0.2 of slant.

Now I'm checking the slant for the 1 digit: a 14-degree lean should make the vertical channel fire strongly while the diagonal channel picks up some of it, which is acceptable. Some real 1s have flags or base serifs, but most are plain strokes, so I'll leave those out and start working on the 2.

Now I'm defining the digit 2 as a top arc, a diagonal down to the bottom left, and a base stroke along the bottom.

Now I'm defining the digit 3 as two arcs open to the left, with the upper one centred slightly left of the middle and the lower one a bit wider and running down to the bottom.

Now I'm sketching the digit 5 prototype, starting with a top bar that runs across from the right.

I'm laying out the digit 6 prototype next, starting from a stroke at the top right that curves down and to the left into a loop.

Now I'm working out the digit 6 prototype: a curved stroke from the top right down to the left, meeting a loop at the bottom.

Now I'm refining the stroke for the 6: a quarter-ellipse arc from the top right, stopping just short of the top, where the tangent is nearly horizontal. I'm considering whether the top should be steeper, closer to a vertical tangent at the start.

Now I'm trying a simpler way to trace the 6's top stroke, since an ellipse with these radii makes the top too flat, and I'm thinking about a polyline starting near the top right.

Now I'm working out the digit 8 as two stacked loops, starting with the upper one centred near the top.

Now I'm working out the figure-8 prototype, trying a Lissajous-style curve so the two loops cross at the centre instead of meeting tangentially.

Now I'm working out the figure-8 prototype as a Lissajous-style curve, where the two lobes are widest at about 0.7 of the vertical radius and cross at the centre.

Now I'm working out the digit 8 as a figure-eight curve, with the two loops crossing at the centre, and I'm setting the digit 9 as a loop at the top with a stem running down the right side. After that I'll apply the global slant and centre the digit.

Now I'm figuring out the centering for the 7: the bar and the diagonal each get a centre point and length, and I'm averaging them weighted by length to find where the centre of mass falls.

Now I'm checking how the template's shift from the centre of mass lands in the image, which puts the 7's lower end near row 26, and I'm deciding that this is acceptable since real MNIST sevens often sit a couple of pixels low. Next I'm turning to the bias term and how it enters the matching score.

Now I'm weighing whether cosine-style matching, with templates normalised to unit norm, would make the score less sensitive to the feature map's overall magnitude than the current dot-product-with-bias form.

Now I'm weighing a cosine-style match with unit-norm templates, where the score depends only on the angle between the feature map and each class template, so the overall feature magnitude stops mattering.

Now I'm estimating the feature-map norm from the template side, working out the stroke length and how many cells each point touches for the digit 0.

Now I'm estimating the feature-map norm by summing the template weights and their spread, which gives a norm around 34, so with the other classes scoring about 0.5 to 0.8 of that, the gaps come to roughly 7 to 17, and an α near 0.25 to 0.3 would keep the logit margins reasonable.

Now I'm settling the matching score: using unit-norm templates with a cosine-style dot product, so the result depends only on the angle to each class and not on the feature map's overall magnitude. I'll start with α = 0.25 and no bias, and adjust later from the loss.

Now I'm weighing a fine-scale version of the same templates with a narrower kernel, which would localise strokes more tightly at the cost of a little more complexity.

I'm weighing whether a coarser kernel, something like [0.5, 1, 1, 1, 0.5], would be more forgiving of the 2-3 pixel misalignment between my hand-drawn prototypes and real digits. I'm leaning toward coarse-only for the first run so I get a clean baseline confusion matrix, and I'll revisit endpoint or other features later.

Now I'm weighing whether to normalise each class template to unit length, so that a simple stroke like the 1 isn't unfairly favoured over richer digits. Cosine similarity would then depend only on the angle between the feature map and each template, which looks like the more robust choice.

Now I'm writing the weights for the coarse channels of the second conv layer, each one a blurred kernel with a positive entry for its own orientation and a negative entry for the opposite one.

Now I'm checking the pooled max-ReLU difference for the paired channels, which keeps the normalised weight between 0 and 1.

Now I'm writing the rasteriser for the templates: sampling points along each stroke and weighting them by how well their local orientation matches each of the four channels.

Now I'm writing the rasteriser's stroke-sampling and the per-channel weights, and I'm deciding to skip saturation effects at junctions and stroke ends.

Still writing the rasteriser's convolution filters...

Still writing the rasteriser's filter values...

Still writing the rasteriser's filter values...

Now I'm settling the digit shapes: I'll scale each one so its vertical extent spans 17 pixels, keeping the aspect ratio, and apply a slant of about 0.15, stronger for the 1.

Still writing the digit prototypes as point lists...

Still working out the digit prototypes as point lists, and I'm now defining the 4 as a left arm, a crossbar, and a stem that sits slightly lower than the arm.

Still writing the digit prototypes as point lists, and I'm checking the 5's stroke endpoints against the bowl arc so the joint lines up.

Still writing the digit 7 prototype as a horizontal bar and a slanted diagonal, checking that both lines land within the typical tilt range.

Still writing the digit 9 and 8 prototypes as point lists...

Now I'm checking the 9's centre of mass: the loop and stem average out to a shift of about 2 pixels down, which puts the loop near row 11.5 and the stem's lower end near row 24.

Now I'm comparing the 4 and the 9 on their top closure and their crossbar, which are the features that separate them once the image is blurred, and I'm noting that the differences are small enough that their cosine scores could end up close.

Now I'm checking whether a larger α or added structural features would help, since the 4 and 9 templates differ only slightly and their cosine scores may end up close.

Now I'm estimating the logit gaps from the feature norm of about 30 and the cosine differences of roughly 0.05 to 0.3, which puts α at around 0.25 to 0.4, so I'm leaning toward 0.35 and checking whether a wrong guess stays bounded if my norm estimate is off by a factor of two.

Still writing the prototype code, with the 4 and 9 and the conv filter setup, and I'm picking α near 0.3 for the temperature.

Still writing the convolution filter definitions...

Still writing the convolution weights for the second layer...

Still working out the pixel-space templates for each digit, including the rasteriser and the weights that map strokes onto the 4x4 cells.

Still writing the template rasteriser, sampling points along each stroke to build the digit prototypes.

Still writing the template rasteriser's filter values...

Still writing the digit prototype point lists and the FC weight setup...

Still writing the digit prototypes as point lists and the FC weight setup...

Still checking the digit shapes: I'm confirming the vertical scale keeps each digit within 17 pixels and that the wide ones don't come out taller than they are wide.

Still checking the digit 2 and 3 arcs: I'm confirming the start and end angles place the strokes where the shapes need them, and that the vertical range runs from about -1 to 0.97.

Still writing the 5's bowl arc, checking the start and top points against the endpoints.

Still writing the digit 8 and 4 prototypes, and I'm scaling the upper and lower lobes of the 8 differently so the bottom reads wider.

Now I'm checking the "1" template, since the vertical stroke and the slanted stroke end up with nearly equal weight, so an upright 1 would only score about 0.76 against its own template.

Still checking the "1" template: a slant of 0.18 keeps an upright 1 scoring about 0.88 on its own template, and a 20° lean still scores around 0.92. For the other digits I'm considering a slant of 0.12 as a middle ground.

Now I'm checking the weight layout and dtype for the conv and FC arrays, and confirming that the pooled max-ReLU differences behave correctly.
