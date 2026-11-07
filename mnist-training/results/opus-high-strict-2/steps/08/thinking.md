Accuracy has stalled around 68%, which suggests the features themselves may be the bottleneck. I'm checking whether max pooling over the line detectors makes thick strokes fire every orientation, starting with the horizontal detector's response to a width-4 vertical stroke.

I'm checking the horizontal detector against a thick vertical stroke and finding it gives zero response, since its columns sum to zero, so it stays selective to vertical lines. Then I'm puzzling over why certain digits like 6, 4, and 8 keep getting classified as 1, and whether weak features are pushing scores toward the class biases.

I'm reasoning about why the classifier leans toward "1": the penalty term for each class scales with its template's mean, so heavy-ink images get pushed toward class 1 and away from 8. A uniform penalty would fix that, but it reintroduces the earlier bias toward 8. The cleaner route is a proper linear discriminant with features scaled to template size, so ink amount doesn't shift the scores unevenly.

I'm working out that Pearson scaling by γ multiplies every logit equally, so the argmax only shifts through the biases, and any ink effect comes from how spread out the ink is rather than its total amount. That makes the penalty on spread-out strokes a built-in property of the method, and I'm wondering whether the features are the real limit instead.

I'm wondering whether the 4-orientation features with max pooling are losing too much fine detail, though HOG-style binning seems to work. I'm also checking whether the conv1 bias is reasonable against the output range, and it looks fine. The remaining idea is to treat the template's negative regions as explicit "should be empty" areas taken from the other classes, rather than applying one uniform negative weight everywhere.

I'm considering whether a combined template that subtracts the strongest competing digit could separate classes better, but a plain mean subtraction cancels out, so the real difference comes from the pairwise gaps, which look messy to compute. Coarser features that are more tolerant of stroke position might give a bigger gain than tuning the templates further.

I'm checking the sign convention on the "/" orientation kernel: for direction (s2, -s2), the response works out to -(u+v)s2, which is zero when the offsets are opposite, so the stroke direction lines up as expected.

I'm checking the orientation conventions against the grid mapping and the PyTorch weight layout, and they all line up. The arc angle convention and the kernel indexing look consistent too, so I'm not finding a bug there. That leaves the center offset c1=2.5 as the thing I still need to look at.

I'm weighing whether per-class temperature scaling could help, since Pearson correlations tend to run lower for complex digits and that may skew the argmax toward simpler templates like 1, even with the biases already compensating.

I'm comparing the confusion counts for 3 and 5: both classes are predicted about equally often, so the bias isn't the cause and it has to come from the template shapes. Real 3s put their upper curve on the right side around columns 8-18, while real 5s have a vertical stroke on the left near column 10 with a top bar running right from there.

I'm comparing where real 3s and 5s put their strokes, and the upper curve of a 3 sits on the right while a 5 has its vertical on the left. The lower bowls look alike, so the orientation features may be picking up the same signal for both. I'm considering weighting features by how much they separate classes, though any scaling shared across all classes would cancel out.

I'm weighting each feature by the spread of its values across the digit templates, so features that differ between classes count for more in the scores.

I'm considering a diagonal discriminant-style weighting: for each feature, use the class deviation from the overall template mean, scaled by an estimate of within-class variance taken from the template probabilities, so the weights come from a formula on my drawn templates rather than from data.

I'm ruling out discriminant analysis here, since fitting class statistics to synthetic data I generated myself is off limits. Instead I'm considering hand-placed negative zones per digit pair: for 3 vs 5, penalize the left vertical where a 5 would sit, and for 5 vs 3, penalize the upper-right arc.

I'm sketching anti-stroke templates for each digit: strokes placed where competing digits have ink, so their contribution is subtracted from the template. For the 3, that means a negative line along the left vertical where a 5 would sit.

I'm adding anti-stroke templates for the 0 and 5 classes that place negative ink where competing digits draw their strokes.

I'm adding anti-stroke templates for 0 and 9: a horizontal bar through the center for 0, where 6 and 9 put their loop crossings, and a lower-left line for 9, where 0 and 8 draw their bowl.

Next I'm sketching anti-stroke templates for the remaining digits: a short bottom segment for 8 would overlap its own loop, so I'm skipping that one, and for 4 I'm considering a negative top bar where 9's loop sits.

I'm adding anti-stroke templates for the 1 and 7 classes: short horizontal segments left and right of the stem for 1, where 4 and 7 draw their strokes, and a left-side stroke near the top of the loop for 7 to separate it from 9 and 3.

I'm adding anti-stroke templates for the 2 and 5 classes: a right-lower arc for 2 where 3's curve sits, and a left-side segment in 5's bowl gap near rows 15-19. For 6 I'm also placing a horizontal bar across the top where 5's top stroke runs.

I'm settling on the anti-stroke approach: negative strokes placed where competing digits draw ink, weighted at about 0.7. I'll also halve the new bias increment, since the prediction counts show the changes would shift things a lot.
