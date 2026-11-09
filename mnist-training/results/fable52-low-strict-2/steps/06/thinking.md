The step 4 settings are slightly worse, so I'm reverting to tanh/5, σ=3, shears [0,0.25] and looking for a structural change instead. We're stuck around 68%, and the limit may be how I picture digits or how the features are designed. The 0→6 errors from 104 to 259 keep showing up, which suggests a 0 is matching the 6 template better than its own, and I'm wondering whether the elliptical zero with negative centre strokes is the cause.

I'm weighing whether the zero's negative centre strokes are the real problem: the vertical ones sit only about 3–6 px from the ring's sides, so the σ=3 blur bleeds them into the zero itself. Limiting the zero's centre suppression to short horizontal strokes would keep them about 10 px from the top and bottom of the ring, which should still suppress the 6's loop without penalising the 0.

Considering whether a plain linear classifier on oriented-gradient features could reach around 97%, since orientation maps at this cell size should separate the commonly confused pairs like 7/9, 4/9, 3/5 and 0/6. I'm also wondering whether replacing the redundant offset-grid channels with different features, such as stroke endpoints or curvature, would help more than another tweak to the current ones.

I'm looking at making the template contrast explicit: for each digit, subtracting a small share of the templates of the digits it gets mistaken for, using the confusion counts as feedback. The 0→6 case would mean pulling some of the 0 template out of the 6, and I'm weighing how far to push that before the weights stop being meaningful.

Still working out the pairwise version: each digit's template would have a fraction of the templates of the digits it gets confused with subtracted from it, with the confusion counts setting which ones, and I'm going to try that from the step 4 base.

Next I'm working out the per-digit weights for the confusion-driven template contrast, with the heavier penalties going to the most frequent confusers like 8 for 2 and 0 for 2.

I'm now weighing a targeted version of the template contrast, where each class subtracts a share of the templates of its most frequent confusers, with a fixed fraction of about 0.12 per unit of confusion weight. The column for 7 is the heaviest, so I'm checking whether the total subtraction stays reasonable relative to the mean term, which I'd lower to about 0.6. I'm also wondering whether subtracting the 9 template from the 7 would start eroding the shared top stroke.

I'm settling the template weights now: the 0 template's centre suppression is limited to short horizontal strokes, and each class subtracts a fraction of its main confusers' templates, with the heaviest penalties on 7, 2 and 8. I'm keeping the step 4 biases and holding the mean coefficient near 0.6.
