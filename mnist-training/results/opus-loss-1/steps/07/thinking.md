The current best loss is 1.0021 at step 4, so I need at least a 1% improvement by step 9, to get under 0.992. Simple tweaks won't get there. The loss sits near 1.0 while accuracy is about 69%, which suggests the model is overconfident, so I'm considering scaling the logits with a temperature and tuning s2 to see if that brings the loss down.

I'm weighing whether the high loss near 1.0 with about 69% accuracy points to overconfidence, and whether a temperature or an s2 adjustment could lower it, though better features or templates would be needed for real accuracy gains. I'm also looking at the 7-to-2 confusions, since the 7 template's diagonal may be off.

I'm weighing whether the image features are as useful as they could be: the centre-tap and max-presence groups saturate under blur, while the amount features are more graded. I'm considering whether dropping some groups would help, or whether finer orientation channels would sharpen the curve discrimination, though that adds complexity.

I'm thinking the templates might be the real bottleneck, since real digit means vary across writing styles while my stroke prototypes don't. Blurring more and loosening the orientation tuning could make the features softer and closer to how real digits look, so I'll try a larger blur and a broader orientation response.

I'm going to try a larger blur, going from 2 to 3, on both the amount and max-presence features, since the broader smoothing should make the templates match real digit variation better. I'm also considering a softer orientation response, so that a stroke 22.5° off still gives roughly 0.6 instead of dropping off sharply. I'll leave the s2 temperature unchanged for now and check whether the step 6 column sums suggest any bias correction.

I'm checking the column sums of the step 6 confusion matrix, which all come to 10000, and I'm going to work out a bias correction from the true-to-predicted ratio for each class.

Rather than keep guessing at fixes, I'll go with the blur change plus a bias correction from the step 6 column sums, since that's a more predictable gain.
