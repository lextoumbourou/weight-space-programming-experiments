The loss is 29, so the logits are far too large and the model keeps predicting 8. Class 8 has the most ink, and the blob templates pick up that total amount, so the centered weights give 8 the biggest values. I should shrink the scale and remove that ink-amount bias by making each class's weights zero-mean.

I'm adding a per-class constraint so each class's weights sum to zero across the cells of each channel, which should cancel the ink-amount bias. The trade-off is that this may blur the difference between a 1 and an 8, since ink amount is part of what separates them.

I'm setting the scale to 0.3 and checking whether the per-channel cell zero-sum also covers the orientation channels, since their totals track overall ink. Then I'll keep everything else the same and normalize the weights to a max of 1 after centering.
