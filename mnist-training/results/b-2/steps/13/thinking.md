I'm mapping the nine class indices to their top and bottom bin pairs. For row 0, the 487 count sits at the (2,2) cell where both bins are strong, while 244 and 104 fall at (1,2) and (1,1), so this row has no holes.

Row 2's top arc is firing the hole detector, which is a false positive since 2 has no real hole. Row 3's bottom bay fires it too. Row 6 is the odd one: its bottom loop doesn't register at all, possibly because the loop is small and thick enough that its center isn't empty, while its upper part gives a weak signal.

I'm checking whether the top and bottom labels are swapped, since row 9 and row 6 look reversed under my current mapping while row 2 and row 3 look reversed the other way.

I'm checking the cell row mapping against the flatten order, and it holds: row 0 is the top of the image, so the top/bottom split is correct. That leaves the odd cases, like 6's loop and 9's top loop not registering, which might come down to loop size or thickness rather than a label swap.

I'm re-checking the edge kernel sign convention for the 90° and 0° orientations to confirm which channels respond to ink on the left versus above, since that determines whether the top/bottom mapping is actually inverted.

I'm checking whether a 2's top arc fits the hole pattern, since its walls all face inward like a real hole's would. The left end of the arc curling down and the diagonal stroke below might make that region look enclosed, so it's a plausible explanation for the false positive.

I'm concluding that the hole detector is really a large-concavity detector, which explains why small, slanted loops like 9's and 6's don't register while big interiors do. For those small loops I'll need a different approach, since at the pooled resolution their interiors only span about one or two units.

I'm considering a 3x3 version of the detector, checking for inward-facing walls on each side and an empty center, since a small hole's interior might only span a unit or two at this resolution.

I'm working out how a small hole differs from a stroke at this resolution. Both show ink on the left and right at the pooled scale, so the only distinction is the order: a hole has its left wall's inward edge before its right wall's, while a stroke has them reversed.

I'm thinking about a small hole detector that tests for ink on opposite sides of a dark center, using a 3x3 pattern of walls and an empty middle, since at this resolution a small loop's interior only spans a unit or two.

I'm considering a small-loop detector at the conv1 level: a 5x5 ring with a negative center, so it fires on dark centers of 2 to 3 pixels surrounded by ink, which would cover the 8, 9, and 6 loops that the large-hole detector misses. Interiors of 5 to 6 pixels would fall between the two detectors, and I'm not yet sure conv2 covers them.

I'm weighing whether to free up two conv1 channels by collapsing the diagonal polarities into single line detectors, which would make room for a ring-shaped detector that fires on tiny dark centers ringed by ink. The catch is that this changes how the diagonal templates respond, so it's a risky trade even if it's workable.

I'm weighing a conv2 small-hole detector built from pool1 units: inner faces of the walls sitting on the center cells, with the outer faces on the far side.

I'm laying out the edge pattern a small hole would leave in the pooled maps: outer faces on each side, inner faces on the inside, with the sequence right-left-right-left across the center. A plain vertical stroke only gives a right-then-left pair, so the order of those edges is what would tell a small loop apart from a stroke.

I'm trying a horizontal-pass version of the detector, weighting inward-facing edges in the center cells and penalizing outward-facing ones on the far sides. The problem is that a thin wall's outer face could sit right at the edge column, so a hard penalty there might throw out real small loops.

I'm weighing a penalty on the outer faces: a light negative weight on right-facing ink in column 1, since a thin-walled loop's left wall could sit near the edge and its outer face would land there.

I'm checking whether a vertical stroke could be mistaken for a small loop at the center. Its edges would only give weak horizontal responses at that position, around 0.6 total, which should stay below a threshold near 1.0. A crossing, like the middle of an 8, would show edges in every direction at the center, so it can be told apart from a loop.

I'm comparing the measured per-class hole responses against the templates I wrote, and they disagree: the hole channel reads as a large enclosed region, firing strongly for 2, 3, 4 and 0, weakly for 6 and 7, and hardly at all for 8 and 9. That means my template assumptions for 6, 8 and 9 were wrong, so I'll rely on the measurements rather than the design.

I'm replacing the hole-based template weights with per-class scores fitted to the measured top and bottom hole responses, since my original template assumptions turned out to be wrong for 6, 8 and 9. To approximate a naive Bayes fit with something linear, I'm assigning rough average bin values to each level and computing each class's expected response.

Now I'm tallying each class's bins by top and bottom position, splitting the counts for classes 0 and 1 into their top and bottom sums.

Now I'm tallying the per-class counts into top and bottom sums, starting with class 3 and class 4.

Now I'm tallying the remaining classes, 7 through 9, into their top and bottom sums.

I'm reconsidering the bottom-left region for class 7, where the count of 664 looks suspiciously high for a digit with no loop, which suggests the detector responds to general concavities rather than enclosed holes. Given that, a naive Bayes fit on these aggregates won't map cleanly onto a linear layer, so I'm weighing whether conv2 can produce thresholded bin indicators per cell.

I'm now turning the hole response into a linear term: each class gets a weight on the top and bottom hole sums, scaled by how far its average bin level sits from the overall mean. For the top position, class 0 and class 2 sit high, class 1 sits near zero, and class 3 sits low.

Working out the rough score for each class from its top and bottom "at least some ink" rates, for example class 2 sits high on both while class 1 is near zero.

Now I'm turning the per-class averages into linear weights: each class's score sits above or below the mean, and I'm scaling that gap so a one-unit difference maps to roughly 1.5 logits per unit of hole response.

I'm going to swap the hole-channel weights for the per-class ones I measured from the histograms, applying them as a linear term over the top and bottom aggregates. Since the bins are nonlinear and the aggregates aren't, I'm using a rough linear fit and accepting that it's an approximation.

Next I'm thinking about measuring the remaining structural channels, 5 through 9, in batches of two per step, so about three more steps. I could also consider aggregating features by quadrant, but that would be far too many measurements to run one at a time.

I'm settling on a diagnostic for the next step: measuring three structural channels at once with a binary threshold on each, which gives eight cells to separate the classes with, instead of measuring two at a time.

I'm going to measure the remaining channels in one pass: top and bottom for 5 through 8, plus center for 9. I'll use three binary features at a threshold around 0.2, since class-conditional probabilities of a binary event are enough to derive linear weights.

I'm weighing whether to measure the remaining structural channels two at a time with three bins each, which keeps scale information, or three at a time as binary features. I'm leaning toward the two-by-three version for consistency and will check the top and bottom responses for channel 7 first.

I'm settling on a measurement for this step: channel 7's top and bottom responses, split into three bins each, with channel 8's top response also in view, rather than one channel at a time.
