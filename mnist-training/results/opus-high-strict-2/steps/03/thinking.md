The biases are dominating the output: class 4 is now over-predicted and class 8 under-predicted, so the logits look flat and the template margins are small. I'm wondering whether the temperature β is simply too small, since a larger β would sharpen the predictions and shrink the relative effect of the biases.

I'm weighing whether discrimination needs sparser, more selective features, like a higher conv1 threshold or sharper orientation tuning, rather than just tuning β. I'm also considering per-class mean-subtracted correlation, which rescales each template by its own mean and spread.

I'm considering Pearson correlation for matching, with each template centered by its global mean and normalized, which penalizes ink where the template is empty and gives each class a different offset on the total ink.

I'm switching to Pearson correlation for matching, with each template centered by its global mean and normalized, and I'm setting the temperature to about 3 with the biases reset to zero, then calibrating from there. I'm leaving the conv1 threshold alone for now so I only change one thing at a time.
