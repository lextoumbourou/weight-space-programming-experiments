The loss is down to 0.8718 with accuracy at 72.8%, but the improvements are small. The best-loss checkpoint is what I'll use for testing, so it's worth continuing to push the loss lower. Looking at the confusion counts, the biggest errors are 4→9, 3→5, and 2→3, and I'm considering whether conv1's free channels 6 and 7 could be reallocated to add more structural features, since all conv2 channels are already in use.

I'm weighing whether to drop the diagonal channels down to two offsets so the freed capacity can go to a new detector. The idea I'm leaning toward is an endpoint detector, since stroke terminations differ a lot between the confused pairs: 4 has two top endpoints while 9 has only one at the bottom, and 3 and 5 terminate in different places too.

I'm working out a direction-agnostic endpoint detector on the pooled ink map: a cell that has ink at its center but only a thin ring of ink two cells out would be a stroke termination, whereas a stroke passing through has ink on both sides.

Still working out the endpoint detector: the center cell gets a strong positive weight, and a negative weight on the ring two cells out makes a stroke termination come out positive while a passing stroke does not.

I'm working out whether a stroke ending can be picked out of the pooled ink map: a cell with ink at its center but only sparse ink two cells out would mark a termination. I'm sketching a weighted sum where the center counts strongly and the outer ring is subtracted, with a threshold set so a stroke that passes through falls below it while an endpoint just clears it, though the margins look tight.

I'm sketching endpoint templates for each digit: the expected stroke-termination locations and how likely each one is, with 1, 2, 3 and 4 getting their top and bottom ends placed by hand.

Now I'm sketching endpoint templates for each digit, marking where the stroke terminations would sit and how likely each one is. The top and bottom ends of 1, 2, 3, 4, 5, 7 and 9 are being placed by hand, and 0 and 8 get no endpoints at all.

I'm checking whether the endpoint idea holds up in the classes where no endpoints apply, like 0 and 8. Since subtracting the same vector from every class leaves the argmax and loss unchanged, only the relative differences between classes matter, so a plain positive weighting should work fine.

Sizing the endpoint detector: it takes one channel on the 4x4 grid, centered at 4a+7.5, and I'd bring back one of the ink offsets to fill the other freed slot.

Setting the endpoint kernel's bias and center weights in conv1's raw ink channel, with the outer ring subtracted, and checking that the pooled values land where the endpoint template expects them.

Checking the bias for the endpoint channel next, since the detector will add positive logits to digits with more endpoints, mainly 4.

Now I'm working out how to offset the endpoint detector's bias so that digits with many endpoints, like 4, don't get an unfair boost across the whole dataset.

I'm settling the channel layout now: the three ink offsets, the sloop and loop features, the endpoint detector, four horizontal and four vertical strokes, and two diagonals, which adds up to 16 channels.
