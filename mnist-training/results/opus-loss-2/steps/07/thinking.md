The feedback signal only gives aggregate information, so I can't learn 2560 weights from 44 steps. A stronger move would be to improve the features, since a carefully designed set of orientation, ink, and arc features on a coarse grid might get well past 90%, and I want it to stay robust to position shifts.

I'm looking at the confusion pairs now, with 5→6 and 2→8 as the largest. I'm also weighing a scale-change test, since the logit magnitude affects the loss and that test would be cheap to run in a single step. A nearest-mean classifier using squared distance to expected feature vectors might fit this setup better than the current template correlation.

I'm comparing the 5 and 6 shapes now: the 6 has a stroke running down its left side into a closed loop at the bottom, while the 5's bowl opens to the left there. I think an orientation feature at around x 8.5, y 16.5 should separate them, though real digits vary enough that I'm not sure it's reliable.

I'm considering whether a nearest-mean classifier, using squared distance to expected feature vectors, would work better here than the current template correlation. I'm also wondering if the mean templates of each digit's variants are blurring the signal, and whether my drawn positions match real MNIST digits.

I'm weighing a small pairwise adjustment for the top confusions, with λ around 0.25 and no zero-sum constraint, and I'll test it on its own before combining it with the bias round and the scale check.

I'm weighing whether a small pairwise adjustment, with λ around 0.25 and applied to the 5/6 pair, could correct the asymmetric errors where 5s get pulled toward 6 far more often than the reverse. A bias shift alone won't fix that since the bias is already calibrated on global counts, so I'm considering a difference-of-templates term instead, though it moves the decision boundary in both directions at once.

The pairwise term turns out to be a no-op for 5 versus 6: since the mean cancels, the update only rescales the existing difference between those two templates. So the 5/6 boundary is set entirely by the templates themselves, and any real fix has to come from changing them or the features.

I'm going to test a scale change alongside another round of bias adjustment. Since the 5/6 boundary is fixed by the templates and the biases, I'll look at the 2 and 4 pair next, since their confusion count is high.

I'm comparing 2 and 4 next, where the 4's stem and crossbar might overlap with the 2's top-left curl, and I'm wondering whether real 2s are shaped differently enough from my drawings to matter. The 7→2 confusion seems to come from the 7's diagonal stem resembling the 2's upper-right to lower-left stroke. I suspect my templates are too thin compared with real strokes, so I'm considering whether the Gaussian sigma of 2.5 is the wrong width, though I can't tell which direction would help.

I'm going to try a scale change of 3.6 together with another bias round, scaling the biases by 1.2 so their effect stays consistent with the rescaled weights. I'll keep it to this one main change so the scale effect is easy to read.

Next I'm rebalancing the per-digit biases against the observed counts: 7 is badly under-predicted and 6 is over-predicted, while 2, 3 and 8 need small nudges. I'm also planning to add a curved-top variant for 7 and a straight-stem variant for 6.

I'm deciding to drop the 7 variant, since a stem that steep might read as a 1 or 9, and I'll leave the 7 fix to the bias round. Next I'm running the scale change at 3.6 together with the bias update, scaling the biases by 1.2 to match.
