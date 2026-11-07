The gain has stalled at 41.75%, so I have five steps left. The largest leaks are still the 1→7, 9→4, and 8→2 transitions, along with several others, and these look like template-similarity problems that bias adjustments can't fix. I need a structural change to get a real improvement.

I'm weighing a structural change, since the confusions between 1/7, 9/4, 3/5 and 8/2 look like limits of linear templates on a coarse downsample. Using the conv layers for nonlinear edge features or raising the resolution are both possible, but designing either blind is risky with five steps left and a template risk already seen at step 8.

I'm trying to figure out why 1s get mistaken for 7s. The 7 template's horizontal top bar should help tell them apart, but since a 1 has no ink there, that region adds nothing against it. The diagonal of the 7 overlaps the vertical stroke of the 1, so 7 still wins, and I'm looking at how to strengthen the 1 template where it has ink and the 7 doesn't.

I'm checking where 1s and 7s differ in the upper-center area: the 1 has ink in column 5 for rows 2–4 while the 7 leaves it empty. The base serif at the bottom of the 1 is another point the 7 lacks.

I'm looking at the 1 template's base serif, which sits along the bottom row and separates it from the 7, and wondering whether leaning harder on that feature would help. Still, a structural fix here looks hard to get right. Maybe the safer move with the remaining steps is to accept roughly 42% and reduce the loss, if the metric rewards that.

I'm weighing whether a single targeted template change on the 9→4 pair is worth trying, since my earlier attempt to suppress 4 backfired. The plan is to test one refinement per step, starting with the 9, and revert if it doesn't help. Scaling the weights won't change the argmax by itself, though shifting the bias relative to the logits might, so that lever is messy and I'd rather leave it alone.

I'm looking at whether the 9 template can be made to win on 9s, since a 9 that scores higher as a 4 is the problem. The 9's closed top loop should be its distinguishing feature, but the template already has it, so I'm still working out what coarse-resolution difference separates the two.

I'm going to try a gentler version of the step 8 idea: a small negative weight only on the top-left of the 4 template, at row 1 columns 3 and 4, where the original had no ink. That should nudge 9s away from 4 without the damage I saw before. I'll keep all of the 4's existing positive ink, since removing it is what hurt last time.

I'm going to add a mild negative weight of -0.3 to the 4 template at the empty cells where a 9's upper-left loop sits: row 1 columns 3 and 4, row 2 columns 3 and 4, and row 3 column 3. Those cells are blank in the 4 but inked in a 9, so this should penalize 9s matching the 4 template without removing any of the 4's existing ink.

Writing the 4 template's row adjustments with a small negative value at the empty cells in the upper-left...

I'm bundling two small changes: a mild negative on the 4 template at row 1 column 3 and row 2 column 3 to push 9s away from it, and a similar gentle adjustment on the 2 template for the 8→2 leak.

I'm noticing that adding strong negatives to a template shrinks its positive weights after the unit-norm step, which is why the 2 and 4 recall dropped in the last attempt. Mild negatives of -0.3 should change the norm far less, so the adjustment is less likely to weaken the digits' own signal.

Still writing the 2 template adjustments...

Now I'm filling in the 2 template's lower-right cells with mild negative weights, where the 8's lower loop has ink and the 2 has none.

Still writing the 4 and 2 template changes...

Still writing the 4 template's row adjustments...

Still writing the 2 template rows...

Setting the 4 and 2 templates' mild negative weights into the code now, then shipping step 11.
