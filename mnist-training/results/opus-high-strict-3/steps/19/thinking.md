I'm checking why the stopping rule hasn't fired yet at step 18: the current value of 74.42 is no better than the earlier best of 74.51, yet the run continues. I'm testing whether the rule compares the best of the last five steps against the value five steps back, and that comparison would give only +0.15, below the 0.5 threshold, so it should have stopped but didn't.

I'm weighing whether the stopping rule compares windows of five steps or counts from the extension at step 15, since neither version would have triggered the stop yet. Either way the gain is only about 0.15, so I need roughly +0.5 over the ~74.5 best, reaching around 75.0 by step 20. The L1 part weights barely moved anything, so I'm considering a larger weight for those parts, a conv1 bias change, or extra feature channels as options for a real improvement.

I'm setting the L1 weight at 0.3, roughly matching the L2 effect at 0.06 but balanced across parts. I'm adding pairs for 3/5, 7/9, 5/6, and 5/8, and I'm checking whether the 5 should show more ink in the top-bar region than the 6 or 8 does.

I'm adding two more balanced pairs at weight 0.3: 2 against 8, with the bottom bar of the 2 set against the lower-right loop of the 8, and 8 against 1, using the loop's sides against the 1's stroke.

I'm adding the 4/9 pair next, treating the open top of the 4 against the horizontal top of the 9's loop, with the 8/1 pair already in place.

I'm settling on a weight of 0.25 for the L1 pairs, since the L2 change at 0.06 was too imbalanced and the last step's small, mixed results make the risk worth taking. If it misfires like step 17 did, I may have to stop early.
