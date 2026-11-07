I'm starting this multi-step task now, and since there's no feedback yet, I'll aim for a reasonable first attempt. I can't run code or pull in synthetic data to compute weights, so I'm planning hand-designed filters, starting with eight 5x5 filters in the first convolution layer that detect edges in different directions.

I'm weighing a simpler route: keeping the spatial layout intact through the convolutions, so the final layer can match patterns against hand-drawn digit templates.

I'm picking the first conv layer's filters by hand: a vertical bar detector, a horizontal one, and two diagonal ones, with negative side weights so only strokes light up. I'm also considering a flat averaging filter to capture overall ink.

I'm settling the last few filters in the first conv layer: one that keeps the top-versus-bottom contrast, one that passes the center pixel straight through, and one that just flags whether there's any thick ink at all. Next I'm planning the second conv layer, which has 16 filters over those 8 channels.

I'm now laying out the second conv layer's 16 filters, each tied to one of the eight first-layer channels with a spatial pattern: a center blob, a vertical bar, a horizontal bar, or a diagonal.

I'm weighing how to set up the second conv layer's filters, mapping each of the 16 outputs to one of the eight first-layer channels with a simple spatial pattern like a vertical bar, horizontal bar, or diagonal. For the final fully connected layer, I'm considering whether to encode a rough spatial layout for each digit across the 4x4 pooled grid, such as a ring-like pattern for zero and a central vertical column for one.

I'm settling on a fully connected layer that scores each digit against a hand-drawn 4x4 ink-occupancy template, applied across the feature channels with weights tuned by how ink-sensitive each channel is.

I'm settling the fully connected layer as a simple spatial template: for each digit, a 4x4 map of where ink is expected, applied across all feature channels equally, so each class score is just the template weighted by total feature activity in each cell.

Filling in the digit templates now, starting with the ring for zero and the center column for one, and continuing into digit two's layout.

Still writing digit templates...

Still writing digit templates...

Still writing digit templates...

Still working out the digit templates, and I'm defining the 8 pattern from the 4x4 grid of expected ink for the digit.

Still working out the digit templates, and I'm filling in the rest of the 4x4 grids for digits nine and the remaining classes.

Still writing the first conv layer's filter weights...

Still writing the first conv layer's filter weights...

Still writing the first conv layer's filter weights...

Still writing the second conv layer's filter patterns...

Still writing the first conv layer's filter patterns...

Still writing the second conv layer's filter weights...

Still writing the first conv layer's weights...

Still writing the first conv layer's filter weights...

Still writing the first conv layer's filter weights...

Still writing the first conv layer's filter weights...

Still writing the conv filter code...

Still writing the digit templates as 4x4 grids, and I'm centering each cell across classes so no constant offset favors one digit over another.

Still writing the digit templates as 4x4 grids...

Still writing digit templates...

Still writing the digit template grids, and I'm settling on a short explanation: this is a first attempt built from stroke-layout priors rather than trained weights, so I expect only modest accuracy.
