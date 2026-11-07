The accuracy is at 66.9% with loss at 1.10, and progress has stalled, so I need a bigger change rather than more small tweaks. A trained linear classifier on similar features would do much better, which points at my templates as the weak spot. I'm considering probing each feature group by changing its weights and watching how the loss moves, a finite-difference style estimate, though with only 42 steps and one scalar loss per step that budget is tight.

I'm weighing whether to probe individual feature groups with finite-difference-style weight changes, but with only 42 steps and a single scalar loss each time, that's a tight budget for coordinate descent on a few parameters. I'm also considering improving the templates so they better match the actual MNIST class mean images, and I'm recalling the rough layouts of each digit, like the ring of a 0 or the vertical bar of a 1.

I'm recalling the MNIST class mean layouts, but that mostly restates what my templates already do. The real question is why the loss stays high, and my guess is that the orientation features are noisy and the dilated ink makes the classes look alike. Features where every template is inked contribute roughly the same score to each class, so they add little discrimination, which suggests weighting by class-mean differences over variance instead.

I'm weighing whether negative evidence matters here: ink where a template doesn't expect it might separate 7 from 9, since 9 has ink on the left loop that a 7 lacks. With cosine scoring, a 7 that overlaps the 9 template's stem and loop top could still tip toward 9, so normalization has to carry that distinction. I suspect the key failure is in how asymmetric the templates are.

I'm considering whether to make the templates zero-mean per class, so that cells where a class usually has no ink get negative weights, and whether per-feature normalization should account for the fact that some feature channels are broader and fire more often than others.

I'm going to group the features into ink, tight orientation, wide orientation, and holes, normalize each group separately, and weight them with tunable factors. Tuning those group weights through feedback looks like the most promising route, and I'd tune the hole weight and the scale alongside them.

I'm weighing whether to score the ink, tight-orientation, and wide-orientation groups each with their own normalization and a tunable weight, starting with the ink group at half weight. The group magnitudes differ a lot, so ink would dominate the score unless I balance them.

Now I'm tallying the column sums for the bias update, working through the per-column totals.

Now I'm tallying the per-class column totals to recalibrate the biases, and 8 comes out well over the others, so its bias needs pulling down. I'm holding off on that update for now, though, since changing the group normalization would shift these totals anyway. I'd rather test a different group weighting first.

I'm going to try weighting the ink, tight-orientation, and wide-orientation groups separately, each at 2.5, so the total weight is higher than before and no single group dominates.

I'm moving the normalized weight toward the orientation groups, giving ink, tight, and wide each a 2.5 scale so that ink's larger magnitude no longer dominates the score.
