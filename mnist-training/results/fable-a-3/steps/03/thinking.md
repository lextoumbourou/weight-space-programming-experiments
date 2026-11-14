The model's now at 69.6% improvement with loss down to 1.128. The biggest remaining error is 2→3 at 373, followed by 4→9 at 230 and 0→2 at 162, with a tail of smaller confusions across the other digit pairs.

Next I'm checking the 9→3 and 9→7 confusions, then 7→9. I'm still stuck on 2→3, so I'm wondering whether my 2 template is off or whether the 3 template is matching 2s. I'm picturing the average MNIST 2, with its top arc, right descent, diagonal sweep to the lower left, and heavy base, and asking what real 2s contribute that my 2 template is missing.

I'm working through whether the 2's diagonal stroke through the centre matches anything in the 3's structure. The upper-right centre "/" is shared between the two digits, so the distinguishing feature has to be the 2's lower-left diagonal near x=8–12, y=16–21, where the 3 has a "\" and a horizontal end-stroke instead.

I'm now checking whether the diagonal filter is responding weakly to the 2's "/" stroke, which would make the 2 look more like a 3 with only a top arc and bottom bar. I want to verify that by working out the filter response for a normal diagonal stroke.

Now I'm checking how the diagonal filter responds to a clean 45° stroke, tallying the weighted pixels by their distance from the line to see whether the sum comes out strong or weak.

I'm checking the diagonal filter numbers again for a thicker stroke, and it still comes out above threshold, so the filter itself probably isn't what's causing the 2→3 confusion. I'm now turning to what the average MNIST 2 looks like, with its top arc, bottom-left blob, and long horizontal base.

I'm now weighing how much the 2→3 mismatch costs in the Bernoulli part: a missing lower-right vertical on a 2 only adds about 0.16 in log-likelihood at α_B = 0.08, which seems too small to explain 373 errors.

I'm weighing whether raising the Bernoulli weight from 0.08 to 0.2 would help, since the current loss of 1.128 at about 70% accuracy hints the model may be underconfident. I'm inclined to test that change, and possibly combine it with other adjustments, even though that makes it harder to tell which change is responsible.

I'm weighing whether the one-class bias toward 1 comes from its sparse expectations: a 6 or 4 with features displaced from the template would then lack many of its own class's expected features, and since the 1 template expects few, it picks up fewer penalties for absence.

I'm considering whether the 1-class pull comes from sparse presence: real digits would then show fewer of the template's expected features than predicted, which favours the class that expects the fewest. One fix would be an asymmetric probability, where a missing expected feature costs less than an unexpected present one, with expected features realised around 70% of the time. I could also try lowering the presence threshold so real strokes register more often.

I'm considering which features would separate the confusable pairs, like 4 and 9, where a 4's two upward-pointing top endpoints could be a distinguishing cue, and 2 versus 3, 0 versus 2, and 6 versus 1 or 5. The unused channels might capture position-specific presence that would help with those.

I'm now looking at endpoint cues to tell apart the confusable pairs: a 3's left-pointing ends at top-left and bottom-left versus a 2's bottom-right end, a 5's right-pointing top-right end against a 3's top-left, and a 4's two upward tips against a 9's none. Zeros and 8s have no endpoints at all, while a 6 has one at the top and a 1 has both top and bottom ends. Detecting those ends in conv2 from the M maps would mean checking horizontal cells where a stroke stops.

I'm sketching a right-end detector for the endpoint cues, starting with a horizontal kernel on the H channel that fires where a stroke stops, with the stroke ending just before it.

I'm sketching the right-end detector as a horizontal filter on the H channel, with three cells in a row firing and a penalty from the empty columns to the right. Any stroke that turns a corner or meets a junction will have other orientations lit there, so it won't count as an endpoint. The catch is that the H response fades a little before the true tip, so the detector may fire slightly early.

I'm checking the right-end detector against the V filter's response at a stroke's cap, which comes out below threshold, so a horizontal tip won't be picked up by the wrong orientation. I'm also noting that curved endpoints, like the ends on a 3 that arrive at a diagonal, will need separate handling.

I'm trying to pin down what would count as a left-pointing end without relying on a specific stroke orientation. The idea is to check for any ink in the window: where the mass sits in the right half around the centre row, and where there's none on the left, that marks a left-facing boundary.

I'm trying to detect a left-pointing stroke end by checking for ink at the centre with nothing to its left, but I need to exclude vertical strokes, which would also show that pattern. So I'm looking at whether there's ink above and below the tip in the centre columns, since a true horizontal-ish end shouldn't have any there.

I'm now comparing 2 and 3 by the features that should differ: a lower-left diagonal for the 2, a lower-right vertical for the 3, and the middle horizontal and bottom base where they diverge.

I'm now estimating the Bernoulli vote gap between a 2 and a 3: with roughly 15 differing features at weight 0.08, that's only about 2.4 logits, and the cosine term adds roughly 3 more, so a perfect template-2 should win by about 5. Yet 40% of real 2s still land on the 3 template, which means real 2s must sit far from my template.

I'm wondering whether real 2s are just much wider and more varied than my template, with a looped bottom-left, a curved diagonal, and a base that can stretch far in both directions. I'm also considering whether my templates sit a couple of pixels off from where real digits actually land, since many 2s nearly fill the box horizontally.

I'm checking whether the templates for 0, 2, and 4 are too narrow, since real digits like these often run wider than what I've modeled. Zeros keep getting labeled as 2s, probably because a wide bottom stroke matches the 2's base while the sides fall outside my template, so widening those three should help.

I'm checking whether the zeros are being pulled toward the 2 template because my 0 template is too narrow: real zeros with wider sides would land outside the modeled columns, leaving the wide bottom stroke to match the 2's base.

I'm working out why zeros get labelled as 2s: my 2 template's top arc, diagonal and base overlap with a slanted zero's long diagonal sides and top and bottom strokes, so the cosine term favours 2 even though the zero's left side is missing from that template.

I'm thinking the 0 template may need a steeper slant, since real zeros often lean 20-25° and their sides then read as diagonals that look like a 2's stroke. One fix is to loosen the orientation tuning in the templates so they tolerate these variants, rather than averaging samples.

I'm settling on a plan for the next step: loosen the Bernoulli weights, blur the template's orientation tuning so intermediate strokes partly count for both neighbouring digits, and nudge the default slant up to about 11°. I'll also check whether any new long-range channels are worth adding.

I'm weighing whether a few more feature channels, such as endpoint detectors in four directions or hole-like cues, would give more than fine-tuning the templates. Tuning might get this approach to around 80-85%, but getting past that would need discriminative information from data, and I only have confusion counts to go on. Still, the additional channels seem worth trying if they can be built robustly.

I'm now considering whether a few more specialized detectors, like top and bottom arcs, corners, and junctions, could capture stroke shapes that the simple orientation channels miss. An X-crossing detector, for instance, would fire where both diagonal orientations meet at one spot, which would help separate 8s and 4s.

I'm now considering co-occurrence features, like a "+" crossing where a horizontal and vertical stroke meet in the same cell, which would help pick out 4s. A plain sum over a region would blur that AND condition, so it would need a per-cell combination, though that leaves coverage sparse after pooling.

Next I'm checking whether a single-cell AND feature, like a crossing of horizontal and vertical strokes, can be picked up anywhere in the central pooled grid, and whether the 4's crossing falls inside that coverage.

Checking how the horizontal filter responds at the junction where the crossbar meets the stem of a 4, since its response drops when only half the filter overlaps the stroke.

I'm testing whether a three-tap horizontal kernel centred on the stem, combined with a vertical tap, gives a usable AND: the sum should only go positive when the vertical stroke is present and at least some of the horizontal neighbourhood is too.

I'm now checking how a "/" stroke and a "\" stroke would both respond at the same cell, since that crossing should mark the waist of an 8 and the diagonal filters might only partly fire there.

I'm checking how the diagonal filters respond at the exact point where a "/" and a "\" stroke cross, since that's the waist of an 8. The sums come out negative there, so the "/" filter barely fires at a perfect crossing.

I'm considering row and column projections as another option, counting how many separate vertical strokes cross a horizontal line. That would separate 0s, 1s and 8s, since each has a different stroke count at mid-height.

I'm weighing whether pooled-cell AND features are worth the trouble, since a crossing can land between cells and the diagonal responses weaken right at the junction. That leaves me leaning toward improving the templates through reasoning and feedback, which is likely the more efficient route, and I'll decide whether to run per-class experiments after addressing the global structure.

Now I'm going through the typical shapes of each digit to check my templates, starting with the 0, which I think leans a bit to the right, and the 1, which varies in slant. For the 4 and 5, I'm placing the strokes by rough coordinates, like the left arm, crossbar and stem of the 4, and the top bar and bowl of the 5.

Now I'm weighing the Bernoulli part against the cosine term: I'd raise its weight from 0.08 to 0.16 while keeping alpha at 0.3, which roughly doubles the Bernoulli share and scales the overall logits up, since the earlier jump from 60% to 70% came from adding that term.

I'm settling on alpha at 0.25 and raising the Bernoulli weight to 0.16, since the loss hints the scale is a bit low. Next I'm planning to broaden the Bernoulli template with a soft orientation tolerance, so strokes at moderate angles count partly toward the digit.

I'm working out how to soften the Bernoulli template's orientation response, since a full-strength soft brush would make a vertical stem also predict both diagonals, so I'm considering applying the softness after saturation instead.

I'm settling on a soft version of the Bernoulli template, where each orientation counts as "maybe" whenever a neighbouring orientation is present at that cell, so a vertical stem doesn't also predict both diagonals. The half-strength neighbour rule lands the mid-probability near the don't-care level, which is the behaviour I want, though I'm not yet sure a neighbour is a good enough cue for a stroke's orientation.

I'm checking whether penalising V strokes for a "/" neighbour would let slanted zeros still fit the 0 template, and whether the 2 template would then wrongly accept them. The top-left and right-side strokes look fine for 2, but the bottom-right corner is where the 2 template expects something different.

I'm thinking about whether an empty centre could separate 0s from 2s, since a zero has no ink in the middle while most other digits do. I'd need a channel that reports whether any orientation is present in the central cells.

I'm testing whether a narrow 3x3 centre channel, flagging the absence of any orientation ink in the hole, could tell 0s apart from 2s, since a zero's inner hole is roughly 6-8 pixels wide and should stay empty.

I'm checking whether an empty centre window could separate 0s from 2s, testing a 6x6 pixel window in the middle of the digit against the hole a zero should have, and wondering whether the hole is wide enough for that window to stay clear of stroke response.

I'm weighing whether a window-based "empty centre" check would actually separate 0s from 2s, since a 6-pixel window is big enough to matter but a 2x2 one would be empty for almost any digit. The max-pooling over shifted windows only means something if each window is large enough to say something about the hole.

I'm weighing whether a broader set of features would help with 2→3, since 2s and 3s share many strokes. I'm also considering whether the template for 2 has the right emphasis on the diagonal in the centre and lower-left.

I'm checking the 2→3 confusion against the template features. A real 2 may lack the straight diagonal and have a wider base, so the 2 template could be penalising it, while a 3 shares its top arc and right-side strokes.

I'm still weighing whether the 2→3 confusion comes from the features themselves, since the two digits share a top arc and right-side strokes. I'm leaning toward nudging the Bernoulli weight up and checking whether that shrinks the 2→3 count, rather than adding new endpoint channels yet.

I'm checking which digit classes get over-predicted, comparing predicted column totals against the true counts, with 1 and 3 looking the most inflated.

I'm comparing the predicted class totals against the true counts: 3 is over-predicted by about 630, 1 by 290, and 5 by 200, while 4, 8 and 0 are under-predicted. So I'm considering bias adjustments, lowering 3 by around 0.6 and 1 by 0.3, and raising 4 and 8 by about 0.4, which is a steady way to correct the imbalance.

I'm weighing whether to keep the Bernoulli term symmetric, since an asymmetric penalty would favour broad templates like 3 and 8 even more. I'm leaning toward keeping it symmetric and correcting the 3 and 1 over-prediction with bias terms instead.

I'm now looking at whether to tune the Bernoulli term so that features a template expects but real digits often lack get a softer penalty, with the spatial boundary cases handled automatically. The plan is to soften the neighbour-orientation cue to 0.5 and raise the Bernoulli weight from 0.08 to 0.16, which should shift the balance away from the over-predicted 3s.

I'm settling on a few changes together: adding "maybe" credit for neighbouring orientations, raising the Bernoulli weight and lowering alpha, shifting per-class biases to pull back the over-predicted 3s and 1s and lift the under-predicted 4s and 8s, and bumping the slant default. If the result gets worse I can revert pieces one at a time, and with 48 steps left a few bolder moves seem acceptable. I'm also wondering whether endpoint detectors could add the information I'm missing, which looks like the most promising direction even though it's less certain.

I'm weighing whether to apply the bias corrections at half strength, since the 3 over-prediction may shrink once the Bernoulli weight goes up, and I'm unsure how large a bias needs to be on this logit scale.

I'm weighing a soft rule where a stroke's presence is partly credited when a neighbouring orientation is present, giving it about half weight rather than a hard penalty. I'm also wondering whether the V strokes should be treated asymmetrically, giving "/" neighbours more credit than "\" ones, since a 4 and a 9 can look similar.

I'm sticking with the 1-vs-7 and 0-vs-2 reasoning, noting that the H-top feature decides the first and slanted zeros keep the second ambiguous. Then I'm defining the detection array with neighbouring orientations given partial credit and switching the default slant to 0.18.
