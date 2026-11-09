I'm sketching a small hand-built CNN for MNIST, starting with the first layer: 8 five-by-five filters on the 28x28 input, giving 24x24 maps, then ReLU and 2x2 max pooling down to 12x12. I'm also checking how each pooled position maps back to its patch of the input image.

I'm working out how the second conv layer's receptive fields line up with the digit, which covers roughly rows 4 to 24 of the image. The field is large, so I'm considering whether to concentrate the conv2 weights at a fixed spot inside the kernel. I'm weighing a template-matching design, with conv1 as oriented stroke detectors and the fc layer holding hand-drawn templates, against a simpler one where conv2 mostly passes oriented features through with spatial pooling.

I'm settling on the fc layer as per-digit templates over the 16 4x4 feature maps, though that resolution is coarse, about 4 pixels per cell against a 20-pixel digit box. The conv2 kernel can choose which offset within its 5x5 window to sample, so I'm working out which pooled1 rows that offset reads from and how the max pooling picks among them.

I'm checking how the 4x4 cells line up with the 20-pixel digit box, where each cell covers about 5x5 pixels. To get finer resolution than that, I'm considering giving different conv2 channels shifted kernel offsets so their grids interleave.

I'm weighing a simpler fixed-offset design against the template version, and I'm considering whether interleaving shifted kernel offsets across conv2 channels could recover finer spatial resolution than the 5-pixel cells give. Pure hand-tuning of this kind would likely land somewhere around 70 to 85 percent, so I'd plan to refine the biases and templates against confusion results as I go.

I'm weighing a set of 8 first-layer filters: oriented stroke detectors at four angles versus eight directional gradient detectors at 45° steps, since directed edges could tell a stroke's top edge from its bottom and help with concavity.

I'm now comparing a set of eight oriented line detectors at 22.5° steps against the four-orientation version, though with a 5x5 kernel that finer angle spacing is hard to resolve. I'm also considering whether the remaining filters should be spent on something like a plain ink detector, since that helps with "where is the ink" templates.

I'm weighing whether conv2 could go beyond orientation pooling and detect larger structures, like a horizontal bar above a vertical stroke for the top of a 7, or a ring-shaped loop roughly 10 pixels across.

I'm settling on a mostly linear design, with conv1 as four oriented line detectors, because nonlinear AND-style units with tuned biases would be hard to calibrate without seeing activation magnitudes. Keeping biases at zero and letting ReLU act on naturally signed features should make the feedback loop more reliable.

I'm settling on four oriented line detectors for the first layer, with zero-mean kernels so uniform regions give nothing, and I'm estimating a stroke response of roughly 0.5 to 1. For the other four filters, I'm considering directed edges in four directions, but they would mostly repeat what the paired oriented stroke detectors already capture, so the gain looks small.

I'm weighing whether to use the remaining first-layer filters as endpoint detectors, since a stroke ending in a given direction is discriminative for several digits. A 5x5 kernel on 2–3 px antialiased strokes would probably make that detection noisy, though.

I'm now considering four half-plane curvature detectors shaped like corners and arcs, since arcs opening in different directions separate digits like 3 and 6. At 5x5 they'll look close to diagonal lines, though, so I'm weighing whether conv2 could combine the first-layer features across positions to capture that second-order structure instead.

I'm now thinking about whether features like "nothing above a stroke" or "nothing to the right of a stroke" could capture the outer contour and concavities, since cavities opening in different directions help separate digits like 3, 5, and 6.

I'm now thinking about whether a fixed-weight AND across four directions could be built from ReLU sums, but without any cap on the ink counts, a few dense strokes in three directions could trigger it falsely. Adding a negative weight on the center to suppress filled regions might help.

I'm working out a hole detector at conv2: a positive ring at radius 2 with a negative center, so loops of about 8 to 10 pixels register. I'm checking the expected hole sizes for 0, 8, 6, 9, and 4, and I'm keeping in mind that this approximation is noisy, so the fc layer will need to combine it with other evidence.

I'm thinking about using the remaining steps to probe the network's own statistics: setting the fc outputs so the confusion matrix reveals how a chosen feature's values are distributed across each true class. Since the feedback is aggregated, this would let me calibrate feature scales before tuning the templates and biases.

I'm considering whether to spend a few of the remaining steps on probing the network's statistics through the confusion matrix, but I'd rather keep the budget for a real classifier. My plan is to design it on principled scales and then tune templates against the feedback.

I'm working out the pooling geometry: the first-layer pooled cells map to image centers around 2i+2.5, so the digit's rows 4 to 23 correspond to pooled rows roughly 1 through 10, with the image center at pooled row 5.5. Next I'll set up how conv2 indexes into that grid.

I'm checking how the second layer's pooled cells line up with the digit's rows: with the center tap, the four pooled cells sit at image rows about 7.5, 11.5, 15.5, and 19.5, drawing on first-layer rows 2 through 9.

Looking at the top stroke of a digit, it sits around image row 5, which is p1 row 1, and the center tap of conv2 for the first cell (reading p1 rows 2 and 3) misses it. So I'm considering taps at rows 1 and 2 instead, so that each cell covers rows 2R+1 through 2R+4 and the overlapping reads are summed.

I'm checking how taps at different offsets line up with the pooled grid: even offsets reproduce the same alignment shifted by two cells, while odd offsets give an interleaved grid. Tap 1 seems to cover the digit's upper rows best, so I'm looking at that alignment for the top strokes.

I'm lining up the pooled conv2 taps at offsets 1 and 3, which together cover pooled rows 1 through 10 as five vertical cells of about four image pixels each. Those cells span the digit's height, so each feature would need two to four conv2 channels to fill the full 5x5 grid.

I'm settling on the 16-channel layout: four features, each with a single channel that sums taps 1 and 3, so every feature gets overlapping 4-row windows over the digit's full height. That gives a 4x4 grid per feature, which trades some resolution for robustness to small shifts.

I'm weighing whether to spend the 16 channels on distinct higher-order features with 4x4 overlapping pooling, or on fewer features at finer resolution. Next I want to pick a set of structural detectors for conv2 that can tell digits apart on the pooled grid.

I'm sketching concavity detectors at conv2 next: a cavity that opens to the left would be an empty center cell with no ink to its left, and I'm working out how the p1 ink channel would encode that.

I'm sketching a cavity detector for conv2 that uses oriented strokes: a horizontal stroke above, a horizontal middle bar below, and a vertical arc on the right, with the left left open. For a 3's upper cavity that spans about four p1 cells, so the kernel needs a positive row at the top and bottom and a positive column on the right, with negative weights on the center and left.

I'm noting that a fixed template needs broad positive regions to tolerate shifts, since the top and bottom strokes can land a row or two off. The detector would act as a loose AND of parts, which feels workable but I'm not sure it will hold up on real digits. I'd expect rough accuracy in the 60 to 80 percent range before tuning, so I'm planning to treat the first version as a baseline and adjust from there.

I'm checking whether drawing templates from hand-described strokes stays within the rules: I'd render them straight into the fc weight space by formula, never run the network on inputs or average over generated samples.

I'm weighing whether to keep each class to a single hand-drawn template, or to add a few variants, since summing several variants could look like averaging over generated samples. Drawing one template per digit, with an optional stroke at reduced weight, seems to stay within the rules. Each class's logit would then be the dot product of its template with the features, with the template mean-subtracted so stray ink counts against it.

I'm weighing whether a nearest-prototype rule, using each class's hand-drawn template and a distance-style penalty, could reach a reasonable accuracy on pooled oriented features. I expect it to fall short of the true class means, but overlapping pooling should help. To go further, I'm considering negative "penalty strokes" in each template that mark where ink should be absent for a given class, such as the top stroke that a 4 lacks but a 9 has.

I'm thinking about whether a finer grid would serve better here: 4x4 overlapping windows of 8 px are too coarse to resolve a 0's center hole, since max-pooling would register ink in every window. So I'm weighing dedicated cavity channels in conv2 as a complement, or a non-overlapping 5x5 grid of 4 px cells instead.

I'm considering a second layout for conv2: instead of an ink grid, each channel would hold a mid-level part detector, like a top arc, bottom arc, left or right arc, a long vertical or horizontal stroke, or a junction. Each would cover about half a digit, so the fc layer would pick where those parts sit on the 4x4 grid.

I'm now listing per-digit structural cues for conv2: a 0 has left and right arcs with a central hole, a 1 is a single centered vertical stroke, and a 2 combines a top arc, a diagonal, and a bottom horizontal with a bottom-left corner. The list continues with cavity-based cues for 3, 4, 5, and 6 as I go.

I'm laying out a 16-channel conv2 design: four oriented stroke poolings, a hole detector for enclosed background, and cavity detectors open to each side. I'm still weighing whether the remaining channels should cover endpoints, a finer ink grid, or corner and curve detectors, and whether a single conv layer over the 8 conv1 features can compute them at all.

I'm working out the cavity detector's inputs: ink above, below, and to the right of the kernel center, with no ink at the center and none on the left. For each direction I'd sum the nearby cells, so the center's emptiness and the missing left side show up as a single response.

I'm checking whether a single conv2 channel can encode a concavity: an enclosing hole needs ink above, below, left and right with the center empty, but summing those directions can't tell an enclosing boundary from a line passing through. Oriented features should help, since a horizontal stroke above and below plus vertical strokes at the sides is what a round 0 looks like.

I'm weighing how a stroke's position shifts across rows: a horizontal stroke could land in row 0, row 1, or both after pooling, so the cavity's upper direction might only register about 1 to 2. Wider strips would raise that toward 6, so I'm considering whether to normalize each direction to a mean so partial presence scores lower.

I'm checking whether a ring-shaped hole detector can work with a 5x5 kernel on the p1 map. The stroke centers for a 0 sit about 8 px apart vertically, which is more than a single kernel can span, so the detector would have to rely on the narrower loops of 8, 6, and 9.

I'm checking whether two paired features could capture the digits: an "LR-enclosed" detector for empty center with vertical ink on both sides, and a "UD-enclosed" one for horizontal ink above and below. The catch is that the fc layer is linear and can't AND them together.

I'm settling on a plan to skip the fine-grained ring detector, since its 5x5 kernel can't span the 0's vertical stroke spacing. Instead I'll weigh a simpler approach: local ink-to-the-side patterns in the background, and accept approximate coverage rather than trying to replicate what a trained network would learn.

I'm settling on horizontal-line detection first: a first-layer filter with a positive center row and negative rows above and below, tuned to MNIST stroke thickness.

I'm settling on the horizontal-stroke filter: a profile with a strong center row, mild neighbors, and negative outer rows, normalized so a clean three-pixel stroke gives about 1.0.

Checking the diagonal case: a 45-degree stroke through the center gives about 0.2, so orthogonal strokes stay low. Next I'm setting up the vertical-line filter.

I'm defining the two diagonal filters, with a positive ridge along the stroke and negative bands on either side, and I'm checking that the zero-sum profile keeps them low on orthogonal strokes.

I'm checking the diagonal filter's response to a horizontal stroke through the center, working cell by cell across the row offsets to see whether it stays low.

I'm testing a version of the diagonal filter with a small negative weight at |d|=2, which should cut the cross-talk from horizontal strokes, and I'm recounting the row sums to check the effect.

I'm settling the remaining conv1 filters: two diagonal-line detectors fill out the orientation set, and I'm now deciding whether the last four should be ink-density blobs, which would help flag empty centers for hole and cavity checks.

I'm weighing a few options for the remaining conv1 channels: an ink-density channel to flag whether a cell is filled, directional edge filters, or end-stop detectors for stroke tips in each direction. I'm leaning toward the ink channel for reliability on thick blobs and junctions, and I'm still deciding whether the edge and end-stop filters would add anything useful.

I'm now checking an end-stop detector for stroke tips: it should fire on the bottom half of a vertical stroke with empty sides, but a horizontal stroke's top edge would also light it up. I'm working out how to suppress that with negative weights on the side columns.

I'm settling the end-stop kernel's layout: a positive block over the bottom three rows of the center columns, negative weights on the top rows and the side columns so a horizontal stroke's edge doesn't fire it. A true stroke end should give a full response, while a thin stroke gives only a third of that, and I'm noting that diagonal ends and curved arc tops will only partly activate it.

I'm checking how the end-stop kernel handles arc tops and slanted strokes, since a narrow loop or a 7's diagonal could partly fire it. I'm accepting that some noise will come through, because the endpoint features still look discriminative overall.

I'm now thinking about whether endpoint detectors or corner detectors would be more useful, and I'm leaning toward endpoints. A top-end detector at the 2-pixel p1 resolution could look for a vertical stroke below with empty space above, which would separate stroke tips from the corners of a closed shape.

I'm now weighing whether to spread the conv2 channels over the four line orientations at a coarser stride, to see where a horizontal bar sits in the digit's height, since the top, middle, and bottom bars would fall into different pooling windows.

I'm weighing whether the conv2 channels should use non-uniform taps, such as the odd rows only, so each pooled cell covers a clean span of the p1 map. I'm also planning to reserve a hole-detector channel, possibly at two sizes.

I'm thinking through the last conv2 channels: a hole detector, cavity detectors in four directions, and endpoint features from conv1 pooled up. I'm also considering two spare channels for long straight strokes or junctions. I'm doubting whether the whole design is too intricate to set by hand without testing it.

I'm sketching out where each digit's features tend to sit on the 12x12 pooled grid, starting from the center of mass, and planning to set the conv2 filter taps and pooling layout around those positions.

I'm mapping the pooled grid back to image rows, with the four-row windows on the 12x12 map covering roughly image rows 4-11, 8-15, 12-19, and 16-23. Since the digits are height-normalized and centered by mass, I'm checking which column cells a narrow digit like a 1 would fall into.

I'm weighing how the fully connected layer's 4x4 templates should be written, since 16 channels across 10 classes would mean hundreds of hand-set cells. I'm guessing many of those entries could just be zero, and I'll try to keep the setup compact with helper functions.

I'm weighing whether to build the fully connected templates from hand-described stroke skeletons, rendering each digit's expected orientation energy into the pooled cells. I'm also second-guessing that approach, since subtracting a mean template across classes starts to look like a discriminant method I'd want to avoid.

I'm settling on writing the fully connected weights directly from hand-described positive and negative regions per class, rather than subtracting a cross-class mean, to stay clear of any approach that derives weights from generated example vectors. Bias terms will also be set by hand, and endpoint and cavity templates will be placed as points or blobs on the 4x4 grid.

I'm weighing whether to write the fully connected 4x4 templates by hand, cell by cell, or to render them in code from stroke descriptions. Hand-writing them lets me check each window directly, so I'm leaning toward that for the 10 digits and roughly 14 channels.

I'm settling on specifying each channel's 4x4 weight template as a small character grid, with signs for expected and forbidden regions and a global scale factor to tune later.

I'm settling on how to lay out the eight first-layer filters: horizontal, vertical, and both diagonals, with a blob detector and a few spares for endpoint or emptiness checks. I'm weighing whether the ink-blob filter can be dropped if the line detectors already cover that role.

I'm weighing whether the ink channel is worth keeping, since summing the four line detectors already acts as an ink proxy. I'm also comparing that against a fourth endpoint detector, and wondering whether endpoints could be computed at conv2 instead.

I'm listing which digits have a tip pointing upward, going through each one: 1, 4, 6 and 5 have clear top tips, while 7, 9 and 0 mostly don't, and 2, 3 and 8 are less certain.

Now I'm listing which digits have endpoints on each side, going through the tips for the bottom, left, and right sides, with the pooled 4x4 windows resolving the positions roughly.

I'm deciding whether a fourth conv1 channel should be an endpoint detector rather than an ink blob, and weighing which tip direction is least useful: right-side tips help separate 2, 5 and 4, while left-side tips help with 3 and 7.

Now I'm weighing whether the end detectors should live at the conv1 scale, where a stroke is only a few pixels thick, or be computed at conv2 instead. Some digits have tips on several sides, so each direction seems useful enough to keep.

I'm weighing a smaller negative weight on the side columns, since thick strokes spill into them and a full penalty would wipe out the endpoint response entirely.

I'm working out whether a top tip can be detected at the pooled scale instead: a vertical-line response over two rows, with no line response above it. That should hold up even when strokes are thick, though it might confuse a stroke's corner with a true end.

I'm now weighing whether the conv2 end detectors should be computed directly from the pooled line maps, which would free up the four spare conv1 channels for something else, such as an ink blob or a set of directed edge detectors.

I'm considering whether a blob channel can serve as the ink signal for the hole detectors, which would mean taking the max over a 3x3 mean at each pooled cell. The catch is that a stroke clipping the edge of that window only partly fills it, so the response would be uneven.

I'm considering a small ink kernel instead, with weight on the four center pixels of the 5x5 patch, so that a narrow hole still registers as empty at the pooled scale.

I'm considering a background channel for the holes: a conv1 map that goes high wherever the center is empty, so after max pooling it flags any empty spot in a region, and conv2 can then combine that with the surrounding ink.

I'm checking whether a hole detector is worth the effort, since it separates the digits that confuse most: 4 and 9, 3 and 8, 5 and 6. Cavities are the clearest discriminator for those pairs, so I want the detector to be sensitive even when the loops are small.

I'm checking whether a hole detector can fit inside a 5x5 pooled kernel, which it can for small inner loops of 1 to 3 pixels, though 0's larger vertical loop won't fit and will have to rely on other features.

I'm thinking about whether a 0's loop, too tall for the kernel, could still be recognized: cavity open downward near its top and open upward near its bottom, with left and right enclosure in the middle, so the pattern itself becomes the signature.

I'm considering a fused conjunction for the hole cue: a background term at the center plus V-line ink on both the left and right, so a "| |" pattern registers. The trouble is that the sum over the left cells can't be capped at one, so I'll have to work out how to keep the AND from being swamped.

I'm estimating how strongly a vertical line registers at conv1 as its horizontal offset from the kernel center changes: about 1 when centered, around 0.25 at one pixel off, and zero beyond that.

Working through how a vertical stroke lands on the pooled grid: a 3-pixel-wide stroke gives one pooled column a full response and its neighbor about a quarter. A 2-pixel stroke sitting between kernel centers gives a flatter response of about 0.75 across two columns.

I'm working out how a vertical stroke registers in a single row of cells, since a cross-section gives roughly one unit of response per stroke. So the left-wall term should look at a horizontal strip, one cell tall, two cells to the left of center.

I'm weighing whether the left-wall term should count diagonal strokes as well as vertical ones, giving diagonals partial weight on both the vertical and horizontal wall detectors, since loops made of slanted arcs would otherwise be missed. For the center row, I'm checking how the left wall of a ring shows up.

I'm checking the left-wall term against plain ink instead: summing ink over the two cells left of center. The open question is what a horizontal stroke running along that strip does to the sum.

I'm checking whether the four directional cues can be combined with a simple threshold, and it doesn't work with plain ink strips, since each one can saturate near 2 and the sums overlap. So I'm leaning toward vertical-line responses on the left and right walls instead, where a perpendicular crossing contributes about 1 and a stroke running along the strip contributes almost nothing.

I'm trying a different route for the hole detector: keeping each side's contribution to a single linear-plus-ReLU sum, but noting that the sum can't act as a clean AND, since three present sides can reach the same value as four.

I'm checking whether pairing the left and right wall terms with the top and bottom ones gives a cleaner AND for the hole cue: a 9's top loop would get both pairs, while a 4, 5, or 3 would only get one, so the sum should separate them.

I'm checking the four-way AND for the cavity cue: if the up, down, and right wall terms plus the background term are all present and the left is absent, the sum lands near 0.4, which gives a usable margin. I'm noting that the 0.6 to 1.2 range of the individual terms is what makes this hold.

I'm noticing that the pair-AND is cleaner than a four-way sum: the left-right pair and the up-down pair each need both walls plus the background term, so a missing wall drops the score well below the threshold. That leaves the open direction, since UD enclosure alone can't distinguish a 3's upper cavity opening left from a 5's opening right.

I'm considering a one-sided gap feature instead: a background cell with a wall to its right and no wall to its left, which would mark the open side of a cavity without needing a full four-way AND.

I'm checking the 4-versus-9 case next: a 9 has a horizontal stroke closing its top loop, while a 4 has its crossbar in the middle, so a horizontal response in the top pooled window should separate them. I'm wondering whether an 8-pixel window covering rows 4 to 11 is tall enough to catch that closure.

I'm moving on to the broader plan: a set of reasonable features with templates, then refining them based on where the classes get confused. I'm also weighing finer pooled resolution for the basic line detectors, since those are the most dependable, and I'm budgeting the 16 channels across pooled lines and the pair-enclosure features.

I'm reviewing the remaining feature budget: the ends, a full four-wall hole detector as extra evidence, and long vertical and horizontal line detectors. I'm also considering curvature detectors for the open arcs, like "(" and ")" built from slanted strokes meeting a vertical in the middle, and "∩" and "∪" built from a horizontal stroke with diagonals on either side.

I'm now considering whether the arc detectors, which respond to curve convexity, could help separate pairs like 3 and 5 or 2 and the others, since pooled orientation plus position already captures much of this.

I'm simplifying the cavity idea: an open-right cavity is basically a "(" arc seen from inside, and an open-left one is a ")" arc, so the arc detectors and the cavity detectors amount to the same thing. I'm sketching what a ")" template would look like on a 5x5 first-layer patch at roughly 10-pixel scale, with the right wall in the middle columns and the top and bottom strokes running leftward from it.

I'm sizing the cavity templates against the digits: the 3's upper cavity is about two cells tall, so a 5x5 window fits it, and the 5's lower belly is only partly covered. For the 2's top hook, the cavity sits below the top arc and opens down-left, and I'm checking whether a 7's bar-plus-diagonal region gives a similar shape.

I'm weighing whether a three-wall AND can be made robust for the open-left cavity, since a missing bottom wall breaks the pair. Instead I'm considering a pairwise curvature cue: a backslash stroke above and a forward slash below on the right side would signal a convex-right arc, and the mirrored pairs would cover the other directions.

I'm now sketching a pair-AND for arc direction: a backslash segment above and a forward slash below on the right side would mark a convex-right arc, with the mirrored pairs covering the other directions. I'm trying to work out which cells the upper and lower segments of a ")" arc would occupy at about a two-cell radius.

I'm weighing a pair-AND where the arc's upper and lower segments each contribute, roughly 1 to 1.5 each when present, and checking whether a middle vertical term would sharpen the separation.

I'm checking whether pooled windows of diagonal strokes can capture the arc direction, comparing a right-side pattern for ")" against the mirrored one for ">", since linear window features might miss the local arrangement that a pair-AND captures.

I'm now grouping the pooled orientation channels with the arc detectors: four channels for H, V, and the two diagonals, plus four for the open curve shapes "(", ")", "∩", and "∪". The pooled orientations lose the arrangement of strokes within each 8-pixel window, so the convexity detectors are the part that adds something new.

I'm now weighing whether the left-right and up-down enclosure features are still needed once the arc detectors are in place, since a big "(" plus ")" pair would cover much of the same ground for a 0. I'm also checking whether the arcs are too small to pick up the top loop of an 8.

I'm sketching arc templates for each digit: 0 gets left and right curves plus a top and bottom cap, 1 is just a central vertical with tips, and 2 needs a top hook, a right-side curve, and a sharp corner where the diagonal meets the base.

I'm assigning arc-type detectors to each digit: for 3 that means right-side ")" arcs at top and bottom with left-side tips, for 4 an open-top cup and right-side verticals, and for 5 a bottom-right ")" with a top horizontal, though I'm not sure whether its top-left corner counts as a "(" arc.

I'm weighing whether a sharp corner like the 5's upper-left "┌" would be missed by diagonal-based arc detectors, which would not fire there. Wall-based cavity detectors would catch it, so I'm thinking the arc detectors should accept both diagonal and horizontal top strokes.

I'm weighing whether the cavity margin problem can be avoided by a simpler convexity cue, such as a feature for a background cell with an ink wall directly to its right.

I'm weighing whether simple pooled ink at shifted positions would be enough, since those features are predictable, and I'd leave the pair-AND features for later. The plan is to choose a reasonable feature set now and then tune the fully connected templates against confusion results, because tuning the feature definitions blind is harder.

I'm weighing whether a finer grid of pooled orientation channels, sampled at several tap offsets, could do better than hand-built arc detectors, since a trained linear model over such features would probably beat a hand-drawn set.

I'm settling on a representation with a 5x5 grid of 4-pixel cells over the central 20x20 box, sampling each orientation at several tap offsets so the rows of line centers line up. Then I can draw each digit's strokes straight into that grid as a template.

I'm checking whether finer band positions would be enough to catch the arcs in a 3, since its upper and lower curves land in neighboring bands. Handwriting jitter of a couple of pixels would blur those bands, so I'd want smooth, blurred templates rather than sharp ones.

I'm weighing the trade-off between hand-drawn structural features and a finer grid of oriented-stroke cells. I expect a trained linear model on the grid to do better, and I'd tune the template biases and pairwise weights from confusion results afterward. I'm considering mixing in a few structural features, like holes and endpoints, to get more discrimination per weight, though that brings more risk since I can't predict how they'll behave.

I'm considering a mixed design: eight orientation channels with finer row bands for the main axis of each stroke, plus eight structural channels for endpoints, left-right and up-down enclosure, and a couple more. The trade-off is that the spec gets more complicated, even if it gives better coverage.

I'm thinking about whether to generate the templates from a renderer that turns each digit's polyline strokes into expected orientation and location features, then sets the template weights from those values with a negative baseline where the digit shouldn't have strokes.

I'm settling on rendering each digit's strokes straight into the feature grid, so the weight for each class is a drawing of its strokes over a constant negative background, with no statistics taken from samples. For the structural channels I'd list endpoints and hole centers by hand in image coordinates and paint them into the matching cell windows.

I'm now considering whether a single linear template per digit is enough, or whether digits like 7, 1, 4, 2, and 9 need several prototypes to cover their different stroke styles. I'm also checking how the endpoints and holes would be placed by hand, with tips marked by the direction the stroke leaves its end.

I'm moving to digit-specific details now: a blurred render of each class's strokes can serve as the template, with optional strokes given lower weight instead of averaging generated samples. For 1 I'm thinking about slant tolerance, and a negative baseline outside the central column should help separate it from 7, 4, and 9.

I'm noting that the negative baseline term β·Σx is identical for every class, so it cancels out of the argmax. That leaves the classifier as t·x − ½|t|², a plain Euclidean nearest-template rule, where unexpected ink is already handled by the template weights.

I'm checking whether a nearest-centroid rule already covers the 1-versus-7 case. The extra bar in a 7 pushes its score past a 1's only when the bar is strongly present, so the decision works out. Discriminating cases like a 4's top horizontal might need class-specific negative weights, which I can add as hand-drawn anti-strokes.

I'm checking whether the features stay on a sensible scale, since real handwriting strokes may only reach about 0.4 to 0.9 against templates capped at 1.0. If the input is systematically weaker than the template, the −½|t|² term starts favoring classes with small templates, like 1, so I'll need to account for that.

Checking the scale of responses to real digits next: the line detectors should be normalized so a clean 3-pixel stroke reads as 1. Stroke cores in MNIST sit near full intensity with anti-aliased edges, so I still need to see how much weaker real strokes come out against the templates.

Checking how the conv1 line kernel responds to different stroke widths: a 3-pixel stroke gives the full response, while thicker bold strokes fall off, so I'm considering a softer profile to handle them.

I'm considering edge-based detectors instead of thin-line kernels: gradient filters that respond to the boundary between ink and background in eight directions. That would handle bold strokes of any width, since a thick stroke still yields its two edges, and the edge polarity would tell me which side of the boundary is ink.

I'm weighing whether edge-based detectors would beat thin-line kernels: they'd respond to both boundaries of any stroke, so bold strokes still register, but they tune more loosely across orientations. I'm leaning toward keeping the line detectors and softening their surround so a 4-pixel stroke still gives a usable response.

I'm comparing the line kernel's response across stroke widths: a 3-pixel stroke gives the full value, while 1- and 2-pixel strokes come out a bit weaker. Working through a typical antialiased cross-section, the response lands around 0.7, which looks usable. I'm also checking what the stroke width in MNIST usually is.

I'm weighing whether to include the endpoint and enclosure structural features from the start or keep the first version to orientation templates alone as a baseline. Building them in now feels fine since the templates are rendered from stroke descriptions, but there's a risk they hurt accuracy, so I'm considering an ablation run to see which choice holds up.

I'm weighing how to split the 16 channels: a full 5x5 grid would give four orientations four channels each with no room for structure, so I'm considering two per orientation, or a few three-channel variants, with the row band mattering most for horizontal strokes.

I'm weighing how to lay out the 16 channels, since a full 5x5 grid per orientation would leave no room for structural features. For vertical strokes the column position matters most, while for horizontal strokes the row band matters most, so the spatial resolution should follow that asymmetry. I'm also wondering whether non-overlapping 4-pixel row bands are fine-grained enough to catch where a 7's top bar or a 3's middle bar sits.

I'm settling on eight orientation channels, two per direction, with the column taps for horizontal strokes and the row taps for vertical ones, and I'm checking how a stroke spanning two taps should be weighted so long strokes don't double up.

I'm settling the column taps for the horizontal orientations: using only the middle tap gives four non-overlapping 4-pixel cells, which is finer than summing two overlapping taps. That still misses strokes centered at the very edges of the image, which should be rare in MNIST digits, so I'll accept it and let the vertical orientations use their own row taps.

I'm moving to the column placement for the vertical channels: fine bands of 4 px at columns 4-7, 8-11, 12-15, 16-19, and 20-23, so the central band covers the image midline at 13.5. I'm noting that the stride-4 cells for the horizontal channels would split the midline between two cells, which is why the vertical taps need to be offset.

Still working out the channel layout: the row and column tap offsets for each orientation, and how to render the templates from those cell positions.

I'm weighing whether the templates should be simulated through the conv2 and pooling ops, or drawn directly in the fully connected space with geometric formulas that map stroke points to cell indices. The formula route seems safer, since running network operations on synthetic inputs could break the rules I'm working under.

I'm deciding how to draw the templates directly into the fully connected weight grid, mapping each stroke point to its cell index with a coordinate formula. I'm also starting to think about the endpoint and structural features and how to define their conv2 kernels.

I'm now considering the four remaining conv1 channels, and whether an INK channel or a BG (emptiness) channel would serve better for detecting hole centers. An AND-style combination could work with negative ink weights and a bias, though max-pooling makes the emptiness check less precise.

I'm settling on a background channel for hole detection: a weighted sum over the center 3x3 of ink, with the center pixel weighted most, so an empty pixel surrounded by light ink still reads as a hole.

I'm now asking which conv1 channels 4 through 7 should hold: the background channel is set, and I'm considering whether two more channels would help with small local features like end points, or whether they should stay zero.

I'm turning to the endpoint features in conv2, starting with a top tip: a downward stroke at the kernel center, with nothing above it in the first rows, so I'd combine positive ink along the stroke with negative weights on the empty region above.

I'm checking how the p1 ink values sit around the tip cell: the blur from the 4-pixel regions at stride 2 means neighboring cells pick up partial ink, and max pooling in conv2 should still find the best alignment.

I'm settling the top-tip detector: positive weight on the ink at the stroke's center cells below, and strong negative weight on row 0 across the middle columns, with a lighter penalty on the side cells of row 1 so that arcs and corners running sideways from the top don't fire it.

I'm now setting the negative taps for the top-tip detector: the arc's top at columns ±4 px still produces ink in rows 2 and 3, so penalizing those cells would wrongly reject 0-style curves.

I'm weighing how strictly the top-tip negatives should cover the sides, since an arc's top only drops about 0.4 px within ±2 px, so the row 2 and 3 cells at ±4 px would wrongly suppress curves.

I'm defining the top-tip detector as a positive weight on the ink at the stroke center, with heavy negative weights on the empty row above and on the side cells of the row just above, so that arcs and sideways corners don't fire it.

I'm checking the top-tip score for a vertical stroke: the center cell and the cells just below it carry most of the weight, so the score comes out around 1.8 before bias. For a horizontal stroke through the middle, the sideways ink in row 2 drives the negative terms far below zero, so the detector stays off.

I'm checking how the top-tip detector responds to a corner shape like a ┌ or ┐, where the stroke turns sideways from the center. The score lands just above zero before bias, so with the bias it stays off. I'm also confirming that a vertical stroke passing straight through the center, with no tip, gets suppressed by the penalty on row 0.

I'm realizing the top-tip detector can't be centered at kernel row 2 for digits whose tops sit at image rows 4-5, since that would put the center above the valid conv2 range. So I'll shift the tip center up to kernel row 1 and keep the same positive and negative pattern around it.

I'm settling the top-tip detector's rows: one row of emptiness above at kernel row 0, the tip center at kernel row 1, and the body at rows 2 and 3, since the digit tops sit at image rows 4 to 6.

I'm checking where the left tips fall for digits like 3, which sit around columns 8 to 9 in the rows near the top.

I'm placing the left and right tip detectors with their centers on kernel columns 1 and 3, so the tips fall within the valid range of positions in the pooled grid. Once pooled, the top-tip channel cells map to a pair of candidate tip rows and columns, which I'll use to pick the exact indices.

I'm working out the column bands for the left and right tip detectors, offsetting the tip center to kernel column 1 or 3 so each pooled column maps to a clean range of image columns, and checking where the boundary cases fall.

I'm trying kernel column 3 for the top-tip detector, which would cover bands roughly at columns 8 to 23, but the bands come out uneven. I'm weighing a shift to kernel column 1 as well, since that covers the 4s' left arm and the lower-left range better.

I'm settling on kernel column 1 for the top-tip detector so the bands line up with the 4's left arm, but that leaves no room for a left-side check at ±2. I'm weighing whether to keep the tip at column 2 instead, accepting that a 1's tip falls on the boundary between two pooled columns, since the template still weights both cells.

I'm settling the tip centers for the other directions: kernel column 2 for top and bottom tips, and kernel row 2 for left and right tips, so the candidate positions stay within the valid conv2 range and each pooled cell maps to a predictable band of image columns or rows.

I'm checking where the right-side tips fall: the top of a 5 and the bottom of a 2 sit at the extremes of the detector's rows, so a center at row 2 only partly covers them. The left tips of the 3s and 5s look better placed within the range.

I'm settling on kernel row 2 for the left and right tips, which covers the middle of the digit, and accepting that the extreme tips at the top or bottom edges will only be partly detected.

I'm checking the right-side tip placement: a kernel row 1 center would cover the top-right tips of 5s and 6s, though it would miss the bottom-right tip of a 2.

I'm checking the right-side tip placement for the top-right and bottom-right tips, weighing whether the empty-cell checks above and below still hold for a horizontal stroke pointing right. I'm leaning toward accepting partial coverage of the bottom-right tip of a 2, since the overall pattern still identifies it.

I'm now listing the orientation-only error cases: 4 versus 9 is intrinsic because closed-top 4s and open-top 9s look alike, and 3 versus 5 should separate by the top-left versus top-right stroke. For 5 versus 6, the left stroke in the lower half is the key difference, since a 6 keeps it going down to the bottom-left while a 5 leaves a gap there.

I'm weighing whether structural features like loops and open ends are worth adding alongside the orientation channels, since a hole detector would separate 0, 6, 8 and 9 from the rest, while end-point detectors seem less reliable. A compromise might be eight orientation channels plus a few enclosure and tip detectors.

I'm weighing whether the tip detectors are worth their cost: they'd help separate 4 from 9 with the top tips, and 3 from 5 with the left tips, while the 5-versus-6 and 7-versus-2 cases stay ambiguous. Plain orientation channels already handle 1 versus 7 and 0 versus 8 without them.

I'm weighing whether the tip detectors earn their keep: they'd separate 3 from 8 and 0 from 6, and their false positives would mostly land on real stroke ends like serifs or open closures. Without per-feature stats, I'd be guessing at their weights, but I'm leaning toward including them at moderate strength.

I'm sketching how the left and right wall detectors for an enclosure would work at conv2, with background cells in the center and vertical-ish strokes on each side, though I'm still weighing how the upper and lower arcs should contribute.

I'm checking how the walls of a loop would show up at the center of the conv2 window, so I'm comparing the ink on each side against the background in the middle.

I'm checking how much of a wall lands in the 3x3 windows on each side of the center cell, which depends on how far the wall sits from the hole: a close wall gives a strong signal, while a wall farther out only partly overlaps the nearer window.

I'm estimating how strongly a slanted wall registers: a vertical line detector gives about 0.6 to 0.7 on a wall tilted 22.5 degrees, and the diagonal detectors give about 0.5, so I'll weight them around 0.7. At 45 degrees the vertical response drops to about 0.2, which is where the diagonals have to take over.

I'm defining the left-wall term of the enclosure detector as a sum over the two cells to the left of center, each combining a vertical-line response with a weighted diagonal response to catch slanted walls.

I'm pinning down the left-wall term: the cell two pixels left of center covers wall positions roughly 1 to 4 pixels out, and the one four pixels left covers about 3 to 6.

I'm checking whether a narrow hole can still register: if the walls sit only 3 pixels apart, the center cell's background signal may get swamped by the wall responses on either side.

I'm setting up the left-right enclosure detector: the center background cell must be empty, and the wall terms on each side add up when the walls sit a few pixels out from the hole. I'm still checking how narrow a hole can get before the background signal drops too low to fire.

I'm checking whether the left-right enclosure detector could fire falsely on two vertical strokes with an empty gap between them, such as the top of a 4. I'm still weighing how often that happens compared with a true hole.

I'm checking which digits a left-right enclosure would pick out: 0 across its whole height, 4 in the top half, and 6 in the bottom half. Some stroke pairs like a 2's top hook or a 5's belly could trigger it falsely, so I'm weighing how often that happens.

I'm checking the up-down version of the same enclosure test, where the walls sit above and below the center. A 0 is too tall for both walls to fall within reach, so it doesn't fire on one. A 2's top hook and the diagonal below it can, though, which puts the signal in the upper middle, and I'm weighing where a similar pattern would show up near the bottom bar.

I'm checking the up-down version of the enclosure test against each digit: 3 and 5 both trip it in two places, while 6 and 8 trip it at the bottom loop, and 4, 1 and plain 7 don't trip it at all.

I'm checking the up-down version of the enclosure test too: it adds a top and bottom wall term plus the center background cell, and I'm working out where the two tests overlap for each digit.

I'm checking where the hole centers of the 9, 6 and 8 fall against the bands of rows the kernel covers, and how that lines up with the 0's center around row 13.5.

I'm settling on the conv2 channel layout: horizontal, vertical, and both diagonal orientations each get two tap rows, with the left-right and up-down enclosure detectors, four tip detectors, and two channels still undecided.

I'm settling on which two channels in conv2 are left: the two-column vertical taps and the diagonal orientation taps already cover row and column placement, so I'm considering whether a convexity-style pair, like a right-facing arc from a down-right diagonal above a down-left one, would separate 3 from 5 better.

I'm laying out the rest of the conv2 channels: the diagonal taps tell an S-shape of a 5 apart from the long diagonal of a 2, and I'm now weighing whether a coarse long-vertical-stroke feature could fill one of the two remaining slots.

I'm considering a crossing detector that fires where the diagonals meet at the center of an 8, and a horizontal-vertical cross for the 4, by checking whether the line responses coincide in the same cell.

I'm checking the horizontal crossing case now: where a horizontal and a vertical stroke meet, the overlap region gets counted twice, so the response comes out a bit lower than the sum of the two lines alone.

I'm weighing whether 14 and 15 should be orientation channels with half-offset row bands for redundancy, or something else, since a crossing detector would need four neighboring cells to fire and the center cell alone is not enough.

I'm considering a left-profile feature for the two leftover channels: for each cell, whether there is any ink to its left within the kernel's reach. That would separate digits by where their left side is open, such as the 3's deep left opening in the middle rows, which the orientation and enclosure channels don't capture.

I'm testing an up-down enclosure variant that stays silent when a left wall is present, so it would catch cavities open to the left like a 3's middle or the lower gap of a 5, while the right-wall version covers the opposite side.

I'm now checking the up-down enclosure variant where the right wall is absent, which would pick up gaps that open to the right, like the upper cavity of a 5 or the upper curve of a 6.

I'm settling on four channels for the leftover slots: plain up-down, left-right, and two open-gap versions, one that stays silent when a left wall is present and one for a right wall. Those gap features should separate 3, 5, 2 and 6 better than the earlier orientation pairs did.

I'm settling the last channels as open-gap detectors: one that stays silent when a left wall is present, and one for a right wall. For the upper cavity of a 3, the top arc and middle bar fire, but the question is whether the left side is really open, since the 3's top-left tip sometimes puts ink there.

I'm settling the last two detector ideas by checking the up-down cavity against the left and right walls, and I'm planning to define the tip features from the pooled ink maps next.

I'm defining a top-tip kernel over the pooled ink map: the cells above the tip must be empty, and the tip cell itself should show ink, so the feature fires when a stroke starts at the top of its region.

I'm checking the top-tip kernel's alignment against the pooled ink map: if the stroke starts right at the tip cell, that cell reads full ink and the cell above reads about a third, and if the stroke sits a little lower, the readings shift. I'm weighing which placement gives the strongest response while keeping the cell above mostly empty.

I'm weighing whether a -1 weight on the cell above the tip works just as well as -1.5, since both placements give the tip cell about 0.67 once the body terms are added.

Defining the top-tip kernel on the ink map now: the tip cell gets the strongest weight, and the cells below it form the body of the stroke, with the sides weighted lower.

Still writing the top-tip kernel weights...

Still working out the arc-top variant of the kernel's weights...

I'm checking the arc-top kernel on a narrow stroke end: the arc drops below the tip at about ±2 px, so the sides cancel and only a narrow stroke's end fires. A horizontal stroke gives no response, so the feature stays quiet there, and I'm now looking at a corner-shaped end.

I'm checking a diagonal stroke that passes through without a tip: the response from the tip cell and its diagonal neighbor is offset by the weights on the cells above, so the total comes out negative and the feature stays quiet.

Still working through the top-tip kernel's weights, checking the leak from neighboring cells and the body terms below the tip, and rescaling the total so the tip response stays near one.

Still working out the column ranges where the tip's stroke center can sit, grouping them by which conv cell each one lands in.

Still working out the column-to-pixel mapping for the tip kernel, checking which image columns each conv cell covers for different tap offsets.

I'm mapping the tap offsets to pixel bands: each cell covers a 4-pixel band that shifts with the tap. To allow some tolerance, I'm thinking of a soft assignment that weights each cell by its distance from the band center.

Still working out how the second-layer taps map back onto image columns, weighting the horizontal-stroke channel across the overlapping column windows.

Still working out the weights for the horizontal and vertical channels, spreading each tap across the overlapping columns at about 0.4 apiece.

I'm sizing the response levels for the orientation channels, which come out around 0.5 to 1.2 where the stroke is present, and I'm checking whether the left-right, up-down and tip channels land in that same range.

Still working out the template weights, and I'm weighing whether the bias should scale with the expected feature magnitude. I'm also considering adding negative weights to the templates, so that classes without holes are pushed down by the channels where other digits have them.

I'm considering whether the nearest-centroid classifier already separates 4 from 9, since the 9 template shares most of the 4's shape and differs mainly by the top arc.

I'm checking that the nearest-centroid rule already gives a clean margin between digits: the difference between two class templates, minus half the gap in their squared norms, is the optimal linear split for isotropic classes. That means explicit negative weights aren't strictly needed, and I can tune the channel gains to emphasize the key discriminators instead.

I'm weighing how much the bias should follow the feature magnitude, probably scaling it by about 0.6, and I'll tune that later. Since the uncertainty in each template is the main source of error, I'm leaning on blur to absorb it. The orientation channels fire on many cells while the structure channels fire on only a few, so I'm giving the left-right and up-down channels a larger gain than the rest.

I'm laying out the target shapes for each digit as polylines in the 28x28 frame, centered at (13.5, 13.5), and starting with the 0 as an ellipse with a stroke-center radius of about 8.5 vertically.

I'm sketching the 2 next, starting from the upper-left, arcing over the top to the right, then cutting diagonally down to the bottom-left corner, and I'm also deciding how to approximate the 1 as a near-vertical stroke with an optional slanted flag.

I'm writing out the polyline for the 2 and checking where its bottom bar and diagonal sit relative to the center of mass, which looks roughly right. I'm also starting to note where the open-left gap and the wedge below the diagonal fall in the grid.

I'm placing the 2's left tip near (9, 8), where it's ambiguous whether it reads as a left or bottom tip, and the right tip at (21, 20). Next I'm sketching the 3 as a polyline starting at the top-left and tracing down toward a middle notch that reaches leftward.

Now I'm placing the 3's lower tips and the 4's stroke layout: a left arm sloping down toward a crossbar, with a vertical stroke on the right side.

I'm checking the center of mass for the 4 by weighting the vertical stroke, left arm, and crossbar, which puts the digit only about half a pixel off center, so I'll shift the columns left by 0.5. I'm also starting to note where the left-right channel responds between the arms above the crossbar.

I'm placing the 5 as a top bar with a vertical stroke down the left, then a rounded belly curving right and back toward the lower-left, with open-right and open-left gaps above and below the belly.

I'm placing the 6's loop near the center-right and tracing its upper stroke down and around, with the tips positioned at the top right and the lower left.

I'm laying out the 7 as a top bar running across the upper row, then a diagonal stroke sloping down-left toward the bottom. Since most of its ink sits up high, its center of mass falls several pixels low, so I'll need to shift it down to re-center.

I'm going to define each digit's prototype in a 20x20 local frame, then auto-center it by shifting the length-weighted center of mass to (13.5, 13.5), since the 7's mass sits high enough that a fixed placement would be off.

I'm placing the 8 as two stacked loops, a smaller one on top and a larger one below, crossing near the middle, and tracing the figure-eight polyline through them.

I'm finishing the 8's coordinates and placing the 9 as a loop with a slanted tail, then marking the left-right and up-down responses near the loop's center.

I'm defining the orientation templates from each segment's angle, with horizontal, diagonal, and vertical responses falling off with angular distance. I'm weighing a tuning curve that gives partial response at 22.5 degrees and none at 45.

Still writing the orientation templates...

I'm working out how each conv2 band's membership falls off near its edges, using a soft window that gives partial weight to strokes just outside the band, and I'm checking that overlapping taps still cover the cells evenly.

I'm setting the structural templates for the left-right and up-down channels at the center tap, with each cell covering about four pixels and a soft margin for stroke placement.

I'm working out where the tip of a stroke lands in the pooled grid, reasoning from the top of the stroke back through the first-layer cells to the pooled rows that read it.

Still working out the tip positions in the pooled grid, placing the top, bottom, left, and right tips against the tap offsets that read them.

I'm weighing whether to shift the right-tip kernel to row tap 1, which would let the 5's top-right tip and the 4's bar end land squarely in their bands instead of on the edge.

I'm deciding to use row tap 1 for the right tip, so the 5's top-right tip lands cleanly in its band. The bottom-right tip of the 2 may get lost in the margin, but the horizontal channel at the bottom covers it. Then I'll check the empty cells above and to the right of that tip.

I'm checking the tip-kernel layout for the left and right tips, settling which row taps read each one and where the soft margins fall for the 3, 7, 5 and 2.

Still working out the tip kernels, building the top-tip version first and deriving the bottom, left, and right tips from it by flipping and transposing.

I'm working out the right-tip kernel by shifting the left-tip layout up one row, which drops the lateral check four pixels above and leaves the empty row at the bottom. That means I lose the check for a stroke turning upward at four pixels, which matters for corner shapes like a stroke that goes right and then turns up.

I'm going to shift the right-tip kernel up one row so the 5's top-right tip lands in its band, and I'll derive the bottom tip from the top one. The corner check I lose is a stroke turning upward four pixels out, but the negative cells beyond column 4 should still kill the false positives I'm worried about.

Still writing the top-tip kernel for the 5x5 filter...

Still checking the top-tip kernel's arithmetic, with the bias and scale applied.

Still checking the top-tip kernel, this time against the "4" arms and a "1" with a flagged upstroke.

Still checking the top-tip kernel against the background filter, which should stay near 1 in empty regions and only drop where ink sits nearby.

I'm checking whether a left-side response could fire falsely when two vertical strokes sit close together, since the left arm of the kernel could then push the sum above the bias.

Still checking the kernel's bias and scale, this time asking whether the left and right wall inputs can be made more robust for bold strokes by adding a bit of ink signal.

I'm checking whether the wall terms could fire falsely on a horizontal stroke, and whether a 0.7 weight on the diagonal inputs keeps the bold-stroke cases from being lost, and I'm leaning toward keeping the pure line version with a threshold of 2.0.

I'm scaling the line kernels by 1.3 so that a typical real stroke gives a response near 1, and I'm checking how the wall terms and the bias then behave on weak and false-positive cases.

I'm checking whether a single strong vertical wall could push the left-right response above threshold along a whole stroke, like a "1". I'm weighing a threshold of 2.3 with the line scale at 1.3 to keep those false positives down.

Still writing the UD and UDoL kernels, weighing whether the right-wall term is needed to tell an "=" apart from a 3.

I'm checking the hole channel next: a four-way AND of the walls and bars would fire falsely when three of them are strong, so I'm keeping the plain up-down channel instead.

Still writing the feature weights, deriving each channel's entries from its template and laying them out in channel, row, column order.

I'm settling the bias for the feature weights: if the input is a bit weaker than the template, a bias of about 0.35 times the template energy still lets a true superset class win, and a subset class stays below it.

I'm settling the feature bias at about 0.35 times the template energy, which lets a true superset class win while a subset class stays below it. I'm also thinking about a global scale on the weights and bias, starting at 1 and tuning from the confusion matrix.

I'm settling the feature bias at about 0.35 times the template energy, so a true superset class can still win while a subset class stays below it. I'm also weighing a global scale on the weights and bias, probably around 0.5 to start, and tuning it from the confusion matrix.

I'm laying out the digit prototypes in image coordinates, starting with the 0 as a tilted ellipse, and the 1 as a near-vertical stroke with a slanted variant alongside it.

Still defining the digit 2 prototype as a polyline, with the bottom bar running across the base.

Still defining the tip positions for the 2 prototype, placing the bottom-left end near row 9 and column 8.5 and weighing how the downward stroke there should split between the left and bottom tips.

Still working out the second digit's prototype, placing the tips and checking whether the upper-middle and lower-middle hole channels respond at the right spots.

Still defining the 3 prototype as a polyline, tracing its top arc and the right-side bowls.

Still defining the digit 4 prototype, with its left arm and the crossbar.

Still working out the digit 4 prototype's tip positions and which line channels should fire on it.

Still defining the 5 prototype, placing its top bar and vertical stroke and the rounded belly beneath them.

I'm tuning the bottom of the 5 prototype now, checking how big the empty gap is between the top bar and the belly so the background filter stays near 1 there. The belly top should sit closer to row 12, which leaves enough empty rows for the background to read clearly.

Still writing out the 6 prototype's coordinates, placing the top tip near row 5 and tracing down the left side to the base.

Still working out the 7 prototype's crossbar, and the 6's remaining tip and channel choices are settled, so I'm skipping the extra right-side response there.

I'm weighing whether the bottom tip of the 7 prototype should carry full weight, and checking how centroid centering shifts the bar and the bottom point lower in the image, since MNIST sevens usually sit that way.

I'm checking the 7 prototype's bottom tip against the p1 grid: at row 25 it falls past the last covered row, so I'm considering moving the tip kernel down a row to catch it.

I'm checking whether bottom tips on 7s would get missed: their ink reaches row 24 or 25, so a tip at kernel row 3 would have its "empty beyond" cell covered by the stroke and never fire.

I'm considering whether the bottom tip for the digit prototypes should sit at kernel row 4 without a check below it, since bottom tips land around rows 22 to 25 at the edge of the pooled grid. I'd be restricting the fully connected attention for that tip to the last pooled rows.

I'm now asking whether a narrow vertical stroke ending in the bottom rows, around 21 to 26, can serve as a "pointed bottom" feature that separates 1, 4, 7 and 9 from digits with flat or round bottoms like 0, 2, 3, 5, 6 and 8, since those have horizontal ink that would trigger the side cells.

I'm checking the bottom tip design for the kernel: a tip at kernel row 4 with no check below would catch 7s whose ink reaches the last pooled row. Restricting the fully connected weights to the lowest pooled rows would keep it from firing on passing strokes higher up.

Still writing the bottom-tip kernel, with a single positive cell in its last row and a body row just above it. The plan is that it fires on any narrow vertical stroke reaching the bottom of the pooled grid, so 7s and 1s whose ink runs down to rows 21 to 23 would register.

Still checking the bottom-tip kernel against 8s and 0s: their bottom arcs would put ink at the sides of the cell and should knock the feature out.

Still checking the bottom-tip kernel against 8s: their loop bottoms put ink on the sides of the cells at the far columns, so those negative weights would partly cancel the tip, with the body row still giving a small positive net.

Still checking the bottom-tip kernel against 8s and 6s: their loop bottoms put ink on the sides of the outer cells, which pushes the total to about zero. Next I'm turning to the top tips, where the same beyond-row check would sit above the stroke.

I'm checking whether a top tip for 6s, whose ink sits slightly higher, would still have clear space above it if the check row overlaps the stroke, which would weaken its response.

I'm checking whether a top tip could drop its beyond-row check and rely on the sides instead, which would mean a bare narrow vertical stroke in the top rows counts as a tip. Given that digits rarely reach above row 4, I think that holds up.

I'm checking whether a narrow-top feature for the top tips needs the same beyond-row check, and I'm leaning toward dropping it for the top row too. Given that digits rarely reach above row 4, I'd treat any narrow vertical stroke in the top rows as a tip and only keep the fully connected weights on the outer cells.

I'm weighing whether a top tip should keep its beyond-row check, since digit tops usually sit around rows 4 to 7 and that check keeps a passing stroke from firing as a tip. I'm leaning toward keeping it for the top, and I'll sort out the bottom tip design afterward.

I'm estimating where the 7's centroid lands: the bar and stem put it around row 10, so the shift down toward row 13.5 is about three pixels, which means its bottom tip sits lower than the detector range I had planned.

Checking the bottom tip now: 7s push ink down to rows 25–26, past where a beyond-row check could reach. So I'm dropping that check for the bottom feature and placing the tip at kernel row 4, which lets it cover the last pooled rows.

I'm checking whether a narrow vertical stroke in the bottom rows, around 21 to 26, would still register for the bottom-tip feature, and whether wide bottoms like 3s or 5s would slip past it.

Now I'm settling the bottom-tip kernel as a narrow-bottom detector with no beyond-row check, and the top-tip kernel with one, then mapping the left-tip kernel's column taps to pixel ranges.

Now I'm settling on the left and right tip kernels: I'll map their column taps to the pixel ranges they cover, and check that the right tip's lower row lines up with the stem so 2's bottom-right corner gets only a small weight.

I'm checking how the background feature behaves near strokes: even two pixels off a 3-pixel-wide stroke, the weighted ink in the window is low, so the background term stays high and only drops right on the stroke's center.

I'm checking whether the "2" digit's left hook and right side could produce a false left-right wall match near the top of the grid, since their spacing is close to the template's tolerance.

I'm assigning partial left-right wall weights to the 2 and 3 templates, then setting the 9, 4, 7 and 6 wall terms aside since they don't need a top or bottom wall.

I'm assigning the hole-digit cells their own rules: 6 gets a single up-down wall at its lower-right, 8 gets two, and 9 gets one near its loop, while 0 has none. For the open-bottomed digits, 3 and 5 get strong up-down walls, 2 gets two weaker ones, and the one-sided versions go to 3, 5 and 2 at the cells where their arms split.

I'm settling the gain values now: orientation at 1, the left-right wall and the up-down walls at 2.5 and 2, and the open-side walls at 2. I'm also weighing the tip gains at 1.5 and how many cells a single point-like structure touches when it falls on a band boundary.

I'm weighing the orientation channels against the structural ones: each stroke segment feeds several overlapping channels and cells, so orientation carries roughly 50 of the total weight against about 10 for the structural features. Giving the structural gain around 2.5 to 3 would bring them to about a quarter of the evidence.

Now I'm settling the orientation kernels for the second conv layer: four channels, two horizontal and two vertical, each reading a single row or column tap of the pooled map and spreading weight across the neighboring taps at 0.4.

Now I'm settling the 16 conv2 channels: orientation channels for each stroke direction on fixed row or column taps, then the structural ones for left-right and up-down walls, the open-side variants, and the top, bottom, left and right tips.

Now I'm mapping out the vertical-stroke channels: each fine band gets an interval around its tap position, and the coarse cells get wider windows that overlap their neighbors. I'm also deciding how a stroke point falling outside its band should fall off with distance, with a soft margin of about two pixels to absorb writer-to-writer variation.

I'm settling the margin for the fine vertical bands at 3 pixels, so a stroke sitting 1.5 pixels outside its band still counts for about half. I'm also weighing the template values, which run from 0 to 1, and how the bias term behaves across classes.

I'm weighing whether a uniform negative offset across all template cells would cancel out between classes, since it would shift every score equally.

I'm now checking the centroid shift for each prototype, and I'm aligning the structural point positions to the same pre-shift coordinates as the rest of the template.

Now I'm writing the left-right wall kernel, which reads the center row of pooled features on either side of a hole-center cell, and I'm defining the up-down wall kernels over the upper and lower cells of that column. Next I'm setting up the horizontal line kernel with its center-heavy profile.

Now I'm defining the horizontal and vertical line kernels from a center-heavy profile, scaled so a centered 3-pixel stroke sums to about 1. The diagonal kernel weights cells by their distance from the main diagonal, and the positive and negative cells balance out to zero.

Now I'm settling the diagonal kernels: the anti-diagonal one uses the same distance-from-diagonal profile, and I'm checking that a 45° three-pixel stroke still lights up its central cells even with the outer cells pulling the response down.

Now I'm adjusting the diagonal profile so the cells two steps off the main line carry less negative weight, which brings the 3-pixel diagonal response closer to the horizontal one.

I'm checking the crosstalk values: a horizontal stroke leaks about 0.28 into the diagonal channel, slightly more than before, which I'll accept. I'm also noting that diagonal strokes leak only about 0.2 into the horizontal one, and that a 45° template offset is ignored since its real response is small. Last, I'm setting the background kernel's center weight to −0.8.

I'm settling the bias and scale values for the conv2 channels: the line-detector scale of 1.3 and the left-right, up-down, and open-side walls at about −2.3, with the tips at a smaller negative bias. I'm also checking whether a vertical line response of about 0.88 after max-pooling is strong enough to clear the left-right wall threshold.

I'm checking the leftover-width estimates for the left-right wall: a typical stroke gives about 1.0 after bias, a crisp 3-pixel wall about 0.3, and thin or bold strokes land in between.

I'm checking how the diagonal strokes behave inside the upper and lower wall strips, since a '/' stroke crossing those cells could push the up-down wall response up or down.

Still writing the tip kernels: the bottom-tip template gets its own row profile with strong negatives at the outer cells, scaled by 1.3 with the same −0.39 bias. I'm checking that its vertical response lines up with the top-tip one.

Still working through the bottom-tip kernel: the 0.9 scaling and −0.3 bias should bring its response in line with the top-tip one, and I'm checking that the sides and body balance out for a plain vertical stroke.

Still writing the bottom-tip kernel: I'm narrowing its soft margin to about one pixel, so a tip near row 22 doesn't leak weight into the row above and fire on unrelated strokes.

Still working on the bottom-tip kernel: I'm forcing its response into row 3 alone with a near-zero margin, and clamping the tip coordinate so it can't spill into row 2 and fire on unrelated strokes.

I'm checking which bottom-tip column separates the digits: the 1 and 7 should land in column band 1, while the 4 and 9 land in band 2, with some 9s and 7s slanting into neighboring bands.

Still writing the template code: I'm defining a helper that gives a coordinate full weight inside its band and fades it linearly outside, and I'm about to lay out the fine-band intervals around each tap position.

Writing the orientation-drawing loop: each segment gets sampled along its length, and every sample feeds the orientation channels with a cosine-squared falloff, weighted by its row and column band membership.

Still writing the template code: the horizontal and diagonal channels take their row tap as the fine band and their column as the coarse band, while the vertical channels reverse that. The structural points (walls, tips) use fine bands on both axes with a 2.5-pixel margin, except the bottom tip, which is pinned to row 3.

Now I'm working out how to shift the template by the stroke centroid, averaging the midpoints of the main strokes weighted by length, and I'm thinking through how realistic MNIST slant might be handled.

Still writing the stroke lists for the zero: I'm placing an ellipse at the center with a vertical radius of 8.5 and a horizontal radius around 6, adding a slight rightward shear so the shape leans like typical handwriting.

Checking the kernel's column reach: I'm recomputing which cells cover the left wall, where a wall at a given offset from the center falls across the two pixels each cell spans.

I'm checking how wide the zero's ellipse is at different heights, since with a radius of 6 the left and right walls sit just outside the kernel's full-response range near the middle rows. The walls only line up with the kernel near the top and bottom, where the ellipse narrows and the walls angle in, so I'm weighting those cases at about 0.7.

Still working on the stroke lists: I'm placing the zero's left and right walls at a middle-row point and near the top and bottom, and expect the wall detector to fire mostly at the narrower rows.

Still laying out the stroke lists for the 3: I'm starting the first points near the top and checking how they line up with the zero's walls.

Still laying out the stroke lists for the 4: the bounding points for the 3's walls are already set, so I'm moving on to the 4's opening strokes.

Still writing the stroke lists for the 5: I'm placing its top bar, left vertical, and curved bowl, and adding the tip weights at the top right and lower left.

Still writing the stroke lists for the 6, 7, and the rest of the digit prototypes: I'm placing the 6's top tip and wall points, then the 7's top bar and diagonal, with weights chosen so each wall and tip detector responds where its shape should.

Still writing the stroke lists for the 8 and 9: I'm placing the 8's two loops with side-wall weights of 0.8, and the 9's upper loop with its tail.

Still placing the 9's stroke points, and I'm checking how its loop and tail sit once the centroid shift moves the whole shape down about 2.5 rows.

Checking the vertical placement of the 6 and 9 after the centroid shift, I'm estimating the 6's top tip lands near row 3 and its loop center near row 16. I'm also checking the 4's row centroid, which comes out around 12.9.

Still checking the top tip of the 6: at row 3 it sits just outside the first band, so the detector should still respond at about 0.92.

Still writing the template weights: I'm settling the 6's top-tip weight at about 0.5 since its ink sits right on the edge of the first band, and I'm about to fold the orientation, left-right and up-down gains into the fully connected weights.

Still writing the weights: I'm setting the structural feature gains and absent-feature penalties so a true-class input lands on a positive net, and I'm checking the orientation channel magnitudes for long strokes.

Still working out the template weights: I'm settling the orientation gain around 0.4 and checking that the diagonal channel's sign convention matches the other templates.

Still writing the template code: I'm finishing the orientation channel mapping, where a stroke at angle θ is taken mod π and the diagonal channels follow the slash and backslash directions.

Still writing the convolution filters: I'm setting up the first-layer kernels, with a horizontal profile and its transpose for the vertical one.

Still writing the first-layer kernels: I'm building the background-suppression filter with negative weights around a positive center, and starting the ink-detection kernel as a flat 3x3 patch.

Still writing the second conv layer's kernels: I'm setting the horizontal and diagonal orientation weights so each responds to strokes in its own direction.

Still writing the second conv layer's kernels: I'm setting the background-suppression weight and the vertical channel for the left-right channel, then continuing into the next group of orientation filters.

Still writing the second conv layer's kernels: I'm setting the left-right channel weights and the vertical inhibition for the open-left and open-right variants.

Still writing the kernel tables for the second conv layer's tip detector, with the top-tip weights set and the bottom-tip kernel next.

Still writing the second conv layer's tip kernels: I'm setting the bottom-tip, left-tip and right-tip weights and their biases.

Still writing the kernel tables for the second conv layer's left-tip detector, with the lateral rows set up as the transpose of the top tip.

Still writing the right-tip kernel: I'm flipping the left-tip pattern and shifting it up a row so the tip lands at row 1.

Still writing the second conv layer's right-tip kernel, shifting its pattern up a row. I'm also checking the left-tip false positives on a "(" arc, where the vertical cells alongside the tip could light it up.

Still writing the fully connected templates: I'm defining the band and wide-band helpers and the membership function that scores how close a position falls to each stroke's range.

Still writing the orientation channel table: I'm mapping each channel to its stroke direction and which tap positions it reads.

Still writing the stroke-drawing helper: I'm sampling each segment at half-cell steps and computing its angle to decide which orientation channels it feeds.

Still writing the draw-strokes helper: I'm looping over the orientation channels and their tap positions to add each stroke's contribution into the matching cells.

Still writing the centroid helper: I'm computing the stroke-weighted center of the digit skeleton so I can shift the whole template to the middle of the frame.

Still writing the point-drawing helper: I'm setting up the lookup of each keypoint's channel and row/column bands, and starting the row-membership weighting for each of the four bands.

Still writing the digit templates: I'm defining the zero's ellipse points with a slight slant, then turning to a second pass on the key digits to check their stroke placement.

Still working out the templates for the remaining digits: I'm checking the 1's vertical stroke with its slight rightward slant and the variant that adds diagonal weight, then moving on to the 7's stem, which I'm treating as a mix of vertical and diagonal orientations.

Still writing the digit templates: I'm checking the 2's bottom loop, the 5's short top bar, and the 3, 6 and 8 shapes, then planning the gains and biases while keeping the fully connected weights consistent with the feature layout.

I'm considering a lower γ of 0.3 so the large templates for 8, 0, 3, 2 and 5 don't get over-penalized, though I'm settling on γ = 0.35 for now and will adjust the biases after checking the confusion matrix.

Still checking the first conv layer's pooled cells against the horizontal orientation taps, so the mapping from each pooled position back to its input rows stays consistent.

Still writing the pooling-to-input mapping for the second layer: I'm checking that the wide window for each pooled column covers the right pixel span, and noting that a point-wise membership will slightly overestimate the response for short strokes.

Still writing the digit polylines: I'm checking the 2's bottom bar and diagonal against the centroid shift, and confirming the upper arc's gap sits within the wall reach.

Still placing the points: I'm putting the upper-loop point at (10, 15) so it sits clear of the left hook, and the lower point at (18, 15), where the diagonal and bottom bar leave a gap that fits the wall reach. Next I'm checking the 3's first stroke, starting from the top at (7, 8.5).

Still writing the digit templates: I'm checking the 5's top bar and the left-wall suppression on its upper-right gap, and confirming that the belly-top gap stays within the wall reach.

Still placing the 5's lower points: I'm checking where the belly arcs converge near the right wall to see whether the bottom-up gap stays within reach.

Still placing the 5's lower point and the 3's lower gap: I'm checking that the bottom arc's gap stays within wall reach near the right side.

Checking the 6's hole center from its loop points, I'm settling the 3's upper and lower points at (8.8, 14.5) and (17.7, 14.5).

Checking the 8's top loop against the wall reach, I'm settling its points on a symmetric shape about column 13.5 so the loop sits centered.

Still placing the points for the 5, 4 and 0 digits, checking each loop and arm against the wall reach. For the 0 I'm working out the half-width of its left and right points at row 8.5.

I'm settling the leftmost-right wall weights for the 0 at rows 8, 13.5 and 19, allowing for the slant that shifts the points a little at the top. I'm also checking whether explicit negative weights are needed for the 1 and 7 cases, and I'm keeping the wall pitfalls in mind so the background stays clear.

I'm checking whether raising the membership threshold to 2.4 keeps the true case positive, since typical antialiased strokes would give a margin of about 0.86 under that setting.

I'm settling on a threshold of −2.4 for the left-right, up-down and corner-wall detectors, since a typical antialiased stroke still leaves a clear margin above it. I'm also checking whether weaker background cells, like the small inner holes of the 8's top loop, stay positive enough under that threshold, and they do. Next I'm thinking about whether the up-down detector might fire falsely on crossed 7s, since their crossbar could give a gap in the upper area.

I'm checking whether crossed 7s could trigger the upper-wall detector, so I'm giving the 7's template a small weight of 0.3 at (9.5, 15) to handle that case. For the 0 and 9, the up-down detector looks unlikely to fire, but the 9's curled tail might behave like the lower points on the 5 and 3. I'm now turning to the 6, where the top stroke's shape determines whether the up wall can register.

I'm checking the 6's upper stroke against the loop top to see whether the upper wall fires near column 15, where the gap centers around row 10.5.

I'm adding a small weight of 0.4 to the 6's upper-right detector at (10.5, 15), since the upper stroke's gap there resembles the 5's upper pattern, and I'm noting that the left-right wall is what separates 6 from 5.

Still writing the code: I'm building the weight-construction function for the digit detectors, with the templates and the fully connected layer's bias terms.

Still writing the digit definitions as a prototype table: each digit gets its strokes with weights, and its points labeled by kind, row, column and weight, starting with the 0 and 1.

Still writing the digit definitions: I'm listing each digit's points and weights for the 2 and 3, using the same kinds of wall detectors as before.

Still writing the digit definitions for the 4 and 5: I'm listing the stroke points and weights for each, checking the 4's arm and stem against the wall detectors.

Still writing the 6's stroke points and its upper detector weight.

Still writing the digit definitions: I'm listing the 8's stroke points and weights, which continue the digit detectors I've already set up.

Still writing the digit definitions: I'm listing the 9's loop and tail strokes, along with its points and weights.

Still writing the 9's stroke points, checking its loop's centroid shift and the closing point of the loop.

Still checking the 7's bar: after the shift its band lands mostly on the row-1 cell, and I'm checking the 0's point positions against the slant.

Next I'm settling the scale factor S by estimating the sum of squared template values for a digit like "1", counting the full cells in the vertical bands plus the partial overlaps from the neighboring margins.

Still estimating the scale factor S: the first-layer template sum for a "1" comes to about 11 from the vertical channels, plus roughly 3.4 from the diagonal channels, and about 4.9 from the tips, for a weighted total near 19.

I'm estimating the scale factor against a sample "8", which should land near 80, and then checking the bias terms. For a true 1 the logit comes out around 3.7, and for a true 8 around 8.4. Cross-checking how an 8 scores on the 1 class gives roughly −0.2, so the scale looks reasonable, and typical margins of several units should keep predictions confident.

Still writing the weight-construction code: setting up the first conv layer's 5x5 kernels and the horizontal profile for the edge detectors.

Still writing the weight-construction code: setting up the second conv-layer kernels and the template draw helper.

Still writing the code: I'm adding the mem helper and the BG-channel and tip detectors, and checking their biases so the background stays silent.

Still writing the weight code: I'm checking the sign convention for the diagonal kernels under cross-correlation, so the anti-diagonal filter lines up with the strokes it should detect.

I'm checking whether the class-8 template, which has its vertical responses concentrated at the sides and diagonals at the center, would overlap much with a strong vertical stroke like a 1, and whether the template magnitudes might let one class dominate every input.

I'm checking whether the 8's vertical-ish segments leave its vertical response weak, since its polyline runs mostly at 45° and steeper angles, and I'm estimating how much each segment contributes.

Checking whether the 8's vertical strokes sit close enough to the center band to give a partial response to a plain vertical "1".

Still weighing the margin for the orientation templates: at 3.0 the neighboring bands would pick up at least a third of the signal, so I'm considering 2.5 to keep the detectors sharper.

Checking the column bands for the bottom tip against the 7, the 1, the 4 and the 9, to confirm each lands in the right pooled cell.

Checking the centroid of the 4's arm, working through its stroke points where the segments meet.

Still checking the 4's centroid: the arm, bar and stem midpoints give a small offset of about 0.4 rows down and 0.35 columns left, so the shift is minor.

Still writing the weight code: setting up the first conv layer's kernels and the horizontal edge profile, with the scale factor LS and a 5x5 template for the horizontal detector.

Still writing the weight code: defining the vertical, diagonal and horizontal 5x5 kernels for the first conv layer and their channel indices.

Still writing the conv2 weights: I'm setting the bias-free kernel entries for the horizontal and diagonal channels across the three central column taps.

Still writing the conv2 weights: I'm filling in the bottom-tip and background channels, setting the horizontal and vertical taps for the center column band.

Still writing the conv2 weights: I'm filling in the wall-detector taps for the right-hand channels and the negative-weight edge kernels.

Still writing the weight code: I'm finishing the conv2 kernel entries and the orientation channel layout, with the bias terms and the wall-detector taps set for the remaining channels.
