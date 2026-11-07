The model has plateaued near 36% and five steps remain, so tweaking the bias isn't helping and I need a different signal. I'm going to look more carefully at what the features actually compute and whether the templates fit the effective 3x3 receptive field. I also want to confirm the template convention, with grid index (row, col) and row 0 at the top, which checks out.

Now I'm weighing whether diversifying channel weights by stroke group could break the plateau, since the earlier grouped attempts were muddied by the centering. Step 4's per-class zero-centering reached only 27% because its biases weren't calibrated, so I'm unsure whether prior-matching bias would lift it.

I'm weighing whether grouped templates with proper bias calibration can break the plateau, since 7 and 9 differ mainly by the top horizontal stroke and the diagonal. Per-class centering alone didn't fix the 8-dominance, and the prototype bias attempt had the same problem, so I'm looking for a way to remove the generic positive sum.

Working through whether activity scale decides which class the prototype matching favors, since a dense class like 8 could win just from its dot product with the feature map. Without any real activation data, I can't measure that scale, and the step-2 logits don't tell me anything about it. I'm leaning toward one more grouped attempt with per-class centering across all entries, since that's the option with the most upside in the remaining steps.

I'm checking whether a prior-matched bias correction could make the grouped templates work, since the earlier step's predictions were lopsided toward a few classes. Some of those counts look badly skewed, so the biases would need large adjustments. Given the five steps left, I'm weighing whether one more grouped attempt is worth it over keeping the 36% design.

I'm weighing whether grouped templates with per-class centering over every group and cell could finally move the model past the 36% plateau. The risk is that the generic positive sum I've been fighting still leaks through unless the biases get calibrated, so I'll need to set them deliberately rather than assume they balance out.

I'm checking step 4's 27% result against per-class centering across the grouped entries. Class 1 comes out with a small positive weight almost everywhere, which may be why it keeps winning.

I'm noticing that the neutral entries, set to a constant -0.3, turn positive for class 1 once each class is centered, which would explain why it keeps winning. My plan is to use zeros for uninformative entries and only ±1 where a stroke actually matters, so centering doesn't create a uniform offset per class.

I'm weighing whether zero-centering each class's template is principled, since with roughly uniform activity the generic term cancels out, but the centre cells carry more activity and could still favor one class. Without a reliable fix from reasoning alone, I'm leaning toward accepting the roughly 36% design and spending the remaining steps on modest bias tuning instead.

I'm going to try the grouped design once more, with neutral entries set to zero and each class centred across all its entries, and keep the biases at zero to start. If it does worse at step 11, I'll revert to the step-10 design at step 12.

I'm going to stick with the current design, since the grouped rewrite would probably land in the 30s and risk the final step. Instead I'll spend the remaining steps on bias tuning, aiming to lift class 6 and class 7 recall without losing overall accuracy.

Now I'm working out bias values that would balance the predicted class counts, since a more even spread across classes should roughly maximise accuracy. The current counts show a few columns taking far more predictions than others, so the corrections will need to be sizeable.

Now I'm tallying the prediction counts per column, and class 7 is getting 396 predictions even though only 145 of them are correct. Class 9 is the bigger outlier at 663 predicted, so the bias corrections will need to pull those columns down.

I'm adjusting the biases by the negative log of each class's predicted share, so the overpredicted columns come down and the underpredicted ones go up. The first few corrections are small, around -0.04 for classes 0 and 1, and I'm starting to work out the larger ones for classes 2 and 3.

Class 6 and class 7 are both getting pulled in the wrong direction by their current biases. I'm nudging class 6's bias up hard, since only 152 predictions went to it, but class 7 already soaks up 396 predictions, including ones from 1 and 8, so raising its bias could make things worse.

I'm going to leave class 7's bias at 2.5 for now, since its low count is mostly from 9 stealing its predictions rather than a shortage of raw score. Nudging 9 up would only make that pairwise confusion worse, so I'll hold 9 at 1.6 and push 7 up to 3.0 instead. Class 8 needs a small downward correction, which puts its bias around 1.57.

I'm settling on the final bias values: the overpredicted columns come down, the underpredicted ones go up, and class 9 stays at 1.6 so it doesn't feed more 7s into its column. I expect this to nudge accuracy into the high 30s, though the gains are incremental and the design looks close to its ceiling.

I'm keeping the code the same and only changing the biases, which is the step-11 calibration. The pairwise 7-to-9 confusion isn't something prior matching will fix, so I'm expecting only a small gain from this.
