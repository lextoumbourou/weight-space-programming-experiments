The 1s get class 0 with a score of 949, so the endpoint detector isn't firing on them at all. I'm wondering whether it's a problem with how the top of a vertical stroke is picked up, or whether "ink" is being summed across the four O's in a way that doesn't line up with a 1.

I'm checking whether the top endpoints of the 1s can even be centered by the conv2 kernel, since the pool1 cells at the top of the stroke seem to fall outside the valid center range (roughly input rows 6.5 to 20.5). If that's right, features at the digit's extremes would need an off-center kernel design to be picked up.

I'm checking whether the corner features at the top of the 7s and 5s can be picked up by a centered kernel, since anything above row 6.5 falls outside the valid range, so those detectors would need an off-center design.

The detector seems to fire at the ends of ink more broadly than I wanted: corners like the 7's top bar, and the tops and bottoms of loops in 4, 9, 5, 6, and 3. That makes it more of a general edge detector than a selective endpoint one. I suspect the lateral penalty is too weak to suppress those cases, and I'm wondering whether the bottom of a loop would look like a continuation upward through its side curves.

I'm rechecking the lateral penalty by hand: with ink on both sides, the 0.38 total still stays under the 1.1 threshold, which doesn't match how often the detector fires in practice. Thick strokes that cover two rows may explain the gap. With only 30 steps left, redesigning the endpoint detector to be off-center and stricter is possible but risky, though it could fix the 1s.

I'm weighing whether to keep refining the endpoint approach or fall back to probing aggregated features, since the top-of-digit detectors are the open question. Accepting around 72–75% and tuning might be the safer path than redesigning under the remaining step budget.

I'm checking whether the top strokes near y≈5 are actually caught: pool1 cell 1 sits at 4.5, which is only at the edge of the neighborhood, so its contribution is weak and lands right at the threshold. The bottom strokes near 22.5–23.5 seem to face the same edge problem at the other end.

I'm considering whether to widen the orientation detectors with a 5x5 neighborhood so the strokes near the top and bottom edges get picked up more reliably, since they currently sit right at the threshold.

I'm considering adding two more features that respond to horizontal bars shifted up and down, so the top and bottom edges of strokes near the digit's extremes get covered. That would give those top bars and bottom bars their own detectors instead of relying on the centered orientation features.

I'm reworking the horizontal detectors into shifted versions, one set nudged up and one nudged down, so the top bar near y≈5 and the bottom bar near y≈23 get covered by their own features instead of sitting at the edge of the centered neighborhood.

I'm shifting the horizontal detectors so the top bar lands at center 5.5 and the bottom bar at 21.5. I'll also check whether vertical features are needed for the left and right extremes, though the column coverage looks adequate already. Next I'll work out the templates for the shifted versions, then go back to step 16 as the base, keeping the two-bar change and replacing the corner features with these shifted ones. Loops get handled as separate channels.

Settling on the shifted-horizontal layout, I'm keeping the pair-based loop detectors as the remaining features.
