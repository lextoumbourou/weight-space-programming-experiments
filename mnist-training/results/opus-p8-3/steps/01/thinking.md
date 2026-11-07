I'm planning the weights by hand, starting with conv1 as oriented edge and stroke detectors, conv2 to combine them into spatial patterns, and the fully connected layer acting as templates over a 4x4 grid of 16 channels. A simpler route I'm considering is making the network roughly perform template matching, with conv1 channel 0 as an identity-like center-pixel or small blur passed through ReLU, which pooling reduces to 12x12.

I'm sketching the second layer as 16 channels that carry oriented-stroke presence forward, so the final 4x4 grid holds per-cell ink information. Each cell in that grid covers a 16-pixel input region, so I'll write the fully connected templates by saying which cells contain which strokes for each digit.

I'm working out how each final grid cell maps back to a region of the input, which puts the cell centers around rows 7.5 to 19.5 and covers the digit's span. Next I need to set the fully connected weights directly in feature space, marking for each digit which orientation channels appear in each cell, possibly derived geometrically from stroke segments.

I'm sketching the first conv1 layer as eight 5x5 filters: one blur-style ink detector with a small negative bias, and four oriented line detectors at 0°, 45°, 90°, and 135° built from a positive stroke band flanked by negatives. The remaining channels are still undecided, perhaps edge or endpoint detectors.

I'm checking how an oriented line filter responds: a horizontal stroke gives a strong positive value on the center row, while a vertical stroke cancels out to zero across the columns. For diagonals I'm defining the weight as a function of distance from the diagonal line, falling off to half strength one step away.

I'm settling on the oriented detectors as a Mexican-hat profile across the line, zero-meaned inside the 5x5 window so flat regions give nothing. Next I need to pin down how the angle maps onto the row and column offsets.

I'm defining the orientation angles in terms of a normal direction, so horizontal lines depend only on row offset and vertical lines only on column offset. For the diagonals I'm working out which way the "\" and "/" strokes fall, and then I'll set the response scale so a matched stroke gives a clear positive value.

I'm settling the scale of the oriented filters so that the positive weights sum to about 4, which should give a matched stroke a response near 3, with a small negative bias. Next I'll set the second layer: a few channels as blurred pass-throughs of the orientation maps and one as an ink blur, with the rest left open.

I'm mapping the 4x4 final cells back to input coverage, and a center-tap conv2 kernel would keep localization sharper than a full blur. Each final cell is then a max over a 2x2 block of those outputs, so I need to work out which input rows each one reaches.

I'm working out how the final 4x4 cells line up with the input: with a center-tap conv2 kernel, each cell should cover input rows roughly 4i+6 to 4i+9, which tiles the digit area without overlap. I'm wondering whether taking a max over that block still keeps stroke positions distinct enough.

I'm weighing whether to shift the conv2 kernel or use eight extra channels for something else, since the eight conv1 channels can't fill sixteen. I'm considering eight orientations at 22.5° steps, and adding a shifted copy of the orientation maps would sharpen the final grid's localization.

I'm weighing a hand-built linear classifier over the 256 orientation-by-position features, guessing it might reach 70 to 85 percent before refining against a confusion matrix. I'm also considering conv2 features for line endings or loops, though those are harder to set by hand.

I'm now weighing whether the conv2 channels should keep the first five conv1 maps with a light blur, with the rest left at zero for the time being, and whether making conv1 channels 5 to 9 shifted copies, offset by one pooled pixel diagonally, would help. I'm inclined toward keeping things simple at first. I also want to check that the 4x4 grid's cells, each covering about four input pixels across rows and columns 4 to 23, still fit a digit that is centered by mass, while narrow digits like 1 only occupy the middle columns.

I'm now defining the fully connected templates by sampling points along each digit's strokes, converting them into cell coordinates on the 4x4 grid, and recording the orientation at each point. Each segment's direction then feeds a soft weight into the matching orientation channel for the cells it crosses.

Now I'm settling how to set the fully connected weights: each digit's template is the presence of each orientation in each cell, centered by subtracting the mean across digits. Since the features are roughly binary, I'll clip the template values, and then I need to pick a scale so the logits don't come out too large.

I'm now writing the classifier logits as a nearest-template score, using the squared distance between each feature vector and each digit's template, scaled by a factor β.

I'm estimating the scale of the conv1 responses next, assuming a stroke core near full intensity, so I can set the filters so that a matched stroke gives roughly 1 and the template weights line up with the features.

I'm settling the Mexican-hat profile at a width of about 1.5 pixels, which gives a narrow positive center, a small positive shoulder one step out, and a negative trough two steps out.

I'm checking the response scale of the oriented filters: a 3-wide stroke gives about 5.7 before normalization, so dividing by that puts a matched stroke near 1. Orthogonal strokes cancel to zero, and diagonals should only respond partially. I'm also setting a small negative bias to suppress weak responses, and now I'm moving on to the diagonal case.

I'm normalizing each oriented filter so its positive weights sum to one, which should keep a matched stroke's response at or below one. For the ink channel I'm thinking of a 5x5 Gaussian with sigma 1, normalized to sum to one, so a stroke about three pixels wide should give roughly 0.6 to 0.8. I'll keep a small negative bias to suppress weak responses.

I'm estimating the response to diagonal strokes, which seems to be only partial, roughly 0.3 for a stroke 45° off the filter's orientation, and I'm checking whether the max pooling keeps that signal usable.

I'm setting up the fully connected templates by spreading each stroke's points into the 4x4 cells, with a little extra reach to account for the 5x5 conv1 receptive field, and taking the maximum presence per cell.

I'm settling the classifier scale: the nearest-template logit with β around 0.5, and a bias term scaled by κ≈0.6 because the features run lower than the template values, so the penalty on templates with many strokes doesn't dominate.

I'm choosing between the distance-based classifier and a normalized correlation version, and I'm going with the distance form. Next I'll place the digits in the input frame, roughly rows 5 to 23 and columns 8 to 20, centered near column 14.

Now I'm sketching the digit shapes as coordinate paths: a 0 as an ellipse, a 1 as a slightly slanted vertical line, and a 2 as an arc over the top that drops down to a baseline.

Now I'm sketching the digit 4 as two strokes, a slanted left line dropping to a horizontal bar and a vertical right line, and then turning to the digit 5 with a top bar and a downward stroke.

I'm listing out the remaining digit shapes as coordinate paths, with 6 as a loop that closes back into the bowl, 7 as a slightly curved diagonal from the top bar down to the baseline, 8 as two stacked loops, and 9 as a top loop with its stem.

I'm writing out the rendering step for the fully connected templates: sampling points along each stroke, taking each segment's direction, and weighting it against the four orientation channels with a max(0, cos(2(φ−θ))) response. Next I'm working out how each sampled point spreads its weight across the 4x4 cells.

I'm now working out the spatial weighting for each cell: a stroke point counts toward a cell if it falls within the cell's reach on the conv1 grid, allowing for the roughly 1.5-pixel positive core of the filter. That gives each cell an interval about six pixels wide that overlaps its neighbors, and I'm checking how the mapping from conv1 output coordinates back to input pixels lines up.

Now I'm pinning down where each final cell's input pixels fall: cell i draws from conv1 rows 4i+4 to 4i+7, which maps to input centers 4i+6 through 4i+9. That leaves the outer rows near the edges covered only through the filter's ±2 reach.

I'm working out how the 4x4 cells map back to input rows, and checking whether a conv2 tap at the middle position would line them up better with the 4-to-23 digit span.

I'm settling on the conv2 tap at the middle position, since it puts the cell boundary at about 13.5 and lines up with the digit's center of mass. I'm weighing whether a small 3x3 blur in conv2 would widen each cell's coverage, but I'll start with just the center weight to keep things simple.

I'm extending the spatial falloff to about 1.5 pixels past each cell's interval, and I'm keeping the conv2 weighting centered rather than spreading it to neighbors. For the ink channel I'm using a wider ±2 reach, and I'm setting the template values as the clipped maximum of the orientation response times the cell weight.

I'm setting the fully connected weights to β times the templates, with a bias scaled from each template's squared norm and κ around 0.7. Conv2 channels 5 through 15 stay at zero, and I'm wondering whether the max-pool will pick up too much from curves and stroke ends, so I'll check that with a modest negative bias.

Writing the conv1 filter code now, starting with the weight arrays and the orientation thetas.

Writing the Gabor-style conv1 weights now, with four oriented filters and a Gaussian ink channel, each normalized to a positive sum of one.

Still writing the rendering code, weighting each sampled point's stroke direction against the orientation channels and spreading it across the 4x4 cells.

Still writing the rendering code, now defining the coverage function that scores how strongly each stroke point reaches a cell.

I'm settling the bias term: deriving it from the squared norm of each template, I get a bias of minus β·κ/2 times that norm, and checking the algebra it matches. Estimating the logits, the correct digit comes out around 10.5β while wrong digits sit near zero, so β around 0.5 should keep the margins workable.

Writing the ellipse helper now, then placing the 8 as two stacked loops and the 9 as a loop with a slanted stem.

Still writing the rendering code, and I'm checking that the float32 conversions and array shapes line up. The fully connected weight index runs as channel times 16 plus row times 4 plus column.
