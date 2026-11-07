I'm at 60% and need bigger jumps. The main confusions are 0, 7, and 1 being pulled toward 2, 2 toward 8, 9 toward 8, and 4 and 7 toward 9. The 2 template seems to draw in digits with its broad top arc, diagonal, and base, and the 8 template pulls in 9, 5, and 2. I'm considering subtracting the mean template across classes from each norm to make the weighting more discriminative.

I'm weighing whether subtracting the average template from each class template would change anything, and concluding it wouldn't, since a shared offset cancels in the ranking. Per-class biases could still rebalance things, nudging the 2 and 8 scores down. I'm also doubting the features themselves, wondering whether the conv1 channels are good enough or whether a coarser HOG or ink-density features would separate the digits better. My templates may not match the real digit geometry either, since MNIST digits are size-normalized into a 20x20 box.

I'm checking the distinguishing features for each confused pair: the 8's lower loop versus the 9's straight stem, the 4's open top versus the 9's closed top stroke, and the 2's base and diagonal against the 7 and 0. I'm then looking at whether a penalty for expected-empty regions, scaled by how much ink each class typically puts there, could separate them.

I'm considering a penalty on ink where a template expects none, which would differ by class and so wouldn't cancel. The earlier distance formulation only had the dot product and norm terms, so it didn't include that per-feature penalty. Looking at the 2 template, its top arc is shared with several digits and its diagonal with 7, so a penalty on unexpected ink could push 0 down relative to 2.

I'm settling on a penalty term that subtracts, for each class, the mean template weighted by how empty that class's template is in each region, so ink where a class expects none pushes its score down. I'll set λ around 0.5, and since it's linear and argmax is unaffected by scale, the ranking stays valid.

I'm checking whether the 9 stem versus the 8's lower loop helps here: a 9 lacks the lower-left ink the 8 template expects, which is missing ink rather than unexpected ink, so the penalty term won't catch it directly and cosine normalization only partly covers it.

I'm picturing the 9's stem as slanted, running down and slightly left from the loop, rather than straight and vertical, and I'm guessing the 4s are slanted too. Since MNIST digits generally lean to the right, I'm thinking about applying a global shear to every template.

Shifting the templates by a slant to match how MNIST digits lean, so the 9's stem and the 4's strokes line up better. I'm holding off on mixing several shear variants into one template, since that would just be averaging generated samples, and I'll keep to a single drawn shear and rely on blur instead.

I'm checking the 4 template's open top and right stroke, and I suspect the 0 ellipse is too narrow, since real MNIST zeros look wider, so I'm trying rx around 7.5 and ry around 9.5 with the same slant. The 7 template's top bar and diagonal also look like they could be pulling in the 2s.

I'm checking whether the 2 template's expected-empty region overlaps with the 7's diagonal, since the 7 stroke sits to the right of the 2's diagonal. The penalty only sees unexpected ink, so the 2's missing base for a 7 gets handled by normalization instead.

I'm checking whether the 1 being pulled toward 2 comes from orientation: the 1's vertical stroke sits in the center, where the 2 template has no vertical ink, so I'm considering broadening the orientation tuning to reduce that mismatch.

I'm adding a per-class penalty for ink where a template expects none, with λ around 0.6, and since the ranking is scale-invariant this stays valid. I'm also planning a global shear of about 0.12 across the templates and adjusting the 0 ellipse to rx 7, ry 9.5.

I'm reworking the templates here: nudging the 0 ellipse wider, pulling the 9's stem down-left, slanting the 4 and 7 strokes, and applying a shared shear so they lean like real MNIST digits. I'm also setting up the penalty term, which subtracts the mean template weighted by how empty each class's template is in each region.

I'm setting the penalty's scale against the mean template, with λ at 0.6.
