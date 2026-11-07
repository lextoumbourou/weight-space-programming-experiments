Let me analyze step 5 results. Accuracy improved slightly from 40.7% to 41.5%. Loss went down from 1.72 to 1.68.

Predicted column sums:
Col 0: 703+0+16+0+6+31+43+15+5+54 = 873
Col 1: 2+837+35+76+40+32+14+68+132+35 = 1271
Col 2: 12+7+375+18+1+9+10+1+42+0 = 475
Col 3: 19+3+298+347+2+29+4+104+49+10 = 865
Still summing the columns...

I'm checking the per-class figures against the column totals now. Class 9 and class 6 are over-predicted, and class 8 is still far above its target of about 1000. Class 2 and classes 4 and 7 are under, and class 1 remains high, though its per-class accuracy of 78.7% is the best so far.

I'm going through the per-class accuracy numbers now. Class 7 is the weakest at 11.9%, and class 9 is barely better at 8.4%. The biggest confusion is true 7 being predicted as 9, with 668 cases.

I'm working through the per-class confusions now, and the biggest ones are true 4 predicted as 8, true 3 as 9, and true 2 as 3. The pattern looks like biases swinging back and forth between classes 8 and 9 from step to step. I suspect the 4x4 templates just can't separate the classes well enough, so I'm considering dropping the bias terms entirely and trying a different approach.

I'm thinking about how to make conv2 produce more useful features, since only part of its 16 channels actually feeds the FC layer. The core issue is that at 4x4 resolution many digits look alike, so the ink, edge and hole patterns don't separate them well. I'm considering digit-specific detectors, such as a horizontal bar detector, a vertical line detector and a curve detector.

I'm weighing whether to drop the bias terms and rely on the templates alone, or to widen the FC layer so every digit uses all 16 conv2 channels. Defining templates for all 160 digit-channel pairs is a lot of work, so I'm considering adding them only for channels 10–15 on the most confused pairs.

I'm still stuck on the roughly 40% accuracy, which suggests hand-designed templates over coarse spatial features have limited capacity. I'm considering a different approach: designing conv2 filters to respond directly to digit components, such as horizontal bars, vertical strokes, and top and bottom loops, each tied to the digits it would help separate.

Still thinking about conv2 filter design, weighing component detectors for the digit shapes. Now I'm working through the confusion pairs, where 7 is mostly mistaken for 9, 9 for 8, and 4 for 8, to see whether a difference-based feature could separate them better than the individual edge features.

I'm checking why 9 and 4 would match class 8's template, since the +0.65 bias alone seems to explain only part of it. Class 8's template is positive nearly everywhere, so the centered pattern rewards any digit with ink spread across the grid.

I'm reconsidering the bias on class 8, since its template adds a moderate positive logit to any digit with ink spread across the grid. The biases should roughly offset the average template match per class, and because the templates are zero-mean, they should end up close to zero if the templates are well designed.

I'm weighing whether the class biases are systematic, since some templates may just match better on average. I'll try normalizing each class's template to the same L2 norm so the base logit levels line up, and test that at step 6. A simpler option is to zero the biases and add a small correction from the diagonal versus off-diagonal balance in the last confusion matrix.

I'm weighing whether to zero the biases to see how the templates perform alone. Zero biases gave 31.2% in step 2, while adding them in step 3 raised it to 36.4%, so they do help and the real problem is keeping them stable. I'm now considering averaging the biases from steps 3 through 5, adjusted for the observed prediction counts.

Now I'm comparing the step 3, 4 and 5 bias values and their prediction counts, to see whether averaging them would give stable biases.

I'm averaging the correction for each class from the step 5 biases, aiming for predicted counts near 1000, and starting with class 0 at a learning rate of 0.4.

Now I'm working out the class 0 to 5 bias corrections from the step 5 values, nudging each one by 0.4 times the log of 1000 over its predicted count.

I'm applying the same correction rule to classes 5 through 9, each with its own learning-rate step from the step 5 bias, and I'm checking the class 9 line I've started.

I'm settling the class 6 to 9 corrections from the step 5 values, with class 9 ending near 0.1 after its learning-rate step, and I'm about to work out what remains for the last class.

I'm going to stop trying to make the biases perfect and put the effort into the templates instead. For step 6, I want to add corner detectors on channels 10 through 13 and the diagonal channels 14 and 15, and give every digit a template across all channels rather than only the selected ones, so the FC layer uses its full capacity.

I'm checking which corner each combination of boundary channels picks out: channel 10 pairs the bottom and right boundaries, so it should mark the bottom-right corner of an ink block.

I'm checking the corner channels now: channel 10 combines the bottom and right boundaries, which should pick out the bottom-right corner of an ink block, and I'm working out what the other three corner channels pick out in the same way.

I'm checking the corner channels: channel 10 combines the bottom and right boundaries, so it should fire at the bottom-right corner of an ink block, where both are positive.

Now I'm working out which digits the bottom-right corner channels would help separate, and I'm drafting a corner template for channel 10 with a 7 in mind.

Still writing corner templates...

Now I'm weighing whether to change the conv2 layer so it keeps finer spatial detail instead of averaging so much.

I'm sketching a delta kernel for the conv2 pass-through channels, since keeping only the center pixel might stop neighboring 4×4 cells from sharing so much of their 3×3 window and make the spatial patterns easier to tell apart.

I'm checking the delta-kernel version now: each conv2 cell copies the center pixel of the matching maxpool1 position, so each 4×4 output cell is the max over a 2×2 block starting at (2R+2, 2C+2). I'm working out which blocks feed rows 0, 1 and 2 of the grid.

I'm checking the border handling next: the delta kernel skips the outer rows and columns of the 12×12 map, so the digit's edges, where ink often sits, would drop out of the features.

I'm weighing whether losing the border positions matters much, since a digit centered in the 28×28 frame rarely has ink there. The delta kernel might sharpen the features, but a single-pixel max is noisier and could cause more false activations, so I'm considering a plus-shaped kernel as a compromise.

Still writing the center-surround kernel...

I'm settling on a sharper kernel for the edge and hole channels, keeping the smooth one for the ink channel, since those features are already localized and the smoothing might be washing out their spatial detail.

Still writing the feature-channel code...

Now I'm checking the delta kernel for the edge channels: the strongest response in each 2×2 block should keep the top and bottom boundaries of a circle visible in the 4×4 grid, which might help tell digits apart.

I'm going to keep the delta kernel change for the edge and hole channels, since the sharper spatial detail should give the template matching more signal. The combination channels are next, and I'm checking whether the delta kernel affects them as well.

Still writing the conv2 kernel assignments for the horizontal stroke channel...

I'm settling on a sharper kernel for the conv2 pass-through channels, but still keeping the smooth kernel on the combination channels, since ch 8 reads maxpool1's edge channels through its own kernel regardless. Each conv2 channel can use its own 5×5 kernel, so I can mix kernel types freely. I'm also wondering whether the delta-kernel channels need a larger scale, since the max over four single-pixel values could come out with a different magnitude than the smooth version.

Comparing the two kernels on a region where every value is the same, they give identical results, so the difference only shows up where the values vary. The smooth kernel gives a weighted average, which lands between the min and max, while the delta kernel just takes one center value. Taking the max over each 2×2 block afterward will tend to keep the stronger responses either way.

Still writing the template code...

Still writing the convolution weights...

Still writing the conv1 kernels...

Still writing the convolution weights...

Still writing the conv2 kernel assignments...

Still writing the conv2 weight assignments and the FC bias setup.

Still writing the border handling for the feature templates...

Trying a plus-shaped kernel now: the center takes most of the weight and the four cross neighbors take a small share, so the features stay localized without dropping the border positions the delta kernel loses.

Still writing the pass-through kernel...

I'm settling on a plus-shaped kernel for the edge and hole channels: the center carries about 60% of the weight and the four cross neighbors share the rest, which keeps the features localized without dropping border positions the pure delta kernel loses. I'll test the delta version first and switch back if it doesn't help.

Now I'm adding corner templates on channel 10 for the digits that have a bottom-right corner, placing them at the spots where the strokes meet.

Now I'm settling on the final plan for step 6: fix the biases, switch the edge and hole pass-through channels to a delta kernel, and reuse the step 5 templates with a few corner and diagonal additions. Before writing the code, I want to recheck the ink density templates for digits 7 and 9.

Now I'm checking the expected ink for digit 7 against each row of the 4×4 grid: the top bar should show up in the first row, the diagonal moving down the left side through the next three, and my template's signs look roughly right for that.

Now I'm weighing whether col 2 should also be positive for row 3, since the MNIST 7 stroke tends to end near the bottom-center rather than the bottom-left.

I'm weighing whether the template adjustment will matter much, since the bias oscillation looks like the bigger problem. After five steps at 41.5%, I want a bigger jump than tweaking templates, so I'm considering treating the FC layer as a per-feature lookup table with weights set from what each feature means for each class. The catch is that this depends on how well I actually understand the features, which is still shaky.

Rather than fixing a 4×4 template by hand, I'm weighing whether raw, non-centered templates with class-specific biases would be easier to reason about, though zero-mean templates still seem necessary so one class doesn't dominate. I'm going to try a bolder change next: giving all 16 conv2 channels to every digit's 4×4 template.

I'm weighing whether to expand the templates to more channels, but I'm only going to add them where I understand what each channel detects, so I'm keeping the set to the ink, boundary, hole, and stroke channels I've already been using.

I'm settling on a final step 6 plan: updated biases, delta kernels on the edge and hole pass-throughs, and the same templates as step 5. I'm also considering a few extra templates to counter the 7→9 confusion, though centering already covers part of that.

I'm comparing the centered ink templates for digits 7 and 9, since their top and right strokes overlap and digit 9's template might still score reasonably well on a 7.

Now I'm comparing the digit 7 and digit 9 centered templates against a sample feature grid, starting to score the digit 7 logit by weighting each template cell with the matching feature value.

Now I'm working through the weighted sum for the digit 7 logit, adding up the products of each template cell with its feature value across the rows.

Now I'm working out the digit 9 logit, which is also a weighted sum of the template cells against the same feature grid.

Checking the digit 9 logit now: the weighted sum comes out to about 0.69, which puts digit 7 well ahead before biases.

Still working out why digit 7 gets confused with 9 when the hole and edge templates are involved.

Now I'm checking the hole templates for digit 9 against an image with a hole at the top, where the hole features should be high in the upper positions.

Now I'm checking the digit 7 hole logit against the hole features for the digit 9 image, working through the rows where the hole channels are active.

Now I'm checking the hole logits for a digit 9 image with holes at the top: digit 7's hole contribution comes out around -0.7, while digit 9's is about +2.24, a gap of roughly 2.9 in favor of 9.

Checking whether my feature estimates are off, since the confusion matrix sends 668 of 1090 sevens to class 9 while my hand-computed logits say 7 should win comfortably. The other templates may be pulling the wrong way.

Now I'm checking the horizontal stroke template for digit 7, which has its top row active and a few weights in the middle rows, and I'm centering it since it averages slightly negative.

Now I'm setting the horizontal stroke template for digit 9, which has its top and bottom rows active and is already zero-mean, so I'm scaling it down to about 0.105.

Now I'm checking the horizontal stroke templates for digits 7 and 9 against a top-bar feature pattern, where digit 7 comes out to about 1.12 and digit 9 is still being worked out.

Checking the vertical stroke template next, but digit 7 has none, and for a 7 the vertical features should be close to zero, so it adds little. Tallying up: ink gives 7 a lead of about 2.91, and horizontal strokes add roughly 0.70 more to 7, so the stroke channels don't account for the 7→9 confusion.

Now I'm checking whether the 7-versus-9 confusion could come from something other than the ink and stroke templates, since those alone should put class 7 well ahead. My hand estimate says a logit gap of about 3.3 in favor of 7, which would be far from the 668 misclassified sevens in the confusion matrix. So either my feature values are off or another channel is pulling toward 9.

Now I'm checking whether the conv1 ink outputs are actually as large as I assumed, since a 0.5 average patch gives about 0.6 after ReLU and a strong-ink patch only reaches about 1.05.

Checking the conv2 pass-through numbers: if the ink areas sit around 0.8 after pooling, the scaled output lands near 3 to 3.5, so my earlier feature estimates of about 2 look too low.

Hold on, if the features were weaker than I thought, the logits would shrink, but the confusion has to come from somewhere else. I'm now wondering whether the 4×4 grid overlaps so much that neighboring positions carry nearly identical values, which would flatten the spatial contrast the templates depend on.

I'm checking how much spatial variation the features actually have, since a template with zero sum only responds to differences across the grid. With variation around 0.5 per cell, each template cell adds only about 0.175 to the logit, so the total stays small compared with the averages I'd been assuming.

Next I'm checking whether the template signal is simply too weak: with features that vary only slightly across the grid, a zero-sum template gives a small logit, so the biases end up dominating the predictions. That points toward either increasing the spatial contrast in the features or scaling up the templates.

One option I'm weighing is a center-surround operation in conv2 to emphasize local contrast, but it can yield negative values that ReLU would cut off, so the output would need to stay positive where the features matter.

Still writing the ink contrast kernel...

Now I'm reconsidering the ink contrast idea, using a center-surround kernel on the ink channel so it fires where ink is concentrated at a stroke's center, which should help separate thin strokes from wide regions. I'm repurposing channel 10 for that.

I'm checking whether channels 10 through 15 are free to repurpose, and I think they are: the FC templates only use channels 0 through 4, 7, 8, and 9, so the unused ones can take the new contrast kernel without breaking existing templates.

Setting channel 10 up as an ink-contrast detector now: clearing its old corner-detector weights and applying a center-surround kernel to the ink channel.

Still writing the ink-gradient kernel for channel 11...

Still writing the vertical gradient kernel for channel 12...

Now I'm weighing whether the ink gradient channels can separate digits by left-right asymmetry, and I'm working out that ReLU only passes the "more ink on left" direction, so detecting "more ink on right" needs a reversed kernel.

Now I'm working out how the gradient channels would show each digit's left-right lean across the 4×4 grid: channel 12 should light up where the right side carries more ink, as it would for a 3, and channel 11 where the left does, as for a 6.

I'm weighing whether to keep the conv2 changes simple or push the gradient-based templates further, since the maxpool1 input is what those kernels actually see. I think the stronger move is to stop overthinking and keep step 6 small: update the biases, leave the conv layers mostly intact, and add only a few templates.

The digit 7 versus 9 confusion probably isn't just about how many templates I have, since the 4×4 grid itself may be too coarse to tell them apart. I'm thinking the edge channels could carry more of the shape information, since the boundary pattern on that small grid may be more distinctive than raw ink density.

Now I'm adding edge templates for digit 0, checking where its top and bottom boundaries fall on the grid.

Now I'm working through the edge templates for digit 0 and 1, checking which grid rows and columns each boundary lands on.

Now I'm laying out the edge boundaries for digit 2 on the 4×4 grid: the top curve on row 0, the bottom curve on rows 0–1 and the bar on row 3, plus the left diagonal and right side.

Next I'm writing out the edge boundaries for digit 4: the top of its left diagonal and right vertical, the bottom of the right vertical and crossbar, and the left and right sides on the grid.

Now I'm writing out the edge boundaries for digit 6 and 7, checking which grid rows and columns the top, bottom, left, and right boundaries land on.

Now I'm listing the edge boundaries for digits 8 and 9 the same way: where the top, bottom, left, and right edges fall on the grid, with the top loop and both sides of the 8 spanning every row.

I'm listing the edge boundaries for digit 9 as well, with the top of the loop on row 0 and the bottom of the stroke on row 3. The edge patterns look distinctive, since digit 1 puts its left and right boundaries in the same center column while digit 7 splits them to bottom-left and top-right. If I add all four edge channels for every digit, that comes to 40 new templates, which I'd then combine with the existing ink, hole, and stroke templates.

Still writing the edge templates in compact form...

Still writing the edge template values for digit 7...

Still writing the edge template lookup tables...

Still writing the edge template values for digit 9...

I'm adding two discriminative right-boundary templates for digits 7 and 9, since 7 has its right edge only at the top while 9 has it along every row. I'm going to keep this to the key confusion pairs and submit step 6.

Still writing the edge template values...

Still writing the edge template tables for the remaining boundary channels...

Still writing the edge templates for the confusion pairs...

Still writing the edge templates for the 4 and 8 confusion pair...

Still writing the edge template values for digits 3, 4, 7, and 9 on the right and left boundary channels.

Still writing the top-boundary templates for digits 0, 1, and 2, with their values on the ink-start row.

Still writing the top-boundary templates for digits 3 through 6...

Still writing the top-boundary templates for digits 7 through 9.

Still working out the edge templates for channels 1 through 4, and I'm checking which direction each conv1 filter responds to before I commit to the values.

Now I'm working out how the first conv1 channels respond to vertical edges: one picks up where ink sits above background, the opposite pattern gives the upper boundary, and the remaining two track left and right boundaries.

Now I'm checking the sign convention on conv1 channels 3 and 4, since their weights run opposite to filter 1 and the boundary direction depends on it.

Now I'm working out how the first conv1 channels respond to edges: channel 3 picks up the right boundary of ink and channel 4 the left, so a vertical stroke shows up as one response at its right edge and another at its left edge.

I'm working out the grid positions for digit 0's edges: the top boundary on channel 2 lands in grid row 0, the bottom boundary on channel 1 in row 3, and the left and right boundaries on channels 4 and 3 in columns 0 and 3.

Working out the edge templates for digit 0 and the other digits on channels 1 through 4, mapping each boundary onto the 4×4 grid.

Still writing the upper-boundary templates for each digit as 4×4 grids.

Still writing the edge template tables, filling in the upper-boundary values for the remaining digits.

Still writing the edge template tables for digit 9's upper boundary and the rest of the templates.

Still writing out the step 6 code, keeping the conv1 and conv2 weights from step 5 and adding the expanded FC templates.
