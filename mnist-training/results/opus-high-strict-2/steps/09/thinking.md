I'm checking the anti-stroke results: six and five improved, three got much worse, and seven and nine shifted toward eight. Eight is now over-predicted and seems relatively favored since it has no anti, so I'm weighing whether to redesign or accept that this approach tops out around 68-70%.

I'm weighing a bigger structural change now, since hand-built linear templates on these features seem capped around 70%. I could move to finer pixel-level features or add a hole detector that picks up the closed loops in digits like 0, 6, 8 and 9, though the kernel sizes may be too small to catch those loops reliably.

I'm sketching a hole detector: a conv2 kernel that responds when background sits inside a ring of ink, which should pick out the closed loops in 0, 6, 8 and 9. I'm weighing how to split the channels between orientation features and a few hole channels at different sizes, so the pooled maps still tell me where each loop sits.

I'm working out the threshold for a hole detector: a 5x5 kernel with a ring of positive weight and a negative center, where a solid blob is suppressed but a partial C-shape still fires, so the bias needs to sit between roughly 10 and 16 times the ring weight.

I'm now testing whether a hole detector can work at this resolution: a 5x5 ring kernel would be too coarse for the small inner holes in 9 and 8, and the 0's loop may not line up with a 10-pixel square. I'm considering doing the loop detection in conv2 by combining orientation signals instead.

I'm considering a closure detector instead: a conv2 channel that sums vertical and horizontal edge signals on the sides of a 5x5 window and subtracts the center ink, so a full loop scores high while a C-shape scores lower. The sums might let one strong side compensate for a missing one, so this is a rough feature, and with seven steps left I'm questioning whether it's worth the effort, given the loop confusions among 3, 5, 8, 9, 7, 0, 2 and 4.

I'm weighing whether to keep the anti-stroke tweaks only where they helped, for 5 and 6, since they hurt 3, 7, 9 and 0. I could make the base step-7 version and tune from there, though the hole features might be worth more.

I'm deciding which anti-stroke tweaks to keep: the ones on 4, 5 and 6 helped, while the ones on 3, 7 and 9 hurt, and the 7 penalty seems to come from its top bar starting in the same place. Before designing the hole detector, I'm settling that base.

I'm sketching the hole detector on the pooled ink map, with a 5x5 kernel whose outer ring should fire on a surrounding loop of ink.

I'm checking how the 5x5 ring would line up with the 0's loop, since its outer width is about 11 pixels and the window spans roughly 10, so the border cells would only catch the strokes if pooling gives a bit of slack.

I'm testing a "both sides" detector instead: ink on the left and right columns with an empty center, which would fire on the loops of 0, 6, 8 and 9 and also on an open 4, while leaving 1 and 7 alone.

I'm checking whether a window that spans the 0's tall loop could still register as enclosed, since its top and bottom rows might fall outside the hole. I'm considering a combined rule that requires ink on both sides and above and below with an empty center, approximating a logical AND through a summed threshold.

I'm settling on a simpler pair of features: one that checks for ink on the left and right with an empty center, and another for top and bottom, each using only the middle cells of those sides. I'm also weighing whether the center should be a narrow vertical strip instead.

I'm laying out the left and right columns of a window, with ink on each side and the center empty, so it catches the loops in 0, 6, 8 and 9 and roughly 8 to 10 pixels apart.

I'm checking whether the loop cells can reach the 11-pixel spacing of a 0's strokes, since the 5x5 kernel tops out around 8 pixels. I'm weighing whether to switch to oriented maps, using vertical-leaning channels for the left and right sides and horizontal ones for the top and bottom.

I'm laying out the pooled output grid for the hole channels, where each final cell maps to a region roughly four pixels apart. I'm also weighing whether to drop to two diagonal offsets to free up channel budget.

I'm settling the checkerboard sampling: taking every other offset in both directions still covers the whole pooled grid, since the templates are smooth enough that the lost cells add little. That leaves eight channels for the hole features, with the rest of the budget going to the four orientations at two offsets each.

I'm placing the three hole channels in the conv2 budget: a left-right enclosure, a top-bottom enclosure, and a combined ring. For the 0, the hole's center column lands near position 13, so I'm checking which pooled columns it falls into.

I'm settling on location-tolerant weights for the hole channels instead of pinning each class to exact cells, since the loop positions shift across the pooled grid.

I'm assigning the hole channels a location-tolerant pattern across the pooled grid: the 8 takes weight in the top and lower-middle rows, the 9 is positive at the top and negative lower down, and the 6 is the reverse. For the 0, its tall hole spans the middle rows, so the left-right detector is the one that should fire there.

I'm defining the left-right loop detector on the pooled ink map, giving the left and right columns positive weight and the center strip negative weight so an empty hole registers.

I'm settling the left-right detector's column placement: the left and right columns each take a single column of pooled cells, so a thick stroke won't count twice. Blur from the pooling should let strokes anywhere from about 5 to 13 pixels apart still register.

I'm working out the center-strip sensitivity for the left-right loop detector, checking how a small 9 loop and a one-sided stroke would score against a bias that should only pass full loops.

I'm settling the left-right detector's weights: the side columns get positive weight, the center gets a strong negative, and a bias that only lets a near-complete loop through. With the ink values I'm assuming, a full loop should land at about twice the weight, while a single side or a lit center cell scores zero.

I'm checking the top and bottom row cells of the second detector, with a negative center strip, to see whether it fires on the loops of 9, 8 and 6. The 0 should mostly slip past it because its height is too great, and I'm also wondering whether a 2's top arc and middle diagonal could trigger it.

I'm checking whether the TB detector can separate a 3 from an 8: a 3's open left side would fire it in the middle, so the left-right test has to be ANDed with it. I'm now looking at a combined ring detector, adding up the four sides with a strong negative center, to see whether a full loop reaches its threshold.

I'm checking whether the ring detector would catch the loop of a 6, given that its loop is roughly nine by nine pixels, so the side cells should still light up.

I'm assigning the FC weights by row, with the 9's loop sitting mostly in row 0 and the 8's top loop there too. The side columns in the middle of the grid get full weight and the outer columns get about half, and the 8's squashed loops may not register at all.

I'm assigning the ring-detector weights per digit across the four row bands: the 0 gets the most weight in the middle columns, the 6 is negative at the top and positive at the bottom, the 8 is positive throughout, and the 9 is positive at the top and negative lower down. I'm still working through the 4's row pattern.

I'm assigning the TB channel zero weights for now, since its center strip would confuse a 3 with an 8, and I'm considering whether to drop it altogether and use that budget for a different feature.

I'm dropping the TB channel since it adds nothing a 3 wouldn't confuse, and I'll keep the feature scale at 1.0 rather than risk a large change. I'm also reverting the anti-stroke weights except for 4, 5 and 6, and switching the orientation channels to two offsets each.

I'm settling the rest of the conv2 weights for the left-right channel: the side columns get positive weight, the center column a negative one, with a bias set so only a near-complete loop passes.

I'm working out the ring detector's threshold: twelve side cells at half weight give about 4.8 for a full loop, so a cutoff near 3.9 should pass only near-complete loops. I'm also checking how much the faint strokes' pooled values could shrink that margin.

I'm settling the center penalty for the ring detector: rather than the whole 3x3 center block, which would catch the outer stroke of a 9-pixel loop, only the middle cell gets a strong negative weight. The left-right detector's center needs the same treatment.

I'm settling the center penalty at a single cell with weight -2.0 for both detectors, since a wider negative block would pick up the strokes of a 9-pixel loop. The side columns still line up with the loop's outer strokes, so the sides keep their positive weight.

I'm checking the ring detector's margin: a full loop lands near 0.9 after bias, a three-sided C scores below zero, and a solid blob is pushed negative by the center penalty.

Still writing the feature weight code...
