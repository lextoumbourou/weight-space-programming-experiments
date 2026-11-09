I'm seeing that 9 is being over-predicted by a wide margin: 7→9 at 457, 8→9 at 170, 6→9 at 107, and 4→9 at 85. My guess is the ch8 cue at (1,1) is too strong for 9, since the ink energy total runs higher than I assumed, and the bias and shear may be adding to it. I also want to check whether 7s actually have ink at (1,1), since that would change the picture.

I'm weighing whether to drop the (1,1) ink cues for 7 and 9 and bring 9's bias down to 0.1, since that pair is where the over-prediction seems to come from. The 7-vs-9 confusion looks structural: a closed top-left loop in 9 that a 7 lacks. I'm also checking whether shear helped, and I'm nudging the cues at (2,1) and (2,1) for 1, 2 and 3 to see how the confusions shift.

I'm weighing a few small fixes to the bias and cue settings, and I'm also considering a bias bump for 7 to lift its low recall. I'm not sure yet whether to add a hole penalty for class 0 in the lower-left region, since that would separate it from 7.

I'm lowering 0's bias from 2.3 to 1.9 and adding a small reward at (2,0) and (2,1) for the lower-left side that 0 has and 7 lacks. That should give 0s the same total while pulling 7s down a bit, though 6s share that region too.
