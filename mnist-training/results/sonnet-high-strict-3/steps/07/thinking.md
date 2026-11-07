I'm still circling because the hand-built rules lack discriminative power, so I'm weighing a more principled redesign. With nine steps left, I'm considering a network that does coarse template matching, with conv2 channels acting as shifted ink-blob detectors over a finer grid.

I'm weighing whether to drop the hand rules and use orientation-specific features instead, with each class template built from strokes I describe in 28x28 coordinates. The class weights would then come from the stroke geometry itself, with the logit as a dot product against the features and the class means subtracted to sharpen discrimination.

I'm sketching a feature scheme where each class template is drawn as polyline strokes in pixel coordinates, with the weights for four orientation channels and an ink channel computed from stroke geometry rather than data. The conv2 masks should be a tighter 3x3 center window, so each cell covers about 10 pixels instead of overlapping heavily with its neighbors.

I'm picking the 3x3 center mask for conv2 so each cell's window is about 12 pixels, with stride 4 between cells. I'm also considering how to fill the remaining channels: orientation features, an ink blob, and possibly duplicated orientation channels, given conv1 only has eight filters to work with.

I'm settling on conv1 channels 0 through 3 as the four orientations and channel 4 as the ink blob, leaving 5 through 7 at zero since they wouldn't add anything to the templates. I'll start filling in conv2's channels from there.

Next I'm setting the bias values: zero for the ink channel and a small negative bias for the orientation channels. Then I'll move on to the stroke drawings for each digit in 28x28 coordinates.

I'm now drafting the stroke polylines for each digit in 28x28 coordinates, starting with the 0 as an ellipse and moving on to the 1 and 2.

Still writing the stroke polylines, now for digits 3 through 5 in the same 28x28 coordinates.

Still writing the stroke polylines, now for digits 6 through 8.

Still writing the stroke polylines, now for digits 9 and the sampling step.

Still working out the conv2 window: the center 3x3 mask over pooled rows, which should put each window about 12 pixels across.

I'm estimating how far each feature's window spreads: about ±5 pixels, or roughly ±7 once max-pooling is included, so I'll use a Gaussian with σ=4 to assign templates to cells.

I'm weighing a normalization for the template weights, since classes with more ink like 8 and 0 would otherwise dominate, and I'm considering subtracting a term proportional to each template's squared norm.

I'm settling on a centered-template score: subtract each class's mean template so the weights sum to zero, then pick a per-class bias that offsets how much ink each template carries. That keeps heavy-ink digits like 8 and 0 from winning by default, and I'll set the bias from the template norms.

I'm working out the scale factor α, estimating the activation per unit of template density, so the logit can be written as γ times the centered template dot product minus half the template norm.

I'm estimating the activation per unit of template density, using an assumed ink-blob response of about half over a window, and I'll tune a scale factor against the bias until the logits look balanced.

I'm settling on centered templates and an α around 0.4 to set the bias, since the norm term has to scale with the features.

I'm now weighing whether to center the class templates by subtracting their mean, so the matched filter isn't dominated by the shared ink in the middle, and I'm considering how to adjust the bias to match.

I'm noting that the centering step cancels out, since subtracting the shared mean leaves every class's logit shifted by the same amount for a given input. That means the only real unknowns are the scale α and how to balance the ink channel against the orientation channels. I'll set the overall logit scale γ to 1.0 for now and check the loss to see whether the class gaps are big enough.

I'm estimating the activation scale α from the ink blob response, assuming a stroke covers roughly 40% of each pooled window, which puts the feature value around 0.5.

I'm working out the activation scale now: the ink channel comes to about 2 × 0.35 ≈ 0.7 per window, so α ≈ 0.7 for cells sitting on a stroke. The orientation channels look similar, around 0.5, so I'll settle on α ≈ 0.6 overall and set each class bias to -0.5·α·‖T_c‖².

I'm dropping the uncentered-versus-centered question here: subtracting a shared class mean only shifts every logit by the same amount per input, so it changes nothing. I'll use an orientation response of cos² and write the stroke sampling code next.

Still writing the stroke sampling and the fc weight layout: each cell's template gets filled in channels 0 through 4, and the bias is set from the squared template norm.

I'm settling on a weight of 1.0 for both the ink and orientation channels, and an α around 0.5 since the features come out a bit weaker than I estimated. Next I'll write the code, starting with the Gaussian helper.
