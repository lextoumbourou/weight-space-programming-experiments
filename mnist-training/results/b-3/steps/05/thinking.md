The feature scales I guessed look unreliable, since the eight-class term is dominating, which suggests the real feature magnitudes are larger than I assumed. Without running the network, I'll have to reason about the scale more carefully or pick features whose range I can control, like clamped or saturating ones.

I'm checking whether saturating features are even feasible here: ReLU alone can't clamp, and getting min-style behavior would need two channels combined at the fully connected layer, which costs capacity. Another option is to go back to the correlation-based approach from step 2, adding the ink penalty gradually. Before choosing, I want to work out the real feature magnitudes from the conv1 kernel's taper weights and row sums.

I'm working out the response for the horizontal kernel: the taper weights make the positive and negative parts of the zero-mean weights come out equal, and the central three rows give a full-intensity response of about 1.0. With the bias of -0.1, a solid 3-pixel stroke lands near 0.9, while a thin 2-pixel stroke drops to roughly 0.7.

Checking the first-layer response near the stroke, the value stays around 0.9 on the centerline and falls to about 0.35 when shifted by one pixel. After max pooling, a horizontal stroke should leave roughly 0.9 in each active pool cell along its length, and I'm now working out how that carries through the 3x3 average in the second conv layer.

I'm checking how the 45° kernel responds to a horizontal stroke, since its weights along the centre row shift with distance. Near the centre the response is strong, about 0.75 one step out and 0.3 two steps out, and I still need the mean to finish that comparison.

Working through the 45° kernel's response to a horizontal stroke, it comes out at roughly 0.4 to 0.5 after normalization, so the orientation selectivity is much weaker than I had assumed. Broad tuning like that would explain why so many features stay on and why the eight class wins.

I'm weighing a bias of -0.3 in the first conv layer to sharpen orientation selectivity, since it would push off-orientation responses toward zero. I'm also leaning back toward the step 2 correlation setup, where the features are scale-free apart from the bias, and adding a partial ink penalty on top of it.

Step 2's column sums still leave class 4 under-predicted and class 8 over-predicted, and changing the conv1 bias would reshuffle the features again. Hand-built templates keep losing to data-derived ones, and the confusion matrix is the only real signal I have, so I should design more carefully rather than keep flailing.

I'm settling on a combined setup: the step 2 correlation approach with the conv1 bias lowered to -0.3, per-class zero-mean weights to strip out the overall ink effect, and a bias adjustment for class 4, which is still badly under-predicted.

I'm now adjusting the template tuning to use a shifted cos² response, so that off-orientation features fall to roughly a quarter of the on-orientation response once the bias is applied.
