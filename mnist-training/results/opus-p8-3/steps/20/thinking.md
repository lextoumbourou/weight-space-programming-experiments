I'm at 71% on this and tracking 7→9 at 300, 3→5 at 190, and 3→2/8. The 7 and 9 both share the same loop and bottom open stroke at row 1, so I need to find what separates them, likely the top bar on 7 and a possible loop difference on 9. I'm also realizing the stroke templates are still guesses, so I'm thinking about probing orientation channels per cell to check them.

I'm weighing a probe that reads several binary feature presences at once: giving each feature its own logit term so the argmax picks out which subset of features is above threshold. With three features that gives eight distinguishable outcomes, so one probe could yield the joint presence pattern per class.

I'm weighing how to tell apart the main confusions now. 9 has a closed loop at the top that 7 lacks, though I haven't measured it yet, and 7's top bar is longer and straighter than 9's curved top. For 3 versus 5, the open stroke on top points the other way in each, and 5 has an upper-left vertical that 3 doesn't.

I'm settling on the feature choice for the probe: LOOP_s split into its top and bottom halves, plus one more stroke feature, to see which of these separate 7 from 9 and 3 from 5.

I'm going to try a three-feature probe on LOOP_s top, LOOP_s bottom, and HB_s top, with each feature's presence encoded as a subset-indexed logit so one argmax reads out all three bits at once.
