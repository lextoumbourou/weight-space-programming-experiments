I'm at about 70% accuracy with a loss of 0.93, so the model still needs structural work. Many of the errors are 4s being read as 9s, especially where the top is closed or narrow. To tell them apart, I'm checking whether the 4's middle bar sticks out past the stem while the 9's loop bottom stays within it.

I'm settling on whether a horizontal stroke at the top row separates the two digits, since the 9 has one while the 4's top stays open. The template comparison is muddier, because the 4's template shows a mix of both. I'm also weighing whether finer spatial resolution in the orientation features would help, given how much these top-closed versus open distinctions depend on exact positions.

I'm weighing whether to draw more style variants per class, since the templates may be averaging over too little slant and width variation. I'm also questioning whether the zero-sum normalization with cosine scoring is the right approach for these max-pooled features, and I'm thinking about testing template changes one at a time.

I'm now considering a larger open-4 template with the left arm angled slightly and the bar at the middle, and I'm wondering whether the hole detector might be firing on some 4s by mistake.

I'm weighing whether to check the struct channel firing rates directly, since I'm mostly guessing at whether the hole detector or the U detector is misfiring on the 4s and 9s. I'm also considering adding a top-closure channel that marks the 9's inner top bar, but I'm not sure the 4 template should carry a matching negative.

I'm thinking about checking the hole and U channels by reading the confusion matrix instead of loss: if I set one logit to a feature sum minus a threshold and leave the rest at zero, the predicted class tells me, per digit, how often that feature fires above the threshold.

I'm working out how to read the confusion matrix more directly: if each logit is a scaled feature minus a threshold, the argmax partitions the feature's range into bands, one per class.

I'm thinking that the logit trick could work as a diagnostic: with each class getting a line of slope k and an offset chosen so it wins over one interval of a scalar feature, one run yields a per-class histogram of that feature. That would let me check a candidate discriminant directly before changing any weights. The open question is whether a single scalar at a time is efficient enough, or whether I could read two features at once through a 2D partition.

I'm noting that the logits could be made separable in two scalar features, so each axis gets its own convex partition and the joint argmax yields a 3x3 grid. That would let nine classes encode a joint histogram of two features in one run, with one class left unused.

I'm considering whether the per-class histogram trick could also yield means, but reading out 256 features that way would take 256 steps, which is too many. A better target is a few compressed quantities, such as the hole channel summed over the top and bottom halves, which a single step could bin into a 3x3 joint histogram per class. That should show which features actually separate the 4s and 9s.

I'm thinking that knowing each class's hit rate for the hole channel in the top and bottom halves would let me set the weights from log-odds, in a Naive Bayes style, instead of guessing them.

I'm planning a few diagnostic steps that read two aggregated hole-channel sums at once, one for the top rows and one for the bottom, binned at low and high thresholds, so I can see how each class's values spread before setting any weights.

I'm weighing whether a few diagnostic steps are worth the budget, since there are 39 left and the struct features may turn out unreliable anyway. I'm also considering whether a 3x3 joint histogram of two aggregated features would carry more information per step than a single 10-bin scalar, and I'm working out how to build that grid separably with the logits.

I'm building the pooled logit so each class's score is a separable function of two aggregated features, with bins set by thresholds and a large scale to keep the partitions sharp.

I'm weighing a few diagnostic steps to measure the hole and U-shape channels, both top and bottom, and the closure channels, since the struct features may be what separates the 4s and 9s. Each measurement would be a scalar sum over a region, so I'd need roughly four steps to cover the eight or so features I care about. Then I'd combine them Naive Bayes style with the orientation templates, though the balance between the two is still unclear.

I'm setting the thresholds at 0.02 for any firing and 0.5 for a strong one. For step 12, I'll sum the hole channel over the top two rows and the bottom two rows, then bin each sum and map the pair of bins to a class index as 3 times the first bin plus the second.
