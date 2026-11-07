Good progress from 11.3% to 31.2%! The zero-mean centering helped a lot. Now let me analyze the confusion matrix:

Main issues:
1. **Class 1 is predicted too often** - many digits are misclassified as 1 (37+385+611+486+409+348+426+584+556 = 3842 false positives for class 1!)
2. **Class 7 is predicted too often** - many digits go to 7 (164+204+115+237+45+80+12+312+348+150 = 1667 false positives)
Some classes are holding up: 0, 1, 4 and 6 get a reasonable share right. Classes 3, 8 and 9 are very poor, with almost none recognized. Now I want to see why class 1 gets over-predicted, so I'm checking the template for class 1, which has rows of [-1, 0, 1, -1] patterns.

The template for class 1 puts its positive weights in column 2, which is the center-right of the image, and most digits have ink there. So class 1 picks up a high logit almost everywhere, which would explain why it wins so many predictions. The vertical-stroke template for class 1 might add to that. Next I want to check the template for class 7.

Next I'm checking the class 7 template, which has a different weight layout, and I'm centering it the same way so it can be compared against the others.

I'm thinking about how the features are overweighted for class 7 too, since its template has strong positive weights in the upper-right. My main problem is that the ink-density channel gives similar coarse patterns for many digits, so I need more discriminative features. Now I'm weighing whether to use more channels in the FC layer, find templates unique to each digit, or rescale the features, and I'm starting to list what distinguishes each digit, beginning with the hole in digit 0.

I'm listing what separates each digit from the others: digit 0 has a central hole, 1 has very little ink with only vertical edges, and 2 has a flat bottom edge with no holes. Digit 3 is open on the left, 4 has a crossing of horizontal and vertical strokes, and 5 has a flat top. Digits 6, 7, 8 and 9 each have their own marks too, like a bottom hole for 6, a flat top bar for 7, two holes for 8, and a top hole for 9.

I'm now thinking about the class-by-class features: holes, flat top or bottom edges, and how much ink each digit has. The main issue is still class 1 being over-predicted, and its template's positive weight in column 2 looks like the cause.

I'm thinking about what makes digit 1 unique, since its template fires on almost every digit. Digit 1 should have ink in only one narrow column, with the rest of the grid near zero, so the template ought to penalize ink in the outer columns and reward a single narrow stripe.

I'm reconsidering class 1's template: my suspicion is that the bigger weights on the middle columns are what's pulling in digits like 5, which have a lot of ink in that same area. Adding more negative weight to the outer columns should help the template separate a thin stroke from the broader shapes.

I'm working through the scoring for class 1 on a sample of a 5-like pattern. Row by row, the template's positive and negative weights roughly cancel, so the logit comes out near zero in the first row and goes negative in the next two.

I'm working out the centered template for class 5 by subtracting the mean of 0.25 from each cell, which gives the first row a mix of slightly negative and positive values.

Working through the class 5 template by centering it, I'm computing its response on the 5-like pattern row by row, and the first row comes out strongly positive.

I'm checking the class 5 scoring against class 1 on this sample, and class 5 comes out at about 2.14 versus about -0.3 for class 1, so class 5 wins here. But the confusion matrix still shows 409 digit 5s predicted as 1, which doesn't fit with this one example.

I'm checking whether the hole channel for class 1 contributes to the misclassification, since its template is centered to a mostly positive pattern with negative weights in the middle.

I'm checking the hole and vertical-stroke templates for class 1, and they only add small terms to the logit, since the ink channel is still the main signal. Those extra channels don't seem big enough to explain why so many digits get predicted as 1, so I want to recheck whether the ink-density estimates I used for digit 5 were right.

I'm wondering whether the real problem is in the feature extraction rather than the templates: with 16×16 receptive fields, neighboring grid cells overlap heavily, so the gap between column 1 and column 2 is small and template matching has little to separate. I'm weighing three fixes: make conv weights more spatially localized, add channels to the FC layer, or add templates for the most-confused pairs. Making the conv2 kernel more peaked, closer to a delta, looks like the most direct way to get more spatially precise features.

I'm going to add edge-direction channels to the template so that digit 1, with its mostly vertical edges, separates from digit 7's top bar and digit 0's edges in every direction. I'll also add discriminators for the confused pairs, like total ink for 1 and the central ink for 8 versus 0.

I'm going through the next set of features to separate the confused pairs. For digit 1, I'd look at low horizontal edges and strong vertical edges in the center; for 7, the diagonal channels; for 8 versus 0, central ink and more evenly spread holes; and for 3 versus 1, the right-side and horizontal edges. I'll also revisit the ink-density templates and push them harder.

I'm listing the confused pairs from the confusion matrix: digits 2 through 8 are each being predicted as 1 in hundreds of cases, with 3 going to 1 the most (611 times) and 2 the least (385 times).

I'm now checking how the class 1 and class 7 templates overlap on the digits they keep catching. Both put negative weight on the left column, which should help, but their positive weights on the middle-right columns are matching far too many digits, and the ink-density templates still don't separate them well enough.

I'm weighing a few ways to fix the class 1 over-prediction, and I think the most direct one is to stop leaning so heavily on ink density. I'll add more discriminative channels to the templates (edges in each direction, holes, and the spatial pattern of ink) so that digits like 1 and 7 stop matching so many of the others.

I'm laying out the top-edge channel for each digit, noting where the flat top bar falls for 5 and 7 and where the curve starts for 2 and 3.

I'm going through the edge channels for each digit now, noting where the top bar, bottom bar, and stroke endings fall, with digit 7's bottom edge being the part I'm still tracing.

I'm now going through the left and right edge channels for each digit, noting where the ink boundaries fall for 0, 1, 4, and 6, and where the right edges sit for 1 and 3.

I'm adding the edge channels to the templates and listing which digits show a horizontal bar or a vertical stroke, so I can tell which features separate the confused pairs. Next I plan to expand the FC templates to use more channels and make them more discriminative, and I'm starting to look at why class 1 is over-predicted.

I'm checking the class 1 template against digit 8: it puts positive weight on column 2 and negative weight on columns 0 and 3, so any digit with more ink in column 2 than at the edges will get a positive logit for 1. I want to see whether digit 8's ink, which runs across all positions, is strong enough to outweigh that.

I'm checking the class 8 template's centered values against digit 8's ink to see whether the weight at those positions gives it a logit high enough to beat class 1.

I'm checking whether a uniform ink value gives zero logit, since the centered templates sum to zero. That means any signal has to come from the spatial pattern, so I'm looking at how the corner and edge densities for digit 8 differ from the center.

I'm checking the template-1 logit for digit 8 by weighting each position's ink density against the template's column pattern, and the sum comes out negative, so this template doesn't pull digit 8 toward class 1.

I'm checking the template-8 logit for digit 8 row by row, with the centered weights applied to its ink density, and the first row comes out to about 0.875.

Now I'm checking the class 1 vertical stroke template on digit 8, since the logits so far suggest class 1 shouldn't win, which means the vertical stroke channel might be what's pushing it up.

Now I'm checking the vertical stroke template for class 1 against digit 8's edge pattern, weighting each position's response to see how much it pushes the logit toward 1.

Next I'm checking the hole template for class 1, which centers its values around a negative mean, so the uniform parts of the grid sit well above the central cells.

I'm checking the class 1 hole template on digit 8, where the center cells carry most of the ink, and working through the weighted sum to see whether it pushes the logit toward 1.

The hole template for class 1 comes out to about -0.375 on digit 8, since its center cells carry the most ink. That pushes class 1's logit down, which helps keep digit 8 from being mistaken for 1.

Now I'm working out the digit 8 logits: class 1 comes out around -0.975 once the ink and hole terms are summed, while the class 8 ink term alone gives about 1.05.

Now I'm working out the class 8 logit for digit 8: the hole template adds about 0.21, bringing it to roughly 1.26. Against class 1's roughly -0.975, that's a gap of about 2.2 in class 8's favor.

I'm checking whether the conv1 ink detector, with its small bias, is producing values weak enough that the spatial contrast in the templates gets washed out.

I'm working out what the conv1 ink detector outputs for background versus ink pixels, and that ink values land around 0.5 to 0.8 after the bias while background gets killed by ReLU. After max pooling they stay in the 0.6 to 0.9 range, so now I'm estimating what conv2's pass-through channel gives over a 3x3 window.

I'm checking whether the spatial contrast between grid positions is weaker than I assumed, since neighboring receptive fields overlap heavily and that could flatten the differences the templates rely on.

I'm checking whether the spatial contrast between grid positions is too weak for the templates to separate the digits. The center values come out high because the receptive fields overlap with nearby ink, which means I may need a more peaked conv2 kernel or contrast-creating negative weights to keep the spatial information.

I'm weighing whether conv2 should use negative weights to build local contrast, so the grid positions stop blurring together. The max pooling already averages things out, so I'll keep the spatial detail in the conv kernel itself.

I'm writing a local contrast kernel for channel 0, where the center weight is positive and the surrounding ring is negative, so strokes get a positive response and holes a negative one. After ReLU that keeps only the stroke-side signal, which changes what channel 0 means compared to the plain ink density I had before.

I'm weighing whether to penalize class 1 through the FC bias, since its template matches too many inputs. I could also tighten class 1's template or make the other class templates more competitive.

I'm moving from the class 1 bias fix to a different approach: using edge features (top, bottom, left, right boundaries) instead of ink density, since edges should capture digit shape better. I'm starting to describe what the edge templates look like for digit 0, beginning with its top edge.

I'm sketching edge templates for each digit now: digit 0 gets a top, bottom, left and right boundary in specific rows and columns, and digit 1 gets a thin vertical stroke along column 2. The idea is that edge channels capture the contour of each digit better than plain ink density. I'll keep the ink and hole templates too, and add edge templates for all ten digits on channels 1 through 4.

Next I'm adjusting the FC biases directly: pulling class 1 down by about 1.0 and class 7 down by 0.5, since they're over-predicted, and nudging class 8 up by 0.5 because it's badly under-predicted.

I'm estimating what the class 1 total would be across the templates, and the centering should make each template sum to zero. That suggests the over-prediction isn't coming from a simple sum offset, so the real cause may be in how the templates were centered before the shift.

I'm weighing whether to build 160 separate 4x4 templates, one per conv2 channel for each digit, since the ink-density templates alone don't separate the digits well enough.

Now I'm deciding to define edge-based templates for the most useful channels, covering ink density, the four edges, the hole detector, and the stroke channels, which comes to 80 templates across the ten digits.

I'm working through the edge channels now: a top-edge detector should fire at the top of a stroke, so for a circle that's row 0, and for a vertical line only at the very top. Checking the bottom-edge channel next, I'm reasoning that it's just the negated top-edge filter, so it fires where ink sits below background.

Checking how the top-edge filter responds: rows of ink above and background below give a positive output, and the reverse gives a negative one.

I'm checking the filter-1 sign convention: it responds positively where ink is above and background below, so it picks up the top edge of a stroke. The bottom-edge filter is just its negation, and the left and right edge filters are the transposed versions, one for each side of a stroke.

Now I'm checking the left-edge filter: it's the transposed top-edge pattern, with positive weights on the left columns and negative on the right. Ink on the left with background on the right gives a positive response, so it picks out the left side of a stroke. The right-edge filter is its negation, firing where ink sits to the right of background.

I'm checking the filter-4 sign convention: it's the negation of the left-edge filter, so it fires where ink sits to the right of background. That makes it the right-side edge detector, picking up where a stroke's right boundary is.

I'm checking the left-edge filter at column 12, where the first weight multiplies background and the sign of the response depends on which side of the stroke the ink sits.

Checking the left-edge filter at columns 10 and 12, I'm finding that the stroke at x=14 produces no response there because the window only sees background, so the result stays near zero.

Checking the filter at column 14: its first weight multiplies the stroke, so the response there is positive and the edge fires. I'm tracing the window position by position to see exactly where the response changes sign.

I'm checking whether filter 3 fires at column 14, where the stroke sits on the left of the window and background on the right. That would make it respond to the right edge of the ink rather than the left, which is the opposite of what I expected from its sign pattern.

I'm checking the sign of filter 3 at the stroke's right side, where ink sits to the left of the window and background to the right, and it turns out this fires on the right boundary, the reverse of my first labels. So I'm flipping the labels: filter 3 marks the right boundary of ink and filter 4 marks the left boundary, and I'm about to recheck filter 1's orientation the same way.

Checking the bottom-edge filter now: it should respond where ink sits above background, and the row-by-row weights confirm that at the bottom of a stroke the top rows give a positive result while the rows below contribute nothing.

I'm checking the bottom-edge filter's rows against the ink-to-background transition, and it does fire at the bottom boundary of the stroke, not the top. So the label I gave filter 1 is backwards, and I need to swap it to "bottom edge."

I'm sorting out which boundary each filter responds to, and the positive-weight side has to line up with ink for the output to be large. Filter 1 therefore fires at the bottom of a stroke and filter 2 at the top, while filter 3 marks the right side and filter 4 the left, which reverses the labels I had. That leaves me checking how the top of a rounded shape like the oval of a 0 lines up with filter 2.

I'm settling the labels for the four edge filters: filter 1 marks the lower boundary of ink, filter 2 the upper, filter 3 the right side, and filter 4 the left. Working through digit 0, its oval's bottom edge is where filter 1 fires, and its left and right sides are where filters 4 and 3 respond.

Now I'm applying the boundary labels to digits 0 and 7: the lower-boundary filter catches the bottom of the oval and the bottom of the top bar, the upper-boundary filter catches the top of each, and the right and left filters pick up the sides.

I'm settling on the labels for the edge filters: filter 2 is the one for a top boundary of ink, filter 1 for a bottom boundary, filter 4 for a left boundary, and filter 3 for a right boundary. I'm going to use those in the FC templates from here.

I'm rechecking the top bar of the 7 in the 28x28 grid, placing it around rows 4 to 8, to confirm where its lower edge falls.

Checking the bottom edge of the top bar, I see it falls near row 8, which is where grid row 0 is centered, so filter 1 should capture it there.

I'm settling the edge-filter labels: filter 1 marks the lower boundary of ink and fires at the bottom of the top bar of the 7, which lands in grid row 0. I'll stop fussing over the exact labels and move on to step 3, adding edge templates, sharpening the ink templates, and adjusting the FC biases. The biggest problem is class 1 being over-predicted, so I'm starting a negative bias for that class.

Reassigning the bias terms now: class 1 gets a stronger negative bias, class 7 a milder one, and class 8 a positive push, since it's badly under-predicted.

Next I'm tallying how often each class is predicted against how often it's correct, and classes 2, 3, 8 and 9 look under-predicted.

I'm tallying the confusion matrix column by column to see how often each digit gets predicted, since the row-based counts I used earlier may have been off. Class 1 is clearly the heaviest over-predicted class, and I want the per-column totals before I set the bias terms.

Now I'm tallying the column sums of the confusion matrix to see how often each digit gets predicted, with column 1 coming out as the heaviest.

Now I'm tallying the column totals and noticing class 1 is by far the most over-predicted, with 4701 predictions against roughly 1135 true cases. Class 7 and class 8 show a similar imbalance, with 8 badly under-predicted, so I'm planning bias corrections to pull these counts back toward their true frequencies.

Next I'm working through the per-class ratios of predicted to true counts: class 1 sits far above the others at about 4.1 times its true frequency, while classes 2, 3 and 5 fall well below theirs, and I'm still checking where class 7 lands.

Now I'm applying the bias correction to the classes that are off. Class 1 is predicted about four times its true frequency, so it gets the largest negative adjustment, around -1.4. Class 7 is over-predicted too, but only by a factor of about 1.6, so its adjustment is smaller at -0.5. Class 8 is badly under-predicted, at roughly a fifth of its true count, so it needs a positive push of about +1.5, and class 2 also needs an upward adjustment.

Now I'm settling the bias values: class 1 gets a firm negative push, class 7 a smaller one, and the under-predicted classes 2, 3, 5 and 8 get positive nudges, trimmed a bit so I don't overcorrect.

I'm realizing the bias adjustments only patch the symptom, since the real problem is that the class 1 and class 7 templates match too many inputs. So I plan to revise the templates along with the biases. For step 3 I'll add stronger bias corrections, more channel templates for discrimination, and denser ink templates.

Next I'm laying out the channel plan for the FC templates: channel 0 for ink density, channels 1 to 6 for the edge features, and channel 7 as a hole detector. I'll keep the conv layers as they are and concentrate the changes on the FC layer, which has room to improve. Then I'll define templates for each digit across the useful channels.

I'm giving the digit 0 its edge profile: strong response on the top and bottom of the oval, with the right and left sides picked up by the other two boundary filters.

Now I'm working out the edge pattern for digit 1: a thin vertical stroke gives small bottom and top boundary responses near the stroke ends, while the left and right boundary filters both fire along its length.

Now I'm writing the digit 1 right-boundary and left-boundary templates, both peaking at the center column, since a thin vertical stroke makes the two sides nearly overlap. That overlap is a useful contrast with digit 0, whose right and left boundaries land in different grid positions.

Now I'm laying out the spatial templates for digits 0 and 1 on the right and left boundary channels. A thin vertical stroke puts both boundaries at the center column, while the zero's sides sit at opposite edges of the grid, so that difference should separate the two digits.

Now I'm setting digit 7's edge templates: the bottom-boundary and top-boundary filters both fire along the top bar, with a smaller response near the bottom of the diagonal.

Now I'm reasoning that the top bar of the 7 spans rows 4 to 8, so both its top and bottom edges fall inside grid row 0's receptive field, which means channels 1 and 2 would both fire there.

Now I'm laying out the horizontal stroke channel for the FC templates, which combines top and bottom boundaries. Digit 7 and digit 5 both show strong responses at the top bar in row 0, digit 2 at the bottom bar in row 3, and digit 4 at the crossbar in row 2, so that channel should help tell them apart.

Still writing the weight builder...

Still writing the weight builder...

Still writing the conv1 kernels...

Still writing the conv2 kernels...

Still writing conv2 kernels...

Still writing the bias corrections...

Still writing the weight builder...

Still writing the weight builder...

Still writing the bias and template table...

Still writing the template table...

Still writing the digit templates...

Still writing the bottom-boundary templates...

Still writing the FC template table...

Still writing the bias and template table...

Still writing the horizontal stroke templates...

Still writing the digit 4 and 9 vertical-stroke templates...

Still writing the bias and template table...

Now I'm checking whether the horizontal stroke channel really combines the top and bottom boundary channels. Channel 8 draws on both, so it should fire only where both edges are present, which fits a horizontal bar. The top bar of the 7 and the bottom bar of the 2 both land where I expect, so the templates look right.

Now I'm comparing the digit 3 and digit 5 ink templates, since they look quite similar in the grid.

Now I'm centering the digit 3 and digit 5 ink templates to compare them, and digit 3 comes out with a mean of about 0.19 while digit 5 sits near 0.25.

Now I'm comparing the centered digit 3 and digit 5 templates cell by cell. They overlap in the top row, but digit 5 has an extra positive response on the right, and in the middle rows the signs flip, so the two patterns should be separable.

Still writing the conv2 sharpening...

Still writing the conv2 kernels...

Trying a sharper conv2 kernel now, with just the center pixel, to see whether it keeps more spatial contrast for the pass-through channels.

Now I'm weighing a sharper conv2 kernel that takes only the center pixel, since the smooth 3x3 averaging may be washing out the spatial contrast I need.

Comparing a sharp kernel to the smooth one for step 3: the sharp kernel keeps more spatial contrast for the 4x4 grid, though it may pick up more noise.

Adding FC biases and more edge templates next, with the conv layers left as they are. I'll see how much the biases help before deciding whether to touch the conv layers.

I'm working out which boundary channel fires for digit 7's top bar: the filter that responds to the lower edge of ink, and the one for the upper edge, both land within grid row 0's receptive field, so both channels should respond there.

Now I'm checking how digit 7's diagonal stroke fits the filter layout, and whether a diagonal channel is needed to pick it out.

Now I'm checking the diagonal filters: filter 5 fires on \ stroke borders, and for digit 7's / diagonal I'd expect the mirrored filter 6 to be the one that responds.

Still writing the digit 7 diagonal template...

Now I'm checking which diagonal this 7 stroke actually matches, since the descending stroke runs from the top-right of the bar toward the lower left, which points to the backslash-oriented filter rather than the slash one.

Now I'm working out which diagonal filter matches the 7's stroke, since its edges are along a "/" direction but the stroke runs top-right to bottom-left.

Still working out the diagonal channels: channel 14 for the backslash stroke and channel 15 for the slash, with digit 7 expected to light up on 15.

Still working out the diagonal templates for channels 14 and 15, with digit 7 on the slash channel and the no-diagonal negatives for digit 1.

Now I'm settling on the FC biases, with a small correction for class 1 and a lighter one for class 7 so the templates keep doing most of the work.

Still writing the negative penalty templates...

Now I'm checking the horizontal stroke channel against digit 1, since the penalty template depends on where that channel fires. Channel 8 only responds where top and bottom edges co-occur, so for digit 5's top bar it should light up across the first row, while for digit 1 it should stay mostly quiet.

Now I'm checking the horizontal-stroke penalty on digit 1: a centered template that's negative in the middle columns should push its logit down wherever digit 5's top bar lights up channel 8.

I'm adding a negative template on the horizontal-stroke channel for digit 7's lower-left region, to penalize left-edge features there. I'll keep its strength small so it nudges the decision without overpowering the other templates.

Now I'm settling the class-rebalancing plan for step 3: FC biases, the same ink and hole templates as step 2, a few key edge templates, and negative templates aimed at the common confusions, with the conv layers unchanged. Looking at the step 2 confusion pairs, most of the errors send true 3, 8, 9, 4, 7 and 5 digits into class 1.

I'm looking at the next few confusions, which are mostly 3, 8, 9, 4, 7, 5 and 2 being predicted as 1 or 7. Once those two classes are pushed down, the remaining mix-ups should be between similar shapes like 3 and 8, 5 and 6, 4 and 9, and 2 and 3.

Still writing the weight-building code for step 3...

Still writing the conv1 weight setup...

Still writing the conv1 weight setup...

Still writing the conv2 weights...

Still writing the conv2 weights...

Still writing the bias corrections for the FC layer...

Still writing the FC weight setup...

Still writing the digit 5 template in channel 5...

Still writing the digit 9 template in channel 9...

Still writing the digit 9 holes template...

Still writing the horizontal stroke templates...

Still writing the vertical stroke templates...

Still writing the template penalties and boundary edges...

Still writing the boundary and hole penalties for digit 0...

Still writing the diagonal templates and wrapping up the weight dictionary...

Now I'm questioning whether my channel 14 reasoning holds: the \ diagonal filter fires on edges running in that direction, and I can't yet tell if digit 2's middle stroke actually lines up with it.

Simplifying step 3 now: I'm dropping the diagonal templates and sticking with the bias corrections and key edge templates, starting with a 5x5 Gaussian kernel for the first conv filter.

Still writing the conv1 weights...

Still writing the conv2 weights...

Still writing the conv2 weights...

Still writing conv2 weights...

Still writing the FC bias setup and the index helper...

Still writing the weight setup for step 3...

Still writing the filter weights for the remaining channels...

Still writing the holes template for digit 0...

Still writing the digit 7 and digit 2 penalty templates...

Still writing the horizontal stroke templates...

Still writing the horizontal and vertical stroke penalty templates...

Still writing the return dictionary for the weights...

Now I'm adjusting the FC biases, since class 1 gets the most false positives and should be pulled down, while 3, 5 and 8 need a lift.

Now I'm checking which edge each filter picks up: the channel that's positive on the left fires at the right edge of the ink, and the one positive on the right fires at the left edge. For digit 3's arcs on the right, that means the right-side edges land on channel 3 and the left-side edges on channel 4.

Now I'm working out the centered template for digit 3's right-edge channel, where the 1s sit on the right side of the arcs.

Still writing the digit 3 right-edge template...

Still writing the digit 0 edge templates...

Now I'm working through the column counts from the confusion matrix, since class 1 is over-predicted about 4.7 times and classes 2 and 3 are under-predicted, so the FC biases need a bigger correction.

Still writing the FC bias values...

I'm settling the FC bias values now, since the computed corrections from the predicted counts come out larger than I'd like. The exact shift depends on the softmax, so I'm treating the logit change as roughly proportional to how far each class's prediction rate is off. Class 1 is over-predicted about 4.7 times, so it needs the biggest cut, and I'm keeping the adjustments a bit conservative.

I'm settling the FC biases now: class 1 gets the biggest cut since it's over-predicted, and the under-predicted classes 2, 3, and 8 get a lift. Given the logit spread I expect from earlier, a correction around 1 should matter a lot, so I'm keeping the values moderate.

I'm considering a sharper conv2 kernel: a delta function at the center instead of the smoothing Gaussian, so the spatial detail survives onto the 4x4 grid.

Now I'm weighing whether a delta kernel in conv2 is worth it: each output would see just one maxpool pixel, so the combination channels would react only at a single spot instead of across a 3x3 patch. That's less robust, though the pass-through channels lose nothing since maxpool already smooths.

I'm weighing a plus-shaped kernel, with the most weight on the center and small weights on the four neighbors, as a middle ground between the current Gaussian and a pure delta. I could also use the delta just for the pass-through channels and keep the Gaussian for the combination channels, so the pass-through features keep their spatial precision while the combinations still average over neighbors.

Now I'm weighing whether a sharper kernel would help the horizontal strokes too: the top and bottom boundaries sit only a couple of pixels apart, so at the 12x12 resolution they usually land in the same or neighboring blocks. I'm settling on a plus-shaped kernel with the most weight at the center for step 3.

Still writing the weighting for the sharper kernel...

Still working out the sharper conv2 kernel and how its scaling compares with the old Gaussian for the pass-through channels.

I'm weighing whether to scale the sharper kernel down: its center weight is about twice the old one's, so the features would come out roughly twice as large. Since the output is a weighted average, the new kernel mostly sharpens spatial differences rather than changing overall magnitude, which is the part I care about for discrimination.

Now I'm weighing whether to keep the Gaussian kernel for step 3 or switch to a sharper one, and I'm leaning toward keeping it unchanged so I can tell whether any gain comes from the FC bias and template changes alone.

Still writing the first conv1 filter weights...

Still writing the conv1 edge filter weights...

Still writing the second convolution weights...

Still writing the second conv layer's kernel weights...

Still writing the FC layer weights...

Still writing the digit 0 template weights...

Still writing the digit 0 edge templates...

Still writing the digit 9 template...

Still writing the digit 7 hole template...

Still writing the horizontal stroke templates for channel 8...

Still writing the vertical stroke template for channel 9...

Still writing the upper boundary templates...

Still writing the left-edge boundary template...

Now I'm double-checking the edge filter by writing out its transposed version, the one with the rows running 2 1 0 -1 -2.

Still checking the edge filters: the right boundary of ink lands on channel 3, and the left boundary on channel 4.

Still writing the digit 3 right-edge template...

Checking the digit 6 left-edge template and confirming it fires on the bottom loop's left side. Now I'm adding a digit 8 template to separate it from 0, since 8 has ink in the center waist while 0 stays empty there.

Next I'm checking whether digit 8 needs a horizontal stroke template at the waist, which would be rows 0 and 2 on channel 8. I'm doubting that: the waist of an 8 is more of a crossing point than a clear horizontal line, so that template may not hold up.

Still writing the digit 8 waist template...

Still working out the digit 7 and filter-direction templates for step 3.

Checking the top bar of the 7 now: its top edge sits around row 4, which still lands in grid row 0. Both the bottom-edge and top-edge filters respond there, and their sum is what the horizontal stroke channel picks up. Both the bottom-edge and horizontal-stroke templates for the 7 look right.

Still writing the hole templates for the digits that have none.

Adding a few hole templates for digits 4 and 5 to penalize the hole detector where it should not fire. The main change is still the FC bias adjustment, and these extra templates are secondary.
