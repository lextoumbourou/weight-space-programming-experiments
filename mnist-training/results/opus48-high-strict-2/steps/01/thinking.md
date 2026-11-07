I'm setting out to build a small CNN for MNIST with hand-picked weights, and I'm laying out its architecture: a 5x5 convolution from 1 to 8 channels, a ReLU, and a 2x2 max pool, then a second 5x5 convolution from 8 to 16 channels, another ReLU and pool, ending at a 4x4 feature map.

I'm weighing a strategy: keep conv1 close to an ink-summing filter so the final 4x4 features act as a coarse ink map, then let the fc layer serve as a template matcher, though I doubt 4x4 resolution will be enough to separate digits well.

I'm working out the receptive field now: two 5x5 convolutions and two 2x2 poolings, so each of the 4x4 output positions covers a fairly large patch of the original 28x28 image. I'm leaning toward making conv1 a single positive averaging filter, so that the pooled channel acts as a local ink-density map feeding the template-matching step.

I'm now settling on conv1 as a single channel that sums ink, and I'm noting that the other channels will stay zero. For conv2, I'm considering letting channel 0 feed a 5x5 ink-summing filter, but I see that if all 16 channels are identical the 4x4 map is redundant, so I want the channels to differ somehow.

I'm now weighing whether the other conv2 channels can differ at all, since the only informative input is conv1's single ink channel and the spatial resolution at the fc layer is just the 4x4 grid. I suspect that with 16 channels all being ink density, the fc input is effectively a 16-value coarse ink map, which may be enough to tell some digits apart.

I'm thinking about whether finer detail could come from conv1 channels that pick out oriented strokes, though pooling fixes the final grid at 4x4 regardless. I'm estimating that template matching on that grid might land around 40-60% accuracy, and I'll lean on the feedback loop to refine the weights from there.

I'm settling on a design with 256 features coming out of the conv stack, and I'm leaning toward having the fc layer act as a linear classifier with hand-set template weights, using the feedback loop to tune its bias and scaling. I'm also considering whether conv1 channels could carry finer spatial detail, like thin horizontal bands, though I'm not sure yet how to make that work.

I'm sketching out the conv stack in terms of what each layer should represent: the first layer as an ink-density extractor, and the fc layer as a template matcher over the 4x4 grid. To keep the 16 channels from being redundant, I'm considering giving conv1 some edge-style filters alongside the plain ink channel, with a few more channels for corners or centers.

I'm settling on a simple first step: conv1 becomes a single ink-averaging filter with the other channels zeroed, and all the conv2 channels act as ink sums too, so the fc layer gets a 4x4 ink map repeated across channels.

I'm now sketching out the 4x4 digit templates, planning to write coarse ink patterns for each digit row by row. I also want to pin down which 4x4 cell lines up with which region of the original image, since the pooling steps shift the mapping.

I'm tracing how each 4x4 output cell maps back to input rows: the pooling and conv windows put each final cell's coverage at roughly rows 4r to 4r+15 of the original image, so the grid is coarse and overlapping.

I'm pinning down the receptive field of each 4x4 cell, which works out to roughly 16 pixels per cell with large overlap between neighbors. That blurs the map, so fine digit templates will be hard to build by hand.

I'm fixing conv1 as a single ink-averaging filter with the other channels zeroed, and I'm about to set conv2's weights so that each of its channels also sums ink from that first channel.

Still writing the conv2 setup and the fc template weights...

I'm now working out the 4x4 digit templates, starting with the zero, which should be bright along the outer edge and dim in the center. Since the ink map is so blurred, I'm assuming each template should be positive where a digit has ink and negative where it doesn't, so the score tracks correlation rather than just total ink.

I'm sketching the rough digit shapes on the 4x4 grid: the zero should be heavy on the border with a dim center, the one should sit in the middle columns, and the rest I'll sort out by feel and tune with feedback.

Now I'm sketching the 4x4 ink patterns for the digits, starting with zero as a bright outer ring and an empty center, then trying a narrow middle-column shape for one and a top-bar-plus-lower-part pattern for two.

Still writing the 4x4 ink templates for digits 6 through 8...

Still working out the 4x4 ink templates for digits 8 and 9, sketching each as a row-by-row pattern before centering them.

I'm worried the blurred 4x4 map will flatten the template scores, since every cell sees most of the digit and the contrast between cells is low. I'm wondering whether that will sink accuracy no matter how carefully I tune the templates.

I'm now going with the ink-template route, since the blurred 4x4 map makes edge-style filters hard to get right by hand. I'm setting conv1 and conv2 to ink averages, then scaling the templates so the logits land in a reasonable range.

I'm settling on a gain G of around 10 to 20 to scale the centered templates, since the raw ink differences are small. With that, each logit should land at a few units of spread, which is about the right range for the loss.

Still settling on the 4x4 digit templates, planning to center each ink grid and scale it with a gain so the logits spread enough for the loss.

Still writing the 4x4 ink templates for digits 5 onward...

Still writing the 4x4 ink templates for digits 8 and 9...

Still writing the 4x4 ink template for digit 8, which keeps coming out identical to the zero template, so I'm trying a different pinch pattern.

I'm settling on a solid 4x4 pattern for 8, but it's barely different from the zero template, and the 4x4 grid can't really show a middle bar, so I'm weighing whether giving 8 more center ink is enough to tell them apart.

Still writing the 4x4 template grids for digits 8 and 9, with 8 as a solid block and 9 as a hollow top with a bottom-right stroke...

Still working out the scaling for the templates, planning to tune the gain so the logits spread enough for the loss.

Still working out the scaling, with the conv weights at 1/25 and the gain on the fc layer set high enough to spread the logits.

Still writing the weight setup for the CNN, with conv1 set as an ink-averaging channel and the final gain G around 20 to spread the logits.

Still writing the conv weight setup and the 4x4 digit template grids...

Still writing the digit templates as 4x4 ink grids...

Still writing the digit template grids and centering each one before setting the fc weights...

Still writing the fc weight loop, flattening each template across the 16 channels and scaling it by the gain.
