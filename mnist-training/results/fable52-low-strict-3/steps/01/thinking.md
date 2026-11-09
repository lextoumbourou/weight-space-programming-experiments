I'm sketching a hand-written CNN for MNIST, with 8 oriented 5x5 edge and stroke filters in the first layer, pooled down to 12x12, then 16 5x5 filters in the second layer, and a final 256-to-10 fully connected layer. I'm leaning toward a template-matching approach, where the first layer stays close to a blur or identity so the features stay simple.

I'm working out how the final 4x4 grid maps back onto the input, and by using a center-tap selection in the second conv layer I can tighten each cell's receptive field to roughly the central 20x20 region of the digit.

I'm weighing how to build the second-layer features and the FC template: I could rasterize stroke segments into the 4x4 orientation grid by hand, which avoids running the network. For conv2 I'm considering pass-through channels at the center tap and offset channels for finer spatial resolution, with the goal of keeping the design manageable.

I'm settling on the conv1 filters now: four oriented bar detectors, plus a few remaining channels that I'm still weighing, possibly a blur or end-stop feature, since MNIST strokes are only two or three pixels wide and polarity matters.

Now I'm working out whether a single conv2 channel can use a 4x4 pooled grid to tighten the receptive field, and how the final cells line up with the input pixels.

Shifting the conv2 tap changes which input rows each cell reads, so I'm checking whether offset taps can cover the full 4 to 23 range rather than just the central 6 to 21.

I'm checking how much of the 20-row digit span a single tap offset can cover, since each 4-pixel-pitch cell only reaches part of it. I'll combine several tap offsets across different channels so the 4x4 grid tiles the full central region.

I'm weighing a conv2 channel that sums several taps, so each cell's footprint is wider and overlaps its neighbors, which would cover the whole 4 to 23 span. That blurs things a bit, but it covers everything. I'm also considering whether a separate conv2 design built around distinct part detectors would be more interpretable, though a hand-built version is harder to get right.

I'm narrowing down which conv1 and conv2 features would separate digits best: the four bar orientations, plus a few other channels for things like endpoints or ink density. Since conv2 has 16 channels, I could split them into orientation channels on two offset grids and spend the rest on higher-level detectors, such as a bar sitting over empty space, that help separate confusable pairs like 4 and 9 or 3 and 5.

I'm noting that a linear classifier on oriented energy should land somewhere around 60 to 75 percent with hand-drawn templates, below the roughly 92 percent a trained linear model reaches on raw pixels. I'll build a renderer that turns each stroke into the same feature layout the network produces, so the templates line up with the actual cells.

Working out the scale of the features is the open question now: I can't run the network, so I'm estimating the response analytically. For a stroke about 2.5 pixels wide at roughly unit intensity, I'll see how strongly a bar filter fires and use that to set the template weights and bias.

I'm settling on a cosine-style scoring rule for the final layer: normalize each digit's template and compare features against it, so the scale of the features doesn't matter for the ranking. I'm also weighing whether to subtract a shared average or penalize ink where a template has none, and I'll decide that once I see how the centroids separate.

I'm checking whether a cosine-style score against each digit's normalized template works as nearest-centroid, since that keeps the ranking independent of feature scale. I'm also wondering whether several stroke variants per digit could be drawn and averaged into one template, but a single row per class in the linear layer makes that unclear.

I'm settling on a template for each digit made of hand-drawn weighted strokes, rendered straight into the weight grid, and I'm treating the blur as a fixed formula rather than something to tune.

I'm defining the four zero-sum bar filters for horizontal, 45°, vertical, and 135° orientations, with a small negative bias to suppress noise. Next I'm checking how a 3-pixel-wide horizontal stroke drives the horizontal filter, working through its row weights and their mean.

I'm checking how a horizontal stroke's response carries over to the diagonal filters, which should be partial and roughly around 1. I'm also considering whether to subtract the orthogonal orientation in conv2 to sharpen tuning, but I'll leave that out for now.

I'm estimating how a horizontal stroke drives the diagonal filter by summing the weights over the 5x5 window, which comes out to a mean of about 0.56.

I'm checking that a 45° tuning comes out near 0.3, which is close to cos^4 of the angle difference, so I'll use cos^4 as the orientation response. Next I'm deciding what the other four conv1 channels should cover, whether more orientations in finer steps or something else.

For the other four conv1 channels, I'm considering a plain ink-blur channel that just reports where ink is present. That could feed a hole detector in conv2: a center tap that reads negative on ink, surrounded by positive taps at about 4 pixels, which would respond to the enclosed loops of 0, 6, 8, and 9. The loop sizes I'd expect are roughly 6 to 10 pixels for a 0 and 4 to 6 for the loops of 8, 6, and 9.

I'm weighing a hole detector in conv2 that subtracts the center ink from a ring of ink around it, though a linear sum can't really enforce "ink on all sides," so it would only fire with a high threshold. Open shapes like 3, 5, and 2 might partly trigger it too, which makes its FC weights hard to guess. Since I only get a confusion matrix back each round and have about 15 rounds, I want to keep the number of guessed parameters small and rely on a robust orientation-energy base.

I'm weighing which conv1 channels to add beyond the four bar orientations, and polarity edges look redundant since both sides of a stroke already show up in the bar responses. Holes seem more useful: a top loop helps separate 8, 9 and 0, a bottom loop helps 6 and 8, and a large central hole points to 0. So I'm leaning toward reserving the remaining conv1 channels for ink blur and hole-related signals.

I'm weighing whether channels 5 through 7 should stay spare, and I'm looking at a hole detector in conv2 that works on the max-pooled ink map at 2px pitch. The inner loops of 8, 6, and 9 are only around 4 to 6 pixels, so after pooling they shrink to one to three taps, which makes that detector fragile.

I'm weighing whether a center-negative, surround-positive filter in conv1 could detect the concavity of a hole directly, rather than relying on pooled ink maps where the small inner loops may disappear.

I'm considering a loop detector in conv2 built from orientation channels: horizontal responses along the top and bottom of the 5x5 window, vertical ones down the left and right sides, and a negative center to keep the hole open. Requiring most of the four sides to fire should let it separate 8, 6, and 9 from open shapes, and max pooling should give some tolerance to small shifts.

I'm thinking about whether a conv2 loop detector built from orientation channels is worth it, or whether spare channels should go to finer position and orientation coverage. I'm leaning toward the coverage, since I can't debug the detectors well. Now I'm working through how the pooled cells line up with the conv1 centers, starting with where a single tap's sensitivity range falls.

I'm laying out the offset grids for the conv1 channels: shifting the taps by one step changes each cell's coverage by two pixels, so the 16-pixel windows can tile the digit box at half-cell spacing. I'm considering combining the row and column offsets for each orientation to cover the typical digit region.

I'm weighing whether to spread the extra conv1 channels across two offset grids for each orientation, which would cover the 4px cells with some redundancy, or to accept a plain 5x5 grid with duplicated center cells as the simpler option.

I'm checking whether the offset grid's coverage reaches the stroke centers, which sit around rows and columns 5 to 22 for a digit spanning 4 to 23. With the taps shifted by 2, a stroke centered one pixel outside the cell should still give a partial response from the bar filter.

I'm checking the corners of the offset grids: the two diagonal grids cover rows and columns 4 to 23 between them, but the top-right corner around rows 4 to 7 and columns 20 to 23 is left uncovered.

I'm weighing whether to pair two offset grids for better coverage, or to sum taps across one dimension so the cells overlap and blend, which should make template matching smoother. Working through the pooling indices for taps 1 through 3 to see where each output lands.

I'm settling on a soft-binned layout: four orientation channels with a 3x3 [1,2,1] tap window, giving smooth 4x4 cells over the whole digit, much like a SIFT-style descriptor. That leaves twelve conv2 channels for sharper, single-tap grids at finer local positions.

I'm settling on a layout with soft SIFT-style cells for the first four conv2 channels, then weighing whether the next group should be sharp single-tap grids at fixed offsets. I'm doubtful those sharper grids help, since my hand-built templates probably won't line up to within two pixels, so I'm considering whether the remaining channels should go to end-of-stroke detectors or discriminators tuned from the confusion matrix.

I'm noticing the discriminative idea I was reaching for doesn't work as written: subtracting the same vector from every class leaves the argmax unchanged, so the penalty has to be specific to each class. I'm thinking the negative weights should only push down energy where a given template expects none.

I'm refining the penalty term for the discriminative weights: rather than subtracting a shared vector, I'd penalize each class only where its blurred template is near zero, which matters for confusable pairs like 1/7, 4/9, and 3/8.

I'm weighing cosine similarity against a Euclidean-style score, since cosine handles subset relations like 1 versus 7 partly on its own. A class-specific penalty should help more with those, so I'm leaning toward a moderate weight on it. Next I'm turning to the conv2 bias and the logit scale, which I'll set by normalizing the conv1 filters against an aligned stroke response.

I'm estimating the scale of the feature vector, figuring the strokes and soft cell values land somewhere around 2 to 3 in norm across the 64 dimensions. Since cosine similarity ignores overall scale, the logit becomes the feature norm times the cosine times a gain, and I'm thinking about how the class-to-class cosine differences will come out.

I'm settling the logit gain at around 4 so the class differences land near 2, and I'll tune it later from trial runs. Next I'm working out an analytic renderer that deposits each stroke sample into the pooled cells, starting with how a stroke center maps onto the triangular tap weights of the conv1 centers.

I'm working out where the pooled cell centers land in input coordinates: stroke-window centers at about 7.5, 11.5, 15.5, and 19.5, with a roughly triangular weight that is full within about 1.5 pixels and falls to zero at about 6.

I'm settling on a Gaussian-like window for each cell, roughly full weight within a couple of pixels of its center and tapering to zero by about six. I'm now checking how a horizontal stroke fills the x taps of a cell, so its contribution saturates across the whole width.

I'm weighing whether to keep the first layer to four soft orientation channels, or to add a finer orientation set at 22.5° steps, though a 5x5 filter may not resolve those angles cleanly.

I'm thinking about adding endpoint detectors as four extra conv1 channels, since where a stroke ends separates digits like 3, 5, 2, 6, 9, and 7 well. I'm working through which ends each digit has, and where they sit, to see whether those positions help tell the confusable pairs apart.

I'm designing an endpoint detector for the first layer: a 5x5 filter that responds to a stroke ending at its center, with positive weight on the center column below and negative weight above and laterally, so that continuing vertical or horizontal strokes give a non-positive response.

I'm checking the endpoint filter against a corner: a convex corner like the top of a 7 would partly trigger it, which is noisy but probably still fine since real stroke ends also fire it. I'm also wondering whether the top of a 0's curve, a horizontal run at the center row, would light up the same way.

I'm sketching out an endpoint detector design for the first layer, with four directional filters (up, down, left, right) that respond where a stroke terminates.

I'm sketching the endpoint filter's lateral profile and vertical weights, checking that a continuing stroke gives a non-positive total while a true end at the center row comes out clearly positive.

I'm checking a diagonal stroke ending at the center and sliding down-left, where the ink fills the lower-left corner of the filter, to see how the end detector responds to it.

I'm checking the endpoint filter's vertical weights against a horizontal bar at the top of the cell, the corner shape of a 7, and seeing how much positive response it still produces.

I'm checking how the end detector fires on corners: the top-right of a 7 and the top-left of a 5 both trigger it, so corners count as convexity detectors. I'm thinking about placing the expected endpoint features by hand for each digit.

I'm checking how rounded curves fire the end detector: at the apex of a wide arc the response is zero, but for a tighter loop the lower rows pull it negative, so curves mostly stay quiet.

I'm normalizing the endpoint filters so a real stroke end produces a response near one, and I'm working out a soft-cell weight for a single point feature.

I'm now checking the endpoint detector's response magnitude against a stroke, since an endpoint only lights up a single pooled tap while a line fills several, so I'll boost the endpoint channels' conv2 gains to compensate.

Now I'm settling the endpoint filter's scale: a single end deposits about half as much as a line, so I'll double the conv2 gains on the end channels to bring them level, with each end counting as roughly one unit in the template.

I'm considering whether the remaining eight second-layer channels should stay empty for now or carry a loop detector, using horizontal and vertical bar responses around a center to pick up the holes in 6, 8, and 9.

I'm now looking at a loop detector for the remaining eight second-layer channels, built from horizontal bars above and below the center and vertical bars to either side, to pick up the holes in 6, 8, and 9. I'm estimating the total response for a small loop against a "3", where one side is missing and the score drops.

I'm weighing whether to skip the loop detector and the finer sharp-grid channels for now, since they'd add complexity without a clear win. I'm leaning toward keeping the design simple with the eight soft channels and revisiting the remaining ones later if the template fit needs help.

I'm setting the endpoint and corner detectors aside for now and leaving the remaining conv2 channels at zero, since finer offset grids wouldn't clearly help. Next I'll place the digit templates in the 28x28 frame, centered by center of mass at (14,14), with the vertical strokes spanning roughly rows 4 to 23.

I'm now placing the digit strokes using their centroid: I'll scale each drawing so its larger dimension fits about 17 pixels, then shift it so the center of mass lands at (13.5, 13.5). I'm drawing the digits in unit coordinates, with curves approximated by sampled arcs as polylines.

I'm now sketching the digit templates as polylines in unit coordinates, starting with the 0 as a full ellipse and the 1 as a near-vertical line with a slight slant. I'm moving on to the 2, beginning its top arc from the upper left.

I'm now settling how to draw the 2: an arc for the top hook, then a diagonal down to the bottom-left, then a horizontal base. The stroke ends get their outward directions taken from the start and finish tangents, and I'm about to work out the corner at the bottom left.

I'm now listing the digit "3" as two stacked arcs, with the top one centered near (0.45, 0.27) and the lower one near (0.45, 0.75), and I'm reasoning through how the arc angles meet at the middle.

I'm mapping out the digit "4" as three strokes: a left diagonal, a horizontal crossbar, and a right vertical, with the ends marked for the endpoint detector.

I'm placing the digit 4 as a left diagonal, a crossbar, and a right vertical, then sketching the digit 5 as a top bar, a short vertical drop, and a belly arc that starts from the upper left.

I'm now checking the 6's path: a stroke coming down from the top right and curving through the left side of a loop near the bottom.

I'm now listing the 8's strokes as two loops, a top one and a bottom one, with the 8 drawn as an S-shaped figure that crosses through the middle.

I'm placing the 8 as a figure-eight curve that crosses at the center, with no endpoints. For the 9 I'm drawing a full loop at the top and a stem running down from its right side.

I'm finishing the digit 9's path, a full loop followed by a stem down to the bottom, with only the stem's end counting as an endpoint. Then I'm scaling every digit so its larger dimension fits about 17 pixels, allowing for stroke width, and checking that the 1 still comes out at the right height. I'm also noting that the 2, 3, and 5 come out a bit narrower than tall, which is fine, and that a little spatial blur in the template should absorb any remaining jitter.

Now I'm defining the cell centers at 7.5, 11.5, 15.5, and 19.5, symmetric about the image center, and a triangular window that falls off with distance from each cell. For each stroke sample I'm adding its length-weighted orientation response into the pooled grid, using a fourth-power cosine to match the four orientation bins.

I'm defining the bar filters by their direction in the y-down frame, with the perpendicular offset computed from each pixel's position, and I'm weighting them against the mean so they respond to strokes of the matching angle.

I'm settling the bar filter normalization, dividing by 3.6 so aligned strokes respond around one, and adding a small negative bias to cut tiny off-orientation responses. Next I'm building the end-point filters: E_up first, then deriving the others by rotating and flipping it.

I'm checking the end-direction vectors for the up, down, left, and right filters, and I want to confirm that a horizontal stroke won't trigger the upward-facing end filter. Then I'm considering whether E_up might still fire along the top edge of a slightly tilted horizontal stroke or a wide diagonal.

I'm checking the diagonal "/" stroke against the end-point filter and finding that its response goes negative in the upper rows, so it stays quiet. I'm also setting up the second convolution layer, where each channel takes its matching first-layer channel with a small blurring kernel, and working out how the flattened index maps onto the final fully connected weights.

I'm checking how strongly a horizontal stroke through a cell center drives the pooled grid, comparing the real first-layer response along the line with the response at the neighboring rows. I'm estimating how that weakens after pooling and the vertical smoothing in the second layer, to see whether the template magnitudes stay in proportion with the end detectors.

I'm checking how a stroke sitting between two cell centers, at y≈13.5, falls into the pooling taps, and finding that the real response for the nearest cell comes out around 0.6 instead of the full template weight.

I'm working out the real pooled response for a stroke near a cell center: it comes to full strength within about 1.5 pixels of the center, roughly half at 2.5 to 3.5 pixels away, and close to nothing beyond that.

I'm refining the window that maps stroke distance to cell response, narrowing it so it sits near 1 within about 2 pixels and falls to roughly 0.3 by 4 pixels. I'm also estimating how strongly an endpoint response reaches the neighboring pooling taps.

I'm now working out how the fully connected weights should be built from the flattened template vectors, scaled by the gain and a penalty term for each digit.

I'm normalizing the template vector and penalizing weights where the template falls below a small threshold, keeping the penalty mild since real images carry some energy outside the template. I'm also checking that the penalty stays scale-invariant, and estimating the active feature norm to see how the gain sets the logits.

Writing digit stroke definitions with arcs and endpoints...

Still writing digit stroke definitions...

Still writing digit stroke definitions...

Still writing digit stroke definitions...

Still writing digit stroke definitions...

Still writing the digit stroke definitions and scaling them to fit the grid...

Still writing the weight-building code and the stroke sampling for the template renderer...

Still writing the FC weight code, setting each digit's template weights with a gain and a mild penalty on off-template channels.
