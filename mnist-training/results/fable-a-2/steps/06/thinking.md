The loss improved to 1.09 and accuracy is at 64%, and the loci features are having some effect, with several pairs getting better. One pair, 4→9, got worse, and a few others are still stuck. The loci feature templates are still guesses, so I need to see what fires where before changing them. I have 45 steps to work with, so I'm weighing which probes would tell me the most.

I'm planning roughly 10 to 15 probe steps to map how the loci features behave across the problem classes before designing anything. One option is a position-resolved probe that shows where each class responds most strongly, though that only gives the top location. A more targeted idea is a pairwise probe for the confusing 4 vs 9 pair: propose a discriminating scalar, look at its histogram per class, and if it separates well, fold it into the FC layer as a rank-one correction.

I'm weighing a hand-fitted approach: measure class-conditional histograms of candidate scalar features and set the FC weights from those, much like naive Bayes log-likelihood ratios. It's close to hand-tuned regression, but the feedback is what drives it, and with 45 steps I'd need to keep enough budget for evaluating the actual classifier variants.

I'm considering a location-map approach instead: for each loci channel, treat the ten linear functionals as the argmax over spatial regions, so each class gets a distribution over where its feature peaks. That would take about one step per channel, roughly ten in total, and would show the spatial pattern per class without needing magnitudes.

I'm thinking about whether a location map would work better, where each channel's ten outputs point to the spatial region of its peak per class, though that would take a lot of steps. The largest confusions are 4→9, 2→3, and 5→3, so pairwise probes on those pairs look like the most efficient route.

I'm wondering whether any scalar in my feature set separates 4 from 9, with the DŪ response at top-centre as a candidate for the cup versus UD and the top horizontal line for the loop. I'd rather test those separately instead of combining them. A mini-classifier using only the loci features could also show how much discrimination that group provides on its own, per class.

I'm comparing the 4 and 9 loci templates and they look almost identical apart from the DŪ versus UD response at the top, so the loci features may not separate that pair well. I'm wondering whether a real 4's open cup top would make DŪ fire where the 9's loop would not, which would be the thing to check.

I'm checking whether the DŪ response at the top of a 4's cup would fire, and whether the loop's interior is tall enough for UD to fire on a 9. The 9's loop may be too small for the edges to register cleanly, which would make that case marginal. I can't settle it by reasoning alone, so I'll run direct probes on the 4/9 pair.

I'm weighing a probe that fits one scalar per step, such as DŪ at top-centre minus UD, and checking its class histograms for 4 versus 9. If the 4 and 9 means split clearly, I could set the FC weights from those means, though I'd still need steps left to evaluate the classifier.

I'm checking whether a single scalar like "DŪ at top-centre minus UD" could split 4 from 9, since the two loci templates differ mainly in that top response. I'm also looking for other features that might separate them, such as the upward-open ray from inside the cup, but I'm not certain how robust those would be.

I'm checking whether a DŪ response in the upper rows near the centre columns separates a 4's open cup from a 9's loop, since the 9's top stroke sits outside the valid range for that probe. I'd expect the 4 to fire there and the 9 not to, so I'll test a scalar summing DŪ over those cells.

I'm checking whether the 6's top curve or the 0's inner top would trigger the same up-ray test, and I'm leaning toward a direct test of the 4/9 weights in the classifier instead of a histogram probe first, since that would show the effect on the confusion directly even if it wouldn't explain why.

I'm thinking about using a two-feature probe with coarse bins, maybe five levels for one scalar and a binary threshold for the other, so each step gives a joint picture rather than a single histogram. The open question is where to set the thresholds, since I don't yet know the magnitude scale of these features.

I'm thinking a single scalar with ten bins will give the magnitude calibration I need first, and I can move to a coarser three-by-three grid later. Before that, I want to see whether the 2 vs 3 pair separates on the bottom-right cells, where a 3's lower bowl and a 2's base should respond differently.

I'm checking whether the 3's lower bowl would block the DŪ response that a 2's base would trigger on the right side, so a bottom-right probe might separate them. I'm also considering a difference between upper-left and upper-centre responses for 5 versus 3, and wondering why some 0s get classified as 6, possibly from slanted or narrow strokes.

I'm weighing probes that sum each loci channel over spatial regions, like the top rows against the bottom, or the left columns against the right, so I can test whether those sums separate the confused pairs. The idea is to use a region-level scalar per class instead of a full argmax map, which would give more direct evidence per step.

I'm weighing a single scalar with around ten bins, with thresholds spanning low to high response values, against a coarser two-scalar grid. The response ranges for the loci features are still uncertain, so the bins might not line up well with the actual magnitudes.

I'm weighing whether to probe the 4/9 pair with a joint 3×3 grid over the top-centre DŪ and UD responses, since separating presence from absence there seems more useful than a single difference scalar. Thresholds near 0.1 and 0.9 should capture whether each response is absent, weak, or strong.

I'm settling on a joint probe with a 3×3 grid over two features, giving nine outcomes with the tenth class slot left unused. The idea is to keep the per-step information richer than a single histogram while still being able to set weights for each class from the results.

I'm listing the feature scalars I want to check across all classes: the top-centre DŪ and UD responses for the 4/9 and 8 cases, the bottom DŪ for 2 versus 3, and the right- and left-side LR̄ and RL̄ responses for 3, 5, 6 and 7.

I'm settling on a set of roughly ten scalars to probe, and I'd rather measure them in 3×3 joint grids across about five steps than spend the budget on one-at-a-time histograms. Then I can build a rule-based layer on top of the loci and orientation templates. I'm also weighing whether four binary scalars per step, giving 16 outcomes, would carry more information than the 3×3 grid, though thresholding binary features is harder to calibrate.

I'm settling on the first probe as a ternary grid over two features, DŪ and UD in the top-centre region, to learn the magnitude scale before committing to binary triples later.

I'm setting the first probe's bin thresholds: 0.15 and 1.0 for the top-centre DŪ response, 0.15 and 0.8 for the UD one. Next I'll rebuild the fully connected layer from those bins, with a dead ninth output, and keep the same conv layers as the last step.
