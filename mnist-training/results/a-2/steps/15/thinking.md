At 71.4% I need a bigger jump, so I'm rethinking the feature design to pull out more information for the NB templates. One idea is to keep 8 orientations at conv1 and add clipped presence features, since the parts currently contribute almost nothing.

I'm weighing a denser sampling option: shifting a second set of orientation features by two pixels to get an interleaved grid. The concern is that correlated duplicates might double count, though the regularization may partly offset that. I'm also wondering whether the model is limited more by template mismatch than by feature resolution, and I'm considering a blur sweep on the template spread as a cheaper test.

I'm weighing whether to lower the off-template penalty by raising the base rate, and I'm thinking about testing a broader template spread first, though it's only a small expected gain per tweak. A bigger possible step is second-stage pairwise discriminators on conv2 features aimed at the confusable digit pairs, since their larger receptive field can relate strokes roughly 10 px apart.

I'm working out corner-type features, the ┌, ┐, └, ┘ shapes, to separate pairs like 3 and 5, since a 5 has a top-left corner that a 3 lacks.

I'm sketching corner detectors for the four orientations of corners, so the ┌ shape can separate 5 from 3, with each arm about two cells long.

I'm now considering whether the arc features should be swapped for corner detectors, with arm cells placed at distance one to two so rounded handwritten corners still register, and I'm sketching the four-corner set alongside the existing loop feature.

I'm sketching a plus-shaped detector for crossings, since a 4's crossbar runs across the vertical stroke while a 9's stem only meets its loop, and I'm checking whether the horizontal arms on both sides of the center are what separates them.

I'm assigning the corner detectors to specific digits: the top-left corner for 5, the top-right corner for 7, and the bottom-left corner for 4. I'm also estimating how strongly each corner shows up in the digits that share it, lowering the weight where the shape is only rounded or incidental.

I'm checking whether a corner detector would still fire on a rounded loop's top-left, since the arms would sit on the loop's top and left sides relative to the corner point.

I'm checking whether the corner detectors would also fire on the top-left of rounded loops and 0s, since their arms sit close enough to the curve to register. The empty corner point would weaken that match for rounded shapes, while a sharp 5 corner keeps full ink and no penalty. Replacing the arc features with these corners seems low-risk, because the parts currently add almost nothing, and I'm asking myself why the parts contribute so little in the first place.

I'm wondering whether the strict parts rarely fire at all, which would explain why they add so little. Before spending more steps on new features, I want to test the strict loop detector directly, using lower thresholds and checking the top and bottom loops separately.

I'm picking thresholds of 0.15 and 0.7 for the loop check, since those midpoints fall between the lattice levels I'm testing.
