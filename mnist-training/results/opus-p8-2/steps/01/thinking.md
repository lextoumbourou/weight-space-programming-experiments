I'm settling on a simple first design: conv1 gets a blur-style channel to detect ink, with the remaining channels acting as oriented edge detectors. conv2 will just pass those features through using a center tap, and the fc layer will act as templates over a 4x4 grid of the resulting features.

I'm checking the receptive field arithmetic: after the two conv and pool stages, each cell in the 4x4 grid maps to input centers near rows 7.5, 11.5, 15.5, and 19.5, which covers the digit area. I'm also weighing a 5x5 conv2 window, which would blur the pooled features for smoother coverage, against a center tap that only picks one pooled cell per position.

I'm sketching the conv1 channels now: one for ink, one each for horizontal, vertical, and both diagonal strokes, with the last few left open for something like background or stroke endpoints.

I'm weighing whether a min-style detector would work better than a max, since max only tells me that ink appears somewhere in a region. I'm leaning toward letting conv2 combine the channels to get around that. A coarse 4x4 grid may cap accuracy around 60-80%, which is fine for a first pass. I'm also considering whether conv2 could carry sub-position information within each cell instead of only increasing coverage.

I'm weighing 16 channels across 16 positions, which gives 256 features, but a center tap only uses half the channels. I could repurpose the spare channels as offset taps for finer spatial detail, though max pooling makes that less clean. Writing hand-made digit templates on the 4x4 grid is the next question.

I'm settling on drawing the digit templates by hand from described strokes, sampling points along each stroke, mapping them into the 4x4 grid, and adding orientation-weighted contributions to the matching channel. That keeps it to analytic template construction rather than running the network on synthetic inputs.

I'm setting conv1 up with a blur channel for ink and four oriented line detectors at 0, 45, 90, and 135 degrees, and I'm weighing what the last three channels should detect, possibly edge polarity like a stroke's bottom edge.

Still settling the conv1 channels: I'm keeping the ink channel and orientation detectors, now weighing six orientations spaced across the half-circle, with the last channel left empty for the moment.

I'm writing the line-detector weights for conv1: a 5x5 kernel per orientation, with a Gaussian profile falling off with perpendicular distance from the stroke center, then made zero-mean so uniform ink gives no response. I'm also keeping a slight negative bias to suppress noise and normalizing each kernel's response.

I'm normalizing each line-detector kernel by the sum of its positive weights so that a stroke along its orientation gives a response near 1. For the ink channel I'm using a uniform 3x3 center average with a slight negative bias, so solid ink reads about 0.9.

I'm thinking about giving conv2's spare channels 8-15 a shifted view: the same conv1 features read from a diagonally offset tap, so each pooled cell carries finer position information rather than a duplicate of the center view.

I'm considering using channels 8-15 for absence-of-ink features, but a linear readout on the ink channel already captures that, so the extra channels would be redundant. I'm leaning toward leaving them as something else rather than duplicating the orientation channels.

I'm leaving channels 8-15 at zero for now, with the option of using them for finer offset views later. I'm also keeping the conv2 bias near zero and giving the orientation filters a slight negative bias around -0.1, so their flank weights don't cancel the response. Next I'm turning to the fc templates, starting with how to lay out each digit's strokes.

I'm working out the fc templates now: each digit's strokes get sampled point by point, mapped onto the 4x4 grid cells whose windows contain them, and weighted by how closely their local orientation matches each channel. Since max pooling keeps only the strongest response per cell, I need to keep that in mind when scaling the template values.

I'm turning the fc weights into a template-matching score: since max pooling gives presence rather than accumulated strength, I'll clip the template values, then use a Gaussian-style comparison, where the logit comes out as 2T·f.

I'm mapping the template score to a logit of 2s·T·f minus a bias based on the template's norm, with the feature scale needing to match the actual conv responses. I'm estimating ink presence near 0.9 and orientation responses around 0.7 times a cosine-squared tuning curve, then considering how the max pooling affects the maxima.

I'm checking the pooling arithmetic: the conv2 center tap pulls in pool cells 2m+2 and 2m+3, which map back to conv1 centers at rows 4m+6 through 4m+9. That makes each pooled cell cover a non-overlapping stride-4 window, so my earlier overlap assumption was off.

I'm weighing whether conv2 can widen coverage by summing over a 2x2 set of taps, which would give windows spanning rows 4m+4 through 4m+11. The catch is that a linear sum doesn't behave like max pooling, so I'm not sure that trade is worth it.

I'm considering using channels 8-15 for a wider view: a 3x3 blurred sum over the conv1 features, which covers more of each cell but needs the template values rescaled to match.

I'm weighing whether to build the wider template views by counting stroke coverage over pooled cells, but that would amount to running the network's feature computation on a synthetic digit. I'd rather keep the template drawing simple and avoid that analytic shortcut.

I'm dropping the idea of wider channels for now and keeping conv2's channels 0-7 on a center tap. For channels 8-15 I'm considering a shifted-grid view, but I haven't settled how to offset the tap without shifting both directions at once.

I'm now looking at whether channels 8-15 should be wide 3x3-summed versions of the orientation features, scaled by a third so a crossing stroke lands near 1 and stays comparable to the template values. The open question is whether the template scale still matches once the wider view is in place.

I'm settling on a logit of s times (2T dot f minus the squared norm of T), with the scale s set to about 0.5 for now. Next I'll define the digit strokes that the templates are built from.

Now I'm writing out the digit stroke definitions as polylines and parametric ellipses, starting with 0 as a full ellipse and 1 as a slanted vertical line, and beginning the arc for 2.

Writing out the stroke coordinates for the digit templates now, working through the 2 and then the 3.

Still writing out the stroke coordinates for the digit templates, now on the 4 and the 5.

Still writing out the digit strokes, now on the 6 and the 7, then the 8, with the 9 next.

Now I'm working out how to lay out the template strokes on the 4x4 grid, marking each cell by whether a stroke passes through its window and how it's oriented.

I'm setting the orientation tuning as max(0, cos(2Δ)), so the response falls off to zero at 90° and stays near 0.6 at 30°. I'm treating the cell's presence value as the best product of the vertical membership weight, the horizontal membership weight, and that tuning across all sample points.

I'm sizing the wide channels' template values so a stroke spanning the wider window lands near the tight-channel values, using a sum over three of the nine pooled cells scaled by a third.

I'm working out how to size the wide-channel templates, weighing whether to scale them by coverage of the 8-pixel window or just use the presence value, and leaning toward keeping them simple.

I'm working out the wide-channel template values now: a straight stroke crossing a 3x3 pooled window should come out near the tight-channel value, so the template is the stroke length inside the window divided by 6, scaled by the orientation tuning. I'm leaving out the max over orientations for these channels.

I'm settling the activation values: ink and orientation channels get a small negative bias to suppress faint responses, and I'm picking template values of about 0.75 for ink and 0.55 for orientation, since the max over a region should land near the peak. I'm also weighing the logit scale against the bias term, which penalizes templates with more ink.

Still writing the stroke-sampling helpers in the Python code, with the line and arc functions built first.

Still writing the stroke-sampling helpers, now the arc and quadratic curve functions.

Still writing the template accumulation loop, now computing the tight and wide window weights for each stroke point and vectorizing the per-cell updates.

Still working through the template construction: the tight and wide window weights are combined per stroke, and I'm taking a max across strokes for the tight channels and a sum for the wide ones. I'm also zeroing the unused conv1 channel and then assembling the final fc weights from the scaled templates.

Still working out the orientation filters: I'm setting the 5x5 Gaussian-derived weights so the central line response sits near 0.36 on average, with the flanks at distance one contributing about 0.46 each.

I'm checking the orientation filter's flanks: the center pixel carries most of the positive weight, the neighbors at distance one add a little, and a thick stroke ends up normalized to about 1. I'm settling the logit scale at 0.5 and moving on to writing the code.
