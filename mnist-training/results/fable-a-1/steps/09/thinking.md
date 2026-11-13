The mixture templates only moved accuracy slightly, from 77.8% to 78.2%, and the loss got a little worse, so this isn't the big gain I hoped for. Maybe the naive Bayes setup is the real limit with these blurred templates, or my templates are still off. Looking at the confusions, the 2→3 and 2→8 errors are both above 140 cases, and 3→5 is similar.

I'm looking at the remaining confusion pairs, like 4→9, 5→6, 6→4, and 8→9, to see where the errors cluster. Nothing I've tried so far has produced a big gain, so I need a different approach. Naive Bayes on these features seems capped, and a discriminative method would do better, but I can't train one, so I'm weighing what hand-tuning could still achieve.

I'm weighing whether pairwise tweaks along the naive Bayes difference direction could help, but they'd also shift scores against other classes. A better bet might be richer features like stroke endpoints and the direction of open cavities, which carry more of the hand-knowledge into the decision.

I'm working out how to detect open cavities by pairing corner responses: a right-closed cavity from stacked top-right and bottom-right corners, and similarly for the other three orientations. A relu over the summed corner pair would fire only when both are present. The full loops would also trigger these pairs, so the fully connected layer would need to subtract hole evidence to keep them apart. I'm also considering how the cavity features would separate 3 and 5, which each have a right-facing opening.

I'm checking which cavity-direction pairs separate 4, 2, 6, and 0, since the open-top corner pattern looks especially strong for 4.

I'm now checking whether the remaining cavity directions can separate 3 from 5 and 2 from 3, since 3 has an opening on the right in its lower half that 2 lacks. The corner pairs could carry that distinction, but all sixteen channels are already in use, so I'd have to shrink the hole detectors to free up room.

I'm weighing whether the hole detectors could be trimmed or the orientation clip dropped to free up channels for cavity-direction features, since all sixteen are in use.

I'm weighing whether to tune the representation itself, since the model is capped by its features. Four candidate knobs are on the table: the softmax temperature, the P squeeze, the conv2 box size, and dropping the orientation clip. My concern is that I have 42 steps to spend on these, and I can only learn from the feedback each one gives.

I'm weighing whether to measure aggregated, semantic quantities instead of estimating every parameter, since I already used diagnostic feedback for the hole feature and this would be a similar, smaller step. The most useful measurements per step are probably the new corner and cavity features, and I'm considering a handful of them, perhaps eight.

I'm considering measuring the new semantic features, like the cavity directions, to see how they behave on the data. Since I already used diagnostics for the hole feature, that seems like a reasonable next step. I'm also thinking about whether to free up channels by trimming the hole sizes or dropping the orientation clip, since all sixteen are in use.

I'm considering dropping the orientation clip, so the features stay unbounded. Scaling the relu'd response by 1.2 or 2.4 would keep the evidence from varying too much with stroke strength, though there's a few-percent accuracy risk to weigh.

I'm weighing whether to drop the clip and rescale the response, since that could free four channels, and I'd test it in one step. The other route is to make the pooled cells act as presence detectors, so that the final max-pool does the job of counting rather than a box sum measuring stroke length.

I'm working out how the pooling coverage would work with a two-tap kernel, checking which pooled rows each tap reaches so the digit edges near rows 4-5 and 22-23 aren't missed.

I'm checking whether dropping the clip and using a tent-shaped kernel over three pooled rows would keep the orientation evidence in a bounded range, roughly 0 to 2, so the scores stay stable across stroke strengths.

I'm trying a tent-shaped kernel over three pooled rows with no clipping, so the orientation evidence stays roughly bounded without spending channels on the clip. I'm estimating the scale by hand: a fully aligned crossing gives about 1.4, plus some spillover from neighboring columns, so I'd divide by about 1.5 to keep typical presence near 1.

I'm working out whether the cavity detectors can share the freed channels: if the corner pair fires when both the upper and lower corners are present, a single strong corner on its own might still trigger it, so the threshold has to sit above that single-corner level, but typical two-corner sums are only slightly higher, which makes the margin tight.

I'm weighing whether raw corner-presence maps for the four corner types, pooled to a 4x4 grid, would serve as semantic features more cleanly than conjunction detectors, since a single strong corner and two typical corners barely separate under any threshold. Corner type alone already carries shape meaning, like an upper-left inner corner showing up in 5 and parts of 6.

I'm now checking which corner types show up in each digit: top-left corners for 5 and 6, top-right for 7, 2, 3, and the loops, and a bottom-right-facing corner at the 4's bar-stem junction.

I'm going through which corner types appear in each digit, now looking at the bottom-left corners for 4, 6, 2, and the loops, and the bottom-right corners for 3 and 5.

I'm comparing the corner-type maps as features, since each corner type already carries shape meaning: the upper-right corner separates 3 from 5, the bottom-left corner marks the 2's neck, and the bottom-right corner distinguishes 2 from 8.

I'm considering a single-tap version that keeps the corner channels as-is, though that only covers the interior rows and misses the edges, so I'd need to check coverage again.

I'm sketching how the corner features could come from the stroke geometry itself, working out where a turning path gives an inner corner on each side.

I'm working out how the corner types follow from the stroke geometry: a curve's inner side points toward its center of curvature, so the corner type is set by which quadrant that center falls in. I'm also checking how junctions would fit into the same scheme.

I'm thinking about hand-annotating corner positions for each digit shape and rendering them into templates, since junctions like the 4's bar-stem join don't come out of a single curve's geometry.

I'm weighing whether to annotate corner positions by hand for each digit shape, since junctions like the 4's bar-stem join don't come out of a single curve's geometry. Measuring the actual corner responses on real digits would be more reliable than trusting my semantic reasoning, but for now I'm thinking the placement only needs to be within a couple of pixels, which the cell size allows.

Next I'm weighing whether to test the tent-shaped orientation kernel without clipping on its own, or to change the corner features at the same time. Changing both would make the result hard to read, so I'm leaning toward the single change.

I'm sizing the tent kernel against a stroke: when a vertical stroke sits in the central column, its summed response is about 2A, with some spillover into the neighboring column. I'm picking a normalization of 1.5 and a threshold of 0.2, so a typical present stroke lands near 1, though a stroke at the edge of a cell's coverage would come out weaker.

I'm now checking the coverage of the tent kernel in pooled space: the central pooled rows get full weight and their neighbors half weight, so a stroke falls within roughly ±2 input rows at full strength and tapers out to ±4. That means the template window should narrow to full weight within about ±2.5 and fade to zero by about 5.5, rather than the current ±3 flat with taper to 6.

I'm settling on the next test: switch the orientation kernel to the unclipped tent version and leave everything else alone, then compare against the 78.2% baseline. I'm also keeping the bias adjustments at zero so the comparison stays clean.
