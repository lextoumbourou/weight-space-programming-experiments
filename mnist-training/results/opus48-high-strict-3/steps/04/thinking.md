The loss has dropped to 2.81 and accuracy is up to 22.7%, but the predictions still lean heavily toward 4 and 8. Even with sharper features, those two keep winning, so the problem seems to be something other than feature quality. I'm now wondering whether the templates are misaligned with where the digits actually sit in the features, which would let the widest templates dominate.

I suspect the templates and the digit ink don't line up with the feature grid, so the central horizontal bar of the 4 template is matching the center of nearly every digit. Next I'm working through the pooling arithmetic to map each feature back to its original pixel position.

I'm checking the pooling arithmetic now: after the second max-pool, each position maps back to a block of original pixels, and I'm tracing where the digit's center of mass lands in that coordinate grid.

I'm checking how the pooling maps feature positions back to original rows, and the second max-pool samples M1 rows roughly 0 through 10, which leaves out row 11 at the digit's bottom edge. That seems like a minor gap, so the alignment is mostly fine.

I've confirmed the feature grid lines up with the digit's center, so misalignment isn't the cause. Something else is making 4 and 8 win, so I'll look at why a 9 would score higher against the 4 template.

I'm wondering whether the templates are too thin compared with real MNIST strokes, which would penalize the ring-shaped digits and favor 4's broad central bar. Thickening the templates or adding per-class bias corrections might counter the dominance, though the hand-drawn templates may simply be the weak point.

The bias trick might rebalance the predictions, but it only moves errors around if the scores don't really separate the classes. Looking at the diagonal counts, digits 1, 4, 8, 6 and 0 carry some signal, while 3, 5, 7 and 9 are close to zero.

I'm checking whether the feature positions are sampled unevenly, since some positions in the pooled grid get hit more often than others and would carry extra weight in the templates' scores.

I'm counting how often each feature position gets sampled by the pooling, and the central rows and columns get hit about twice as often as the edges. That means the central template cells end up carrying up to four times the weight of the edge cells, which tilts the scores toward whichever template has the most central mass.

I'm realizing the central cells get counted up to four times as often as the edge cells in the feature vector, so templates with a lot of central mass gain an unfair boost. I want to fix that by weighting each position by how often it's sampled, so the scores reflect real feature-space contributions.

I'm correcting for the uneven sampling: the central rows and columns get counted about twice per axis, so I'll divide each feature weight by its count so every position contributes equally to the correlation.

I'm working out how often each feature position gets sampled by the pooling, so I can tell whether the central cells are being counted more than the edges. The pooled grid's lower-row indices show up about twice as often in the middle as at the edges, so I'm planning to divide each template weight by its sampling count to even out the contribution.

Dividing each template weight by its sampling count, so the central cells stop being overcounted, and I'll keep the scale in mind since the values shrink.

I'm writing the feature weights so each template cell is divided by how many times its pooled position gets sampled, with a scale of 2.0 to keep the magnitudes reasonable.
