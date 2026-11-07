The accuracy dropped slightly to 43.4% from 45%. The template changes and threshold adjustments seem to have caused category 3 to collapse, while category 5 has become a magnet for predictions, and I'm trying to work out whether the lowered and raised thresholds are to blame.

I'm weighing whether to go back to the step 12 setup, since it has the best loss and a confusion pattern I already know. Step 10 scored a touch higher on accuracy, so I'm comparing the two bias sets to see which differences matter most.

I'm settling on step 12 as the base for step 14, since it has the best loss and nearly the best accuracy. Step 3 and 4 are still absorbing a lot of predictions, though they also hold high correct counts. I'll try lowering the bias on category 4 to 0.0, and leave the rest alone.

I'm considering a small tweak to step 12: lowering the bias on category 4 a little, since it pulls in predictions from 6, 7 and 9, and raising category 9 slightly so it recovers some of those. I'll keep the all-ones template for 8, since the hollow version didn't help, and leave the rest unchanged.

I'm going with step 12 as the base again, but this time only lowering the bias on category 4 to 0.0 and raising category 9 to +0.15, since 4 is pulling in predictions from 6, 7 and 9. I'll go back to the all-ones template for 8 and keep category 5 at -0.05 so it doesn't become a magnet like before.

I'm settling on step 12 as the base for step 14, with a few small changes: lowering category 4's bias to 0.0, raising category 9 to +0.15, and reverting the 8 template to all-ones while keeping category 5 at -0.05. For step 15, I'll go with whichever configuration does best, falling back to step 10 or step 12 if step 14 regresses.
