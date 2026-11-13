The 8 class is being over-predicted: 1308 samples land in column 8, and several transitions into it (4→8, 6→8, 2→8) are heavy. The loss got worse at 0.7256. The Z magnitudes seem to vary too widely, so the unclipped linear zone features look like the culprit, with some samples producing large Z values that let 8 win. I think the zone features need saturation. The Z_TYP setting between 0.6 and 0.33 gave the best result around 0.45, but the underlying signal still looks noisy.

I'm weighing whether conv2 channels can give a saturating zone feature instead of a raw count, since per-cell clipping would need two channels per type and only four are free after dropping the hole channels. A clipped per-cell response still sums to 1–3 firing cells per zone, so it cuts variance without making the feature binary. I'm also considering a larger pooled window so one zone maps to roughly one cell, though I haven't worked out whether a 5x5 max-pooled kernel can act as an OR over that area.

I'm considering whether a 5x5 window over the pooled features, clipped with a threshold, could give each final cell a binary "corner present nearby" value. The trouble is the windows overlap heavily, and the upper-zone window would spill past the rows I actually measure, so the zone sums still wouldn't be clean.

I'm thinking about whether a zone-level binary can come out of this at all. Since the FC layer is linear, the final features have to be binary per cell and the zone sum just counts them, so the only route is making the conv2 window large enough that each cell's feature already covers a whole zone.

I'm checking whether a 5x5 window over the pooled map lines up with the zones: each final row would cover roughly the upper or lower band of corners, so the zone sums might become cleaner.

I'm working out that splitting the zone into two disjoint 12-pixel windows, one on the left and one on the right, would cover every column. That would give each zone a pair of binary quadrant features, though when both fire they'd still add up to 2.

I'm settling on quadrant-level binary features as the workable route: two disjoint 12-pixel windows per zone, summed to get a count of 0 to 2. The catch is that my measurements are per zone, not per quadrant, and dropping the hole detectors to free the channels will cost the roughly 2% they gave me.

I'm looking at whether the conv1 corner response could be saturated at the source: if the filter weights are scaled so the output clips naturally, the zone features would become bounded without needing extra channels. I'm also weighing whether dropping the hole channels to fit more corner channels is worth the roughly 2% they contributed.

I'm checking whether a single conv2 channel can saturate on its own: compute the corner-window sum and clip it at a threshold, so the feature is bounded without spending two channels per type.

I'm realizing that a single channel can clip from above on its own: the corner-window sum is always nonnegative, so relu(c − S) yields min(S, c) when subtracted from c. The max-pool then turns this into an intersection of shifted windows rather than a union, which only shrinks the effective window slightly and is acceptable.

I'm realizing the clipping can be done with a single channel per feature: since the window sums are nonnegative, subtracting them from the clip ceiling gives a bounded "absence" value that drops to zero when a corner is present. That would halve the channel count for the orientation features too, though the lower threshold needs checking so the output doesn't overshoot when the sum is below it.

I'm checking whether the clipping can be done with one channel instead of two: a channel that outputs the clip ceiling minus the window sum gives an absence value, and the max-pool then becomes a minimum over shifted windows. That would mean an intersection rather than a union, which only shrinks the effective window a little, so the saving on channels looks worth it.

I'm seeing that a min over shifted windows gives an intersection rather than a union, so each cell becomes a crisp, roughly non-overlapping 4x4 block that only responds when the stroke sits in its central band. That would make the template win function narrower, with a flat core and a taper beyond it.

I'm checking whether a 5x5 box with absence coding recovers the old 8-pixel cell coverage, since the min over the four shifted windows should match a 4x4 intersection. The sums are bigger over that wider window, so the min only bounds presence from below rather than matching it exactly.

I'm checking that the clipping works in the other direction too: a single absence-coded channel, relu(C − S), gives min(S, C) after subtraction, so it saturates from above with one channel instead of two. Taking the min over the four shifted windows yields roughly the intersection of their coverage, so with a 5x5 box the cells should keep their 8-pixel reach and the sums just need a slightly higher ceiling, around 1.8, to saturate properly. That would bring the orientation features down to four channels and free the rest for corners.

I'm planning to keep orientation at four channels with absence coding, and to give corners four quadrant-binary channels using a 5x5 window. That leaves the hole detectors at four and four more channels free. The corner statistics I measured were for the upper and lower zones, so these new quadrant features won't carry those numbers over directly.

I'm working out how to align the kernel rows so the intersected windows land on the upper and lower zone bands, rows 6–13 and 14–21.

I'm working out how the zone bands line up with the pooled rows: the intersected windows cover pooled rows 1–4 and 5–8 at different offsets, which puts the splits near rows 4–11 and 12–19 rather than exactly at the 6–13 and 14–21 zones I need. I'm weighing whether shifting the kernel rows can bring the upper and lower bands into alignment.

I'm testing whether the kernel rows can be shifted so the intersected windows line up with the zone bands. A 4-row kernel subset gives intersections at pooled rows 2–4, 4–6, 6–8, and 8–10, which still doesn't split cleanly at the image center around row 14.

I'm testing whether two cells of two rows each could line up with the upper zone's pooled rows, since a single four-row cell can't land exactly on rows 2–5.

I'm checking whether a single channel with a 3x3 box and absence coding gives an intersection equal to the 2x2 pooled cells I already measured, which would keep the same binary cell features. Getting a zone-wide binary from one cell doesn't work, since a single cell can only span four pooled columns.

Checking whether the corner cells can stay as they are while I add the quadrant features on top, since re-aligning the windows to the measured zones would shift the statistics I already have.

I'm checking whether a 3x3 box with absence coding keeps the same 2x2 cell region as the current max-pooled corner features. The four overlapping windows would make the feature roughly a clipped sum over that central block, rather than a plain maximum.

I'm weighing whether the clipping can use a soft threshold, so a small corner response still registers a little instead of being cut off entirely.

I'm settling on a soft-binary cell feature: a clipped window sum that ramps from zero up to a ceiling of about 0.4, so a weak corner response still registers partially. Summing those over the eight cells gives a zone count that should land around 1 to 2 when the zone fires.

I'm weighing whether a zone count built from these cell features would be better than the raw zone magnitudes, since it might keep the measured zone statistics. The concern is that the count over-counts when two or three cells fire together, so a simple weighted sum may still carry about a twofold spread.

I'm weighing whether capping each cell's contribution at a higher ceiling would keep the zone count closer to the raw magnitude for small masses, so that a blob straddling a cell boundary doesn't double-count.

I'm considering a different option: instead of the same cell grid, I could use quadrant cells starting at pooled rows 1 and 5, which puts the split near row 12 rather than the measured 14. That shifts the zone boundary, so I'd have to remeasure, but it might give cleaner binary features than the soft clipped sums.

I'm weighing whether the zone boundaries can be matched exactly with a shifted kernel, since a four-row kernel subset puts the intersections at the wrong offsets for the upper zone. Maybe the zone features will need re-measuring if the boundary can't be aligned.

I'm weighing quadrant-binary cells built from a 5x5 window with absence coding, four corner types across each quadrant. The 16 overlapping cells would give 64 binary features, while restricting to the non-overlapping rows and columns 0 and 2 gives four quadrants but leaves rows 20–23 uncovered.

I'm settling on Plan A for now: keep the four corner channels, but compute each cell's response as an absence-coded 3x3 window sum with a soft ceiling around 0.4, so weak corners still register partially. The zone count would then be a sum over those eight cells, normalized against the measured zone statistics.

I'm setting up the absence-coded corner cells: each 3x3 window is subtracted from a 0.4 bias and passed through a ReLU, then max-pooled to a presence value. The zone count then becomes eight minus the summed activations scaled by 0.4, and the weight on each cell gets folded into the zone term for each class.

I'm checking whether the intersection claim holds for the 3x3 box: a blob in the central two rows of the window counts in all four overlapping windows, but one sitting just outside that core only registers in some of them, so the minimum drops it.

I'm setting the cell response so a blob split across two rows still registers, and estimating about 1.5 cells firing per fired zone as the normalizer.

I'm working out whether a soft per-cell threshold can stop diagonal-stroke responses from adding up to a false presence, since their small corner values could sum past the cutoff across neighboring cells.

I'm lowering the corner bias from −0.9 to −1.05 so each corner response is shifted down by 0.15, and I'd bring the hole threshold down to 0.9 to roughly compensate. The approximation isn't exact for weak responses, but it should be close enough that the hole detector fires about the same.

I'm settling the corner threshold at 0.25 and shifting the conv1 corner bias to −1.05 so weak diagonal responses stop counting, with the hole threshold dropped to 0.9 to compensate. The zone count will be a normalized sum over the absence-coded cells, and I still need to pick the per-class gain before writing the loop over zones and rows.

Still writing the feature weights...
