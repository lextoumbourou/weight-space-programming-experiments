I'm weighing whether to push the scale up to around 1.8 or 1.9, since the loss fell a lot going from 1 to 1.3 and the model still looks under-confident. With only three steps left, I'll settle on S=1.8 at step 13 and adjust from there. I'm also starting to look at how accuracy shifted at step 4, where the count dropped from 938 to 863.

I'm going through the accuracy shifts by digit pair and the tweak list: relaxing the 4 penalty, raising the 8 and 6 biases, reducing k for the persistent 0s, and nudging 7's bias up.

I'm going back over the 3↔5 confusion, weighing stronger V-shape cues on each side, and then looking at 1→2 errors, where a bottom bar in row 3 might help separate 2s from 1s.

I'm settling the scale at S=1.8 and planning to tune the bias for the 2 class: adding a bottom bar cue, which should separate 1s from 2s and help with the 7→2, 3→2, and 0→2 confusions.
