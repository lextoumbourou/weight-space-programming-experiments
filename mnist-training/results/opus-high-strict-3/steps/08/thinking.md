The last approach came out worse, so the template matching itself looks like the weak point. With eight steps left I need something sturdier. Raw blurred ink features with pixel templates are one option, but my hand-drawn means would probably land below the real-mean nearest-centroid result of about 82%, so that isn't clearly better. I'm wondering whether the network's own features could be made more invariant so that the templates line up with them.

I'm wondering whether the trouble is that the real feature distributions don't match my template assumptions, and that cross-orientation leakage and thick-stroke edges are part of the reason. The step 7 numbers show 8 pulling in too many confusions, so the features clearly differ from what I'm modeling. Going back to make incremental template and bias edits might reach around 75%, or I could try making the first conv layer itself more robust, using the remaining steps as experiments.

I'm estimating typical MNIST mean shapes from memory, like the ring of a "0" and the diagonal bar of a "7," to see if better hand-built templates could beat the current ~70%. My row placement still needs to match where real digits sit in the 20-pixel box.

I'm wondering if the trouble is with how the templates are built, since the max-union shapes might have a different sharpness than the real features. I'm also weighing whether the 3 and 5 confusion at the top could come down to where the vertical strokes sit, which should still be visible on the 8x8 grid.

I'm checking whether the digits might be a bit smaller or shifted relative to my templates, since the 20-pixel box and grid alignment look fine on paper. The center-of-mass target and the stroke width seem close enough to be a minor factor. The bigger lever looks like tuning the biases from the confusion pattern and making targeted template edits at steps 5 and 6, which might get me to around 75%.

I'm wondering whether adding more orientations would help much, and I doubt it would. The thick-stroke concern is that edge responses might sit slightly off-center, but with blur that should still line up well enough. Loops at a 2-pixel grid look workable too. I may have to accept the template-matching ceiling and look for simple global features the fully connected layer can exploit.

I'm weighing whether a centered-template variant would help, since it would penalize ink in proportion to each template's mass. That might favor compact shapes like the 1, which could explain the 8→1 and 4→1 errors, while the 3→5 and 5→8 errors point elsewhere.

I'm considering a uniform penalty over the central digit region to counter the "1" attraction, since dense central ink currently favors the compact 1 template. Subtracting a per-class share of that uniform mask should make generic ink score equally across classes. Step 4 tried a similar correction with a different mask and made the 8→1 errors worse, so I'm not confident this will help.

I'm weighing whether to skip the template-matching tweaks and instead try small conv1 bias changes, or to tune the classifier biases from the step 5 confusion counts. Step 5 is still the best at about 70.8%, so I'll start from there and check how the predicted-class totals are distributed.

I'm comparing the predicted-class totals against the approximate true counts: class 1, 6, 9, and 7 are over-predicted, while 4, 5, 8, and 3 are under-predicted. The margins between top classes look small, so bias shifts of about ±0.3 could move a lot of decisions. I'll keep that in mind when I look at step 6, which also changed the templates.

I'm going to revert the "1" template to a single slanted line, since the union version pulled in too many 8s and 4s, and then recheck the biases against step 5's counts.

I'm comparing the step 6 confusion counts against step 5: 3→5 rose, 5→8 rose, and 5→6 fell. Next I'll try reverting the 8 template to the step 5 version, lowering the bias on 5 and raising it on 3, and keeping the single-line 1 template.

I'm going to try a 4 bias increase, since the 4s are under-predicted, and then give 2 and 7 a look. I'll leave the 2 bias alone for now, since its count is already fine, and nudge the 7 bias up a little because some 7s are landing on 9.
