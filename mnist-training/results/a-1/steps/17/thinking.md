Reverting σ to 1.5 since the last change made things worse; I might try 2.0 later. I'm around 72% and need a bigger structural change, so I'm considering whether conv2 could do more, such as using the full 5x5 kernel as mid-level part detectors combined by the fc layer. I'm also weighing a linear model that makes richer use of negative evidence.

I'm checking whether the linear model could get more out of negative evidence. Pairwise, W_8 - W_3 is just T_8 - T_3, so I can't sharpen 8 against 3 without affecting the other classes. LDA's inverse covariance might help by downweighting high-variance regions like the outer cells, though that isn't obvious yet.

I'm weighing whether 8 orientation channels at 22.5° steps would help distinguish slanted 1s, 2s and 7s, though the cross-talk between 5x5 detectors at that angle makes me doubt it. A cheaper option is 4 orientations sampled on a checkerboard grid, leaving room for other channels like blurred ink or endpoint detectors, since endpoints and junctions look discriminative.

I'm checking which digits have endpoints where, since that could separate 1, 7, 3, 6 and 9 from the rest. A single 5x5 filter can't pick out endpoints in every direction, so I'd need a channel for each: a half-line detector that is positive on one side and negative on the other, responding at the end of a stroke.

I'm listing which digits have endpoints where, since that could separate pairs like 1 and 7 or 3 and 9. Four endpoint channels could cover the directions, with the top-left endpoint of 7 and the left endpoints of 3 as key cases, and 4 standing out for its two top endpoints.

Still working out how the checkerboard sampling would fit the endpoint channels into the 16 conv2 slots...

Still working on the endpoint filter design for conv1, sketching the weights for a top-end detector of a vertical stroke.

Still working on the conv1 endpoint filter, checking the weights for a top-end detector: the vertical stroke's positive response gets offset by the negative rows above, and horizontal strokes only give a weak response.

Still sketching the conv1 endpoint filter: a top-end detector gets its strength from ink below the tip against negative rows above, while a horizontal stroke only lands slightly negative. For corners like the top of a 7, I'm considering a separate tip-right detector, though I still have to work out how it behaves on the stem below.

I'm settling on a single rule for endpoint detectors: a tip pointing in some direction gets a positive weight on its side and a stronger negative weight behind it, with a half-strength falloff for the off-axis columns. Corners will respond weakly no matter what, and I'm fine with that. I also need to check how max pooling after conv1 keeps these endpoint responses intact.

I'm settling the tuning for the endpoint detectors: each tip gets a response of max(0, cos Δ)² against its outward direction, so a diagonal tip only half-activates the neighbouring channels. Closed shapes like ellipses contribute no endpoints at all, and I still need to work out how the junction of an 8 fits into this.

Still working out how the endpoints get declared for each variant: a stroke split into two pieces that meet at a shared point shouldn't count as an endpoint there, so I'll compute them from the polylines and skip any tip that coincides with another piece's tip.

Now I'm working out which endpoints each variant has, so a piece's tip only counts when it doesn't touch another piece, which leaves out the stem of a 9 and the crossbar of a 4.

Next I'm setting the endpoint template values: each endpoint contributes a Gaussian bump scaled by its tip tuning, with a wider sigma since tip positions vary more. The filter gets normalized so an ideal tip lands near 1, which means the bias becomes -0.25. I still need to check how these endpoint channels scale against the orientation channels in the fc layer.

Still settling how the endpoint templates scale against the orientation channels, and I'm restructuring each variant as a list of pieces so endpoints can be computed after the shear and centre transforms.

Still restructuring the variants as lists of pieces, and I'm writing the endpoint code to match.

Still working out the conv2 channel layout: orientation channels take the even and odd taps, and endpoint channels read conv1's tip channels with the same parity split. I'm defining how each filter weights tip direction, with the along-axis and perpendicular offsets setting positive, half, and negative weights.

Still settling the endpoint weights: a tip gets a positive weight on the side behind it and a negative weight past the tip, with the centre row fixing the sign at 1.5 and the outer rows at -0.5. Dividing by 6 normalises an ideal tip near 1, which puts the bias at -0.25.

Still working on the endpoint templates: tip directions get a tuning of max(0, cos)², and the normalization will be taken over the sampled checkerboard cells rather than the full grid.

Still working out the normalization: I'll compute the mean over the checkerboard-masked cells and scale the filter to p=0.5, then check whether the endpoint channels stay neutral on inputs without tips.

Still writing the endpoint helpers: pieces get a closedness flag, and the tip directions get flipped for the start versus end of each polyline.

Checking the endpoint rule on the 4 and the 7: the shared corner at the 4's apex shouldn't count as a tip, but the bottom tip and the right tip at (15,20) should. The 7's crossbar is trickier, since its left and right ends would both register even though the stem cuts through the middle.

I'm checking the middle junction of the 3 now: its cusp points left, so it might need to count as a tip like the outer ends do.

Still working out the feature template: each endpoint's tip direction gets matched against the four detector directions, with a squared cosine tuning, and weak matches get dropped. I'm about to fill the endpoint channels window by window over the checkerboard cells.

Still writing the final assembly: I'm masking the checkerboard cells, zero-meaning each channel and normalising, then mapping the results into the fc weights and conv2 taps.

Still wiring conv1's channels into conv2 and the fc weights, and I'm keeping the biases from the earlier step as they are.
