I'm tallying the column sums across the matrix rows, working out each column's total, and I'm at 54% of the way through.

I'm continuing the column-sum tallies and finding the 1→7 and 4↔9 confusions, which suggests the templates need adjusting. I'm considering a penalty term for ink in regions a class shouldn't occupy, since the plain matched filter ignores that.

I'm weighing whether a linear classifier can do better here: shifting a penalty over the class templates only rescales or re-biases them, so the gains would have to come from better template shapes or from nonlinear features like "empty-region" detectors that reward blank centers for 0s and loops.

I'm working on an emptiness feature for the center window, where a class should have no ink, and I'm defining how strongly each class's template should reward blank space at each cell. The catch is that the 5-pixel windows around the center cover most of the image, so nearly every cell has some ink for every digit.

I'm adding an emptiness feature with a threshold on the ink in each window, so a class like 0 can reward blank cells at the center. The emptiness template would weight cells where the class expects no ink, and that gives a nonlinear, two-sided match on top of the ink channel.

I'm adding an emptiness channel where the weights reward blank cells that a class should have, with the strength scaled against the ink template. The effect looks mild since the center windows of a 0 still catch some ink, so I'm not sure how much it will help.

I'm going to try an emptiness feature anyway and keep the bias energy computed on the first five channels, since the new channel complicates the bias formula. If it turns out worse, I'll revert.

I'm adding an emptiness term to the logits: wherever a class expects blank space, a cell with little ink earns a small reward, which penalizes ink where a class shouldn't have any. I'm keeping the bias energy on the first five channels and setting the weight to about 0.5, since the emptiness contributions stay small.

I'm settling on the emptiness mapping: where a class's ink template is low, the expected-empty weight goes up, clipped to [0, 1]. The emptiness weight gets scaled to 1.0 directly, with the threshold near 0.4, and I'm nudging the biases for classes 6, 7, and 8 upward a little.

I'm applying small bias corrections to a few classes (up for 2 and 6, down for 0, 3, and 7) and keeping the rest of the logits as they are, since the emptiness rewards will shift the counts anyway.
