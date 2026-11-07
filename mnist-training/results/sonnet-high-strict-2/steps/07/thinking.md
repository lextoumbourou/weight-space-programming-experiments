The template approach is hitting its limits, so the gains are small so far. Next I'm looking at stroke-orientation features to tell apart the digits that get confused, since coarse template matching alone seems capped around 60%. I'm also weighing whether hierarchical features would help, and I'm considering stroke-orientation templates drawn from the conv2 channels.

I'm weighing whether to use stroke-orientation channels from conv2 as features, since coarse template matching seems capped around 60%. The worry is that deriving orientation templates from my ink templates would amount to computing features directly rather than running the network, so I'm leaning against that. I'm turning instead to the mistakes themselves, starting with 1 being confused for 7.

I'm considering whether the 1 template needs a slanted band, since real 1s lean to the right and my vertical template is probably why 1 gets mistaken for 7. I'm also questioning whether the overall template approach can reach the accuracy I need, and checking whether my digit shapes, like the 0's width and height, match the typical MNIST proportions.

I'm checking the x-amplitude reasoning: a solid stroke gives around 0.8 at its center and falling toward 0.5 at the edges, so after ReLU and max-pooling the ink spreads about ±3px, roughly three to four cells wide on the 2px grid. That makes the 1-cell templates with blur still tolerable for the data, so I don't need sharper templates. I'm going to focus on improving the classifier itself instead.

I'm considering whether to reduce the ink sampler to four channels and use the freed channels for coarse orientation density maps on a 4x4 grid, then set the weights from what I know about each digit's typical orientation layout.

I'm weighing whether orientation features would actually separate the confusable digits like 1 and 7 or 4 and 9, but my guesses at those orientation maps could be off and I can only judge them by overall accuracy. My plan is to test them as a small-weight addition to the ink templates and drop them if accuracy falls, or else to spend the remaining steps tuning the ink templates against the confusion pairs.

I'm checking why the 7 template scores so poorly: its in-mask is just the top bar and a diagonal, so 7 images end up matching 9 and 5 instead. I'm also thinking the bias on class 1 might be too strong, so I'll try softening it to -0.8.

I'm checking the 7 template against how real 7s look: the stem should run down toward column 3 or 4 rather than sitting far left, so I'm planning to move its top-right start and shift the diagonal rightward.

I'm working out the stem's grid positions for the 7 template, mapping the typical MNIST coordinates onto my 2px cells, and it puts the stem around columns 3 to 4 at the bottom and column 7 at the top.

I'm checking where the 7's mass sits: since it's top-heavy, its bounding box should shift downward, so the bar would land lower than the center.

I'm thinking about whether to make the templates blurrier, so small misalignments matter less, or to add orientation channels as extra spatial features. Blurring the templates twice and subtracting the mean template is one option; sticking with the IoU approach is the other.

I'm considering drawing each digit as hand-described polyline strokes on the grid, which would give both the ink templates and per-segment orientation maps from one source without running the network on any input.

I'm working out how to build the orientation features from the hand-described polylines, mapping their directions onto the 4x4 coarse grid that conv2 pools down to, and figuring out which grid position each cell should sample.

I'm going to describe each digit as hand-drawn polyline strokes on the 9x9 grid, so the ink templates and the orientation maps both come from the same source. I'm starting with the 0.

Now I'm defining the 0 as an ellipse and the 1 as a slanted stroke with a small flag, then starting on the 2 as a top arc.

Still writing digit polylines...

Still writing digit polylines...

Still writing digit polylines...

Still writing digit polylines...

Still writing digit polylines...

Still writing digit polylines...

Now I'm working out how to build the orientation channels from the same grid. I'll sample each coarse cell from the fine orientation maps, averaging over a small neighborhood, and then decide whether to weight them by mean-subtracting across classes or by normalizing each channel separately, like the ink templates.

I'm deciding to keep the ASCII ink templates and their calibrated biases, and to add the orientation features from the polylines as a separate term. Since I'm mean-subtracting those features across classes, they should average out to zero per class and leave the bias alone, though I'll need to recheck that once they're in.

I'm settling the orientation weights at a scale of about 2.0, since the cell differences should land in the range of a few logits once summed across the grid.

I'm tallying the column totals of the confusion matrix to see which digits get over-predicted, starting with the 2, 5, and 8 columns.

I'm tallying the column totals of the confusion matrix to see which digits get over-predicted, and I'm noting that 8 is the biggest over-predicted column. I'm adjusting the biases to offset that: 8 goes down, 6 and 4 and 7 go up a bit to help their recall, and 1, 0, 2, and 3 get small corrections.

Still writing the polyline helpers...

Still writing the orientation and weight code...

Still writing the orientation helper code...
