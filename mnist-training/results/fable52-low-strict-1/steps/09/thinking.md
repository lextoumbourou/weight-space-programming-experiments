The score has climbed to 0.729, and the bias changes shifted one result noticeably (425 to 580), so the logit margins look fairly large. The loss is 0.91 at 73% accuracy, and I'm not sure raising the scale would help, so I'll leave that alone. Next I'm considering structural changes: the feature set only draws on 4 of the 8 conv1 channels, and the templates are single prototypes, so I'm weighing a few targeted improvements.

I'm working through the confusion pairs now: the slanted 1s account for many of the 1→2 and 1→7 errors, so I'm considering a slant variant for the 1 template, with its weight reduced a bit to avoid pulling in other digits. For the 0→6 and 4→9/4→8 errors I'm adjusting a few biases and adding a farther-right negative stroke on the 6 template, with some doubt about whether it will hurt 6's recall.

I'm placing a negative stroke for 5 just right of the 3's upper arc, and a similar one for 3 along the base of the 2, then I'm reconsidering whether a negative stroke for 2 near the 8's lower-right corner would land correctly.

I'm adding a few negative strokes to separate the confusable digits: one for 9 against 4, and others for 8 and 2 in the lower-left. I'm also considering a tuned horizontal stroke for 6 to set it apart from 5, and I'm checking whether a negative for 7 near the upper-left would help with the 9→7 errors.

I'm dropping the non-zero-sum penalty to 0.08, since the earlier 0.12 version hurt the blobby templates, and I'll be more selective about where the negative strokes go. I'll keep the tuned model from step 8 as the base for this pass.

Continuing the tuned model from step 8, I'm applying the cosine-clipped version to finish this pass.
