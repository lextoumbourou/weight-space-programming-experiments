I'm mapping the readout slots, then pulling the results for each one: OPEN_R at 184, OPEN_U at 279, OPEN_D top at 352, and OPEN_L bottom still coming through.

I'm reading off the readout slots for the remaining rows: the top half and bottom half of 0 through 9, with each row's openings tied to the cavities I can see in the ink.

I'm now setting up a classifier that uses the observed readout patterns as topology templates. The activation values are only lower bounds, so I'm spreading them across the cells in each row and half, and I'm assigning likely cavity columns from the stroke positions I can see.

I'm setting the cavity weights per column for the left, right, and up/down/loop channels, scaling each template value by its column weight across the rows in a half.

I'm filling in the per-row weights for the LOOP_l template: the middle rows carry most of the signal, with the top and bottom rows lighter, and row 1 being the heaviest for digits like 9 and 7.

I'm dropping the unmeasured channels for now, since I have no probe data for LOOP_s, HB_s, VB_s, HB_l, or VB_l, and their guessed templates may be wrong. The plan is to build the classifier on LOOP_l plus the four cavity templates, and maybe probe the remaining slots afterward.

I'm going to build the classifier using only the channels I've actually probed, LOOP_l and the four cavity templates, and leave the unmeasured ones out for now. If the improvement looks real, I can probe the remaining slots afterward and see whether the stroke templates need shifting too.
