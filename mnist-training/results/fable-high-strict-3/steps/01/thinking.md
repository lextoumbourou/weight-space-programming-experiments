I'm sketching out a small hand-built CNN for MNIST, with two conv layers feeding a final linear layer to ten classes. The first conv layer will use eight 5x5 filters, aimed at picking out simple oriented strokes and edges.

I'm weighing whether to leave conv2 as a near-identity pass-through and rely on fc template matching, but a 4x4 digit template would be too coarse to do well. A better route is to have conv2 carry distinct spatial information through its channels, since the pooled 4x4 maps from the 16 outputs give 256 features to work with.

I'm working out which input rows the 4x4 grid actually covers: the conv and pooling offsets land the grid on roughly rows 6 to 21 of the 28x28 image, which is close to where the digit sits.

The 4x4 grid lands on roughly input rows 6 to 21, so it misses a little of the edges, though the 5x5 receptive field reaches past that. I could use off-center taps in conv2 to shift different regions, giving each channel a different conv1 source and offset. Richer conv2 kernels could also encode combinations like a horizontal stroke above a vertical one, but designing those by hand without data is hard, so I'd plan to iterate using the confusion matrix feedback. Another option is to treat the network as a linear template matcher on a downsampled image.

I'm considering using conv2's taps at shifted offsets so each channel samples a different spot, which would give finer spatial coverage than a 4x4 grid of one fixed alignment. Max pooling makes the shifted copies behave like maxes over different 2x2 windows, so I'm checking whether a few offsets together could recover resolution.

I'm checking how the 4x4 grid of pooled values could be sharpened. Four conv2 channels with taps at offsets (0,0), (0,1), (1,0), and (1,1) would together give the full 8x8 pooled grid for one conv1 channel, and with 16 channels that covers four conv1 channels at 8x8 resolution, roughly covering the central input pixels.

I'm working out how shifted conv2 taps would sample the pooled conv1 maps at offsets. For a tap at kernel position k, the pooled output at each cell lands on different pool1 indices, so two shifts of 2 and 3 give two different stride-one views of the same region.

I'm checking whether using k=1 and k=3 offsets would give a strided sampling that covers a wider stretch of rows than the k=2,3 pair.

I'm weighing whether to use hand-drawn templates on the 8x8 pooled map, which would give four oriented feature types, or to rely on a linear classifier over raw pixels. Hand-drawn templates would probably land around 60 to 75 percent, while a trained linear model does better, so I'm considering using the feedback loop over several steps to tune the weights instead of fixing them by hand.

I'm settling on a design where one conv1 channel acts as an ink detector, with conv2 producing shifted copies of it at 8x8 resolution. The remaining channels would carry a few stroke-orientation detectors in the same shifted layout, and I'd draw the fc templates over that 8x8 grid for each class.

I'm weighing whether a nearest-centroid or linear template approach could work here, since those baselines hit roughly 82% and 92% on MNIST pixels, while hand-drawn templates from memory would probably land around 50 to 70%. Adding horizontal and vertical stroke features should help separate pairs like 1 and 7 or 4 with its middle bar. I'll build a reasonable design first and then tune it against the confusion matrix.

I'm settling the fc templates as centered discriminants, subtracting the mean of the class templates so each one only needs to say how it differs from the rest, and I'm noting that drawing them by hand is fine. Next I'll set up the conv1 filters, starting with an ink-detecting channel that has a slightly negative bias to suppress faint background.

Next I'm setting the horizontal-stroke filter's row weights so it fires on a bar through the center row and stays quiet just above and below it. Its column weights are flat, so it responds across the full width of the patch.

I'm laying out the remaining conv1 channels: a vertical stroke detector that mirrors the horizontal one, and two diagonal detectors, one for "/" and one for "\", each set to respond along its own direction and stay quiet along the other. I'm also considering the last few channels for a hole detector, since a background-focused filter could help separate 0, 6, 8, and 9, though a 5x5 window is probably too small to capture enclosed loops cleanly.

I'm weighing whether to shift the conv2 taps vertically only, giving each feature eight rows at four columns, since vertical structure may matter more for telling digits apart. I'm also considering whether to skip shifting entirely and use the conv2 kernels to combine features directly.

I'm laying out the fc layer as 4 features over an 8x8 grid, with ink, horizontal, vertical, and diagonal channels each sampled at shifted positions. Writing out the 10 class templates over that 256-value layout is the next step, and it's going to be tedious by hand.

I'm now converting each digit into a list of line segments on the 8x8 grid, with the orientation of each segment implied by its direction. From those segments I'd rasterize the ink map and the horizontal, vertical, and diagonal maps, weighting each by how closely the segment matches that orientation. For curved parts I'd fall back on polyline approximations.

I'm working out how the input-to-pool mapping lines up with the 8x8 grid, so each conv2 tap lands on the right spot for placing the templates.

I'm working out where the pooled rows land in the input: each conv2 tap picks a band of input rows, and the effective row index R maps to a center around 2R+7.5, so the bands run from about row 7.5 at the top to 21.5 at the bottom.

I'm checking whether the 8x8 grid is centered on the digit: with shift offsets 2 and 3 the bands center around pixel 14.5, a bit below the image center at 13.5, which is close enough for MNIST's center-of-mass placement.

I'm mapping the 8x8 template grid back onto input rows, so cell R sits around rows 2R+6 to 2R+9, and the digit box ends up slightly cropped at the top. Shifting to the other pair of offsets would spread it higher, but the current pair seems better for placing the digits.

I'm checking which row offsets to use for conv2: the pair 2 and 3 covers rows 6 to 23 and the pair 1 and 2 covers rows 4 to 21, and I'm reasoning through how the input rows of each pooled cell line up.

I'm picking the row offset for conv2: starting at 2 gives rows 6 to 23, and I'm weighing whether to start at 1 instead, which would cover rows 4 to 21. I'm also checking whether mixing the two offsets across even and odd pooled rows would give a more even spread.

I'm settling on an input-to-template mapping where the 8x8 grid covers input rows and columns 6 through 23, centered near 14.5. I'm checking how a template coordinate relates to an input pixel so each class template lands on the right spot.

I'm converting the template coordinates so that input row y maps to template row (y − 6.5)/2, which puts input rows 6.5 to 22.5 across the 8x8 grid. Digits extend a bit beyond that span, so I'll draw them with their heights running slightly past the top and bottom edges.

I'm considering whether to shift the conv2 taps to cover a different row range, since a 2x2 pool forces each pooled cell to pair up specific rows. Taps at offsets 0 and 4 might let one channel cover the top of the digit and another the bottom, though it's unclear whether that gives a cleaner scale than the current mapping.

I'm weighing whether to offset the conv2 taps so the pooled windows cover more of the input rows, comparing a set of three overlapping offsets (0, 2, 4) against the current pair. Either way I'd be giving up some independence between the windows.

I'm weighing whether conv2 should do more than pass features through, since a learned conv2 could combine them more robustly than hand-built templates. Hand-building that layer is the hard part, and I'm expecting the templates to be rough, so I'll build the first version and refine it from there.

I'm checking how the conv1 filter outputs scale: the Gaussian ink filter stays in [0,1], and the horizontal stroke filter gives about 2 for a full 3-pixel-thick stroke, 1.5 for a 2-pixel one, and 0 for solid ink.

Normalizing the stroke filters by 2 should keep their max response near 1, and conv2 can simply carry each feature channel through at its shifted position. For the fc layer, I'm aiming for template weights that keep the logit gaps to a few units.

I'm mapping out the digit templates on the 8x8 grid, drawing each one as polyline segments and converting input rows to template coordinates. Digits run a bit past the grid's top and bottom edges, so I'm figuring out how much of each stroke gets clipped.

I'm sketching digit shapes on the template grid now, giving each one a height that runs slightly past the top and bottom edges and a width that varies by digit, such as a wider 0 and a narrower 1.

I'm now laying out the rasterization step: each template segment gets sampled densely and splatted onto the 8x8 grid, with its contribution weighted into horizontal, vertical, and diagonal maps by the segment's angle. Those maps get normalized and lightly blurred, and then the fc weights for each class are set from the centered template.

I'm now thinking about the sign of the logits: since the features are non-negative, the mean-subtracted templates behave like a discriminant, though a thin vertical stroke could still score highly for an 8 because both share a center column. Orientation features should help separate a 1 from an 8.

I'm weighing whether the templates should be blurred slightly, since max-pooling dilates the strokes into roughly one-cell-wide bands. A modest blur should absorb variation in handwriting, though too much would blur away the distinctions between classes.

I'm now defining each digit as a set of segments in a unit box, then mapping those points into template coordinates with the digit's width and a fixed height. The 0 gets an ellipse with a width of about 5.5 cells, and I'm working out how wide that comes out in pixels.

I'm working out the vertical extent of the digits in template coordinates, since a 20-pixel-tall digit spans about 10 cells and wouldn't fit the 8.5-cell span I'd first assumed. I'm settling on roughly ty from −1.2 to 8.7 for full-height digits.

I'm settling the digit widths on the template grid: 0, 2, 4, 7, and 8 get about 7 cells, while 1 is much narrower at around 1.5 cells, since a 20-pixel-tall digit's natural aspect gives most digits a width of roughly 7 cells.

I'm defining the digit shapes as stroke segments in a unit box, starting with the 0 as an ellipse and the 1 as a slightly slanted line.

I'm defining the digit 2 as an arc across the top, starting from the left side and curving over to the right, then a diagonal stroke down to the bottom left and a horizontal base.

I'm defining the digit 3 as two stacked arcs, a top one that starts at the upper left and sweeps right and down to the middle, and a bottom one that continues from the middle around to the lower left.

I'm moving on to the digit 4, planning a vertical stroke on the right and a left stroke running down to a horizontal bar.

I'm specifying the digit 5 next: a top bar, a short left vertical, and a bottom arc centered lower in the box, and I'm working through where that arc's starting point should sit.

I'm placing the arc for the digit 5's lower bowl at center (0.5, 0.7) with radius 0.3, starting near the upper-left and sweeping over the right side toward the bottom-left.

I'm defining the digit 6 as a polyline that runs from the top right down to the left side, then closing it with a full circle for the bottom bowl.

I'm now defining the remaining digit shapes as polyline and circle segments in the unit box: a 7 with a top bar and diagonal down to the bottom, an 8 built from two stacked circles, and a 9 with a top circle and a slightly slanted stem. I'm also starting to think about the orientation features, since the ellipse of the 0 should register as vertical strokes on the sides and horizontal ones at top and bottom.

I'm checking how strong the ink and orientation responses should be, roughly 1 for solid strokes and 0.5 for oriented ones. I'm setting the fc weights as a scaled, mean-subtracted version of each template and working out how large the logits should get.

I'm setting the first conv layer's ink channel to a 5x5 Gaussian with sigma 1 and no bias, so a stroke a few pixels wide peaks near 0.8. I'm starting to define the horizontal orientation channel as an outer product of smoothing and derivative kernels.

Still working out the first conv layer's channels: the vertical and horizontal orientation kernels, and now the diagonal one, where I'm weighting the anti-diagonal positions where a+b = 0.

I'm tuning the anti-diagonal kernel so a uniform patch gives zero response: the weights on each diagonal get signs that balance out, and I'm adjusting the ±2 diagonals to −0.6 so the total comes back to zero.

I'm checking the mean-subtracted sum over the diagonal kernel, adjusting the off-diagonal weights so a uniform patch returns zero, and then testing how a vertical stroke responds to it.

I'm settling the diagonal kernel's weights so the vertical response comes out small and the "/" stroke response is normalized to about one, and I'm also thinking about whether the orientation filters should be allowed to go negative.

Writing the convolution weights in code now...

Still checking the coordinate mapping for the second conv layer's pooled cells.

I'm checking the coordinate mapping from the pooled cells back to input pixels, confirming that cell R sits at input row 2R+7.5 and so maps to template coordinate (y − 6.5)/2. Next I'm setting the vertical extent for the digits, starting at about −1.1 with a height of 9.4 template cells, and I'm just beginning to work out the horizontal placement.

I'm adjusting the horizontal center to about 3.7 cells, and the vertical center to roughly 3.5 so the digit box starts near y = −1.2. I'm also wondering whether the center of mass should shift the box for digits like 7, 4, 6, and 9, since their ink sits unevenly.

I'm planning to rasterize the template at high resolution, find its centroid, and shift it so the centroid lands at (3.5, 3.7). I'll also scale the strokes so the bounding box's largest side is 10 cells, mirroring MNIST's 20-pixel fit before centering on the center of mass.

I'm making the strokes in each digit template match MNIST's preprocessing, so I'll fit the digit to a 20-pixel box, then shift it so its center of mass lands where it should. I'll also check that the thin 1 still scales to full height and keep the blur small, and I'm starting to weigh how the mean-subtracted template for the 1 will behave.

Checking whether the 1 template's mean-subtracted weights still give a positive logit for a thin input, given that its ink covers only about ten cells.

I'm checking the logit size for a 0 image against the 1 template, where the center-column cells come out negative, so it stays a clear rejection. I'm also making sure the thin 1 still gets a positive score from its own template, and I'm noting that biases can be tuned later from the confusion matrix. The main risk is thick ink saturating the logits, which I expect to matter less than the template fit itself.

Working through how the diagonal orientation response behaves on a 45° stroke, I'm estimating the weights across columns and checking how it compares to the horizontal and vertical filters.

I'm settling on a cos⁴θ weighting for the horizontal orientation response, and sin⁴θ for vertical, since a diagonal stroke gives only about 0.2 of the full horizontal response. The diagonal channel uses sin²(2θ), which peaks at 45° and sits near 0.5 at 22.5°, so it covers the in-between angles.

Still writing the convolution code...

Still writing the first conv layer's weights in code...

Still writing the first conv layer's weights in code...

Still writing the convolution code...

Still writing the convolution code...

Still writing the convolution code...

Still writing the code for the digit strokes...

Still writing the digit stroke definitions in code...

Still writing the digit stroke definitions in code...

Still writing the digit stroke definitions in code...

Still writing the digit stroke definitions in code...

Still writing the digit stroke definitions in code...

Still writing the digit stroke definitions in code...

Still writing the digit stroke definitions in code...

Still writing the digit stroke definitions in code...

I'm weighing how to map the template points into the eight-by-eight cell grid, using a Gaussian splat around each cell center. Then I'll scale the whole digit so its largest bounding-box side fits the target size.

Checking the centering: the image center sits at pixel-index 13.5, so mapping through (y − 6.5)/2 puts it at template coordinate 3.5 on both axes, and I'll use (3.5, 3.5) as the target center of mass for the digit.

Still working through the digit stroke scale: I'm estimating the logit gap at roughly 13 times the scale factor, so a scale around 0.35 looks safer than 0.5, and I'll tune it from the loss.

Still writing the first conv layer's weights in code...

Still writing the first conv layer's weights in code...

Still writing the digit template definitions in code...

Still writing the digit template definitions in code...

Still writing the digit template definitions in code...

Still writing the digit template definitions in code...

Still writing the splat normalization code...

Still writing the weight-building code for the orientation and fully connected layers.

Writing the final code cleanly...
