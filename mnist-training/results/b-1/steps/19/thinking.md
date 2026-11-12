The model is at 67.3% accuracy and the calibration step is working, so the next thing is to improve how well it tells digits apart. The biggest confusions are 5 with 8, 8 with 3, and 8 with 2. I'm considering better templates, starting with 5 versus 3, where the main difference is the upper-left vertical stroke that a 5 has and a 3 lacks.

I'm weighing whether hole detection is worth another try, since 8 has the worst precision and holes separate 4 from 9 and 0 from 8. The earlier small-hole detector misfired, so its effect is uncertain. I'm also considering adding shifted orientation channels in the free slots 13 to 15.

I'm working out how to detect holes: a hole is an empty region fully enclosed by ink, and a 5x5 window needs ink on all four sides, which summed weights can't express directly. Pooling and dilation may erase the small interiors of 9s and 8s, so I'm considering a conv1 channel that tests only the center pixel's ink without dilation.

I'm sketching a small hole detector that checks the four sides around the center cell, weighting each side's two neighboring cells and setting a bias so that only fully enclosed interiors fire. The worry is that an open 3 with empty left-side cells could still push the sum high enough to trigger it.

Checking whether a hole has ink on all four sides means each direct neighbor of the center cell must be inked, which a single weighted sum can enforce with a tight bias. The catch is that a hole wider than one cell won't have its neighbors line up with any single center position, so it would go undetected at that spot.

I'm weighing a scale-2 hole detector that would catch larger interiors, since a single fixed-distance check would miss holes wider than one cell, though I'm wary of the extra cases this adds.

I'm considering a larger hole detector with a few different spacings, since the interiors of 8s, 9s, and 0s vary in width. Some variants would check neighbors one cell away and others two cells away, so the detector can catch both tight and wider loops, and I'll need to keep the false-positive rate in mind.

I'm working out a hole detector that needs ink on each side of the center cell, but a hole's distance to the ink varies with its position. So I'm considering letting each side count if the ink sits one or two cells away, allowing for asymmetric interiors.

I'm settling on a two-variant hole check: one with neighbors at distance one, and one with them at distance two, since a single fixed spacing would miss interiors of different widths. A third, taller variant with horizontal sides at distance one and vertical sides at distance two may cover the asymmetric cases, though a hole two cells wide still slips between them.

I'm considering a dilated ink channel with a larger kernel so that the side cells of a two-cell-wide hole register as ink, while keeping the raw ink map for checking that the center is empty.

I'm considering a binarized dilation for conv1, where the response is clipped to the 0-to-1 range with a bias before summing over a 3x3 neighborhood. Summed ink can overshoot on thick strokes, so clipping first would stop a thick side from compensating for a missing one.

I'm weighing a hole check that requires each side to be inked at distance one or two, but summing two cells per side lets a thick stroke on one side cover for a missing one. Single-cell checks at several distances avoid that, though a 2x2 hole with an asymmetric position would still slip past each one.

I'm weighing whether a different approach would help more than hole detection, such as reshaping the orientation features or trimming the redundant shifted ink grids to free up channels for more useful ones.

Still working through the hole detector: a 1-cell variant with four neighbors inked and the center empty, which is where the sketch is breaking off.

Still working out the weights for the bottom-left-anchored hole detector, and now sketching a taller variant that checks the cells above and below the hole.

I'm sketching a larger hole detector for 0s: a 3x3 cell interior that must stay empty, with ink required on each of the four outer sides at one-third weight, and a bias set so that a single missing side keeps it from firing.

I'm settling on a 2x2 hole detector with asymmetric side weights, and a tall 2-wide, 3-tall variant for the 0s whose interiors don't fit a fixed square. Each side is capped at one cell's worth of ink, so a missing side can't be made up by a thick stroke on another.

I'm settling the hole detectors' weights: each side cell gets a positive weight and the interior gets a negative one, with a bias set so a single missing side can't trigger a fire. For the digit scores, the top and bottom rows of the hole grid each get their own per-digit weights, with 9 and 8 favored on top, 6 and 8 on the bottom, and a separate tall detector mainly rewarding 0s.

I'm scaling the hole detector weights down by about half, since at logit scale a 0.8 hole response already contributes a lot. The class calibration will shift once holes add positive or negative contributions, so I'll keep the bias for now and recalibrate on the next step.
