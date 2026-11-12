I'm at 59% baseline, so I need to improve. The predictions lean heavily toward class 2, and 7 gets confused with 9 and 2, while 3 gets confused with 5. A template approach without data only goes so far, so I'm thinking about tuning per-class biases using feedback. The predicted-class totals are lopsided, with 2 far above the rest.

I'm weighing a change from cosine templates to feature normalization, and wondering whether the blurred max-pool features are too diffuse to discriminate well. I also want to correct for the mean-subtraction effect, where classes with heavy template mass in common features win too easily. Since estimating that average feature vector is hard without knowing its scale, I'm considering simply adjusting the biases empirically, lowering the one for 2 and raising those for 7, 8, and 3. I'm now working through a bias update based on the ratio of predicted to true counts per class.

I'm working through the per-class column totals against the true counts, computing log ratios for each class. Class 2 comes out far above the others at about 0.76, while 5 is at roughly 0.45 and 3 and 4 sit below zero.

I'm working out bias corrections from the log ratios of predicted to true counts, with the strongest offsets for classes 2 and 7. I'm also weighing whether to change the features alongside the biases, though that would make it harder to tell which change helped. Class 2 is over-predicted, pulling in digits like 0, 7, 8 and 3, so the templates for that class may be too broad.

I'm considering a nearest-centroid style classifier that scores each class by distance to a mean feature vector, which splits into a dot-product term and a norm term. Without normalized templates the norm term varies by class, so I'd add a tunable scale factor on the template to adjust it.

Now I'm weighing whether finer spatial resolution could help, perhaps by giving different channels shifted copies of the same orientation features so that cell coverage is offset by one pooled cell. That might recover some of the within-cell position the max pooling discards, though the template quality itself still seems to be the main limit.

I'm weighing a larger change to the features, and I'm thinking about adding a shifted copy of the orientation channels so cell coverage moves by one pooled cell and recovers some of the position that max pooling discards. For now, though, I'm going to apply a simple bias correction, one step at a time, to see how much it moves the accuracy.

Setting the bias update factor to 1.0 times the log ratios.
