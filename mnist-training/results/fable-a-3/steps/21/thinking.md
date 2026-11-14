I'm at 88.35% with a loss of 0.4279 and 30 steps left. Next I could finish measuring the unmeasured "/" positions, nine of them plus refining five rough ones, which is about 3-5 steps for a small expected gain, since the corner and side positions might matter more than the rest.

I'm weighing a few other options now: new feature channels, which would take several steps each to measure, tuning the NB weights for correlated features, or calibrating the temperature and biases, which looks like a cheap way to lower the loss.

I'm considering whether calibration matters as much as accuracy for the test score, since the final pick uses the lowest-loss step. I'm also thinking about how NB's independence assumption limits it, and whether a pairwise correction targeting the 2-vs-3 confusions could help.

I'm considering whether scaling the weights for each orientation group, with four factors tuned by feedback, could help, since some features like the horizontal ones may be double-counting the same evidence. Scaling alone won't flip the wrong-direction errors, but reweighting redundant features might.

I'm now weighing which new features would best separate the curvy digits, 3 from 8 especially, since 8 closes loops on the left side that 3 leaves open. I'm thinking about vertical features in the left column for that.

I'm checking how the 3-versus-8 and 5-versus-8 splits look on the left and top-right columns, where the typical digits separate cleanly and the errors are probably atypical samples. I'm also considering loop-closure features, like whether a loop closes in the upper or lower half, since those would separate the curvy digits in a way the current channels don't.

I'm thinking about loop detection as a way to separate the curvy digits, since 8, 9, 6 and 0 enclose holes that 3, 5, 2 and 7 don't. A local detector could look for an empty centre with ink above, below, left and right in a 5x5 window, using a combined ink map across orientations.

I'm working out whether a loop detector can be built from linear convolution: a hole would need ink in all four directions around an empty centre, but the "any ink to the left" test isn't capped at one, so the sum can overshoot and I'd need weights that keep it roughly in range.

I'm checking whether a simple cap on the left and right arms would stop the loop detector from overcounting stroke thickness, and I'm weighing single-cell arms against the fact that loops vary in size. I'm also considering whether an emptiness test at the centre, combined with a complementary "not bounded on the left" signal, could avoid the cap problem altogether.

I'm working out whether the four directional "open" indicators can be combined linearly: a leftward ray counts as blocked when the summed ink to the left is at least one, and a hole needs all four blocked. A final sum of the four open indicators equal to zero would then mark a hole.

I'm realizing the per-channel max-pooling breaks the idea: each "open" indicator gets pooled separately, so the four directions aren't tied to the same position, and since the ray origins often sit on ink or outside the digit, the open signal is almost always 1 somewhere. So the summed feature wouldn't isolate real holes.

I'm now looking at endpoint features as an alternative to loop detection: a stroke end would show ink along one direction at the centre and nothing beyond it, which avoids the cap problem that breaks the hole detector.

I'm checking whether an endpoint detector can work: a vertical stroke's top end would show ink at the centre with nothing above it, and a ReLU over that difference gives a clean AND-NOT. The catch I'm noticing is that the vertical response seems to fall off about a cell before the true end, so the detector might fire early or miss the tip.

I'm checking the endpoint idea for the top of a vertical stroke: the centre should have ink, while the cells directly above it, in the row above and the row above that, stay empty. I'm also considering that a leaning stroke would continue up-right, so those cells need to count as well, and I'm thinking about whether to add diagonal responses to the centre test so that slanted endpoints get caught.

I'm weighing whether a false positive would appear at the top of an arc: a centre sum of 2 with a little ink beyond it gives a small positive response. I'm considering whether a strong penalty on the cells beyond the centre is enough to suppress those cases.

I'm checking the top-end detector against the digits: a stem's top with nothing above it should fire for 1, 4, 5 and likely 6, while 7 and 9 would get no top end from this rule.

I'm now going through which digits have endpoints in each direction: the 2, 3 and 5 have left-facing ends, while 1, 4, 7 and 9 have downward ends at the stem bottom.

I'm checking which digits have endpoints in each direction: the 3 and 5 have left-facing ends at their top and bottom, while 2 and 5 have right-facing ends at the base and top bar. Those left and right ends should help separate 3 from 8 and 2 from 3.

I'm checking where the centre taps actually land: they cover input rows roughly 6 to 21, so a stroke end near the top or bottom edge could fall outside that range and get missed.

I'm now checking where the centre taps land for the up-end detector: with the stroke tap shifted down a row, the coverage moves, but it pushes the top-end response later, which is the wrong direction for stroke starts near row 6-7.

I'm settling on the upward end detector: its stroke tap sits at kernel row 1 so it covers input rows 4 to 19, and the "beyond" test only needs the three cells in the row directly above. I'll check whether that single row is enough to rule out a continuing stroke, and whether the top boundary at pooled row 0 causes any problems.

I'm checking how the vertical response fades near a stroke's top end: it reaches full strength a bit below the true end and only partly covers the cell just beyond it, so that partial value could leak into the "beyond" check if it's weighted heavily.

I'm checking how a stroke end straddling two pooled cells affects the response: the partial value in the cell above, around 0.33, gets multiplied by the beyond weight and can wipe out the detection, giving zero in one alignment. Shifting the stroke tap to the cell above only brings the peak back to about 0.33, so the detector's strength depends on where the end falls.

I'm testing whether a stroke tap split across two vertically adjacent cells, each at half weight, keeps the top-end detector from being weakened when the endpoint straddles a pooled boundary.

I'm settling the up-end stroke term by splitting the stroke tap across two vertically adjacent cells at half weight, so a stroke end that straddles a pooled boundary still gives a strong response. I'm also checking whether adding the diagonal responses keeps that term from exceeding one when the stroke leans.

I'm settling the top-end stroke term now, and noticing that a lower-row ink cell with an empty cell above it would still count as an end, just one row off. I'm accepting that small localisation error as fine.

I'm checking the upward-end detector's "beyond" penalty against the arc case: the top of a "∩" has horizontal cells in the row above the shoulders, and those shouldn't count toward the stroke term, so the shoulder diagonals alone give a false response of about 0.5.

I'm settling the inhibition term so that the horizontal bar cells in row 1 also count against the stroke, which should suppress arc tops and the corner of a 7. Since the probes measure each feature's class statistics directly, I don't need the detector to be a perfect endpoint. The cost is the measuring itself, about four to five steps per channel.

I'm noting that endpoint features are sparse, so a single priority-encoded probe step could cover about nine or ten of them at once. Measuring the sixteen cells would then take roughly two steps per endpoint channel, around eight steps for four channels. I'm also considering a soft formulation where each endpoint channel is a value between zero and one, with presence read as the value exceeding one half, and feeding it into the classifier as a weighted log-odds term.

I'm weighing whether to cap each endpoint feature's total weight around 1.4 so the naive Bayes combination stays roughly bounded, accepting slight over-weighting rather than building a saturating trick. Then I'm asking whether spending the remaining thirty-odd steps on endpoint channels is the best use of them, estimating maybe two to four points of accuracy from genuinely new topological information.

I'm considering the max-pool coverage next: each pooled cell takes the max over its conv2 positions, so a stroke tap at kernel row 1 maps to input rows roughly 4 to 19. I want to check whether the top ends of digits like 1, 4 and 6, which usually sit around rows 5 to 8, fall inside that range.

I'm checking the downward-end detector next, using a stroke tap at kernel row 3 so it covers input rows roughly 8 to 23, which should catch stroke bottoms near 20 to 24. For the left and right ends, I'm moving the stroke tap to kernel column 1 with the beyond check on column 0, and then checking how its pooled columns line up with the input.

I'm defining the upward-end stroke term as an average over the vertical tap cells in rows 1 and 2, weighted so a stroke that straddles a pooled boundary still registers strongly.

I'm settling the up-end stroke term as a weighted mix of the vertical-plus-diagonal responses at the two cells below the top, so a stroke that leans or straddles a boundary still registers. I'm also adding an inhibition term from the three cells above and the horizontal cells in row 1, so arc tops and the corner of a 7 don't trigger it.

I'm working out whether the up-end channel should also be suppressed by ink at the two tip-side cells, since a 0 or 9 loop curving off the top of its left side could otherwise look like a free end.

I'm checking the inhibition for the up-end channel against a neighbouring vertical stroke one column over, which could wrongly suppress a real end, but I'm accepting that since such cases should be rare. I'm also moving on to the down-end channel, which mirrors the up-end one with the stroke tap shifted to the lower rows.

I'm defining the left-end channel as a stroke term over the horizontal and diagonal taps in the two cells to the right, with an inhibition term from the left-side cells and the vertical cells in column 1.

I'm checking the left-end channel's diagonal case: a stroke starting at the cell with a down-right or up-right diagonal gives only about 0.5, right at the probe threshold. I'm thinking about raising the diagonal weights so those ends register more reliably.

I'm reconsidering how to weight the left-end stroke term so the tip cell carries most of the signal and the cells beside it add less, which keeps the sum from growing too large when several next cells light up.

I'm working out a left-end detector with a stronger weight on the tip cell and smaller weights on the neighbours, plus an inhibition term from the cells beside the tip so vertical strokes passing nearby don't trigger it.

I'm checking the left-end detector's tip-isolation rule, since small-radius "(" arcs like the left bulges of 6, 8 and 9 could still look like free ends at the tip cell.

I'm testing whether a left-end detector can tell a true stroke end from a small left-pointing cap, since both would light up the tip cell and its neighbours. One continuing cell suggests a real end, while two suggests a cap, but a simple weighted sum can't express that distinction, so I'm looking for another formulation.

I'm realizing that an endpoint detector accepting every small left-pointing cap would fire on nearly all digits, so it wouldn't separate 3 from 8. I'll need a suppression rule that tells a true stroke end apart from the convex bulge of a loop.

I'm working out a left-end detector that only fires when the stroke continues horizontally to the right, with the tip cell and the cell beside it carrying the signal. To reject caps, I'm inhibiting ink in the left column and in the diagonal neighbours, so a small bulge that also continues diagonally doesn't count as a true end.

I'm checking whether horizontal-ish ends like the bar of a 7 or the tail of a 5 can be caught by a left-end detector that requires isolation from ink on the left, above, and below. Diagonal-ending strokes would be missed there, so I'm leaning on the up and down detectors to pick those up.

I'm now checking whether the up-end detector can be suppressed by ink in the row above and in the neighbouring columns, so that a stroke that continues diagonally doesn't count as a true end. I'm thinking about whether diagonal-ending strokes at 45 degrees are left out by all the horizontal and vertical detectors, and whether four extra diagonal end detectors are worth their cost of about sixteen steps, or whether I should first test up, down, left and right.

I'm worried that the inhibition from side neighbours would wipe out the up-end detector for any vertical stroke that is a few pixels thick, since its thickness alone would trigger the suppression. So I'm thinking the side cells should only reject caps and diagonal continuations, not the same-orientation neighbours.

I'm settling the up-end detector as a vertical-only term, leaving out the horizontal cells so a small cap doesn't count as a true end, and I'm starting to write its weights.

I'm finalizing the up-end detector's weights: the vertical cells count fully, the diagonal ones at half weight, and the horizontal cells are left out so that caps don't register. I'm also inhibiting ink in the row above and in the top-row horizontal cells, since ink directly above the tip means the stroke keeps going and a T-top isn't a free end.

I'm tightening the left-end detector: its tip cell and the cell beside it carry the signal, with inhibition from the column to the left and from the vertical cells in column 1, so that loop bulges, the corner of a 5, and a 7's serif don't count as clean ends.

I'm settling four channels for the up, down, left and right ends, each built from a short kernel that requires the next cell to continue the stroke and inhibits ink in the row or column beyond the tip. I'm placing the up-end tip at the top row and the down-end tip at the bottom, with the left-end tip in the left column, and I'm checking the inhibition cells for each.

I'm setting the right-end detector the same way: the tip at column 3 with the next cell at column 2, inhibited by column 4 and by the vertical cells in column 3. Slanted stems should still reach about 1.5, so the final feature range stays near [0, 1.5] with a probe threshold of 0.4.

I'm now sorting out the probing order: I'll check rows 0 and 1 first, since top ends are most likely there, and only then look at the rarer rows 2 and 3.

I'm now deciding how to combine the per-cell probes for the up, down, left and right ends, since a simple sum over a pooled set of lower-row cells would only tell me that something is present, not where. Some digits will light up several end detectors at once, like the two top ends of a 4, so the priority encoding has to handle more than one active cell per image.

I'm checking the tap positions one row above the tip, where the "next" cell lands on the tip itself, which gives a response of about 0.5. That clears the 0.4 threshold, so the same end could fire at two adjacent positions and land in different final cells.

I'm trying the tip cell alone, or weighting it at 0.75 against 0.25 for the cell beside it, so each end fires at its true position rather than at two neighbouring ones. That keeps the response high whenever the tip is fully inked and still strong when it is only partly on.

I'm settling the probe threshold at 0.45 with the 0.75/0.25 weighting, since that keeps the true tip above it and the neighbouring positions below. Then I'm running into a snag: a digit like a 4 has two top ends, so a single priority chain would only read the later one as absent, and I need to decide whether to group those cells jointly or reorder the chain.

I'm checking how the up-end features split between the left and right halves of the top two rows, since a 4 can show one end in each half and a joint encoding might handle that better than a single priority chain.

Now I'm working out how to split the eight cells: a two-step joint encoding for each channel, with one step over the left-half cells and one over the right-half, giving 8 steps total across the four directions.

I'm considering measuring all eight cells in a single step with a nine-outcome chain, accepting that it misreads the case where a 4 has ends on both sides. Running a second pass with the priority order reversed would recover the marginals for each cell, which is the same two steps but with more information per step.

I'm working through the joint probe for the case where one image has both ends of a 4. If two cells can be present together, reading them one at a time under a priority order undercounts the later one. Running the same probe in reverse order should give the missing marginals, though the cell that is the only one present is counted in both orders, so I can only bound each cell's true rate between the larger and the sum of the two readings.

Working out the sums for the two halves, I'm leaning toward one step that orders the left-half cells first, which gets their marginals right, and a reversed-order step for the right half. I'm considering whether to skip the second step and instead estimate the right-half rates for the digit 4 by assuming independence from the left-half ends.

I'm checking whether the hazard estimates for the right-top end of a 4 get biased low, since a 4 without a detected left-arm end may be a closed-top shape that also lacks a stem end, so the independence assumption may not hold.

I'm weighing whether to measure the up-end cells in one step, ordered by position, or split the work into a second pass. Some digits like a 4 have ends on both sides, so I need to check how a priority order treats the right-side cells once the left ones are counted.

I'm leaning toward putting the right-half cells first in the chain, since they matter for more classes, and I'm wondering whether a joint encoding would give exact right-side rates.

I'm settling on two probe steps for the up-ends, one for the right-half cells paired with a check on the left, and one the other way round. The down-ends look like a single bottom end around columns 1 to 2, so one chain over those rows should cover them. For the left-ends I still need to work out how the 2, 3, 5 and 7 cases split across rows.

I'm settling the up-ends as two probes, one chaining the right-half cells with a check on the left and one the other way round. The down-ends are a single bottom end, so one chain over rows 2 and 3 covers them. For the left-ends, the top and bottom halves get a joint probe in each direction, and the right-ends take one chain over columns 2 and 3, giving six steps in total.

I'm settling on six probe steps for the four channels, with the up-ends getting two joint probes each way round and the others one each. Before spending steps on it, I want to check the detectors aren't badly broken: if class 1 shows no up-end responses, the features are wrong and the measurements would be meaningless.

Still writing the convolution weights for the orientation channels...

Now I'm settling the inhibition for the up-end detector: suppressing row 0 across all orientations and the horizontal filter in row 1 beside the tip, since the stems of a 4 sit about four cells apart and won't interfere. I'm checking the closed-loop top of a 9 as well, which should be suppressed by the arc above it.

Writing the down-end inhibition for channel 13 now...

Now I'm setting the left-end channel: the tip gets a horizontal response with diagonal support, the cell beside it gets a weaker one, and the column and vertical cells around it are suppressed. The right-end channel mirrors this on the other side.

I'm checking the left-end responses for the 2, 3, 5 and 7 cases, and noting that the 3 has two ends on the left side, which makes a simple threshold on those cells a bit unreliable. I'll use a presence threshold around 0.45 and feed the features into the classifier linearly, since values between zero and that threshold still carry partial evidence.

I'm setting up the encoding for the right-half cells and the any-left check as a single joint outcome, so each probe step yields one combined reading.

I'm settling the separable encoding for the right-half cells and the left-any check: the best right-side cell gets chosen if it clears the threshold, and the left check is independent of it, so each probe step gives one joint reading. Step A pairs the right chain with left-any, and step B does the reverse with the left chain.

I'm thinking about using the extra binary factor in each probe step to measure a separate single feature, rather than leaving it idle.

I'm planning to cover all 32 endpoint cells in eight probe steps, each using a four-cell exclusive chain paired with one binary feature, which also lets me measure the remaining unmeasured "/" features one at a time.

Still working out how to cover the 8 cells per channel, with a plan to trim each chain to the four most likely positions for the downward ends.

Next I'm working out how the top and bottom probe rows should be covered: the down-ends likely sit in row 3 with row 2 as a backup, and the up-ends in rows 0 and 1. I'm starting to set up the left-edge cells by tip position.

I'm laying out the remaining probes as four steps: one for each of the upper and lower rows of endpoint cells, with a spare binary feature paired into each step to measure something else at the same time.

I'm working out the layout for the left and right endpoint probes, since each channel's cells need covering. The up-end cells, though, can't simply be chained along rows: the two ends of a 4 both sit in row 0, so a row chain would not be exclusive. I'm switching to column-wise chains instead, grouping the left half and the right half of the top two rows separately.

I'm splitting the endpoint probes into exclusive chains: the up-ends and the right-end cells each get a top and bottom half, and the down-ends get a left and right half, since each channel's ends mostly fall on one side. The left-ends need separate top and bottom halves because the 3 has ends in both.

I'm deciding how to cover the upper-right endpoint cells first, and I'll check whether the detectors behave before committing to the full plan. I'm also picking the first unmeasured "/" feature to pair as the extra binary factor in this step, starting with the bottom row.

Still setting up the weights for the up-end channel, with the probe encoding for each cell worked out.

Still writing the convolution weights for the channel 12 up-end detector, with its tip and neighbouring cells set.

Still writing the weights for the right-end channel, with its tip and inhibition cells set.

Checking the upper-end detector's inhibition against a partial response at the tip, the reduced score still clears the threshold. Next I'm turning to the 45-degree strokes, where the tip and the neighbouring cell don't line up the same way.

Checking the argmax chain: I'm confirming the outcome logit for each cell is weighted by how far it clears the threshold.
