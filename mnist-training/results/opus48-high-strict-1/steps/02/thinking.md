The first run landed at 20.8% accuracy, with predictions piling up on 0, 3, 5, and occasionally 9, so the template matching looks badly skewed. Classes 1, 2, 4, 6, 7, and 8 never came out as predictions at all. The loss of 3.82 is worse than a uniform guess, which points to confident wrong answers, and I think the ink maps are too alike to separate the digits.

Reworking the template approach, the problem looks like it's in the features rather than the scale. With all 16 channels identical there are really just 16 distinct values per image, and the coarse ink averages look too alike across digits for dot-product matching to separate them. I'm also considering whether lowering the scale would curb the overconfidence without fixing the bias toward a few classes.

Switching the first layer to oriented edge detectors so each digit yields a distinct feature map instead of near-identical ink blobs.

I'm sketching a 5x5 horizontal bar detector, with the middle row weighted positive and the surrounding rows negative, so it responds to horizontal strokes.

I'm defining the edge filters now: a horizontal bar detector with a positive middle band and negative bands around it, plus vertical and both diagonal variants, so each responds to strokes at its own orientation. With ReLU on top, each channel should only fire where strokes of that direction are present.

I'm weighing whether to give the conv2 channels a simple pass-through of each orientation map, so the 16 channels carry 8 distinct orientation densities over the 4x4 grid. That would give richer features, but hand-designing fully connected templates on top of them looks laborious, so I'm also considering keeping the ink density and adding the edge signals alongside it.

I'm now wondering whether I can get finer spatial detail into the fully connected layer. The 4x4 ink map is too coarse, so I'm considering having different conv2 channels respond to ink at slightly shifted positions, which might recover some sub-cell resolution.

I'm considering whether conv2 could use a spot-like filter per channel, so each output channel samples a specific position on the 12x12 ink map. That would keep much more spatial detail than the 4x4 pooled grid and could let the fully connected layer tell digits apart.

I'm noting that max-pooling over each 2x2 block would blend the four sampled positions together, which could blur the finer detail I'm trying to recover.

I'm checking whether a delta filter in conv2 could sample a specific position, so each pooled cell would take the max over four neighboring input positions rather than a true sub-cell value. The max-pool would still blend those four positions together.

I'm weighing whether a delta filter in conv2 can pull out finer spatial detail, but max-pooling over each 2x2 block would still blend the four sampled positions together, so the approach looks fragile.

I'm going to keep the approach but move to oriented edge detectors for the first layer, aiming for a plan that gives each digit a distinct feature pattern instead of near-identical ink blobs.

I'm planning the first conv layer as a set of distinct detectors: plain ink density, vertical, horizontal, and the two diagonals, with the last few channels left open. The second layer would then pass each of these through to 16 output channels, duplicating a few since there are fewer useful inputs than outputs.

I'm listing eight first-layer filters: plain ink density, vertical, horizontal, both diagonals, and a few more meant to pick up edges and regional ink. Then I'm planning the second layer to pass each of those eight maps through twice, so the fully connected layer gets sixteen channels to work with.

Rather than hand-tuning 128 numbers per digit, I'm leaning toward keeping just the ink density from the first layer and improving the 4x4 templates with proper normalization and bias correction. The 4x4 ink ceiling is probably around 40%, but that's a safer step to take while I keep thinking about richer features.

I'm thinking about whether conv2 could use channels to recover finer position detail on the ink map, so the final layer sees more than the coarse 4x4 grid.

I'm working out whether delta-style conv2 filters could shift which ink positions each channel reads, so the pooled grid captures finer sub-cell detail.

I'm working out how the 2x2 pooling blends each sampled offset, and whether 16 offset channels over a 4x4 range would recover sub-cell detail the single 4x4 grid misses.

I'm thinking about recovering finer spatial detail by having the second conv layer sample different offsets of the 12x12 ink map, so the fully connected layer gets something close to full-resolution ink. Template matching on that could plausibly reach 60-70%, though hand-drawing 12x12 digit templates is laborious but feasible.

The max-pooling over each 2x2 block is the catch: each sampled value is really the max of a small neighborhood, so the offset channels give blurred sub-cell detail rather than exact positions. I still need to check how well the ~0..10 coverage holds up.

I'm considering delta filters at four offsets in conv2, so each pooled cell takes a max over a shifted 2x2 block of the ink map. Together those samples would cover most of the 12x12 map more densely than the single 4x4 grid, though the max-pooling still blurs each sample.

I'm checking whether a delta filter at a fixed offset in conv2 can cover the central 8x8 of the ink map without the max-pooling blur, and whether the valid-convolution index ranges actually line up.

I'm settling on sixteen offset channels in a 4x4 grid of shifts, so each channel samples a different spot on the ink map and the fully connected layer gets a denser view.

I'm working out how each conv2 offset channel reads a shifted 2x2 block of the 12x12 ink map, so I can map each channel's pooled cells to approximate positions. I plan to set the fully connected weights for each digit from a hand-drawn high-resolution template, sampled at the location each channel and cell reads.

I'm setting each fully connected weight to the template value at the inkpool position that a given conv2 channel and pooled cell read, which turns the matching into a weighted sum over sampled positions. The offsets are meant to cover rows and columns 0 through 9 of the 12x12 map, and I'm about to pick the full set of 16 offsets.

I'm sampling inkpool rows and columns 0 through 9 with offsets 0 to 3, which gives 16 combinations that cover most of the map with some overlap. The next step is drawing the 10x10 digit templates by hand.

I'm settling on hand-drawn 12x12 digit templates, since describing strokes directly is allowed and avoids any regression or averaging to set the weights.

I'm mapping where each digit's strokes fall on the inkpool grid, placing the 20x20 box at roughly rows 1 through 10, so the 12x12 templates should span that range.

I'm switching the offsets to a and b in {1,2,3,4} so the sampled rows and columns run from 1 through 10 and cover the digit's lower part, which the earlier 0-to-3 choice missed.

Still drawing the 12x12 digit templates...

Still drawing the digit templates...

Still drawing the digit templates...

Still drawing the digit templates...

Still drawing the digit templates...

I'm estimating the scale of each template term: features around 0.3 times centered template values around 0.3 give small products, but with a couple hundred terms the sum could grow large, so I'll pick a modest scale and tune it from feedback.

I'm settling on a scale of about 2 for the logits, and I'll adjust it from the loss feedback rather than trying to predict the magnitudes exactly. The conv2 delta channel for the inkpool input is set up so it reads only the ink-density channel, with the other input channels zeroed out.

I'm confirming the conv2 output size: an 8x12x12 input with a 5x5 filter gives 8x8, and a delta filter at (a, b) just reads inkpool[i+a, j+b], so the offsets stay in range. Pooling 2x2 down to 4x4 is what comes next.

Still working out the offset list for the 16 conv2 channels, mapping each one to a sampled position on the ink map.

I'm settling the offset mapping: each conv2 channel k reads inkpool at row 2R+1+k//4 and column 2C+1+k%4, which keeps every sampled index within 1 through 10 of the 12x12 map. Next I'll set the fully connected weights and try a scale of 4, adjusting if the loss looks off.

I'm settling on a logit scale of 3 to start and will tune it from the loss. The reasoning is that each inkpool position gets read by many channel and cell combinations, so the summed contributions could grow large, and I want the logit differences to stay moderate.

I'm checking the duplication count: a given inkpool position gets read by about four row-and-column combinations, so each position's contribution is multiplied roughly fourfold before the template weighting.

Still writing the weight-setup code...

Still writing the weight-setup code...

Still laying out the 12-by-12 digit templates, row by row, and checking that each row comes to exactly twelve characters.

Still laying out the 12-by-12 digit templates, row by row.

Still drawing the digit templates...

Still drawing the digit templates...

Still drawing the digit templates...

Still drawing the digit templates...

Still drawing the digit templates...

Still drawing the digit templates...
