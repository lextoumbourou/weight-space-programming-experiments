I'm sketching a small hand-built CNN for MNIST: 5x5 convolutions with 8 filters first, then a second 5x5 layer going to 16 channels, with pooling in between and a 256-unit fully connected layer at the end. For the first layer I'm planning to use oriented edge and stroke detectors.

I'm weighing whether conv2 can be a simple smoothing pass-through with extra combination channels. The harder part is the FC layer: I'd need to hand-write per-digit templates over the 16 channels and 4x4 positions, drawn directly in feature space since I can't run the network on inputs to check them.

I'm settling on rendering the templates straight from the stroke geometry, binning stroke density by orientation onto the 4x4 grid, rather than running the network on any digit images. Next I'm working out where each pooled cell's receptive field lands in the input, so the feature-space templates line up with the actual spatial positions.

I'm working out the 4x4 final-cell centers in input coordinates, which land at rows 7.5, 11.5, 15.5 and 19.5, and checking how that lines up with the 20x20 digit box. Each cell's receptive field depends on the conv2 kernel, so with a 5x5 blur it covers roughly a 12x12 region, and since neighboring centers are only 4 pixels apart those regions overlap heavily.

I'm checking whether a 4x4 grid over the central region fits the digit box, which runs from row 4 to 23. A full 5x5 conv2 kernel would give a cell at row 7.5 coverage of roughly 1.5 to 13.5, so the coverage holds. A more localized kernel would give tighter receptive fields, and those would overlap the conv1 extent at the edges of the grid.

I'm considering using offset kernels in conv2 so that each channel samples the conv1 features at a shifted position, which would give finer spatial coverage on the 4x4 grid. I'm also weighing a simpler route of one conv2 channel per conv1 feature. Without data to check against, I think template matching on soft features is the sturdiest approach, though I'd expect only moderate accuracy until the weights are tuned.

Now I'm working out how to set the conv1 filter geometry, with the stroke width still to settle.

I'm settling the stroke width at around 2–3 pixels and trying a horizontal line detector with a profile that is negative at the outer rows and positive in the middle. I'm checking its response on a centered thick stroke and on a vertical crossing.

Next I'm settling the Mexican-hat-style profile for the diagonal detectors: a perpendicular-distance function that peaks at the center, drops negative on the flanks, and gets its mean removed so the filter sums to zero.

I'm thinking about whether the other four first-layer channels should be finer orientations, edge detectors with polarity, or a simple ink-density channel. The fully connected layer is linear over pooled features, so template matching on four orientation maps at 4x4 might reach around 80%, and I'm weighing how much the extra channels would add.

I'm weighing whether hand-set prototype weights can get anywhere near trained-network accuracy, and I expect something like 70–80% at first, which I'd then push up using the confusion matrices. For the 16 conv2 channels, one option is 4 orientations at 2 spatial offsets, so each feature gets sampled at two shifted positions.

I'm working out how conv2 kernel offsets could sample the pooled grid at finer spacing, using one-tap or small kernels so each final cell reads shifted pooled positions.

I'm checking which pooled rows a single-tap conv2 kernel reads at each offset, since the 4-pixel cell spacing means each cell covers two pooled rows. An offset of 0 reaches pooled rows 0–7, an offset of 4 reaches 4–11, and an offset of 2 sits centered at rows 2–9.

I'm checking the pooled-row coverage for the border of the digit box: a single-tap centered kernel reaches input rows 4 to 23, but a stroke near row 5 falls on pooled row 1, which that kernel misses.

I'm working out which pooled rows a 4-tap kernel would need to cover so that strokes near the top border of the digit box still register. Shifting the taps to span pooled rows 2a+1 through 2a+4 would reach the rows a single centered tap misses.

I'm checking how the 3x3 taps at offsets 1 through 3 cover the pooled rows, which gives cells that overlap by two pooled rows and reach from row 1 to row 10. That lines up with the border of the digit box. I'm also considering the 8 remaining conv2 channels and whether they should be shifted versions of the same taps.

I'm now turning to the non-linear features that conv2 could compute, since linear combinations would be redundant with the fully connected layer. Hole detection, meaning an ink-free area surrounded by strokes, looks like the most useful target, because it would help separate digits like 0, 6, 8 and 9.

I'm checking whether the ring-and-center test can work with the summed orientation channels as a stand-in for ink, since a hole should show zero response in the middle while the surrounding strokes stay positive.

I'm now considering what the eight first-layer filters should be. One option is four line orientations plus four other channels, but I'm leaning toward signed edges in eight gradient directions, since each thin stroke produces two opposite-polarity edges that the 4-pixel cells would otherwise blur together, and polarity can still locate the stroke within a cell.

I'm weighing whether conv1 should use four line orientations plus four curve or corner detectors instead of finer orientations. Corner shapes that open in different directions seem more discriminative for digits like 3, so I'm considering arc-like L-shapes for the remaining channels.

I'm weighing whether a robust base with later tuning beats a more elaborate curve-detector design, since arc-shaped features would be hard to get right without visual feedback.

I'm settling on defining each digit as a few prototype strokes in a 20x20 box, with variants for things like slanted 1s or open 4s. I'll render their expected feature maps analytically by sampling points along each stroke, weighting them by orientation tuning and spreading them over the final cells, after recentering each prototype on its center of mass and scaling it to fit the box.

I'm checking whether computing feature maps from hand-described prototype strokes falls under the rule against running the network on synthetic inputs, and I'm reading that rule as allowing templates built directly from stroke descriptions.

I'm now deciding whether a single hand-drawn stroke template per digit is acceptable, with optional weaker strokes folded into the same template, and I think that's fine. The open question is whether subtracting the mean template across classes counts as discriminant analysis, which I want to avoid, so I'm looking at nearest-prototype scoring as the alternative.

I'm settling on a pure template-matching setup: each class gets a weight vector equal to its prototype and a bias that scores the squared distance. Dropping the cross-class mean changes nothing, so I'll leave it out. The remaining worry is that templates ignore ink appearing where a class expects none, and I'm considering explicit negative weights to handle that.

I'm now checking how a single-scale template's response should be calibrated against real strokes, so that the feature magnitudes line up with the template weights.

I'm making the features saturate by splitting the activation into two ReLU channels, one at x and one at x−1, and combining them with opposite signs in the fully connected layer, so the response is effectively clipped at 1 regardless of stroke intensity. I still need to check that the max-pool step keeps this identity intact.

I'm noting that saturating the features with a pair of ReLUs, one at x and one at x−1, would clip the response at 1 and keep the max-pool step intact. I'm also weighing whether simply letting the template amplitude vary with stroke thickness would be good enough, especially for thicker strokes.

I'm weighing edge detectors against line detectors here, since signed edges in eight gradient directions should respond the same way regardless of stroke thickness, and each boundary of a stroke gets its own response.

I'm checking whether a line detector with a symmetric profile holds up across stroke widths, since its response swings from strong to zero as the stroke thickens. Wider profiles and an edge-based alternative that doesn't depend on thickness are the options I'm weighing.

I'm checking the edge-filter response numbers: a horizontal edge filter with a [-1,-1,0,1,1] row profile gives full strength on a stroke at least two pixels wide, but only about half on a single pixel line, and a blurred 3-pixel stroke lands somewhere in between.

I'm working out how a diagonal stroke would respond to the horizontal edge filter, and the 45° case only gets partial credit. Because gradient filters respond with a cosine-like falloff, neighboring orientations overlap a lot, so I'm considering a sharpening step to tighten the orientation tuning.

I'm now looking at a thresholding alternative, which would depend on contrast, and considering whether elongating a thin filter along the edge sharpens its orientation tuning. For a tilted edge, the response would depend on how far the edge's position shifts across the filter's columns.

I'm checking how a 45° stroke responds to the horizontal line filter, and the partial overlap across columns suggests the tuning is broad whichever filter type I pick. Even filters should cancel a diagonal stroke more sharply than edge filters do.

I'm checking how a 45° stroke of width 3 responds to the horizontal line filter: its partial overlap across columns gives about 3 against 10 for an aligned stroke, so selectivity is decent. For thickness robustness I'm considering a mixed profile with a stronger center weight, to see how the response changes for widths 1 and 2.

I'm checking how a thick stroke's edge responds to the line filter: at the first ink row the response drops to about half, so the filter still picks up bold strokes at their boundaries, and max pooling should carry that through.

I'm weighing a saturating clip on the line-filter response, since a profile like [-1, 0, 2, 0, -1] gives a steady value for thin strokes and about half for thick ones, which keeps presence features robust. Clipping that response would yield roughly binary per-cell orientation maps. I'm also wondering whether the other four first-layer filters could cover the in-between orientations.

I'm weighing a second grid offset for the conv2 channels, shifted by half a cell, to get finer spatial localization. Handwriting variation may outrun that finer resolution anyway, so I'm not sure it's worth the extra channels.

I'm going through which digit pairs tend to get confused, like 4 versus 9, 3 versus 5, and 5 versus 6. For most of them, the orientation maps already contain the distinguishing stroke, such as the top horizontal bar on a 9 or the lower-left loop on a 6, so I'm leaning toward keeping the eight first-layer filters as they are.

I'm considering using the remaining filters for stroke endpoints, since an endpoint shows ink at the center with a ring around it that has ink in only one direction. A linear threshold can't cleanly capture that, so I'm wondering whether a combination of ink and ring sums could work instead.

I'm weighing whether thickness-normalizing the endpoint test is worth the effort, since a ring-versus-center comparison would double its response on through strokes and make the threshold fragile. Then I'm considering whether the confusion matrix from a few probe steps could tell me which digit pairs need dedicated features.

I'm considering whether the feedback from each step could serve as a measurement, with the predicted class encoding a binned feature value, so that the confusion counts give per-class feature distributions. I'd only get around three bits per step that way, but that is still a usable signal.

I'm weighing how much a step-by-step feedback signal is worth against just tuning the classifier directly on loss and accuracy. Each step's confusion matrix carries far more information than the scalar loss, but spending steps on feature measurements is slow next to using them for real tuning. Before settling on the approach, I want to check how well hand-drawn templates can actually work in feature space, so I'm about to write the generator that turns strokes into orientation density on a 4x4 cell grid.

I'm settling on a naive Bayes style score for the templates, where each feature's presence probability is clipped to a safe range so that both unexpected ink and missing expected ink get penalized in log space.

I'm settling the template scoring so that each feature's presence probability is scaled down to tame overconfident logits, and then I'll tune by adjusting class biases from the confusion matrices.

I'm looking at whether the remaining first-layer filters should cover edge directions or line endings. Using the extra capacity for more features could make the templates more robust, since each of the eight feature types gives a 16-cell presence map to work with.

I'm considering conv1 channels 5-8 as nonlinear conjunction detectors, since purely linear combinations of the orientation maps add nothing new. A hole detector for closed loops could separate 0, 6, 8, and 9 from the rest, and a top-closure feature might resolve 4 versus 9.

I'm thinking about which features to put in the remaining first-layer filters, starting with stroke endpoints since they separate digits like 3, 5, 2, and 7 well. Ordinary orientation maps already capture much of that, though. For a first pass I'm leaning toward four signed edge detectors pointing in the cardinal directions, since they're simpler to hand-design than endpoint or loop detectors.

I'm considering larger-scale filters in conv2, which see 10x10 pixel windows, to pick up long strokes like horizontal bars on 7s and 2s or vertical stems on 1s, 4s, and 7s, with position as a discriminating cue.

I'm thinking about long-stroke detectors in conv2, using 10x10 pixel windows to catch long horizontal bars and vertical stems with position as a cue, and I'm considering curve detectors that respond to arcs opening in different directions.

I'm checking whether a conjunction of arc-segment responses can be picked out with a thresholded sum, since conv1 outputs aren't clipped and their magnitudes vary. Then I'm working through where each arc sits in the digits, such as the top cap and bottom cup on 0s and the top arc on 2s.

I'm checking which digits the arc shapes distinguish, like the top cap on 9 or the bottom cup on 5, and I notice these arcs mostly line up with the orientation maps already, since a right-opening arc is just a vertical edge flanked by diagonals. That makes arc detectors look largely redundant, though I still can't verify that cleanly yet.

I'm considering whether the remaining first-layer filters should be end-of-stroke detectors, perhaps four oriented ones, or line orientations at a 22.5° offset. Another option is spending a few channels on long-stroke detectors, a hole detector, or an ink-total channel. I'm weighing which of these I can write reliable templates for.

I'm working out the weights for an end-of-stroke detector: a positive response on the lower center column where a stroke terminates, with negative weights in the upper rows so that a stroke passing straight through cancels to zero.

I'm sketching a top-terminator filter: negative weights in the upper rows and across the outer columns, positive in the lower-center, so a stroke that ends at the top fires while a stroke passing straight through cancels out.

I'm thinking about whether thick strokes would break a top-terminator filter, since a 5-pixel-wide stroke could cancel its own response, so I'm leaning toward skipping that filter for now and deciding on the conv1 orientations for this first step.

I'm weighing whether a hand-made model could lean on invariant features like holes or endpoints more than on orientation maps, since their presence per digit class is something I can estimate with some confidence. A trained linear model on orientation features would probably reach the mid-90s, while templates built from simple orientations would likely land lower.

I'm working out how a hole detector in conv2 would pick out the closed loops in 0, 6, 8, and 9, using the expected inner sizes in pooled cells.

I'm working out a hole detector for conv2: the center pooled cell should be empty because the line filters see nothing inside a narrow loop, but the surrounding ring needs ink in every direction, and an AND across directions is awkward to express as a linear sum.

I'm checking whether a hole detector could rely on four orientation terms summed together, but a single strong response might stand in for a missing side, so a fixed threshold looks unreliable. I'm wondering whether saturation in the conv1 outputs could make those terms more uniform.

I'm checking whether clipping the conv1 responses is needed at all, since strokes already give fairly bounded, semi-binary outputs. Thick strokes would only drop to about half response, so a clip at 0.5 scaled by two might make the presence features more robust.

I'm weighing a hole detector built on a dedicated conv1 ink channel, where a pooled map that saturates near 1 is close to binary. The catch is that an empty center surrounded by ink in every direction is an AND across several terms, which a single linear sum can't express directly. I'm checking whether pairing left-right and above-below terms, each as an AND of two near-binary inputs, could recover that conjunction.

I'm checking whether a hole detector on pooled cells holds up: the ring needs ink at distance one or two in every direction, but a thick stroke on one side could compensate for a missing one, and zeros have holes too tall for a 5x5 pooled window to cover.

I'm checking whether a left-right enclosure test catches the open top of a 4, and whether a top-bottom test would also fire on the gaps in a 3 and on 2s and 5s.

I'm dropping the hole detector for now, since the AND across directions is hard to express linearly. Next I'm weighing whether to spend the 16 conv2 channels on position resolution instead, using four orientations at four sub-grid offsets to get a finer effective grid than the coarse 4x4 final map.

I'm looking at whether a finer effective grid could help: four orientations sampled at four sub-grid offsets would give an 8x8 layout at 2-input-pixel spacing, instead of the coarse 4x4 final map. The open question is whether that extra resolution actually helps hand-built templates, since class-average maps are blurry and finer sampling may add little for discriminating small details.

I'm comparing a trade-off: 8 orientations on a coarse 4x4 grid without clipping, versus 4 orientations plus 8 other channels with clipping. I'm also considering a different approach built on pixel-like templates, though I'm leaning against it. The bigger question is which errors would dominate with hand-built templates, such as slanted digits or varied shapes of 2, 4, 7, and 9, and I'll rely on iterative feedback to refine the templates.

I'm thinking about using some network capacity for probing measurements, where the logits are set so the predicted class encodes which threshold a feature falls under, which would reveal the per-class distribution of that feature.

I'm considering whether the feedback channel could serve as a measuring device, using logit patterns to read off class-conditional feature statistics from training data. That would be learning through the oracle rather than purely hand-writing weights, so I'm questioning whether it fits the spirit of the task.

Next I'm weighing whether to spend the remaining capacity on finer position resolution, and I'm wondering how much I can trust magnitudes I can only reason about by hand, since I can't run anything. Feedback over many steps should be the main way I refine things, with real classification attempts serving as candidates rather than any measuring trick.

I'm now setting up the conv1 line detectors: four orientations at 0°, 45°, 90°, and 135°, each computed over a 5x5 grid from the perpendicular distance to a line through the center. I'm still settling on the profile shape for how the response falls off with distance.

I'm settling on a smooth profile for the conv1 line detectors, a Gaussian-like center with a negative surround, sized so it covers the 2 to 3.5 pixel stroke widths typical of MNIST.

Checking the stroke-response profile for a 5-tap line filter: with the center weight at 2 and the outer taps at -1, a stroke of width 1 to 3 gives the same response of 2, while wider strokes drop off, so I'm testing how the output falls as the stroke gets wider.

Comparing two stroke-response profiles for the conv1 line filter: a 3-tap version with center 2 and outer taps at -1 holds its response across stroke widths 1 to 3, while a wider-lobed version with 0.5 side taps peaks a bit higher. I'm leaning toward the flatter version, then smoothing its profile so the diagonal orientations sample it evenly.

I'm settling the conv1 line filter weights: the profile goes from 2 at the center, to 0 at distance one, to -1 further out, and I'm normalizing so the positive weights sum to 1. That keeps the response near 1 for a full-ink stroke of 1 to 3 pixels across all four orientations.

I'm checking whether a small negative bias on the conv1 line filters would sharpen their orientation tuning and cut down on partial responses from strokes at other angles, though I'm concerned it might weaken faint strokes.

I'm settling the conv1 bias at −0.1 and checking that the horizontal filter sums to zero, so a flat region gives no response. Next I'm looking at how conv2 should be set up, and whether clipping, spatial offsets, or more orientations serve the hand-built templates better, given that digits are centered by their center of mass and their heights vary only a little.

I'm checking where the digit's center of mass lands: the strokes shift a digit down or up by a pixel or two, so I'm centering the rendering at about (13.5, 13.5) to match MNIST. The final-layer cell centers at 7.5, 11.5, 15.5, and 19.5 are symmetric around that point, so the grid lines up.

I'm weighing whether a 3x3 window summing the orientation responses measures how much of a straight stroke falls inside it, since a stroke crossing all three pooled rows or columns reaches about 3 while a short piece scores only 1 or 2.

I'm thinking about the window sum: a 3x3 pooled sum of each orientation response measures how much stroke falls in that cell, so clipping it at around 2 turns it into a presence signal. I'll use half of the channels for that clipped version and the other half with an extra offset, so the templates can tell a short piece from a long one.

I'm checking how the 3x3 box sum and max-pooling combine, since the effective window spans about four pooled pixels and cells sit two pooled pixels apart. I'm leaning toward the plain box weighting, then deciding whether the remaining eight channels should be four clipped features or eight unclipped ones.

I'm considering a different kind of conv2 channel: terminator detectors that fire at the ends of strokes in each of the four directions. The idea is to use the conv1 line channels plus an ink channel, and fire only when there is ink at the stroke's end and nothing above it, so through-going strokes and curves are suppressed.

I'm working out how to tell a stroke end apart from a stroke's edge: a stroke end would be ink at the center with nothing above it, but a horizontal stroke's top edge looks the same, so the test needs something more.

I'm weighing whether to use the remaining eight channels for eight orientation features or four plus a second scale, and I'm going through the hard digit pairs like 4 and 9, 3 and 5, and 7 and 9 to see which would help most.

I'm weighing whether the remaining conv1 filters should be signed edges that show which side is blank, but they look redundant, so I'm considering larger-scale ink gradients or eight orientations instead.

I'm trying a half-cell offset for the second grid, so the cell centers interleave with the first set rather than coinciding with them.

I'm now weighing 8 orientation channels against a finer 22.5° split, since a 5-long line filter only resolves orientation to about ±25 degrees. I'm still on the fence about whether the extra resolution pays off on the hard digit pairs.

I'm weighing whether a more elaborate hole detector in conv2, one that compares a blank center against ink in a surrounding ring, could beat the simpler orientation channels, though a linear FC layer can't express that kind of AND on its own.

I'm now testing a hole detector built from paired checks: a blank cell with ink on both left and right, and another with ink above and below. Each pair is an AND, so it could catch an enclosed gap that a single linear feature can't express.

I'm trying to make the enclosed-hole detector work with the orientation channels: a left-right check on a blank center, where the strokes on either side are roughly vertical. The trouble is that a plain sum of the neighboring cells can't tell one ink cell from two, so the single-distance version might only catch holes of one specific width.

I'm weighing whether a conv1 ink map can be near-binary, but pooled values stay somewhere between 0 and 1, so I'll just decide between skipping holes entirely and keeping eight orientations or four plus long-stroke detectors.

I'm settling on a core of four orientation channels with clipping, leaving the other conv2 channels for later as incremental tests against the loss. Before adding anything I want the stroke templates to be sensible, so next I'm designing how each digit's strokes get rendered into a normalized box with the right width aspect.

I'm checking the scale of the digit: MNIST fits the longer side into 20 pixels, so the height is 20 and the skeleton spans roughly 17.5 pixels once stroke thickness is included. Next I want the center of mass of the strokes, weighted by length, and I need to confirm the exact wording of the MNIST centering rule.

I'm pinning down the centering point as 13.5 in pixel-index terms, since MNIST uses a center of 14.0 in continuous coordinates. Next I'm working out how each pooled feature cell maps back onto input-image coordinates.

I'm checking which cells each pooled feature covers in input coordinates: the cell at index a responds to strokes whose centerline falls roughly in rows 4a+3.5 to 4a+11.5, so the four cells are about 8 pixels wide and spaced 4 apart. I'm also starting to estimate how much stroke length in a 6x6 pixel window would saturate the box sum.

I'm settling on the clipping constants: a threshold around 0.2 and a cap near 1.2 so that a 22.5° stroke still lights up both neighboring orientation channels. I'm also wondering whether the clipping makes partial presence look identical to full presence.

I'm considering a gentler clip at around 2, which would let a feature grade between faint and strong presence instead of saturating at a small amount of stroke. Then the rendering model needs to match that, with each cell's response scaling with stroke length times orientation tuning, capped at 1.

I'm turning the stroke-length model into a concrete rule: a 0.75 response per pooled pixel, scaled by tuning and by length in a 6x6 window, then clipped at 1.5. That makes a cell saturate once it holds about 4.5 px of well-aligned stroke, and I want the rendering code to follow the same rule.

I'm weighing a soft-saturation rule, y = 1 − exp(−L_eff/L0), where L_eff is the stroke length in the cell's window weighted by a soft spatial window, as a way to model variability without averaging over jittered samples.

I'm defining each template cell's response as a soft-saturating function of aligned stroke length, weighted by a tent window over the cell's region. The FC weights then come from those template probabilities as log-odds, with a bias term from the complement, and I'm leaning toward clipping the probabilities to roughly 0.08 to 0.92 so no single feature dominates.

I'm settling on a scale for the weights: the logit contributions could be tens of units if s is 1, which makes wrong predictions very costly, so I'll start with s around 0.2 and tune it from the loss.

I'm settling the scaling for the weights, with the starting value of 0.15 or so, and I expect the best value to come from tuning against the loss. Next I'm defining the per-digit stroke templates in a unit box, then scaling them so the skeleton fits into roughly 17 pixels and the center of mass lands on the MNIST centering point.

I'm working out how the digit variants get weighted: each alternative stroke gets a probability, and a cell's presence combines the per-stroke probabilities.

I'm now writing the presence probability as a product over the variant strokes, so a stroke with weight w contributes w times its saturating term and the combined value stays below the sum. For single-weight strokes it reduces to one exponential over the total length, and I'm leaving the slanted "1" variant for later since weighted strokes can't capture it well.

I'm settling the orientation tuning as a cosine-of-twice-the-angle-difference curve, so a stroke 22.5° off a filter's axis still gives about 0.7 response and one 45° off gives nothing. I'm now thinking about widening that to account for writers' slant varying by about ±15°.

I'm settling on a tuning curve of (0.5 + 0.5·cos 2Δ)², which gives full response on the filter's own axis, about 0.73 at 22.5° off, roughly 0.25 at 45°, and nothing near 90°. Next I'm fixing the angle convention for stroke directions in image coordinates, so horizontal, "/", vertical and "\" each map to a clear value.

I'm checking the orientation convention for the filters: with y pointing down, a line at angle θ has its normal distance from a pixel computed as x·sinθ + y·cosθ, which gives the horizontal case at 0°, vertical at 90°, and "/" at 45° where points satisfy x + y = 0.

I'm now sketching out the digit skeletons, with coordinates running top to bottom and a rough width-to-height ratio for each digit to keep the shapes close to MNIST proportions.

I'm sketching the digit skeletons as stroke paths in unit-height coordinates, starting with the 0 as a fairly round ellipse about 0.7 times as wide as it is tall.

I'm settling on three slant variants for the "1" at 0°, 12°, and 25°, weighted 0.4, 0.5, and 0.3, since a single stroke can't cover the range of writers' slants. Because the template is centered by its center of mass, the variants all pass through the middle, so the cells there stay consistently present while the top-right cells only respond to the more slanted versions.

Now I'm working out the orientation channels for the slanted "1" variants, with the vertical one plus two leaning ones feeding mostly the vertical and near-45° channels. Next I'm starting on the "2" skeleton: a top arc running from the left, over to the right, then a diagonal down to the bottom-left and a base stroke along the bottom.

I'm laying out the digit "3" as two stacked arcs: an upper one starting at the top-left, sweeping over the top and down to a midpoint, then a lower one bulging right and closing at the bottom-left.

I'm placing the "4" as an open shape: a left stroke, a horizontal crossbar partway down, and a right stem running the full height.

I'm now sketching the "4" as an open shape with a left stroke, a crossbar partway down, and a right stem, and I'm skipping the closed-top variant since most 4s in MNIST are open. Next I'm laying out the "5" as a top bar, a short down stroke, and a bowl arc curving to the right.

I'm sketching the "6" as a stroke starting top-right and curving down-left, then closing into a bottom loop, roughly centered at (0.33, 0.72).

Now I'm laying out the digit "7" as a top bar with a diagonal down to the bottom, plus an optional crossbar and a small serif variant. Next I'm starting the "8" with an upper loop.

Still working out the figure-8 shape for the "8": I'm trying a Lissajous-style parametric curve, which would cross itself in the middle to give the diagonal X.

I'm working out the parametric figure-eight for the "8": x = 0.33 + 0.3·sin(2t) and y tied to sin(t), so the two lobes sit above and below a crossing point in the middle.

I'm placing the "9" as a loop at the top with a stem running down its right side and curving slightly left at the bottom. I'm also considering a mild global shear of about 0.1 across the digits to match MNIST's typical rightward lean, skipping the ones already drawn slanted.

I'm setting the stroke scale so the skeleton spans about 17.5 pixels, leaving room for the ink thickness within the 20-pixel box. Next I'm working out how each stroke segment is sampled and mapped onto the feature-cell grid.

I'm now converting each stroke sample into cell contributions, using a soft window around each cell center and an exponential saturation with a length scale of about 3 pixels. Since the features aren't strictly binary, a naive Bayes setup with soft inputs should behave like linear interpolation, so that's fine. I'm also clipping the probabilities to 0.05–0.95 to keep the log-odds bounded.

I'm settling on clipping the feature probabilities to a narrower band, around 0.08 to 0.92, since my templates are approximate and I don't want heavy penalties for ink where I expected none. I'm also noting that the bias term comes from treating the features as binary with these probabilities, which means any miscalibration between the model and the real features would shift the class biases.

I'm estimating the log-odds magnitude to choose the scale: for the true class, the summed per-feature terms come to roughly −25, while the wrong classes pick up a much larger penalty, so the typical margin should be around 40, with harder cases closer to zero.

I'm settling on a scale of 0.2 for the logits, with a fallback to 0.15 if the templates turn out poor. Next I'm working out the conv1 normalization for the horizontal filter and how a stroke's response at its center depends on its width.

I'm checking how strong a stroke's response is at its center: with a 2–3 px ink width, the filter gives about 0.9, and curved strokes come out lower, around 0.4–0.7. After pooling, neighboring cells along a stroke still pick up about half the response, so each stroke spreads across roughly two pooled cells.

I'm settling the saturation constant: with thresholds at 0.3 and a scale of 1.5, the response saturates once the stroke sum reaches about 1.8, which corresponds to an aligned stroke a few pixels long inside the window.

I'm checking whether a 45-degree stroke would push the horizontal channel's response above the saturation threshold. Working it through, it comes out around 0.2 to 0.4 per position, which is in a reasonable range and roughly matches the template estimate of about 0.49. I'm also going to revisit the conv1 bias, which I set to −0.1.

I'm settling the diagonal filter's weights: the center cells get a strong positive value, the outer ones go negative, and the negative side has to be scaled down so the whole filter sums to zero.

Working out the diagonal filter's normalization: the negative side has to be scaled so the weights sum to zero, and I'm checking what a width-2 diagonal stroke contributes to the response.

I'm normalizing the diagonal filter so its negative side balances the positive center, and I'm trying a gentler falloff profile so its width response matches the horizontal filter's more closely.

I'm comparing the normalization options for the horizontal and diagonal filters, and I'm keeping the interpolated profile with the negative side rescaled, since it gives the horizontal filter cleaner responses.

Now I'm settling the conv2 weights: each of the first four channels copies its matching conv1 channel over the 3x3 center with bias set to the threshold, and channels 4 through 7 get the same weights with the threshold plus the saturation constant. The remaining channels stay zero. I'm also weighing whether to add more conv1 orientations for the rest of the channels.

I'm considering whether an orientation set of eight, using a cosine-based tuning curve, is worth it for the naive Bayes setup. Adjacent orientations would be strongly correlated, so the independence assumption would double-count evidence, and any gain from distinguishing close angles looks small.

I'm considering an 8x8 ink-presence map built from a single conv1 filter and four conv2 channels, each taking one sub-offset of the pooled grid. The idea is a fine spatial template, complementary to the orientation channels, where a single-tap kernel keeps the values bounded.

I'm weighing which sub-offsets to use for the single-tap ink channels, looking at how each tap's pooled rows line up across the grid.

I'm working out the pooled grid offsets for the single-tap ink channels, looking at which rows each offset covers and how the cells overlap. Using two adjacent offsets gives a finer stride, but it leaves the coverage asymmetric, so I'm checking whether three offsets would fill the grid more evenly.

I'm checking which offset pairs cover the pooled grid evenly: offsets {1,2} leave the bottom and right edges slightly short, while {1,3} covers 1–10 but duplicates cells. I'm working out whether a four-channel layout at (1,1), (1,2), (2,1), (2,2) is worth the imbalance.

Weighing whether to add the fine ink-presence map alongside the orientation channels, I'm leaning toward starting with orientation features only, so I can check the baseline and then add the ink channels one at a time.

I'm weighing whether to probe the templates more actively, since hand-tuned weights are the main bottleneck, and I'm asking whether reading the classifier's feedback and its confusion patterns counts as legitimate improvement or just a roundabout way of learning from the data. I'll keep to classification attempts and infer from the confusions, maybe trying a few variations of the scale.

Writing the line filter code for the oriented detectors...

Checking the line filter's sign pattern: the diagonal responses should peak where the stroke's offset from the center line is zero, and I'm verifying that for the 45-degree case.

Still writing the line filter setup and the digit stroke templates...

Still writing the digit stroke templates and the feature rendering...

Still writing the stroke-to-orientation rendering loop, sampling points along each segment.

Still writing the stroke rendering: each segment is sampled, weighted by a tent window around the cell centers, and projected onto four orientation channels.

Still working out the feature mapping: the fully connected weights take each conv2 channel's cell at its row and column, with positive weights on the first four channels and negative on the matching ones, scaled by the log-odds. I'm also setting the output bias from the log of the complement probabilities and centering it so the numbers stay tidy.

Still checking the pooled-grid math: each final cell covers conv2 outputs at 2a and 2a+1, which map to pooled rows 2a+1 through 2a+4, so the input centers land near 4a+7.5 with about a half-width of 3.5 plus filter spread. I'm treating the window as flat out to 3 and falling to zero at 6, which seems fine. Next I'll write the digit stroke coordinates and check them against the scaled grid.

Checking the digit 0 and digit 1 stroke coordinates against the scaled grid: the ellipse comes out about 15 pixels wide with the stroke included, which seems plausible for MNIST zeros, and the three slanted 1s all keep their center of mass at x=0.

Still working out the digit 2 template: an arc across the top, then a diagonal down to the bottom-left, and a base line that I'm deciding whether to keep flat.

Still working out the digit 3 and 4 stroke layouts, including where the middle bar sits.

Still writing the digit 4 and 5 stroke layouts, with the bowl of the 5 starting from its upper-left end.

Still working out the digit 5 and 6 stroke layouts, and the shear for each.

Still working out the digit 7 and 8 stroke layouts, with the 8 built as a Lissajous curve.

Still working out the digit 8 and 9 stroke layouts, with the 8 built from a Lissajous curve whose upper lobe is narrower than the lower.

Still working out the digit stroke layouts and how the stroke weights get normalized before placement.

Still working out the digit stroke layouts: I'm setting the bounding box from the strokes with weight of at least 0.35, and computing the center of mass from all strokes weighted by length.

Checking the cell-by-cell weights for the vertical 1: the column centers near x=11.5 and 15.5 pick up full weight, while 7.5 and 19.5 get none. Summing the stroke length that falls within each row's window gives about 7.25 for the top row, which maps to a response near 0.91 under the saturating curve.

Now I'm checking whether the blur is too wide: the window is flat out to 3 and tapers to 6, but the real cell response may only reach about 4.5.

Checking the scale and threshold choices now: with the scale at 0.2 and the threshold at 0.3, cross-talk from diagonal strokes on the vertical filter could push the 3x3 pooled sums over the cutoff, so I'm estimating how often that happens.

Checking how a typical bold MNIST stroke cross-section responds to the edge filter, I'm estimating about 0.8 for a centered stroke.

I'm settling on the bold-stroke numbers now: lowering the saturation constant to 1.2 and the threshold to 0.25, so a stroke crossing three pooled cells still reaches the cap.

Still writing the weight matrix: the fully connected weights are scaled by the log-odds, with positive and negative copies for the paired channels, and I'm checking the flatten order and the bias terms against the feature count.

Still checking the sampling cost of the stroke rendering loop, since each digit has about a hundred segments and several samples per segment across four orientation channels.

Still writing the digit stroke templates and the bounding-box normalization, with the strokes weighted and placed before the final output.
