I'm stuck on the core issue: the hand-built templates are too rough, and feedback is the only signal I have. With 50 steps total, I need a richer representation that makes templates less finicky. One thought is to let the network act more like a direct template matcher at higher resolution, since conv2 could learn spatially specific templates and fc sees all 16 channels across 16 positions. The part I haven't worked out yet is

I'm weighing a different encoding: four-by-four max-pooled ink blocks laid out as sixteen shifted maps, so the fully connected layer sees something close to a coarse binarized image. Stroke width suggests each block would be nearly binary, which could make template matching at roughly seven-by-seven resolution workable.

I'm considering that a linear classifier with hand-set weights tops out around 92% on raw pixels, and class-mean templates around 82%, so reaching roughly 80% with hand templates would be a solid result. Nonlinear orientation features at finer resolution might do better if the weights are chosen well. The feedback only gives me a confusion matrix, so my plan is per-class adjustments over the remaining steps. Right now the errors are 4 being read as 1, 9, or 6, and 8 being read as 1 or 6.

I'm checking the coordinate assumptions, since the 4s are being misread badly. I want to verify the digit box placement and the diagonal line filter normalization, and I'm wondering whether the thin, anti-aliased MNIST strokes are part of the problem.

I'm checking whether thick strokes are breaking the filter: with negative flanks around a 4-5 pixel wide stroke, the response can drop to zero or below, so bold digits lose their oriented features. I'm considering a softer negative weight, around 0.6 of the current one, so solid ink still gives a positive response.

I'm working out whether a perpendicular stroke gives zero response when the flanks are zero-mean, and whether softening the negative flank weight keeps thick strokes positive. Next I'm trying a wider ridge profile, around sigma 1.3, so the side taps hit thick ink less hard.

I'm working out the thick-stroke problem: a five-pixel-wide kernel with zero-mean flanks gives zero response on bold ink, so I'm considering whether a non-zero-mean profile or oriented first-derivative edge detectors would hold up better.

I'm switching to edge detectors instead: eight directional filters at 45° steps, each sensitive to one gradient direction and polarity. Since a stroke produces opposite-polarity edges on its two sides, this should keep thick strokes from cancelling out the way the zero-mean line kernel does, and the polarity may help separate the inside of a loop from the outside.

I'm settling on eight directional edge detectors as conv1 instead of line kernels, since a stroke's two sides give opposite-polarity edges and thick strokes should no longer cancel out. Then, for each stroke point, I'm working out which of those channels should fire on the side facing the stroke center.

I'm weighing a shift in conv1 to eight directional edge detectors, since the two sides of a stroke give opposite-polarity edges that won't cancel on thick ink. For conv2 I'm thinking about how to use the remaining eight channels, perhaps as the same edges sampled on a grid shifted by one pooled cell for finer localization.

I'm settling on the edge-filter kernel now: each direction's weight is the signed projection onto that gradient direction, times a Gaussian falloff across it. I haven't yet checked how that kernel responds to thick strokes.

I'm checking how the edge filter's kernel behaves on thin strokes: a two-pixel stroke sitting at the center cancels out, so the response only shows up when the stroke is offset from the middle.

I'm defining eight directional edge detectors at 45° steps, where each one responds to ink increasing along a single gradient direction. For a stroke point, I'll work out which channels fire on each side of the stroke, since the two edges have opposite polarity.

Next I'm settling on the template scoring: squared cosine weighting so a feature 45° off still counts for half. I'm also dropping endpoint edges at stroke caps. For conv2, the eight edge channels pass straight through with a small blur, and I'm estimating the scale that brings a typical edge response to around 1.5.

Going to write the eight-direction edge kernels with polarity in code next, and I'm keeping the naive Bayes scoring at gamma 0.3 since loss and accuracy look fine there. The digit 4 is still the weak one, so I'm leaving its template as is for now, and the 8 templates should be fine despite the slant.
