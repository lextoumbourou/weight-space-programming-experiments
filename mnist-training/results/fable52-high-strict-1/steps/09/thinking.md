I'm decoding the value as the sum of three bits: HOLE with weight 1, OL with weight 2, and OR with weight 4. For digit 0, I'm tallying the per-value rates across k0 through k7, and then summing the odd-k values for HOLE and the k values 2, 3, 6, and 7 for OL.

I'm checking the OL and OR rates in digit 0, which come out around 90%, far above the expected zero. Inside the 0 near its right side, the chord half-height works out to about 5.6, which sits right at the edge of the strict tolerance, so I'm checking whether that borderline geometry explains the firing.

I'm testing whether a point just inside the 0's right side can satisfy the strict vertical tolerance for the up and down samples while the center cell still counts as background. At around x=4 the chord half-height lands just above the strict limit, so the borderline geometry may not fully explain the firing.

I'm working out that near the left and right ends of a closed loop, the upper and lower arcs pinch together, which would make the OL and OR firing in 0s come from those inner ends.

I'm now going through digit 2's counts, where k2 is the largest term at 87 and k0 and k3 are smaller, to see how its OL and OR rates compare with the digit 0 and 1 results.

I'm now checking digit 2 and digit 3's rates: digit 2 shows about 45% HOLE and 97% OL, while digit 3 reads roughly 51% HOLE and 94% OR, which is surprisingly high for HOLE in a 3. I'm trying to see whether the open left-side cavity of a 3 could be what the center-background check is picking up.

I'm checking whether the 3's OR firing comes from a "(" arc near its top-left hook or the waist notch, since the sums tolerate partial overlaps.

I'm checking the digit 4 counts next, where HOLE, OL, and OR all land between roughly 47% and 69%. I can't yet see a clean geometric cause for OL in a 4, since the area under the bar and beside the stem doesn't have ink above it, so I'm wondering whether the cup between the arms could be closed at the top in some 4s.

I'm now seeing that the 47% HOLE rate for 4s may be inflated by the low threshold, since grazing activations of about 0.2 across several cells add up to a value above 0.4. That suggests I should raise the threshold to something like 1.0 to get a cleaner count. Next I'm moving on to the digit 5 counts.

I'm tallying digit 6's rates next: HOLE comes out around 80%, OL about 76%, and OR about 96%. Digit 7 is starting in the same way, with its k2 term at 523 and k3 at 131.

I'm noting that 7 also shows OL at about 94%, which I can explain: the horizontal bar and the diagonal stem form a wedge open to the left, so the stem passes below the center point. Digit 8 comes next, where k7 dominates at around 89%.

I'm working through digit 8's counts, where HOLE comes out around 88%, OL about 98%, and OR about 97%. Then I'm moving to digit 9, where HOLE is roughly 78%, OL about 92%, and I'm tallying the rest of its row.

I'm tallying the threshold-0.4 rates for each digit: HOLE is highest for 8, 6, and 9, OL and OR run high for most digits, and 1 stays low across the board. I'm now looking at whether OL or OR "any" fires broadly enough to be a useful signal.

I'm noticing that OL and OR alone don't separate the digits well at this threshold, with only 1 and 7 standing out. HOLE is more useful, with 6, 8, and 9 well above the rest. I'm now looking for a more reliable signal, and the strongest one so far is the row-sum check: the set {1, 4, 7, 9} stands out at about 95%, while the others sit below roughly 11%.

I'm checking which of the probe results are reliable enough to build rules on, since OL and OR alone barely separate the digits at this threshold. The row-sum signal and the "OL without OR" pattern for 7s look like the strongest facts, and I'm planning to use them in linear rules over the summed features.

I'm weighing whether a linear rule can use these threshold-0.4 sums directly, since the saturation risk makes it unclear. Within the BOT group {1, 4, 7, 9}, the OL and OR rates separate 1 cleanly from the others, while 7 and 4 sit closer together on OR.

Now I'm weighing whether location-specific features, like HOLE in the bottom half versus the top half, could separate the non-BOT digits better than the cavity sums alone, since those sums barely distinguish 0, 2, 3, 5, 6, and 8.

I'm now thinking about a feature that mirrors the BOT detector: whether the top of the digit is narrow, which might separate 1, 4, and 6 from the wider-topped digits.

I'm thinking about whether the extreme-position stroke idea that worked for the bottom could be mirrored for the left, right, and top edges, though digit extents shift with width and height, so fixed-position detectors may be less stable there.

I'm now testing whether the top edge can work like the bottom detector: a narrow stroke in the upper rows would suggest 1 or 4, while a wide, rounded top would point toward 7 or 9.

I'm checking whether a narrow top stroke in the upper rows could mark 1, 4, and 6, the way the bottom detector picked out 1, 4, 7, and 9. Combined with the bottom check, that would put 1 and 4 in the both-ends group, 6 with only the top, and 7 and 9 with only the bottom.

I'm sorting the remaining digits {0, 2, 3, 5, 8} next, since the cavity sums only weakly separate them. For 8 the hole rate is clearly higher than for the others, and for 2, 3, and 5 I'd need a bottom-right or top-right tip detector to tell them apart.

I'm sketching a rightward counterpart to the bottom detector: a kernel that fires on an isolated horizontal stroke ending on the right, which might help tell 2, 3, and 5 apart.

I'm sketching a rightward version of the bottom detector: a horizontal stroke that ends on the right and has nothing above or below it. The catch is that the right extent of a digit isn't pinned to the image edge the way the bottom is, so a simple kernel would also fire on strokes that continue past it. I'll need to check whether strokes like 2's bottom bar and 5's top bar actually reach far enough right to be told apart.

I'm settling on a nine-step plan: a classifier that combines the strong bottom-row rule with a new narrow-top channel, keeps the earlier features, and adds per-class biases for 3 and 0.

I'm weighing whether the top-edge narrow-stroke detector should replace the existing top-tip channel, since it's simpler and mirrors the bottom rule. The concern is whether a stroke ending near row 4 or 5 falls inside the upper kernel window, which is borderline for some digits.

I'm checking the top-edge narrow-stroke idea against the digits it should catch: 1, 4, and 6 should register a narrow top, while 7 and 9 should not. For the two-armed 4, the top detection depends on where its ink starts, so it may be weaker than for the others.

I'm repurposing channel 15 as a narrow-top detector and keeping channel 14 as it is, so the top-edge rule can work like the bottom one. The bottom rule will be rebuilt as a weighted row sum, boosting 1, 4, 7, and 9 and suppressing the rest, with 2 penalized less.

I'm settling on a moderate-weight top-row rule to pick out 1, 4, and 6 as narrow-topped digits, and I'm leaving 5 slightly penalized since its short top bar might trigger it. For 1, I'm considering a strong penalty on the OL, OR, HOLE, SLOT, and CUP sums, though that would hurt the roughly 20% of 1s whose sums run above 0.4.

I'm settling the rule weights now: the 1-class forbid on OL and OR goes up, and for 7 I'm dropping the OL penalty and adding a small positive OL requirement in the upper region. The OL and OR sums still fire almost everywhere in the 0s, the loop ends, and the 4s and 9s, which is the part that's disappointing.

I'm checking the forbid weights against the actual firing rates: 0 fires OL and OR about 90% of the time, 4 about 69%, 9 OR about 84%, and 6 OL about 76%. Those forbids are penalizing the digits they should favor, so I need to loosen them for 0, 4, and 9.

I'm going to drop the forbid weights on OL and OR for every digit except 1 and keep the strong 1-specific penalty. Since those features fire almost everywhere, the required-point thresholds don't separate digits, so I'm weighing whether their location alone can help with 2, 3, 5, and 8.

I'm weighing whether the HOLE rule should be a hard requirement: 6, 8, and 9 would need a hole in the bottom, middle, or top region respectively, with 0, 2, 3, 4, 5, and 7 penalized. I'm not sure a 0.4 threshold separates them well enough, so I'm also considering a higher cutoff.

I'm working out the HOLE weight: if the hole feature is present it should push toward 6, 8, and 9, and if absent it should push against them. Treating it as a linear function of the hole sum with a threshold near 0.63 gives roughly a weight of 1.9.

I'm reworking the HOLE rule so the forbid weights drop to about half for the non-1 classes, keeping a strong penalty only for 1. The other gains I'm expecting come from the bottom-row rule, a top-row channel, and fixing the OL and OR forbids that were hurting 0, 4, 9, 6, and 3.

I'm lowering the bias for class 0 and class 3, and raising it for the under-predicted digits 2, 4, 5, 6, and 7, to offset the over-predicted 8.

I'm restructuring the fc assembly so the rules come together: the bottom-row rule and new top-row rule are sum-based, and the old 1-class and 7-class forbids get loosened, with 1 keeping the strong penalty.

Next I'm overriding the bottom-row channel with a sum-based rule: the listed classes get a positive weight per cell and the rest get a penalty, with the bias set to match.

I'm setting the top-row detector's weights: it should fire positively for 1, 4, and 6 and count against the other digits, with 5 penalized a little more since its short top bar could trigger it.

I'm sizing the top-row kernel: the outer negatives at the sides and the smaller ones next to the center. The concern is that an 8's top loop, roughly 8 pixels wide, could put ink on the side cells at the apex row and trigger the narrow-top rule for a digit that shouldn't have it.

I'm checking the top-edge kernel against an 8's apex: the side cells at ±2 and ±4 px pick up only partial ink, and the loop walls two rows down add enough positive weight that the net comes out slightly negative, so 8 stays clear of the narrow-top rule. The same reasoning should hold for 9, whose top loop is a bit wider, and for the wider arcs of 2 and 3.

I'm removing the left-tip channel's points from the prototypes, then updating the HOLE forbid table with lower values for classes whose hole rate is near half.

Still setting the per-class forbid weights for SLOT, CUP, OL, and OR, and I'm keeping the 1 and 7 penalties strong...

I'm setting the bottom-edge and top-edge rules as sum-based detectors and tuning their penalty weights, plus adding a few location-specific OL and OR points for 0, 3, 6, 7, and 9 to sharpen their templates.

I'm working out the bottom-row rule as a set of per-class weights rather than a template, and setting the sum-based constants for it.

Next I'm writing the bottom-row rule as a sum-based weight per class, positive for the classes that show the bottom feature and penalized for the rest. Then I'm setting up the top-row detector to fire for 1, 4, and 6 and count against the others.
