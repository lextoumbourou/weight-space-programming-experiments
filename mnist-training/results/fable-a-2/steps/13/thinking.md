I'm comparing the unclipped and clipped results: the unclipped model scores a bit better on loss but worse on accuracy. Clipping seems to buy roughly 0.055 in loss and 2% in accuracy, and I think adding six more channels of features could gain more than that. I'm wondering whether I can get bounded features from a single channel by reshaping the dynamic range instead, though without a cap that's harder to pin down.

I'm considering a "absence" channel built with ReLU, but it isn't bounded: when a veto is present the value grows large, and a max-pool over it would track the wrong thing. So bounded features really do need clipped pairs. Sixteen channels means four line templates plus six pairs, so adding features means trading something away. I'm weighing keeping the four line channels against replacing them with binary detectors, and I'd test the line templates' contribution first by setting their weight to zero.

I'm checking whether saturation can come cheaper by clamping the feature in conv1, since the edge maps are already bounded in [0,1]. The loci sum over the ray cells only spans about a 2× range, though, so a single-cell reading would mostly lose the wall-distance tolerance I need.

I'm sizing up how much per-cell range the loci sum contributes, since a full wall gives roughly 2.8× variation. Narrowing that could do some of the clipping's work, but the count of firing cells would still vary.

I'm testing whether a narrower edge filter could make the conv1 response nearly constant across a wall, so that only about one cell fires at a steady level. The idea is that a sharp edge would give a stable sum and a soft edge would still produce a usable but lower value.

I'm weighing whether clipped feature pairs are the only route to bounded features, since the edge-softness and per-cell range tweaks only narrow things to about 2×. Then the real choice is between twelve unclipped features and six clipped ones, and I lean toward the unclipped set, though I'm not certain. I'm also considering dropping the four line-template channels to make room for eight clipped features, or mixing six clipped with four unclipped.

I'm wondering whether the cosine line templates are pulling their weight: zeroing their weight would show how much accuracy they actually contribute. If they add little, replacing them with measured binary detectors could be the better use of the budget, but I'd need to estimate how many probe steps that takes against the remaining 38.

I'm thinking about which unmeasured regions and finer row resolution would sharpen the detectors, and I'm sketching three new line-based detectors: a long horizontal bar, a long vertical stroke, and a long diagonal, each aimed at particular digits.

I'm weighing whether to drop the four cosine line templates and reuse those channels for measured binary detectors, since the hand-drawn templates may be weaker per channel. Options include long horizontal, vertical, and diagonal strokes, or an X-crossing at the centre. That would give 4 unclipped new features or roughly 5–6 clipped loci features in the same budget.

I'm weighing whether to spend the next step on an α=0 test of the clipped setup, which would show how much accuracy the cosine line templates contribute before I restructure the channels. If they add only a few points, replacing them with measured detectors is the better use of the budget.

I'm weighing whether the next step should probe the remaining regions for the existing six loci features. Either way, since more measured rates per feature don't need new channels, that seems worth doing regardless of whether the line templates turn out to matter.

I'm now considering which outer columns to measure for the six loci features, since those regions don't need any new channels. The catch is that the left-edge position only fires for narrow digits or indented strokes, so I'd need to check which features actually reach those columns.

I'm looking at the outer columns next, since the left and right edges might catch narrow digits or indented strokes that the centre misses. Then I'm thinking about splitting the centre features into finer row bands, which would add more measured rates without needing any new channels.

I'm weighing which top-of-digit cues could separate 4 from 9 and 8, since the current features only capture the top closure partially. A detector for a horizontal bar at the top centre, or an unmeasured top-region ray test, might help.

I'm weighing how to tell a 4 from a 9 at the top: a 4's top is open with two prongs, so there's a gap between them with walls on both sides and nothing above, whereas a 9's loop is closed or filled, which blocks that upward opening.

I'm working out why a 9 might read as "floor below, open above" at top-centre about 44% of the time: the loop's top probably sits low enough that the probe falls above it. Since 9s get shifted down by their centre of mass, that would explain it, though finer row resolution may not separate the two digits.

I'm weighing a cup-shaped detector for the top of the digit: walls on both sides with nothing above. That should favour 4 over 9, since a 9's loop has no side walls above it, though the threshold and the upward veto would need tuning to keep it from leaking.

I'm checking whether a detector for a left-side wall at the top-centre could separate the 7 from the 9, since the 7's top is open on the left while the 9's loop sits there. Its measured rate is .63 for 7 and .11 for 9, which looks like a strong split.

I'm weighing whether the 7-versus-9 split from the top-left wall is enough, since 37% of sevens lack that cue and could be misread. I'm considering whether a line-energy detector for the upper-left quadrant would add independent evidence, but with no free channels it would have to be measured directly.

I'm considering whether the line channels could feed a continuous Gaussian model instead: thresholding their smoothed region sums at some τ gives per-class probabilities, and from those I could back out class means and derive a linear weight for the continuous score.

I'm working out how to turn the line-region energies into a Gaussian classifier, where two thresholds on one scalar would give both its class-conditional spread and each class's mean. That would mean 24 scalars, about 12 steps.

I'm weighing a Gaussian model on the line-channel energies, where two thresholds on one scalar would recover each class's mean and the spread, at the cost of roughly 24 scalars in about 12 steps.

I'm going through the remaining line-region detectors: a bottom horizontal stroke, a middle horizontal bar, and vertical strokes in the upper-left and upper-right quadrants, each with a list of digits it should favour or exclude.

I'm listing the remaining line-region detectors: a vertical stroke in the lower-left and lower-right, a centre column, and diagonal strokes in the lower-left and centre, each with the digits it should favour.

I'm estimating the threshold scale from the stroke energy at the pooled level, working through how the smoothing kernel weights a vertical stroke across the centre and side columns.

I'm estimating the threshold scale from the region sums: a vertical stroke passing through a 2×2 block should total around 2, and an empty block stays under 0.3, so thresholds near 0.6 and 1.6 look workable.

I'm working out how to calibrate the thresholds for the line-energy probe, guessing roughly 0.5 and 1.3 for a single row band, and then checking how the two probit values give the spread for each class.

I'm settling on a Gaussian-style calibration for the line features: two thresholds per region give each class's mean and a shared spread, which yields a linear weight. Next I'll test two concrete probes, a horizontal stroke across the top-centre and a vertical stroke in the upper-left quadrant, each with its own pair of thresholds.

I'm settling on a probe that uses the step-11 convolution over channels 0–3, with a 3×3 encoding where each cell's index is 3 times the first bit plus the second. I'm checking that the top row covers stroke heights from about 5 to 10, so it still catches digits whose tops shift with their centre of mass.
