The template method is stalling around 66%, so I'm going to need a better feature and classifier design. My suspicion is that the feature extraction is the weak point: the Mexican-hat convolution for orientation responds noisily to MNIST strokes, which are only about 2–4 pixels wide and sometimes thicker. I'm also wondering about the effect of max-pooling over 4

I'm wondering whether max-pooling over 4x4 blocks blurs the stroke information too much, since strokes land in many cells and the pooled map may not match how my rendered templates look. One option I'm considering is finer features at several sub-offsets, which would give a closer ink map and lean on hand-described mean images. I also realize a near-linear conv path with non-negative weights and zero bias would behave roughly like smoothed downsampling, so a linear classifier on those features could work, though setting its weights by hand is the hard part.

I'm thinking the real bottleneck is template quality, and that better features built around invariant structure, like whether a digit encloses a hole, might make hand-specified rules more reliable than tuning raw mean images. Holes could be detected by checking for ink on all sides of a background pixel, which a second conv layer with a larger receptive field could approximate.

I'm working out how a hole detector could be built from the pooled ink channel: a background pixel with ink above, below, left, and right, sampled at a couple of offsets so it catches loops of different widths. Max-pooling should make that fairly tolerant of stroke thickness.

Now I'm sketching the second conv layer's channels: keeping the orientation and ink pass-throughs, and adding a hole detector that reads the pooled ink map at a couple of offsets with a negative weight at the center.

I'm sizing the hole detector's bias and weights: ink values near 0.6–0.8 mean four directions summing to about 2.8, so a bias near -2.2 would leave a response around 0.6. I'm also considering several samples per direction and a few small offsets to catch tighter loops.

I'm mapping which digits would show a hole in each of the four quadrants, and noting that small holes might be filled in, so I'm also considering a finer detector with tighter offsets to catch tiny loops.

I'm now considering topological features that describe which direction a background region opens: a concavity with ink above, below, and to the right but not the left would signal an opening to the left, which could help separate 3s and 5s, and similar patterns could flag 4s and 9s as open at the top.

I'm thinking about open-bottom concavities as well: a background region with ink to the left, right, and above but none below, which might mark a 7 or the top arc of a 2. For classes like 3, I'd want to know where these openings fall on the grid, and I'm considering rasterizing my stroke drawings to measure them geometrically rather than guessing the weights by hand.

I'm weighing whether ray casting over my rasterized digit drawings would count as computing weights from generated inputs, which the rules forbid. It doesn't run the network, but it's close enough to the line that I'd rather avoid it, so I'll hand-specify the hole and concavity cells for each digit in a table.

I'm laying out the hole detector's sampling grid over the 4x4 cells, mapping input rows 6–21 and cols 6–21 so the digit body falls in the central columns. For a zero, the interior is only about 11 pixels wide, so I'm checking whether ink at roughly four pixels in each direction still lands on the loop stroke after the blur and pooling.

I'm checking whether the vertical reach of the hole detector is enough for a tall zero, since the top and bottom ink sit about 8 pixels from the center and the detector's taps may only reach about 6 or 7.

I'm checking whether a symmetric up-and-down hole test can work for a tall zero, since the top and bottom ink sit too far from the center to be reached. A simpler left-and-right test with no center ink might catch the interior of 0s, 6s, 8s, and 9s instead.

I'm wondering whether the concavity idea can work at all, since a symmetric up-and-down test can't reach the interior of a tall zero. Checking only left and right ink with no center ink might do better, and I'm considering that plus up-and-down as the two halves of a hole test. I'm also reconsidering whether the cell-level coverage from max pooling is saturating the ink channel too much to separate digits.

I'm checking how far the coverage interval actually reaches, since the falloff seems to make the cells respond to strokes farther out than the convolution really does. That would make the templates a bit too blurry, though that may not be all bad.

I'm now testing whether a left-and-right ink pattern with no ink at the center could pick out the interior of a loop, since that might be more invariant than the hole detector I was tuning. I'm planning to specify the weights for the left and right taps on the pooled ink map first.

Now I'm checking whether pooling dilates the ink map enough that a center cell only two pixels from a stroke still reads as ink, which would break the hole detector for small loops.

I'm noticing that a hole detector built on the ink channel loses small loops after pooling dilates the strokes. So I'm considering a background channel from conv1, a thresholded response that's positive only in dark regions, which max-pooling would keep alive inside even tiny holes. Combining that background signal in conv2 with ink on the left and right might recover the interiors that the ink-only version misses.

I'm setting up a between-strokes detector on the second convolution: a background signal at the center, with ink required on both the left and right sides. The thresholds are tricky, since a single thick stroke could satisfy one side alone, so the bias has to demand both.

I'm trying to get a "between" detector without a true min operation, since the ink channel can't be clipped and a single thick stroke on one side could pass the threshold. I'm considering a bias that demands both sides, and I'm wondering whether a background channel from conv1 would hold up better for tiny holes than the ink channel does.

I'm now weighing a "between" detector for holes: a background signal at the center with ink required on both sides. The trouble is that without a true min, one thick stroke on a single side could pass the threshold, so I'm looking at a bias that demands both.

I'm now sorting out the two "between" detectors: one checking for ink on both the left and right of a background point, which would show up inside 0s, 8s, and the loops of 4, 6, and 9, and one checking for ink above and below, which covers 0s, 8s, the loops in 6 and 9, and the openings in 3, 5, and 2. A 7 wouldn't trigger the vertical one below its bar, since nothing sits underneath.

Now I'm defining a background channel in the first convolution, a dark-region detector that stays positive only in empty space, so that max-pooling keeps it alive inside even tiny holes.

I'm working out the "between" detector for the horizontal case: a background cell at the center, with ink on both the left and right taps. Each side's ink sum typically lands around 0.7, sometimes more, so I'm checking how the weights should combine so that both sides are required.

I'm checking the weights for the center background cell and the two ink taps on each side, so that the detector only fires when a background point has ink on both sides. Setting the threshold just above what one side can contribute should block single-stroke false positives, though a thick stroke on one side may still get close.

I'm setting the background cell in the first convolution to be positive only in empty space, so max-pooling keeps it alive inside small holes. I'm also adding vertical versions of the between-detector, with taps above and below the center.

Now I'm finishing the vertical between-detector, which should fire inside 0s and 8s and in the openings of 3 and 5, but not inside a short 0. Each pooled cell takes the max over its 2x2 block, so a hole that's only a few pixels wide still shows up.

Now I'm filling in the H-between table for digit 0, expecting strong presence in the middle two columns of the top and bottom rows.

I'm working out which digit the vertical between-detector fires on: for a 2, the region right of the diagonal and above the bottom bar, where the diagonal sits about 5 pixels above and the bar about 3 below.

Now I'm filling in the V-between table for digit 3: the upper left concavity, between the top arc and the middle cusp, should show strong presence in the first two rows, and the lower left one, between the cusp and the bottom, in the last two.

Now I'm filling in the H-between weights for digit 4: the open top between the two verticals should show strong presence in the upper middle cells, and a closed top would trigger it too. For the V-between table on 4, there's little below the horizontal on the left, so only a closed interior would give a weak signal. Next is starting the 5 entry, with the top-right opening between the top bar and the middle stroke.

Now I'm filling in the H-between weights for the digit 6, which has a loop at the bottom, and the V-between table for the digit 3, where the middle rows and the bottom stretch matter most.

Now I'm filling in the V-between weights for digit 8, with the top loop and bottom loop each giving presence in their middle cells, and the sides near the waist showing ink above and below.

Now I'm adding the top-loop and bottom-loop cells of the 9 and 8 digits to the template, and deciding to give them moderate weight in the classifier as well.

Checking the tap offsets: (2,1) and (2,3) sit within two input pixels of the center, so a stroke that close still falls in range.

Next I'm setting up the lookup tables for the horizontal and vertical between-detectors, one 4x4 grid per digit, and I'm leaving the bias adjustment as it is for now, though the large template values may penalize some digits.
