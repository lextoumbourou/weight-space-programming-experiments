The loss has dropped to 1.90 and accuracy is up to 32.9%, so the multiplicity fix clearly helped. Class 8 still pulls in a lot of predictions, and class 4 still attracts some, so I'm going to look at the diagonal and the column for class 8.

I'm checking the class 8 column, where 3→8 and 5→8 look like the biggest pulls. The 8 template is probably too heavy across the center, so it overlaps with many digits. Since its recall is already good, I'll focus on tuning its strength and the 9→4 and 7→4 leakage rather than rebuilding everything.

I'm tallying the per-class prediction counts, and class 8 is far over-predicted at about 3336 against roughly 1000 true instances. Classes 1 and 4 are also high, while 5, 3, 2, 0 and 6 are under-predicted. So I'm considering a bias that pulls down 8, 1 and 4 and lifts the rarer classes.

I'm weighing a bias adjustment to pull down the over-predicted classes, starting with 8, and nudge up the under-predicted ones. Working from the per-class prediction counts, I'm estimating each bias as roughly the negative log of how far each class's count sits from about 1000.

I'm estimating a per-class bias as the negative scaled log of each class's predicted count relative to about 1000, which pushes down the over-predicted 8 and lifts the rare 5 and 3. I'll use a moderate scale of 0.6 to avoid overcorrecting.

I'm setting the per-class biases now, using the scaled-log correction on the over- and under-predicted counts. I'm also considering whether to sharpen the scale, but with loss at 1.9 I'll hold it at 2, and I want to improve the 5 template, which is currently very weak.

I'm turning the per-class biases into a fixed array, nudging up the rare classes 5, 3 and 2 and pulling down the over-predicted 8 and 1, with a conservative scale so I don't overcorrect.

I'm settling on a moderate bias strength of 0.6 for the per-class offsets, so the rebalancing corrects the over-predicted classes without overshooting, and I'm keeping everything else unchanged for this step.
