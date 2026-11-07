Loss has dropped to 3.98 but accuracy is stuck at 36%, so the features and templates look like the real bottleneck rather than calibration. I need a fundamentally stronger classifier signal. Looking at the confusions, class 5 keeps absorbing predictions from several classes, and my 4x4 spatial template approach using mean

I'm weighing whether to exploit the conv2 structure by giving each channel its own orientation-specific template, since right now all 16 channels share one template and the orientation information is lost in the sum. For each class I'm sketching which stroke orientations should show up in which grid cells, such as horizontal strokes at the top for one digit and a vertical centre for another.

I'm planning per-class templates that split the channels into orientation groups, since the shared template throws away stroke direction, and I'm estimating the size of that table. The conv2 outputs pair up, so channels o and o+8 share a primary pattern, which sorts them into vertical, horizontal, diagonal, blob, and centre groups.

I'm working out the channel grouping: output channels 0 and 8 share the vertical primary, 1 and 9 horizontal, 2 and 10 one diagonal, 3 and 11 the other diagonal, and the rest form a mixed group. Channel 8 also picks up a weighted blob feature, so it's not a pure vertical detector, but the grouping still holds.

Now I'm setting up the per-class spatial weights: for each class, a 4x4 expected-presence map for each of the five orientation groups, applied across the 16 channels.

I'm sketching the per-class orientation maps for digit 0, which is a ring: vertical strokes down the left and right sides, horizontal strokes across the top and bottom, and diagonal corners.

I'm now laying out the spatial pattern for digit 0 as a ring: vertical strokes on the left and right, horizontal ones along the top and bottom, and diagonal corners, with the centre kept negative to tell it apart from other digits.

Still working out the digit-0 template: vertical strokes down the left and right columns, with the centre kept empty.

Still writing the digit-0 template: vertical strokes down the outer columns, horizontal along the top and bottom, and the centre kept negative.

Still writing the digit-0 template: the top-left and bottom-right corners get a half-weight diagonal, the top-right and bottom-left get the opposite one, and the centre cells are negative.

Still writing the digit-1 weights: a strong vertical column in the middle cells with a mild penalty on the outer ones, and small negative values for the other orientations.

Still working out the digit-2 template: a horizontal bar along the top and another along the bottom, with a right-side curve and a diagonal running down to the lower left.

Still writing the digit-2 and digit-3 weights: the top-row horizontal and right-side vertical cells are being set in the grid.

Still writing the digit-3 template: the top and bottom arcs get horizontal weights, with a vertical curve on the right side and the centre left empty.

Still writing the digit-4 weights: a left-side diagonal and a vertical stroke, with the rest of the cells kept near zero.

Still writing the digit-4 template: the right-hand stem runs full height, a crossbar sits across the third row, and the left stroke only appears near the top.

Still writing the digit-4 and digit-5 maps: the negative penalties for the bottom-left cells, then the digit-5 top bar.

Still writing the digit-5 weights: a top bar across the full width, a left stem on the upper row, and a bowl curve at the bottom right with the rest left empty.

Still writing the digit-6 weights: a left-side vertical stroke in the upper and middle rows, a right-side cell on the third row, and the rest kept near zero.

Still working out the digit-6 map: the left column gets a stroke, with a diagonal along the top.

Still working out the digit-7 weights: a horizontal bar across the top row, with a diagonal stem running down and to the left.

Still writing the digit-8 weights: the left and right loop columns get vertical cells in the middle rows.

Still writing the digit-8 and digit-9 maps: the crossing stroke for the figure eight and the matching centre cells.

Still writing the digit-9 weights: a top loop row, a left-side cell in the upper row, and a right stem running down the far column.

Still filling in the digit-9 weights: the centre cells get negative values to mark the hole, and I'm noting a left-side piece I haven't finished setting.

Still working out the group mapping: output channels are bucketed by their pattern index modulo 8, so each orientation group covers two channels, and I'm scaling the per-class templates before applying them to the classifier weights.

Still working out the classifier biases: the earlier values helped the loss a little, but class 5 is still being over-predicted for several digits, so I'm looking at whether the bias for 5 needs pulling down.

Still tuning the biases: I'm nudging the class 5 bias down since it keeps absorbing predictions, and I'm planning to mean-subtract the per-group templates across classes before building the classifier weights.

Still writing the per-class template arrays, now coding the group mapping and the weight tensor layout.

Still writing the per-class template arrays for digits 1 and beyond, with the same 4x4 layout of vertical, horizontal, diagonal, and negative maps.

Still writing the class-2 templates: the vertical map has a single half-weight cell, and the horizontal and diagonal maps are being set.

Still writing the digit-3 and digit-2 maps: the vertical cells down the right side, and the horizontal top and bottom rows.

Still writing the digit-5 template: a top row of ones, a left-side stroke on the upper rows, and the rest of the cells kept near zero.

Still writing the digit-6 template: the left column carries a stroke in the upper rows, with a right-side cell and the bottom row kept near zero.

Still writing the digit-7 and digit-8 templates: a top bar and a diagonal stem for the 7, with the left-side cells kept negative.

Still writing the digit-9 template: the top loop and right stem are set, and the left and centre cells are being filled in.

Still writing the digit-9 template's per-class arrays, and this stretch is the 4x4 maps for the 4, 7, 8 and 9 classes: vertical, horizontal, and the negative bottom-left penalties.

Still writing the final code, reusing the convolution section from the previous step.
