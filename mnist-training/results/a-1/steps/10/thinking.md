I'm noticing the accuracy is climbing while the loss goes up too, which might mean the model is getting overconfident on its mistakes. Since loss is what gets scored, I need to focus on that, and the current approaches are stuck around 55 to 58 percent. I'm wondering whether a simpler handcrafted feature set, using downsampled raw pixels and drawn templates, would hold up better, though the confusions between 7, 8, and 9 still look like a problem. I also want to check whether some component of the pipeline might be broken.

I'm checking why the 1s get labeled as 7s, since a real 1 is basically a single stroke and the 7 template's slanted stem could be pulling it in. Looking at the shear and orientation math, the 7-template's response seems to dominate on slanted 1s. I'm also suspecting the feature set itself may be dominated by noise, and I'm considering a simpler approach using local ink density on a fine grid instead of orientation features.

I'm weighing whether to design hand-built structural features for the confused pairs, like checking for ink at the bottom-left to separate 8 from 9 and 6 from 5. That approach feels like it could get complicated fast, so I'm still deciding whether it's worth the effort.

I'm comparing the confusable digit pairs, reasoning that the shared strokes in the templates may be swamping the discriminative ones. I'm also considering whether centering the templates across classes, now that each channel is zero-sum, could fix the bias toward 8 that the earlier attempt ran into.

I'm realizing that subtracting a shared mean across classes changes nothing about which class wins, so centering alone can't fix the confusions; only the template shapes and per-class scale or bias actually matter. That points to the real limit being one linear template per class, which is why I'm wondering whether downweighting high-variance regions, a rough stand-in for LDA's covariance whitening, would help more than tweaking the orientation pooling.

I'm thinking about adjusting per-class biases directly from the confusion matrix, since the columns show 8 and 2 are badly under-predicted while 9 and 7 are over-predicted. Pushing the biases up for 8, 2, and 4 and down for 9 and 7 looks like a quick win, and I'm just trying to settle how big those shifts should be relative to the logit scale.

I'm weighing a redesign of the 8 template, since my two circles may not match how real 8s are drawn. I'm thinking of tracing it as one continuous stroke instead, with a smaller top loop and a crossing in the middle.

I'm checking the 8 template's crossing at the center, where the two diagonals meet, and comparing their slopes to see how it should look. Then I'm considering the 2, whose diagonal stroke runs close to the 7's stem, so its bottom bar is what should tell them apart.

I'm planning to try drawing several variants per digit and averaging them, since a single template may not capture how varied real handwriting is. I'm also thinking about shifting the per-class biases to counter the confusion-matrix imbalance, and lowering the scale to tame the loss.

Still drafting the stroke variants for digit 2, sketching out a looped version and a Z-shaped one alongside the original.

I'm drafting more stroke variants for the 4, 5, and 6, sketching a second and third shape for each alongside the originals.

Still drafting digit variants, adding a looped 6, a few 7 versions, and a crossing-stroke 8 alongside the 9 template.

Continuing the stroke variants for each digit, I'm averaging the features across them and shearing, and I'll wait to see how the variants alone change things before adding any bias.
