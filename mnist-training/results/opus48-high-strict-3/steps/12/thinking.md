Accuracy fell from 41.75% to 40.0%, so the mild anti-regions are still a net loss. Recall for class 2 dropped (591→362), and the 4-change pulled some misclassifications out of class 9 and 8 while class 9 and 8 recall still went up.

I'm reverting both anti-region changes, since the 2 change clearly hurt and the 4/9 pair ended up slightly worse overall. Going back to the step 10 state at 41.75%, then I'll try a few bias-only tweaks.

Going back to the step-10 config is the safe bet, since it's the best result so far at 41.75%. Any small bias tweak has been close to noise, so I'll restore that exact state for the final steps and only change things I'm confident will help.

I'm restoring the step 10 config, which is the best result at 41.75%, and I'll leave the bias values alone for the final steps.

I'm weighing whether any small, data-driven bias rebalance could help without the regressions I saw before. I'll restore the step-10 config first, then consider a very modest nudge toward the most lopsided columns.

Now I'm totaling the columns of the confusion matrix to see how the predictions are distributed across the classes.

Summing the column totals of the confusion matrix gives about 9986, roughly 10000. The distribution looks fairly even, with classes 5, 9, and 2 a bit high and class 8 a bit low, so I'm weighing whether that imbalance is worth touching.

I'm weighing whether any structural change could break the plateau, but I'll keep step 10's config as the fallback. If one experiment fails, I can restore it in the final step.

I'm going to keep the step-10 config as the safe fallback, and use step 12 to test an idea aimed at the 1↔7 confusion, which is the biggest remaining leak. My hunch is that the "1" template has too little ink compared with the "7," so I'm checking the ink counts.

I'm thinking the "1" template might need to be wider so slanted 1s still overlap it, since the diagonal ones currently fall to 7. The risk is that it would also pull in other digits, so I'll test it as an experiment and revert if it's worse.

I'm weighing whether the 1-versus-7 confusion can be fixed by reshaping either template, but widening the "1" would just pull in other digits, and thinning the "7" would cost recall I can't spare. Both moves trade one error for another. I'm leaning toward accepting the plateau and spending the remaining steps on a scale change, since with fixed biases a larger scale lets the raw correlations dominate the decision.

I'm settling on a scale-based adjustment over bias changes, since bias is already near-balanced and tweaks there tend to cause regressions. I'll restore the step-10 config at step 12 and hold it through the remaining steps.

I'm restoring the step-10 config exactly: the original templates with bias values [0.89, -0.17, 0.78, 0.63, -0.34, 0.92, 0.28, 0.25, -0.30, 0.09].
