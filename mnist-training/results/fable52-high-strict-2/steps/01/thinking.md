I'm sketching a hand-built CNN for MNIST and want a layout that should still reach decent accuracy. The first layer would use eight oriented stroke and edge detectors, pooled down to 12x12 maps, and the second layer a 5x5 convolution followed by pooling to 4x4.

I'm checking the receptive field math: each final 4x4 pooled cell would span about 16 pixels, with neighboring cells overlapping heavily. That's too coarse with a uniform conv2 kernel, so I'm considering making the conv2 filter focus on its center weights instead.

I'm working out where the pooled cells land in pixel space when conv2 only uses its center weights: the first cell spans roughly rows 4 to 11, and each later cell shifts by four rows. The centers come out near 7.5, 11.5, 15.5, and 19.5, which sit a bit off the image midpoint of 13.5, so I'm checking whether that asymmetry matters.

I'm checking the cell centres against the image midpoint and they come out symmetric, at offsets of -6, -2, +2, and +6 from the centre. That means a 4x4 grid of overlapping 8x8 regions with stride 4 covers the digit area. With 16 channels over 16 cells, I'd have 256 features to hand-design digit templates from, which I'd guess reaches roughly 70 to 90 percent accuracy, to be tuned later with confusion-matrix feedback. I'm also wondering whether conv2 could use different kernel offsets to get finer positional detail.

I'm weighing whether conv2 could use different kernel offsets so that the pooled cells land on shifted grids, which would give finer positional detail. Working through the arithmetic, shifting the kernel anchor by a moves the cell starts to 4i+2a, so an offset of 2 would tile the digit area differently from the centred grid.

I'm checking whether using a=1 and a=3 offsets would interleave two grids so the pooled windows start at 2, 6, 10, 14 and 6, 10, 14, 18, which would give a finer effective stride but also duplicate some positions.

I'm comparing offsets for the conv2 kernel anchor: a=2 gives pooled windows starting at 4, 8, 12, 16, and a=3 gives 6, 10, 14, 18, so I'm checking which pairing actually produces a finer grid without redundant positions. I'm also weighing a=1 with centres at 5.5, 9.5, 13.5, 17.5, since interleaving it with a=2 would tile the digit area more evenly.

I'm weighing whether a linear classifier over pooled oriented features could beat hand-drawn templates on raw pixels, and estimating that such a design might reach roughly 80 to 90 percent accuracy. I'm planning to design the digit templates carefully, since I can't run the code to check them.

I'm now fixing the first layer: eight 5x5 filters, with bar detectors built from a centre line flanked by negative weights so each one responds to strokes at a particular orientation.

I'm checking whether bar detectors with a zero-sum row profile stay silent on orthogonal strokes and uniform regions, which they do, and giving partial responses at line ends. I'm also planning the other four first-layer filters as edge detectors with odd symmetry, so they can tell which side of a stroke is bright.

I'm thinking about what the other four first-layer filters could do instead of duplicating the bar detectors. One option is an all-positive blurred ink channel that captures raw density in each region, which would help with cases like an empty centre for a 0. Another option is endpoint detectors that respond to where strokes stop in a given direction, since endings like the left-pointing tips of a 3 or the right-pointing top of a 5 could be useful discriminators.

I'm now weighing how the conv2 kernel could pick up larger shapes like arcs, corners, and stroke endings, since a 5x5 kernel over the pooled maps covers a 14x14 pixel area. I'm also noting that 5x5 filters are a poor fit for fine orientation steps, so the richer structure probably has to come from conv2 rather than conv1.

I'm working out which curve-like shapes the digits contain, such as cap, cup, and open-side arcs, and where each one sits. Examples are a right-side bracket shape for the 3, a cap plus a diagonal and base line for the 2, and a left bracket with a bottom loop for the 6. I think these curve detectors could separate the digits well if placed at the right locations.

I'm settling on the digit features now: the 4x4 grid with orientation channels may already reach around 80 percent, and I'd rely on negative weights in the places where a given digit should have no ink.

I'm listing the features the conv2 channels should capture: the four orientations at the centred offset, some ink-presence signal, four curve shapes, possibly endpoint detectors, and whatever remains. I'm also starting to worry that the endpoint detectors may be too complex to get right by hand.

I'm considering whether the first layer could use some of its filters for stroke endings instead of duplicating bar detectors, such as a kernel that fires for the top end of a vertical stroke, with ink below and none above or to the sides. Then I'd check whether the response on a stroke's middle stays low, which would make those endings distinct from plain bars.

I'm now checking which first-layer filter could show a stroke's top ending: ink below the centre, with negative weights above and at the sides, so a plain bar would score lower there. I'm weighing whether endings add enough over the orientation and position features, since the main confusions like 4 vs 9 and 3 vs 5 seem to be the ones they'd help with. My biggest worry is getting the response magnitudes calibrated.

I'm weighing whether a nearest-template style classifier could beat the linear layer here, but a single linear map only gives one template per class, so extra prototypes would have to come from conv2 features. I'll keep the logits moderate so the cross-entropy stays reasonable, and I can try a couple of scales to see which works best.

I'm sketching the conv2 layer as a set of 16 part detectors, each covering roughly half a digit, so they could pick out loops, corners, and open cups. I'm also weighing whether a middle path, with fine-grained orientation channels plus a few part detectors, would be less risky to hand-design.

I'm settling on a plan to be incremental: start with baseline oriented features and templates, then refine them from confusions and add part detectors later. Since I can't run the code, I'm leaning toward generating the template weights from stroke descriptions in the 28x28 frame, so editing them stays manageable.

I'm checking whether building the template weights from hand-described strokes is still allowed, since the rules forbid running the network on inputs but not drawing features directly. I think it is, as long as each stroke contributes to the orientation cells through a formula rather than through a forward pass.

I'm checking whether building templates by hand from stroke descriptions still counts as drawing rather than generating samples to fit against. I'd keep each digit as a single hand-described template and avoid averaging over anything generated.

I'm settling on building the template weights from hand-described strokes, with positive values where a digit's strokes are expected and negative values where ink would be unexpected. I'm considering whether to subtract a constant per channel to penalise unexpected ink, or to subtract the mean across digits, and I'm leaning toward the constant since it avoids any averaging over generated examples.

I'm settling on a matched-filter scoring rule: reward ink where a digit's template expects it and penalise ink where it shouldn't be. For a digit like 1, a clean match should score high, while a 7 template might still partly overlap its vertical stroke, so the penalty term matters. I also need some normalisation so that heavy-ink digits like 8 and 0 don't dominate.

I'm working out why a plain linear template scorer would favour the wrong digit, since missing strokes carry no penalty unless a bias term accounts for how much ink a template expects. A 1 drawn as a slanted stroke could score well on a 7's diagonal, so I'd want the 7 template's bias or weights adjusted so each digit scores similarly on its own pattern.

I'm normalising each template by its L2 norm, which turns the score into a cosine-style match that peaks when the features line up with the template's direction. Subtracting half the squared norm as a bias gives the equivalent nearest-prototype rule under Euclidean distance. That only works if the feature magnitudes are on the same scale as the template weights, so I'd need to calibrate them.

I'm normalising each template by its L2 norm, so the score becomes a cosine-style match that doesn't favour digits with heavy or light ink. Mismatched ink doesn't need a separate penalty here, since the best-matching template still wins under argmax, and a 1 scored against a 7 template comes out lower because the 7 template's larger norm shrinks its score.

I'm going to scale the template weights by their L2 norms and calibrate the conv responses so each oriented stroke gives roughly a unit response, which keeps the channels comparable. I'm also considering a saturating nonlinearity, since binary-like features for "stroke of this orientation present in this cell" would be less sensitive to thickness and intensity.

I'm turning the saturating feature idea into a concrete conv1 setup: each of the four orientations gets two thresholded channels, and taking the difference in conv2 yields a clipped response. Since the max-pool commutes with that difference, the clipped maps stay exact at 12x12.

I'm weighing whether a centre-surround filter with zero-sum weights would miss thick strokes, since a width-5 stroke could cancel out completely. A profile with positive weights at the centre and a softer negative surround might keep thick strokes responding.

I'm checking how a zero-sum five-tap profile responds to thick strokes, since a width-5 stroke centred on the filter would cancel to zero. Shifting the filter to straddle the stroke edge gives a response of about 1, so the thick-stroke case may still register.

I'm weighing edge-based filters against the centre-surround profile, since an edge filter keeps responding to strokes of any thickness of two or more pixels. Every stroke has a top edge whichever way it runs, so a single polarity per orientation should be enough to pick up its direction.

I'm thinking about edge filters for the orientations: one polarity per direction should pick up any stroke, and the thickness-robust response means I don't need zero-sum bars. The worry is short edges at stroke ends, like the top of a vertical stroke, which a threshold could suppress. I'm now checking whether a horizontal edge filter stays silent on vertical strokes, and how it behaves on a 45° diagonal.

I'm weighing whether to use both bar and edge filters, or just the edge version. Edge filters look more thickness-robust, but I'm still weighing whether the extra polarity information is worth the added channels, and I want to check how saturation would interact with that choice.

I'm checking whether saturation is worth the cost: argmax doesn't depend on overall scale, so it mainly affects confidence in the loss. I'll leave it out and use eight conv1 channels, four oriented bars plus four other features, and iterate from there, since a hand-designed setup might reach the high 80s or low 90s.

I'm now listing which digit pairs are most confusable on a 4x4 grid of 8-pixel cells, checking whether a horizontal feature near the top centre separates 4 from 9. I'm also comparing the upper-left and upper-right cells to tell 3 from 5, and checking whether a lower-left vertical separates 5 from 6.

I'm comparing which digit pairs are most confusable on a 4x4 grid of 8-pixel cells, like 4 versus 9 near the top centre, and 3 versus 5 by the upper-left and upper-right cells. Since the grid is coarse, I'm also considering whether conv2 kernel conjunctions could sharpen the spatial resolution.

I'm working out the pooling arithmetic for the second layer: a pool2 cell takes the max over a 2x2 block of pool1 positions, which covers a 4x4 span of conv1 outputs and roughly an 8-pixel window in the image. I'm checking which pool1 rows each offset from the conv2 kernel actually reaches.

I'm checking where the pool1 rows for the offset-2 tap land: pool2 rows 0 through 3 map to pool1 rows 2 through 9, which corresponds to pixel centres around rows 6 to 21. I'm also considering whether a top-edge detector at row 4 would still be covered by that window.

I'm checking the pooling coverage for the second conv: an offset of 2 only reads pool1 rows 2 through 9, so strokes centred at pixel rows 4 and 5 would be missed. Using taps at offsets 1 and 2 instead would shift the windows so that the top rows of the digit box are covered.

Checking the tap offsets again: taps at 1, 2 and 3 cover pool1 rows 1 through 10 between them, so the top and bottom edges of the digit box are reached. Pooled cell centres then sit symmetrically around 5.5 only when the offset averages to 2, which is what I'd need for the mapping to line up.

I'm settling on taps at offsets 1, 2 and 3 with equal weights, which centres the cells on the digit box and lets them overlap by half. I'm also weighing a 5x5 blur kernel of [1,2,3,2,1] before the max pool to make the features more tolerant of small shifts.

I'm weighing blur kernels of different widths for conv2, since a wide triangle would overlap cells heavily while a narrower weighting like [0.3, 0.8, 1, 0.8, 0.3] might keep the features sharper. The aim is a blur wide enough to absorb the roughly 2-pixel spread in stroke positions across MNIST digits.

I'm settling on a Gaussian-like blur of about [0.15, 0.6, 1, 0.6, 0.15] before pooling, and I'm considering offset versions of it so the conv2 channels can cover finer positions than the current four-orientation setup.

I'm working out where the pooled positions land: the two offsets together cover pool1 rows 2 through 9, which means eight evenly spaced positions about 2 pixels apart, symmetric around the digit's centre. With four orientations times two row offsets times two column offsets, that's sixteen channels giving an 8x8 grid of orientation features, or 256 values in total.

Weighing whether finer spatial resolution (8x8 grid) or more feature types on the coarser 4x4 grid would give better accuracy. Drawing from HOG-style results on MNIST, finer grids usually help a trained classifier, but for hand-built templates my own drawing precision is the real limit rather than resolution.

I'm settling on the idea of template negative weights as a way to encode discriminative knowledge, like a veto on the top-centre horizontal feature for class 4 that separates it from 9. I'm considering whether to mix in a few extra non-orientation features alongside the offset channels, but the complexity is adding up.

I'm weighing whether to cover the 16 channels with four orientations at four offsets, or to reserve some for other feature types, since the conv2 budget is fixed and the fully connected layer only sees what those 16 channels provide. Using eight conv1 channels for four orientations with two polarities is another option, though it doesn't relieve the 16-channel limit at conv2.

I'm weighing whether a finer 8x8 grid of four orientations is worth more than a 4x4 grid with extra feature types, since the 4x4 cells with 8-pixel windows are coarse but might still localise the top bar of a 7 and the mid bar of a 4 well enough.

I'm weighing a quincunx layout, with four orientations sampled at two diagonal offsets for eight channels, and reserving the other eight for special features. Since I'm drawing templates from stroke formulas rather than a fixed grid, the odd sampling pattern shouldn't matter much.

I'm weighing a set of special endpoint features for the remaining channels, such as detecting where a vertical stroke terminates by pairing a vertical response below a point with an absence of ink above it. Getting that absence signal would mean negative weights across all four orientation channels in the cells above, since conv1 alone can't express it.

I'm checking whether a conv2 conjunction can pick out stroke endings: a positive vertical response a couple of rows down, paired with negative weights on all four orientation channels above, so a stroke that continues upward gets suppressed. That should work for tops of 4s and 1s while staying quiet on 9s and 7s, where a horizontal bar sits above the stroke.

I'm weighing a "hole" detector for loops: a background point surrounded by ink on all four sides, using a 5x5 conv2 kernel over pool1 with an AND-style threshold. The concern is that loop sizes vary a lot, since a 0's interior is much larger than the loops in 6, 8 or 9.

I'm now weighing a "hole" detector for enclosed loops, which would need an AND across four directions of ink. A plain linear sum can't express that reliably, so I'd need saturated conv1 responses and some threshold trick to get the conjunction.

I'm thinking through the saturation step: clipping the conv1 responses between a noise floor and a stroke-level threshold, so the orientation maps become near-binary and conv2 can form reliable AND conjunctions. The hard part is picking that upper threshold, since I don't know the exact intensity statistics of MNIST strokes beyond their roughly full-intensity centres and thin antialiased edges.

I'm comparing bar filters with edge filters for conv1, looking for a response that stays roughly constant whether a stroke is thin or thick. A bar profile like [-1, 0, 2, 0, -1] gives a peak of 2 for strokes up to about three pixels wide, dropping to 1 for wider strokes, which would make saturation thresholds shift with thickness.

I'm checking how a bar filter with a profile like [-1, 0, 2, 0, -1] responds to strokes of different widths: thin strokes peak at 2, while wider ones settle around 1, so saturating at that level should make thickness matter less. I'm also weighing a gentler profile, and I'm wondering whether doubled responses at both edges of thick strokes will cause any trouble.

I'm now laying out diagonal bar filters for the 5x5 kernels, giving each pixel a weight from its perpendicular distance to a line through the centre, with negative flanks and a zero-mean adjustment so uniform ink produces no response.

I'm choosing the profile for the diagonal filters: a Mexican-hat shape with its zero crossing at distance 1, so the negative lobes sit just outside the bar. I'm checking its values at the first few perpendicular distances to see how strong the flanks get.

I'm checking the Gaussian-based profile numerically at a few distances and seeing that its sum over the truncated window isn't zero, so the filter would still respond to uniform ink. I'll subtract the mean from each filter to make them zero-sum.

I'm working out the diagonal filter weights from the Mexican-hat profile, checking the values at each perpendicular distance and counting how many pixels fall at each one.

I'm checking the diagonal filter's response numerically: a centred stroke gives about 5.5, close to what the horizontal filter gives on a width-3 horizontal stroke, so the two orientations look roughly balanced.

I'm settling on saturation thresholds around 1.0 and 3.0, since the ideal diagonal response is about 5.5 and thick-stroke edges fall to roughly 2.5 to 3. I'm checking that against a thick horizontal stroke, where the edge responses come out near 2.25 and 2.8, which both sit inside that band.

I'm settling the saturation band: horizontal stroke edges land around 2.5, so I'll set the upper threshold there and the noise floor near 0.5. Orthogonal and crossing strokes give roughly zero response, while strokes tilted by about 22.5 degrees should still drive both the horizontal and diagonal filters to around 4, so both saturate.

I'm checking how tuning width works for these bar filters: a stroke tilted by some angle shifts its ends sideways, and the response drops once that shift passes roughly 1.5 pixels, which suggests a half-width near 35 to 45 degrees.

I'm weighing a looser saturation band, with the upper threshold near 4.5, so 22.5° strokes still register partially while thick strokes don't wash out.

I'm checking whether a profile with a larger centre weight makes the response to thin and thick strokes more even, and I'm working through the algebra for a zero-sum version of it.

I'm now trying a wider positive centre in the bar profile so thin and thick strokes give more similar responses, and I'm weighing saturation thresholds around 1.5 and 5 against the expected per-column response.

I'm reconsidering whether broad orientation tuning is a real problem: with four channels at 45° spacing, a stroke near 22.5° would drive both neighbouring channels, which is roughly what a continuous orientation code needs. I'll draw the templates with that same tuning curve, so the saturation thresholds and the template shapes stay consistent with each other.

I'm weighing a softer alternative to hard saturation: a linear falloff in the template tuning, full response within about 22.5° of the preferred orientation and tapering to zero at 45°, so the templates match the thresholds.

I'm weighing whether saturation is even needed for plain template matching, since argmax over cosine scores doesn't require it, but it does matter for conjunction-style features. I'm also considering an alternative with eight conv1 channels instead of four, and noting that the softmax temperature would drift with how bold an image is.

Now I'm turning to the second-layer features, with the conv1 channels set up as clipped orientation responses.

I'm weighing three layouts for the second-layer features: sixteen channels on an 8x8 grid for pure template matching, a mix of quincunx offsets with eight special detectors, or a coarser 4x4 grid with twelve specials. I'm also starting to think about endpoint detectors for the tips of strokes, such as an up-ending at the top of a stroke that continues downward, and how a digit like 1 would be signalled by an up-ending at the top and a down-ending at the bottom.

I'm listing which endpoint pattern each digit would show, like a left-end at the upper-left for 2 and 3, up-ends at the top for 4, and a down-end at the bottom for 9, to see which pairs of digits the ending detectors could tell apart.

I'm moving on to the endpoint features, matching each digit's tip pattern to the detectors that would separate the confusable pairs. For the holes, I'm thinking about a loop detector that checks for ink on the left, right, above and below an empty centre, since the sides of a loop can be any orientation except horizontal.

I'm checking the hole detector's reach against loop sizes: for small loops like 6, 8, and 9, the strokes sit within the kernel's range, but for a 0 the sides of the loop fall outside it, so the detector would only catch small zeros and I'm fine with leaving 0 to its own signature. Still, I'm wondering whether a partial response on the upper or lower side might still leak through.

I'm weighing whether a hole detector can be built as a clean AND of four side signals, but a sum of side terms could exceed 1 and fire falsely. Without another saturation step to bound them, I'll have to accept that limitation and rely on the spread-out weights.

I'm checking whether the side terms of the hole detector stay bounded: each side's weights sum to about one, so a short arc piece gives a fraction and a long stroke gives at most one, though overlapping orientation channels could push a side slightly above that. I'm weighing whether a threshold on the summed sides is still safe under that looseness.

I'm now sketching curvature features for the second layer: a ")" curve would show a "\" stroke on top and a "/" stroke below it, and a "(" the reverse. I'm also weighing shapes like "∩" and "∪" as pairs of diagonal strokes meeting at the top or bottom.

I'm now working through how diagonal stroke pairs could mark curves and arches: a "\" over a "/" reads as ")" and the reverse as "(", while "/" then "\" side by side suggests "∩" and the opposite suggests "∪". I'm also noting that an X-shaped crossing of both diagonals at one spot could mark the centre of an 8, and a crossing of horizontal and vertical strokes could mark the centre of a 4.

I'm now checking which conv2 pairings of diagonal strokes would signal the ")", "(", "∩" and "∪" curve shapes, and whether an AND of two saturated maps keeps each term bounded. I'm comparing how the 3, 5, 6 and 8 curve signatures differ on each side.

I'm now weighing whether endings and holes work as the most useful extra features, since a stroke that stops at a point is something a linear template over orientations can't capture. For telling 4 from 9, the question is whether the top of the digit is closed, so I'm thinking about the template that would encode that.

I'm comparing the 9's top-centre strokes with the empty top-centre region of a 4, and expect an orientation template to separate them. Writer variation in where the top sits is the concern, though blurring should soften it. I'm inclined toward a dense orientation grid as the baseline and treating the special detectors as optional experiments, since the effective resolution after blur and pooling isn't much finer than a 4x4 grid.

I'm weighing the blur kernel spacing for the second-layer detectors: with three taps, cells would sit two pool units apart and still sample the map reasonably, while the quincunx layout doubles the density and seems like the better compromise.

I'm now weighing a blurred conv2 kernel with a Gaussian-like weighting, so each second-layer feature measures roughly how much of a given stroke orientation lies nearby rather than just whether it is present. Because the blur sums saturated values, a long stroke passing through the kernel will drive the response higher than a short piece, which makes the template match an expected amount of stroke rather than a binary hit.

I'm treating the template as a soft rendering: each stroke becomes a set of sampled points with orientations, weighted by distance to each cell centre, so the result approximates the network's response up to scale. Since the template gets normalised, only the relative weighting between orientation channels and the hand-placed ending features really matters.

I'm settling on normalised cosine scoring against each digit's template, and I'll add a logit scale on top. Since the features are roughly magnitude-calibrated, the true class should score near the feature norm while the others score that norm times their cosine similarity to it, which should sit somewhere around 0.3 to 0.7.

I'm settling on how to score the digits: subtracting a shared vector from every class wouldn't change the argmax, so that step isn't needed. I'll add veto strokes as negative weights for each digit's template to suppress confusable shapes.

I'm weighing whether deskewing is worth attempting, and deciding instead to draw the templates with a slight rightward slant, since MNIST digits typically lean that way. For the special features I'm starting with an up-ending detector: it would respond to a stroke below centre with nothing above it, using positive weights on the vertical and diagonal orientations in the lower rows and negative weights to suppress activity above.

I'm checking the up-ending detector: it should fire on a stroke's top tip, with positive weights on the vertical and diagonal orientations just below and negative weights above to suppress it mid-stroke. That should handle the tops of 1s, 4s, and 6s, with about 2-pixel resolution at the tip.

I'm checking which digits an up-ending detector would catch: the tops of 1, 4 and 6 should fire it, while 5, 7, 2, 3, 8, 9 and 0 mostly shouldn't. A top-left horizontal bar on a 5 would suppress it, and a 4 should trigger it at both the top-left and the top-right. I'm treating the absence of an up-ending near the top of a 9 or 0 as negative evidence against those digits.

I'm treating the bottom-tip detector as a split between digits: down-endings near the bottom centre would show up for 1, 4, 7 and 9, while 0, 2, 3, 5, 6 and 8 mostly lack them. The bottom-tip evidence and the top-tip evidence together look like they could separate 4 from 9 and 1 from 7 fairly well. A left-ending detector would then pick out the 7's horizontal bar, with a separate check for 2's horizontal base, which points right instead.

I'm going through the stroke endings as location-specific features: right-endings at the top of 5, the bottom of 2, and the crossbar of 4, with 6's top tip possibly curving right. The left-endings at the top of 7, the upper and lower left of 3, and the bottom of 5 and 9 are the mirror cases. The tricky part is diagonal tips, where a 7's bottom stroke points down-left and could register as a down-ending instead of a left-ending.

I'm defining a down-ending detector on a 5x5 grid: positive weights on the vertical and diagonal orientations at the tip, negative weights below it to suppress activity beneath the stroke, and I'm still checking how the horizontal orientations should be handled around the tip.

I'm working out the thickness effect at a stroke's end: a bar filter's response falls off past the tip, and a thick tip can leave a partial horizontal response that I need to account for when placing the down-ending detector.

I'm checking how far the response spreads past the stroke's tip: the vertical filter still catches a bit about a pixel and a half beyond the last ink. At pool resolution that leaves the negative suppression region just barely reaching the tip's neighbours.

I'm weighing whether to keep eight orientation channels in a quincunx layout or switch to four channels with a narrower blur plus extra curve detectors. Either way, the max-pooled outputs after the second pool would stay bounded near 1.7 when vertical and diagonal responses both fire.

I'm checking the pooled coordinates: the four cell centres land at about 7.5, 11.5, 15.5 and 19.5 pixels, and with the blur and pooling the effective spread is roughly a Gaussian with σ≈3px sampled every 4px. That's dense enough that the eight-channel quincunx layout doesn't seem necessary.

I'm settling on 4x4 cells with four orientation channels, reasoning that the blur already gives roughly 3px smoothing at a 4px stride, so finer sampling wouldn't buy much. Hand-placed templates are only accurate to a few pixels anyway, so the design constraint is my feature quality rather than grid resolution. I'm still checking whether digit strokes near the top border fall too close to the first cell centre.

I'm now deciding on the remaining channels: I'm keeping the four endings (up, down, left, right), and I'm considering diagonal tip variants, curve detectors for the four arc shapes, a couple of hole detectors, and a junction channel for crossings like the 4 and 8.

I'm considering whether a second layer of digit-level part detectors would work better than more local orientation channels. A 5x5 kernel on the 12x12 map would cover about 14 pixels of the image, so it could respond to multi-stroke configurations, like a closed loop or a horizontal bar sitting to the left of a diagonal, with a ReLU threshold making them behave as AND-style detectors.

Next I'm laying out the plan in steps: first the four orientation channels and four endings with everything else zeroed, templates built from the strokes, then checking the confusion matrix and adding features aimed at whatever errors show up.

Still defining the conv1 orientation filters, working out the pixel offsets and perpendicular distance to each line direction.

Still defining the orientation profile for the conv1 filters, using the perpendicular distance from each pixel to the line through the centre, and checking the 45° and 135° cases against the horizontal and vertical ones.

I'm working out the diagonal response profile by checking how far each pixel sits from the line, using the same weighting scheme as the horizontal and vertical filters.

I'm checking the diagonal response numbers: a thin diagonal stroke gives a strong score, and the score drops when the stroke gets wider, so the diagonal filter's profile is the same shape as the horizontal one but sampled more finely across the perpendicular direction.

I'm weighing whether to normalise each filter against an idealised stroke profile so the horizontal and diagonal responses come out comparable, though I'm not sure that counts as running the network on inputs, so I'm leaning toward a purely formula-based normalisation instead.

I'm checking whether the two filters' L2 norms match, and they do at about 2.67 versus 2.69, yet the diagonal filter still responds differently to wider strokes. I'm now testing how a Gaussian-profile stroke of width around 1.1 px falls off with perpendicular distance to see where the two responses diverge.

I'm checking the response strength of the diagonal and horizontal filters against a typical Gaussian-profile stroke, and both come out around 4.2 at unit intensity. They differ only for wide flat strokes, which I'm fine with, so I'll keep the per-orientation gains at 1.0.

Checking the thicker-stroke case now, with a wider Gaussian profile that spreads the response further out to the sides.

I'm estimating the typical response strength of these filters against strokes of different peak intensity, and it comes out around 3 to 4.9 for full-intensity strokes, dropping for fainter ones. I'm considering a clipped linear mapping from response to activation, with thresholds at 1.0 and 3.0, so saturated strokes read as full activation.

I'm settling on a threshold range of 1.5 to 3.5 so that thick strokes land around 0.6 and off-angle strokes at 22.5° map to about half activation. Next I'm estimating how the response falls off as the stroke tilts away from horizontal, using the row offset that a tilted line produces at each column.

Checking the response of the horizontal filter to a stroke tilted at 22.5°, I'm working through the row offsets at each column and the weighted sums that follow from them.

Working out the response at 45° now: sampling the row offsets at each column gives a much weaker sum than at 0°, so the diagonal-tilt tuning drops off quickly.

I'm working out the 45° case, where the summed response drops below threshold and the filter goes to zero, and tracking how the tuning curve flattens out near 22.5°.

I'm fitting the orientation tuning as a clipped falloff with angle, so the response drops smoothly from full strength at 0° to zero near 45°.

Next I'm setting the conv1 weights to half the orientation weights, with bias thresholds at -0.75 and -1.75 so each channel pair gives a 0-to-1 activation.

I'm working out the orientation channels in the second layer: a blur kernel over the pooled stroke maps, and I'm checking how much of a stroke's response survives the normalisation, which comes out around 0.4 for a line through the centre. I'm also considering how wide the first-layer activations spread across pooled columns, since a vertical stroke three pixels wide seems to light up only a narrow band of neighbouring columns.

I'm working out how many pool columns a vertical stroke lights up: when it's centred on a pixel, the first-layer response is strong in one column with only a faint neighbour, but when it sits between two pixels both columns respond strongly and may fall into one pool cell or two.

Now I'm working out how the stroke's response spreads across neighbouring pooled columns, and treating a long line through the cell centre as the reference case. I'm scaling the blur kernel so that a typical stroke gives a response near 1, then describing each orientation template as a sum over stroke samples weighted by the angle tuning and a Gaussian.

I'm working out the blur's Gaussian width from its kernel weights, which comes to about one pooled unit, or roughly two pixels, and then I'm considering how taking the best of nearby convolution positions changes the effective response.

I'm working out the template amplitude next, taking the effective blur width to be about 2.6 px so a line through the cell centre gives roughly 1.0. Then I'm checking how the max-pooling over neighbouring kernel positions widens the response for strokes slightly off-centre.

I'm working out how the top endings respond as the stroke's top edge moves past the filter's centre, scoring the vertical filter by how many of its five rows are covered.

I'm setting the vertical-edge kernel's weights: a positive pair at the two rows just below the top edge and negative weights across the rows above it, so the threshold sits right at the stroke's top end.

I'm working out the bottom-of-stroke signal for the vertical filter: at the best alignment, the positive rows should sum to roughly 0.75 to 1, with the negative rows contributing only about −0.08. Since a slanted stroke can drift into the neighbouring pool column, I'm considering adding positive weights on the side columns in the lower row as well.

I'm settling the up-ending kernel's orientation weights: the vertical filter gets full weight, and the two diagonal filters get a lower one, since a stroke tilted at 45° only reaches the tip one column per row. I'm also laying out the exact positive weights on the middle rows so a vertical stroke scores about 1.0.

I'm setting the down-stroke kernel's negative region: rows above the tip get −1 across the three central columns for all four orientations, and I'm weighing whether the horizontal filter needs its own side weights at the tip.

I'm working out how the horizontal bar at the top of a stroke, like the corner of a 5, should be suppressed: the horizontal filter would fire near the same row as the vertical tip, so I'm considering negative weights for it in the rows at and just above the tip, across the central columns.

I'm checking whether the horizontal filter should also be suppressed near a tip, using the 4's top-left corner as a test case. The left stroke of a 4 runs down and meets the crossbar about 8 px below, so no horizontal response appears there. The right vertical's top, and the apex where the two diagonals meet, should still register as up-endings because the negative region above is empty.

Now I'm checking the left-ending case by transposing the kernel, and I see a conflict: the diagonal that tips up-right from the left end is the same shape as the down-ending diagonal, so the two channels can't be told apart by orientation alone.

I'm deciding whether the diagonal filters should count toward vertical endings at all, since a steep diagonal's lower-left tip would look the same to the down-ending and left-ending channels. I'm leaning toward giving the diagonals to the up and down endings only, which would mean a 2's upper-left arc tip and a 5's bottom-left curl get classified by their vertical component, though I'm still checking which orientation that actually picks.

I'm settling on ending detectors for eight tip directions (N, NE, E, SE, S, SW, W, NW) rather than only four orientations, since separate diagonal channels avoid the ambiguity between a "/" tip and its mirror. Each direction would be assigned a template, and I'd need to work out which digit cells fire for each one.

I'm now listing which tip directions each digit would fire for, and I'm weighing whether eight ending channels justify their extra cost over four. For the 1, the top tips point north or northeast and the bottom ones point south or southwest, plus west and east at the base if it has a foot. The 2 and 3 have endings in the upper-left and lower-left, each pointing in a few different directions.

I'm now going through which tip directions each digit's endings point toward, looking at the 4, 5, 6, 7, 8 and 9 in turn. The bottom tips pointing south or southwest seem to show up across several digits at bottom-centre, and the north-facing tips at the top.

I'm grouping the tip directions into four ending channels: up, down, left and right. The diagonal tips fold into the vertical channels, so the 2's start and the 3's top count as down-endings, and the bottom tips of the 3 and 5 count as left- or up-endings.

I'm weighing whether the remaining eight channels should hold extra features, and I'm leaning toward offset copies of the orientation maps, sampled at half-cell positions, since they come from the same stroke templates and so stay consistent with the rest of the network.

I'm weighing whether to add offset copies of the orientation maps at half-cell shifts, which would give 12 channels, but the two offset grids overlap and double-count the central region.

I'm weighing whether to add curve detectors as well, such as a "(" channel that fires when an upper "/" and a lower "\" line up in the same column. That would be an AND of the two diagonal responses, which might be worth having from the start given how often digits get confused.

I'm considering a ")" curve detector built from a downward diagonal above an upward one in the same columns, but spreading weights across the patch means a single long stroke only reaches a partial sum, so the AND condition doesn't hold cleanly. Larger weights on the group would let one diagonal alone trigger it, so I'm still looking for a threshold that requires both halves.

I'm now checking whether a tight, non-spread conjunction is the only way to get a clean ")" detector, since spreading the weights lets a single long diagonal leak through. The idea is to pin the upper "\" and lower "/" parts to exact positions a couple of pool rows apart, with the arc's radius setting that vertical gap.

I'm working out the position of the diagonal response along the arc: with radius 5, the tangent-based detector would be active for points spanning roughly 15° to 75° from the top, which puts its vertical extent between about 0.97r and 0.26r above the centre.

I'm checking how a conjunction detector for the ")" curve would respond, and whether splitting its weights across neighbouring rows lets a single diagonal stroke trigger it alone. Each half of the pair would only reach about 0.5 from one stroke, so the threshold has to be set carefully.

I'm now weighing whether a ring-shaped template over the pooled maps, with weights matching the tangent direction at each position, can act as a matched filter. I'd set its threshold at roughly 60% of the ideal response, so that only good matches pass the ReLU.

I'm settling on a simpler first design with four orientation and four ending channels, then testing it before adding more. The extra channels would only be worth it if the endings hold up, so I'm checking that next. I'm not sure the endings stay reliable for bold digits or noisy strokes, but I expect the response to hold near 0.6.

I'm checking whether tight curves break the orientation responses: on a narrow arc, a 5px filter can't match one direction well, so the endings near the bend could drop below threshold. The top of a narrow 0, the top loop of an 8 or 9, and the tight turn at the top of a 2 are the cases I'd want to test.

I'm checking whether tight arcs break the bar filters: with a radius of about 2.5px the curve deviates about 1px at the ends of a 5px filter, so the stroke could look like it terminates. For a narrow 0 with a 3.5px arc radius the deviation stays near 0.6px, so the top should still respond strongly.

I'm checking how the pooled ending cells are centred, so the tip kernel at (2,2) lines up with the orientation maps.

I'm checking where the top tips land in pooled coordinates: a tip at row 4 maps to pool row 1, which falls just outside the first ending cell's range of rows 2 and 3, so the very top of the digits may be missed.

I'm placing the up-ending tip one row higher so the top of the digit lands in the first ending cell, and shifting the down-ending tip one row lower so the bottom tips do too. That leaves only a single row above the up-ending tip to serve as the negative region.

I'm checking whether the top tips of the digits fall into the first ending cell: a top at row 2 to 6 maps to pool row 0, 1 or 2, so cell 0 may still miss some of them.

I'm checking the edge case: if the top tip sits at pool row 0 or 1, cell 0 misses it, but an up-ending kernel with its tip at row 1 still catches tops in the 4–7 range, and I'd accept that partial miss rather than shift the kernel to row 0, which would turn it into a plain V-detector.

I'm checking where the tops of the digits land in the pooled grid, using the 20-pixel box and how the centre of mass shifts it. The 1 and 4 should have their tops near row 4 or 5, which the cell covers, but the 6 might shift its box so the top falls to row 3, and I'm not sure that case is handled.

I'm checking the top-row case for the 6: its box may shift up so the stroke starts near row 3, which only partly lands in the first ending cell, with the negative row above giving a half-strength response. I could lighten that negative weight a little, or just accept the partial miss.

I'm checking the bottom tips too: for 7s and 9s the box can shift down by a row or two, so the last ink row lands at pool row 11. The down-ending tip at row 3 would then cover only partway into the last cell, so I'm weighing whether to accept that partial miss or lighten the negative weight below.

I'm checking the bottom tips of 7s and 9s, where the box can shift down so the stroke reaches the last pooled row; the negative weight there would only partly cancel the response. I'm also wondering whether the image border gives me any extra room, since the first convolution only produces outputs for the central rows.

I'm now thinking about how the bottom tips of 7s and 9s might be told apart from arcs and bars, perhaps by looking at the horizontal orientation in the lowest pooled rows, where the blur from the convolution thins out.

I'm reasoning that the bottom and top endings mostly duplicate what the orientation channels already encode: the "V without H" pattern at the top and bottom rows separates 1, 4, 6, 7 and 9 from the arcs and bars, so a linear layer can capture it without separate ending detectors. That means the endings only earn their place in the interior, such as telling a 4's top apart from a 9's, where the H response at the top-centre matters.

I'm now weighing whether the endings add anything beyond what the orientation channels already capture, since "V without H" at the top and bottom rows already separates most digits. The more useful extra channels may be ones that encode relations between parts, like an H bar sitting above-left of a downward diagonal, which should hold up better when the digit is shifted or slanted.

I'm now turning to the first-layer design and thinking about whether the second layer could build class-specific part templates, such as the top half of a digit, instead of only summarising orientation. The question is whether that would beat what a linear layer over the orientation channels already captures.

I'm now listing the shapes that show up in the top half of each digit, like the open arc of a 2 or 3, the loop of an 8 or 9, the bar-and-stem of a 5, and the wide arc of a 0. For the bottom half, I'm sorting out the bar of a 2, the closed arc of a 3 or 5, and the loops of a 6 or 8.

I'm weighing a part-based second layer where each digit is described as a combination of a top shape and a bottom shape, with each pair unique to one digit. The point is that nonlinear part detectors might separate classes better than a linear sum over orientation channels, though pooling only gives a few pixels of shift tolerance.

I'm working out how to build the 5x5 part kernels by drawing strokes on a 14x14 local grid at 2-pixel spacing, then subtracting a penalty to keep them selective. The last step is choosing the threshold for each part detector, which I can only set by reasoning, since there's no data to calibrate it against.

I'm weighing whether a hierarchical design, with part detectors built from a shared stroke-rendering routine, would beat flat linear templates. The main worry is that I can't check the part responses directly, so I'd be relying on reasoning alone to trust the thresholds.

I'm estimating the response of a part kernel on a real digit: it's roughly the stroke patch's norm times the cosine match, around 2.5 for a good match and about 1 for a poor one. Partial overlaps are unavoidable, so I'd set each part's bias to sit near half the ideal response.

I'm now considering using the logits as a measuring device: each output would be a threshold on one feature, so the prediction reveals how that feature's values are distributed across the true classes, which would let me check the part detectors without labelled debugging.

I'm considering whether the 10-bin histogram trick could measure any linear feature per class: the logits act like a nearest-bin-centre readout, so each probe run would reveal how that feature's values spread across the true digits. Since only the final run is scored, the intermediate probe runs can be spent on this kind of diagnostic.

I'm weighing whether to build the first step as a flat set of orientation templates with ending detectors, or as a hierarchy of part detectors. Probing the network with threshold-style logits could reveal feature distributions per class, but I'd rather spend the first run on a real classification attempt to see the confusion matrix directly.

I'm weighing whether to start with flat orientation templates plus ending detectors and examine the confusion matrix, then add part detectors aimed at the worst confusions, such as 4 versus 9 or 3 versus 5.

I'm weighing whether to start with a flat set of orientation templates plus ending detectors, since the endings add modest value and the errors will show up clearly in the confusion matrix. Some pairs like 4 and 9 or 3 and 5 tend to get confused, so I'll check the first run for those before deciding whether part detectors are worth the extra complexity.

I'm weighing whether a denser second bank of orientation maps, offset from the first, would help the flat template version. The idea is that four channels at a shifted grid could fill in what the coarse blur loses, and since the template rendering is automatic, it's a low-risk addition for step one. I still need to settle on the offsets for that second grid.

I'm checking where the sampling centres for a second, offset orientation grid would land: a centre at 1.5 just duplicates the first grid shifted by half a pool unit, so that's no good. A centre at 1 or 3 spreads the cells differently, and covering all four combinations would take 16 channels, while a mix of (1,1), (3,3) and a centred grid would fit in 12.

I'm checking how the two offset grids would combine: the centres from the 1-offset and 3-offset cells overlap in nine spots, so the centre gets counted twice. That leaves a quincunx-like coverage of the middle region, with the outer corners rarely inked anyway. I'm deciding that the double weighting in the centre is acceptable, if a little unprincipled.

I'm settling on three orientation banks for the flat version: one at the main offset and two shifted ones at centres 1 and 3, plus the endings detectors. The shifted banks duplicate some centres, which I'll accept for now, and I'm reconsidering whether probing the network early would help calibrate the features.

I'm now sanity-checking the input scale for the stroke detectors: real MNIST strokes peak near 1 at the centre and drop to around 0.3–0.6 at the edges, with widths of roughly 2–5 px. If typical ink per unit length is only about 2.3 px wide, the orientation responses might come out weaker than my thresholds of 1.5 and 3.5 assume.

I'm checking the scale of the logits: the score for each digit would be a cosine match between its template and the features, and with around 192 template dimensions, the norm will set how large those scores get.

I'm estimating the logit scale as roughly 4.7 for the true class against about 3 for the others, so a softmax temperature near 3 seems reasonable for now, to be recalibrated later. Next I need to define the stroke prototypes for each digit on the 28x28 grid, starting with a helper that adds line segments between points.

Next I'm sketching the digit prototypes for 0, starting with an ellipse centred at (13.5,13.5), tilted a little so the top leans right, with the centreline sized to fit inside the 28x28 box.

Now I'm defining the digit 1 as a mostly vertical stroke with a slight slant, and I'm starting on the 2's outline from the upper left.

Now I'm mapping out the digit 2 as a top arc, a diagonal sweep down to the lower left, and a bottom bar, with the centre of mass kept near the middle of the box.

I'm laying out the digit 3 as two stacked arcs: an upper one centred near (13, 8.5) that starts at the upper left and sweeps round to the middle, and a larger lower one centred near (13, 17.5) that runs from the middle, around the right side, and ends at the lower left.

I'm placing the 4's left stroke from about (9.5, 5) down to (8, 14.5), then a crossbar across to (19.5, 14.5) and a right vertical running down to about row 23.

Now I'm defining the digit 5 as a top bar, a vertical drop, and a curved belly sweeping round to the lower left, then starting the 6 as a stroke curving down from the top right.

Now I'm defining the digit 7 as a top bar running right to left, then a long diagonal stroke sweeping down to the bottom centre, and I'm considering whether to add an optional crossbar.

I'm planning to normalise each digit prototype automatically: shift the stroke samples so their centre of mass lands at (13.5, 13.5), then scale so the centreline bounding box is about 17.5 px, matching how MNIST itself is preprocessed. That way I don't have to hand-tune each digit's position, including the 7, which runs top-heavy.

Now I'm working out the figure-eight for the digit 8, so its two loops meet in a crossing at the middle rather than just touching.

Next I'm settling the figure-eight for the 8: a crossing at the centre with diagonal tangents, the top lobe slightly narrower, and each stroke built as a dense polyline so the tangents can come from finite differences.

Still writing the digit prototypes, and I'm defining the 9 as a loop with a slanted stem. Then I'll render each bank's features as a weighted sum over the stroke samples.

I'm giving each ending detector a template by flagging which stroke endpoints are tips, taking the tip direction from the tangent pointing away from the stroke, and spreading a Gaussian into the matching channel's 4x4 grid. The channel offsets need to be accounted for when placing those cells.

I'm working out the ending detectors' amplitude, and I'm reckoning they'll sit at about the same scale as the orientation features, so I'm still deciding how much weight they should carry since they're the discriminative part.

I'm weighing a ×1.5 boost for the ending detectors, since they carry the discriminative signal, and I'm noting that a cosine scoring setup doesn't need negative ending templates. I'm also setting aside any veto or negative-weight strokes for now and will only add them later if specific confusions show up in the data.

I'm working out the conv1 weights for each orientation, using a Gaussian-like profile over the distance from the line and subtracting the row mean so the kernel has zero mean. I checked the values for the horizontal case against the expected pattern, and they match. Both orientations should give typical responses around 4.2 and 4.7 at the chosen blur scales.

Now I'm working out the diagonal filter weights: for the 45° case I'm checking how many kernel positions fall at each distance from the line, then plugging the distances into the Gaussian-like profile to get the raw values.

I'm checking the arithmetic on the diagonal filter's mean, which comes out to about 0.235, and that checks out. Next I'm setting the conv1 weights to half the orientation kernel for both channels in each pair, with biases of -0.75 and -1.75. I'm also wondering whether a noise floor around 1.5 will suppress spurious responses from other orientations at stroke ends and corners.

Now I'm setting up the second conv layer's kernels in three banks, each a separable Gaussian-like profile centred at a different offset, with the bank B kernel getting clipped at the edge.

Now I'm working out the scale for the conv2 kernel, with a constant near 0.32 so a line through a bank's centre gives a response of about 1.04. Next I'm setting up how each bank's template cells map to pixel positions in the 4x4 grid.

Now I'm writing out the endings channel's weights: the upward-tip channel gets its main weight at the tip cell and a smaller one beside it, with the two diagonal variants shifted sideways, and I'm penalising all four orientations along the row above.

I'm checking whether the horizontal filter's negative weights should sit at the tip row for the vertical and diagonal endings, since a stroke tilted about 30° from horizontal could still partly trigger it there. I'm leaning toward keeping those suppressors at −1 on the top row and −0.7 on the row below. I'm also asking whether the diagonal endings should carry the same 0.6 and 0.4 weights as the vertical ones.

Still setting the ending detector weights: the down-facing channel gets its main weight at the tip cell and a smaller one beside it, with the diagonal variants shifted sideways, and I'm suppressing the orientations along the rows around the tip.

Now I'm setting the ending detectors' weights for the left and right channels: the tip cell gets the main weight, the neighbouring cell a smaller one, and I'm suppressing the orientations along the columns beside the tip. I still need to place the cell centres for these endings.

I'm placing the ending detectors' cell centres on the 4x4 grid for each channel, with the up and down tips spaced along the columns and the left and right tips along the rows, and I'm noting that each cell covers a window of about four pixels around the tip.

I'm working out where the ending detectors' tip cells should sit: the boundary where the filter's coverage reaches about 60% depends on the ink extending slightly past the centreline endpoint and on how far inward the filter centre lands.

I'm settling how to decide which strokes get tips: each stroke gets a start and end flag, and the tip direction points outward along the tangent. If that direction is within about 35° of horizontal, it goes to the left or right channel by its horizontal sign, and otherwise to up or down by its vertical sign. I'm still weighing whether diagonal-ish tips between 35° and 55° should fire both channels softly instead of being assigned hard.

Now I'm assigning expected ending tips to each digit prototype, starting with the 1 (up at the top, down at the bottom) and the 2 (a down-type tip at the upper left and a right tip at the end).

Now I'm assigning the expected ending tips to each digit prototype, working through the 1, 2, 3, 4, 5, 6, 7 and 9, and noting which strokes have a tip at each end. Once those are set, I'll compute the fully connected weights for each class as a normalised template over the channel, row and column layout.

Now I'm settling the flattened index order for the final layer, then normalising each digit's prototype to a 17.5-pixel centreline height and centring it on the 27x27 canvas.

I'm now sketching the digit prototypes in an upright frame, applying a shear of about 0.15 so they lean right like typical MNIST digits, and starting with the 0 as an ellipse.

I'm sketching the zero as a tall ellipse, roughly 5.7 pixels wide at the centreline after scaling. For the one I'm drawing a straight vertical line with a slight shear, and I'm wondering whether a shear of 0.2 suits the average slant better. Now I'm starting the two as an arc with its centre near the top, beginning at the left.

I'm working out the prototype for the 2 in an upright frame, starting with an arc from the upper left over the top and around the right side, then down toward the bottom-left. I'm also weighing whether the bottom bar should rise or curve, since many real 2s have a small loop there.

Now I'm sketching the 3 as two stacked arcs, the upper one centred near the top and the lower one near the bottom, meeting at the middle. Next I'm starting the 4 with a left stroke running down to a crossbar.

Now I'm sketching the 6 as a large arc whose top stroke starts near the upper right and curves around the left side.

Now I'm working out the prototype for the 6 as a top stroke that curves around to the left and into a small loop at the bottom, and I'm plotting the 8 as a figure-eight traced over the full height.

I'm checking the figure-eight prototype for the 8, where the crossing point and the direction the stroke travels through it still need sorting out. A stroke that starts at the upper right and runs counter-clockwise over the top would cross the centre heading toward the lower right, so the lobe sizes and traversal order have to be set to match that path.

I'm finishing the figure-eight for the 8, with the top lobe about 4.2 wide and the bottom lobe about 5. Then I'm laying out the 9 as a loop at the top with a stem running down from its right side to the bottom.

Still working out the prototype geometry: the 7 gets a steeper diagonal, and the 4 needs its scale set from width versus height. I'm now planning a densify helper that resamples each polyline into short steps with tangent angles, for use in rendering.

I'm checking the direction convention for the orientation channels: a line going up and to the right gives 45°, so the "/" channel is the one at 45°, and the rest follow as horizontal, diagonal "/", vertical and diagonal "\" in order.

I'm writing the template formula for each orientation bank: each cell's weight sums the stroke contributions, weighted by orientation tuning and a Gaussian falloff over distance. Endpoint templates use a similar Gaussian, and the final vector stacks the orientation channels in order.

Now I'm working out the fully connected weights: each class vector gets scaled by a constant and normalised by its length. I'm estimating the typical magnitude of those vectors, reasoning from how much each stroke sample contributes across the grid cells.

Working out the rough magnitude of each class's template vector: summing the stroke contributions per orientation bank gives roughly 25 per bank, and with three banks plus the endings the total norm lands near 7, assuming the amplitude calibration holds. I'm now checking whether that scale is in the right range for scoring the true class against the real features.

I'm checking whether the template for the 1 could dominate, since its normalised vector is concentrated on a few cells and any digit with a vertical stroke through the centre would score well against it.

I'm checking whether the 8 and the 1 would overlap too much, since the 8's centre crossing shares orientations with the 1's vertical-plus-slant template. I'll see how that plays out once I have real data.

I'm checking how slanted 1s would score against the upright template: a 30° lean brings in a strong diagonal response that the template only weakly matches, and that diagonal also shows up in the 7's template, so slanted 1s could drift toward 7 or 2.

I'm thinking about adding a second, more slanted stroke to the 1's template, weighted lower, so that leaned 1s still match. I'm also weighing whether a veto step belongs in the first pass, but I'll start with a baseline and see how it does.

I'm weighing whether to place the second and third banks on shifted grids, one toward the top-right and the other toward the bottom-left, since the right-leaning slant of many digits puts more ink in those corners. I'm not sure the gain is worth it, so I'll compare it against a centred layout, which keeps the columns unshifted.

I'm settling on the layout for the second and third banks, leaning toward a centred column arrangement so the top and bottom bars get finer vertical coverage.

Still working through the bank layout, and I'm settling on banks B at (1,2) and C at (3,2) instead of shifted grids, since the top and bottom bars sit at rows 5 and 22 and those extremes need coverage.

Writing the conv1 weight setup with eight oriented kernels...

Writing the second convolution weights...

Writing the conv2 weights for the three banks...

Still writing the endings weights for conv2...

Still writing the endpoint weights for conv2...

Working out how the tip detectors should cover shallow diagonals: a tip heading about 30° below horizontal still counts as a horizontal end, so the left and right channels pick it up, while the diagonal channel responds partly as well.

I'm settling the template weights for the horizontal and vertical tip types, blending them softly so tips at intermediate angles pick up partial responses from both detectors.

Still writing the weight-setup code for the conv2 endings...

Still writing the prototype preparation code, setting up the shear and bounding-box normalisation for the digit strokes.

Still writing the sampling loop for the prototype strokes, computing the angle and step count for each segment.

Still writing the rendering code, setting up the Gaussian splat parameters for the digit templates.

Still writing the template code, looping over the bank grid and computing the Gaussian weight of each sample at every cell.

Still writing the tip-template code, setting up how each endpoint's angle decides its horizontal or vertical weighting.

Still writing the tip-template code, looping over the endpoint channels and adding each tip's Gaussian response to the matching cells.

Still working out the digit 1 prototypes, with a main upright stroke and a more slanted variant weighted at half strength.

Still writing the digit-2 prototype, with a curved top stroke, a diagonal, and a bottom bar, and I'm computing the arc endpoint directly from the geometry instead of hardcoding it.

Still writing the prototype strokes for digits 3, 4 and 5...

Still working out the digit 6 prototype, with a long arc for the outer curve and a closed loop at the bottom, and checking the endpoint coordinates by hand.

I'm checking the tip direction for the 6's top stroke: the outward vector at the start comes out nearly horizontal, around 14°, but a real 6's top tip should point more upward, so the arc is too flat there.

Still working out the 6's top tip: I'll try an ellipse with its centre moved to (7,13) and a larger radius so the start point sits further round and the outward direction points more steeply upward.

Still reworking the 6's prototype, switching its spine to a polyline that runs down and to the left so the top tip points up and to the right at a steeper angle.

Still writing the digit 7 and 8 prototypes, with the 8 built from a closed parametric curve whose lobes are sized separately.

Still working out the digit 8 prototype, a teardrop-shaped loop per lobe with the widest point near the middle of each lobe.

Still working out the digit 9 and 8 details, checking the stem's attachment point against the loop's right side and confirming the row span.

Still checking the pooling geometry: each pool2 cell's conv2 taps line up with the pool1 cells I expected, so the kernel centres average out to the right spots.

I'm now checking the pooling offsets: each pool2 cell's centre works out to 4i+2ca+3.5 pixels, which puts the ending detectors where I expect. The endings add only orthogonal noise, so they shouldn't shift the class scores, unless they match the wrong templates. I still need to settle the thresholds for the tip detectors against the actual filter response.

Still working out the digit 8 and 9 details, and I'm building the final weight-setup code with the bias and loss settings.

Still writing the conv1 kernels, with four oriented stroke-detector filters whose response falls off with distance from each orientation's axis.

Still writing the prototype strokes for the digits, including the arc helper and the template dictionary.

Still writing the prototype strokes for digits 4 and 5, with the 4's left stroke running down to the crossbar.

Still writing the digit 7 prototype's stroke list.

Still writing the digit 9 prototype and the 1's variant strokes, with the bounding box sized to include the slanted version.

Still writing the prep helper for the prototype strokes, applying the shear to each point before the bounding-box scaling.

Still writing the sampling loop for the prototype strokes, now splitting each segment into steps and computing its angle.

Still writing the sampling loop, now computing each segment's angle and splitting it into steps to place samples along the stroke.

Still writing the template-scoring function, vectorising the Gaussian sample responses and the angle-tuning comparison over the bank grid.

I'm settling on a scale factor of 3 for the loss, and I'm wondering whether the logits will come out too flat or too sharp, though I can't tell yet. The rest of the code looks finished, so I'll write out the final answer and revise it if feedback points to problems.
