I'm at 71% with loss 0.913, and progress has stalled. The 6→4 confusions are still high because the slanted 4 pulls 6s toward it, and several other pairs like 2→8 and 3→5 are also frequent. I'm starting to think a bigger change is needed, and I'm considering whether richer orientation features could help, since I only have 8 conv1 channels arranged as 4 clipped pairs.

I'm weighing whether to drop upper-clipping at conv1 and keep only the 8 orientation channels, since the part-detector AND logic seems to contribute little. Finer orientation bins might separate stem-count confusions like 7 versus 1 versus 9, but I'm not sure it would help enough.

I'm weighing whether to keep 16 single-channel features in a roughly bounded range, arranged as 8 orientations at two spatial phases or 4 orientations at four sub-positions. The shifted sub-positions could give finer location information, though the gain may be modest.

I'm now comparing the 3 vs 5 confusion, where the distinguishing cue is a left-side vertical stroke in the top row for 5 versus a right-side curve for 3, and I'm wondering whether 3s sometimes start with a left hook that blurs that difference. For 2 vs 8, the key difference seems to be whether the center is crossed by both diagonals, as it is in an 8.

I'm also thinking about a more systematic route, like tuning each digit's template parameters through coordinate ascent, but that would be slow. Another option is to estimate per-class probabilities from the confusion matrix, perhaps with an EM-style approach, rather than relying on guesses about which features are present.

I'm thinking about whether a multi-output probe could give per-class signal faster than one scalar per step, since the argmax only reveals a single winner at a time. Using the loss alone is too coarse, so for now I'm leaning toward reasoning-based changes and tuning the global hyperparameters.

I'm checking the conv1 threshold setup, where strokes near 0.7 intensity should register clearly, while thin or faint strokes may only partly activate. I also think the diagonal orientation channels respond to curves almost everywhere, which would make them less informative. Next I want to compare the 6 and the slanted 4, since the 6's top-right stem curving down into a bottom loop may overlap with the 4's left stroke.

I'm reconsidering the 4 shear: it made the 4 look more like a 6 on the left stroke and crossbar, and the net effect looks negative, so I'm thinking about undoing it. The 6 has a bottom horizontal at about y=22.5 that the 4 doesn't share, which may be the cue to separate them.

I'm going to undo the 4's shear, since it made the 4 look more like a 6 on the left stroke and crossbar. Then I'll check whether the bottom-left vertical of the 6 could separate the two. I'll also look at the bias terms using the class counts from the last step.

I'm now tallying the per-class column sums from the confusion matrix to estimate bias corrections, starting with the counts for classes 4 through 9 and comparing each total against its expected size.

I'm applying a 0.7 damping factor to the bias corrections, since undoing the 4's shear will shift the 4 and 6 counts anyway.
