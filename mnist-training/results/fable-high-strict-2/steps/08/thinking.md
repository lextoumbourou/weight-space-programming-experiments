Accuracy got worse, down to 54%, with 6, 7 and 4 now over-predicted and 3 and 5 nearly dropping out. The equalization step stripped out the biases that 3 and 5 relied on, which suggests their templates match real examples poorly and will need large boosts. I'm now working out how to fix that.

I'm going back to step 6's config and applying a damped bias update from its digit counts, since that was the best run. The earlier equalization seems to have removed the biases that 3 and 5 needed, which points to their templates matching real digits poorly.

Now I'm checking the 3 and 5 templates against what real digits look like, comparing the arc positions and the junction point for the 3 template.

I'm checking the 5 template against typical 5s: a top bar, a left stroke down to the middle, then a bowl curving around the right side to the bottom. The points I've set look reasonable, so the weak match probably comes from how much real 5s and 3s vary in slant and in where the top bar sits.

I'm weighing whether wider orientation binning, around 45° instead of 30°, would help the curved 3s and 5s match more robustly to slanted real digits. The concern is that curved classes get weaker orientation responses than straight-stroked ones like 1, 4, and 7, so the normalization may be treating them unfairly.

I'm weighing whether to widen the orientation binning to about 40° to make the curved 3s and 5s more tolerant of slant, but I'd rather not add a second change on top of the damped bias update, since each swing has been costing a full step. Widening would scale all the orientation sums roughly uniformly, so the class balance should mostly hold, though straight-stroked digits could still shift a little.

I'm going with the widening to about 40°, since it should make the curved 3s and 5s more tolerant of slant, and I'll keep the hand negative on 4.
