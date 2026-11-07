Accuracy is at 41.6%, which is marginal, and bias tuning has stopped giving much. Some confusions dropped, like 1→7 down to 306 from 505, but 1→2 appeared at 114, and recall for 7 and 8 fell. I'm starting to think the core templates are what's holding us back.

I'm weighing whether the feature pipeline itself is the limit, since the pass-through conv layers and coarse 12x12 features cap accuracy around 40-45%. The biggest problem is 9s getting classified as 4s (558 cases), with 8s going to 2s and 7s scattered across several classes. I'm considering whether thickening the templates to look more like real MNIST strokes would help, though the payoff from hand-tuning them is uncertain.

I'm comparing the 4 and 9 templates now, looking at how the 4 has a full-width bar and a long vertical stem while the 9 has a loop at the top. That structural difference is what I need to exploit to separate them.

I'm comparing the 9 and 4 templates, noting that the 9's loop-bottom stroke overlaps the 4's full-width bar, which may be why 9s keep getting pulled toward 4. The 4 template also carries a lot of ink overall, so it may be attracting predictions too broadly.

I'm recomputing the column totals and noticing the 4 template is over-predicting, with about 1349 hits, so I'll reduce its bias.

Column totals are off: the sum comes to over 10,000, so I'm probably miscounting somewhere. Still, the picture is clear enough. Class 1 is over-predicted at about 1601, class 4 at about 1498 even after its bias cut, while 7 is far under at 453 and 8 and 9 are low too. My bias changes likely overshot on 1, which explains the new 1→2 leak.

I'm recalculating the column totals for each class to see which ones are over- or under-predicted, and I'll adjust the biases from there in smaller steps so I stop swinging between 1 and 7.

Now I'm tallying the per-class column totals from the confusion matrix, starting with class 0.

Tallying the per-column totals now, which puts class 1 at about 1601 and class 4 at about 1498, both over-predicted, while 7 sits low at 453.

Checking the column totals, the sums come to about 10,123 instead of 10,000, so there's an arithmetic slip somewhere. Re-adding each column individually, the counts for classes 1 and 4 still look over-predicted.

Now I'm checking the row sums, which come out close to 1000 each, and the total is about 10,123, a small error I can live with. I'm computing the bias deltas from each column's log-ratio against 1000, starting with class 0 at about -0.015 and class 1 at about -0.165.

Now I'm recomputing the bias for each class by applying the gain to the log-ratio of its column total, which gives class 0 a small cut and class 7 a sizeable boost.

I'm recomputing the bias for each class from its column total, which gives the 7 class a boost back to about +0.18. Bias tuning seems to plateau near 41%, so I'll try improving the templates themselves to better separate the confused digits.

I'm listing the distinguishing features of each digit at this coarse resolution: 0 as a ring with an empty center, 1 as a vertical stroke, and 4 with its stem, bar, and diagonal. I'm also noting that 3, 5, and 8 and the pairs 4/9 and 7/9 will be the hardest to separate. One idea is to weight the distinctive regions more heavily than a plain binary template does, such as penalizing ink in a 0's center.

I'm considering adding explicit negative weights to the templates, so that each digit is penalized for ink in regions where its confusers, like 9, 0, and 8, tend to have it. The 4 template in particular should be negative in the upper-center loop area.

I'm weighing contrastive templates that push down ink where confusable digits tend to have it, like a strong negative in the 0's center or the lower-left for 7 and 9. Those tweaks would separate the pairs I'm stuck on, though I can't be sure they'll work blind. A safer step may be thickening the templates to match MNIST stroke width.

I'm thinking about switching to a contrastive template scheme, where explicit negative weights mark the regions a digit should avoid. The 0's center hole would be the first place to try it, and I'd keep the current templates in place so the change stays easy to compare.

I'm defining the 0 template with a negative-weighted hole in its center, since an empty center is what separates a 0 from an 8.

Continuing the template work, I'm sketching a contrastive version for digit 1 with negative weights on the side columns, so that ink away from the center stroke counts against it. That should separate 1 from digits that have ink on the sides, though it may also penalize some true 1s with slight slant.

I'm weighing whether to add anti-regions to the templates, which would be a sizable change given how little room is left. I'm leaning toward a moderate version, touching only the most confused pairs like 9→4 and 8→2, and I'll leave the 0 template alone since it's already performing fine.

I'm weighing whether to adjust the 4 template to penalize ink in its upper-left area, where the 9's loop sits, which would target the 9→4 confusion more directly. Still, lowering 4's bias further is the simpler lever, since 4 is over-predicted at about 1498 and that alone should cut the 9→4 errors.

I'm settling on a bias push for class 4 and a lift for class 7, since the mismatch with the 9→4 confusion looks mostly like over-predicting 4. I'm also considering a conservative template change, adding a negative hole to the 0 and thinning out the top flag on the 1, to see if the template side can add a little more separation.

I'm going to leave the templates alone for this step and just apply the balanced bias, then see where the confusions land. Once predictions are balanced, the remaining errors should reflect how good the templates really are, so I can target template fixes from there. I've been adjusting biases for three steps now, so I'll also try a template change this round: contrastive weights for the 0 and 1, and better separation for 4 versus 9. If it helps I'll keep it, and if not I'll revert.

Still working out the anti-region values for the 0 template, using a middle-strength negative in its center hole.

I'm sketching the 1 template as a clean central vertical, then reconsidering whether dropping the flag and base serifs would hurt recall on real 1s that have them.

Still writing the 1 and 4 templates...

Still writing the 4 template...

I'm checking whether 4's template has any ink in the left side of the 9's loop, since 9 has overlap with 4 almost everywhere else, so a negative there could separate them.

I'm checking where 9 and 4 overlap, and the diagonal and loop-left regions do intersect. The clearer difference is in the upper-right, where 9's loop sits a column further right than 4's diagonal, though that offset is small. I'm still looking for a region where 4 has ink and 9 does not.

Still working on the 4 template, now adding negative weights in the top-left cells to penalize the closed top loop that 9 has.

Still writing the 4 template...

Still writing the 4 template...

Still working out the anti-region for the 2 template, now adding negative weights on the lower-right cells where 8 has ink but the 2's diagonal does not.

Still writing the 2 template...

I'm wondering whether the 5s are landing on the 1 template because they are thin, since my new vertical 1 is so plain it might attract more of them. Removing the flag should at least cut back some of the top overlap. This is a lot to change at once, so I won't be able to tell which edit did what, but I'll go ahead since the feedback supports it. For 7, I'm looking at adding a negative weight in the bottom-left area that's empty for it but filled for 9 and 4.

Still writing the 7 template...

Still writing the 7 template...

Settling on the changes now: the 4 template gets negative weights at its top-left to penalize 9's closed loop, and the 2 template gets negative weights at its lower-right where 8 has ink. The 0 and 1 templates change shape too, so I'll leave 7 alone and just fix its bias to +0.18, then recalibrate the biases to match the new templates.

Shifting the biases to 0.70 for class 0, 0.65 for 2, 0.63 for 3, 0.85 for 5, 0.28 for 6, 0.25 for 7, and 0.10 for 9, with 1, 4, and 8 pushed negative, is a guess that depends on how the reshaped templates will respond. Since I'm changing several templates at once, I won't be able to tell which edit moved accuracy, so I'll have to judge the result as a whole.

Still writing the template values...

Still writing the template grids...

Still writing the 4 template...

Still writing the template values...

Still writing the template values...
