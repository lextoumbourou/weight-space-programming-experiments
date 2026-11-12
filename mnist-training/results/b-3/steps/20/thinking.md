The model is at 71.8% and the loop change helped, but recall on class 8 is still weak at 440 and it mostly gets confused with 2, 7, and 1. I'm going to raise the bias for class 8 and check the 9→7 and 2→3, 3→5 confusions as well.

Still tallying the column sums and working out the per-class bias corrections from the log ratios.

I'm weighing whether a second loop detector could capture bigger loops, though the 5x5 limit on pool1 makes that hard. I also note the bottom-left stroke could separate 2 from 3, which may be enough. Next I want to raise the loop weight to 1.5 and test it, keeping the bias changes separate since those are safer to make.
