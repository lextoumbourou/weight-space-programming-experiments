The score has only moved slightly, to 0.8613, and it's still hovering around 72.6%. Recall for class 8 remains stuck near 48–52%, and I'm seeing it mostly get confused with 9, 2, 1 and 6. The predicted totals for 8 come to about 870, which is below the true count, so the model is under-predicting it. I'm now going to look into why the 8 template is weak.

I'm reasoning that 8's template is spread thinly across many cells, so under cosine similarity partially drawn 8s lose out to 1 or 9. I'm considering a crossing detector that fires where the two diagonals meet at the center, since an 8 has that and a 9 usually doesn't.

I'm checking whether a crossing detector can pick up the 8 directly: both diagonals meeting at the center should respond strongly for an 8 and not for a 9, which only has one diagonal there. I'm planning to set one free channel to that tight center response, with a template weight of 1.0 for the 8.

I'm checking whether the crossing detector would also fire for other digits: a 2's top arc turns sharply enough to show both diagonals at one spot, and a 3's middle cusp could do the same at center. That could push 3 and 2 toward 8 and make the confusion worse.

I'm working out how to build the crossing feature from the diagonal orientation maps, taking the minimum of the two diagonal templates per cell so it fires only where both are present. I'll scale it so it responds only where the two orientations genuinely meet.

I'm setting the crossing channel's template to the overlap of the two diagonal orientations, and I'm also recomputing the per-column count totals for the step-23 bias update.

I'm working through the bias correction for each class from the step-23 column counts, comparing true totals to predicted ones and applying a damped log adjustment of about 0.8.
