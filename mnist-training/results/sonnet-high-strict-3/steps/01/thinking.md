I'm settling on a hand-designed approach: eight oriented edge and stroke filters in the first layer, a combining layer for parts at positions, and a final layer that matches classes against templates.

I'm sketching the filter bank by hand: oriented bar detectors (vertical, horizontal, and both diagonals, possibly with a few more blob-style ones) feeding a second layer of combinations. I'm now working out how the final layer could use a 4x4 grid of spatially pooled features, and how much of the input each cell actually covers.

I'm working out how each of the 4x4 pooled cells covers the input: each one spans roughly 16 pixels, starting every 4 pixels, so the windows overlap heavily. That makes the grid coarse but workable. I'm also considering giving each of the 16 second-layer channels a weighted sum over the eight first-layer types, so each channel acts as a pooled measure of stroke orientation within a window.

I'm weighing a simpler route: rather than guessing the fully connected weights, I could make the second-layer channels spatially selective, so a kernel favors orientations in the upper or lower part of its window. That would give the final layer finer position information, and I could set up a template-like readout on top of it.

I'm thinking about the weights for the class templates. Plain strong-feature readouts would get me maybe 60%, and learned weights would do better, but I'm going to hand-build them anyway and see how the feedback looks.

I'm weighing how to set the fully connected weights: the class scores could follow a discriminative form, with each template minus the average across classes, but building those averages from generated example inputs is off the table, so I'd rather assign the weights straight from stroke descriptions with positive and negative regions. For the first layer, I'm leaning toward four oriented bar detectors (vertical, horizontal, and two diagonals), each with a positive center and negative flanks.

I'm settling the conv1 filters and the conv2 channel layout: channels 0-3 pool each orientation's presence over a small blob, and channels 4-7 are meant to carry ink density and a loop/hole cue from conv1 channels 4 and 5.

I'm setting up the first-layer filters now: a ring detector that responds to empty centers surrounded by ink, plus horizontal edge detectors that respond to ink on one side and blank space on the other. Then I'll start writing the conv1 code, beginning with a vertical bar filter whose across-profile is weighted to sum to zero.

Still writing the first-layer filter code...

Still working through the first-layer filters: I'm building a generic bar detector parameterized by orientation, then adding a blob detector for ink density and top and bottom edge detectors. For the last channel I'm considering a ring-shaped filter to pick up loops, though the left and right edges will have to go without.

I'm laying out the 16 second-layer channels now: the first eight pool the four bar orientations plus blob, hole, and edge cues over the full window, and the rest use top, bottom, left, right, or center kernels to keep some position information. Still deciding how the fully connected weights should map each class onto these regions.

Still working out the per-class weights for the final layer: I'm sketching simple region-based rules, starting with the zero class, where the center hole and edge blobs carry most of the weight.

Still setting up the fully connected weights as an array indexed by class, channel, and cell, using a helper to fill in each region's value.

Still writing the per-class weights: for class 0 I'm putting a strong positive weight on the center-hole channel in the middle cells, a negative weight on the center blob, and a modest positive weight on the vertical bar channel at the left and right columns.

Still writing the per-class weights: for class 1 I'm giving the vertical bar at the middle columns a positive weight and penalizing horizontal bars, the corner blobs, and the hole channel.

Still writing the per-class weights: for classes 5 through 7 I'm giving the top horizontal edge and left vertical bar positive weights in the upper rows, and penalizing the hole channel.

Still writing the per-class weights for the final layer, now on classes 8 and 9.

Still writing the bar-detector code: I'm computing the perpendicular distance for the horizontal, forward-slash, and backslash orientations, then zero-centering the Gaussian profile and scaling it so a clean stroke gives roughly 1.

Still working on the filter code: I'm making the ring detector zero-sum by weighting the outer ring positively and the center negatively, so it only fires when the center is empty and the surround is inked.

Still writing the conv2 kernels: I'm scaling each mask so its weights sum to a fixed total, and boosting the fully connected weights to keep the logits in a reasonable range.
