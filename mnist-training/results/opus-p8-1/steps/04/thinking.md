Both 1-channel features the template gives come out biased: the zero-mean template for digit 1 is concentrated, so after normalization it reads strongly positive at the center vertical. I'm wondering whether the feature design itself needs rethinking, since the maxpool magnitudes are unknown and I can't inspect the data, so feedback is the only signal. Maybe conv2 should be made to compute richer features, but first I want to pin down what is actually limiting performance.

I'm weighing whether to adjust the per-class biases instead, since the predicted counts show the model over-predicting 1 and 2 and under-predicting 4 and 8. Correcting biases from those counts might balance things without touching the features, though I can't yet tell whether partially subtracting the mean would help or hurt.

I'm weighing whether a partial mean subtraction could help the features, and whether per-class bias corrections from the predicted counts could balance the over-predicted 1 and 2 without changing the templates. I'm considering combining the step-2 templates with a half-mean adjustment and tuning the biases from matching-configuration counts.

I'm weighing whether to combine the step-3 full mean subtraction with bias corrections from its counts, or to go back to the step-2 setup, which had better accuracy and smaller count discrepancies. The step-3 errors toward 1 look structural, since 8s are landing on 1, which suggests the 8 template isn't matching its own ink.

I'm now weighing a bias correction on the step-2 setup, using the log ratio of true to predicted counts for each class, since 1 and 2 are over-predicted and 4 and 8 under-predicted. I'm also considering whether to raise the logit scale alpha, given the loss is still fairly high at this accuracy.

I'm computing the per-class row sums of the step-2 confusion matrix to get true counts, since the earlier totals don't match the validation size I expected. Digit 1 comes out to about 1064 and digit 2 to about 990, so I'll use these to set the bias corrections.

I'm adding up the per-class totals from the step-2 confusion matrix to confirm they sum to 10,000, and they do. Summing the columns gives predicted counts such as 1,125 for digit 0 and 1,591 for digit 1, which is the over-prediction I need for the bias correction.

Now I'm tallying the per-class column sums from the step-2 confusion matrix and taking the log ratio of true to predicted counts for each digit, to size the bias corrections.

Next I'm applying the log ratio of true to predicted counts as a bias correction for each class, with the shift taken at full strength since the softmax spread should soften its effect on the counts. I'm keeping alpha at 5 so the bias scale matches what I've computed.

I'm keeping alpha at 5 so the bias corrections stay on the same scale, and I'm going to apply the step-2 bias correction without changing anything else. I'll also look at refining the 8 template, since only 252 of the true 8s come out right and many land on 2.
