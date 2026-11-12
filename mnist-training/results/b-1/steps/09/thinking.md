I'm still stuck around 50%, and wondering whether single-prototype templates can ever get past that when nearest-centroid with means reaches 80%. I suspect a systematic geometric error, like a coordinate mapping that is off or transposed, so I'm rechecking how conv1 output positions map to input rows and their centers.

I'm checking the rest of the coordinate chain: pool1 to conv2 to pool2 lands the tap centers where I expect, and the flatten order matches. The digit boxes and stroke rows also line up, so the mapping itself looks correct. That leaves the templates and the coarse 4x4 grid as the likely weak point, since my hand-drawn 8s are much worse than the rest.

I'm weighing whether structural features like loops and endpoints would be more robust than the templates, and I'm considering hand-setting linear weights on such rule-based features. To detect a hole, I'm thinking about how conv2's 10x10 receptive field could pick up background enclosed by ink in several directions.

I'm sketching a hole detector for conv2: a background cell with ink on all four sides, roughly 4px out, approximated by summing directional ink samples and subtracting a threshold so only enclosed centers fire.

I'm working out how to detect holes with conv2: a background cell that has ink on all four sides, using directional ink sums with a threshold, plus a check that the center is empty. Small holes like those in 6s and 9s will need smaller offsets than the large ones in 0s, so I'll need two scales.

I'm tuning the hole-detector feature: averaging three cells per side gives about 0.9 when a stroke runs past that side, so the sum of four sides minus a threshold of 2.8 and a penalty for ink in the center should leave a peak of about 0.8. I also want to handle open shapes like 2, 3, 5, and 7, which usually show only three sides, so the threshold needs to be tuned around that.

I'm settling on a two-scale hole detector: one set of directional offsets for small loops like those in 6s and 9s, and a wider one for the big holes in 0s. I'll test whether the four-side threshold catches enough of the open shapes like 2, 3, 5, and 7 to matter.

I'm settling the hole detector's scales: a small one with offsets (1,1), a medium one at (2,2), and a tall one at (1,2) for the narrow interiors of 0s. Each hole channel then gets max-pooled into the final 4x4 grid, so where it fires should tell me which digits have a loop at the top, the bottom, or the center.

I'm mapping the hole features to the 4x4 grid next, with each cell's center at 4r+7.5, so a top loop lands in the upper rows and a bottom loop in the lower ones. The template score alone is weak, so I'm planning to add these hole rules on top of it, and I'll check whether accuracy improves before adding more feature types.

I'm weighing per-class hole weights next: the top-hole and bottom-hole channels should push 9 and 6 apart, and 8 should collect both. Holes can't be ANDed linearly, so I'll lean on the summed response and accept that. Open shapes like 1, 2, 3, 5, and 7 get a penalty for any hole.

I'm assigning per-class weights to the hole channels by row group: the small detector should push 9 up when its hole is at the top, 8 up a bit less, and 6 down there, while the large channels handle 0.

I'm assigning the medium and tall hole channels a broad weight: 0 gets a strong push, while 8, 6, and 9 get a smaller one where their holes sit, and the rest get penalized.

Next I'm assigning weights to the hole channels, planning to add a negative bias for 6, 8, and 9 so their holes actually have to be present.

I'm defining the small hole kernel's offsets, with a negative weight at the center and single orthogonal neighbors on each side for the tighter loops.

I'm settling on the kernel layout for the hole detector: the center gets a negative weight, and the four sides use single orthogonal cells for the small scale or three-cell averages for the larger ones. I'll set the threshold around -2.6 so that every side needs to carry ink.

I'm assigning the hole-channel weights to the 4x4 grid by row, with the top rows picking up 9 and 8 and the bottom rows picking up 6 and 8, using each cell's center at about 4r+7.5 to locate the loops.

Now I'm assigning per-class weights to the small hole channel, with the top-hole and bottom-hole responses scored separately for each digit, and I'm giving the medium and tall channels a single broad weighting across all cells.

I'm settling the biases for 0, 6, 8, and 9 at about -0.4 each, leaving the template score as the main signal, and I'm keeping the scale from step 8 as it is. I'm also checking whether the hole detector could false-fire on thick strokes or between the parallel strokes of an open 4, and the center-empty and four-sided requirements should rule that out.
