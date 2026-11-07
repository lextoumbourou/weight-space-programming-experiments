I'm checking why the Gaussian approach keeps collapsing onto a single class, likely a scale mismatch between the quadratic term and the feature values. The dense rasterized prototype for 8 seems to dominate, so I'm testing whether the class with the largest total mu wins on weak feature images, starting from the score expression.

I'm working out whether the features really are larger than my occupancy estimate, since the sinks suggest f might be around 0.8 on strokes, which would push the gain toward 2.5 or more.

I'm checking whether the features really are larger than my occupancy estimate, since the sinks suggest the dense class's cells have f above mu, so raising the gain would pull mu toward f. I'll re-estimate the feature magnitudes through the conv and pooling stages, and consider that MNIST strokes may be thicker than I assumed.

I'm weighing a cosine-style score, dividing each prototype's dot product by its norm, since that would remove the mass bias toward dense classes. I'm also considering centering the features by subtracting a constant threshold before scoring, though I haven't settled on that yet.

I'm centering the prototypes by subtracting the mean across classes, and centering the features too, since the average-like prototypes keep winning the sink.

I'm checking whether centering the prototypes changes anything: subtracting the mean across classes leaves the Gaussian argmax the same, but it would alter the cosine-style score and how the bias term behaves.

I'm checking whether centering the prototypes actually changes the Gaussian argmax. Expanding the squared distance shows that subtracting the mean across classes only adds a class-dependent cross term and a norm term, so the argmax stays the same, and only a different bias form would shift it.

I'm weighing whether a bias-free dot product would work, but it would just favor the dense class, since the class-independent term drops out and leaves f·mu_d. So the bias has to be something like a penalty on the prototype's squared norm.

I'm weighing a bias term proportional to each prototype's total mass, to counter the dense-class advantage, but the Gaussian's quadratic penalty is the principled choice, so the real question is the feature magnitudes. The earlier sinks suggest the direction, since the dense class keeps winning at higher gains.

Trying a much lower gain would shrink the prototypes below the feature values, but if features exceed the prototypes everywhere, the score keeps rising with mu, so the class with the most ink would win. That matches the dense-class sink I'm seeing with class 8. So the real question is whether the prototypes are larger or smaller than the features.

I'm settling on a gain of about 2.0 for the ink and orientation features, since matching the prototype magnitude to the feature magnitude should stop the dense class from dominating. I'm leaning against clipping the prototypes at 1 because that would weaken class 8, and I'm noting that earlier runs at gains 1.0 to 1.5 gave accuracies of 36%, 22%, and 20%, which argues against those lower settings.

I'm wondering whether the trend across gains is really monotonic, since the step 7 result at gain 1.2 doesn't line up cleanly with step 5 at 1.5, especially now that orientation channels were added. Rather than keep tuning the gain blindly, I'm considering whether the conv2 blur on the orientation channels is being used correctly, and I'm leaning toward a different calibration approach.

I'm now wondering whether to drop the rasterized approach and go back to the zero-mean linear template method that gave 43.6%, since it might do better with better-drawn templates and orientation channels.

I'm seeing that subtracting each class's mean occupancy makes the penalty on dense classes scale with the image's total ink, which is why the zero-mean template approach gave 43% earlier. So a linear classifier with per-class centering could be a principled way forward.

I'm now checking whether zero-mean per-class prototypes change the picture: with each class centered across cells, the score has no bias term, so the overall gain no longer affects the argmax and only the relative shape of each prototype matters.

I'm checking whether zero-mean prototypes avoid the dense-class bias: for the 8-like image with uniform feature mass, the centered weights sum to zero, so that dot product comes out near zero rather than favoring the dense class.

I'm noting that zero-mean prototypes make each class's weights sum to zero, so a uniformly inked image scores near zero everywhere and the dense class loses its advantage. A digit with ink concentrated in the center should still pull ahead for its own class, but ties between classes on evenly inked inputs will need a finer tiebreaker.

I'm noting that a zero-mean classifier is essentially invariant to total ink, which is why it avoids the dense-class bias. Step 2 already did exactly this with hand-drawn 4x4 templates and reached 43.6%, so the approach itself works and the next gains should come from better templates. Adding per-block zero-mean terms in step 3 dropped accuracy to 30%, which suggests the extra blocks are contributing noise rather than signal.

I'm reconsidering whether per-channel scale matters. I'll try zero-centering each class's prototype across all cells and channels together, so the orientation and ink channels contribute on the same footing, and draw the oriented templates as rasterized occupancy maps.

I'm checking whether zero-centering each class's prototype across all cells and channels removes the dense-class bias, since the centering pulls out the class's average level. The concern is whether a class with higher average ink ends up with weights that still favor it.

I'm checking whether the zero-mean approach avoids the dense-class sink, since without a mass bias the Gaussian's 8 problem should go away. A sparse class with many negative weights might still pick up ties on low-ink images, so I'm also thinking about how small noise would decide those cases.

I'm going to try a zero-mean prototype for each class over all cells and channels, so the total ink no longer biases the score. Since the score then has no bias term, the overall gain won't affect which class wins, and I'm working out how to weight the channels against each other.

I'm going to build each class's prototype across all five channels and 16 cells, then subtract the overall mean so the weights center on zero. Since the score has no bias term, that centering keeps a dense class from winning on total ink, and I'll use the occupancy values directly with equal channel weights.

I'm double-checking the orientation canvas ordering so each channel maps to the right index, then I'll confirm the scale of the zero-centered weights.

Writing the zero-mean prototype code, building the 80-entry vector per class and scaling it...

Still writing the zero-mean prototype code...

Still writing the prototype fill-in code...
