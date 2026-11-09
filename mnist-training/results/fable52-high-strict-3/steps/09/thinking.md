Now I'm tallying the per-class recall figures and starting on the predicted-column totals for class 0.

Now I'm working out the predicted-column totals for each class, which I'll check against the true counts. Class 3 and class 9 stand out, since 3 is over-predicted by about 400 and 9 is pulling in mistakes from 4 and 2.

Now I'm adjusting the k=1 BayR thresholds for classes 3 and 5, since 5→3 jumped from 10 to 128 once 3's threshold was relaxed. I'll set 5 to +0.6 and 3 to −0.5, which should balance the 3→5 flow that was 104 before and is now 52.

Now I'm applying a damped bias correction from the log ratio of predicted to true counts. Class 3 gets the largest cut, class 4 the biggest raise, and the rest move only slightly.

Now I'm weighing the 4→9 confusion, which is the largest single error flow at 174. The plan is to strengthen the bottom-open evidence for 4s so that the upper-hole feature stops pulling them toward 9.

Now I'm raising the penalty on 9's upper bay-open feature to −0.7, since a 9 almost never opens upward at the top, and tightening 8's upper bay penalty to −0.6 to cut the 4→8 flow. I'm also softening 6's upper bay term to −0.5 at k=0 and −0.3 at k=1, so it stops pulling 4s away, while noting that the top-hole cue (closing arc on 9, none on 4) could separate the two.

Now I'm adding a rule for class 4 that forces the top-center hole feature to a strong negative weight, since a 4 never closes at the top the way a 9 does, and I expect that to cut the 4→9 flow.

Now I'm weighing a 3-side adjustment: the hole penalty for class 3 looks like it should sit around −0.65, since at −0.8 it pushed 3→8 up, while at −0.5 the 9→3 flow grew. I'm also considering a milder version of the left-upper V/D rule for 3, to see whether it helps without the earlier side effects.

Now I'm adding a milder rule for class 3, pushing the left-upper vertical feature down to about −0.5, since the 9's left loop side would otherwise pull it in. I'm also comparing 2 and 3 in the lower half: 3 has a right-side vertical at the lower right that 2 lacks, so I'm leaning toward a lower bias for 3 there, and I'm noting that 2's bottom bar extends further right.

Now I'm looking at the lower-left diagonal for class 3, since the 2's diagonal runs through that region while a 3 has none there, so I'll push that feature down to about −0.5.

Now I'm restricting the lower-left diagonal rule for class 3 to the rows where a 2's stroke runs but a 3's bowl doesn't, since the 3's own lower-right arc can also slant that way.

Now I'm checking the 5→3 flow, which jumped to 128 once the k=1 threshold for class 3 was relaxed, so I'll bring 5's k=1 weights up and 3's down to rebalance them.

Now I'm tuning class 1's bias upward a little more, to about −0.08, since its false positives are low. For class 0, I'm raising the upper-right corner feature to +0.4 at k=0 and k=1, because 0→2 is being driven by that corner, and I'm reworking the hole weights for tilted 0s, since 0→8 is still high.

Now I'm tuning the 0-class hole weights and the 8-class hole weight at k=1 and k=2, since the 0→6 and 6→0 confusions are tied to those values. I'm also reviewing the 8 and 2 flows, which move in opposite directions and may be linked to the same feature.

Now I'm raising the hole-feature weights for 9 against 3, 5 and 7 and lowering class 3's hole penalty to −0.7, which should counter the 9→3 flow that grew when those weights were cut. I'm also bumping the overall hole multiplier from 0.35 to 0.4 and keeping the neutral values for 0, 2 and 4, so the over-firing there stays under control.

Now I'm checking the loss, which sits at 0.76 against 77% accuracy, and deciding whether to leave the temperature alone. I'll add three rules for classes 4 and 3: a top-center hole penalty for 4, and vertical and diagonal penalties in the lower-left for 3.

Now I'm checking whether the lower-left features for 3 hold up on real 3s, since their tails may curl upward at the tip and pick up a vertical component there.

Now I'm finishing the tail of the rule set and the bias values, with class 3 settling near −0.52 and class 4 raised to about +0.40. I'm also starting the structure-table update for the hole weights.

Now I'm writing out the per-class weight tables for the hole, corner, and bay features, with the corner values for 0 raised and the bay weights for 3, 5, and 9 adjusted.

Now I'm finalizing the bayU and bayR weights and setting the last bias values.
