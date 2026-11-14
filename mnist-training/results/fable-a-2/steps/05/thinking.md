I'm looking at the histogram for digit 1, and the bins show most samples sit between 0.9 and 1.1, with a smaller spread toward the lower end. So the V-crossing sum for a 1 typically lands around 0.9 to 1.

The amplitude checks out at about 1.0, so the weights aren't too small, and I'm now suspecting the cavity geometry or the inhibition strength instead. I'll recheck the kernel normalisation and the FC weight application next.

I'm checking the feature-detection part now: the cup walls need to sit about 7 px apart, and with a narrow position tolerance, a wall off by even a pixel or two drops the response a lot, which could explain why real 4s rarely trigger it.

I'm working through why the cavity detector doesn't fire on real 4s, and my estimate says the walls should drive a response near threshold. I'm now checking whether the centre inhibition, especially the upward rays, is suppressing it in the 7-pixel-wide cups.

I'm checking whether the diagonal filters respond to a vertical stroke two pixels away, since their far cells overlap the stroke while their negative regions pull the other way. I'm working out the column sums of the "/" filter to see whether its net response to a V-shaped wall is near zero.

I'm checking the diagonal filter's column sums: the centred V stroke gives about 0.25, and offsetting it by one pixel drops that to roughly 0.06, so the diagonal leak only reaches about one pixel. That rules out the filters as the reason the cavity detector misses real 4s, so I'm going back to the valid output region to make sure the cavity centres aren't falling outside the range where the detector can fire.

I'm checking whether the input side is off instead: the expected position of the 4's upper cup, around x = -0.08, maps to roughly pixel 12.5 once the shear and scale are applied, so I want to confirm the encoding lines up with that.

I'm checking the projected position for the 4's upper cup, where the pixel y lands near 10.7, and I'm mapping that onto the cell grid to see which cells should carry the most weight. The cell at row 1, column 1 picks up nearly full weight, so if the ∪ feature fired there it would add roughly 1.2 logits toward 4, though the 4-to-9 margin barely moved, so something else is likely absorbing that contribution.

I'm noticing that the hole detector seems to almost never fire on 8s, 9s, 6s, or 0s, since those rows barely change from the first pass. I want to check whether a ring of radius around 3.6 px with an empty centre can clear the 0.65 threshold on real loops, since loops in real digits rarely match that geometry exactly.

I'm now thinking the inner hole for 9s, 6s, and 8s may be only 2 to 4 px across, since the stroke is about 3 px thick. My earlier loop size of 8 to 9 px is probably too large for real MNIST digits. If the loop radius is nearer 1.5 cells, the walls fall between grid cells, so each one only partly activates the detector.

I'm checking whether the centre pool cell picks up ink from the walls when the loop is small, since a filter centred one pixel off could catch the stroke at a two-pixel offset.

I'm suspecting the ring's response on curved loops falls short of the threshold, since tight curvature and orientation mixing weaken the line-filter output to around 0.6 to 0.7 at best. That would mean the 0.65 threshold is too high for real loops, so lowering it is the next thing to test.

I'm weighing whether the sum-based threshold can tell apart three strong straight walls from four weaker curved ones, since a 4's cup could score higher than a real loop. That suggests the hole needs a different detection principle, so I'm considering more reliable linear templates instead of tuning the cavity detector further.

I'm now thinking about a different route: instead of tuning the cavity detector further, I could use probes to vote among candidate linear templates, each perturbed by a global parameter such as width scale, and compare which variant matches the data best.

I'm weighing a parallel version of the same search: each class gets its own perturbation per step, and I read the per-class recall changes as feedback, though the signals are confounded by the other templates changing too. That could mean tuning about three or four parameters per digit across the 46 steps, with gains that are uncertain but probably steady, perhaps from 62% toward 75%. The alternative is variant voting, where each step tests ten variants for one digit to see how the match scores are distributed.

I'm weighing variant voting against the parallel per-class search: the first would give mixture weights for each digit in 10 steps, the second tunes several parameters per digit at once but with confounded signals. Variant voting looks more promising, since the vote distribution over variants could approximate the class mean, though the choice of variants (width, bar height, and so on) would have to cover the real variation.

I'm weighing a more fundamental issue: whether my rendered templates actually match real digit features, since any mixture of them is only as good as the rendering model. Given the limited budget of about 46 steps, I'd rather spend calibration on the nonlinear structural detectors, which generalise across digits with few parameters.

I'm planning to calibrate the hole detector by looking at the histogram of its summed response per digit class, with the threshold set to zero, to see whether 0, 6, 8 and 9 separate from the rest. Each variant of the detector takes one step to test, so I can iterate until the classes split cleanly, and that would make about 10 to 15 steps for the ⊃, ⊂ and ∪ detectors before I combine them with the templates.

I'm planning to build a hole detector that checks for an empty centre ringed by ink on all four sides, using rays in each direction rather than fixed walls, so it can handle the small loops in real digits.

I'm considering whether the AND across the four directions can be made sharper by using the spare conv1 channels to produce a saturated ink indicator at the pixel level, since stroke cores already sit near 1 and that could keep the ray check from depending so heavily on amplitude.

I'm thinking about using the ink map itself as the saturated signal: a light blur of the raw image gives roughly uniform values near 1 on stroke cores, which should make the ray-based hole check less dependent on stroke amplitude. After 2x2 max-pooling, that gives a clean occupancy grid at about 2-pixel resolution, and each ~3-pixel stroke should cover one or two of those cells.

I'm working out how the occupancy map gets built: a 3x3 box blur over the ink, sharpened so only windows that are mostly ink fire, which should leave strokes about one or two pooled cells wide.

I'm settling on the occupancy map: a 3x3 blur with a sharpening threshold so a 3-pixel stroke comes out near 1 on its centre line and falls off to about 0.5 one pixel away. Max-pooling 2x2 then gives a thin, near-binary skeleton-like grid, though 2-pixel strokes only reach about 0.5 at their centre, which is weaker.

I'm settling on a center-weighted 3x3 kernel for the occupancy map, giving the centre the most weight and the corners the least, so a 3-pixel stroke centred in the window reads close to 1 while a 2-pixel stroke comes out weaker, around 0.8. I'm also checking how a stroke one pixel off the centre would respond, since that determines how wide the occupancy band ends up after pooling.

I'm checking whether an occupancy map built from a sharpened 3x3 blur is a better input for cavity detection than raw line filters, since its values should stay roughly uniform across curved and straight strokes. With a bias of about -0.3, a centred 3-pixel stroke reads near 0.7, a stroke one pixel off reads about 0.5, and anything further falls to zero, giving a roughly 3-pixel-wide occupancy band.

I'm thinking about a hole detector built on the occupancy map: a ring of cells around a centre that must be ink. The catch is that a fixed ring only fits loops of one size, since smaller loops put their ink at closer distances, so I'd need a check that works across loop sizes.

Thinking about the hole check: if the occupancy map is only one cell thick, each ray from the centre hits at most one ink cell, so a closed loop gives a clean count. Thick walls of two cells would push the ray sums past the threshold and produce false positives on open shapes.

The thought is about the wall thickness after pooling: a 3-pixel stroke spreads across two pooled cells, so a ray crossing it sums to about 1.5 rather than 1. That means the ray-based hole check only stays clean if the loop's inner radius is small enough for those walls to fall within the two-cell reach.

I'm switching to an "escape" detector that checks whether each direction from a point stays clear of ink, since a clear ray is a clean signal even when the walls are thick. The trouble is that max-pooling takes the maximum of these signals, while I need to know whether every ray is blocked, so I'm still working out how to express "blocked" as a positive output.

I'm working out a hole detector that is robust to thick walls: a linear check along each ray that sums the occupancy and subtracts a threshold, with the centre cell suppressed. The open question is how conv1 can give saturated directional signals before pooling, since a single ReLU in conv2 can't express "all four directions are blocked" on its own.

I'm now thinking about edge-style filters with polarity, where a detector fires when ink sits on one side and background on the other. Such an edge response should stay close to 1 across strokes of any thickness or curvature, since ink saturates and background stays at zero, which would be much steadier than line filters.

I'm now looking at edge-style filters with polarity: a detector that fires when ink sits on one side and background on the other. Using the four spare conv1 channels for these, the right-facing, left-facing, up-facing and down-facing edges would mark the inner walls of a cavity from the inside.

I'm checking whether edge filters with polarity would hold up better for the hole test, since each stroke's inner boundary gives a steady response. Along a ray, the sum over the wall should come to roughly one, though the two-cell reach may spread it a little.

I'm checking each direction's wall contribution for the hole detector: an inner edge gives roughly 1 to 1.5 per ray whatever the stroke thickness, so four walls should sum well above a threshold near 12, while three walls fall short.

I'm checking whether the per-direction wall contributions can be tightened so the four-way sum separates a closed loop from one with a missing wall. The spread of roughly 1 to 1.5 per ray is the real problem, so I'm looking at how to normalise the edge response more precisely after pooling.

Checking the edge response across an ideal step: the filter's values sum to a fixed total over the transition, so the pooled contribution per ray should stay close to 2 whether the edge is sharp or blurred.

The per-ray sums look well normalised as long as the whole edge transition falls inside the ray's cells and the stroke core sits near full intensity. That holds for holes whose inner radius lands roughly between 1.5 and 4.5 pixels from the centre.

I'm noting that a hole detector works for inner loops about 3 to 9 pixels wide, which covers most 6s, 8s and 9s. Zeros are the problem: their tall holes mean a centre point can't see both the top and bottom walls, so they'd look like a top arc, a bottom arc and a middle vertical pair rather than a hole.

Now I'm checking the hole test with the edge channels: if each direction's wall contributes close to 1 per ray, four walls should sum near 4, and a threshold around 3.4 separates a closed loop from one with a missing wall, though the margin is thin if some rays come in weak.

Now I'm settling the last cavity cases: a centre with three blocked directions and one open, where the open ray gets strong inhibition so it doesn't fire by accident. The "||" pattern for zeros would use left and right blocked with up and down open, which a lower threshold can catch.

Still enumerating the cavity states...

I'm settling on a "which rays are blocked" encoding for each background point: each of the four directions is either blocked by ink within about 5 pixels or open, giving the classic characteristic-loci style features. That means roughly eleven cavity-state channels plus the four orientation grids, with one channel still spare for something else. The remaining question is how to turn those per-position states into digit-specific weights for the fully connected layer.

Now I'm weighing whether ray-casting on my hand-drawn digit templates to set the expected cavity states counts as generating example inputs, or whether it's just geometry on a template I drew myself.

I'm weighing whether a ray-cast check on my hand-drawn template would count as running the network on generated inputs, and I'm leaning toward specifying the cavity positions by hand instead. Before building the full classifier, I want to confirm the detectors work, either by probing them on a few cases or by checking how the confusion matrix shifts once the classifier is trained.

Now I'm weighing whether a quick probe of the detectors, one output per cavity type with a dominant-type table across the digit classes, would confirm they behave as intended before I commit to the full classifier.

Now I'm working out the edge filters for the first four extra channels: a left-boundary detector whose positive side sits on the ink and whose negative side sits on the background, normalised so an ideal edge gives roughly 1.

Now I'm setting the weights for the first edge filter, with a column profile that tapers off toward the outer cells and a row profile that's heavier in the middle, then normalising so a straight edge centred on the filter gives a response of 1.

I'm working out the response profile of the edge filter as it slides across a boundary, checking how much it picks up when the stroke is one pixel wide versus three.

I'm tuning the edge filter so its response stays the same wherever the boundary falls relative to the pooling grid. The current profile gives pooled sums anywhere from about 0.9 to 1.6, depending on alignment, so I'm trying a narrower kernel profile that responds with only one position per edge.

Checking whether a response profile only one cell wide keeps the pooled sum steady: a 3-wide plateau always lands in exactly two pooling cells, so the total stays at 2 no matter where the edge falls.

Checking a one-pixel-wide edge filter: its response should only fire at the first ink column, so the pooled sum stays steady whatever the alignment.

Antialiasing spoils the one-cell edge response too: a half-intensity boundary pixel splits its response between two neighbouring positions, so the pooled sum swings between 0.5 and 1. I'm considering a saturating alternative, since the sum-based pooling is what's breaking the invariance.

Relying on inhibition for the open directions feels more robust than the sum thresholds, since any ink in a ray kills the response outright. So I'd define each cavity state as its set of clear rays, with only the blocked walls needing a looser sum check.

Now I'm considering whether a single positive requirement plus inhibition from the other rays would be more robust than summing three walls with a threshold, since the inhibition kills a state outright when ink shows up. That would mean checking each ordered pair of blocked and open directions, twelve combinations in all.

Now I'm checking whether a single positive requirement plus inhibition from the other rays holds up, pairing each blocked direction with an open one. On a 0 the centre's left and right walls both sit within reach, so a one-sided open-and-blocked feature won't fire there, which helps tell it apart from a 1.

I'm checking whether the features that pair an exposed wall with an open side fire mostly on the outer silhouette of each digit, which would make them encode shape more than interior structure. Something like an exposed-left boundary would light up along the outside of a 0 and inside the bowls of a 3, so the pattern is distinctive but also tied to edges.

I'm treating the right-side strokes as the key signal: a wall on the right with open space on its left should mark right-half features like the inner face of a 3's bowl. The mirror version, a wall on the left with open space on its right, would pick out left-half strokes.

I'm now weighing which few of the exposed-edge features would separate the confusable digits, starting with 4 versus 9, since their stems and loops overlap most.

I'm checking which exposed-edge features separate the confusable digits: one that fires when the top is open and the bottom is blocked should pick out the 4's cup against the closed loop of a 9, and left-blocked/right-open versus right-blocked/left-open should split 5 from 3 in the top half and 2 from 3 in the bottom.

I'm checking which features separate the remaining confusable pairs, like 7 versus 9 and 0 versus 6, by looking at where a wall is blocked and the opposite side stays open. I'm also weighing whether "both sides blocked" features for the hole in a loop would add enough separation to be worth including.

I'm settling on six robust features: four that fire when one side is blocked and the opposite side is open, and two that fire when both sides of an axis are blocked, with the threshold set at 2u so a single wall can't trigger them.

I'm settling on how to define the per-ray sum: whether the centre cell should count, and how much weight the lateral neighbours should get, so the wall signal stays robust when the edge sits right next to the point.

I'm settling the edge filter so the per-ray sum stays within about a factor of two: a wall's left boundary gives a ridge one or two cells wide, so summing two cells on each ray keeps the value roughly between 0.8 and 2.

I'm working out a narrower edge filter, with a response that fires on a single cell at the boundary, so the pooled sum stays between about 1 and 1.3 no matter where the antialiased edge falls.

Trying a centre-weighted edge filter that puts half its weight on the first ink column and a small negative on the cell before it, so a sharp edge fires on one position instead of two.

I'm settling on a narrow edge filter and accepting that the response to a soft antialiased boundary will be a bit weaker than to a sharp one. Perfect invariance isn't achievable here, so I'll rely on tolerant thresholds and the inhibition terms to carry the load.

Now I'm settling on a simple edge filter that weights the cells just past the boundary, with a small negative on the cell before, and a bias to keep background near zero. I'm also weighing whether ink occupancy along each ray would work instead, but stroke thickness makes that range too wide compared with edge responses, so edges look more reliable. The line-detector channels might still serve as an inhibition signal for the centre.

Now I'm writing out the four edge channels for the right, left, below and above directions, each a weighted sum over the pooled cells, with a small negative bias to keep background near zero.

Now I'm working through the edge response values for a thin stroke, checking how a vertical edge and a diagonal edge each respond to the filter.

I'm weighing whether the centre cell belongs in the ray sum, since a wall that close would make it unclear whether the point is really background. I'm leaning toward lateral weights of 0.25, 0.5, 0.25 so curved walls are smoothed, but I'm still undecided about including the centre column.

I'm settling the ray sum to cover only the outer two columns, since the centre cell is too ambiguous to count as evidence either way. The centre is ruled out by line-detector activity instead, which catches a stroke passing straight through the point. For the open-ray inhibition on the left, I'm weighing which signals should suppress it: every line channel, plus both horizontal edge polarities, since a stroke to the left would show its boundary there.

Still writing feature definitions...

Still working out the thresholds: I'm setting the ReLU cutoff at 1.9 so that a single wall can't trigger the both-sides feature, while a real double wall clears it most of the time.

I'm comparing a position-resolved probe on one feature channel, where each of ten output cells tracks a location, against the simpler total-over-cells probe, which doesn't tell me much for a digit like 1 where the left and right features fire equally.

I'm planning to skip hand-setting the classifier weights and instead derive the expected feature maps from the digit geometry: for each candidate centre on a lattice, I'd test whether a stroke blocks the right ray within a set distance, whether the left ray stays open, and whether the centre itself is empty.

I'm now weighing whether a hand-drawn prototype per digit counts as a template or as generating example inputs to derive weights from, since the rules bar synthetic examples but allow stroke-based templates.

I'm now thinking about whether to hand-specify expected feature regions as line segments per digit, rather than deriving them by geometric ray-casting, to stay clearly on the safe side of the rules.

Now I'm writing out the expected feature regions for each digit by hand, describing where each cavity signal should appear, with a reach of roughly 0.11 to 0.34 units on either side of the empty point.

I'm now sketching the expected cavity regions for digit 0 as an ellipse, placing the feature segments about 0.2 units inside each wall so the reach band lands where the features should fire.

Now I'm working out the expected cavity regions for digit 0: inside the loop, a vertical line of points along the centre should register strongly on the both-sides feature, since the walls sit about 4 pixels away on each side.

Now I'm checking which outer-silhouette features land inside the usable centre range, which for the 0 falls just outside it on the left. For a narrow digit like the 1, the points beside the stroke do fall in range, so I'll keep those.

Now I'm placing the expected cavity regions for digit 1: one feature segment sits just left of the stroke and another just right, each running the full height of the digit.

Now I'm working through the expected cavity signals for digit 2, starting with the hook under the top arc, where the ceiling above and the right wall should both register while the left side stays open.

I'm placing the expected regions for digit 2 under the hook, where the ceiling and right wall block one side and the left stays open. I'm also checking the lower-right wedge, where the base and diagonal should both register.

Now I'm checking the remaining digit 2 cases: a point just above the base on the right side should see the hook's lower end as far enough away to leave the upward ray open, so it registers as a downward-facing feature.

Now I'm placing the digit 3's upper and lower bowls, where the right walls and the inner top and bottom boundaries of each bowl fall within reach of the same points.

Still writing feature definitions...

I'm marking where the ray-sum features should fire for digit 4: a cup region inside the left and right strokes above the bar, where the bar blocks the downward ray, and a lower-left region beside the stem, where the stem blocks the right side.

Now I'm working through the digit 5 case, starting with the top bar and the bowl beneath it.

Now I'm checking the upper cavity of the 5, where the left stroke and the bowl's top and the top bar all block the nearby points, leaving only the right side open.

Now I'm checking the digit 6's upper section: just right of the curve, the left side is blocked by the stroke while the right stays open.

Now I'm checking the upper part of the 6: the stroke on the left blocks that side while the right stays open, so a vertical line just right of the curve should register strongly on the right-open feature. Inside the loop, the walls on both sides and the top and bottom all sit close enough to block, so the centre should fire the both-sides and both-ends features.

Still writing feature regions for digit 7...

Now I'm checking the digit 7's left-of-diagonal region and the open space to its right, then moving on to the 8.

Now I'm checking the upper loop of the 8 for the left side of the waist, where the crossing blocks the right and the left stays open, and the right-side notch for the opposite pattern.

Still writing the digit 9 feature regions...

Now I'm checking the right-hand side of the stem for digit 9, where the upper part of the loop is still in reach.

Now I'm settling how to combine the samples: taking the maximum per cell rather than the sum, scaled by weight, so each cell's signal stays in the range 0 to 1. Then I'll weight the feature contributions with a gain of about 1, since the magnitudes look like they fall around 0.5 to 1.5.

I'm settling on how to normalise the cavity template: I'll scale each digit's expected-feature map to unit norm so that digits with many expected regions don't get an advantage. Then I'll apply a gain to keep the cavity contribution comparable to the orientation term.

I'm settling on a normalisation for the cavity template: scaling it to unit norm like the orientation term, with a matching gain so the two groups contribute about equally.

Now I'm defining the blocked-direction sums over the pooled ink channels, with the right, left, below and above walls each sampled at the offsets that sit just beyond the centre cell.

Now I'm checking the cell just right of the centre: ink starting within the centre cell's own span would make it part of the stroke rather than background, so I'll leave that case out. The centre cell's line channels need an inhibition term too, since they should stay quiet when the middle is empty.

Now I'm settling the inhibition terms: the line channels at the centre cell get a penalty to keep them quiet when the middle is empty, though thick strokes only partly respond there, so the penalty stays moderate. I'm also weighing whether a wall detected right at the centre cell should count, since the point would then sit against ink rather than in open space.

I'm settling the inhibition for the left-open case: the centre cell and its neighbours on the left need penalties across the line and edge channels, since any ink there would mean the point isn't in open space. The stroke's left and right edges both light up along the left ray, so I'm treating those as part of the same suppression.

Now I'm settling the inhibition for the both-blocked case: the centre cell gets penalties on the four line channels to keep it quiet when the middle is empty. I'm not yet sure the left and right edge channels alone ensure the point sits between two walls, since a single thick stroke might trigger both.

I'm settling on the two-wall case: the "both blocked" feature should need a wall on each side, and each wall's response is a pooled edge value minus a small bias. Averaging across antialiased profiles, the contributions from each wall land around 0.9 to 1.1, so the threshold has to sit above a single wall's contribution but below two full walls.

Now I'm checking the wall strength: a single thick stroke's edge profile pools to a wall response of roughly 1.1 to 1.8 per side, with about 1.5 typical, so the two-wall threshold needs to sit between those values.

I'm settling the two-wall threshold at 1.8, since a single strong wall contributes up to about 2.0 and a real double wall typically reaches about 3.0. For the single-wall case I'm setting the right-open threshold at 0.4, which keeps a typical 1.5 response comfortably above it. I'll then normalise the outputs so they stay around one.

I'm checking the edge-based features for digit 1's right-open and left-open cases, and noting that the wall responses may also fire on outer boundaries of wide digits like 0 and 3, which the templates don't model.

Now I'm setting up the feature templates for the cavity channels, mapping each digit's expected features to their response channels and weights.

Still writing the cavity template entries for the digits...

Still writing the cavity template entries for digit 4...

Still writing the cavity template entries for digit 7...

Still writing the digit 9 cavity template entries...

Still writing the cavity template entries for digit 9...

Writing the cavity template entries and the conv kernel code now...

Still writing the convolution blocking code...

Still writing the convolution blocking code...

Still checking the horizontal-stroke response of the right-edge filter...

Still writing the convolution blocking code...
