I'm decoding the mapping where each value combines a residue with a flag, and I'm tallying the counts by residue for each class. I'm starting on class 0, which has 991 items, and going through its first values.

I'm working through classes 1 through 5, tallying each residue share and the flagged fraction for every one.

I'm finishing the residue tallies for class 5 and moving on to class 6, where the flagged share comes out to about 93.5%. For class 7 I'm counting the residue-1, residue-2 and residue-4 entries and getting roughly 92% flagged, and I've started class 8, where I'm tallying residues 1 through 4.

I'm checking the detection ratios for the top-right end, and classes 1 and 4 show clear signal, while class 6 doesn't register at all, so I'm wondering whether its top stroke sits at a different angle or position.

I'm checking where the remaining detections for class 1 are coming from, since only about 53% of its top-right responses fire. One possibility is that the stroke top sits above the coverage window for some of them, and I'm working through which pooled columns the tip positions map to.

I'm checking how the remaining responses split between the left half and the top-right tip, and comparing the endpoint detectors on classes 4 and 9, since they separate those two more cleanly than the slash feature does.

I'm weighing which endpoint features to prioritize given the limited steps: the left and right ends of 3, 5, 2 and 7, since those confusions are the largest, and then the downward ends.

I'm checking whether diagonal stroke ends get missed by the detectors, since a 45° tip only clears the threshold when the horizontal weight is also on. I'm considering raising the diagonal weight at the tip so a diagonal-only end still gets detected.

I'm thinking about whether the tip detectors can handle left-pointing cases like the waist of a 3 without firing on the bulges of an 8, since vertical inhibition at the tip should block the 8's bulges. Raising the diagonal weights at the tip to about 0.6 means a diagonal-only end would still clear the threshold.

I'm weighing whether to keep the upper-right detector weights as they are, since they were already measured, and to use more tolerant diagonal weights for the left, right and downward ends that haven't been tested yet. I'm also setting priorities for the remaining steps.

I'm planning the remaining detector steps: seven of them, covering left, right, and downward ends plus the upper-left case, which leaves about 21 steps for the classifier. I'm also wondering whether nine-way chains could handle the left, right, and downward ends in one step each, though classes with two ends of the same type, like 3's left side, would make that tricky.

I'm weighing whether to use a single nine-way chain for the left, right, and downward ends, since classes with two ends of the same type would only have their stronger side reported, which biases each measurement but not badly. That would cut the remaining work to about four detector steps: left, right, down, and the upper-left case.

I'm now considering whether the remaining cells in each direction matter much, and whether the rare ends, like the serif on a 7 or the bottom of a 4's left arm, are worth covering. I'm leaning toward one nine-way chain per direction that picks the most plausible eight cells, which would bring the classifier up to about step 26.

I'm assigning the left-end cells to columns 0 and 1 and the right-end cells to columns 2 and 3, since those ranges match where the 3, 5, 2, 7 and 4 endpoints sit, and I'm laying out the downward-end rows next.

I'm settling on a nine-way chain for the left-end cells, with eight cells mapped to outcomes 1 through 8 and one spare outcome left over.

I'm deciding how to handle the leftover column-2 case for the left ends: I'd make it a ninth outcome that fires when the strongest left-end cell sits in column 2, which would give a rough aggregate rate for those endpoints. I'm also planning to raise the diagonal weights at the tip to about 0.6 and lower the next-cell weights for L, R and D, and I'm wondering whether the next cell should include the diagonal neighbours in row 1 and row 3.

I'm cutting the inhibition weight to 2.5, since a partially covered tip cell on a diagonal stroke was getting suppressed by its neighbour and missing detection in about 40% of alignments.

I'm settling the inhibition weight and noting that a partial tip cell on a diagonal stroke can still fall below threshold in some alignments. I'm going to keep the diagonal tip weight at 0.6 and the next-cell diagonal weight at 0.125, and move on to the code changes for channels 13 through 15.
