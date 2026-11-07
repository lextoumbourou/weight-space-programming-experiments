Step 11: 44.1% accuracy, down slightly from 45.5% in step 10. The compromise on hole detector bias (-0.15 vs -0.2) and the template changes didn't help.

Let me compare steps 10 and 11:

Step 10 (conv1_b[7]=-0.2): 45.5% accuracy
Step 11 (conv1_b[7]=-0.15): 44.1% accuracy

The more aggressive hole suppression (-0.2) was BETTER overall. Let me go back to -0.2.

Step 10 per-class:
- 7: 49.6%, 8: 3.9%, 9: 6.7%
Step 11 per-class: class 7 fell to 39.9% from 49.6%, while 8 and 9 rose to 6.5% and 11.2%. The -0.15 bias helped the smaller classes but cost too much on 7, so the net result was worse. I'm now setting up step 10's configuration again, adjusting the biases from there.

I'm recomputing the bias for each class from step 10's predictions, starting with class 0, which works out to about 0.10. Class 1 is over-predicted at 1386, so I'm pulling its bias down to about -1.66. Classes 5, 6, and 9 are under-predicted, so their biases need to go up.

Working out the new per-class biases from step 10's predictions, I'm nudging class 7 down to about 0.01 and class 9 up to about 0.03. Next I'm setting the bias list together, starting with 0.10, -1.65, 0.90, 0.91, 0.47, 0.95, and 0.18.

Stepping back to step 10's setup for step 12: keeping conv1_b[7] at -0.2, the step 10 hole template scales, and the biases recalculated from step 10's predictions. The waist-focused h-stroke from step 11 reduced 8→7 confusions from 401 to 303 but pushed 8→2 up from 176 to 209, so I need to weigh whether it's worth keeping.

Going back to step 10's setup is the better move, since it was the strongest result so far. I'll rebuild it with the holes at the reduced scales, the earlier h-stroke, v-stroke, and boundary templates, and conv1_b[7] at -0.2, then apply the recalculated biases.

I'm comparing the step 10 and step 11 settings, looking at which parameters changed and which of them mattered.

Next I'm reviewing the settings I'd use for step 12: conv1_b[7] at -0.15, hole scales at 0.9, 0.4, 0.3, and so on, the waist-focused 8 h-stroke, and the updated bias list. The main change from step 10 is that conv1_b[7] and the hole scales differ.

I'm going back to -0.2 for conv1_b[7] and restoring step 10's hole scales, keeping the waist-focused 8 h-stroke and the updated biases from step 10's counts. Then I want to try improving the templates for the most-confused pairs (7→9, 8→7, 9→8) rather than just tuning biases.

Next I'm checking which confusions the hole-detector bias actually affects: 7→9 dropped from 479 to 302 at -0.2, but it's still the largest error for class 7. I'm also comparing the top-bar features, since a 7 should be positive across the wider top row while a 9's top loop sits narrower in the middle columns.

I'm checking how the digit 7 and 9 templates differ across the top row. Column 0 of row 0 sees the left part of the 7's bar, so it should carry moderate ink for a 7, while the narrower top loop of a 9 would leave that column mostly empty.

I'm weighing whether hand-designed 4×4 templates have hit their limit, so I'll focus on getting the biases right for step 12 and maybe try one small template change. I'm also considering a different approach for the last four steps, using purely positive templates without zero-mean centering and letting the biases handle the rest.

Next I'm weighing whether to try different conv2 channel configurations, but I'd rather not risk breaking what already works. I'll go back to step 10's exact setup and change only the biases, then compare what happened between steps 9 and 10.

I'm going back to step 10's setup with conv1_b[7] at -0.2, since step 10 had the better accuracy even with slightly higher loss. I'm keeping the waist-focused 8 h-stroke and building the new bias list from step 10's predictions.

Still writing the step 12 configuration...

Still writing the step 10 template parameters...

Writing the step 10 template parameters...
