The score is at 73.6% with loss 0.833, and the measurement approach seems to keep helping. Next I want to measure orientation features, since the templates are hand-built. Those are 64 features, so I'm considering pooling them into regions, maybe per quadrant or split by top/bottom and left/right.

I'm weighing whether to pool the orientation channels into quadrant sums, which would give 16 scalars across 8 steps. The sums run larger than the other features, so the bin thresholds would need adjusting, and coarse bins would make the class-mean estimates rough. I'm also considering spending the free struct channels on better detectors first and measuring those instead.

I'm considering measuring the template scores per class instead, so I can recalibrate each hand-drawn template's scale and offset with an LDA over those 10 scalars. That could help with the confusions like 9→7 and 4→1 more than pooling the orientation features does.

I'm considering calibrating the template scores with a learned LDA over the ten per-class template values, since that could fix confusions like 9→7 better than pooling orientation features. The hard part is the bin thresholds, because the template values have an unknown range and could be binned badly. One option is a single step that gives a finer histogram for one scalar first, to see its distribution before committing.

I'm estimating what a quadrant orientation sum would look like: a stroke crossing a quadrant should give roughly 1.5 to 2.4, and an absent one close to zero, so the thresholds need to sit well above the usual 0 to 1 range I'd assumed.

I'm weighing quadrant pooling for the orientation features against a different option: pooling the 16 scalars across 8 steps would give a usable LDA input, but the bin thresholds have to sit higher than I first assumed, so the class-mean estimates would be coarse. I'm also considering whether tuning the temperature of the combined classifier could give a small gain without any new measurements.

I'm settling on measuring the orientation quadrants: 16 scalars across 8 steps, with the top-left and top-right pairs for the horizontal channel coming first.

Now I'm settling the bin thresholds at 0.3 and 1.2 for the quadrant sums. Then I'm checking whether the top and bottom halves would be a better split than the 2x2 quadrants, but each quadrant is four cells, so the quadrants stay.
