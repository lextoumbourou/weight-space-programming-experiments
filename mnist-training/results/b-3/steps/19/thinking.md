Blur didn't help much either, and it shifted errors onto 7s. So the template blur seems close to its best setting, and I'll go back to σ=2. We're still stuck around 70%, so I need a different angle; the main confusions are thin narrow 8s read as 1s, 4s read as 9s, and 3s and 2s mixed up with 5, 7 and 3.

I'm thinking about loop detection, since 8, 9, 6, 0 and closed 4 all contain loops. A conv2 detector could check for background enclosed by ink on all four sides, though that only really fits small loops and the bigger 0s would fall outside the receptive field. Getting an approximate AND from the four sides would mean a sum with a threshold.

I'm weighing which conv2 channels to repurpose for loop detectors, since all 16 are in use. Dropping the diagonal orientation maps would free four channels, though those help with 7s, 4s and 2s. Trimming the ink maps to fewer offsets is another option, but the orientation types already carry much of the same information.

I'm sketching out the loop detector's wiring: the ink inputs would come from a couple of conv2 channels, with the ring check built as a thresholded sum over the four sides. I'm also thinking about how a max-pooled ring value could approximate an AND, and how the center cell should suppress activation when it is ink.

I'm working out the loop detector's kernel on the 5x5 pool1 grid: a strong negative weight on the center so the hole has to be empty, and positive weights on the four ring taps two cells out. That should respond to small loops like those in 8s and closed 4s, though the larger 0s may still fall outside its reach.

I'm working out the loop detector's sides as averages over a few taps each, so that a full ring gives a high sum, and I'm wondering whether the threshold leaves enough margin for blurred ink at around 0.8.

I'm working out the threshold for the loop detector: a sum of the four sides minus a penalty on the center, where a full ring clears the threshold and an open shape like a C falls short. The loop's hole radius sets the ring distance, so it catches small loops like those in 8s and closed 4s, while the larger 0s fall outside its reach.

I'm now sketching the template values for the loop feature: the loops sit at roughly (14, 9) and (14, 18.5) for 8, (14, 9.5) for 9, and (14, 18) for 6. I'm weighting each digit's loop chance (around 0.8 for 8, 9 and 6, lower for 0 and 4) and placing a Gaussian falloff around each loop location, with the unit amplitude left as a guess.

I'm working out the position mapping for the loop channel: the pooled outputs land on a 4x4 grid at roughly 7.5 to 19.5 px, and max-pooling over the two neighboring positions covers the full range.

I'm settling on one loop channel and using the spare channel for ink at a third offset, which brings the total to 16. Next I need to work out how the loop feature should enter the distance model, since its real magnitude is still uncertain.

I'm settling the loop kernel's weights and thresholds, with the on-stroke ink values in mind, and starting to work through the top side's taps.

I'm working out the loop kernel's negative weights around the hole: the center and its four neighbors at about 2px should stay near zero, since blurred stroke ink there is only around 0.2 to 0.3.

I'm checking the C-shape case: with the right side only partly on-stroke, the open shape scores about 7.1, which would slip past the threshold. Raising the threshold to -7.5 should leave a full loop at about 0.9 and the C at zero.

I'm checking the loop detector's threshold against the side sums: a crossing "+" stays well below it because its center is inked, and a solid blob is suppressed by the center penalty. The caveat is that loops bigger than about 8px fall outside the ring, so the larger 9 loop won't be picked up.

I'm placing the loop templates by digit: 8 gets a top and bottom loop, 9 a top loop, 6 a bottom loop, with smaller chances for 0, 4 and 2. I'm also setting the loop activation to about 1.2 as a rough guess and giving each loop location a Gaussian falloff of about 2.5 px.

I'm setting the loop template's Gaussian falloff and then mapping the ink channels by offset, with the loop channel at a fixed center, and I'll build the template per channel from that spec. For the biases I'll start from the step-16 correction and let the loop weights boost 8, 9 and 6, since 8 is already under-predicted, and calibrate on the next step.
