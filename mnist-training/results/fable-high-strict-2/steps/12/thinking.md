The model has hit a plateau at 59.6% accuracy, and bias adjustments are only shifting errors between classes. With four steps left, I need a structural change that's low-risk, or else I should accept the current result and fine-tune. The biggest confusions are 7→9, 8→2, and 3→5.

Tracing the 7→9 confusion, the bias numbers don't add up: raising 7's bias should have helped, not hurt. The cause looks like two negative ink points I added in an earlier step, which seem to be penalizing a 7's own top bar in the second grid rather than real non-7 digits. I'll drop those points and then look for a larger structural fix to the plateau.

I'm considering a lower-risk structural change: shrinking the ink-detection box to just the center pixel so the emptiness cells stop picking up neighboring strokes. That would sharpen the features but could cost some tolerance, so I'm weighing it against simply tuning the biases.

I'm weighing whether 8→2 comes from 8s with a narrow left side: a 2 template penalizes the left-middle cells, so the penalty only bites if the 8's left stroke is far enough inside the cell region, which would make the penalty small per cell.

I'm reasoning about why narrow 8s get misclassified as 2s: the emptiness cells pick up the stroke near the edge of the box, so the 8 loses points on its own template. Because a 2 template fits inside that narrow shape, I'm considering making the 8's ellipses less tall, around ry 1.3 instead of 1.5, so the template tolerates width variation.

Reconsidering the 8 template's ry at 1.3 instead of 1.5 would spread the side cells so narrow and wide 8s both earn partial credit, and it would cut the number of expected-empty cells that penalize 8s. Still, the exact geometry is hard to settle without running it, so I'm not yet sure that's the right fix.

I'm weighing whether to try a symmetric-confusion fix for the 4/9, 2/8, and 3/5 pairs, since those errors run in both directions. The 7→9 confusion is lopsided, so it may need a different treatment than the rest.

I'm noticing the remaining confusions split into two kinds: the symmetric ones (like 6↔9 and 5↔6) mean the features themselves aren't separating those digits, so bias tweaks won't fix them. The asymmetric ones, such as 7→9 and 1→2, are the ones bias adjustments could help. I'm checking the per-class totals to see where a downward bias on 9 might be justified, though that could push up 9→4. For now I'm leaving the damped bias change at zero.

I'm working out bias corrections from the class counts, and the 7 and 8 classes look like they need a boost. I also plan to widen the template's tolerance ramp so cells stay partially credited out to about 1.1, which might help the narrow 8s and the 7s.

Weighing whether to swap in a bolder structural change now, since I only have a few steps left. I'm also considering a 7 vs 9 distinction based on 9's closed loop on the left side, though I haven't settled whether that's worth pursuing given the remaining budget.

Narrow 9s would sit too far right for the left-side ink box to catch their loop, so the usual cues stop working. Then the only things separating a 7 from a narrow 9 are the horizontal at the loop bottom and the diagonal orientation, which are weak signals. The column placement of the grid cells looks like the underlying issue across several digits.

I'm wondering whether finer horizontal sampling would help, since narrow digits only register in about two columns right now. One option is to give some conv2 channels a different horizontal offset, though that might lose the vertical shift that helped with position.

I'm weighing a sharper ink feature, like a horizontal left-minus-right edge detector, but that feels too speculative with four steps left. A simpler option is to drop the coarse 5x5 box idea and stick with the plan: remove the bad negatives on 7 and then adjust the biases.

I'm dropping the widened-tolerance idea, since it could add penalties as easily as it removes them, and I'm keeping the structure as is. The plan is to fix the 7's bad negatives and make the bias changes: a +0.5 boost for 7, a small decrease for 9, a boost for 8, and a slight decrease for 2, while leaving 6 alone.

I'm settling on the bias values for each digit: 0 gets +1.48, 1 gets -0.86, 2 gets 0.40, 3 gets 1.33, 4 gets 0.21, 5 gets 1.89, 6 stays at 0.05, 7 gets 0.14, 8 gets 0.96, and 9 gets 0.26.
