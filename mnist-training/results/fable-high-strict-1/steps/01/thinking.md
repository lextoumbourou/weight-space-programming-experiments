I'm planning the weights by hand for a small MNIST CNN, with conv1 having 8 filters and conv2 having 16. The idea is to have conv1 pick out oriented strokes like horizontal and vertical edges.

I'm weighing a simpler route first: a single ink-detecting channel in conv1 with conv2 averaging over it, which would give a coarse 4x4 map for a template-matching classifier. It should be a workable starting point, though not strong, so I'm also considering oriented edge features as the better option.

I'm working out where each final 4x4 cell's receptive field lands in the input when conv2 uses only its center tap, which gives input rows 4-11 for the first cell, then 8-15 and 12-, with the overlap shrinking.

I'm checking how the 4x4 cells line up with the digit box: with a center-tap conv2, the grid covers rows and columns 4 through 23, so each final cell is a max over a 2x2 block of conv2 outputs, which spans a region of the input.

I'm settling on a plan where conv1 holds eight oriented edge detectors and conv2 mostly passes those features through, with a few channels mixing them or using a wider spatial weighting. The rest of the design is the fc layer acting as hand-set templates over the 4x4 grid.

I'm weighing whether to write out 1280 template values by hand, one per digit, orientation and grid cell. The task allows describing digits as strokes and deriving templates from those, so I'm considering that route, though I'm checking whether it crosses into computing weights from example inputs.

I'm now listing the eight conv1 channels: an ink blob detector, horizontal and vertical strokes, two diagonals, and a fifth channel that responds to empty background, which could help pick out holes in digits like 0, 6, 8 and 9.

I'm considering the hole detector as the fifth channel, since it would fire inside the loops of 0, 6, 8 and 9. I'm also thinking about a horizontal line detector, with a positive center row and negative rows above and below, to be checked against stroke width.

I'm sizing the horizontal line detector so a vertical stroke doesn't also trigger it: positives on the middle three rows, negatives on the rows above and below, with the weight chosen so a crossing vertical stroke cancels out.

I'm sizing the horizontal detector so a crossing vertical or diagonal stroke cancels out, with the middle rows positive and the rows above and below negative. Then a bias around -6 should leave only strong horizontal responses, though the real ink values and stroke widths will need rescaling later.

Working through the diagonal detector now: I'm checking how a "\" stroke sits in a 5x5 window, with the cells near the main diagonal positive and the corners negative. I'm also testing whether a horizontal stroke gives a clean response there.

I'm checking the horizontal detector's negative weight against a vertical stroke, which gives about 9 positive and 6 negative hits, so a weight of 1.5 cancels it out. The diagonal detectors work the same way: the "\" stroke matches the main diagonal band, while the "/" stroke only gets about 5 positive hits against 12 negative, so it comes out strongly negative. I'm now deciding on a common output scale so the eight channels stay in a comparable range.

I'm setting the horizontal detector's weights: positives at 1/15 so an aligned line gives about 1, and negatives at 2/15 so a crossing vertical or diagonal stroke cancels out. The diagonal detector works out to zero response on a horizontal line with these weights.

I'm settling on the hole detector as a background-based channel: a bias of 1 with each of the 25 weights at -1/5, so a completely empty 5x5 window scores 1 and any window with five or more full ink pixels drops to zero. I'm still unsure whether max pooling over the 8x8 window will keep that signal useful, since nearly every window contains some empty region.

I'm wondering whether the emptiness detector is worth keeping, since a max over 8x8 windows would rarely reach zero. I'm considering instead averaging the conv1 channels in conv2 rather than taking the max, and thinking through how a pass-through with a 3x3 center average would behave before the max pooling.

I'm considering using extra conv2 channels to keep top-half and bottom-half spatial weightings of each orientation feature for finer position detail, though I'm leaning toward a simpler set of pass-through channels first and refining after checking the errors.

I'm settling the conv2 spatial taps now: with 3x3 center taps each final cell covers a slightly overlapping region, and I'm weighing whether a 5x5 Gaussian-like weighting would be more robust.

Now I'm working out the fc templates: a digit becomes a pattern of strokes across the 4x4 grid, with 0 as an oval whose top corners curve in opposite diagonals.

I'm moving on to the digit templates in the 4x4 grid, describing each digit's strokes cell by cell. For 2 I'm placing a top horizontal, a curve down the right side, a diagonal back to the lower left, and a bottom bar, and now I'm starting on 3.

I'm sketching the digit templates for 4 and 5 on the 4x4 grid: 4 gets a left vertical in the top half, a horizontal bar across row 2, and a right vertical running the full height, while 5 gets a top bar, a short left stroke, a middle bar, a right stroke in the lower half, and a bottom bar. Now I'm starting on 6, beginning with a "/" stroke at the top.

I'm working out the digit 9 template next, starting from the top of the 4x4 grid.

I'm now laying out the digit templates as stroke lists in 4x4 cell coordinates, each stroke tagged with its orientation, and I'm building the lookup from those lists instead of writing out grids per feature.

I'm weighing whether the fc weights should be centred by subtracting the average template across digits, since that's a formula over my own hand-written templates rather than over any generated data. I'm leaning toward it, though I still want to check that it doesn't blur the distinctions between similar digits like 3, 5 and 8.

I'm weighing whether to center the fc weights by subtracting the average template, treating it as arithmetic on my hand-drawn templates rather than on any generated data. I'm also keeping the logit scale moderate so the differences between digits stay within a few units.

Still writing the conv1 filter definitions...

Still working out the empty-region detector for conv1: since a 5x5 window of empty pixels only fits inside an 8x8 window when the stroke sits near one edge, I'm wondering whether it will fire often enough to be useful at the pooled level.

I'm weighing an emptiness detector over only the center 3x3 of conv1, with a soft pooled signal, and wondering which digits should mark empty cells in their templates.

I'm now weighing which additional channels to add beyond the emptiness detector, since some digit pairs like 4 and 9 are hard to tell apart with orientation features alone. I'm considering stroke endpoints or coarser-scale ink as candidates for the last two conv1 channels.

I'm checking which features separate the confusable pairs like 3 and 5, or 4 and 9, and I'm considering whether finer-angle diagonals at roughly 22.5° steps would help with digits that slant around 70°.

I'm weighing a stroke-end detector for conv1 channels 6 and 7, which would fire at the ends of horizontal-ish strokes, but it may be too subtle to add in a first pass. A coarser blob detector would mostly duplicate the ink channel, so I'm leaning away from it and still considering what to put in those last two slots.

I'm making channel 6 a steep diagonal detector, tilted from bottom-left toward top-right at around 67 degrees, and checking which cells in each row should carry its weights.

I'm settling channel 6 as a steep diagonal detector and leaning toward a broad 5x5 ink average for channel 7, and I'm keeping the emptiness detector as channel 5.

I'm sketching conv2 as two groups of eight channels: the first copies each conv1 feature with a tight 3x3 average, and the second uses a wider 5x5 average to get a coarser view of the same features.

I'm settling the conv2 channels: rather than offsetting the taps vertically for finer position, I'm leaning toward channels that combine horizontal and vertical features at the same spot, to catch corners and crossings, and I'm still checking whether a shifted receptive field would help place strokes more precisely on the 4x4 grid.

Now I'm looking at the channels 8 through 15 for conv2, with the idea of using broader 5x5 averages for those so the fc layer gets some coarser context alongside the local features.

I'm working out which conv2 taps would shift the receptive field: taps in rows 1 through 3 land the window at offsets of 4 to 12 input pixels, so the final grid can sample stroke positions at a finer vertical spacing than the default alignment allows.

I'm settling the last conv2 channels: since the taps in rows 1 through 3 already cover the digit box well, I'm going to keep channels 8 through 15 simple, as 5x5 uniform averages over the same features, and set the fc template weights across both sets.

I'm settling the fc templates next, writing out the per-digit feature patterns over the 4x4 grid for ink, the horizontal and vertical edges, both diagonals, the empty-region detector, and the steep diagonal, with the conv2 taps covering roughly rows 2 through 13 of the input.

Still laying out the 4x4 ink templates by hand, starting with the digit 0 as a wide ring shape.

Still writing out the 4x4 ink templates, now working through digits 1 and 2 as vertical bars and a top arc with a diagonal.

I'm sketching the 4x4 ink templates for each digit, and the dense strokes at this grid size mean the ink map alone won't separate the classes, so the orientation channels will have to carry most of the discrimination.

Still writing the orientation templates for digit 0, with horizontal and vertical edge patterns across the 4x4 grid. The diagonal templates follow the same layout, and the ink map is simply the union of the four orientations, so I'm not hand-writing it separately.

Still writing out the digit 2 templates on the 4x4 grid, filling in the horizontal, vertical, and diagonal patterns row by row.

Still writing the digit 3 templates, laying out horizontal and vertical stroke patterns across the 4x4 grid.

Still writing the digit 3 templates, now working on the bottom-left curl of the stroke pattern for the S channel.

Still writing the digit 4 templates, working out how the left arm and the right stem should sit across the 4x4 grid.

Still writing the digit 4 templates, now filling in the vertical stem and left arm patterns across the 4x4 grid.

Still working out the digit 4 and 5 templates on the 4x4 grid, sorting out which cells the crossbar and lower loop should occupy.

Still working out the digit 5 and 6 templates on the 4x4 grid, sorting out the bottom-left curl and the lower-right cells.

Still working out the digit 6 templates on the 4x4 grid, placing the lower loop's top and sides across rows 1 through 3.

Still working out the digit 6 and 7 templates on the 4x4 grid, placing the steep diagonal and the top bar.

Still writing the digit 8 templates, laying out the H and V patterns on the 4x4 grid and working out the crossing cells at the center.

Still writing the digit 9 templates, placing the stroke patterns for the bowl and the tail across the 4x4 grid.

Still working out the fc template weights for each digit, centering them against the per-digit mean and deciding how much to down-weight the duplicate channels.

Still working out the fc weights: the ink channel takes the union of the four orientation templates, and I'm penalising ink in cells where no template expects it. After centering across digits, I'm picking a scale of about 3, since typical feature values near 0.4 across roughly ten cells should give logit gaps of a few units.

Still setting the bias, and I'm inclined to start it at zero and adjust once the confusion matrix comes back. I'm also wondering whether the orientation thresholds need a small negative offset, since MNIST ink is mostly full intensity with soft edges.

Checking the stroke response numbers: a 2-pixel horizontal stroke gives about 0.42 after the bias, a 3-pixel one about 0.75, and a thick 4-pixel one only about 0.08. Max pooling should recover some of that loss. Next is the steep "/" filter for channel 6.

Still working out the steep diagonal filter's active cells row by row, settling on a ±1 band around the drifting center so each row lists its positive positions.

Still working out the steep diagonal filter, and the empty-region detector: a 3x3 center with weights of -1/3 should stay at zero whenever three or more full pixels are inked.

Still setting up the conv2 weights and the fc template scheme: the eight channels get 3x3 averages over their matching conv1 channel, the other eight get 5x5 uniform averages, and I'm weighting the duplicates at half strength.

Still writing the templates for each digit as code, mapping the channels and their values.

Still writing the digit 2 templates, filling in the horizontal, vertical, and diagonal patterns on the 4x4 grid.

Still writing the digit 3 and 4 templates as grid strings, now on the vertical and bottom-curl patterns for the 4s.

Still writing the digit 5 and 6 templates as grid strings, now on the horizontal and vertical patterns.

Still writing the digit 9 templates on the 4x4 grid, now filling in the horizontal and bowl patterns.

Still writing the digit 9 templates, now working on the horizontal bowl and the lower-left cells.

Still writing the conv1 filter weights in code, setting up the ink channel and the horizontal and vertical edge detectors.

Still writing the conv1 filter weights in code, now setting the slash and backslash diagonal detectors plus the empty-region detector.
