The score came in at 0.8041, still short of the 0.8014 target, so I have two steps to get below it and step 14 has to be a real gain. I'm looking for a structural change rather than a tweak, and I'm considering class-specific discriminative weighting as one option. The largest confusion is between classes 7 and 9.

I'm checking which confusion pairs matter most: 1→2 at 98 errors, with 2→8, 3→8, and 2→3 also large. For the 1s, my template is narrow and most real 1s are more slanted than it allows, so one option is adding a more-slanted variant to the template, though that's still just an idea.

I'm weighing a metric that down-weights the shared ink direction, so thick and thin digits don't get scored so differently. I'm working through how the bias terms shift under that change and whether they can be pre-compensated.

I'm working out how the shared-direction correction shifts each class's constant term when the features are typical. Assuming they roughly match the average template, I'm trying to pick a bias compensation that makes the class shifts cancel out, since earlier attempts failed on class-level bias errors.

I'm finishing the compensation: subtracting the template's mean-projection times the sample's deviation from typical ink, so average-ink samples stay unchanged while heavy-ink ones get penalized toward large templates. I still need a good estimate for the typical projection c, and I'm considering the mean of the templates' projections onto u as that estimate.

I'm checking whether scaling down the shared ink direction would help, but on reflection the errors may come from stroke structure rather than total ink, since thick and thin strokes produce similar edge features. The bigger lever looks like the templates themselves, especially the 7 and 9 pair, which is the largest confusion, so I'm turning to how their shapes differ.

I'm considering whether the 7 and 9 confusion can be addressed through the bins that actually separate them: the left side of the 9's loop and its bottom horizontal edge. If a 7 lacks those features, its distance to the 9 template grows only by the 9's squared values in those few bins, so the boost would need to be targeted at that pair rather than applied globally.

I'm considering a pairwise metric that adds weight along the direction separating each confusing pair of classes, so that the score emphasizes the features where they differ. I'm working out how that metric would reshape each class's score in the nearest-centroid setup.

I'm wondering whether a metric change would actually help here, since if within-class noise is roughly isotropic, reweighting directions wouldn't gain much. The real bottleneck looks more like the templates not matching the true class means, so I'm turning to compare each digit's template against typical MNIST average shapes, starting with the 0.

I'm going back over the digit templates against the typical MNIST average shapes, and the 0 is already done. For the 1, 2, 3, 7, 8 and 9 I'm noting the rough geometry of their mean strokes: the 1's slight slant, the 2's wide bottom bar, the 7's top bar and diagonal stem, and the 9's loop and stem. I'm also checking how my row mapping (row = 14 + 10y) places those features.

Next I'm weighing whether to sharpen the orientation tuning from power 3 to 6, since the 5x5 kernels make the templates broad, though I'm not sure that trade-off is worth it. Rather than tuning bias or power, the bigger expected gain looks like the 7→9 confusion, which accounts for the most errors. I'm also considering a small change to the temperature T from its current estimate of 1.81, but the bias tweaks may give only minor improvements, so any change needs to clear the roughly 0.35% gap.

I'm weighing a targeted pairwise term for the 7-versus-9 confusion, using the difference between their templates as the direction, and keeping its strength small so the midpoint stays neutral. I'm not sure a change this narrow will clear the roughly 0.35% gap, so I'm treating it as one candidate among a few.

I'm testing whether a pairwise boost along the 7-versus-9 direction, centered at their midpoint, would change anything. My worry is that it only rescales the same discriminant, so it may not shift which side of the midpoint a sample lands on, unless the biases are set differently.

I'm seeing that a pairwise decision between 7 and 9 is linear along their template difference, so reweighting that direction alone won't change anything; I'd need better templates or a different metric. The features that separate them are the loop's left side and bottom versus the 7's top bar, and I'm weighing whether template edits to those areas could reduce the 7→9 errors.

I'm looking at the 7-versus-9 confusion from the template side: a 7 lacking the 9's left loop edges and bottom would only shift its distance by a few bins. The 9's loop top is horizontal like the 7's bar, so the discriminating features are really the left side of the loop and the stem's direction, and I'm checking whether a template change could capture that.

I'm weighing whether downweighting the shared ink direction would help, since the 2→8 and 3→8 errors seem tied to how much ink a digit has. Heavy-ink 2s and small 8s may be drifting toward each other, so a metric that compensates for total ink could reduce those specific confusions.

I'm now thinking the ink-normalization idea might work, since many of the confusions look like lighter digits being pulled toward heavier ones, like 7→9 and 1→2. I'm starting to write out the deviation form of the score, where each class's score is adjusted by a term tied to its projection on the shared ink direction, and I'm checking how the mean of that projection should be centered.

I'm considering an ink-normalization fix: subtract a term along the mean-template direction u, scaled by each class's projection on u, so that the heavy-ink bias behind confusions like 7→9 and 1→2 gets partially removed. I'm settling on α=0.6 for the strength and centering the adjustment with the mean projection across classes, and I'm noting that the 144-dim bin features need to be handled before this applies.

I'm building the per-bin weights from the mean-template direction, subtracting a scaled projection of each class's template onto it, and I'm going with α=0.5 since the risk of this step not improving is real but it's my best option.
