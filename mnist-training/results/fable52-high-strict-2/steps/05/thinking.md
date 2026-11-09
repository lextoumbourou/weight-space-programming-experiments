I'm sorting out the counts by column for each digit, starting with the zeros. Their distribution across the a-values is already tallied, and I'm working out where the bottom-H responses for the zeros fall.

I'm checking the up-tip detector on the zeros: it fires for about half of them, and the threshold is low enough that the top arc of the zero seems to be triggering the negative-region cells incorrectly.

I'm checking the digit-1 counts next: nearly all of them land in the a0 column, and the up-tip detector fires for about 85% of them, which looks good. Then I'll start on the digit-2 tallies.

I'm tallying the digit-3 and digit-4 counts by column now, and for the 4s the bottom-H response lands in the 0.5–1.2 range about half the time, with a fair share above 1.2. That mid-range response seems to be leaking in from the crossbar.

Now I'm tallying the digit-5 counts by column: the b=0 and b=1 groups are sorted, and the bottom-H responses for those 5s are the next thing to check.

I'm moving on to the digit-6 tallies, where the up-tip detector only fires about 10% of the time, which is far lower than I'd expect for a 6's top. I suspect its tip sits too high or the spine reads as a shallow slant, so the detector misses it, while the 0s fire far more often than they should.

I'm looking at the digit-7 counts, where the b=0 and b=1 groups are nearly identical and almost all land in the a0 column. The up-tip detector fires for about half of the 7s, which I suspect comes from the corner where the stem meets the top bar, since the horizontal response there is only partial.

Now I'm tallying the digit-9 counts, starting with the b=0 group, where the bottom-H responses are mostly near zero.

I'm tallying the digit-9 counts by column, where the up-tip detector fires for about 69% of them, which is too high for a clean discriminator. I'm also noting that the bottom-H response for 9s lands in the 0.5–1.2 range for roughly 38%, probably from the slanted bottoms leaking into the horizontal channel.

I'm comparing the bottom-H response distributions across digits to find a threshold that separates the present strokes from the absent ones, landing around 1.0. I'm also noting that the up-tip detector is unreliable, firing on 0s, 7s, 8s and especially 9s at rates too high to discriminate well.

I'm weighing whether to make the negative weights on the top rows much stronger, since the up-tip detector is firing on loop tops for 9s and 0s. The 6's top tip is being missed altogether, so the ending detectors need redesigning rather than just retuning the threshold.

I'm checking why the up-tip detector fires on 9s: the stem and loop seem to meet at a top-right corner, a bit like a 7's corner, and that corner may be what's triggering it.

I'm checking why the up-tip detector also fires on 9s: where the loop's top meets the stem, the stroke leaves the corner heading left, and an arc leaving a corner like that could look just like the closed-4 apex. I need stronger inhibition on the row-1 horizontal and diagonal responses to the left of the tip, but that alone may not separate a 9 from a closed 4.

I'm checking the up-tip detector on the 0s and 8s, where the loop tops are tight arcs. The horizontal response is weak there while the diagonal and vertical responses on both sides are strong, so those loops look like isolated tips. I need lateral inhibition that separates a true single-sided tip from an apex with strokes on both sides.

I'm checking how wide the loop top is, since at a shallow depth a round arc is about three pool columns across. That means the far side sits just outside a five-column inhibition window centred on the tip, so lateral inhibition at columns 0 and 4 may not reach it.

I'm working through how the negative weights around the loop top could keep the tip detector from firing on the arc's shoulders, since a point just down-left of the tip would still read as a positive response.

I'm working out the negative region around the loop top: a wider inhibition window, roughly -1.5 across row 0 and the horizontal channel on row 1 for cols 0–4, so the arc's shoulder doesn't count as a tip.

I'm settling on the inhibition: a −2 penalty across row 0 and the horizontal channel on row 1, cols 0–4, so loop tops and the 7's corner stop firing the tip detector.

I'm checking whether the 6's top tip survives the row-0 inhibition, since its tip could land on pool row 0 and get suppressed. Plain orientation tuning on that cell won't separate it, so I'm considering a fully connected layer over the orientation banks to catch top-row tips instead.

I'm settling on a single feature for telling 4s from 9s: whether the top is open or closed. A horizontal stroke across the top links the two sides in a 9 but is missing in a 4, so I'm thinking of a linear unit that rewards its presence for the classes that have it and penalises it for the rest.

I'm settling on the symmetric evidence rule: each stroke item adds a weighted term above or below its threshold, so features that are present push toward the classes that have them and absent ones push the other way. I'm estimating the weight g at around 0.3, with the leak-prone classes near zero.

I'm working out the evidence weights: a ±0.5 separation per feature with g=0.3, which is comparable to the base margin, so with around fifteen features the summed evidence should dominate the template term. I'm checking whether per-class signatures can be set accurately enough, including fractional values for the partial strokes.

I'm now settling the evidence weights per feature and planning to measure more candidate items before fixing their class signatures.

I'm weighing whether to spend the next few steps measuring each feature's per-class signature directly with binary probes, or to estimate the signatures by hand and check the confusion matrix afterward. Measuring is more reliable but slower.

I'm weighing whether to measure each item's per-class signature with binary probes before fixing the weights, or to estimate them by hand and check the confusion matrix afterward.

I'm now settling on a set of evidence items with per-class signatures, starting with a bottom horizontal stroke, and considering whether to organize the features across a coarse grid of locations and orientations instead.

I'm sketching a second stroke-based item for the top of the digit, a horizontal bar near the loop top, and estimating how strongly each digit class would respond to it. Most classes with a top bar should score positive, while 4, 1, and 6 should score negative, though the 9 and 0 values are less certain.

I'm settling the signatures for a middle horizontal stroke and a left-side vertical stroke, estimating how strongly each digit class would respond to them. Most loop-bearing digits should score positive on the middle bar, with 2 and 0 leaning negative, and the left vertical should favour 4 and 5.

I'm sketching a third stroke item on the right side, a vertical near the upper-right, and estimating how each digit class responds. The zeros, nines, threes, and twos should score positive, while the fives and sixes come out negative, and the one is only weakly negative.

I'm adding a lower-left vertical item at x≈9.7 for rows 15–19.5, scoring it per class: positive for 0, 6, and 8, negative for 1, 3, 4, 5, 7, and 9, and leaving 2 near zero. Then I'll add a matching lower-right vertical item at x≈17.7, which I expect to favour 0, 3, 5, 6, and 8 and disfavour 1, 2, and 7.

I'm assigning signatures to a centre-vertical item running down through the lower middle of the digit: it should favour 1 and 7, with weaker positive responses for 4 and 9 from their nearby strokes, and I'm still deciding how to handle 2.

I'm adding a centre-diagonal item running from the upper right down to the lower left through the middle of the digit. I expect it to favour 2, 7, and 8, while the 0's hole and the 3, 5, and 6 lower bowls should score it negative.

I'm assigning a bottom-right horizontal item near the baseline, which I expect to favour 2 and disfavour 3, 5, 0, and 6.

I'm sketching a fourth item, a diagonal running from the centre down to the lower left, which I expect to favour 2 and weakly suit 7, while 3, 5, and the 1, 4, and 9 classes would score it negative.

I'm sketching an item for the left side near the top, a horizontal bar around y≈6, and estimating its signature: a 7 should respond strongly, while 5, 2, and 3 should respond weakly to it. The 9 and the 0 are still unclear, with the 0 leaning slightly negative.

I'm now sketching a top-right horizontal item for the end of the 5's bar, and noting that it would overlap with the top item I already have, so I'm considering whether it adds anything.

I'm checking the top-bar item against the 5 and 7, then weighing it against the 6, 4, and 1, which should score negative. The 2, 3, 9, and 0 might leak into it through their top strokes, so I'll keep its weight small. For 5 versus 6 and 5 versus 8, the lower-left vertical and the top bar already separate them, so this item adds little there.

I'm weighing whether to keep the tip detectors in the templates at their current weight, since they fire on too many wrong classes, or to redesign them with stronger inhibition and drop them from the evidence items for now.

I'm now writing the tip-detector kernels with negative inhibition: the row above and the row below each tip get penalized so the ends stop firing on neighbouring strokes. I'm checking that the true tips of the 1 and the 4 still keep most of their response, and I'm starting on the left-end version.

I'm adjusting the tip detectors so the wider inhibition covers the rows and columns around each tip, and I'm assuming the true tips still keep most of their response. I'm then turning to the weights: with about eleven evidence items at a small gain, each one can only nudge a class score a little, but across the items where two classes differ those nudges add up to a usable margin.

I'm weighing whether to measure each evidence item's signature with a few probe steps before tuning weights, treating the feedback as a rough training signal for log-odds weights. I'm checking that this stays within the rules, since the feedback is the only information I get about performance.

I'm deciding not to probe every evidence item to estimate its statistics, since that would amount to fitting on validation labels through a side channel. I'll set the signatures by hand and use only the ordinary classification feedback, with the evidence logit as the sum of the gains times the signatures times the difference from each threshold.

Now I'm writing out the signature table for the bottom-horizontal, top-horizontal, and middle-horizontal evidence items, with a small gain and per-class weights, and I'm starting on the upper-left vertical item.

I'm writing out the evidence signatures for the lower-left vertical item, giving the zeros, sixes, and eights positive weights and the sevens and nines the strongest negative ones.

Continuing the signature table, I'm now setting the weights for the middle-right horizontal item, which should favour the 4 and penalise the 9, 1, 2, and 7 through its inhibition term.

I'm checking the 2-versus-3 pair: the bottom-right vertical item and the lower-left diagonal both lean toward 2, giving it a margin of roughly half a unit over 3. Next I'm moving on to the 4-versus-9 pair, where the top horizontal item should separate them.

Now I'm checking the 4-versus-9 pair, which is the hardest one: the top horizontal item separates them only by about 0.25 to 0.3, and in the earlier step the 4→9 confusions were much more frequent, so I'm questioning whether the tip detectors were what drove that.

I'm checking the 4-versus-6 pair next, where the top-right vertical and lower-left vertical items should separate them, and I'm weighing the lower-left evidence against the bottom horizontal.

I'm checking the 7-versus-3 pair next, where the bottom-horizontal item should do most of the separating.

I'm checking the 9-versus-3 and 9-versus-6 pairs against the evidence items: the top-right vertical and lower-left vertical separate 9 from 6 by roughly 0.3 each, and the bottom horizontal helps with 3. I'm also verifying the 0-versus-6 pair, where the middle-horizontal and top-right vertical items give a margin of about 0.3, and I'm starting on the 5-versus-6 comparison.

I'm checking the remaining confusable pairs against the evidence items: 1 versus 5, 2 versus 8, and 3 versus 8 each separate by roughly 0.2 to 0.3 on the upper-left and lower-right verticals and the lower-left diagonal. The 1-versus-2, 6-versus-1, 4-versus-1, and 8-versus-1 confusions still need weights that keep the 1 well apart from these neighbours.

I'm working through the bias term for the 1 class: with the absent-feature contributions summed, it comes out near +1.0, which is fine for 1 images but needs to stay in check for the other digits. I'm also considering how the scale factor α should be set.

I'm settling on the scale factor: 3 would make the evidence swings large enough that wrong classes come out overconfident, so I'm considering 2.5 as a safer setting. I'll keep 3 for now, since the margins should hold, and I'm also dropping the old vetoes from step 3 in favour of the symmetric evidence items.

I'm setting up the lowcentre vertical item with orientation detectors at two angles so slanted stems register too, and I'm starting to code the evidence list.

I'm writing the final code for the evidence items, with the lowcentre vertical's V-only stroke at a lower threshold and the middle-right horizontal set to partial-length detection.
