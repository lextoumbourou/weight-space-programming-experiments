I'm at 81.7% with a loss of 0.60 and four steps left, so step 15 has to produce a strong classifier. I could spend step 12 on one more probe to measure three features aimed at the remaining confusions, then use steps 13 through 15 for classifiers, or I could just tune what I have.

I'm going through the remaining confusion pairs and their counts, mostly the 8, 9, 4, and 6 errors. Then I'm looking at the 0-versus-2 case in particular: 140 zeros get called 2s, and I suspect the centre veto on 0 is pushing them the wrong way, so I'm weighing a lower-left vertical and a centre diagonal as features that could separate them.

I'm going through the 2-versus-3 confusions next, where 169 twos get read as threes. Two features look promising: a diagonal stroke in the lower-left zone, which 2 has and 3 mostly lacks, and extra ink reaching far to the bottom right, which fits 2's base better than 3's curved ending.

I'm now weighing the 5-versus-3 confusion, where 121 fives get read as threes. The upper-right vertical is nearly absent in 5 but strong in 3, while the upper-left vertical is common in 5, and on those features alone a five with both verticals missing still leans slightly toward 5, though the lower-right, middle and top cues mostly favour 3.

I'm checking whether a top-right feature separates 5 from 3, since the upper-left vertical alone isn't enough. A diagonal in the upper-right zone looks like it could distinguish a 3's curving top arc from a 5's flatter bar, though I'm wary that 3's top stroke may also register there.

I'm now checking an upper-right feature that would fire on any stroke orientation in that zone, since a 3's right-side curve should register there while a 5 leaves it empty.

I'm now trying to find a feature that separates 8 from the other digits, since 8 has crossing diagonals through the centre. I'm checking which digits have a diagonal running from upper-left to lower-right through the middle box, and the candidates so far are 3 and 5 at their belly and lower-arc starts.

I'm weighing a centre-diagonal feature, since 8 is the only digit with a crossing stroke through the middle, and I'm also looking at a lower-left vertical as a way to separate 5 and 6.

I'm weighing a centre diagonal and a lower-left vertical as candidate features, checking which digits carry each one so I can cover the 2-versus-3 and 5-versus-6 confusions.

I'm weighing a centre-diagonal feature that would fire for 2 and 8 but not 0, which might fix the 0-versus-2 mix-up.

I'm weighing three probe features for step 12: a centre diagonal running one way, which should separate 0 from 2 and help with 8, a centre diagonal running the other way, which should pick up 8's crossing strokes, and a lower-left vertical-plus-diagonal feature for the 2-versus-3 and 5-versus-6 cases. The 3-versus-5 confusion would still need another approach, since it doesn't fit in the same three-feature budget.

I'm weighing how to split the remaining confusions across the three probes: the centre diagonal for 0 versus 2 and 8, the lower-left feature for 2 versus 3 and 5 versus 6, and the upper-right feature for 5 versus 3. I'm also considering whether one centre-diagonal feature could cover both the 0-versus-2 and 8 cases.

I'm weighing whether to spend steps 12 and 13 on probes, leaving 14 and 15 for classifiers, since the known 81.7% configuration gives a safe fallback if the new one underperforms. The new features would be added to the working classifier with measured probabilities, which keeps the risk low.

I'm now planning six probe features to measure, starting with a centre diagonal that should separate 0 from 2.

I'm now describing three probe features for the lower-left zone, a vertical and a diagonal, and sizing their cell layouts so a vertical stroke registers strongly in the right places.

I'm now sizing the lower-left probe as vertical and diagonal strokes over two rows of cells, which should flag 2s and 0s but not 3s, and a fourth probe checks the upper-right zone for any stroke orientation so 3 and 5 separate.

I'm checking whether an upper-right feature that fires on any stroke orientation would help more than a plain vertical, since a 3's upper arc is short and its strokes may be diagonal rather than vertical. I expect it to fire strongly for 3 and weakly for 5, though I'm unsure about the 5's bar. I'm also considering a top-right horizontal feature or an upper-left any-orientation feature as alternatives to separate 3 from 5.

I'm sizing a fifth probe, the upper-left zone for any stroke orientation, using the lower cell rows where a 5's vertical sits and leaving out the top band where 2s and 3s start, which could otherwise fire it.

I'm sizing the bottom-right probe, a horizontal stroke in the far lower-right cells where 2's base sits, and checking which digits carry it so it can separate 2 from the others.

I'm weighing which six probe features to measure, and I'm settling on the bottom-right horizontal for 2 first: it should separate 2 from 3 and favour 0 over 2, which together cover a sizeable share of the errors. The remaining candidates are the two centre diagonals, the lower-left vertical-plus-diagonal, and an upper-right any-orientation feature, and I'm still deciding which three of those to keep.

I'm settling the step-12 probe: centreD1, centreD2 and llVD1 come first, and step 13 gets urAny, ulAny and brH. The threshold is 1.0 for all of them except brH at 0.7, and I'm planning to set each zone's linearisation weight by how many cells it covers.

I'm settling on the vertical-plus-diagonal probe for the lower-left zone.
