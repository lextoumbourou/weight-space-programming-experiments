The model is at 28% accuracy with a loss of 6.1, which suggests the logits are too large. Predictions bunch up on 5, 1 and 9, so I'll check whether the template weights for 5 and 1 are driving that.

I'm weighing whether the emptiness feature is overpowering the stroke features, since its values sit near 1 while stroke responses are closer to 0.3. That could explain why class 1, with its many empty-side cells, keeps getting picked. I'm also checking whether the stroke detectors fire at all on thin or antialiased digits.

I'm going to rescale the orientation features, since their responses are around 0.1 while the emptiness features sit near 1 and dominate. Doubling the conv1 weights and bias should bring a typical present stroke up to around 0.4 to 0.8. Raising the conv2 pooling weights to 1/3 should then let a stroke crossing three of the nine cells land near 0.6.

I'm going to scale the emptiness and orientation features against each other, since the empty-area signal currently dominates. I'm also considering whether to fold in a bias term that accounts for class template sizes, because digit 5's dense template seems to be pulling in too many other digits.

I'm considering normalizing each class's weight vector to unit L2 norm, so that the larger templates like 5 stop pulling in other digits. The ink penalty of -0.5 may also be too strong now that the ink features sit around 0.7, and I'm thinking about the duplicated 5x5 averaging as a possible source of confusion.

I'm going to double the orientation filters' weights and bias, and loosen the bias to -0.4 with a 2/15 positive weight per cell, so a clean 3px stroke still comes out at about 1.6.

I'm rebalancing the feature scales so the stroke detectors aren't drowned out by the emptiness feature. I'll bring the conv2 pooling weights up for strokes and ink, keep them low for emptiness, and then L2-normalise each class's weights so the bigger templates stop pulling in other digits. A final scale of about 2 should keep the logit gaps reasonable.

I'm settling on a scale of 2 for the final weights, which should keep the logit gaps reasonable after the L2 normalisation.
