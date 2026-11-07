Now the eight and five templates are dominating. Eight has no E template and only dense stroke templates, so after centering its weights come out positive wherever there's ink and carry no negative E components, and classes with fewer positive entries are losing out.

I'm weighing a nearest-template formulation: the logit would be 2·x·t minus the squared norm of the template, which penalises dense templates and gives a natural per-class bias. The catch is that this only works if the features are on the same scale as the templates, and I'm not sure they are.

Sparse templates can tie with the correct class when one is a subset of another, so the subtraction of the template norm would need to be large enough to break that tie, and I'm checking whether it actually does.

I'm now trying to split the difference: a per-class weight vector centered over the 16 cells, so an evenly inked image scores zero for every class, though I'm not sure centering across classes achieves quite the same thing.

I'm working out that a per-map centred template gives each class a weight vector whose dot product with the features is a covariance, so an 8 input scores by its variance and a 0 input scores by its covariance with the 8 template. Normalising each row to unit norm would turn that into a correlation scaled by the input's norm, which should not depend on how large the feature magnitudes are.

I'm checking whether centering each class's template over the 16 cells makes the logits behave like correlations, so the scale of the features wouldn't matter. Channels with different magnitudes are still a concern, but the centering should absorb uniform offsets. The remaining worry is that blurred feature maps might weaken the match, though correlation should tolerate that. The loss at 24% accuracy suggests the wrong classes are still getting too much confidence, so I need to pick a scale that tempers that.

I'm setting the logit scale to 1.5 so the range lands near ±3, given the row-normalised correlations and a feature norm of roughly 2 to 3. I'll also keep an eye on the 7→9 and 4→8 confusions, though I'm not sure yet whether the diagonal stroke is the cause. The per-class bias stays at zero, and the 5x5 duplicate channels stay at 0.5.

Now I'm centering each class's template per channel map and concatenating them into one vector, with the duplicate channels weighted at half. Then I'll normalise each class vector to unit norm and multiply by the scale.
