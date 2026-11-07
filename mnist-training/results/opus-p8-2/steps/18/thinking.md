The temperature bump to 1.25× gave a real drop in loss, down to 0.874, so I'm going to try 1.6 next and maybe pair it with another change. Since 0.05 came from that single step, the optimum could sit somewhere around 1.6 to 2. I still need accuracy gains, and I'm weighing whether to add orientation diversity to conv1, which has channel 7 free, possibly with a curvature feature. The main confusions are 8→9 at 154, 9→8 at 98, and 2→3 at 104, so those are what I should target.

I'm considering a crossing detector for the center of 8, since its ring would show ink in several places. The idea is to tell an X junction apart from a plain stroke or a T junction by ring intensity, though it could be noisy with thick strokes. Finding room for it in conv2 is the hard part, since no channels are free there.

I'm running the crossing-detector numbers for the thick-stroke case, and it's looking like the threshold would fire on thick middle strokes the same way it fires on T junctions, so it doesn't separate them cleanly. I'm leaning toward dropping this idea and instead tuning the template blur and stroke widths, which I already know helps with the matching.

I'm going to try temperature 1.6 and update the biases using the column sums from step 17, which come to about 945, 1158, 1094, 979, and 1036.

I'm checking the column sums for the remaining digit classes and noting that the bias adjustments are small, around 0.8 scaling. I'm also considering whether to raise the ink group weight from 1.5 to 2.0, though that would confound the temperature test.

I'm still weighing whether a temperature change alone would be cleaner to test, since any accuracy shift from the ink weight or bias tweak would otherwise be tangled up with it.
