Now I'm checking whether class 1 dominates because of how its template lines up with the 4x4 grid cells, which overlap across columns 2 through 25. A digit about 20 columns wide would sit across those overlapping side cells, so the centring affects which cells end up with ink.

The E channel is biased toward the borders for every digit, since the side cells are mostly empty, so its template matches class 1's pattern no matter what the digit is. That's why class 1 keeps winning. I'm thinking of dropping E from class 1's score and cutting its weight overall, while the ink channel still separates class 1 reasonably well.

I'm checking the 5 template next, since 5 only gets 113 correct. Its top bar and left vertical stroke fall across the overlapping cells, so the stroke at column 8 lands in two cells at once and the feature maps come out blurrier than I assumed.

Now I'm weighing whether to switch from averaging over the 3x3 neighbourhood to a single tap, which would give cleaner stroke presence but lose some sense of how much ink there is. A 2x2 tap might be a middle ground.

I'm weighing whether a single centre tap, with weight 1.0, is cleaner than the overlapping 2x2 option, since its cells cover the digit box with less overlap. For the E channel, a mean over the centre 3x3 taps still leans toward the borders, and an ink-negative version would need something the ink channel can't supply after ReLU.

I'm dropping the E channel from the templates, since the centring already penalises cells with no expected ink, so the hole in a 0 still gets handled. That frees up conv1 channel 5 for something else.

I'm weighing whether to describe the strokes in pixel coordinates and let the code map each one onto the cells it touches, rather than placing them by hand in each cell.

Now I'm turning the stroke layout into a rasteriser: each segment in pixel coordinates gets sampled, and every cell that covers a sample point gets credit, so overlapping cells both register the stroke. The orientation of each segment will be classified from its angle, which should make the templates more accurate than my hand placement.

Now I'm thinking about the fully connected layer, deciding to drop the E channel and normalise each feature map before combining them, and I'm weighing whether to reuse channels 8 through 15 for finer vertical detail instead of blurry averages.

Now I'm thinking about shifting the channel geometry: some channels would sample at a different offset so the cells cover the digit more finely, and the rasteriser would handle whatever layout I pick.

I'm weighing whether channels 8 through 15 should sample one step up and left, which would give extra vertical and horizontal detail beyond the centre-tap grid. I'm also wondering whether the extra channels could carry the P and E features instead.

I'm sketching the digit strokes in pixel coordinates and rasterising them into the cell grid, so each template comes from the actual geometry. The zero is an ellipse centred in the box, and the one is a near-vertical line with a slight slant.

I'm deciding how to assign each stroke's orientation to the H, V, B, S, and P channels. The plan is to compare each segment's angle with each channel's preferred angle and give more weight to the closer ones, with a narrower tolerance for P.

Still working out the stroke geometry for each digit: a zero as an ellipse, a one as a near-vertical segment, and the start of a two as a top arc with a diagonal and base line.

Still working out the stroke arcs for the 3: a top arc and a bottom arc, each defined by a centre, radius, and angle range.

Still working out the stroke coordinates for the 4, 5, and 6, placing each arm and the belly of the 5 as arcs in the pixel frame.

Still placing the 9's loop and tail in pixel coordinates, using a circle near the top and a segment running down the right side.

Now I'm finishing the template clipping step: each stroke's sample points get credited to the cells they fall in, and I'm deciding whether to cap the accumulated values so the features read as presence rather than stroke length.

I'm deciding to repurpose conv1 channel 5 rather than keep the E channel, since the rarely used steep "\" orientation isn't worth a slot. I'm considering a wider spread of orientations, eight in total, with the ink channel alongside them.

Still settling the orientation set: six angles from 0° to 150°, with the 60° channel standing in for the old P slot, and a diagonal stroke at 45° splitting its response between the 30° and 60° channels. Next I'm working out how to build the filter for any given angle.

Still working out the orientation weights: each sample's tangent angle gets split across the nearby channel angles, and I'm building the filter for an arbitrary angle from its perpendicular distance to a line through the cell centre.

Still checking the orientation bands: for each angle I'm measuring how far each cell sits from a line through the centre, keeping the cells within about one unit, and I'll normalise by the count of cells in each band.

Still setting up the conv2 layout: channels 0 through 7 take the centre tap, and I'm about to work out what offset the next group should use.

Still tuning the scaling: I'm checking whether the feature norms around 4 to 5 justify keeping the scale at 1.5 or raising it to 2 if accuracy climbs, and I'm thinking about adding an ink template built from the union of all strokes.

Still writing the stroke-sampling helper for the arcs, so the points follow the curve at a steady step.

Writing the angular weighting and cell accumulation code...

Still defining the digit shapes: a zero as an ellipse, a one as a slanted segment, and a two as a top arc with a diagonal and base line.

Still placing the remaining digit strokes: the 3's lower arc, the 4's arms, the 5's bowl, the 6's loop, the 7's diagonal, and the 8's top circle.

Still placing the 9 and the arc templates in pixel coordinates, then checking the 7's steep diagonal angle and the 1's slant against the orientation channels.
