I'm at 91.3% accuracy with loss 0.294, so the gains are getting small with 16 steps left. I'm weighing three paths: fine-tuning the scales for a modest gain, adding new features like the NE-end and side-cell ones, or trying something more fundamentally stronger.

I'm now considering option C: getting discriminative signal from probes on misclassified examples, since the fc can produce both logits and a feature. I'm also ruling out a confusion-specific pairwise feature in conv2, because there are no spare channels there, and I'm looking at modeling correlations between adjacent cells through the run-length patterns I already have, though a linear model can't capture those joint terms without products of the inputs.

I'm considering a linear approximation to the per-row log pattern probabilities, fitting weights over the 10 observed patterns so the score accounts for correlation within a row rather than double counting it. Whether a least-squares fit on my own measured table counts as the forbidden kind of regression is the open question I'm still weighing.

I'm ruling out a least-squares fit over enumerated bit patterns, since it looks too close to the forbidden regression and hand-fitting ten classes would be too heavy. Shrinking the scale is already in place as the simpler correlation fix. I'm now considering composite conv2 features aimed at specific confusable pairs like 8 vs 5 and 3 vs 2, and wondering which topological cues might separate them.

I'm weighing whether diagonal end detectors in the four free channels (NE, NW, SE, SW) would pick up the 5's bar end and curled tail, since the current end detectors miss a lot of the 5's shape and that may be why 5 and 8 keep getting confused.

I'm sketching out diagonal end detectors now: NE for the 5's slanted bar end and the 6's top, NW for the 5's curled bottom-left tail and the 3's lower tail, and SW for the hook starts of 2 and 3. Each would need one more probe step, which I estimate at roughly +0.5 to 1% accuracy, and I'm starting with the NE-end design, where the tip cell connects back to a previous cell one step down-left.

I'm working out the up-right side of a diagonal end detector: the tip cell with the previous cell down-left, and the cells beyond it in the up-right direction that should stay empty for a true end.

I'm sketching the NE-end stroke term: the tip cell carries most of the weight on the diagonal, with the cell down-left of it contributing a smaller share. Beyond the tip, the up-right neighbors should stay empty for a true end, so any ink there would suppress the response.

I'm checking which digits a diagonal end detector would fire on: the top of the 6, a slanted bar on the 5, the left arm of a leaning 4, and a leaning 1 all have up-right ends, while the 7's corner, the 2's top arc, and the 0, 8 and 3 are inhibited or silent. I'm also working out how the tip cell lines up with the pooled rows so the coverage of the kernel is right.

I'm placing the tip cell one row lower for top-edge ends, so the pooled rows cover the tops of digits like the 6. I'm also checking the horizontal span to confirm the 6's top end falls within the kernel's reach, and then I'll turn to the NW-end design for the 5's curled tail.

I'm working out the coverage for the NW-end detector: the tip sits at row 2 so the pooled rows span the bottom-left region where the 5's and 3's tails curl, and the down-right neighbor carries the stroke back toward the tip.

I'm setting up the southwest-end detector now: the tip cell sits at kernel row 3 so the pooled rows reach the bottom of the digit, with the up-right neighbor carrying the stroke back from the tip.

I'm sketching the southeast-end detector as a possible fourth channel, but it looks weak: the cases where a "\" stroke ends in the lower right, like the base of a 2 or a drooping 7, are rare. So I'm reconsidering whether that channel should go to something else, such as a more tolerant version of the L-end detector.

I'm settling on three diagonal detectors, NE for the top area, NW for the bottom-left tails, and SW for the top-left hooks, and leaving out the SE channel. Running the numbers, that's about four probe steps and a classifier, which leaves roughly eleven steps for tuning.

I'm laying out the cell groups for the northwest detector, covering the bottom-left rows and the first few columns where the 5's tail tip lands, and I'm starting to map the top-left cells for the southwest one.

I'm settling on three probe channels, with NE and NW first and SW decided later, and I'm setting up the NE-end weights: the tip cell at (1,2) carries most of the stroke, with the down-left cell at (2,1) contributing a smaller share.

I'm checking whether the NE-end detector should also inhibit horizontal strokes at the tip, since a bar passing through that cell could look like a corner. I'm leaning toward skipping that extra inhibition, because the horizontal-end detector already catches a slanted bar when nothing sits to its right.

I'm fixing the southwest and southeast end detectors now: the SW tip goes at (3,1) with its neighbor up-right at (2,2), and the SE tip at (3,3) with its neighbor at (2,2), each with the cells beyond the tip kept empty.

I'm placing the NW-end probe cells over the bottom-left block, covering the rows and first columns where the 5's and 3's tails land, with everything else lumped into one aggregate outcome. For the NE-end probe I'm starting to line up the cell rows and columns against the top-edge coordinates.

I'm setting the NE-end probe's cells: the top two rows across the four columns that cover where the 6's top end falls, plus the lower-row cells, with the rest lumped into a single outcome. I'm fixing the step at 35 and keeping the diagonal weight at 0.45, so a tip with only the main stroke still registers.
