I'm sketching out a hand-built CNN, starting with first-layer edge and stroke detectors at several orientations, then pooling. I'm also considering a simpler template-matching approach, where the first conv channel is close to an identity on the center pixel.

I'm weighing how to lay out the 4x4 features. Each cell covers a broad region, so I'd rather use oriented stroke channels than coarse per-digit templates. I'm also working out how the receptive field grows through the two conv layers and pooling, and I expect the fully connected weights will need to be set by hand from where each digit's strokes sit.

I'm checking whether I can fit the fully connected weights by running the network on template digits, but that's ruled out, so I'm considering writing the low-resolution templates directly by hand instead.

I'm weighing a second option: template matching at higher resolution, with conv2 doing the matching over the 12x12 pooled maps, since the final 4x4 grid alone is coarse.

I'm working out the receptive field math for the second conv layer and pooling, mapping where each 4x4 output cell sees in the original 20x20 digit region.

I'm considering whether a linear classifier on a 4x4 grid of oriented features could reach decent accuracy, though hand-setting those weights would likely do worse. I'm leaning toward defining each digit's template as a set of strokes described in code, and deriving the grid features from those stroke positions and orientations, treating that as drawing templates rather than running the network.

I'm settling on a concrete first conv layer: eight 5x5 kernels with four oriented line detectors at 0°, 45°, 90°, and 135°, each shaped to respond to strokes a couple of pixels wide. I'm thinking of their flanking weights as negative so they pick out thin strokes rather than thick blobs.

I'm setting the first conv layer to oriented line detectors: each kernel has positive weights along a stroke and negative flanks, so uniform ink cancels out and only thin strokes at a given angle respond. I'm also considering a diagonal variant, where the weight falls off with perpendicular distance from the line.

I'm settling the first-layer kernel shape: a Gaussian-like profile over perpendicular distance from the line, with the flanks pushed negative so uniform ink cancels out.

I'm giving the second conv layer's channels a zero-sum window along each line so the kernels stay inside their square, and I'm considering eight orientations at 22.5° steps, though neighboring ones correlate heavily. Four might be enough for the fully connected template, so I'm leaning toward a simpler layout.

I'm considering using eight orientation channels in conv2 as well, so each 4x4 cell carries 128 features. Alternatively, I could shift conv2 with a single center tap so each output tracks a specific offset of the pooled map, though that would only cover part of the digit's rows.

Now I'm working out where the pooled grid cells land on the input: each conv2 tap picks a pool1 position, and the pooling step maps those onto a band of input rows that covers the digit.

I'm checking how the pooling offsets line up with the digit's rows, and a tap at offset 2 would start at row 6 and miss the top edge at row 4. A horizontal detector centered at row 6 would also read row 4 as negative. So I'm considering a maxpool over a wider span of conv2 taps, like offsets 1 through 3, to cover the full digit height.

Now I'm settling on conv2 as a 3x3 box over pooled taps at offsets 1 through 3, so each output cell sees about eight input rows and the overlapping windows cover the whole digit. I'm also weighing how to spread those 16 conv2 channels across the eight conv1 orientations.

I'm considering a finer grid by using four orientations with four spatial shifts in conv2, which would give an effective 8x8 layout at 2-pixel spacing instead of the coarser 4-pixel step.

I'm settling on a sampling scheme for the final features: four orientations, each with two spatial shifts in each direction, so the 4x4 grid becomes an effective 8x8 grid at 2-pixel spacing. Each shifted conv2 tap reads a slightly different band of input rows, so the overlapping windows give finer localization than the coarser 4-pixel step.

I'm working out the sampling offsets for the final grid: with the taps shifted by one pooled unit, the grid centers move down toward the middle of the digit, so the layout sits better over the digit's rows.

Working out which pooling offset gives the best coverage of the digit's rows. Offset 1 covers rows 4 through 21 and offset 2 covers 6 through 23, and the digit spans roughly 4 to 23. I'm weighing whether to blend the two taps or pick one for symmetry.

I'm checking where the 4-to-23 digit band sits against the grid, since shifting the grid one way or the other changes how well the edges are covered. The first-layer line detectors are narrow, so a stroke right at row 23 may fall out of range for the center positions I'd need.

I'm deciding to use four orientations with four spatial shifts in conv2, and leaving conv1's other four channels unused since conv2 has no room for them. I'm also considering whether to fold those extra channels in, or to add an intensity-style feature alongside the oriented lines, but I'm leaning toward keeping the oriented lines alone since they already capture most of the ink.

I'm planning to hand-draw one stroke prototype per digit, compute each segment's orientation directly from its geometry, and paint those values into the 8x8 template cells, without running the network on them. I'm then starting on the linear classifier weights, comparing each class template against the others.

I'm weighing how to turn each class template into logits: normalizing the templates, subtracting the per-feature mean across classes so shared features don't dominate, and picking a global scale for the stroke responses that I'll tune from feedback.

I'm sketching hand-drawn stroke prototypes for each digit as point lists and reading their coordinates off the 4-to-23 digit box. I'm starting with the zero, one, and two shapes.

Still writing out the stroke coordinates for digits 3 through 5.

Still listing the stroke coordinates for digits 6 through 9, and I'm planning to sample each segment and spread its orientation into nearby template cells.

I'm setting each orientation's tuning to fall off with the angle difference, so a 22.5° offset gives about 0.7 and 45° gives nothing. Then each feature cell gets the stroke points whose rows fall within a couple of pixels of its center, with soft weights, since max-pooling means a stroke anywhere in the 4x4 region drives the full response.

I'm setting each template cell to the strongest response from any stroke point near it, scaled by how well that stroke's orientation matches the detector and how close the point sits to the cell's center. Full response within about two pixels, falling to zero by 3.5, mirrors how max-pooling lets a stroke anywhere in the region drive the cell.

I'm settling on fc weights as the template minus the mean across classes, so shared features cancel out. Then the logits look like nearest-centroid scoring, with each class's template dot-producted against the features and offset by half its squared norm.

I'm settling on a nearest-centroid score for each class: the template dotted with the features, minus half the template's squared norm, scaled by a global factor. Mean subtraction doesn't carry over cleanly into this form, so I'll stick with the plain version. I'm also keeping in mind that the rendered templates are fairly blurred compared with real features.

I'm reconsidering whether I can normalize the conv1 kernel by summing its weights over the stroke band, since that starts to look like running part of the network on an input. I'll sidestep it and set the normalization analytically from the kernel's profile instead.

I'm setting the conv1 bias to around -0.3 so weak or off-angle responses get suppressed, and scaling the filter so a matched stroke comes out near 1.0 after the bias.

I'm building the first-layer kernel as a zero-sum line detector, a Gaussian across the stroke times a window along it, with the mean removed. Then I'll set its normalization so a matched stroke gives a response near the target scale.

I'm settling the first-layer normalization by scaling the kernel so its positive weights sum to a fixed value, rather than measuring its response on a synthetic stroke, and I'll let later feedback tune the overall scale.

I'm estimating the filter's response by summing its weights across the rows and columns of the kernel, using a Gaussian profile over the stroke direction to get the row contributions before I normalize.

I'm checking the row sums of the kernel's center row, the ±1 rows, and the ±2 rows against each other, and the ±2 rows come out clearly negative.

I'm checking that the stroke response comes out near 2.9 with the full ink, and that the positive weights sum to about 3.0, so the normalization can be set as a simple rescale. For a 2-pixel stroke the response drops to about 2.55, which I'll average into the target. I'm scaling the kernel so its positive sum gives roughly 0.9 after a bias of -0.25, and leaving the rest for feedback to tune.

I'm checking the vertical stroke response on the horizontal detector: the center column comes out around 0.46 and the side columns around 0.2 each, so the total is roughly 0.85 against about 2.9 for a matched stroke. After normalization and the -0.25 bias that leaves about 0.12, which is low enough. I'm now turning to the scale of the fc weights.

Setting the fc weights to the template values scaled by s, with the bias set to minus half the squared template norm times s, so the logits come out as a nearest-centroid score. I'm keeping s at 1 for now.

I'm working out where each pooled cell's receptive field lands in the original image: the conv1 centers feeding each pool1 position, then how conv2 and pool2 shift those positions into the final 4x4 grid.

I'm working out how each 4x4 cell's template should respond to nearby stroke points, measuring how far each point sits from the cell's central band and how far the stroke runs from the detector's center.

I'm working out how far each template cell should respond to a stroke based on its distance from the cell's center, and I'm leaning toward a Gaussian falloff so the response drops off quickly with distance.

I'm settling the template's falloff with distance, going with a softer 1 − dist/2.5 since the templates should reflect the blur in real digit features. Then I'm weighing how orientation tuning should fall off, leaning toward a cosine-based response with a small floor so off-angle strokes still contribute a little.

I'm settling the orientation tuning as a cos² falloff, which gives about 0.5 at 45° off-angle and drops to zero at 90°. Then I'm laying out the four stroke directions as 0, 45, 90, and 135 degrees, using y-down coordinates so 45° points down-right.

Still writing the digit prototype definitions...

Still writing the digit prototype definitions...

Still writing out the digit stroke coordinates...

Still working out the digit stroke coordinates, checking whether each prototype's center of mass lands near the middle of the field the way MNIST-style digits do.

I'm now checking where the digit strokes' center of mass should sit, settling on about 13.8 in pixel index coordinates, and deciding that adjusting the hand-drawn templates geometrically is acceptable. I'm also noting that the cell grid covers centers from about 4 to 21 in each dimension, and I'm beginning to work out how the template is computed across that range.

Still writing the first-layer kernel code...

Still writing the render loop, stepping along each stroke segment and computing its angle.

Still writing out the template construction code...

Still writing the fc weight assignment code...
