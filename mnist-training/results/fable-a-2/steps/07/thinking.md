I'm mapping each digit's pattern to an index, where the first bit is DŪ at top-centre and the second is UD at top-centre. For digit 4, DŪ shows up in the cup only about 40% of the time across its three indices, and UD never does.

Now I'm tallying how often each detector fires per digit, and the 9s and 8s come out lowest for the both-blocked UD signal, around 6–10%. That suggests the threshold is too high or the loop interiors are too small for the centre to read as empty. Digits 7 and 2 fire more often than I expected, and 0 and 3 barely register.

I'm working out whether the edge response of a small loop interior lands in the centre cell, since with only 2–4 empty rows the wall boundaries sit just a pixel or two from the centre and the ridge could fall on either side.

I'm checking whether the centre cell should count toward the blocked sums, since for these small loop interiors the wall edges sit only a pixel or two from centre and the current rows 0–1 reach misses about half the ridge. Including the centre cell at full weight for every feature would bring the both-blocked sum for 8s and 9s up to where it should fire, and the strokes' own centre line would stay out of that cell.

I'm now considering whether the centre cell should count toward the left-and-right blocked sum too. A thin stroke sitting in the centre cell could put both of its edge responses there, since a 3-pixel stroke's boundaries land about 1.5 pixels to either side of its middle, which is inside the same 2-pixel pooled cell.

I'm checking whether a gap's edge responses land in the centre cell too: a stroke centred there gets one edge counted and its other edge falls outside the range, so the line inhibition should keep it below threshold. For an empty gap between two strokes, the left stroke's right edge and the right stroke's left edge both sit within the counted columns, so the centre would register as blocked.

I'm checking the gap case next: with a two-pixel empty gap, both the left stroke's right edge and the right stroke's left edge fall within the centre cell, so the both-blocked sum reaches about 2 there and the neighbouring cells add more on top.

I'm settling on a detection threshold of about 1.9, since a single wall's edge ridge can only land in two cells and would otherwise leak past 1.8. I'm also noting that the DŪ strong bin shows up in roughly 12% of 4s and the weak bin in about 29%, though I haven't measured the edge amplitudes for the E responses yet.

I'm checking whether the 4s' cup is narrower than I assumed, since a 3–4 px inner width with slanted strokes could put ink in the upward ray and block the DŪ detection. Adding the centre cell to the excitation sums might also catch more of the cup's floor that sits only 2–5 px below centre.

I'm now thinking the ray veto may be too strict: with the 4's cup only about 4 px wide, the side walls' edge responses would spill into the centre column and trigger the up-ray block on the cup's own walls.

I'm working out which channels should count as a veto for each ray: for the upward ray, only horizontal-ish and vertical-gradient edges signal a crossing stroke, while the left and right edge channels mostly bleed in from the cup walls.

I'm now checking the centre cell's veto: it should ignore the edges in the blocked direction, since those now count as excitation there. But for the DŪ ray, the centre cell would still veto on ink above, plus the side edges, which in a narrow cup bleed into the centre and could wrongly block detection.

I'm settling on a centre veto that only checks the line channels, since in a tiny loop the centre cell picks up wall edges from every side and vetoing on those would block real loops. For the both-blocked case I'd leave the edge channels out of the centre veto, and keep the line inhibition for strokes that actually run through the middle.

I'm setting the right-edge feature for the left-open case: it keys on the right-wall edge in row 2 across the centre columns, and I'm vetoing on vertical lines, both edge channels, and the diagonals on the two left cells, but not the centre edge, which now counts as excitation.

I'm now defining the remaining features: the left-open and right-open cases key on the wall edge on their side, the up and down rays use the top and bottom edges, and the both-sided case uses both walls. For each, I'm choosing which channels count as excitation and which count as a veto in the cells along the ray and at the centre, keeping the line channels as the main veto in the centre.

I'm settling the detector thresholds at θ=1.9 for the both-sided case, and the one-sided ones at 0.4. Before going further I want to check whether the changes actually help, so I'll re-run the same probe on DŪ and UD at the top centre, comparing the 4s and 9s against the earlier numbers.

I'm keeping the same probe as before so I can compare the 4s and 9s directly, and the bins stay where they were for a fair comparison.
