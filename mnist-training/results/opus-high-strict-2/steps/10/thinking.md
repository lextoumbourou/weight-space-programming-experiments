The first detector came back worse, with 0 and 8 being over-predicted. The loop-based features seem too permissive, firing on digits like 2, 3, 5 and 7, so I'm wondering whether the checkerboard reduction is part of the problem too. With six steps left, I need to decide what to change next.

I'm weighing whether to roll back to step 7, the best so far at 67.88%, and tune small things, or keep the loop features with lower weights and fix the 0 detector. Looking at per-digit changes against step 7, the loop info looks mixed. I suspect the LR detector fires on any C-shaped ink with a gap in the middle, so its threshold is too loose and a stricter ring detector may work better, but I can't fit four offsets into the 16 channels that way.

I'm weighing whether the spare channels can hold the ring detector, or whether dropping an offset to make room is worth it. Going back to the step-7 setup and keeping the anti features only for 4, 5 and 6 looks like the safest move with the steps I have left.

I'm weighing a combined setup: three offsets per orientation, dropping the odd-even one, plus a stricter ring detector with a higher bias and a smaller weight, while dropping the LR channel. That should test the ring while keeping most of the grid resolution.

I'm checking whether the ring detector might be the thing firing on 2s, 3s, and 5s, since those errors pushed 8 upward. The left-column cells near the top of a 3 could be partly lit, which would give the ring some false positives.

Going with the ring detector stays on the table, but I'm setting the bias to 4.5 so it needs nearly every cell lit, and I'll pool the step-7 counts with the step-8 ones, using preds 3-7 for the bias.
