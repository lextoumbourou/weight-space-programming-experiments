The negatives are having almost no effect on the 4→9 and 7→9 counts, which I didn't expect. That might mean the features aren't behaving the way I've modelled them, perhaps the conv1 filters respond to things I haven't accounted for. The zero-sum negative term adds a roughly uniform offset, so it's probably harmless. But 7→9 going up while there's a negative 7 in the upper-left is puzzling, and I'm trying to work out why a 7 would push toward a 9 there.

I'm checking whether a 7 could plausibly push toward a 9, since the 7's top bar and diagonal overlap with the 9's top and stem. The 7's diagonal leans about 26° from vertical, and I'm wondering whether real 7s are steeper than my template. I'm also considering whether centring shifts the centroid in a way I haven't accounted for.

I'm now checking whether the diagonal filters respond to horizontal and vertical strokes more than my tuning assumed. Summing a 45° kernel across a thick horizontal stroke gives a positive response, so the real value may be closer to 0.3–0.4 rather than zero.

I'm working out whether the diagonal filters pick up horizontal and vertical strokes, since summing the 45° kernel over a thick horizontal stroke gives a positive response. Going through the kernel values by hand, the positive entries come out to about 4.0 once the mean is subtracted, so the effect is real but modest.

Working through the kernel sums by hand, a horizontal stroke three pixels thick gives the 45° filter a response of about 0.25 of its norm, so the diagonal filters do pick up horizontal strokes, just weakly.

I'm checking the diagonal filter's response to a horizontal stroke against a diagonal one, working through the H kernel's row weights by hand to estimate how much a diagonal stroke spanning a few rows contributes.

I'm now working out the cross-talk between the diagonal and horizontal filters, which comes to roughly 0.2 to 0.3 with a small negative bias. That suggests the tuning model should include a bit of response off-orientation, so I'm considering a cos⁴ falloff instead of pure cos(2Δ).

I'm comparing the 4 and 9 templates directly: the 9 has a top bar around y≈0.03 spanning the middle of the image, while a 4 has nothing there but the tops of its arms. The 4's horizontal bar sits lower, near y≈0.58, which the 9's loop doesn't match.

I'm weighing whether a discriminative weighting could separate the 4 and 9 templates better than plain correlation, since most of their features overlap. The idea is to down-weight the features they share and emphasise the ones where they differ, like the 9's top bar and the 4's lower crossbar.

I'm weighing whether to reweight the features so the ones the templates share count for less, since that would help separate the 4 and 9 prototypes. It would amount to fitting weights to my own hand-built templates, though, which feels too close to discriminant analysis, so I'm leaning against it.

I'm still trying to explain why the negative strokes I added for the 4 didn't pull the 4→9 confusions down. One possibility is that the misclassified 4s are ones with nearly closed tops, which my template doesn't cover. I'm also checking whether centring shifts the 4 template so the top-bar negative lands in the wrong place.

Now I'm working out why the 4→9 confusions survive my negatives: the 4-only features aren't the problem, so I need negatives on the 9 template at the spots where a 4 has ink and a 9 doesn't, like the bar extending right of the stem and the top-left arm.

I'm now looking at the 4→9 errors: the 9 template could be given negative strokes where a 4 has ink but a 9 doesn't, such as a horizontal bar to the right of the stem near mid-height and a short vertical at the top-left arm. Those positions are only approximate after centring, so I'll need to check them. I'm also wondering whether adding positive emphasis to the 4's distinctive features, beyond normalisation, would work better.

I'm planning to give the 4 template an emphasis stroke on the right end of its bar, and a matching one on the top of its left arm, with the 9 template getting an emphasis on its top bar. For the 4→1 confusions I want negative strokes on the 1 template along the upper-left, where a 4's arm has ink and a 1 doesn't.

I'm adding emphasis strokes to the 9 template along its loop's left side and bottom, since those are features a 7 lacks, so a 7 input stops scoring well against the 9.

I'm now weighing emphasis on the 9 template's top bar and loop's left side, though the 4 has the loop-side features too, so it may not help separate the two.

I'm going through the confusion pairs one at a time and deciding where each negative or emphasis stroke should go. For 0→6, the upper-right negative on the 6 isn't enough, so I want to strengthen it. For 5→6, I'll add a top bar to the 6 negatives and emphasise the lower-left vertical side. For 3→5 and 2→3, I'm adjusting the 5 and 3 templates to target where the errors come from.

I'm tweaking the 2 template by strengthening its base stroke and diagonal, and adding negatives to the 3 and 7 templates at their bottom corners and lower-left to cut the 8 confusions.

I'm now planning to tune the emphasis strokes and negatives together at a shared strength, with the 9 template getting positive emphasis on its top bar and loop-left side and the 8 and 2 templates strengthened at their lower parts. I'll also switch the orientation tuning to a cos⁴ falloff, accepting that changing several things at once makes it harder to tell which change helps.
