Reverting to step 23 is the fallback, since the last change made things worse. With two steps left I need a score of at least 77.77, so the next change has to actually move it. Tuning the learning rate or kappa is a possible small gain, but the bigger leverage is in geometry, where the largest remaining costs are the 3→5 and 5→8 transitions. The 7→9 and 4→9 transitions also stand out, so I'm weighing those next.

I'm weighing whether a slightly bigger shear on the 7s would help, though earlier tries with that shear dropped the 7s and didn't clearly fix 7→9. For 4→9, a closed-top 4 looks a lot like a 9 with an angular loop, and I'm trying to find a feature that separates them. I'm also considering shifted orientation windows in place of the 2x2 emptiness channels, or a small bias tweak on conv1, but those are single risky shots.

Bias tweaks look like they'd add only about 0.1 to 0.2, which isn't enough to reach the 77.77 target. To get a real gain I need something structural, so I'm turning to the 3 vs 5 confusion and what distinguishes the upper-right arc and middle cusp of a 3 from the top bar of a 5.

I'm looking at the 3-versus-5 distinction again: the 5 has an upper-left vertical stroke that a 3 lacks, while the 3 has a right-side curve in its upper arc. The trouble is that at this resolution those two areas are hard to tell apart. I'm considering a gentle pairwise weighting that boosts only the 3-versus-5 distinguishing features, rather than a global contrastive change like the one that failed earlier.

I'm weighing a pairwise tweak for the 3-versus-5 pair: either boosting each class's weight on the features that distinguish it from the other, or penalizing each class for the other's distinctive features. The boost would raise 3 for images with the upper-right curve, which could add confusion elsewhere, while the penalty would push down 5 for those same images, including some 8s.

I'm weighing a pairwise penalty for the 3-versus-5 and 5-versus-8 pairs, where each class is pushed down for the other's distinctive template features, computed directly from the templates.

I'm now sketching a generic pairwise penalty: for each confusion pair, lower the rival class's weight wherever the other class's distinctive template features show up. That would also need a small bias correction, since penalized classes will lose overall score.

I'm now thinking about a pairwise penalty for the 2-versus-4 pair, lowering the 4 score wherever 2-specific features appear, and extending the same idea to the other confusion pairs. Each penalty would be a unit-normalized difference of template features, scaled by a small weight.

I'm settling on a moderate penalty strength of 0.25 for the confusion-pair adjustments. I'm leaving the step 23 biases untouched for now, since the penalties will shift class scores and I plan to correct the biases in the next step.
