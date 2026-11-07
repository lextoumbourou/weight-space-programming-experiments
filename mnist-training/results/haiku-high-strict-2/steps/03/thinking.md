I'm noticing the model keeps predicting class 2 for most inputs, which seems off since the templates should be zero-centred and balanced. I'm checking whether the background features are actually zero: the conv2 channel 7 response on blank pixels comes out as zero, so the background contributes nothing to the logits. That leaves the class 2 bias coming from the ink images, and I'm wondering if one template is dominating the sum.

I'm checking the class 2 template weights: its centred values are large along the bottom row, and the centring doesn't remove that mass, so the per-cell differences are what drive the bias toward class 2.

I'm thinking the common-mode bias comes from the template-matching readout itself: with nonnegative features that are mostly central, a class whose centred template is positive in the middle cells gets a large dot product. Zero-centring the weights per cell only makes the logits sum to zero across classes, not make each class's score fair, since the individual differences still depend on the feature mean. The cleaner fix would be to subtract an average feature vector before the dot product, but I can't compute that without generating data, so I'm looking at a bias term instead.

I'm thinking about approximating the mean feature vector by hand, using the average of the class templates as a stand-in for typical per-cell ink, and folding its dot product with each centred template into a bias term. That would give a centring effect without generating any data. The catch is that pooling and ReLU make the real feature scale nonlinear, so I can't pin down the scaling constant exactly.

I'm checking why digit 1 images come out as class 2 when class 1's centred template should match them best, since its positive weights sit exactly on the stem columns. That suggests the feature magnitudes are off from what I'm assuming, so I'm now looking at how the max-pooled conv2 averages scale the features.

I'm estimating the feature magnitudes: at ink cells the pooled conv2 values come out around 2 to 3, so the logit differences could be fairly large, and the direction should still favour class 1 for digit 1. Yet the model keeps picking class 2, which doesn't fit that estimate.

I'm working out the receptive field of each final feature cell: after the two conv and pooling stages, each of the 4x4 cells covers a fairly large patch of the input, around 14 pixels or more and overlapping its neighbours. So the features are spatially coarse, and that blurring may be part of why digit 1's thin stem gets smeared into the features of other classes.

I'm wondering whether the bias comes from the features being roughly proportional to the mean template, so each class's logit picks up a term from how much its centred template overlaps with that average shape, and I'm checking which class overlaps the most.

I'm settling on subtracting an estimated average feature vector as a bias term, so each class is scored by how far its template match deviates from typical ink. The open question is the scale of the features, since I can't pin that down exactly, and I'm setting the logits from there.

I'm setting the bias as the negative of k times each centred template's overlap with the average digit, with k around 3 from a feature scale of about 2 times a readout factor of 1.5. Even if that scale is off, the bias should still remove most of the overlap-driven pull toward class 2. Next I'll check whether digit 4 is also being pulled toward 2.

Thinking about whether the template-matching readout can get much past 60 to 70 percent at this coarse 4x4 resolution, and whether sharper templates would help. The final grid is fixed at 4x4, so finer detail would have to be encoded in the channels instead, for example through conv2 filters at different offsets or stroke-type channels that stay sparse and localized rather than blurring into neighbouring cells.

I'm weighing a centre-only conv2 filter to cut the blur, so each final cell reflects a tighter patch of pooled density and the thin stem of a 1 stops smearing into other cells.

I'm reconsidering the receptive field: with a centre-only conv2 tap, the final cells would cover about 10 pixels instead of 16 to 18, so there's less blur. Still, the 4x4 grid is fixed, and the box average gives smoother features that suit linear template matching, so I'll keep it.

I'm keeping the conv layers as they are and only changing the fc bias, scaling the centred weights down to 1.0 to temper the overconfident wrong predictions. The bias for each class is set to the negative of its centred template's overlap with the mean template, times the assumed feature scale.

Now I'm writing the code that sets the bias to the negative of the scaled overlap between each centred template and the mean template, and I'm planning to note that the class 2 pull comes from a shared offset in the readout.

I'm settling on the fix: subtracting the expected feature vector through the fc bias, since the class 2 pull comes from a shared offset in the readout.
