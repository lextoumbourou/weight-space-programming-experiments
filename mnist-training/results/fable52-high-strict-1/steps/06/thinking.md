I'm decoding each digit's output as a sum of the three signals, a + 2b + 4c. For digit 0, the value 3 means the LR and UD signals both fire and bot is off, which suggests UD is firing on zeros where it should be silent. For digit 1, the three candidate values point to LR firing on most 1s and bot matching them.

I'm checking which digits the bottom-row signal fires on: it looks strong for 1, 4, 7 and 9, and weak for 0, 2, 3, 5, 6 and 8. The left-right and up-down signals are firing in nearly every cell, so the wall responses are probably adding up past the threshold.

I'm working out the wall response for a stroke sitting between cells, which comes to about 0.33 for a neighbouring cell at a one-pixel offset, and I'm checking how the response changes as the stroke center shifts toward a cell's edge.

Checking the one-pixel offsets, a stroke centred on a cell's edge gives that cell a response near 1.19 and its neighbour about 0.33, so the strip totals around 1.52. That leaves the LR response near zero, which is small enough that a background of 1 could tip it either way.

I'm checking whether slanted strokes, like the diagonal parts of 1s, could push the left-right response past threshold even when the stroke sits between cells, since a tilted line might spread its response differently than a vertical one.

I'm working through the slanted-stroke case: the response splits between the vertical and diagonal walls, roughly 0.85 and 0.7, and spreads into the neighbouring cell as the stroke shifts horizontally, bringing the total near 1.7 and the left-right response to about 0.2. Next I'm turning to 45° strokes.

Diagonal strokes break the cap I was relying on: a slanted wall lights up two adjacent cells in the same strip at full strength, so the sum climbs to around 1.8 and the left-right response turns positive from a single wall. I still need to check whether the up-down strips behave the same way for diagonals.

I'm now weighing the probe's 0.3 threshold, which is too low: weak false positives of 0.05 to 0.2 across several cells add up past it, so the probe can't tell real firing from noise. That suggests the detectors might work with a higher threshold. I'd need the distribution of values rather than a single sum, so I'm considering a histogram probe.

I'm looking for a way to make the wall responses saturate, since a single wall's strength varies too much for a plain sum-threshold AND to be reliable. One option is to cap the response with a difference of two ReLUs in the first layer, so the second layer sees a bounded value.

I'm looking at a way to cap each wall's response, using a difference of two ReLUs so the second layer sees a bounded value. The idea is to compute a broadly vertical-tuned wall detector directly from pixels, so a single stroke saturates to about 1 regardless of its slant.

I'm weighing whether a saturating first layer could cap each wall's response, since a plain sum over two cells can still reach 2 for a diagonal stroke. Limiting the pooling to a single cell per side might keep the strip total bounded.

I'm considering whether the single-cell alternative could work: put one capped wall detector at each side's offset, so the AND becomes a crisp threshold rather than a fragile sum. The cost is that the wall spacing then has to match a narrow range, so I'd need separate channels to cover different hole widths.

I'm weighing whether a conv1 kernel could detect a vertical-ish wall located anywhere within a single pooled cell, so the left-strip signal would be capped at one regardless of how many cells the stroke touches.

I'm weighing whether the wall detector can be made to saturate without losing its reach: a close-range version only catches very narrow holes, so the real option is to accept fuzzier features and set thresholds from a histogram of the left-right sums across each digit class.

I'm thinking about making the wall detector cost less on diagonal strokes, by reducing the weight on the diagonal kernels so that a slanted wall spread over two cells contributes about as much as a vertical one.

I'm working out the threshold for the combined left and right wall responses: if I cap each single-wall response near 1.3, a lone wall stays under a combined cutoff of 2.5, while two typical walls still clear it, though only narrowly.

I'm weighing a cleaner way to combine the two strip responses: taking their minimum, which can be written as a linear sum minus rectified differences, though max-pooling after the second layer would break that linear combination.

I'm considering a different route: since the two-cell strip sums are hard to cap, I'll rely on the INK-based tip-like detectors, which have been reliable, and build the new design around their geometry and coarse negative surround.

I'm now considering whether the same ink-based template idea can handle holes: a center cell that must be empty, surrounded by ink at a fixed radius, using the fact that ink values are already capped at 1 after max-pooling.

I'm considering a hole detector built from ink rather than wall strips: the center cell should be empty, with ink at a fixed distance on each of the four sides. Since ink is capped at 1 per cell after pooling, each side's response stays bounded, which avoids the summing problem I hit with the wall detectors.

I'm now proposing the hole detector as a fixed AND: ink at each side and background at the center, passed through a ReLU with a threshold of 2.3. Since ink and background are both capped at 1, a single wall can't push the sum past the threshold, so the response should be safe from single-stroke false positives. Two solid walls with the center empty should still clear it, though only just.

I'm looking at making the ink signal saturate, so a thin stroke still reaches full strength. One way is to split a scaled mean into a clipped ReLU and an excess term, then subtract them, which caps each cell at 1.

I'm working out a saturating version of the ink signal: keep the plain 3x3 mean as one channel, and add a second channel that only turns on above a higher level, so subtracting the two gives a value that tops out at 1. Taking the max over pooled cells keeps that cap intact, so a thin stroke can still reach full strength.

I'm working toward a hole detector built from saturated ink cells: each side needs ink at a fixed offset and the center must be empty, so an n-way AND can't be fooled by a single stroke. The remaining question is how to widen the position tolerance, perhaps with separate channels for different hole sizes.

I'm laying out the channel budget for the gap detectors: replacing the four current ones with a medium-sized hole detector, a left-right enclosed variant for the 0s and 4s, and an open-left cavity detector that needs the right wall and empty background on the left.

I'm sizing the hole detector's offsets: a wall at two cells out should only register if its center falls roughly 1.5 to 6.5 pixels from the cell center, and the center window has to stay empty, which pushes the wall at least about 2.5 pixels away.

Checking the hole detector against the 0's case: its vertical inner span is about 14 px, so the top and bottom walls can't both sit within the offset window. The template fails for 0, and I'm working out whether that is a fundamental limit or just a matter of channel placement.

I'm checking whether a zero's tall inner hole can be captured by an open-ended slot: walls on the left and right, with empty space above and below. A hole that tall would need about 11 px of inner height, which the smaller loops in 6, 8 and 9 don't have, so the slot would separate 0s from them.

I'm laying out the channel set for the new gap detectors: a full hole detector that needs walls on all four sides, a tall slot for the 0s that needs walls only on the left and right with empty space above and below, and a cup variant for the open top of a 4.

I'm now checking the open-left cavity variant for 3s, with walls above, below and to the right and empty space on the left, which would also catch some 2s and 5s. A plain cup opening upward would pick up 4s and the bottom of 0s.

I'm now checking the open-right cavity for 5s, 6s and the bottom of 2s, with walls above, below and to the left and empty space on the right. I'm also considering a fourth variant with the opening downward, which might catch the top of 0s, though I haven't settled on its exact walls yet.

I'm listing the structural features that might separate the digits: the hole detector would catch 6, 8 and 9, and the tall slot is for 0. The bottom-narrow shape looks strong for 1, 4, 7 and 9, and I'm weighing whether the top and side tip detectors are reliable enough to add, since they'd need the same kind of checks.

I'm mapping out which digits each proposed channel should fire on: the hole detector for 6, 8 and 9, the tall slot for 0, the open-up cup for 4, and the bottom-narrow shape for 1, 4, 7 and 9. I'm checking whether the top-wide orientation feature is enough to tell 1 from 7.

I'm now weighing a fifteenth channel for a top-narrow feature, the mirror of the bottom-narrow one, which might pick up 1, 4 and 6 but not the round digits.

I'm weighing whether to swap the top tip detector for a top-narrow feature, the mirror of the bottom-narrow one, since the bottom version has worked well. The concern is that digit tops sit at different heights, so I'd need to check that the pooled regions still catch the tops of 4, 1 and 6.

I'm weighing whether to add a top-narrow feature alongside the top tip detector, since it would be the mirror of the bottom-narrow one, but it might duplicate it. I could instead use a left or right tip detector to help separate 3 from 5 and 2, though I haven't verified any of these yet.

I'm settling the geometry for the wall offsets next, starting from the saturated ink cells and the conv1 positions that feed each pooled cell.

I'm checking how far a wall can sit from a pooled cell's center and still register: the 3x3 windows cover columns 2j+1 to 2j+4, so a three-pixel-wide wall only fires its cell if it lies within about one pixel of the window center, which makes the usable tolerance roughly ±1 pixel.

I'm working out how wide a wall can be and still register in a pooled cell: with a lower threshold, a three-pixel stroke anywhere within about two pixels of the cell's center would fire it, which gives roughly ±2.5 px of tolerance. The trade-off is that a more sensitive threshold also picks up stray ink touching the window.

I'm checking the wall offsets for the gap detectors: with a four-pixel-tolerant threshold, a three-pixel wall whose center sits roughly 1.5 to 6.5 pixels from the cell center would still register, while the center window has to stay empty.

I'm working out the exact wall offsets for the left side of the hole detector: with the stricter threshold, a wall whose center sits at about 2.5 px or further out, and inside the window the cell center stays empty, has to fall at roughly half-pixel positions on the grid.

I'm working out the wall placements for the hole detector: the walls can sit about 5 to 13 pixels apart, center to center, and still register, with the 6-pixel case giving a full empty interior and the smaller spacings giving a partial response.

I'm checking whether the hole detector really demands enclosure, since the axis cells alone might not be enough to prove a closed loop. The diagonal corners shouldn't matter, so I'm confirming that an open-top 4 gets no hole signal, which leaves it at zero.

I'm checking the top of the 2s: the hook start could fall within reach of the hole detector's left wall, so some 2s might trigger it falsely. I'll let that channel carry zero weight for 2s at the top and move on to the 5s and 3s.

I'm checking how the slot detector would respond to the zero: its side walls sit about five to six pixels out and the cells above and below the center stay empty, so it should fire on 0s. For a 4, the same check comes out borderline, and for 6, 8 and 9 the loop walls leave too little empty space above and below for it to fire.

I'm working through the cup-up detector for 4s: its two arms sit about 8.5 pixels apart and the bar below falls within reach, so the open top should keep the cell above empty. Its response should be strongest where the center cell lands in the 4's interior.

I'm checking whether the 4-versus-9 separation holds: a 9's loop can have enough inner space that the cup-up detector partly fires there too, so I want the open top to be required explicitly.

I'm working out a layout where the center sits at kernel row 3 with side walls at columns 0 and 4, and a bottom wall one cell below. The open region above the center would need to be checked with two background cells, so the detector only fires when the top is genuinely open.

I'm checking whether the open-top requirement holds for 9s: their loop is too short for the cup detector's background cell above to stay empty, so I'd move the center down and the bar lower so the top region must be clear, keeping 4s firing and 9s silent.

I'm checking how the 9's top arc interacts with the background probe: a point just above the arc still reads as empty background, but a probe placed inside the loop catches part of the wall, so the response for 9s comes out partial.

I'm settling on a simpler split for 4 versus 9: the hole detector gets required at the top for 9s and forbidden for 4s, and the cup-up detector handles the open top of 4s. For the open-left check I'm starting from the top, bottom and right signals, with the center cell kept empty.

I'm checking the open-left test for the 3's upper cavity: the top arc, the middle bar, and the right wall should fire, with the left side and center left empty, which holds since the top-left tip sits a few rows above the probe.

I'm checking the open-left test for the 0's right side and the belly of the 5: the bottom-left tip of the 5 sits a few rows below the probe, so that cell still reads as empty, and I'm still working out whether the 0's interior keeps the top and bottom walls within reach.

I'm checking the open-right case as the mirror image: the top and bottom walls plus the left wall should fire, with the right side left empty. For the 5's top bar, the gap is small enough that the center still reads as empty, and I'm now looking at whether the upper stroke of a 6 gets close enough to trigger it.

I'm checking the open-right case for 6s: the upper stroke should sit up and to the left of the center, so the top and left signals fire while the right side stays empty. The 2's bottom wedge only gives a partial response, and the other digits stay near zero.

Writing the convolution definitions for the second layer...

Still writing the convolution weights...

Now I'm checking the spacing and thresholds for the convolution weights, since the bias values and the 4x4 window for the wall signals need to line up with the cell positions.

Now I'm assigning which features each digit should fire or stay silent on: the slot detector for 0s, the bottom-row signal for 1s, and the open-left and open-right detectors for 2s.

Still writing the detector assignments...

Now I'm assigning the forbidden cells for 8s and 9s, and marking the hole detector as required at the top for 9s. The remaining digits get their scaling factor bumped so the features stay crisp.

I'm weighing whether to build a classifier outright or keep probing the detectors one at a time, since each classifier run also tests them. The BOT detector's misfire on 2s is the main risk, so I'll set its weight carefully and let the confusion matrix show whether it holds.

Now I'm settling on a classifier built from the orientation signals, the verified bottom-row rule, and the new detector features at moderate weights, and I'll keep the class bias for 8 at -0.2 since its two hole detectors and the forbidden cells should suppress it on the 0s.

Now I'm setting the forbidden-cell weights for the hole detector: it should stay silent on the wrong half of 6s and 9s, with the others scaled by digit.

Still writing the table of forbidden and required weights...

Now I'm assigning the point positions for the 0's slot detector and the left and right wall cells, which are both 1.

Now I'm setting the slot detector's extra cells for the 0s and the cup detector's bottom cell, then moving on to the overall weighting and thresholds for each feature.

I'm settling the amplitude at 1.3 rather than 1.5, since the feature values are already saturated to crisp 0-or-1 values by the S = min(4M, 1) construction.

Still writing the point table for the classifier, this time assigning the hole detectors for 8s and the top-arc tip weights.

Still writing the point lists for the classifier...

Still writing the point lists for the classifier...

Still writing the classifier weights and point lists, now the bias terms for each class.
