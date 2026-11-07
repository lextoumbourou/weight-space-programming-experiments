Accuracy is at 43.6%, so I need to improve it. Class 5 is still a sink, and 6, 8 and 9 are doing poorly, so I'm working out what's causing that.

I'm weighing whether to keep tuning the hand-built templates or change the features themselves. The pooled 4x4 grid is the real bottleneck, so I'm considering a per-cell, per-channel design or stroke-type channels, though that's hard to tune by hand.

I'm considering richer templates that use orientation channels (vertical, horizontal, diagonal) at each cell, since diagonals would help distinguish 7, 2, 4 and 9. I'm also checking class 5, which is being predicted for 0, 6, 4, 8 and 9. Its top-row weight may be too generic, so I'm comparing it against 0 to see where the separation should come from.

I'm realizing the features are too blurred to detect holes: the blur and pooling spread ink from the ring into the center cells, so a 0 looks like a filled silhouette. I'm thinking about a less blurred channel or a center-on-surround detector at the right scale to pick up the hollow.

I'm weighing a conv2 redesign, where each channel would detect oriented strokes at a given position over the 5x5 receptive field, rather than tuning the hand-built templates further. The fixed 4x4 pooled grid still limits what fc can see, though.

I'm working out the receptive field of each final unit: roughly 18px, since the conv and pooling layers stack up, which explains why the features blur so much.

I'm sketching a conv2 hole detector: a unit centered over the digit's interior that fires when the ring of pooled conv1 cells around it has ink but the center does not, which should pick up the hollow in a 0 at roughly 6-8 px scale.

I'm sketching the hole feature as a ring-versus-center contrast: the score is the mean ink around the ring minus the mean ink in the center, so a 0 scores high while a 1 comes out negative. I'm also thinking about how 6, 8 and 9 would show loops at the top and bottom.

I'm settling on a conv2 redesign where one channel acts as a hole detector: it scores ink in a surrounding ring against the emptiness of the center. Swapping out the blob channel for it should separate 0, 6, 8, 9 and 4 better, and cut down the class 5 sink.

I'm settling the hole detector's weights: a ring of positive weight around the center, and a negative weight over the center itself, so a hollow digit gives a positive response while a solid stroke comes out near zero or negative.

I'm checking the hole detector's numbers: a stroke through the center scores about zero, while a 0's ring has far more ink than its center. The conv1 ink channel averages about 0.04 per pixel, so the pooled values are on a usable scale. Next I need to get this hole feature into the 4x4 grid cells.

Now I'm sketching the per-digit hole templates for the fc layer, with the hole feature marked on the interior cells that enclose a loop, starting with the 0.

I'm laying out the hole templates for the fc layer, marking the interior cells that sit inside each digit's loops, starting with the 0's center hole and moving on to the loops of 6 and 8.

I'm picking out the hole cells for each digit: the 0 gets a strong center hole, the 8 gets half-weight marks on its two loops, the 9 gets the top loop, and the 4 gets a small enclosed triangle at the top left.

I'm setting the hole template weights: the center cells get a small negative value for digits without a hole, and the 4 gets a half-weight mark at its enclosed top-left triangle. Next I'm turning to the orientation channels, starting with the vertical one for 1 and 4.

Still writing the orientation templates: vertical strokes for the sides of 0, 6 and 8, and the diagonal channel for 7 and 2.

Still writing the orientation templates: the '/' channel for 2 and 7, and checking which digits carry a '\' stroke.

I'm working out the zero-mean normalization for the hole channel, since the scale of the hole and orientation features differs from the ink features, so the per-digit scores stay comparable.

I'm deciding whether to zero-mean the hole and orientation templates the same way as the ink ones, so every channel measures contrast rather than raw mass. Sparse templates like the 1's vertical stroke still come out sensible after mean subtraction, so I'll apply it across all channels and scale each channel's weight separately.

I'm deciding whether to apply the zero-mean normalization uniformly across all channels, since the sparse orientation templates still look sensible after mean subtraction. I'm also considering whether to reduce the class 5 ink template's magnitude, since 5 keeps competing with 2 and 3.

Still writing the conv2 channel mapping: the hole detector on the ink channel goes in slot 4, with the blurred vertical, horizontal, and diagonal channels in the others.

Still writing the hole detector: a positive ring weight around the center and a negative center weight, so the output is high only where the ring has ink and the middle is empty.

Still working out the hole templates for the fc layer, with a positive weight on the digit's loop cells and a small negative baseline elsewhere.

Still writing the hole templates: the 0 gets its center cells marked, the 6 gets its bottom loop, and the 8 gets half-weight marks on both loops.

Still working out the hole templates: the digits with loops get positive weight on their enclosed cells, and the rest stay at zero before the mean subtraction.

Next I'm setting the hole templates for the digits without a loop: the center cells get a negative value so the hole feature pushes their scores down. After that I'll zero-mean the templates and check whether the hole channel's scale matches the ink channel.

Setting the vertical-stroke templates now: the 1 gets full weight down its center columns, while the 4 and 7 get stems in the right-hand columns, and the 0, 6 and 8 get their side strokes.

Still writing the slash-channel templates for 2 and 7, placing the diagonal weights on the cells where those strokes run.

Still writing the slash-channel templates: the '/' weights go on 7 and 2 along their diagonals, and 4 gets its left-hand diagonal too.

Still working out the orientation templates: the '/' channel gets weight on the diagonal cells of 4, 6, 2 and 7, and I'm leaving the '\' channel unused for now.

Still tuning the template weights: the horizontal channel gets a smaller multiplier, and I'm checking whether the top-row ink pattern is pushing class 5 and the other top-stroke digits too high after mean subtraction.

Next I'm softening the class 5 ink template, lowering its top-row weights to 0.5 so the top bar stops pulling the score toward 5 for digits like 7 and 2.

Still writing the feature-building code: looping over the ten digits and assembling each digit's ink, hole, vertical, horizontal and slash blocks with their weights.

Still writing the feature-building code: each digit's ink, hole, vertical, horizontal and slash blocks get zero-meaned, scaled, and flattened into the fc weights.

Still writing the conv2 channel mapping: the ring-and-center hole detector goes into slot 4, with the blurred channels filling the rest.

Now I'm wrapping up the conv2 changes: the ring-minus-centre hole detector goes on the ink channel, and I'm softening the class 5 template since its top bar is what keeps pulling it up.
