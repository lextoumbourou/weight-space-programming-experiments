The forbidden strokes are hurting more than helping: the 3s dropped to 6 correct, and the 0s fell to 260. The trouble seems to be that real digits have ink in the areas I'm forbidding, and the wide footprint means the centre exclusion overlaps the sides of the 0s.

The forbidden strokes are backfiring: the cells are too coarse, so the negative strokes bleed into the positive ones, and the classes without them (8 and 1) end up winning. Lowering λ to 0.8 at this resolution clearly hurts, though 4, 1 and 9 did improve. Before changing anything else, I want to know the real per-class feature statistics, and I'm wondering whether the feedback can be used to probe them directly, since the aggregate confusion matrix might reveal more than I'm assuming.

I'm considering whether the feedback could be used to probe the real per-class feature statistics, for example by designing hand-picked features so the confusion matrix reveals which one dominates each class. That would be slow, but it could calibrate things like stroke positions. I'm also weighing whether to instead make the features more robust, drawing on what I know of typical MNIST digit shapes, since the template approach only reached about 61%.

I'm thinking about moving the feature design down to the conv2 layer, where the 5x5 kernels work at 2-pixel resolution, so each channel can act as a part detector with inhibitory regions and ReLU combining presence and absence. Those part detectors would then be max-pooled into the 4x4 grid and combined by the FC layer.

I'm sketching a set of conv2 part detectors instead: closed loops, cups, C-shapes, corners, an isolated vertical bar, crossings and T-junctions, each one a specific stroke arrangement with inhibitory regions and a threshold. Max-pooling those into the 4x4 grid and letting the FC layer combine them by position should give far more discriminative features than the template approach.

I'm sketching out a mapping from each digit to a set of part detectors: for 3, an open bracket at the top and another at the bottom, for 0 a large top arch, bottom cup and side brackets, and so on down the list.

I'm sketching the detectors at the pool1 scale, using 5x5 cells spaced 2 px apart. For a "⊃" shape that opens to the left, I'd want a vertical stroke on the right, horizontal strokes at the top and bottom, and an empty left column with an empty centre. The cavity in the upper bowl of a 3 is roughly 9 px wide and 8 px tall, which sets the size I need to cover.

I'm sketching each detector as a pattern over the 5x5 pool1 cells: positive weights where the stroke should be, negative weights on the cavity, then a bias to suppress partial matches. The cavity scale works out so that a 5x5 window covers roughly one lobe of a digit.

I'm weighing whether the detectors can be made fuzzy enough to tolerate a one-cell shift in stroke position, since a rigid pattern would miss real digits with slightly different placement.

I'm working out where the part detectors can actually sit on the grid: the final 4x4 cells map to conv2 outputs, which put kernel centres at roughly 7.5, 11.5, 15.5 and 19.5 px, so a part can only be placed within about 6.5 to 20.5 px.

I'm weighing whether the structural approach is worth the extra design rounds, since pure templates seem to cap out around 60–65%. A cheaper route would be to revert to the step-1 setup and add compression and gains, maybe reaching 65–70%, though the structural route could plausibly reach 80–90%.

I'm asking whether probing the data with hand-built outputs counts as a legitimate use of the feedback, or whether it drifts away from what the task intends.

I'm weighing whether to keep refining the part-detector idea or to settle for a simpler, more robust feature set. The template approach has plateaued, so the structural route looks more promising despite being geometry-sensitive.

I'm listing which digits contain each kind of cavity: open-left for 3, 2, 7, 9 and 5, open-right for 5, 6 and 2, an open-top cup for 4, and I was starting on open-bottom shapes for 7.

I'm listing which digits have each kind of closed or open shape: the 0 has a central hole, the 1 has none, and the 2 has an open-left top and open-right bottom. The 3 has open-left shapes at both top and bottom, while the 4 has an open-top cup. The 5 and 6 have open-right top shapes, and I'm still mapping the bottoms of the 6, 7, 8 and 9.

I'm sketching the part detectors as oriented conv2 kernels: a "⊃" detector wants ink on its top, bottom and right walls, with negative weights on its centre and left column, and a threshold on the sum. The open question is whether a simple sum of wall presences works, since a wall that is present only partly, or a stroke that covers several cells, could overwhelm the threshold.

I'm checking whether a single wall-sum threshold can separate a true open-left cavity from corner shapes, since a strong top wall plus a strong right wall would already clear a loose threshold. Capping each wall's weight should keep one long stroke from pushing the sum over the line.

I'm tuning the wall-sum threshold so that a full ⊃ scores well above a corner, with caps on each wall's weight to stop bold strokes from tipping corners over. I'm also considering a decomposed alternative, where each direction's "bounded" feature is a ReLU of the ink above or beside a point minus the ink at its centre, which would let the linear layer combine them more robustly than a hard AND.

I'm settling on five conv2 cavity channels, for open-left, open-right, open-top, open-bottom and closed holes. The hole detector needs a larger ring to cover the 0's interior, so I'm considering a version with left and right walls only.

Next I'm treating the 0 with its own detector: two vertical walls about 4–5 px apart with an empty centre column. That pattern also shows up in other digits, but a 0 puts it at the centre of the image, so the fully connected layer can tell them apart by position.

I'm settling on five wall-based cavity detectors, with each one requiring some walls present and one forbidden. The last one, a line-pair for the 0, is questionable because the hole detector and the open-top and open-bottom ones may already cover it partly, and I'm unsure whether the 0's centre empty column fires any of them.

I'm planning to design the cavity detectors directly on the 5x5 pool1 grid, with the wall-and-centre pattern for each cavity type.

I'm working out the size of the cavity kernels on the 5x5 pool1 grid, where each cell covers about 2 px. A wall sitting one cell from the centre would leave the cavity centre only partly empty, since the stroke's ink reaches close to it, so the walls probably need to sit at two-cell distance.

I'm sizing the cavity kernels on the 5x5 pool1 grid, where the walls might sit at ring distance 1 or 2 cells from the centre, so I'm considering spreading the top-wall weight across rows 0 and 1 to tolerate a slightly larger or smaller cavity.

I'm sizing the cavity walls against each digit's actual lobe heights: the 9's loop is about 9.5 px tall and 8.4 px wide, the 3's bowl is close to 8.75 px, and the 5's upper cavity is nearer 6.6 px, so a single wall distance won't fit them all.

I'm sizing the cavity walls against the digits' actual extents, which run from about 6.6 px for the 5's upper bowl up to roughly 9.5 px for the 9's loop and 17.5 px for the 0. Walls at 5 px sit past the last kernel cell centre, so I'm checking how pool1 positions at that distance get sampled.

I'm checking whether cavity walls at up to 5 px from the centre can fit the tallest loops, since a 5x5 kernel only reaches about 4 cells, or 8 px, plus a pooling slack of about 1 px. The 9's loop and the 0 are taller than that, so they won't fit fully, and the 3's bowl sits right at the limit, meaning real 3s with slightly taller bowls would be missed. I'm considering placing the detector off-centre toward the wall that is present, so the reach is spent where the ink actually is.

I'm switching to a curvature detector instead of a full cavity: a right-facing arc built from a top-right "\" stroke, a right-side vertical, and a bottom-right "/" stroke, with the centre and left left empty. That fits inside the 5x5 window without needing to span the whole bowl, and it would separate ")" arcs like the 3's and 2's from "(" arcs like the 6's.

I'm comparing the arc detectors' logits against the cavity ones: a ")" on top should favour 3 over the "(" that a 6 or 9 loop also produces. Since the 9's loop shows both arcs at the same height, an arc alone won't settle it, so the linear layer will need the open-versus-closed distinction as well.

I'm weighing whether to build the cavity detectors with walls at fixed distances, since real digits have lobes anywhere from about 6 to 10 px tall and a 5x5 kernel only reaches about 8 px. Curvature detectors for the arcs fit the window better, but they don't separate open from closed shapes the way a cavity does. The real gain from the cavity design is that the forbidden walls are placed relative to the detected structure, so they don't depend on absolute position.

I'm considering a right-facing arc detector for the 0's right side, looking for a ")" stroke with nothing in the centre or left. The trouble is that a wide 0 has its left wall beyond the window, so this detector would still fire on the 0 and fail to separate it.

I'm now sketching a ⊃-shaped detector for the conv2 kernel: positive weight on the right-side vertical stroke in the middle rows, with the centre and left columns kept empty. The 0 would trigger it on its right side, and a 3's upper and lower right curves would too, so the linear layer has to rely on the position of the firing to tell them apart.

I'm sketching the right-facing arc detector: a top-right "\" stroke, a right-side vertical, and a bottom-right "/" stroke, with the left and centre kept empty. I'm checking how the 9 fits this: its loop's left wall inhibits the arc, but the stem's right side and the loop's bottom still give a partial right-facing response lower down.

I'm reconsidering whether a full cavity is needed, since the walls would have to span up to 9–10 px and the 5x5 window only reaches about 8. A right-facing arc detector, with a right-side stroke and emptiness on the left and centre, fits inside the window and separates the 3's and 0's right sides from the 6's left ones. A single vertical stroke would be too weak a signal, so the detector should need at least one closing curve at the top or bottom too.

I'm going to revert to the step-1 baseline, since the forbidden strokes clearly hurt, and then add the new features on top of it. That way I can see what each change actually contributes.

I'm now turning to the classifier weights for the cavity features: each digit gets positive weight on the cavity types it should contain at the right positions, and I'm weighing whether to also add small negative weights for cavity types it should never have, like an open-right bowl for a 3.

I'm scaling the cavity contributions as a group, so each expected cavity adds a few logit units to its digit's score. Because a cavity's response can spill into neighbouring cells after pooling, I'm estimating how much of the footprint actually lands on the kernel to set that gain.

I'm weighing whether penalising unexpected cavities adds anything, since a 4 gets its gain from the ∪ at the top while the 9 gets nothing from that position. The exclusivity between detectors seems to rest on the forbidden walls doing their job, so I'll plan the kernel geometry with that in mind.

Next I'm defining the wall positions for a "hole" detector in cell units, with the loop's half-size around 2 cells, and blurring them slightly so a small shift still registers.

I'm settling on a concrete kernel design: the positive part is a ring of radius about 2 cells, deposited as an arc, and the negative part is a blob in the centre, with the corners left out since they sit too far out. Without a way to run it, I'll scale the response so a matching real pattern gives a moderate activation, roughly proportional to the normalised kernel.

I'm setting the weights for each detector: the positive kernel is normalised so a perfect match gives about 1, with a bias around -0.5 so partial matches of roughly three walls out of four still pass. The negative parts get a smaller scale, around 1 to 1.5, so a forbidden stroke pulls the response down.

I'm raising the threshold to about 0.7 so a full hole scores around 0.3 while a three-wall partial drops to about 0.05, though that makes the detector more sensitive to faint or thin strokes.

I'm now checking whether the three-wall detectors can separate a full hole from partial matches: a hole should push each open-side detector's response down, since the forbidden wall on the missing side would contribute a strong negative term.

I'm checking whether the amplitude sensitivity breaks the scheme: the threshold that separates a full hole from a three-wall partial depends on stroke strength, and real MNIST strokes vary a lot in intensity and width, so a fixed θ could miss faint or thick digits.

I'm weighing a simpler option: a ")"-shaped detector whose right arc is the required part, with small positive weights on the top and bottom and negative weights on the left wall and the centre. That should let the classifier fire on the bowls of 3s and the top of 2s, with a low threshold so a strong right arc is enough to trigger it.

I'm settling on a set of arc detectors, each defined by which side it opens toward, starting with a ")" detector that needs a strong right-side arc and tolerates a few top or bottom hits. Straight strokes, like a 1's stem or a 7's diagonal, should only match the middle of that arc and fall below threshold, while the loops of 9s get suppressed by their left walls.

I'm checking the left-facing "(" detector next: it would fire on 6's upper-left curve, while a corner shape like ┌ only matches part of it, since its top bar and left stroke each cover just a fraction of the arc.

I'm sketching the C-shaped detector as a rounded path: a top bar running from the centre to the left, a curved corner down to a left vertical wall, and a matching bottom bar, so the left-opening shape of a 5's upper bowl is covered by the deposited strokes.

I'm setting the C-shaped detector's weights: the left wall gets full weight and the top and bottom bars get a bit less, so a real 5's top bar and the 6's upper curve should both land on it. For the 0's left side, the far top and bottom walls drop out, and the right wall sits too far away to matter.

I'm checking how the "⊂" kernel responds to the other digits: a 0 only hits the left wall, so it scores about 0.45 and stays under the 0.5 threshold. A 1's vertical stroke and a 4's stem produce the same partial response and stay off. For a 7, the top bar and the diagonal on the right would match the "⊃" kernel's top and right arcs, which is the case I still need to settle.

I'm checking whether a "top and bottom bar without a side wall" pattern, like a 5's top bar over its bowl, would fool the right-opening detector, and whether the left-side inhibition would cover it.

I'm checking whether a normalised kernel will give a response near 1 on a clean pattern, though real strokes are sharper than the blurred template, so the centre-line cell carries most of the weight.

I'm checking how the stroke profile spreads across pooled cells: the centre cell carries most of the response, with neighbouring cells picking up only a fraction of it, and the filter's negative lobes cut off anything two pixels away. Real digit strokes are more concentrated than my blurred template, so that centre-line weight matters most.

I'm estimating the response from the blurred kernel: with a line of cells at a small offset from the template, the normalised weight comes out a little above one, and the across-stroke spread adds roughly a quarter more.

I'm working out the kernel's half-size: walls at ±2 cells would be about 8 px apart, and with real cavities varying in width, that spacing is the main thing to check.

I'm checking whether the wide kernel walls would fall outside the window for larger cavities, so I'm considering shifting the detector centre toward the main wall. Typical 3 bowls are around 8.75 px apart, which sits right at the edge of a ±2-cell kernel, and with blur it should still give a decent weight.

I'm setting the wall positions for the kernel: the right and left walls sit at ±1.8 cells, with the top and bottom walls at the same spacing, and I'm blurring with σ=0.7. Edge cells at ±2 keep most of their weight, while the next cells inward drop to about half, so I'll weight the outer rows at 1 and the inner ones at 0.5. Next I'll write out each kernel's strokes in cell coordinates, starting with the right wall.

Still writing the kernel definitions...

Still working out the inhibition weights and the open-side extents for the remaining arc kernels...

I'm settling the inhibition weights next: each wall crossing the inhibit region should cancel the response, so I'm spreading a negative weight across those cells, and I'm checking whether a separate centre penalty is needed to stop a cavity from being detected right at the crossing point.

I'm placing the upward-facing "∪" detector's inhibition across the top row, so the side walls of a 4 can't be mistaken for an open cavity. The inhibition weights sit on the middle columns and ignore the corner cells that only partly overlap the walls.

I'm weighing whether a top closure above the centre column would be visible at the lower detection position, since the ∪ kernel's inhibition would only cover cells in that one column.

I'm checking whether the upward-opening "∪" detector would fire inside the taller loops of 9s and 8s, since its cap-blocking inhibition only reaches a few pixels above the centre. A 9's loop is close to the edge of that reach, so I'm weighing whether a centre placed near the loop bottom would still see the top closure.

I'm checking whether a tall 9's loop would still be detected by the ∪ kernel, since its top closure sits just beyond the reach of the inhibition row. The 5x5 window looks too small for the taller loops, so the hole detector misses the top closure there. I'm considering whether a ∩ detector centred nearer the top of the loop could catch the closure instead.

Still working out the 9's loop: its top closure sits just outside the reach of the ∪ detector, so the ∩ detector and the hole detector have to cover it instead.

Checking whether a 0 triggers any of the cavity detectors: its top and bottom arcs are wider than the kernel reaches, so the ∩ and ∪ responses stay partial, and the side walls alone fall below threshold. That leaves 0 with no firing cavity feature, so it has to rely on the orientation template and the absence of cavities instead. I'm weighing whether a dedicated centre-hole detector would help separate 0s from the rest.

I'm weighing whether a 0 would trigger any of the cavity detectors. Its inner width is too wide for the kernels to reach the side walls, so nothing fires for it, and I'm deciding whether to assign 0 no cavity weights at all.

I'm setting up the cavity detectors for the remaining digits: the 2 gets a top-opening ⊃ and a bottom ⊂, and the 3 gets two ⊃ detectors, one near the top and one near the bottom. For the 4, I'm placing a ∪ detector at the top, centred between the strokes.

I'm now assigning the cavity detectors per digit: the 5 gets a top ⊂ and a bottom ⊃, and the 6 gets a top ⊂ just right of its left curve, above the loop.

Now I'm assigning the remaining cavity detectors: the 7 gets a top-opening ⊃ and maybe a ∩, and the 8 gets a hole at the top and another at the bottom. For the 9, I'm placing a hole at the top, a ∩ there too, and a partial ⊃ lower down on the stem. I'm also setting negative weights so that 4s are penalised for ∩ and top holes, and 3s for any ⊂.

I'm settling the cavity detectors: a baseline negative on every cavity feature would cancel out in the softmax, so I'm dropping that idea. What matters is only the specific strong negatives, like penalising 4s for a top ∩ or a top hole.

Now I'm weighing whether to give the 0s and 1s a positive bias, since they have no cavity features to earn points from and could otherwise lose to digits that get bonuses on stray cavity hits.

I'm weighing whether a positive weight on each cavity feature is enough, since the 0s and 1s have no expected cavities to gain from. A cavity response of roughly 0.25 to 0.5 needs a large gain to matter, so I'm considering γ=4, though spurious firings could then cost more than they help.

I'm settling on the base templates: I'll keep the step-1 versions so the cavity features can be measured on their own, though I'd like to keep the improved "1" variants if they don't confound the comparison.

Now I'm fixing the base to step 1 exactly, so I can measure the cavity features on their own. The channel layout stays as before: grid A in channels 0–3, grid B in 4–7, and the five cavity types in 8–12. I'm writing the kernel builder next, depositing each mini-stroke as a Gaussian-weighted contribution across the cells for each orientation.

Now I'm weighing how to normalise the kernel weights, so that a well-placed response comes out near 1: I'll scale each kernel's deposited contribution by the sum of its products with the ideal response.

I'm still weighing how to normalise the kernel weights without running anything on images. Rather than matching against an idealised pattern, I'm leaning toward a closed-form scale: dividing each kernel by its total deposited mass along the line, so a well-placed response lands near 1.

I'm working out the normalisation for the kernel weights: each stroke piece contributes a response proportional to its length and its deposit weight, so the raw total is a weighted sum over the pieces of the path. I'll scale the kernels by that closed-form total so a well-placed response lands near 1, without running anything on images.

I'm settling the normalisation: I'll divide each kernel by a closed-form total of its weighted stroke length, about 1.17 times the sum of weight times length, so a well-placed response lands near 1. Edge cells at the kernel boundary still keep most of their Gaussian weight, so the pooled response at the edge holds up.

I'm now setting the inhibition weights: every channel gets the same negative value per cell, about −0.4 on the wall regions and −0.6 at the centre. A real ink cell also leaks into the other channels, so I'm checking that the total ink response still holds up with the equal split.

Now I'm checking whether the 3's upper hook start falls into the inhibition zone on the left, since its top-left end sits roughly one row down and at the edge column. That would mean a genuine stroke partly suppresses its own cavity detector, so I need to judge how much the inhibition weight there should be.

I'm restricting the inhibition to the ray cells: (row 2, cols 0 and 1) plus the centre, each at about −0.6. That way a real upper hook that drifts down the left side won't suppress its own detector, while a wall that crosses the ray still shows up as a strong negative.

Now I'm working out which cells the inhibition should cover for the ⊃ detector, since its top and bottom walls might leak into the same row.

Now I'm checking how a partially shifted ⊃ detector would respond: its right wall picks up about half strength while the left wall falls out of reach, so the detector would still fire weakly on a hole that sits slightly off-centre.

I'm settling the inhibition for the ⊃ detector so that it stays quiet when a left wall is present. The cells along the leftward ray carry the strong negative weights, and the detector's threshold goes up to 0.6 so that off-centre loops only produce weak responses. I'll accept some leakage and test it, falling back to another approach if the results don't hold.

I'm settling the cavity-detector thresholds at 0.65 for the hole and 0.55 for the others. Next I need to map each expected cavity position into the pooled grid, using the digit's transform, then weight nearby cells with a footprint that falls off to zero by about 5 px.

Now I'm listing the cavity positions for each digit in its own coordinates, shifting x a little to match the shear, and looking at which ones should count as expected.

Now I'm listing the expected cavity positions for the remaining digits, with the 3s and 5s using the mirrored bowl openings, and weighting each one with a footprint that falls off within a few pixels.

Now I'm listing the expected cavity positions for the 6, the hole at its lower loop, and the 8 and 9 loops at their top and bottom, each with a weight and footprint in the pooled grid.

Next I'm writing the kernel builder, so each mini-stroke is deposited as a Gaussian-weighted contribution across the grid for its orientation.

Still writing the kernel builder...

Now I'm working out the kernel normalisation: the raw response is the sum over the cells of the stroke's deposited weights, so dividing by the total weighted length of the stroke, with a small allowance for leakage into neighbouring cells, should bring a well-placed response close to 1.

Still writing the kernel geometry...

Still writing the kernel geometry...

Still writing the kernel geometry...

Still writing the kernel geometry...

Still writing the kernel geometry...

Checking whether the 3's upper hook lands in the row-2 inhibition cells: its start sits about 8.8 px left of the right wall, well outside the ray, so it shouldn't suppress the cavity detector.

Checking the inhibition placement for the 5 and 2 detectors: the lower bowl's tail and upper start both sit outside row 2, so they shouldn't suppress the cavity detector. Now settling the bias values, with the hole detector at −0.65 and the rest at −0.55, and the orientation spec still to work out.

Still writing the kernel geometry...

Still writing the kernel geometry...

Still writing the kernel cavity code...

Still writing the kernel cavity code...

Still writing the kernel cavity code...

Still writing the cavity piece definitions...

Still writing the cavity kernel code...
