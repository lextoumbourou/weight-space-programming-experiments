Accuracy sits at 73.8%, so progress is slow. The biggest remaining confusions are 2→3 at 337, followed by 7→9, 5→3, and 3→5. I'm also tallying the column sums, which run highest for column 3 at 1638.

The model is still confusing 2 with 3 more than any other pair, even though the features I expected to separate them didn't. The 2-vs-3 signatures are probably off, and since I can't inspect the images directly, the next useful step is to measure how often each feature appears in each class.

I'm weighing whether a few targeted probes would beat more tuning. Each probe can give at most about three bits, so I'd only get three binary features per step, and I'd rather use those to measure how each feature shows up across all ten classes.

I'm weighing whether to keep tuning by hand, which might reach about 85%, or to spend steps on probes that could support a naive Bayes model with 9 to 11 binary features and reach 85 to 90%. The largest errors are 2→3 at 337 and 7→9 at 259. For 2 versus 3, both digits have ink at the bottom-left, since a 2 has its corner and base stroke there while a 3 has its curled tail tip, so that region alone won't separate them.

I'm comparing the lower halves of the two digits now. A 2 keeps its stroke heading down toward a horizontal base, while a 3's lower part curves back in toward the centre, so the bottom-right shape is what should set them apart.

I'm comparing the lower halves of the 2 and the 3: the 2's stroke runs down-left to a bottom-left corner and then a base going right, while the 3 bends right and back toward the bottom with a tail to the left. My guess is that the lower-right features should separate them, but I'm checking whether the feature locations are wrong.

I'm thinking the 2's base end may curl upward near the bottom-right, which would make that lower-right feature fire for 2s too. The bottom mass could also shift the centre of mass for 2s. Rather than keep guessing, I'd run a probe on three features for 2 versus 3 and read off their presence rates across all classes.

I'm settling on a plan to probe the largest confusions directly, rather than keep tuning blind. Six features, drawn from the 2-vs-3, 7-vs-9, 5-vs-3 and 9-vs-3 pairs, could give me the signatures I'm missing within the remaining steps.

I'm weighing whether to spend the next few steps on probes that measure a handful of existing features across all classes, or to keep tuning by hand. I plan to measure three features in one probe and three more in a second, leaving out the few I've already checked, and then see whether the per-class rates expose the wrong signatures.

I'm settling on three binary probes at a threshold of 1.0 per step, since that's the most information one step can carry, and I'm planning two probe steps for six features before classifying. For the feature K, which tracks the lower-left diagonal, I'm setting the same threshold of 1.0 as the others.

I'm going to measure three candidate features on the 2-versus-3 confusion first, since those are the biggest errors. I'll encode the probe outcomes as a three-bit index and set the unused classes to a very low score.

I'm writing the probe's weight and bias setup now: each of the eight used classes gets a weighted sum of the three feature responses, with a bias that sets the threshold, and the last two classes are pushed to a very low score so they can never win.
