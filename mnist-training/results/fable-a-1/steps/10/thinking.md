Accuracy fell to 63%, with heavy over-prediction of classes 1 and 7, which suggests the sparse classes are winning. The tent no-clip features look under-scaled, since typical values seem to sit around 0.7 to 1 rather than near NORM=1.5, so I'm considering lowering NORM to calibrate them.

I'm checking whether the clipped version was better calibrated, and whether NORM should drop to around 0.8 with T0 at 0.2 so the tent features aren't under-scaled.

I'm weighing whether to keep the clipped orientation channels and split the hole detector into smaller, lower-count groups, since the corner-size maps look partly redundant.

I'm weighing whether to keep the hole detector at eight sizes or trim it to four, since the corner evidence from a few sizes may already cover the loops. I'd like to know which sizes are most redundant before deciding.

I'm weighing an alternative to keeping all eight hole channels: giving the corner evidence only four sizes, such as (1,1), (2,2), (2,1) and (1,0), though I'm unsure which sizes are actually redundant. Trimming would change the measured hole weights too, so either I'd need another diagnostic pass or I'd accept rough approximations.

I'm weighing whether to drop the clip on the orientation channels, since reducing the hole channels or adding corner maps would mean giving up hole channels I already have. I'm also considering a shared-pattern channel for the hole detector, but two partial fills could add up to a false positive, so that's likely a poor idea. Calibrating the no-clip variant with NORM around 0.8 is the option I'm leaning toward.

I'm weighing a no-clip variant with the stroke amount left unbounded, which could work tolerably but might cost a few points of accuracy against the clipped version. Four hole channels chosen by geometry could also cover the loops, since corner responses should sit about (h−1, w−1) pixels apart for a rectangular hole, though the exact spacing for round holes is still unclear.

I'm working out how the corner-pooled sizes map to hole dimensions: a pooled separation of about 1 covers the smaller loops, and about 2 covers the larger ones. Mixing tall and wide variants looks like it would cover the most shapes with four channels, so I'm starting to list which four pairs to keep.

I'm considering whether to keep the four corner channels on top of the hole sizes, or whether the corner maps could pass through conv2 without a ReLU.

Next I'm settling the four hole sizes and the corner pass-through channels, then working out the hand-set FC weights for the corners.

I'm settling on the corner pass-through kernel: a single center tap with max-pooling keeps the response bounded, though it misses corners near the top edge of the digit.

I'm checking how the corner taps line up with the pooled cells: each cell covers a four-pixel band of filter centers, so a corner at a band boundary can flip cells, which the soft templates should tolerate. A single center tap with no threshold seems enough, since the conv1 output is already thresholded.

I'm annotating each digit's corner positions in the unit shape coordinates, then having the placement step transform those points along with the strokes. Each corner response gets spread with a soft window across the pooled cells, since hand-placing a 4x4 grid per digit would be error-prone once the center-of-mass shift is applied.

I'm sketching how to turn each corner annotation into a 4x4 grid of pooled cells, using a soft window around each cell's center. The corner probabilities would then convert to weights via log-odds, with the scale set so typical corner responses come out near one.

I'm settling on how to annotate the corners by concavity, with the corner type set by which sides are ink, and I'm weighting the corner evidence at about the same strength as the template features.

I'm placing the corner annotations relative to each arc's inner side, using 45-degree offsets from the arc center for the points where each corner type fires.

I'm working out where the corner responses sit relative to each arc's hole: the filter center falls about one and a half pixels inside the inner radius, so I'm checking how that offset changes with the skeleton radius.

I'm placing each corner annotation at the arc center offset by half the radius on each axis, and working out the zero's corners next, where the loop is wide enough that they fire only weakly.

I'm annotating the zero's corners as an elongated ellipse, placing the top and bottom pairs just inside the arcs at about 0.45 of the radius on each side and 0.6 vertically, with a fairly weak strength of about 0.35.

I'm assigning the zero's corners a weak strength of about 0.3, since the hole diagnostic showed they rarely fire. For the two, I'm placing the top-left and top-right corners on the arc's cap and checking whether the lower-right arc, where the neck starts heading down-left, still has an outward normal that points down-right.

Now I'm working out the corner annotations for the two digit, where the bottom-right and bottom-left junctions get rough strengths of about 0.4 and 0.5.

Now I'm placing the corner annotations for the digit 3, starting with the upper bowl's top-left and top-right corners and its lower-right corner.

I'm placing the corner annotations for the digit 3 now: the upper bowl's top-right and bottom-right corners get strong weights, the top-left a weak one, and the lower bowl's right-side corners are strong with a weaker bottom-left tail.

Now I'm assigning the annotations for the three shapes: for the 3s, the upper bowl's top-right and bottom-right corners are strong, the top-left is weak, and the lower bowl's right-side corners are strong with a weaker bottom-left. Next I'm moving on to the 4, where I'll place the left stroke, the bar, and the stem.

Now I'm placing the corner annotations for the 4: the left-stroke and bar junction gets a strong weight, and the bar-stem crossing gets another strong one in the upper-left quadrant.

I'm placing the stem/bowl-top corner where the stem meets the bowl, with its inner region to the right.

I'm placing the corner annotations for the six, starting with the top-left corner of its loop.

I'm finishing the corner annotations for the 7, placing the top-left serif corner just under the bar with a light weight.

I'm now annotating the eight: two loops, with the upper lobe's corners placed around its center near (0.33, 0.25) and the lower loop's corners around (0.33, 0.75), each weighted fairly strong.

I'm placing the nine's loop corners at the usual 0.135 and 0.405 rows, and I'm starting its stem down from the upper right.

Still writing the corner rendering code...

I'm working out how the pooled-cell weighting should behave: each cell's response falls off linearly with the filter-center offset, so a corner gets full weight within two pixels and fades out by five. I'm setting the corner weights from the squeezed probabilities, scaled against a typical value of 0.6, and adding a bias term from the log of the complements. I'm also keeping in mind that the corner probabilities might be off and fire in the wrong places.

I'm considering a threshold in the conv2 pass-through, since diagonal strokes like the 7's and a slanted 1 can produce weak corner responses around 0.1 to 0.3 that would wrongly push those classes.

I'm settling on a corner weight scale around 0.2 and a bias near -0.15, normalized against a typical response of 0.45, since I can't measure how these will behave until I test them. I'm also adding a pass-through in the conv2 stage for the corner channels, so the corner signal feeds forward, and I'm keeping the hole-size slopes the same even though there are now only four channels instead of eight.

Still writing the corner rendering code...

Still writing the corner rendering code...

Still writing the corner rendering code...
