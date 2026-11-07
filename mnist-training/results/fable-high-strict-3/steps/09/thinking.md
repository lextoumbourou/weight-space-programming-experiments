I'm comparing the results: the overall accuracy is roughly unchanged at 54.0%, with 9 and 8 improving while 2, 3, 4 and 5 dropped. Eight is again becoming a sink in the predictions, probably from the +0.37 bias together with the crop change.

I'm weighing whether the orientation maps should count for more than they do now, since they capture structure like the horizontal base on 2 that 9 lacks. Right now the ink weight outweighs them, and I'm thinking about whether shifting that balance could break the 2/9 and 4/9 confusions.

I'm weighing a few options to get past the ~54% plateau: a stronger template blur, giving the orientation maps more weight so the structural cues like the 2's base register, or using thin-ink features so empty regions like the 0's center actually show up as empty. Balancing the biases is the safe fallback, but I'd rather try something with more upside first.

I'm considering a more targeted version of the forbidden-region idea using thin ink features, so that empty areas like the 0's center stay empty. The earlier failures may have come from fat strokes spilling into those zones, so I'd lower the penalty strength and shrink the regions to reduce the risk from slanted 1s and wide 7s.

I'm weighing whether the 8 template's uniqueness can be pinned down: its center ink overlaps with 3, 2, 4, 5, 6 and 9, so the distinguishing cues are really the left-side and right-side ink, which pushes its template toward being a union of the others.

I'm looking at the 8 template as the sink problem: its shape overlaps the others, so a half-norm penalty only helps when digits are consistently sized. For 8, I want to penalize the classes it gets confused with, using the forbidden zones for 0, 3, 6 and 9, rather than just tuning its bias. I'll try that with a weaker penalty on the ink and a stricter mask, and add a check for the empty hole in 0's center.

I'm reworking the per-class bias values from the latest prediction counts, nudging each class by its over- or under-prediction. Eight and 9 come out over-predicted and get pulled down, while 5 and 0 get pushed up. I'll then pair the rebalanced biases with the forbidden-region penalty.

I'm settling on the bias formula and the forbidden regions, with a small compensation term for classes whose regions shrink their predictions. The penalty will be scaled by how much forbidden area each class has, and I'm starting to lay out the region coordinates for each digit.

I'm laying out the forbidden regions for the rest of the digits: the left-middle band for 2 and 3, the top-center and bottom-left zones for 4, the upper-right areas for 5 and 6, the lower corners for 7, and the bottom-left for 9. The 8 gets no forbidden region, and I'm keeping the penalty weight at 0.15 against the ink scale of 0.3.

I'm settling on the mask rule, where each candidate's score gets scaled down by how much ink sits in its thin-ink region, and I'm leaving the blur sigma at 0.9.
