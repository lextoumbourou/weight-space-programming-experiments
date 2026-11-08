The small probe result is mildly worse, and I'm not sure the -|x9| term helps much. Next I want to test interactions between features. The linear probes may have missed pure pairwise effects, so features that look irrelevant on their own, like x0, x2, and x8, could still matter when combined with others.

I'm weighing whether to reweight the features first, since that's cheap and might only gain about 0.01. For the interaction probe itself, I want a term that's zero-mean and built from four hidden units, so I'm thinking about restructuring the code around a generic list of units. As for which pair to test first, I'm leaning toward x1 with x7 among the relevant features, but there are 28 possible pairs, so I'll go one at a time.

I'm weighing whether to test the pairs one at a time or two per step, since a null result on both would save steps, but opposite signs could cancel out. I'll keep it clean and probe (x1, x7) with a positive coefficient of 0.5 first.
