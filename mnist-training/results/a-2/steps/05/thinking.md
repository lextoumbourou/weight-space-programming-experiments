The feature approach has stalled around 60% accuracy, so I need stronger features. The 7 confusions with 2 and 9 are the main problem, and 7 itself is recognized only 179 times. I'm checking whether my 7's diagonal stroke is too slanted, comparing its angle against the stem I'd expect from a real 7.

Now I'm checking whether the 2 and 9 confusions come from how I'm picking up orientation, since the conv1 kernels might not separate a vertical stroke from a horizontal detector well. The mean-subtracted kernel probably gives only a weak response to vertical strokes, so the selectivity may be weaker than I'd like. I'm also wondering whether the template approach is fundamentally limited, because the coarse features may not capture the topology that separates these digits.

Now I'm weighing whether the 3s get confused with 5s and 8s because their left side is open, while the 8's closed loop has vertical strokes in those same cells. I'm also considering whether the templates I'm hand-crafting can carry enough detail to separate these digits, since I can't check them against real data.

I'm weighing whether the orientation channels, with their Gaussian proximity at 4x4 and sigma 3, are too blunt to separate these digits, and whether the intensity channel weight is drowning out the differences that matter.

I'm now thinking about a more targeted option: hand-designed features for the confusable pairs. For 7 versus 9, the 9 has a closed loop with a left vertical stroke and a bottom horizontal, which the 7 lacks at the top left. The 3-versus-8 split comes down to left-side verticals, and 2-versus-7 to the bottom horizontal stroke. Nearest-centroid weighs every feature equally, so an LDA-style weighting of these discriminative cells might help more. I also want to recheck my cell-center mapping before trusting any of this.

I'm checking the pooling arithmetic: the pool2 cells center on input rows around 4r+7.5, so the grid spans roughly 7.5 to 19.5, while the digit itself runs from about 4 to 24. The edge cells should still pick up the outer strokes through the blur.

I'm considering whether to add more orientation detectors or extra conv2 channels for finer sub-cell detail. My guess is the templates are the real bottleneck, not the feature set, so I'm weighing whether a more careful per-digit refinement is worth the cost in remaining steps.

I'm weighing whether to test a different scale for the templates, since if the real features are much weaker than the template values, the bias term could be unfairly favoring the sparse 1 digit over the others. I'd try a smaller alpha to see if the balance between big and small templates improves, and I'm also thinking about sketching the mean shape of a 7 from memory to compare it against my current template.

I'm comparing the 7, 2, and 3 confusions against template size: the smaller 7 template may be losing to larger ones like 9 and 2 if the penalty scale is too weak, so I'm testing whether a smaller alpha fixes the bias toward big templates.

I'm considering raising the alpha scale to 0.6 so the bias penalty grows, since the over-predicted big templates suggest the real features are larger than my current α·T values. I'll keep the change to that one knob for now and scale the other term so the logit gap stays comparable.

I'm settling on the scale factor now: I'll keep the product of the scale and alpha squared near 2.4, which puts the scale factor at about 6.7 when alpha is 0.6.
