I'm checking the tuning results: 71.9% overall, with the under-predicted groups using bias around −0.3 to −0.5. Sharper features seem to mean the bias for group 8 can be less negative than before.

I'm working out a bias-update rule: nudge each group's bias by an amount proportional to the log ratio of predicted to actual counts, with a step size of about 0.6 based on how sensitive the counts were to the earlier bias changes.

I'm working out the per-class adjustments now: class 0 is slightly under-predicted and barely needs a shift, while classes 1, 2 and 3 are over-predicted, so their biases should come down, with class 3 needing the largest cut.

I'm working through the per-class column sums and the log ratios of predicted to actual counts, which gives each class's bias adjustment. Most classes are close to balanced, with class 3 still needing the biggest cut and class 8 needing a sizable boost.

I'm recalculating the bias updates for each class from the predicted-to-actual count ratios, which gives new values ranging from about −0.6 for class 3 to +0.4 for class 9. I expect that to land somewhere around 78 to 80 percent. I'm also wondering whether I can improve discrimination in the same step, though any structural change would shift the balance I just worked out, so the rebalancing would need another pass.

I'm weighing whether to do a pure rebalancing step now to get a solid baseline, or to slip in structural changes, since the 5→3 confusion (320 cases) is large even with class 3's bias already lowered.

Now I'm working out how 5 and 3 differ in my templates: real 5s tend to have a short, detached top bar and a large bowl, and the bottom end usually points left, which makes them look like an S. My 3s have a top arc running from upper-left to the right, then back toward the middle.

I'm comparing the 5 and 3 templates: real 5s may have their upper vertical closer to the center or shorter, and their top bar sits further right, so the top-right region is where they overlap with 3s.

I'm picturing how 5s and 3s differ at the top: a 5 seems to have its upper vertical on the left, slanting like a "/" or bending into a "(", while a 3's upper arc sits further right, around x≈16–18. So a penalty on upper-left vertical ink for class 3 might separate them.

I'm weighing whether a pairwise difference term could sharpen the 3-versus-5 boundary without shifting the balance I just worked out, since it would add signed weight to whatever differs between the two templates.

I'm checking whether the pairwise idea would work: for a confusable pair like 3 and 5, add a term that widens their separation, but then the 2s that share 3's upper-right arc could tip toward 3 and make the 2→3 confusion worse.

I'm weighing whether a purely pairwise contrast can change anything: summing the contrast over all other classes just rescales the template and adds a common vector, so the argmax stays the same. That means only the selective pairs matter, and the linear template classifier is already discriminative across all pairs in that sense. What's really missing is knowing which features are reliable, which I can only guess at without data. The real limit seems to be how faithful my templates are to typical digits and how much they vary within each class.

Now I'm recalling the typical mean image of a "5": a short top bar, a slanted upper-left vertical, and a large bowl lower right, with the tail ending bottom-left. I can't really sharpen my templates from memory alone, and I'm wondering whether the vertical scale or alignment is off, since I assumed a 17-pixel centerline height.

I'm thinking about whether the ceiling is set by the blurry class-mean templates themselves, since linear template matching may cap out around 80–85%. Getting past that would likely require parts-based features that capture structure independent of position, though designing those well takes more steps than I have left.

I'm sketching a ring detector for the conv2 layer, using 5x5 cell windows, to pick up closed loops in the upper and lower halves of the digit. That kind of loop feature should separate 9s and 8s from open shapes like 4s, 7s and 5s, and help with 6s versus 5s.

I'm sketching the ring detector's cell layout: a top band and bottom band, plus left and right bands, each allowing either a straight stroke or a diagonal. I'm leaning toward broader bands and a scale-tolerant center check instead of a strict empty-center requirement, since smaller loops would otherwise trip it.

I'm checking whether a ring detector with broad side bands would hold up, since a plain threshold on the four sides could fire on a wide loop like a 0 that has only its left and right walls present.

I'm weighing whether saturation can come from conv1 itself: a ReLU of the form 1 minus a scaled response gives a bounded "absence" signal, and inverting it through pooling would yield a presence measure that doesn't grow with stroke length. That would let a four-sided loop check avoid the weak-side problem, but it means conv1 would need to change, which costs another pass.

I'm considering whether a saturated background map could fix the weak-side problem: a blurred ink signal turned into "clear background" with a ReLU, then max-pooled, so a cell counts as ink only when all its pixels are inked.

I'm settling on a "hole" check: the center cell should be background, with the ring around it all ink, which I can build from a saturated background map.

I'm thinking about whether a hole detector can work with a saturated background map: the center cell should be background while the ring around it is all ink. The catch is that a band wide enough to cover the stroke can also fill in a small loop, so the ring radius would have to match the hole size.

I'm checking whether a background map works for a hole detector: a ring cell counts as ink only if all four of its pixels are ink, so a band of about 4 px should still leave one or two background cells inside a loop of centerline diameter 8. The open question is whether a cell that is background if any single pixel is background will make the ring cells look empty too often.

I'm testing an alternative enclosure check: the center should be background, and moving outward in each of the four directions should hit ink within two cells. The open question is whether requiring a full ink ring is too fragile, since real loops aren't perfectly round or fixed in size.

I'm trying to avoid false positives from a linear enclosure test: if one direction has both cells as background it should kill the response, but a direction with both cells inked would add a bonus that could cancel a failure elsewhere. So I'm considering using only the far cell in each direction, requiring it to be ink.

I'm checking whether a center-background test with the four far cells required to be ink works for loops of roughly diameter 6 to 10, since the far cells have to sit inside the stroke band despite small misalignments of the hole center.

I'm checking whether a center-background test with far ink cells would wrongly fire on open shapes like a 4 or a 3, where one of the four directions stays open. Quantized cell positions and the hole's offset from center make the far-cell radius fragile, but a 4-direction closure check still rules out most open-top shapes.

I'm testing whether a small loop survives the band thickness I'd need for stroke-width tolerance: if the ink band is dilated too far, an 8's upper hole shrinks to nothing, and the detector misses the very shapes it's meant to catch.

I'm now separating the hole test into two maps: a sharp background channel for the center pixel, and a dilated ink channel for the surrounding ring, so that small loops don't get filled in by the band thickness.

I'm weighing whether the four ending channels are worth keeping, or whether two of them could become a sharp background map and a wider ink map for a hole test. I can't tell their value without testing, but a loop detector looks like it could separate 9s and 8s from 4s and 7s, so the trade is worth considering. I'm also starting to think about whether enclosed background can be detected at the conv1 level.

I'm wondering whether a tiny 5x5 filter could catch the small hole in an 8 directly at the conv1 level: a dark center surrounded by ink on the border ring. MNIST strokes are close to binary, so an AND over those ring pixels might be reliable, though only for loops a few pixels across.

I'm weighing whether to drop the four ending channels for loop detectors, since their value is unknown and a loop check could separate 9s and 8s from 4s and 7s. Ten steps remain, so I'm thinking through a short plan: rebalance the biases first, then test the loop idea.

I'm now weighing whether to use the freed channels for enclosure features: a background cell with ink on both sides, which an AND over saturated pixels can express without extra nonlinearities.

I'm working through a concavity-style feature: a center background cell combined with ink at distance two in each direction would flag a hole. I'm also considering an "open to the right" check, where a background cell at distance two is ANDed with the center background, while the other directions must be ink.

I'm checking whether a loop with a centerline diameter of roughly 5 to 11 pixels would be picked up by "ink at distance two cells" tests, given a dilated ink band that covers the stroke within about 1.5 pixels of tolerance.

I'm checking whether "ink at two cells left, right, up and down" plus a background center would reliably mean a loop, or whether an open top on a 4 could still satisfy it. The up-direction is the risky one: if the crossbar sits just below the center, the down cell catches it, but the up cell should stay background.

I'm checking the 5 and 3 cases: the bowl of a 5 should be ink on the right, bottom and top, with the open left side usually background, and a 3 stays open on the left. The 2's top arc should register as ink, but a curled start could close the left side, so that case is uncertain. A 0 would need its inner half-width to stay under about 5 pixels for the four-direction check to fire.

I'm checking the hole detector on the remaining digits: a 0 has its top and bottom open within the four-cell reach, so it won't fire, which is fine since other features handle it. Loops in 6, 9 and the lower loop of an 8 should register, and thick strokes with narrow bays look safe because the bay center's left neighbor stays background.

I'm checking where the loop features would sit vertically: the conv2 map is 8x8 and pools into four row bands, and a 9's upper loop should land in the second band while an 8's upper loop could fall into the first or second.

I'm mapping the hole features onto the vertical bands: a hole in the top rows should push toward 9 and 8, one in the bottom rows toward 6 and 8. Class weights would then reward upper holes for 9, lower holes for 6, and both for 8, while holes generally count against 1, 2, 3, 5 and 7.

I'm weighing the per-class weights for the hole feature: a hole in the upper rows should push toward 9 and 8, a lower one toward 6 and 8, and a hole that spans several pooled cells would need a bit of care so its contribution isn't counted multiple times.

I'm settling on the sharp background channel: a 3x3 local ink average with the center weighted at 0.4, scaled so a pixel reads as background only where nearby ink is low. A hole's interior still picks up some ink from the surrounding edges, so the center needs to be quite clear before the channel fires strongly.

I'm settling the sharp background channel with a center weight of 0.5 and 0.125 on each of the four neighbors, scaled so a hole of 2 pixels or more still reads as background. I'm now starting on the wide background channel, which needs to stay clear of any ink nearby.

I'm now working out the Gaussian weights for a wide background channel, checking how much ink a 5x5 window picks up at roughly 2.5 pixels from a 3-pixel stroke's centerline.

I'm working out the wide background channel's weight: with a 5x5 Gaussian at σ≈1.5 and a factor of 4, the pixel one step past a stroke's edge reads as ink, and the pixel two steps past it comes out about half background.

I'm checking how wide the background band around a hole needs to be: a far cell two steps out counts as ink only if it sits within the 5-pixel ink band, which depends on the hole's distance from the stroke centerline.

I'm checking the band width for the wide background channel: a loop of radius 3 has its far cells inside the ink-free band, and radii of roughly 3 to 5 should work. The smallest loops, around radius 2.5, only just fit, and their inner hole is about two pixels wide, so the sharp channel would fire only partially there.

I'm checking the loop radii for the hole features: each loop's horizontal and vertical radii should fall roughly between 2.5 and 5.5 pixels, which fits the 9, 6 and 8 loops and rules out the 0's much taller opening.

I'm settling the hole test: the four far cells, two steps up, down, left and right, each get a negative weight on the wide background channel, while the center gets a positive weight on the sharp one. That way any ink in those far cells shuts the feature off, which should keep crossings and spirals from firing it.

I'm checking the bay openings next: a 3 has open bays on the left, a 5 has its upper bay open to the right and its lower bay open to the left, and a 2 has its upper bay open to the left. A 6's upper bay opens to the right, while a 9's lower-left bay is open on the left, which is more of a corner than a true bay. A 7 has an open bay under its bar on the left.

I'm checking the bay detector for openings to the left: the center needs to be background, the cells above, below and to the right need ink, and the cell two steps left needs to be clear. For a 3's upper and lower bays, the height works out to roughly 7 to 8 pixels, which fits the bay size I estimated.

I'm checking whether the bay detector's left-side test holds up: the cell four pixels to the left of the bay center may catch the start of the 3's top-left hook, which would leave it partly inked and make the detection uncertain.

I'm checking whether a 5's upper bay opens to the right, with the top bar and the bowl's top forming its edges and roughly 6.8 pixels of height. The bay center should be clear to the right, though the bowl's top might reach into that spot.

I'm now checking the bay detectors for the upper openings: a bay open to the left points toward a 3, one open to the right toward a 5, and one open upward toward a 4. I'm also weighing whether a downward-open bay would help, though I can't yet tie it to a clear digit.

I'm settling on bay detectors for the four open directions, with the upper-left and upper-right bays separating 3 from 5. Each detector needs a background center, ink on three sides, and a clear cell two steps out on the open side, so I'm planning four channels in the second layer.

I'm settling the channel layout: the first four convolution channels stay as orientation detectors, with the two ending types for left and right kept at two offsets each, and the vertical-ending channels dropped. The second layer then carries those endings, plus the hole and left-bay channels.

I'm defining the background-detection channels now, with the sharp one tied to a center pixel and the wide one checking its surroundings. I'm working out how each channel's response is computed from its neighborhood, and how the pooled cells pick up whether any pixel in them reads as background.

I'm defining the hole feature's response as a weighted check on the sharp background channel minus the wide background channel at the four far cells. Then I'm testing it on a circular loop of radius 4 with a 3-pixel stroke, looking at which pixels count as background at each distance from the stroke.

I'm checking the hole test's distances: the far cells sit about 3 to 5 pixels from the loop's center, which keeps them clear of the stroke's ink.

I'm checking the loop radii for the background test: at radius 3 the far cells fall inside the clear band, and the center still reads mostly as background. Radii up to about 5 keep the far cells clear of the stroke, and the band gets tight around 5.5 and above.

I'm checking the hole test on a 0 with a larger loop: a background cell inside the top of the loop has ink above it and to either side, but four pixels below it is open background, so the test fails there as it should. Then I'm starting on the open-top 4, where the cell between the two verticals just above the crossbar should have ink below, left and right.

I'm checking the potential false positives for the hole feature, where a background cell might have ink four pixels away in every direction, like the lower bowl of a 5 whose tail curls upward.

I'm weighing whether a lower-left hole should count against a 2, since many 2s have small loops at the bottom-left. Those loops are small, so they'd only partly trigger the hole channel, and the hole's column position should separate them from the centered loops of 6s and 8s.

I'm now writing out the hole feature's response for the far-cell check and how the lower-left loops of 2s interact with it. I'm also setting up the bay detectors' formulas for left, right and up openings, which will repeat the same pattern as the hole feature.

I'm estimating where the bay detectors should fire for each digit, starting with the 3's upper-left bay. Its center lands near the boundary between the first two conv2 row positions, so I'll count it as upper, covering the first two rows.

I'm now checking where the bay detectors should fire for the 5 and the 2: a 5's right-open bay should land in the upper rows and its left-open bay in the lower rows. For the 2, the upper bay looks open on top, right and maybe below, but whether the lower side counts as clear depends on a diagonal stroke I haven't settled yet.

I'm working through the bay detector for the 6's upper region, the open space right of the upper stroke above the loop, and whether it lines up with the expected rows.

I'm checking the bay detector for the 6's upper region: the open space to its right, above the loop, should have ink above it and to the left and below, so it fires for many 6s much like it does for 5s. For the 7, the upper bay under the bar left of the stem looks open on the right and below only if the crossbar extends far enough left, so that case is still uncertain.

I'm working out which bay detectors should fire for each digit, with the 9 and 8 cases still uncertain.

I'm now sorting the bay detectors by digit: 3 and 5 get bays on the left or right, 4 gets an upper bay, and 6 gets one on the right. I'm also noting that 9 and 8 lean on the hole feature, and the 2 has neither a bay nor a hole to lean on, so its absence needs to come through the bias terms.

I'm checking whether the far-cell test is too strict for thin strokes, since a 2-pixel stroke blurs its ink and narrows the background zone, leaving only about four clear pixels to fit a 2-pixel cell.

I'm now assigning per-class weights for the four background channels across the 16 pooled cells, starting with the hole and bay detectors and how strongly each should vote for a digit.

I'm working out where the hole feature for 9s and 8s should land in the conv2 rows: a 9's loop sits around row 11.6, which maps to the upper-middle group k=1, while an 8's upper loop falls around row 8.7, more into k=0.

I'm now placing the bay detectors' center rows into conv2 groups: the upper bay for 3s and 5s falls in k=0 or k=1, and the lower bay falls in k=2 or k=3.

I'm settling the split for the features: the upper bays and holes sit in k=0 and k=1, and the lower bays and the bottom loop sit in k=2 and k=3. Next I'll assign per-class weights to those groups.

Now I'm writing out the per-class weights for the hole feature across the four pooled row groups, with the upper groups mostly negative for most digits and the 6 and 8 getting positive weights in their loop rows.

Now I'm assigning the per-class weights for the bay detectors, with the lower bay boosting 3 and 5 and the upper bay boosting 3 while penalizing 5, and the 2, 9, 7 and the rest set to small or negative values.

I'm assigning the bay detector weights for the right-open shapes: a 5's upper right bay gets a strong positive weight, while its lower one is penalized. The 6's upper right bay gets a moderate positive, and the 3 is pushed negative across the board. The 2 gets mildly negative weights everywhere, since its bottom-right corner doesn't clearly open up or right.

I'm now checking the bay detector for a 2's lower-right corner: the diagonal stroke and bottom bar leave that area open to the right, so a lower right-open bay should fire for 2s. For the 7, I'm working out whether the stem's down-left slant leaves the space below-left of it open.

I'm assigning the bay detector weights for the upper-open case: 4 gets a strong positive weight in its upper rows, and I'm checking the remaining digits' bay weights, with 0 and 1 leaning negative.

I'm assigning the bay detector weights for the upper-open case, with the 2 getting a small positive value. Most other digits get negative weights, while the 4 and 9 get their own adjustments. For the bottom arcs of 3s and 5s, I'm checking that the open sides line up with the left bay.

I'm setting the background-channel weights for digit 0, giving its lower bottom-open region a positive value and its upper region a slight negative. I'll keep the other digits' bay weights mostly negative and leave the hole feature for 0 to be handled separately.

I'm settling on a moderate scale factor of about 1.0 for these weights, since the features are bounded and the bias shifts are large, so the effect will be decisive when the features fire but not overwhelming. The 3s should pick up some extra support from the bays, but the negative BayR weight for 3 and the upper-right penalty for 5 should keep the 5s from being pulled toward 3.

I'm settling the final bias shifts, with the 8 and 9 adjustments trimmed slightly since the hole features already help those digits, and the 3 bias pulled down a bit.

Still setting up the channel layout, with the endings reduced to just the left and right types.

Still defining the background and hole kernels for conv2, now starting on the bay detectors...

Still setting the bay channel weights in conv2, with the left, right, and upper detectors each keyed to their open side and penalized where that side is blocked.

I'm checking whether a 3's bay is actually open to the left: the right arc sits about four pixels to the right of that spot, and the bay's interior runs inside those bounds, so the left-open detector should fire there.

I'm checking whether the left-open bay for a 3 holds up at the far-left cell, since the starting hook of the 3 sits only about two pixels above that point and could break the background test.

I'm checking whether the left-open bay for a 3 still registers when the kernel center moves, since the 3's upper start hook sits close enough to that far-left cell to block the detector. I'm weighing whether shifting the center column would keep the right wall in range while leaving the left cell clear.

I'm weighing whether the hole detector can be made looser by only requiring the center to be background and the three other sides to be ink, which would let one feature cover both bays and holes. The worry is that a 3's upper bay, closed off by its hook, could then register as a hole and throw off the digit's detection.

I'm weighing whether a bay's mouth still reads as open at a 4-pixel test range, since the stroke zones narrow the gap to a few pixels of background that the edge test may or may not catch.

I'm weighing a conflict: min-pooling the open sides wants thick bands of background and ink, but detecting a narrow opening needs thin ones, so the dilation can't be pushed in both directions at once. I'm considering a looser detector that treats a bay as an enclosure missing one side, though that risks mistaking narrowed bays for holes.

I'm now checking whether max-pooling the raw ink values, which are already close to 1 on stroke cores, can stand in for the saturated ink test, so that a far cell counts as containing ink whenever any stroke pixel falls inside it.

I'm now weighing a softer version of the ink test: rather than requiring all four far cells to be fully saturated, I'd take a weighted sum and let the threshold absorb faint strokes, so the detector still fires when the strokes are lighter than full intensity.

I'm trying to get around the conflict between thick and thin bands by pooling the ink values instead. Since pixel intensities are already near 1 on stroke cores, a max-pooled ink channel could mark a far cell as containing ink whenever any stroke pixel falls inside it. The open question is how to combine the four far-cell checks so faint strokes still register without a hard all-or-nothing requirement.

I'm settling on the hole test as a single AND across the four sides: the center must be background and each side must show ink, with the ink terms summing so that one missing side drops the response to zero. Partial or faint sides still give a partial response, which is what I want. The open question is whether a 2x2 far-cell ink check is narrow enough to catch a 3-pixel-wide stroke passing through it.

I'm now looking at a tolerance issue with the ink cells, since a narrow 2x2 far-cell test only catches strokes at certain distances. I'm considering pre-dilating the ink channel so each far cell covers a wider band, though that could blur the open/closed distinction again.

I'm weighing a pooling trick to get a saturated ink signal, since raw pixel values near 1 on stroke cores might serve as the test without dilation. I'm also considering a second hole channel at a smaller radius to widen the tolerance for tiny loops.

I'm now checking whether the loop detectors need a second radius or an elliptical shape, since loops like the 9's and 6's vary in width and height and a single fixed-radius test might miss some of them.

I'm checking whether loops with narrow sides, like some 9s, still hit all four far cells, since a 2.5-pixel wall would fall outside the 3-to-5-pixel test range.

I'm considering whether a moderately dilated ink zone, with the threshold set so it covers the stroke plus about a pixel, could satisfy the all-four-sides requirement without the thick-versus-thin conflict. The concern is that a 5-pixel band would need the far cell to fit inside it at any alignment.

I'm weighing whether several hole detectors at different radii, each feeding the fully connected layer, could cover loops of varying width and height, since a single fixed test misses narrow ones.

I'm now considering whether several hole detectors at different cell sizes would cover loops of varying width and height. A pair of cells per direction, or a narrow-tall versus wide-short shape, might catch the 9s and 8s that a single fixed test misses, though the channel budget is tight.

I'm now deciding how many hole and bay detectors to keep, with eight structure channels in place of the endings: four hole sizes and four bay directions. The bays probably only need one scale, since a fixed center cell can sit four pixels from any wall.

I'm deciding whether to keep the four ending channels or swap them for more structure detectors, since loops and bays seem more useful than endings I haven't tested. The worry is that dropping endings could unbalance the classes, though the structure features should stay additive enough that false firings don't cause much harm.

I'm now weighing whether to drop the endings channels so that more structure detectors fit, or keep them to avoid shifting the class balance. I'm leaning toward keeping the endings and fitting four structure channels, with the bay detector for the upward direction competing for a slot.

I'm weighing whether a small hole detector would help with 9s, since it could catch loops the larger one misses. The bay-up detector might separate 4 from 9 in the other direction, so the two could be complementary. I'm still going back and forth on which of the two should take the last channel slot.

I'm thinking about dropping the endings channels down to a single offset each, which would free two conv2 slots for more structure detectors. Then I could fit six structure channels: three hole sizes, plus left, right, and up bay detectors. The endings would use a 4-row grid with the same kernel shape for rows and columns.

Writing the feature layout now...

I'm considering whether to amplify the ink values so that stroke pixels around 0.6 to 0.8 count as full ink, but a ReLU can't saturate, so I'll keep the ink channel as the identity. The background-smoothing channel with its center-weighted kernel stays as originally defined.

I'm defining the hole detector as a ReLU over the clear-background center plus the four ink sides, with weights chosen so that a fully closed loop reaches the threshold while a missing side pulls it to zero. Setting the bias around 4.6 makes three full sides plus a faint fourth still fire, but an open side does not.

I'm checking the hole detector's scaling: with weights of 1.25 and a bias of 4.75, a fully closed loop gives about 1.25, while a missing side drops it to nothing. Next I'm turning to the narrower Hole12 variant, where the side walls sit only one cell away from the center.

I'm checking whether the Hole12 detector can catch narrower loops than Hole22, since its side walls sit only one cell away from the center. The worry is that bare background cells flanked by ink on the left and right could also trigger it falsely.

I'm sketching the bay detectors next, with the left bay checking that the center is clear while the right, up, and down cells contain ink, and the two cells on the left must stay empty. I'm also keeping a smaller hole detector at one-cell spacing for tiny loops.

Writing the bay detector formulas now...

I'm working out the bay-up detector for the digit 0, checking how far its side walls sit from the center when the center is four pixels above the bottom stroke.

Now I'm setting the lower-zero bay case aside and turning to the class weights for the structure features, one table per feature and row, applied the same across columns.

I'm now assigning each expected loop or bay center to a pooled row, using the 4-pixel-wide bands: the 9's hole sits around row 11.6, which falls in the second band, while the 8's upper and lower holes land in the first and last bands.

Now I'm assigning the structure features to the pooled rows: the bay detectors for 3 and 5 go in rows 0 to 1 for the upper bays and rows 2 to 3 for the lower ones, and the 0's lower bay goes in rows 2 to 3 too. The 2's right bay goes in row 2, and the 6's right bay in row 0, since its top stroke sits above the center.

Now I'm filling in the weight table for the hole detectors, going class by class across the four row bands.

Writing the weight tables for the remaining structure features now...

Writing the bay-up weights now...

Still filling in the weight table, now working through the bay-up detector's values for each digit row by row.

Now I'm checking the bay detectors for the other digits, ruling out false firings for 4, 7, and 9, and then turning to whether the waist of the 8 could trigger the right and left bay detectors.

I'm checking whether the bay-up detector could fire on the waist of the 8, where the outline pinches inward on the right side at the crossing.

I'm checking whether the waist of the 8 could trigger the bay detectors on either side, since the outline there pinches inward at the crossing. If so, the 8 would pick up positive weight on BayL and BayR in the middle rows instead of a negative one.

I'm still settling the bay detectors for the 8's waist, where the outline pinches inward and might trigger the side-bay weights. I'm also checking how the 3's middle junction, with its inward-pointing arms, might or might not count as an enclosed bay on the right.

I'm weighing whether the arms of the 3's middle junction open far enough to count as a bay on the right, and they don't: at four pixels out the gap is only about two pixels, too narrow to fire. The 8's waist is borderline at roughly three pixels, so I'm leaving its side-bay weights near zero. Given how uncertain these bay detectors are, I'll scale all the structure weights down by 0.8.

Now I'm mapping the endings onto the pooled 4x4 grid, weighting each cell by how close it sits to its expected center, and then combining those with the orientation features.

Still computing the endings' coverage penalty and the normalization constant for the orientation and ending features.

Rebalancing the per-class biases, I'm settling on a few small adjustments after the computed values: nudging the 8 down, the 9 and 5 up slightly, and the 4 a touch lower. I'm also rechecking how the first convolution treats the ink channel under max-pooling, and confirming the indexing of the center-cell weight in the Hole22 detector.

I'm now checking the Hole11 detector, which would look for a single background cell with ink on all four sides, so it only catches very tight loops. The concern is whether it could also fire on narrow gaps between strokes, such as the acute angle inside a 4.

Still defining the bay detectors: the BayL one needs its center on, the cell to its right and the cells above and below it inked, and the two cells on the left kept empty, with a total bias around −3.5.

I'm checking the bay placement in the 3's upper bay, where the center cell needs both the up and down walls within about 3 to 5 pixels and the right wall 3 to 5 pixels away. Given the 2-pixel grid, I estimate it'll hold roughly 60% of the time, which I'll accept. The hook closure concern drops out too, as long as the nearby cells stay free of ink.

Checking the bay detector's open-cell penalty: the start stroke grazes the edge of the left probe cell, so I'll drop the open-cell weight to 1.5 each to soften that contribution.

Still working out the hole-detector weights: I'm weighting the three hole channels the same, but with the Hole11 variant at about 0.7 of the others, since it's less reliable. I'm also checking that when several hole detectors fire on the same loop, their contributions add up.

I'm weighing whether a loop of radius 3 would set off all three hole detectors at once, which would double-count it, so I'll scale the 22 and 12 channels down to 0.5 and the 11 channel to 0.35. I'm also keeping the bay weights at 0.8. Next I'm looking at a special case for the 2: the lower-left hole cells should carry zero weight for that class rather than a negative one, and I'm wondering whether a small loop at the bottom of a 2 could push the 6 and 8 scores upward.

I'm settling the hole-detector weights for the 6 and 8 at the lower rows, halving their left-column values since a small loop at the bottom of a 2 sits there, and I'm working out how the 6's loop center maps onto the grid.

Still writing the convolution kernels, the background-surround and ink channels, and the matching conv2 weight setup.

Still writing the bay detector weights, the BayR variant with its walls and open cells mirrored.

Still writing the bay detector weights for the BayR and BayU variants, with the walls and open cells set to match.

Still writing the template function: mapping the endings onto the 4x4 grid with a Gaussian-like falloff per cell, then assembling the FC weights by channel and index.

Still writing the structure table, with each hole and bay channel mapped to its weights, and I'm working out the normalization for the orientation and ending features.

Still writing the code: the structure table, with the hole and bay weights mapped per class and channel, and I'm scaling the bias and orientation values to match.

Still writing the template function, with the two strokes mapped onto the grid as before.
