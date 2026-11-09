The accuracy has plateaued at about 79.9%. Four classes improved, but the digit 9 dropped noticeably, with many 9s now being confused with 5, 7, 3, 0 and 2. I suspect the new rule for 9 is responsible, since it seems to fire on the right side of the loop-tail junction and pull 9s toward other digits.

I'm checking whether the 9 rule is the cause of the 9→5, 9→7 and 9→3 confusions, and whether the same rule is also pulling 6s toward 0. The 6→0 count went up even though the 0 change should have helped, which doesn't fit my current explanation.

Reverting the erules for 9, 8 and 6 looks like the obvious fix, but 4 gained 91 from that same rule (4→9 went from 145 to 69), so the net effect is zero. The ER detector seems to respond to the right side of convex arcs, not only to true stroke endings, which would explain why it hurts the loop-heavy digits.

I'm weighing a narrower version of the 9 rule that only applies at row band k=2, since the loop's right extreme sits higher at k=1. That would mean dropping the 6 rule, which has its loop extreme at k=2, and keeping the 8 rule at k=2 as well.

I'm checking whether the 6 rule is also hurting 6s, since 6→0 rose from 102 to 118 even though it only touches 6's logit when a upper-right stroke is present. I suspect the top of the 6 is pulling it toward the 0 template.

I'm dropping the ER rule for 6 as well, since the 6s' top stroke already produces some vertical-stroke response in my template, so that rule was penalizing real 6s. The 6→0 confusion is still the largest flow, and 0 is over-predicted overall (about 1104 against a true 991), so its bias needs to come down by at least 0.06 to start with.

I'm weighing whether the 0 template is too lenient toward 6s with large loops, where the lower-loop bay fires like a 0's and the corner inside the upper right looks like an opening. I suspect that's why 6s are sliding into 0, so the 0's bottom-bay bonus may need trimming.

I'm equalizing the bay weights for 6 and 0 so the big-loop 6s stop sliding into 0, and I'm bringing 0's hole weight down, since its narrow hole sits closer to row 13.5 than 6's does. I'm also lowering 0's bias by 0.05 and raising 6's by 0.04.

I'm now looking at 9s with open tops, which seem to get read as 5s, and that may be why the 9→5 count is so high. I'm also weighing a small upward bias for 9 since it's being under-predicted overall.

I'm looking at why 5 has become such a strong attractor: 9→5, 3→5, and 7→5 are all high. Its bonuses for the upper right bay and lower left bay seem to be firing on 3s and curled 9s, so I'm considering trimming the lower left bay bonus instead of just lowering 5's bias.

I'm lowering 5's bonus for the lower left bay from 0.6 to 0.3, since that bay is shared with 3s and curled 9s and should not carry the discrimination. I'm giving 9 a small lower left bay bonus of about 0.2 instead, to handle its curled tails. Next I'm turning to the 1s, which are leaking into 2, 4 and 7, with 4's bias already running high at 0.63 and 1s with long downward flags looking the most suspicious.

I'm giving the 1 template a flag variant, a stroke running down-left from the top, plus a base stroke at the bottom. Since 1's false positives are already very low, I think there's room to broaden it, though it may pull in some 7s, 2s and 4s.

I'm checking 2's false positives next: 0s, 1s, 8s and 4s are all being read as 2, and 2 is over-predicted overall, so its bias needs to come down a bit. I'm also wondering why 0s pick up 2's lower-right bay, since that bay should only fire for real 2 structure.

I'm moving on to the 8s, where the 8→2 confusions are up and 2 is over-predicted, so the 8 bias only needs a small trim. Then I'm tallying the 3 and 4 columns: 3 is absorbing 5s and 8s, and 4 is under-predicted by about 120, so it gets a bias bump of about 0.05.

Now I'm working out the per-class bias corrections from the column totals, nudging 0 down and 3 down further, and raising 1 slightly while I keep the flag variant in mind.

I'm nudging the per-class biases again: 0 and 2 come down, 1, 4, 6 and 7 go up, and 9 gets a tiny trim. I'm also planning to remove the 6 rule and relax the ER rules for 9 and 8.

Still tuning the per-class biases and bay weights for the 6, 0 and 5 templates.

I'm working through the bias and bay adjustments for the 9 and 5 templates, and I'm adding a flag and a base stroke to the 1 template. Since these extra strokes will move the template's centroid, I'll need to recheck the 1's offset afterward.

I'm wrapping up this round of tuning, with one more pass before I settle on a final configuration.
