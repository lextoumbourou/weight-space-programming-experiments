I'm at a plateau and need a bigger structural gain. The features are the likely bottleneck: only four orientation maps at 6x6, so a linear classifier could reach around 95% while templates top out near 85%. I'm also weighing another reduction in A, maybe down to 0.45 with gamma at 6, since the last cut helped alongside the biases. The main confusion is 3 being read as 5, 212 times.

I'm looking at the 3-versus-5 confusion and whether the top stroke of the 5 is what's pulling them together. My 3 template's top arc looks right to me, so the difference seems to be the 5's left vertical stroke. I'm also considering a broader orientation response, since a real detector probably responds partly to strokes 45° off rather than being zero there.

I'm thinking about broadening the orientation tuning so a stroke 45° off still gives a partial response, maybe squaring a softened cosine, and I'm also weighing a blur adjustment to the template spread. I plan to try that broader tuning together with A=0.45 and gamma 6 in this step, and I'm about to update the bias terms from the column sums.

I'm recomputing the bias terms column by column from the confusion counts, comparing each column total against the true class size. Columns 0 and 2 come out well under their true counts, so those biases need pulling up or down accordingly.

I'm recomputing the bias terms from the column totals, adding the log-ratio corrections for each digit. The sums show the classes that are over- or under-represented in the predictions, and the adjustments are starting to pull toward a different balance. Since changing the orientation tuning and A will shift these numbers, I suspect the accumulated bias values may be off.

I'm weighing a smaller reduction in A to 0.5 with gamma at 5.5, since the bias changes may have done most of the work, and I'd pair that with the broader orientation tuning.
