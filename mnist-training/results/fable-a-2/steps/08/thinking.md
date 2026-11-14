I'm decoding the index as 3 times b1 plus b2, where each bit is the top-centre signal for DŪ or UD. Digit 4 mostly lands on index 0, with DŪ firing in about 70% of the 4s and UD only around 0.6%. Now I'm moving on to digit 9.

Now I'm tallying digit 9: about 42% land on index 0, and the UD signal fires on roughly 29% of the rest. DŪ also fires on about 44% of the 9s at top-centre, which is surprisingly high, and I'm wondering whether open loops or a point above the loop top are responsible.

Digit 3 shows the upper bowl's ceiling and floor both firing, so UD picks it up in about 45% of cases. Digit 2 splits almost evenly between UD and DŪ, around 43% and 42%. For digit 5 I'm unsure whether DŪ's 38% comes from the region above the top bar or from the upper cavity, since that veto should have blocked it.

I'm checking the per-digit rates for which digits the top-centre signals favour. DŪ leads on 4s and 7s, while UD shows up most on 3s and 2s. The fact that UD almost never fires on 4s is a useful clue for telling them apart.

I'm comparing the 4 and 9 signals, and they separate poorly: DŪ fires on 70% of 4s versus 44% of 9s, and UD on 0.6% versus 29%. That suggests the 9's loop isn't being picked up as closed at the top, perhaps because the loops are tiny or filled in. So I'm looking for a more reliable cue, such as ink spanning the top with the centre empty between the two prongs, which is typical of a 4.

I'm reasoning that the 9's top-centre DŪ hits may come from ink sitting above its loop, but if that were so the row positions would put those points out of range, so the source is still unclear. I'll need finer diagnostics for that, though each one costs another step, so for now I'll combine several modest features instead of relying on any single one.

I'm weighing whether a structural approach can separate 4 from 9, since the top-centre signals give only weak separation there. Combining them naively still leaves the odds close to even, so I'm considering probing the horizontal-line energy at the top-centre cells to see whether a 9's loop top shows up where a 4's doesn't.

I'm weighing whether to probe class-conditional distributions of the top-region horizontal-line energy for every digit at once, then set per-class weights from their means and variances, treating each feature on its own in a naive-Bayes style.

I'm weighing whether measured per-class statistics for a set of pooled features could give a naive Bayes classifier good accuracy, perhaps 80 to 85 percent. That would beat the cosine-template approach, but I'm wondering whether writing the per-class numbers straight into the code would count as hand-tuning weights rather than learning them.

I'm thinking about using binarised probe results, with each bin giving a per-class probability, to build a naive Bayes model that I can then turn into linear weights on the raw features.

I'm turning each binary feature's on/off probabilities into log-odds weights for a Bernoulli naive Bayes model, with the per-class bias coming from the off-case terms. The catch is that features with unbounded values could push the logits too far, so I'd need them roughly bounded for this to hold up.

I'm considering saturating features: two ReLU channels with offset biases, differenced after max-pooling, would clip each feature to a 0–1 range, though it would cost two conv channels per feature.

I'm considering how to turn per-region feature sums into linear weights, fitting each class's log-likelihood over three bins of activation strength. Then I'm thinking about how many channel-and-region combinations I'd need to probe to make that feasible.

I'm sizing up the remaining budget: with 4 line types and 6 loci features over four quadrants, that's about 40 region-level scalars, which is feasible to probe in roughly 14 to 20 steps. I think a naive Bayes over those measured statistics could beat the current 64%, though I'm leaving the combined-with-templates option open.

I'm weighing a second route: instead of probing every region, pick a few scalars aimed at specific confusion pairs. The top-centre signals already separate some digits well, for example UD firing on 3s, 2s and 5s but almost never on 4s, and DŪ firing on 7s and 4s but rarely on 3s, 1s or 8s. That suggests a small set of designed scalars could cover the worst pairs.

I'm settling on how to split the grid into regions: top and bottom rows, with the left and right columns, though the centre structures of a 4 or a 9 fall across the middle columns, so I need to think about how to handle those.

I'm settling on a partition for the regions: columns split into left, a centre pair, and right, and rows into top and bottom. That gives six regions, which times ten feature types would be too many scalars. So I'll concentrate on centre-band features, top-centre and bottom-centre, for about a dozen scalars, and add the horizontal, vertical and diagonal line types afterward.

I'm weighing how to bin the features: presence at a 0.15 threshold for the loci signals, which already separate the digits, and a finer ternary or ten-bin split for the continuous line energies, which have no clear cutoff yet.

I'm settling on which regions to check for each of the six loci features: top-centre and bottom-centre for most of them, with the top-centre DŪ and UD features already measured.

I'm now picking the regions for the remaining loci scalars: the centre band for most of them, and I'm weighing whether to add the whole left or right column, or split the centre columns by row. Wider top-and-bottom halves would pick up firing outside the digit, which dilutes the signal, so I'm leaning towards the centre columns.

I'm checking whether the centre-column loci probes are worth keeping, and they look sound, so I'll run three binary scalars next: the right-wall-open feature in the centre band, then the others.

I'm going to probe the top-centre region next, with three binary scalars for the right-wall-open, left-wall-open and horizontal features. I'll pack them into one index and plan the bottom-centre and vertical probes after that.

I'm setting the top-centre region to rows 0–1 and columns 1–2, and picking channels 8, 9 and 12 for the three binary probes.
