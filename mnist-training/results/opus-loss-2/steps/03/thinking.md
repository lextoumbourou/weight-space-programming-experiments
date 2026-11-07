Checking which digit pairs still get confused after the latest adjustment, and looking at whether pure template correlation is enough or whether I should tune the templates with feedback. A pairwise approach, boosting one class's logit where its template beats the other's, might help separate pairs like 4 and 9.

I'm now asking why the 0 gets mistaken for a 2, and I'm considering a wider and taller 0 template with a slanted variant. The 0's center is empty while a 2 has a diagonal stroke there, so the real issue may be how the template scores overlap with the features shared by both digits.

I'm weighing a distance-style bias, where each class logit subtracts a penalty scaled by its template's squared norm, since the raw correlation doesn't normalize the input. That would depend on the scale of the features, which I don't know. Another option is per-class bias adjustments drawn from the confusion matrix, comparing the predicted column sums against the expected true counts.

Now I'm working out per-class bias corrections from the confusion matrix, comparing predicted column totals against the expected true counts, with 4 needing the largest upward push. I'm also looking at a structural cue for the 4 and 9 pair: a 9 has a closed top stroke near the top edge, while a 4 has an open top and a crossbar that extends left of the stem.

I'm comparing which digit pairs get mixed up, such as 5 and 6, where a closed left side versus an open bowl separates them. For the 1 and 7 pair, the top horizontal stroke is the key cue. I'm also considering whether to weight each class by the difference between its template and the other's, so the discriminative features get more weight.

I'm weighing whether a distance-style bias, one that penalizes each class by the squared norm of its template, would fix the mismatch in feature magnitudes, since thick strokes with a lot of ink push up every template's response.

I'm now considering making each class's weight vector zero-sum across the spatial positions for each orientation channel, so that a generally inkier image doesn't favor digits like 8 or 0 just because their templates spread across more features.

Zero-summing each class's weight vector over all 256 features should keep a generally inkier image from favoring digits like 8 or 0. I'm also planning a wider 0 template with a rotated-ellipse variant and a top bar for the 5 that runs further right, though I'm not yet sure how the 6 arc fits into that.

I'm looking at 5 and 6, which share a similar coarse shape, and I think the top bar is what separates them. Adding an explicit pairwise term that pushes each template away from the other for confused pairs like this one might help.

I'm going to add a pairwise term for the confused pairs, nudging each template away from its partner by an amount tied to how often they get mixed up. The pairs include 4/9, 5/6, 1/7, and several others, all at a weight of 0.5. I'm worried the differences could emphasize the wrong features if the templates are inaccurate, so I'll need to test it.

I'm going to make each class's weight vector zero-sum, add a rotated-ellipse variant for the 0, and apply a pairwise push between the confused pairs, but I'll hold off on the bias correction since the other changes would throw it off.

I'm checking how the rotation sign works for a slanted 0: a positive angle should push the top of the ellipse to the right. I'm also noting that 1s often lean the other way, so I'll consider templates in both slant directions.
