The model is getting worse, with loss at 18.7 and accuracy down to 14.6%, mostly guessing 4 and 8. Its wrong predictions are overconfident, which points to the template matching failing, possibly because the scale is too high, the templates aren't discriminative, and max-pooling makes the features look alike. Now I'm checking whether the 4 and 8 templates are the ones pulling the predictions toward those classes.

I'm working through why the max-pooling makes the features nearly uniform, so the logits end up tracking each template's total weight. That would explain why the digits with the most ink, like 4 and 8, keep winning, while 0 doesn't.

The blurring from the 5x5 averaging in conv1 is washing out the spatial detail, so after max-pooling the 12x12 grid is effectively much coarser than it looks. Maybe I need a more localized first layer, something that responds sharply to strokes and stays sparse, so the max-pool still keeps where the ink is. This looks like a hard problem under these constraints, so I'll step back and look for a different approach that can give better discrimination.

Rather than relying on ink density, which saturates, I'm considering sparse edge or contrast detectors so max-pooling keeps the location information. Hand-designing an accurate MNIST CNN is hard, so I'll go incrementally and aim to get back above 20% first. The 4x4 template at scale 12 reached 20% but collapsed onto a few classes, so I'm thinking about tuning fc.bias to even out the predicted class frequencies.

I'm weighing whether to lower the bias on classes 4 and 8, since they dominate predictions, but the features are nearly useless given the huge loss. I think the better move is to redesign them to be sparser and more discriminative, perhaps using a profile of ink by row and column rather than raw density.

I'm reconsidering the conv1 design: ReLU'd ink density saturates on dense digits, so max-pool loses where the strokes are. Sparse edge-style detectors that fire only at stroke boundaries might keep location information through the pooling, though hand-designing the whole network with only loss, accuracy, and confusion feedback is hard, so I'll build it incrementally.

I'm thinking about whether I can get more useful features by making the ReLU threshold sparse, so only strong-ink cells fire and max-pooling keeps location instead of saturating.

Adding a negative bias so that only strong-ink cells pass the ReLU could keep the max-pooled features sparse and location-specific. The threshold is the open question, since a value around 0.3 might cut away too much of the stroke signal, given that typical stroke density in a 5x5 average sits near 0.2 to 0.5.

The threshold at 0.3 still leaves every digit filling the center, so the features come out similar across classes. The real discriminating detail is fine stroke shape, and the 5x5 averaging followed by max-pooling blurs that away. I'm thinking about a more localized first layer, something with a smaller effective kernel, so the spatial information survives.

I'm weighing a single-pixel sample in conv1 to keep full resolution, but that would make the input binary and noisy. A small 3x3 average centered inside the 5x5 kernel looks like a reasonable compromise, keeping more detail than the full 5x5 blur, so I'm working out what the 28-pixel input resolution leaves after that.

I'm sticking with the 3x3 blur inside the 5x5 window, which still gives a 24x24 output that pools down to 12x12. Each of those cells covers roughly two input pixels. I'm planning a delta-offset sampling across channels to get a finer ink map, and I'm wondering whether a threshold bias could keep it sparse. Since the max-pool problem and the heavy processing make this hard, I'll go back toward the step-one template approach, which at least reached 20%, and try to improve it with a finer map and a lower scale to avoid the huge loss.

Rather than fixing the delta sampling, I'm now questioning whether it's even the culprit: the step-one version averaged over a 5x5 window and still reached 20%, yet the delta version scored much worse, so blur doesn't seem to be the main problem.

Why only digits 0, 3, 5, and 9 get predicted while the rest never win: with ink features that are nearly uniform across the center, each class logit tracks the total weight of its template, so a template's sum decides the winner. I'm checking whether that sum-based effect explains the collapse.

I'm now trying to make the templates zero-sum across cells, so the constant part of each feature map cancels and only the input-dependent variation drives the logits.

I'm realizing the templates should be zero-mean across cells, so a flat feature map cancels out and only real spatial differences drive the logits. Subtracting each template's spatial mean would turn the scores into true shape matching rather than total-ink comparisons. Combined with balancing the classes, that might finally let the less frequent digits win.

I'm now making each template zero-mean across cells, so a flat feature map contributes nothing and only real spatial variation drives the scores. I'll also switch to a sharper 3x3 average in conv1 and keep the delta sampling, but with a smaller scale, since the earlier version's overcounting made the logits explode.

I'm normalizing the fc weights so each template has a comparable scale, and I'm considering going back to the step-one conv2 averaging, with a 4x4 map, while keeping the zero-mean templates.

Next I'm normalizing each digit's template to unit length and keeping the zero-mean version, so no single digit wins just by having a larger template. The aim is to stop the constant-feature effect from deciding predictions.

Setting the scale at 8 with unit-norm templates should put the logit spread in a workable range, and zeroing the fc bias leaves calibration to the feedback loop.

I'm making the fc weights zero-mean directly, so that a constant feature map gives every digit the same logit, and then normalizing them so no digit wins just by having a bigger template.

I'm making each digit's weight vector zero-mean across all its entries, so a flat feature map contributes nothing, and then normalizing it so no digit wins just by having a larger template. I'm also keeping the subtraction of the shared average template, since that should make the distinctive parts stand out.

Checking the grid alignment now: the 12x12 templates put ink around columns 2 to 9, and the pooled ink map should cover roughly the same span, so the offsets should line up with the digit.

Since this is the same code being written, I'll keep it short: Writing template weights...
